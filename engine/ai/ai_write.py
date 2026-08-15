"""Article writer: DAILY_RUN.md Step 5, run by `llm.model_writer` (with
`llm.model_writer_fallbacks`). One generate_with_fallback() call off the
brief + research pack + source pool + recent history, with up to 2 bounded
re-asks (FIX J, raised from 1) if the model's front matter doesn't parse
or is missing required fields.

Contract (SPEC.md, Agent B):
    run(date_ist, client, cfg, retry_feedback: str|None = None,
        reuse_slug: str|None = None) -> path

The model is told NOT to invent the `date`/`slug` front-matter values —
prompts/v1/write_article.md has it write literal placeholder tokens
(`{{ARTICLE_DATE}}` / `{{ARTICLE_SLUG}}`, quoted) that this module
substitutes only *after* validating the draft and computing the real slug
from the model's own title — exactly the order a human writer would
follow (draft first, permanent URL decided from the title, not invented
up front). `reuse_slug` overrides that title-derived slug: pass the prior
attempt's slug on a retry (writer_cli.py's shared retry loop does this) so
the corrected draft overwrites the SAME `content/articles/<date>-<slug>.md`
in place instead of minting a second, orphaned slug from a retry draft's
(possibly reworded) title.

review.* flag ownership is split, matching who can actually vouch for
each: the writer self-asserts `title_promise_check`, `no_fabrication`,
and `policy_pass` as `true` in its own draft (it is the author — see
prompts/v1/write_article.md's title/body rules for what each promise
means); `facts_verified` and `sources_checked` must stay `false` in the
draft — only the citation gate, which independently re-verifies every
source, is allowed to flip those two (engine/ai/citation_gate.py). This
split exists so a fresh draft doesn't hard-fail engine/gates.py's G08
(needs title_promise_check) and G11 (needs the whole review block) before
the citation gate ever gets a chance to run — see writer_cli.py's
write -> citation_gate -> build -> gate ordering.

Deviations from SPEC.md's literal text (kept minimal, called out per the
task brief):
  * `run()` takes an optional trailing `root: Path = ROOT` kwarg, same
    testability pattern as ai_select.py/ai_research.py.
  * `cfg` is the FULL config.yaml dict; `cfg["llm"]` is read internally —
    matches how engine/ai/writer_cli.py (Agent D) actually calls this
    module.
  * The bounded re-ask is hardcoded to exactly `_PARSE_REASK_ATTEMPTS - 1`
    = 2 retries (3 total generate_with_fallback() calls, FIX J) for
    front-matter *structural* validity, independent of
    `llm.max_retry_rewrites` (that config caps writer_cli.py's outer
    gate-failure retry loop, a different, higher-level retry around this
    whole function — see writer_cli.py's docstring). FIX J also made
    extraction itself lenient (fence-unwrap trying every fence, then a
    bare '---'-anywhere-in-the-output search, then a trailing-fence
    strip) — live smoke runs showed the model occasionally wraps the
    document in a code fence or prefaces it with commentary with no
    token-truncation involved, so paying for a whole re-ask over pure
    formatting was wasteful; the re-ask budget still exists for the
    genuine structural failures lenient extraction can't route around.
  * Recent-history / existing-slug lookups are implemented locally
    against `root` (`_load_history`/`_existing_article_slugs` below)
    instead of calling `engine.util.load_history()`/`all_articles()` —
    those are hardcoded to the real repo ROOT with no root/path
    parameter, and engine/util.py is out of this section's scope to
    modify. The local versions read the same on-disk shapes, so
    production behavior (root=None -> real ROOT) is identical; the only
    difference is tests can now fully isolate this module against a
    tmp_path tree instead of hitting the real data/history.json.
  * `reuse_slug` (new): if not passed explicitly but `retry_feedback` is,
    this module falls back to reading `data/run-state/<date_ist>.json`'s
    `slug` field (writer_cli.py's FIX-2 run-state file) — so a bare
    `ai_write.run(..., retry_feedback=...)` call still reuses the right
    slug even if the caller didn't wire the explicit kwarg through.
  * Grounding-redirect resolution (new, engine/ai/resolve_links.py):
    right before writing the final draft to disk, every
    `vertexaisearch.cloud.google.com/grounding-api-redirect/...` url in
    the resolved article text (front-matter `sources[]` and inline body
    links alike — the writer copies these in from the research sources
    pool, which is grounded via `googleSearch`) is resolved to its real
    final url and substituted in place, so citation_gate verifies (and
    the site eventually publishes) a stable real url, not an opaque
    token that expires in ~a month. Failures to resolve are fail-open —
    the original redirect url is left in place and reported in a
    `data/gate-reports/<date>-<slug>-link-warnings.json` side file that
    writer_cli.py folds into run-state; they never raise or block the run.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

from ..util import ROOT, slugify
from .resolve_links import GROUNDING_REDIRECT_RE, resolve_grounding_links

_PROMPTS = Path(__file__).resolve().parent.parent.parent / "prompts" / "v1"
PROMPT_PATH = _PROMPTS / "write_article.md"
STYLE_PATH = _PROMPTS / "_style.md"

FENCE_RE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
ARTICLE_FNAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")
# FIX J: scans EVERY fenced block (not just the first) so a stray
# illustrative fence earlier in a chatty reply doesn't win over the real
# document in a later fence.
_FENCE_ALL_RE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
# The first '---'-starting line anywhere in the raw output, capturing from
# there to the end of the string — lets a bare (unfenced) document survive
# leading commentary ("Here's the article:\n\n---\ntitle: ...").
_BARE_FM_START_RE = re.compile(r"(?:^|\n)(---[ \t]*\n.*)", re.DOTALL)
# Inline citation = a markdown link whose target is an http(s) url — same
# pattern citation_gate.py uses for the same purpose.
_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
# A draft only has to prove deep-link fidelity when the research pack
# actually offered enough real sources to cite — with fewer than this,
# rejecting every draft for citing "the best it had" would be punitive,
# not a quality bar.
_MIN_SOURCES_FOR_FIDELITY_CHECK = 3

# FIX J: 1 initial attempt + 2 bounded re-asks for front-matter *structural*
# validity (parse/YAML/citation-fidelity failures) — bumped from 1 retry.
# A parse flake (stray fence, chatty preamble) is cheap to re-ask for
# against a whole ~$1 run; two corrective rounds converges reliably.
_PARSE_REASK_ATTEMPTS = 3

# Literal tokens the model must echo back verbatim (quoted) in its draft's
# front matter; this module fills them in only after the draft validates
# and the real slug is computed from the model's own title.
DATE_TOKEN = "{{ARTICLE_DATE}}"
SLUG_TOKEN = "{{ARTICLE_SLUG}}"

REQUIRED_STR_FIELDS = ["title", "slug", "date", "hub", "description",
                       "hero_alt", "keyword", "original_value"]
REQUIRED_LIST_FIELDS = ["tags", "sources", "faq"]

# review.* flag ownership is split (FIX A): the writer self-asserts the
# three it can actually vouch for as the author; the citation gate is the
# only thing allowed to flip the other two, so they must stay false here.
REVIEW_SELF_ASSERT_KEYS = ["title_promise_check", "no_fabrication", "policy_pass"]
REVIEW_GATE_KEYS = ["facts_verified", "sources_checked"]
REVIEW_BOOL_KEYS = REVIEW_GATE_KEYS + REVIEW_SELF_ASSERT_KEYS  # full set, order matches SPEC.md


class WriteValidationError(RuntimeError):
    """The model failed to produce structurally valid front matter even
    after the bounded re-asks (_PARSE_REASK_ATTEMPTS)."""


def _strip_trailing_fence(text: str) -> str:
    """Strip a stray trailing ``` a model sometimes leaves dangling —
    e.g. when strategy 2 below grabs "everything from the opening ---
    onward" and that opening --- happened to be inside a fence, its
    closing fence comes along for the ride. (FIX J, step 3)."""
    stripped = text.rstrip()
    if stripped.endswith("```"):
        stripped = stripped[:-3].rstrip()
    return stripped


def _extract_article(text: str) -> str:
    """Lenient article extraction (FIX J). Live smoke runs showed the
    model occasionally wraps the document in a code fence, prefaces it
    with commentary, or both — with token counts showing no truncation,
    this is a formatting flake, not a content failure, and shouldn't burn
    a whole re-ask/rewrite cycle. Tries, in order:

      1. Any fenced code block (``` / ```markdown / ```yaml / ```md —
         FENCE_RE's `[a-zA-Z]*` language tag already covers all of
         these) whose content is a genuine '---front matter---\\nbody'
         document once unwrapped. Multiple fences are checked in order;
         the first one that's actually the document wins, not just the
         first fence at all (which might be an illustrative snippet in
         some preamble).
      2. Failing that, the first '---'-starting line anywhere in the RAW
         output (inside or outside a fence — commentary before it is
         simply discarded), taken through to the end of the output.
      3. Either candidate has a stray trailing ``` stripped.

    Only if NEITHER strategy yields a document starting with '---' does
    this fall back to the old best-effort behavior (first fence unwrapped,
    else the raw text) — which the caller's FM_RE.match() check will then
    correctly reject, triggering the existing corrective re-ask path."""
    text = text or ""

    for fence_match in _FENCE_ALL_RE.finditer(text):
        candidate = _strip_trailing_fence(fence_match.group(1).strip())
        if FM_RE.match(candidate):
            return candidate

    bare_match = _BARE_FM_START_RE.search(text)
    if bare_match:
        candidate = _strip_trailing_fence(bare_match.group(1).strip())
        if FM_RE.match(candidate):
            return candidate

    first_fence = FENCE_RE.search(text)
    return _strip_trailing_fence((first_fence.group(1) if first_fence else text).strip())


def _validate(meta: dict) -> list[str]:
    errs = []
    if not isinstance(meta, dict):
        return ["front matter did not parse to a mapping"]
    for k in REQUIRED_STR_FIELDS:
        if not str(meta.get(k, "")).strip():
            errs.append(f"missing/empty front-matter field: {k}")
    for k in REQUIRED_LIST_FIELDS:
        v = meta.get(k)
        if not isinstance(v, list) or not v:
            errs.append(f"missing/empty front-matter list: {k}")
    rev = meta.get("review")
    if not isinstance(rev, dict):
        errs.append("missing front-matter 'review' block")
    else:
        for k in REVIEW_GATE_KEYS:
            if rev.get(k) is not False:
                errs.append(f"review.{k} must be false in the draft "
                           "(the citation gate flips it after verifying)")
        for k in REVIEW_SELF_ASSERT_KEYS:
            if rev.get(k) is not True:
                errs.append(f"review.{k} must be true in the draft "
                           "(the writer self-certifies this — see the prompt)")
        if not str(rev.get("reviewed_at", "")).strip():
            errs.append("review.reviewed_at missing")
    return errs


def _bad_citation_url_reason(url: str) -> str | None:
    """None if `url` is an acceptable citation; otherwise a short reason
    it isn't (FIX H: deep-link fidelity)."""
    if GROUNDING_REDIRECT_RE.search(url):
        return "a vertexaisearch grounding-redirect url, not a resolved deep link"
    if urlparse(url).path in ("", "/"):
        return "a bare domain root, not a specific article/page"
    return None


def _citation_fidelity_errors(meta: dict, body: str, sources_available: int) -> list[str]:
    """FIX H: reject a draft that cites a bare domain homepage or an
    unresolved vertexaisearch redirect instead of copying a real url
    verbatim from the research source pool — but only once that pool
    actually offered enough real sources to hold the draft to that bar
    (see _MIN_SOURCES_FOR_FIDELITY_CHECK)."""
    if sources_available < _MIN_SOURCES_FOR_FIDELITY_CHECK:
        return []
    errs: list[str] = []
    seen: set[str] = set()
    for src in (meta.get("sources") or []):
        url = src.get("url") if isinstance(src, dict) else None
        if not url or url in seen:
            continue
        seen.add(url)
        reason = _bad_citation_url_reason(url)
        if reason:
            errs.append(f"front-matter sources[] url '{url}' is {reason} — "
                       "copy a url VERBATIM from the numbered research "
                       "sources list instead")
    for _anchor, url in _LINK_RE.findall(body):
        if url in seen:
            continue
        seen.add(url)
        reason = _bad_citation_url_reason(url)
        if reason:
            errs.append(f"inline body link to '{url}' is {reason} — "
                       "copy a url VERBATIM from the numbered research "
                       "sources list instead")
    return errs


def _load_history(root: Path) -> dict:
    p = root / "data" / "history.json"
    if not p.exists():
        return {"published": []}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"published": []}


def _existing_article_slugs(root: Path) -> set[str]:
    slugs = set()
    d = root / "content" / "articles"
    if d.exists():
        for p in d.glob("*.md"):
            m = ARTICLE_FNAME_RE.match(p.stem)
            if m:
                slugs.add(m.group(1))
    return slugs


def _recent_history_lines(root: Path, n: int = 10) -> str:
    hist = _load_history(root)
    recent = (hist.get("published") or [])[-n:]
    if not recent:
        return "- (no published history yet — first article(s), relax internal-link expectations)"
    return "\n".join(f"- {p.get('date')} [{p.get('hub')}] {p.get('title')} "
                     f"(/articles/{p.get('slug')}/)" for p in reversed(recent))


def _existing_slugs(root: Path) -> set[str]:
    hist = _load_history(root)
    slugs = {p["slug"] for p in (hist.get("published") or []) if p.get("slug")}
    slugs |= _existing_article_slugs(root)
    return slugs


def _reuse_slug_from_run_state(root: Path, date_ist: str) -> str | None:
    """Fallback source for `reuse_slug` when a caller passes
    retry_feedback but not the slug explicitly — reads writer_cli's FIX-2
    run-state file. Never raises; missing/unreadable -> None (caller falls
    back to normal title-derived slug generation)."""
    p = root / "data" / "run-state" / f"{date_ist}.json"
    if not p.exists():
        return None
    try:
        state = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return state.get("slug") or None


def _dedupe_slug(base: str, existing: set[str]) -> str:
    base = base or "article"
    if base not in existing:
        return base
    i = 2
    while f"{base}-{i}" in existing:
        i += 1
    return f"{base}-{i}"


def _build_prompt(date_ist: str, brief_text: str, research_text: str,
                  sources: list, recent_lines: str, style: str,
                  retry_feedback: str | None, validation_errors: list | None) -> str:
    tmpl = PROMPT_PATH.read_text(encoding="utf-8")
    msg = (tmpl.replace("{{style}}", style)
                .replace("{{today_ist}}", date_ist)
                .replace("{{brief}}", brief_text)
                .replace("{{research_notes}}", research_text)
                .replace("{{sources_json}}", json.dumps(sources, indent=2, ensure_ascii=False))
                .replace("{{recent_articles}}", recent_lines))
    if retry_feedback:
        msg += ("\n\n## Gate-failure feedback from a previous attempt — fix these\n"
               f"{retry_feedback}\n")
    if validation_errors:
        msg += ("\n\n## Your previous draft's front matter did not validate — "
               "fix exactly this and resend the COMPLETE article\n"
               + "\n".join(f"- {e}" for e in validation_errors) + "\n")
    return msg


def run(date_ist: str, client, cfg: dict, retry_feedback: str | None = None,
        root: Path | None = None, reuse_slug: str | None = None) -> Path:
    root = root or ROOT
    if retry_feedback and not reuse_slug:
        reuse_slug = _reuse_slug_from_run_state(root, date_ist)
    briefs_dir = root / "data" / "briefs"
    brief_path = briefs_dir / f"{date_ist}.md"
    if not brief_path.exists():
        raise SystemExit(f"no brief at {brief_path} — run `engine.run brief` first")
    brief_text = brief_path.read_text(encoding="utf-8")

    research_path = briefs_dir / f"{date_ist}-research.md"
    research_text = (research_path.read_text(encoding="utf-8") if research_path.exists()
                     else "(no research notes on disk — research step did not run or found nothing)")
    sources_path = briefs_dir / f"{date_ist}-sources.json"
    sources = json.loads(sources_path.read_text(encoding="utf-8")) if sources_path.exists() else []

    style = STYLE_PATH.read_text(encoding="utf-8") if STYLE_PATH.exists() else ""
    recent_lines = _recent_history_lines(root)

    llm_cfg = cfg.get("llm", cfg)
    models = [llm_cfg["model_writer"], *llm_cfg.get("model_writer_fallbacks", [])]

    validation_errors: list | None = None
    for attempt in range(_PARSE_REASK_ATTEMPTS):
        user_msg = _build_prompt(
            date_ist, brief_text, research_text, sources, recent_lines, style,
            retry_feedback if attempt == 0 else None, validation_errors)
        res = client.generate_with_fallback(
            "write", models,
            contents=[{"role": "user", "parts": [{"text": user_msg}]}],
            thinking=llm_cfg.get("writer_thinking"),
            max_output=int(llm_cfg.get("writer_max_output", 8192)),
            temperature=0.7,
        )
        article_text = _extract_article(res.text or "")
        m = FM_RE.match(article_text)
        if not m:
            # FIX J: explicit, directive corrective feedback — lenient
            # extraction (fence-unwrap, bare-'---'-search) already tried
            # and failed, so this is a real formatting miss, not a flake
            # extraction couldn't route around.
            validation_errors = [
                "output was not a valid '---front matter---\\nbody' document "
                "even after lenient extraction (fence-unwrap / bare '---' "
                "search both failed) — your ENTIRE reply must START with "
                "'---' as its very first three characters: no code fence, "
                "no ```markdown wrapper, no preamble or commentary before "
                "or after it, nothing but the front matter + body"
            ]
            continue
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            validation_errors = [f"front matter is not valid YAML: {e}"]
            continue
        errs = _validate(meta)
        if not errs:
            errs = _citation_fidelity_errors(meta, m.group(2), len(sources))
        if errs:
            validation_errors = errs
            continue

        # Valid draft — resolve the literal placeholder tokens now that we
        # have the model's real title to derive a slug from. On a retry
        # (reuse_slug set), REUSE the prior attempt's slug instead of
        # deriving a fresh one from this draft's (possibly reworded)
        # title — otherwise a retry can mint a second, orphaned slug for
        # what is supposed to be the same article (FIX D).
        if reuse_slug:
            slug = reuse_slug
        else:
            slug_base = slugify(str(meta.get("title", "")))
            slug = _dedupe_slug(slug_base, _existing_slugs(root))
        final_text = article_text.replace(DATE_TOKEN, date_ist).replace(SLUG_TOKEN, slug)

        # Resolve any Vertex AI Search grounding-redirect urls (opaque,
        # expire in ~a month) to their real final url before anything else
        # ever sees this draft (FIX E) — fail-open: unresolved urls are
        # left as-is and reported to a side file, never block the write.
        final_text, link_warnings = resolve_grounding_links(final_text)
        if link_warnings:
            warn_dir = root / "data" / "gate-reports"
            warn_dir.mkdir(parents=True, exist_ok=True)
            (warn_dir / f"{date_ist}-{slug}-link-warnings.json").write_text(
                json.dumps(link_warnings, indent=2, ensure_ascii=False),
                encoding="utf-8")

        out_dir = root / "content" / "articles"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{date_ist}-{slug}.md"
        out_path.write_text(final_text, encoding="utf-8")
        return out_path

    raise WriteValidationError(
        f"ai_write: model failed to produce valid front matter after "
        f"{_PARSE_REASK_ATTEMPTS - 1} retries: "
        + "; ".join(validation_errors or ["unknown validation failure"]))

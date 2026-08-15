"""Article writer: DAILY_RUN.md Step 5, run by `llm.model_writer` (with
`llm.model_writer_fallbacks`). One generate_with_fallback() call off the
brief + research pack + source pool + recent history, with a single
bounded re-ask if the model's front matter doesn't parse or is missing
required fields.

Contract (SPEC.md, Agent B):
    run(date_ist, client, cfg, retry_feedback: str|None = None) -> path

The model is told NOT to invent the `date`/`slug` front-matter values or
flip any `review.*` flag to true — prompts/v1/write_article.md has it
write literal placeholder tokens (`{{ARTICLE_DATE}}` / `{{ARTICLE_SLUG}}`,
quoted) that this module substitutes only *after* validating the draft and
computing the real slug from the model's own title — exactly the order a
human writer would follow (draft first, permanent URL decided from the
title, not invented up front).

Deviations from SPEC.md's literal text (kept minimal, called out per the
task brief):
  * `run()` takes an optional trailing `root: Path = ROOT` kwarg, same
    testability pattern as ai_select.py/ai_research.py.
  * `cfg` is the FULL config.yaml dict; `cfg["llm"]` is read internally —
    matches how engine/ai/writer_cli.py (Agent D) actually calls this
    module.
  * The one bounded re-ask is hardcoded to exactly one retry (two total
    generate_with_fallback() calls) for front-matter *structural*
    validity, independent of `llm.max_retry_rewrites` (that config caps
    writer_cli.py's outer gate-failure retry loop, a different, higher-
    level retry around this whole function — see writer_cli.py's
    docstring).
  * Recent-history / existing-slug lookups are implemented locally
    against `root` (`_load_history`/`_existing_article_slugs` below)
    instead of calling `engine.util.load_history()`/`all_articles()` —
    those are hardcoded to the real repo ROOT with no root/path
    parameter, and engine/util.py is out of this section's scope to
    modify. The local versions read the same on-disk shapes, so
    production behavior (root=None -> real ROOT) is identical; the only
    difference is tests can now fully isolate this module against a
    tmp_path tree instead of hitting the real data/history.json.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from ..util import ROOT, slugify

_PROMPTS = Path(__file__).resolve().parent.parent.parent / "prompts" / "v1"
PROMPT_PATH = _PROMPTS / "write_article.md"
STYLE_PATH = _PROMPTS / "_style.md"

FENCE_RE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
ARTICLE_FNAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")

# Literal tokens the model must echo back verbatim (quoted) in its draft's
# front matter; this module fills them in only after the draft validates
# and the real slug is computed from the model's own title.
DATE_TOKEN = "{{ARTICLE_DATE}}"
SLUG_TOKEN = "{{ARTICLE_SLUG}}"

REQUIRED_STR_FIELDS = ["title", "slug", "date", "hub", "description",
                       "hero_alt", "keyword", "original_value"]
REQUIRED_LIST_FIELDS = ["tags", "sources", "faq"]
REVIEW_BOOL_KEYS = ["facts_verified", "sources_checked", "title_promise_check",
                    "no_fabrication", "policy_pass"]


class WriteValidationError(RuntimeError):
    """The model failed to produce structurally valid front matter even
    after the one bounded re-ask."""


def _extract_article(text: str) -> str:
    m = FENCE_RE.search(text)
    return (m.group(1) if m else text).strip()


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
        for k in REVIEW_BOOL_KEYS:
            if rev.get(k) is not False:
                errs.append(f"review.{k} must be false in the draft "
                           "(the citation gate flips it after verifying)")
        if not str(rev.get("reviewed_at", "")).strip():
            errs.append("review.reviewed_at missing")
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
        root: Path | None = None) -> Path:
    root = root or ROOT
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
    for attempt in range(2):  # exactly one bounded re-ask
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
            validation_errors = ["output was not a valid '---front matter---\\nbody' document"]
            continue
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            validation_errors = [f"front matter is not valid YAML: {e}"]
            continue
        errs = _validate(meta)
        if errs:
            validation_errors = errs
            continue

        # Valid draft — resolve the literal placeholder tokens now that we
        # have the model's real title to derive a slug from.
        slug_base = slugify(str(meta.get("title", "")))
        slug = _dedupe_slug(slug_base, _existing_slugs(root))
        final_text = article_text.replace(DATE_TOKEN, date_ist).replace(SLUG_TOKEN, slug)

        out_dir = root / "content" / "articles"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{date_ist}-{slug}.md"
        out_path.write_text(final_text, encoding="utf-8")
        return out_path

    raise WriteValidationError(
        "ai_write: model failed to produce valid front matter after 1 retry: "
        + "; ".join(validation_errors or ["unknown validation failure"]))

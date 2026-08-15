"""Citation gate — fail-closed verification that every source an article
cites actually supports the claim it's attached to.

Contract (SPEC.md, Agent C):
    run(date_ist, slug, client, cfg) -> (passed: bool, report: dict)

For each front-matter `sources[]` url, one `urlContext` fetch+check model
call (model_fast, prompts/v1/citation_check.md) returns a JSON verdict
`{supported: bool, quote: str, fetch_ok: bool, reason: str}` for the
claim the article body ties to that url — the full SENTENCE containing an
inline markdown link `[anchor text](url)` whose target matches the source
url (FIX G — NOT the link's anchor text, which is a label, not a claim;
"Google Official Blog" is not something a page can "support"). A source
never linked inline falls back to the article's own description + that
url's title in the research source pool (`data/briefs/<date>-sources.json`,
if present); if neither exists, the source is never sent a fabricated
claim — it's marked `needs_corroboration` instead (Rule 3 below).

FIX F (hard fact from a live smoke run): Vertex rejects controlled
generation (`responseSchema`) combined with the `urlContext` tool — HTTP
400 "controlled generation is not supported with URL Context tool". The
check call below therefore passes NO `json_schema`; the prompt demands raw
JSON instead, and `_parse_verdict`/`_extract_json_object` parse that
leniently (first balanced `{...}` block, string-quote aware) rather than
trusting a schema-enforced shape. `GeminiClient.generate()` itself now also
raises `ValueError` if json_schema + a urlContext/googleSearch tool are
ever passed together, so this class of 400 can't ship again from any
call site.

FIX I: an individual source's check that ends in an ERROR outcome (a call
exception, an HTTP error, or an unparseable model reply) is retried ONCE
— a fresh `generate()` call, the exact same prompt — before its
fail-closed verdict is recorded (`_check_one_source_with_retry`, tagged
with ledger note `retry` on the second attempt). This is flake tolerance,
not a second chance at the editorial call: a clean `supported: false`
verdict (the model actually fetched the page and it didn't support the
claim) is never retried — see `_is_error_verdict`.

Fail-closed rules (SPEC must-fix #3) — this module never "trusts" silence:
  * fetch_ok == False (paywall / robots / fetch error) marks that source
    `unverified: paywalled`. NOT a failure by itself.
  * BUT every claim whose *only* linking url(s) are all fetch_ok=False must
    have >=1 corroborating claim elsewhere in the article that (a) is tied
    to a DIFFERENT source with fetch_ok=True and supported=True, and
    (b) is textually similar to the uncorroborated claim (tokenized-shingle
    Jaccard over engine.util.shingles/jaccard — the same near-duplicate
    technique the rest of the engine uses, e.g. scoring.py). No such claim
    -> HARD FAIL.
  * A source with NO extractable claim at all (`needs_corroboration`, FIX
    G) requires at least one OTHER source anywhere in the article to be
    independently fetch_ok+supported — there's no claim text to test
    similarity against, so this is a weaker bar than the rule above, but
    zero independently-verified sources backing the whole article is still
    a fail-closed problem (Rule 3).
  * Any fetch_ok=True source whose verdict is supported=False -> HARD FAIL,
    unconditionally. A live, checkable source that fails its own claim is
    never rescued by corroboration.
  * Any error while requesting/parsing a source's verdict (bad JSON,
    exception, unparseable model reply) is treated as the WORST case for
    that source (fetch_ok=False, supported=False) — never treated as a
    silent pass. This is the highest-stakes module in the pipeline;
    ambiguity always resolves to "verify more," never "ship it."

Report is always written to
`data/gate-reports/<date>-<slug>-citations.json`. On PASS only, the
article's front matter is edited in place: `review.facts_verified` and
`review.sources_checked` -> true, and every fetch_ok=False source gets
`unverified: paywalled` added (key order otherwise preserved).

CLI: `python -m engine.ai.citation_gate <slug> [--date D] [--fixture]`
     exit 0 = pass, 1 = fail, 2 = infra error.

Deviations from SPEC.md's literal text (kept minimal, called out per the
task brief):
  * `run()` takes an optional trailing `root: Path = ROOT` kwarg (not in
    SPEC's literal 4-arg signature) so the module is testable against a
    tmp_path tree, per SPEC's own testing instructions. writer_cli.py
    (Agent D) calls `citation_gate.run(date_ist, slug, client, cfg)`
    positionally, which still works since `root` defaults.
  * `prompts/v1/citation_check.md` (Agent B) did not exist yet while this
    module was written. The renderer assumes `{{style}}`, `{{url}}` and
    `{{claim}}` placeholders (mirroring the `{{style}}` convention already
    used by `prompts/v1/_style.md`) but ALSO appends an explicit
    "SOURCE URL / CLAIM TO VERIFY" block after rendering regardless of
    whether those placeholders exist in the real template, so the model
    always receives the url + claim even if Agent B's final placeholder
    names differ.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

from ..util import ROOT, jaccard, now_ist, shingles, today_str, tokenize

# Documents the verdict shape the prompt is told to reply with (and what
# _parse_verdict validates by hand). NOT passed as generate()'s json_schema
# any more (FIX F) — Vertex 400s on responseSchema + urlContext together,
# so the model is instead told in the prompt to reply with raw JSON only,
# and _parse_verdict extracts+parses that leniently.
CITATION_SCHEMA = {
    "type": "object",
    "properties": {
        "supported": {"type": "boolean"},
        "quote": {"type": "string"},
        "fetch_ok": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": ["supported", "quote", "fetch_ok", "reason"],
}

# Inline citation = a markdown link whose target is an http(s) url. Internal
# links (/articles/..., /topics/...) never match a front-matter source url
# so they're naturally excluded once we filter to known source urls.
_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

# Claim texts are now full sentences (FIX G), not short link-anchor phrases
# — n=5 (engine.util's usual default, tuned for full-article near-dup
# detection) rarely overlaps between two independently-worded sentences
# about the same fact. n=3 + a lower bar suits sentence-level corroboration.
_SHINGLE_N = 3
CORROBORATION_JACCARD_THRESHOLD = 0.25

# Naive sentence-boundary split: a run of whitespace preceded by ./!/? and
# followed by something that plausibly starts a new sentence (capital
# letter, digit, quote, or a markdown link). Good enough for prose written
# to a style guide (this pipeline's own writer prompt) — not a general NLP
# tokenizer, and doesn't need to be: any ambiguity falls back to the whole
# paragraph (see _sentence_containing), never a wrong/truncated claim.
_SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\[])')
_MAX_CLAIMS_PER_SOURCE = 3  # bounds prompt size when one url is cited repeatedly


class CitationGateError(RuntimeError):
    """Infra-level failure (missing article, unreadable front matter) —
    distinct from a normal fail-closed gate FAIL, which is reported via the
    (passed=False, report) return, never raised."""


# ---------------- article I/O (front matter kept separate from engine.util
# so this module can round-trip-edit sources[] without disturbing the rest
# of the document; engine.util.parse_article is read-only) ----------------

def _read_front_matter(path: Path) -> tuple[dict, str, str]:
    raw = path.read_text(encoding="utf-8-sig")
    m = FM_RE.match(raw)
    if not m:
        raise CitationGateError(f"{path}: missing YAML front matter block")
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(1), m.group(2)


def _write_front_matter(path: Path, meta: dict, body: str) -> None:
    fm_text = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True,
                             default_flow_style=None, width=100)
    path.write_text(f"---\n{fm_text}---\n\n{body.strip()}\n", encoding="utf-8")


def _article_path(root: Path, date_ist: str, slug: str) -> Path:
    return root / "content" / "articles" / f"{date_ist}-{slug}.md"


# ---------------- claim extraction (FIX G) ----------------
# The claim to verify a source against must be the actual factual SENTENCE
# the article ties to it — not the markdown link's anchor text (e.g. "Google
# Official Blog" is a link label, not a claim; verifying a source against
# its own link text is a no-op that can never fail).

def _paragraphs(body: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", body) if p.strip()]


def _split_sentences(paragraph: str) -> list[str]:
    return [p.strip() for p in _SENTENCE_SPLIT_RE.split(paragraph.strip()) if p.strip()]


def _sentence_containing(paragraph: str, match_start: int, match_end: int) -> str:
    """The sentence inside `paragraph` that contains the [match_start,
    match_end) character span — falls back to the WHOLE paragraph whenever
    sentence-boundary detection can't cleanly map the span to exactly one
    sentence (ambiguous), per FIX G's explicit fallback rule.

    Requires the FULL span (start AND end) to fit inside one sentence
    chunk, not just the start — a naive split can false-trigger on an
    abbreviation *inside* the link's own anchor text (e.g. "[Bloomberg
    L.P. News](url)" — the "P. N" looks like a sentence boundary to the
    naive regex). Checking only match_start there would return a
    TRUNCATED sentence with a dangling, unclosed "[" and no matching
    "](url)" — worse than just using the whole paragraph. Checking both
    ends makes that case fall through to the paragraph fallback instead."""
    sentences = _split_sentences(paragraph)
    if len(sentences) <= 1:
        return paragraph.strip()
    pos = 0
    for sent in sentences:
        idx = paragraph.find(sent, pos)
        if idx == -1:
            return paragraph.strip()  # reconstruction failed -> ambiguous
        sent_start, sent_end = idx, idx + len(sent)
        if sent_start <= match_start and match_end <= sent_end:
            return sent
        pos = sent_end
    return paragraph.strip()  # span didn't land cleanly inside any one sentence


def _strip_markdown_links(text: str) -> str:
    """[anchor](url) -> anchor, everywhere — a claim must read as plain
    prose, not raw markdown, when handed to the citation-check model."""
    return _LINK_RE.sub(r"\1", text)


def _extract_claims(body: str, source_urls: set) -> dict:
    """url -> [claim sentence, ...] (up to _MAX_CLAIMS_PER_SOURCE, in
    first-occurrence order, de-duplicated): the full sentence containing
    each inline markdown link to that url (whole paragraph if sentence
    splitting is ambiguous), with markdown link syntax stripped so it reads
    as plain prose."""
    claims: dict = {u: [] for u in source_urls}
    for paragraph in _paragraphs(body):
        for m in _LINK_RE.finditer(paragraph):
            url = m.group(2)
            if url not in claims or len(claims[url]) >= _MAX_CLAIMS_PER_SOURCE:
                continue
            sentence = _sentence_containing(paragraph, m.start(), m.end())
            claim_text = _strip_markdown_links(sentence).strip()
            if claim_text and claim_text not in claims[url]:
                claims[url].append(claim_text)
    return claims


def _load_sources_pool(root: Path, date_ist: str) -> dict:
    """url -> entry from data/briefs/<date>-sources.json (the research
    source pool ai_research.py wrote), if present. Used ONLY as a
    last-resort claim source for front-matter sources[] never cited
    inline in the body — never invented, always read off disk."""
    p = root / "data" / "briefs" / f"{date_ist}-sources.json"
    if not p.exists():
        return {}
    try:
        entries = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {e.get("url"): e for e in entries if isinstance(e, dict) and e.get("url")}


def _fallback_claim(description: str, pool_entry: dict | None) -> str | None:
    """A source never cited inline in the body has no sentence to verify.
    Last resort: the article's own front-matter description + that url's
    title from the research source pool (data/briefs/<date>-sources.json)
    — real text that already exists on disk, never fabricated. Returns
    None (caller marks the source `needs_corroboration` instead of ever
    inventing a claim) when there's nothing usable to build from."""
    description = (description or "").strip()
    title = ((pool_entry or {}).get("title") or "").strip()
    if not description or not title:
        return None
    return f'{description} (source referenced for: "{title}")'


def _similar(a: str, b: str) -> bool:
    sa = shingles(tokenize(a), n=_SHINGLE_N)
    sb = shingles(tokenize(b), n=_SHINGLE_N)
    return jaccard(sa, sb) >= CORROBORATION_JACCARD_THRESHOLD


# ---------------- prompting ----------------

def _load_prompt(root: Path, name: str) -> str:
    path = root / "prompts" / "v1" / name
    if not path.exists():
        raise CitationGateError(f"missing prompt template: {path}")
    return path.read_text(encoding="utf-8")


def _load_style(root: Path) -> str:
    path = root / "prompts" / "v1" / "_style.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _render_check_prompt(root: Path, url: str, claim: str, title: str) -> str:
    template = _load_prompt(root, "citation_check.md")
    style = _load_style(root)
    claim_text = claim or (
        f'(no inline citation found — verify the source supports its '
        f'listed title: "{title}")')
    rendered = (template.replace("{{style}}", style)
                        .replace("{{url}}", url)
                        .replace("{{claim}}", claim_text))
    # Defensive: always append explicit context, regardless of whether the
    # placeholders above existed/matched in Agent B's actual template.
    rendered += f"\n\n---\nSOURCE URL: {url}\nCLAIM TO VERIFY: {claim_text}\n"
    return rendered


def _extract_json_object(text: str) -> str | None:
    """Find and return the first balanced {...} block in `text`, respecting
    string quoting (so a brace inside a "quote"/"reason" string value never
    throws off the count). Returns None if no balanced object is found.

    FIX F: controlled generation (responseSchema) can't be used alongside
    the urlContext tool, so citation_gate's verdict is no longer schema-
    enforced — the model is told to reply with raw JSON only, but may still
    wrap it in a code fence or add stray text despite that instruction.
    This is the lenient-parsing half of that fix."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def _parse_verdict(text: str) -> dict:
    obj_text = _extract_json_object(text or "")
    if obj_text is None:
        return {
            "supported": False,
            "quote": "",
            "fetch_ok": False,
            "reason": "unparseable verdict: no JSON object found in model output",
        }
    try:
        data = json.loads(obj_text)
        return {
            "supported": bool(data["supported"]),
            "quote": str(data.get("quote", ""))[:500],
            "fetch_ok": bool(data["fetch_ok"]),
            "reason": str(data.get("reason", ""))[:500],
        }
    except Exception as e:  # noqa: BLE001 — fail-closed: malformed verdict
        return {
            "supported": False,
            "quote": "",
            "fetch_ok": False,
            "reason": f"unparseable verdict: {type(e).__name__}: {e}",
        }


# ---------------- one-source check + error retry (FIX I) ----------------

def _is_error_verdict(verdict: dict) -> bool:
    """True for an ERROR outcome (call exception, HTTP error, or an
    unparseable model reply) — these are flake, not an editorial verdict,
    and get retried once. A clean `supported: false` from a model that
    fetched and read the page is a real verdict and is NEVER retried."""
    reason = verdict.get("reason", "")
    return reason.startswith("gate call error:") or reason.startswith("unparseable verdict")


def _check_one_source(root: Path, model: str, client, step: str, url: str,
                      claim: str, title: str, note: str = "") -> dict:
    """One citation-check attempt against one source. Never raises — any
    exception (network, HTTP, ledger budget, etc.) becomes a fail-closed
    'gate call error' verdict, same as an unparseable model reply."""
    try:
        result = client.generate(
            step=step, model=model,
            contents=_render_check_prompt(root, url, claim, title),
            # FIX F: NO json_schema here — Vertex rejects controlled
            # generation combined with the urlContext tool. The prompt
            # demands raw JSON instead; _parse_verdict extracts+parses it
            # leniently (fail-closed on failure).
            tools=[{"urlContext": {}}],
            temperature=0.0,
            note=note,
        )
        return _parse_verdict(result.text)
    except Exception as e:  # noqa: BLE001 — fail-closed on any call error
        return {"supported": False, "quote": "", "fetch_ok": False,
                "reason": f"gate call error: {type(e).__name__}: {e}"}


def _check_one_source_with_retry(root: Path, model: str, client, step: str, url: str,
                                 claim: str, title: str) -> dict:
    """FIX I: an ERROR outcome (exception / HTTP error / unparseable
    verdict) is retried ONCE with a fresh generate() call using the exact
    same prompt, before the fail-closed verdict is recorded — a genuinely
    flaky call (rate limit blip, transient 5xx, a model that garbled its
    JSON once) shouldn't sink an otherwise-good source. The retry attempt
    is tagged with ledger note 'retry'; whatever it returns (success or a
    second error) is final — there is no second retry."""
    verdict = _check_one_source(root, model, client, step, url, claim, title)
    if _is_error_verdict(verdict):
        verdict = _check_one_source(root, model, client, step, url, claim, title,
                                    note="retry")
    return verdict


# ---------------- main entry point ----------------

def run(date_ist: str, slug: str, client, cfg: dict,
        root: Path = ROOT) -> tuple:
    """Returns (passed, report). Never raises for a normal gate FAIL — only
    for infra problems (missing article/config), matching writer_cli's
    expectation that a returned passed=False is a gate failure while a
    raised exception is an infra error (EXIT_INFRA_ERROR)."""
    root = Path(root)
    article_path = _article_path(root, date_ist, slug)
    if not article_path.exists():
        raise CitationGateError(f"no article at {article_path}")
    meta, _fm_raw, body = _read_front_matter(article_path)
    sources = meta.get("sources") or []
    model = (cfg.get("llm") or {}).get("model_fast")
    if not model:
        raise CitationGateError("cfg['llm']['model_fast'] is required")

    source_urls = {s.get("url") for s in sources if s.get("url")}
    claims_by_url = _extract_claims(body, source_urls)
    sources_pool = _load_sources_pool(root, date_ist)
    description = str(meta.get("description", ""))

    checked = []  # per-source result rows
    for i, src in enumerate(sources):
        url = src.get("url")
        if not url:
            continue
        claim_list = list(claims_by_url.get(url) or [])
        needs_corroboration = False
        if claim_list:
            primary_claim = " ".join(claim_list)
        else:
            fallback = _fallback_claim(description, sources_pool.get(url))
            if fallback:
                primary_claim = fallback
                claim_list = [fallback]
            else:
                # FIX G: never invent a claim to send to the model — mark
                # it and let Rule 3 (below) require independent
                # corroboration from elsewhere in the article instead.
                needs_corroboration = True
                primary_claim = ""

        step = f"citation_check_{i}"
        if needs_corroboration:
            verdict = {"supported": False, "quote": "", "fetch_ok": False,
                       "reason": "needs_corroboration: no claim could be "
                                "constructed (not cited inline in the body, "
                                "no matching source-pool entry)"}
        else:
            verdict = _check_one_source_with_retry(
                root, model, client, step, url, primary_claim, src.get("title", ""))
        checked.append({
            "url": url, "title": src.get("title", ""),
            "primary": bool(src.get("primary", False)),
            "claims": claim_list, "needs_corroboration": needs_corroboration,
            **verdict,
        })

    by_url = {row["url"]: row for row in checked}
    failures = []

    # Rule 1: any fetchable source that doesn't support its claim -> HARD FAIL.
    for row in checked:
        if row["fetch_ok"] and not row["supported"]:
            failures.append({
                "type": "unsupported", "url": row["url"],
                "claim": row["claims"][0] if row["claims"] else "",
                "detail": row["reason"] or "source did not support its claim",
            })

    # Rule 2: claims tied ONLY to unfetchable sources need corroboration.
    corroborators = [row for row in checked
                     if row["fetch_ok"] and row["supported"]]
    for row in checked:
        if row["fetch_ok"] or row["needs_corroboration"]:
            continue  # unfetchable-but-claimed sources only; Rule 3 covers needs_corroboration
        for claim in row["claims"]:
            corroborated = any(
                other["url"] != row["url"] and (
                    any(_similar(claim, c) for c in other["claims"])
                    or (not other["claims"] and _similar(claim, other["title"]))
                )
                for other in corroborators
            )
            if not corroborated:
                failures.append({
                    "type": "uncorroborated_paywalled", "url": row["url"],
                    "claim": claim,
                    "detail": "no fetchable+supported source corroborates "
                              "this claim, and its only source is unfetchable",
                })

    # Rule 3 (FIX G): a source with NO extractable claim at all (not cited
    # inline, no source-pool match — needs_corroboration=True, never sent
    # to the model) needs at least one OTHER independently fetch_ok+
    # supported source to exist ANYWHERE in the article; there's no claim
    # text to test similarity against, so this is a weaker bar than Rule 2
    # — but zero verified sources backing the whole piece is still a
    # real fail-closed problem, never silently passed.
    for row in checked:
        if row["needs_corroboration"] and not corroborators:
            failures.append({
                "type": "needs_corroboration_unmet", "url": row["url"], "claim": "",
                "detail": "no extractable claim for this source (not cited "
                          "inline, no source-pool match) and no other source "
                          "in the article is independently verified",
            })

    passed = not failures
    report = {
        "slug": slug, "date": date_ist, "checked_at": now_ist().isoformat(),
        "passed": passed, "hard_failures": len(failures),
        "sources": checked, "failures": failures,
    }

    out_dir = root / "data" / "gate-reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{date_ist}-{slug}-citations.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if passed:
        review = meta.setdefault("review", {})
        review["facts_verified"] = True
        review["sources_checked"] = True
        paywalled = {row["url"] for row in checked if not row["fetch_ok"]}
        for src in sources:
            if src.get("url") in paywalled:
                src["unverified"] = "paywalled"
        _write_front_matter(article_path, meta, body)

    return passed, report


# ---------------- CLI ----------------

def main(argv=None) -> int:
    import argparse

    from ..util import load_config

    ap = argparse.ArgumentParser(prog="python -m engine.ai.citation_gate")
    ap.add_argument("slug")
    ap.add_argument("--date", default=None)
    ap.add_argument("--fixture", action="store_true")
    args = ap.parse_args(argv)

    import os
    if args.fixture:
        os.environ["TTD_AI_FIXTURE"] = "1"

    date_ist = args.date or today_str()
    try:
        # Deferred imports: this CLI is the only place in the module that
        # needs a real GeminiClient/Ledger; the library function `run()`
        # only needs a duck-typed `client` and never imports them, so unit
        # tests can pass a fake client without gemini_client.py existing.
        from .gemini_client import GeminiClient
        from .ledger import Ledger

        cfg = load_config()
        ledger = Ledger(cfg["llm"], run_id=f"citation-gate-{date_ist}")
        fixture_dir = str(ROOT / "tests" / "fixtures" / "ai") if args.fixture else None
        client = GeminiClient(cfg["llm"], ledger, fixture_dir=fixture_dir)
        passed, report = run(date_ist, args.slug, client, cfg)
    except CitationGateError as e:
        print(f"infra error: {e}")
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"infra error: {type(e).__name__}: {e}")
        return 2

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

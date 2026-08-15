"""Citation gate — fail-closed verification that every source an article
cites actually supports the claim it's attached to.

Contract (SPEC.md, Agent C):
    run(date_ist, slug, client, cfg) -> (passed: bool, report: dict)

For each front-matter `sources[]` url, one `urlContext` fetch+check model
call (model_fast, prompts/v1/citation_check.md) returns a JSON verdict
`{supported: bool, quote: str, fetch_ok: bool, reason: str}` for the
claim(s) the article body ties to that url (an inline markdown link
`[claim text](url)` whose target matches the source url).

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
  * Any fetch_ok=True source whose verdict is supported=False -> HARD FAIL,
    unconditionally. A live, checkable source that fails its own claim is
    never rescued by corroboration.
  * Any error while requesting/parsing a source's verdict (bad JSON,
    exception, malformed schema) is treated as the WORST case for that
    source (fetch_ok=False, supported=False) — never treated as a silent
    pass. This is the highest-stakes module in the pipeline; ambiguity
    always resolves to "verify more," never "ship it."

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

# Claim texts are short phrases, not documents — n=5 (engine.util's usual
# default, tuned for full-article near-dup detection) rarely overlaps on a
# 5-12 word claim. n=3 + a lower bar suits short-phrase corroboration.
_SHINGLE_N = 3
CORROBORATION_JACCARD_THRESHOLD = 0.25


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


# ---------------- claim extraction ----------------

def _extract_claims(body: str, source_urls: set) -> dict:
    """url -> [claim text, ...], restricted to inline links that target a
    known front-matter source url."""
    claims: dict = {u: [] for u in source_urls}
    for text, url in _LINK_RE.findall(body):
        if url in claims:
            claims[url].append(text.strip())
    return claims


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


def _parse_verdict(text: str) -> dict:
    try:
        data = json.loads(text)
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
            "reason": f"gate parse error: {type(e).__name__}: {e}",
        }


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

    checked = []  # per-source result rows
    for i, src in enumerate(sources):
        url = src.get("url")
        if not url:
            continue
        claim_list = claims_by_url.get(url) or []
        primary_claim = claim_list[0] if claim_list else ""
        step = f"citation_check_{i}"
        try:
            result = client.generate(
                step=step, model=model,
                contents=_render_check_prompt(root, url, primary_claim,
                                              src.get("title", "")),
                tools=[{"urlContext": {}}], json_schema=CITATION_SCHEMA,
                temperature=0.0,
            )
            verdict = _parse_verdict(result.text)
        except Exception as e:  # noqa: BLE001 — fail-closed on any call error
            verdict = {"supported": False, "quote": "", "fetch_ok": False,
                       "reason": f"gate call error: {type(e).__name__}: {e}"}
        checked.append({
            "url": url, "title": src.get("title", ""),
            "primary": bool(src.get("primary", False)),
            "claims": claim_list, **verdict,
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
        if row["fetch_ok"]:
            continue  # only unfetchable sources' claims need this check
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

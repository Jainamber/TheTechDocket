"""Tests for engine.ai.citation_gate — the fail-closed citation gate.

Covers the four citation scenarios called out in SPEC.md:
  1. supported                        -> pass
  2. unsupported (fetchable)          -> HARD FAIL
  3. paywalled + corroborated         -> pass
  4. paywalled-only (no corroboration)-> HARD FAIL

Runs with TTD_AI_FIXTURE=1 semantics via the real engine.ai.gemini_client.
GeminiClient + engine.ai.ledger.Ledger, pointed at a fixture_dir passed
explicitly (so no env mutation / no network / no gcloud is ever needed).
Each source's canned verdict lives at
tests/fixtures/ai/citation_check_<i>.json under a per-test tmp_path root —
GeminiClient's fixture lookup is one JSON file per `step` name, and
citation_gate.py calls generate(step=f"citation_check_{i}", ...) once per
front-matter source (index i), so each source gets its own canned verdict.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from engine.ai.citation_gate import CitationGateError, run
from engine.ai.gemini_client import GeminiClient
from engine.ai.ledger import Ledger

DATE = "2026-08-15"
SLUG = "test-article"

STYLE_MD = "# style\nBe accurate.\n"
CITATION_CHECK_MD = (
    "<!-- v1 | test fixture | placeholders: {{like_this}} -->\n"
    "{{style}}\n\nCheck whether {{url}} supports: {{claim}}\n"
)


def _cfg() -> dict:
    return {
        "llm": {
            "model_fast": "gemini-2.5-flash-lite",
            "location": "global",
            "daily_budget_usd": 100.0,
            "max_grounded_queries_per_run": 1000,
            "max_url_fetches_per_run": 1000,
        }
    }


def _make_root(tmp_path: Path) -> Path:
    (tmp_path / "prompts" / "v1").mkdir(parents=True, exist_ok=True)
    (tmp_path / "prompts" / "v1" / "_style.md").write_text(STYLE_MD, encoding="utf-8")
    (tmp_path / "prompts" / "v1" / "citation_check.md").write_text(
        CITATION_CHECK_MD, encoding="utf-8")
    (tmp_path / "content" / "articles").mkdir(parents=True, exist_ok=True)
    (tmp_path / "tests" / "fixtures" / "ai").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _write_article(root: Path, sources: list, body: str) -> Path:
    fm = {
        "title": "Test Article", "slug": SLUG, "date": DATE, "hub": "ai-tools",
        "sources": sources,
        "review": {"facts_verified": False, "sources_checked": False,
                   "title_promise_check": True, "no_fabrication": True,
                   "policy_pass": True},
    }
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n" + body + "\n"
    path = root / "content" / "articles" / f"{DATE}-{SLUG}.md"
    path.write_text(text, encoding="utf-8")
    return path


# The four canonical scenario fixtures live at tests/fixtures/ai/ in the
# repo (SPEC.md: "citation fixtures cover: supported, unsupported->fail,
# paywalled-with-corroboration->pass, paywalled-only->fail") and are copied
# here into the per-run, per-source-index filename GeminiClient's fixture
# mode looks up (`citation_check_<i>.json`), since one gate run makes one
# generate() call per front-matter source and each needs its own verdict.
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ai"


def _use_canonical_fixture(root: Path, index: int, name: str) -> None:
    src = FIXTURES_DIR / f"citation_check_{name}.json"
    dst = root / "tests" / "fixtures" / "ai" / f"citation_check_{index}.json"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _write_verdict_fixture(root: Path, index: int, supported: bool, fetch_ok: bool,
                           quote: str = "", reason: str = "") -> None:
    """Ad-hoc verdict for edge cases the four canonical fixtures don't cover
    verbatim (kept alongside them, not a replacement)."""
    verdict = {"supported": supported, "quote": quote, "fetch_ok": fetch_ok,
               "reason": reason}
    payload = {
        "text": json.dumps(verdict), "usage": {"in": 10, "out": 10, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 1 if fetch_ok else 0,
        "sources": [], "finish_reason": "STOP", "model": "gemini-2.5-flash-lite",
    }
    (root / "tests" / "fixtures" / "ai" / f"citation_check_{index}.json").write_text(
        json.dumps(payload), encoding="utf-8")


def _client(root: Path) -> GeminiClient:
    ledger = Ledger(_cfg()["llm"], run_id="test-run", root=root)
    return GeminiClient(_cfg()["llm"], ledger,
                        fixture_dir=str(root / "tests" / "fixtures" / "ai"), root=root)


# ---------------- scenario 1: supported -> pass ----------------

def test_supported_source_passes(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Primary source", "url": "https://example.com/a", "primary": True}]
    body = "The company [raised $10 million](https://example.com/a) last week."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is True
    assert report["hard_failures"] == 0
    assert report["sources"][0]["supported"] is True
    # front matter was edited on pass
    updated = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(updated.split("---\n", 2)[1])
    assert fm["review"]["facts_verified"] is True
    assert fm["review"]["sources_checked"] is True
    assert "unverified" not in fm["sources"][0]
    # report file written
    rep_path = root / "data" / "gate-reports" / f"{DATE}-{SLUG}-citations.json"
    assert rep_path.exists()
    assert json.loads(rep_path.read_text(encoding="utf-8"))["passed"] is True


# ---------------- scenario 2: unsupported (fetchable) -> HARD FAIL ----------------

def test_unsupported_fetchable_source_fails(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Contradicted source", "url": "https://example.com/b"}]
    body = "The company [raised $10 million](https://example.com/b) last week."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "unsupported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is False
    assert report["hard_failures"] == 1
    assert report["failures"][0]["type"] == "unsupported"
    # front matter must NOT be edited on failure (fail-closed)
    original = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(original.split("---\n", 2)[1])
    assert fm["review"]["facts_verified"] is False


# ---------------- scenario 3: paywalled + corroborated -> pass ----------------

def test_paywalled_source_with_corroboration_passes(tmp_path):
    root = _make_root(tmp_path)
    sources = [
        {"title": "Paywalled outlet", "url": "https://paywalled.example.com/story"},
        {"title": "Open wire report", "url": "https://wire.example.com/story"},
    ]
    claim = "the company raised $50 million in new funding"
    body = (f"According to a paywalled report, [{claim}](https://paywalled.example.com/story). "
           f"A wire service independently reported [{claim}](https://wire.example.com/story).")
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "paywalled")
    _use_canonical_fixture(root, 1, "corroborating")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is True
    assert report["hard_failures"] == 0
    updated = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(updated.split("---\n", 2)[1])
    assert fm["review"]["facts_verified"] is True
    paywalled_src = next(s for s in fm["sources"] if s["url"] == "https://paywalled.example.com/story")
    assert paywalled_src["unverified"] == "paywalled"
    open_src = next(s for s in fm["sources"] if s["url"] == "https://wire.example.com/story")
    assert "unverified" not in open_src


# ---------------- scenario 4: paywalled-only -> HARD FAIL ----------------

def test_paywalled_only_source_fails(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Paywalled-only outlet", "url": "https://paywalled.example.com/lonely"}]
    body = "The company [raised $50 million in new funding](https://paywalled.example.com/lonely)."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "paywalled")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is False
    assert report["hard_failures"] == 1
    assert report["failures"][0]["type"] == "uncorroborated_paywalled"
    original = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(original.split("---\n", 2)[1])
    assert fm["review"]["sources_checked"] is False


# ---------------- infra / edge cases ----------------

def test_missing_article_raises_infra_error(tmp_path):
    root = _make_root(tmp_path)
    with pytest.raises(CitationGateError):
        run(DATE, "no-such-slug", _client(root), _cfg(), root=root)


def test_malformed_verdict_json_is_fail_closed(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Weird source", "url": "https://example.com/weird"}]
    body = "As [reported](https://example.com/weird), the sky is blue."
    _write_article(root, sources, body)
    # not valid JSON -> _parse_verdict must fail closed, not raise/pass
    payload = {"text": "not json at all", "usage": {"in": 1, "out": 1, "thinking": 0},
              "grounded_queries": 0, "url_fetches": 0, "sources": [],
              "finish_reason": "STOP", "model": "gemini-2.5-flash-lite"}
    (root / "tests" / "fixtures" / "ai" / "citation_check_0.json").write_text(
        json.dumps(payload), encoding="utf-8")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is False
    assert report["sources"][0]["fetch_ok"] is False
    assert report["sources"][0]["supported"] is False

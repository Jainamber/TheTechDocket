"""Tests for engine.ai.ai_docket — the AI-drafted Today's Docket step.

`ai_docket.run()` reuses `engine.docket.write_draft()` for candidate
harvesting/scaffolding (task brief: "reuse its entry points ... rather than
reimplementing"). `write_draft()` itself has no root parameter — it always
resolves paths from its own module-level `engine.docket.ROOT` /
`engine.docket.DOCKET_DIR` — so these tests monkeypatch those two names to
point at tmp_path, matching real (unpatched) behavior exactly when
`engine.docket.ROOT` already equals the repo root (the default/production
case). `engine.util.load_config()` is left untouched (it is read-only and
only used by write_draft() to *suggest* tags in the human-facing comment
lines of the throwaway draft template — never in the parsed/AI-filled
output this module actually writes), so it harmlessly reads the real repo's
config.yaml.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

import engine.docket as edocket
from engine.ai.ai_docket import run
from engine.ai.gemini_client import GeminiClient
from engine.ai.ledger import Ledger

DATE = "2026-08-15"

CANDIDATES = {
    "date": DATE,
    "candidates": [
        {"title": "Today's lead article candidate", "sources": ["hn"],
         "evidence": [{"url": "https://example.com/lead", "points": 500}], "score": 0.9},
        {"title": "A second interesting story", "sources": ["gnews:IN"],
         "evidence": [{"url": "https://example.com/second"}], "score": 0.6},
    ],
}

DOCKET_ENTRY_MD = "<!-- v1 | test fixture -->\n{{style}}\n\nFill items from:\n{{draft_template}}\n"

DOCKET_ITEMS_RESPONSE = {
    "items": [
        {"hub": "ai-tools", "lead": True, "rank": 1, "tag": "", "headline": "Lead headline",
         "dek": "**Lead in.** Rest of the dek.", "url": "/articles/today-slug/", "source": "The Tech Docket"},
        {"hub": "big-tech", "rank": 2, "tag": "", "headline": "Second headline",
         "dek": "**Lead in.** Rest of the dek.", "why": "Because it matters.",
         "stat_line": "500 points", "url": "https://example.com/second", "source": "example.com"},
    ]
}


def _cfg() -> dict:
    return {"llm": {"model_fast": "gemini-2.5-flash-lite", "daily_budget_usd": 100.0,
                    "max_grounded_queries_per_run": 1000, "max_url_fetches_per_run": 1000}}


@pytest.fixture
def root(tmp_path, monkeypatch):
    (tmp_path / "data" / "briefs").mkdir(parents=True)
    (tmp_path / "data" / "docket").mkdir(parents=True)
    (tmp_path / "prompts" / "v1").mkdir(parents=True)
    (tmp_path / "tests" / "fixtures" / "ai").mkdir(parents=True)
    (tmp_path / "prompts" / "v1" / "docket_entry.md").write_text(DOCKET_ENTRY_MD, encoding="utf-8")
    (tmp_path / "data" / "briefs" / f"{DATE}-candidates.json").write_text(
        json.dumps(CANDIDATES), encoding="utf-8")
    monkeypatch.setattr(edocket, "ROOT", tmp_path)
    monkeypatch.setattr(edocket, "DOCKET_DIR", tmp_path / "data" / "docket")
    return tmp_path


def _client(root: Path, response: dict) -> GeminiClient:
    (root / "tests" / "fixtures" / "ai" / "docket.json").write_text(json.dumps({
        "text": json.dumps(response), "usage": {"in": 5, "out": 5, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 0, "sources": [], "finish_reason": "STOP",
        "model": "gemini-2.5-flash-lite",
    }), encoding="utf-8")
    ledger = Ledger(_cfg()["llm"], run_id="test-run", root=root)
    return GeminiClient(_cfg()["llm"], ledger, fixture_dir=str(root / "tests" / "fixtures" / "ai"), root=root)


def test_happy_path_writes_valid_docket_file(root):
    client = _client(root, DOCKET_ITEMS_RESPONSE)
    result = run(DATE, client, _cfg(), root=root)

    assert result["ok"] is True
    out_path = Path(result["path"])
    assert out_path.exists()
    assert out_path == root / "data" / "docket" / f"{DATE}.md"
    data = edocket.parse_docket(out_path)
    assert data["date"] == DATE
    assert len(data["items"]) == 2
    assert data["items"][0]["lead"] is True


def test_missing_candidates_file_is_reported_not_raised(root):
    (root / "data" / "briefs" / f"{DATE}-candidates.json").unlink()
    client = _client(root, DOCKET_ITEMS_RESPONSE)

    result = run(DATE, client, _cfg(), root=root)

    assert result["ok"] is False
    assert result["path"] is None
    assert "no candidates file" in result["note"]
    # article-first invariant: nothing touched under content/ or data/history.json
    assert not (root / "data" / "history.json").exists()


def test_zero_items_from_model_is_reported_not_raised(root):
    client = _client(root, {"items": []})

    result = run(DATE, client, _cfg(), root=root)

    assert result["ok"] is False
    assert "zero items" in result["note"]


def test_malformed_model_json_never_raises(root):
    (root / "tests" / "fixtures" / "ai" / "docket.json").write_text(json.dumps({
        "text": "not valid json", "usage": {"in": 1, "out": 1, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 0, "sources": [], "finish_reason": "STOP",
        "model": "gemini-2.5-flash-lite",
    }), encoding="utf-8")
    ledger = Ledger(_cfg()["llm"], run_id="test-run", root=root)
    client = GeminiClient(_cfg()["llm"], ledger, fixture_dir=str(root / "tests" / "fixtures" / "ai"), root=root)

    result = run(DATE, client, _cfg(), root=root)  # must not raise

    assert result["ok"] is False
    assert "JSONDecodeError" in result["note"]

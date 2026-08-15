"""Tests for engine.ai.ai_social — the AI social-caption export step.

Reuses `engine.docket.parse_docket()` (read-only, takes an explicit Path,
no global-root coupling) to load the day's already-drafted docket data
file, so no monkeypatching is needed here (unlike test_ai_docket.py).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.ai.ai_social import run
from engine.ai.gemini_client import GeminiClient
from engine.ai.ledger import Ledger

DATE = "2026-08-15"

DOCKET_MD = """---
date: 2026-08-15
items:
  - hub: ai-tools
    lead: true
    rank: 1
    headline: "Lead headline"
    dek: "**Lead in.** Rest of dek."
    url: /articles/today-slug/
    source: "The Tech Docket"
---
"""

SOCIAL_CAPTION_MD = "<!-- v1 | test fixture -->\n{{style}}\n\nWrite a caption for:\n{{docket_json}}\n"


def _cfg(enabled: bool = True) -> dict:
    return {
        "llm": {"model_fast": "gemini-2.5-flash-lite", "daily_budget_usd": 100.0,
               "max_grounded_queries_per_run": 1000, "max_url_fetches_per_run": 1000},
        "social": {"enabled": enabled},
    }


@pytest.fixture
def root(tmp_path):
    (tmp_path / "data" / "docket").mkdir(parents=True)
    (tmp_path / "prompts" / "v1").mkdir(parents=True)
    (tmp_path / "tests" / "fixtures" / "ai").mkdir(parents=True)
    (tmp_path / "prompts" / "v1" / "social_caption.md").write_text(SOCIAL_CAPTION_MD, encoding="utf-8")
    (tmp_path / "data" / "docket" / f"{DATE}.md").write_text(DOCKET_MD, encoding="utf-8")
    return tmp_path


def _client(root: Path, text: str) -> GeminiClient:
    (root / "tests" / "fixtures" / "ai" / "social.json").write_text(json.dumps({
        "text": text, "usage": {"in": 5, "out": 5, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 0, "sources": [], "finish_reason": "STOP",
        "model": "gemini-2.5-flash-lite",
    }), encoding="utf-8")
    ledger = Ledger(_cfg()["llm"], run_id="test-run", root=root)
    return GeminiClient(_cfg()["llm"], ledger, fixture_dir=str(root / "tests" / "fixtures" / "ai"), root=root)


def test_happy_path_writes_caption_file(root):
    client = _client(root, "Today's top story: lead headline. #tech")
    result = run(DATE, client, _cfg(), root=root)

    assert result["ok"] is True
    out_path = Path(result["path"])
    assert out_path == root / "data" / "social" / f"{DATE}.md"
    assert "lead headline" in out_path.read_text(encoding="utf-8")


def test_disabled_in_config_is_reported_not_raised(root):
    client = _client(root, "caption")
    result = run(DATE, client, _cfg(enabled=False), root=root)

    assert result["ok"] is False
    assert "disabled" in result["note"]
    assert not (root / "data" / "social").exists()


def test_missing_docket_file_is_reported_not_raised(root):
    (root / "data" / "docket" / f"{DATE}.md").unlink()
    client = _client(root, "caption")

    result = run(DATE, client, _cfg(), root=root)

    assert result["ok"] is False
    assert "no docket data file" in result["note"]


def test_empty_model_output_is_reported_not_raised(root):
    client = _client(root, "   ")

    result = run(DATE, client, _cfg(), root=root)

    assert result["ok"] is False
    assert "empty caption" in result["note"]

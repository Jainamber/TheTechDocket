"""Tests for engine.ai (gemini_client, pricing, ledger).

Fixture-mode only: TTD_AI_FIXTURE=1 / an explicit fixture_dir, zero network,
zero gcloud. Covers each module's import + happy path + a key failure path.
"""
from __future__ import annotations

import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from engine.ai import pricing
from engine.ai.gemini_client import (GeminiClient, GenResult, ModelUnavailable,
                                     _endpoint, _parse_grounding, _thinking_config)
from engine.ai.ledger import BudgetExceeded, Ledger

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "ai")

LLM_CFG = {
    "location": "global",
    "daily_budget_usd": 2.00,
    "max_grounded_queries_per_run": 12,
    "max_url_fetches_per_run": 25,
}


def _client(tmp_path, ledger, **cfg_overrides):
    cfg = dict(LLM_CFG, **cfg_overrides)
    return GeminiClient(cfg, ledger, fixture_dir=FIXTURE_DIR, root=tmp_path)


def _ledger(tmp_path, **cfg_overrides):
    cfg = dict(LLM_CFG, **cfg_overrides)
    return Ledger(cfg, run_id="test-run-1", root=tmp_path)


# ---------------------------------------------------------------- pricing

def test_pricing_known_model_estimates_cost():
    cost = pricing.estimate("gemini-3.5-flash", 1_000_000, 1_000_000, grounded_queries=0)
    assert cost == pytest.approx(1.50 + 9.00)


def test_pricing_grounding_surcharge_added():
    base = pricing.estimate("gemini-2.5-flash", 0, 0, grounded_queries=0)
    with_queries = pricing.estimate("gemini-2.5-flash", 0, 0, grounded_queries=5)
    assert with_queries == pytest.approx(base + 5 * pricing.GROUNDING_USD_PER_QUERY)


def test_pricing_unknown_model_returns_negative_one():
    assert pricing.estimate("not-a-real-model", 100, 100) == -1.0


def test_pricing_table_has_all_four_served_models_with_dated_source():
    for model in ("gemini-3.5-flash", "gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"):
        entry = pricing.PRICES[model]
        assert entry["in"] > 0 and entry["out"] > 0
        assert entry["as_of"] and entry["source"]


# ---------------------------------------------------------------- ledger

def test_ledger_record_writes_header_and_row(tmp_path):
    led = _ledger(tmp_path)
    led.record(step="write", model="gemini-3.5-flash",
               usage={"in": 100, "out": 200, "thinking": 30},
               grounded_queries=1, url_fetches=2, cost_usd=0.0021, note="unit-test")
    rows = list(csv.DictReader(open(led.path, encoding="utf-8")))
    assert len(rows) == 1
    r = rows[0]
    assert r["step"] == "write"
    assert r["model"] == "gemini-3.5-flash"
    assert int(r["tokens_in"]) == 100
    assert int(r["tokens_out"]) == 200
    assert int(r["tokens_thinking"]) == 30
    assert r["note"] == "unit-test"


def test_ledger_day_total_treats_unknown_cost_as_placeholder(tmp_path):
    led = _ledger(tmp_path)
    today = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")
    led.record(step="a", model="m", usage={"in": 1, "out": 1, "thinking": 0}, cost_usd=1.0)
    led.record(step="b", model="m", usage={"in": 1, "out": 1, "thinking": 0}, cost_usd=-1.0)  # UNKNOWN
    total = led.day_total(today)
    assert total == pytest.approx(1.0 + 0.05)


def test_ledger_precheck_raises_when_budget_reached(tmp_path):
    led = _ledger(tmp_path, daily_budget_usd=1.0)
    led.record(step="a", model="m", usage={"in": 1, "out": 1, "thinking": 0}, cost_usd=1.0)
    with pytest.raises(BudgetExceeded):
        led.precheck("next-step")


def test_ledger_precheck_raises_when_query_cap_reached(tmp_path):
    led = _ledger(tmp_path, max_grounded_queries_per_run=2)
    led.record(step="a", model="m", usage={"in": 0, "out": 0, "thinking": 0},
               grounded_queries=2, cost_usd=0.028)
    with pytest.raises(BudgetExceeded):
        led.precheck("next-step", uses_grounding=True)


def test_ledger_precheck_ok_when_under_caps(tmp_path):
    led = _ledger(tmp_path)
    led.precheck("first-step")  # no rows yet -> must not raise


def test_ledger_precheck_does_not_block_non_grounded_step_after_cap_reached(tmp_path):
    """Regression: ai_research.py is designed to legitimately spend the
    entire max_grounded_queries_per_run cap across its research calls. A
    later non-grounded step (write, citation-check verdicts, select) in the
    SAME run must not be blocked just because that cap is now exhausted —
    only a call that itself declares uses_grounding=True should be gated by
    it. Caught via the full writer_cli --all fixture e2e, where the write
    step was raising BudgetExceeded immediately after research legitimately
    used its whole grounded-query budget."""
    led = _ledger(tmp_path, max_grounded_queries_per_run=2)
    led.record(step="research", model="m", usage={"in": 0, "out": 0, "thinking": 0},
               grounded_queries=2, cost_usd=0.028)
    led.precheck("write")  # no tool-use flags -> must not raise
    led.precheck("citations", uses_url_fetch=True)  # different cap -> must not raise


def test_ledger_precheck_url_fetch_cap_scoped_to_url_fetch_calls(tmp_path):
    led = _ledger(tmp_path, max_url_fetches_per_run=1)
    led.record(step="citations", model="m", usage={"in": 0, "out": 0, "thinking": 0},
               url_fetches=1, cost_usd=0.0)
    with pytest.raises(BudgetExceeded):
        led.precheck("next-citation", uses_url_fetch=True)
    led.precheck("write")  # unrelated step, no tool flags -> must not raise


# ---------------------------------------------------------------- client: helpers

def test_endpoint_uses_plain_host_for_global_location():
    url = _endpoint("proj-x", "global", "gemini-3.5-flash")
    assert url == (
        "https://aiplatform.googleapis.com/v1/projects/proj-x/locations/global"
        "/publishers/google/models/gemini-3.5-flash:generateContent")


def test_endpoint_uses_region_prefixed_host_for_non_global_location():
    url = _endpoint("proj-x", "us-central1", "gemini-2.5-pro")
    assert url.startswith("https://us-central1-aiplatform.googleapis.com/")


def test_thinking_config_string_is_level_int_is_budget():
    assert _thinking_config("high") == {"thinkingLevel": "high"}
    assert _thinking_config(4096) == {"thinkingBudget": 4096}
    assert _thinking_config(-1) == {"thinkingBudget": -1}


def test_parse_grounding_handles_missing_metadata_gracefully():
    grounded, fetches, sources = _parse_grounding({"candidates": [{"content": {"parts": []}}]})
    assert (grounded, fetches, sources) == (0, 0, [])


def test_parse_grounding_extracts_queries_and_sources():
    payload = {
        "candidates": [{
            "groundingMetadata": {
                "webSearchQueries": ["q1", "q2"],
                "groundingChunks": [{"web": {"uri": "https://x.example/a", "title": "A"}}],
            },
            "urlContextMetadata": {"urlMetadata": [{"retrievedUrl": "https://x.example/a"}]},
        }]
    }
    grounded, fetches, sources = _parse_grounding(payload)
    assert grounded == 2
    assert fetches == 1
    assert sources == [{"url": "https://x.example/a", "title": "A"}]


# ---------------------------------------------------------------- client: fixture mode

def test_fixture_mode_auto_on_via_env(tmp_path, monkeypatch):
    monkeypatch.setenv("TTD_AI_FIXTURE", "1")
    led = _ledger(tmp_path)
    client = GeminiClient(dict(LLM_CFG), led, root=tmp_path)
    assert client.fixture_mode is True
    assert client.project is None  # never resolves a GCP project in fixture mode


def test_generate_happy_path_reads_fixture_and_records_ledger(tmp_path):
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)
    result = client.generate("happy_step", "gemini-3.5-flash", "irrelevant in fixture mode")
    assert isinstance(result, GenResult)
    assert result.text == "Fixture reply text for the happy-path test."
    assert result.usage == {"in": 120, "out": 340, "thinking": 50}
    assert result.grounded_queries == 2
    assert result.url_fetches == 1
    assert result.sources == [{"url": "https://example.com/source-a", "title": "Example Source A"}]
    assert result.cost_usd == 0.0

    rows = list(csv.DictReader(open(led.path, encoding="utf-8")))
    assert len(rows) == 1
    assert rows[0]["note"] == "fixture"
    assert rows[0]["step"] == "happy_step"
    # run counters incremented even in fixture mode, so caps are still testable
    assert led._grounded_queries_this_run == 2
    assert led._url_fetches_this_run == 1


def test_generate_missing_fixture_raises_and_does_not_write_ledger(tmp_path):
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)
    with pytest.raises(RuntimeError):
        client.generate("no_such_step", "gemini-3.5-flash", "hi")
    rows = list(csv.DictReader(open(led.path, encoding="utf-8")))
    assert rows == []  # missing-fixture error happens before ledger.record()


def test_generate_rejects_json_schema_with_url_context_tool(tmp_path):
    # FIX F: Vertex 400s on responseSchema + urlContext together — the
    # client must refuse before ever making the call (fixture mode
    # included), never letting this combination ship again.
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)
    with pytest.raises(ValueError, match="urlContext"):
        client.generate("citation_check_0", "gemini-2.5-flash-lite", "hi",
                        tools=[{"urlContext": {}}],
                        json_schema={"type": "object"})
    # rejected before any ledger row is written
    rows = list(csv.DictReader(open(led.path, encoding="utf-8")))
    assert rows == []


def test_generate_rejects_json_schema_with_google_search_tool(tmp_path):
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)
    with pytest.raises(ValueError, match="googleSearch"):
        client.generate("research", "gemini-3.5-flash", "hi",
                        tools=[{"googleSearch": {}}],
                        json_schema={"type": "object"})


def test_generate_allows_json_schema_without_tools(tmp_path):
    # the schema-forced style must keep working for calls with no tools —
    # this is the FIX F guard's negative case (no false positive)
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)
    result = client.generate("happy_step", "gemini-3.5-flash", "irrelevant in fixture mode",
                             json_schema={"type": "object"})
    assert result.text  # fixture read succeeded — the call was not blocked


def test_generate_allows_url_context_tool_without_json_schema(tmp_path):
    # tools alone (no schema) must keep working — this is exactly what
    # citation_gate.py now does after FIX F
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)
    result = client.generate("happy_step", "gemini-3.5-flash", "irrelevant in fixture mode",
                             tools=[{"urlContext": {}}])
    assert result.text


def test_precheck_blocks_generate_before_reading_fixture(tmp_path):
    led = _ledger(tmp_path, daily_budget_usd=0.01)
    led.record(step="prior", model="gemini-3.5-flash",
               usage={"in": 0, "out": 0, "thinking": 0}, cost_usd=1.0)
    client = _client(tmp_path, led)
    with pytest.raises(BudgetExceeded):
        client.generate("happy_step", "gemini-3.5-flash", "hi")


def test_generate_with_fallback_uses_second_model_on_model_unavailable(tmp_path, monkeypatch):
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)

    real_generate = client.generate
    calls = []

    def fake_generate(step, model, *a, **kw):
        calls.append(model)
        if model == "gemini-unavailable-model":
            raise ModelUnavailable("not served")
        return real_generate(step, model, *a, **kw)

    monkeypatch.setattr(client, "generate", fake_generate)
    result = client.generate_with_fallback(
        "happy_step", ["gemini-unavailable-model", "gemini-3.5-flash"], contents="hi")
    assert calls == ["gemini-unavailable-model", "gemini-3.5-flash"]
    assert result.model == "gemini-3.5-flash"


def test_generate_with_fallback_raises_when_all_models_unavailable(tmp_path, monkeypatch):
    led = _ledger(tmp_path)
    client = _client(tmp_path, led)

    def always_unavailable(step, model, *a, **kw):
        raise ModelUnavailable(f"{model} not served")

    monkeypatch.setattr(client, "generate", always_unavailable)
    with pytest.raises(ModelUnavailable):
        client.generate_with_fallback("happy_step", ["model-a", "model-b"], contents="hi")

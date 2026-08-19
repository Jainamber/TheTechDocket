"""Sanity checks for Agent E's GitHub Actions workflows.

These are YAML-structure checks only (no network, no `act`/gh execution) —
they guard against the class of mistake that breaks a workflow before it
ever runs: bad YAML, wrong trigger, missing mode gate, secret leakage.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


def _load(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def test_daily_pipeline_parses_and_has_no_pull_request_trigger():
    doc = _load("daily-pipeline.yml")
    # PyYAML 1.1 resolves the bare `on:` key to the boolean True.
    triggers = doc[True]
    assert "schedule" in triggers
    assert "workflow_dispatch" in triggers
    assert "pull_request" not in triggers


def test_daily_pipeline_concurrency_and_tz():
    doc = _load("daily-pipeline.yml")
    assert doc["concurrency"]["group"] == "engine-main"
    assert doc["concurrency"]["cancel-in-progress"] is False
    assert doc["env"]["TZ"] == "Asia/Kolkata"


def test_daily_pipeline_has_run_and_gate_check_jobs():
    doc = _load("daily-pipeline.yml")
    jobs = doc["jobs"]
    assert "run" in jobs
    assert "gate-check" in jobs
    assert jobs["gate-check"]["needs"] == "run"


def test_daily_pipeline_mode_gate_reads_repo_variable():
    text = (WORKFLOWS / "daily-pipeline.yml").read_text(encoding="utf-8")
    assert "vars.TTD_PIPELINE_MODE" in text
    assert "staging" in text and "live" in text


def test_daily_pipeline_no_hardcoded_secrets():
    text = (WORKFLOWS / "daily-pipeline.yml").read_text(encoding="utf-8")
    assert "VERTEX_SA_KEY" in text
    # Only ever referenced via the secrets context, never a literal value.
    assert "secrets.VERTEX_SA_KEY" in text
    assert "AIza" not in text  # no stray API key literal
    assert "-----BEGIN" not in text  # no embedded key material


def test_watchdog_parses_and_triggers():
    doc = _load("watchdog.yml")
    triggers = doc[True]
    assert "schedule" in triggers
    assert "workflow_dispatch" in triggers
    assert "pull_request" not in triggers
    assert doc["permissions"]["issues"] == "write"


def test_watchdog_gated_on_live_mode_for_issue_creation():
    text = (WORKFLOWS / "watchdog.yml").read_text(encoding="utf-8")
    assert "vars.TTD_PIPELINE_MODE" in text
    assert "jainamber" in text
    assert "data/skips/" in text


def test_existing_workflows_left_untouched():
    # Agent E must not modify the two pre-existing workflow files.
    fetch = (WORKFLOWS / "fetch-trends.yml").read_text(encoding="utf-8")
    publish = (WORKFLOWS / "on-publish.yml").read_text(encoding="utf-8")
    assert 'cron: "15 0 * * *"' in fetch
    assert "IndexNow ping" in publish

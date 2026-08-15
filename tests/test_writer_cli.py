"""Tests for engine.ai.writer_cli — fixture-mode, zero network, zero gcloud.

Covers: STOP-guard exit 3, --all step ordering, the shared gate/citation
retry budget, best-effort docket/social, the infra-error exit path, the
history.json record step (FIX 1) and the data/run-state/<date>.json
run-state file (FIX 2).
The real Runner (subprocess + lazy sibling-module imports) is never
exercised here — a FakeRunner with the same method surface stands in, so
these tests do not depend on engine.ai.gemini_client / ai_select /
ai_research / ai_write / citation_gate / ai_docket / ai_social existing or
being finished yet.
"""
from __future__ import annotations

import json
import os
from types import SimpleNamespace

import pytest

os.environ.setdefault("TTD_AI_FIXTURE", "1")

from engine.ai import writer_cli  # noqa: E402


CFG = {"llm": {"max_retry_rewrites": 1},
       "site": {"base_url": "https://thetechdocket.com/"}}


def _write_article(path, slug, title="Test Title", *, keyword="test keyword",
                    hub="ai-tools", date="2026-08-15", review=None):
    # review defaults to the POST-citation_gate state (all true) since
    # FakeRunner.citation_gate never actually touches the article file —
    # tests that exercise the record step need the fixture to already look
    # like a citation_gate PASS would have left it.
    review = {
        "facts_verified": True, "sources_checked": True,
        "title_promise_check": True, "no_fabrication": True,
        "policy_pass": True, "reviewed_at": "2026-08-15T10:00:00+05:30",
    } if review is None else review
    review_lines = "\n".join(f"  {k}: {json.dumps(v)}" for k, v in review.items())
    path.write_text(
        "---\n"
        f'title: "{title}"\n'
        f'slug: "{slug}"\n'
        f"date: {date}\n"
        f'keyword: "{keyword}"\n'
        f'hub: {hub}\n'
        "review:\n"
        f"{review_lines}\n"
        "---\n"
        "Body text.\n",
        encoding="utf-8",
    )


def _canonical_article(tmp_path, date, slug, **kw):
    """Write a test article at content/articles/<date>-<slug>.md — the same
    path the real pipeline uses. Required for any test that reaches the
    record step (FIX 1), since _record_entry() re-reads the article from
    that canonical path rather than trusting the path FakeRunner.ai_write()
    happened to return."""
    d = tmp_path / "content" / "articles"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{date}-{slug}.md"
    _write_article(path, slug, **kw)
    return path


class FakeRunner:
    """Records every call; feeds back scripted results for gate/citations/
    ai_write so retry-budget and step-ordering behaviour can be asserted."""

    def __init__(self, article_paths, gate_results, citation_results,
                 write_raises=None):
        self.calls: list[tuple] = []
        self._article_paths = list(article_paths)
        self._gate_results = list(gate_results)
        self._citation_results = list(citation_results)
        self._write_raises = write_raises

    def engine_run(self, *args):
        self.calls.append(("engine_run",) + args)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    def ai_select(self, date_ist, client, cfg):
        self.calls.append(("ai_select", date_ist))
        return {"pick_rank": 0, "reason": "fixture", "override": False}

    def ai_research(self, date_ist, slug_hint, client, cfg):
        self.calls.append(("ai_research", date_ist))
        return {"notes": "fixture research"}

    def ai_write(self, date_ist, client, cfg, retry_feedback=None):
        self.calls.append(("ai_write", date_ist, retry_feedback))
        if self._write_raises is not None and len(self.calls) == 1:
            raise self._write_raises
        return self._article_paths.pop(0)

    def gate(self, slug, date_ist):
        self.calls.append(("gate", slug, date_ist))
        return self._gate_results.pop(0)

    def citation_gate(self, date_ist, slug, client, cfg):
        self.calls.append(("citation_gate", date_ist, slug))
        passed, report = self._citation_results.pop(0)
        # mirrors the real Runner.citation_gate contract: feedback is a
        # JSON string (or None), never a raw dict
        feedback = None if passed else json.dumps(report)
        return passed, feedback

    def ai_docket(self, date_ist, client, cfg):
        self.calls.append(("ai_docket", date_ist))
        return {"ok": True}

    def ai_social(self, date_ist, client, cfg):
        self.calls.append(("ai_social", date_ist))
        return {"ok": True}

    def call_names(self):
        return [c[0] if c[0] != "engine_run" else ("engine_run", c[1])
                for c in self.calls]


# ---------------- STOP guard ----------------

def test_stop_guard_exit_3_when_already_published(tmp_path):
    hist = {"published": [{"date": "2026-08-15", "slug": "already-done"}]}
    (tmp_path / "data").mkdir(parents=True)
    (tmp_path / "data" / "history.json").write_text(
        json.dumps(hist), encoding="utf-8")

    fake = FakeRunner([], [], [])
    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_STOP
    assert fake.calls == []  # never touched the runner

    state = json.loads(
        (tmp_path / "data" / "run-state" / "2026-08-15.json").read_text())
    assert state["date"] == "2026-08-15"
    assert state["slug"] is None
    assert state["status"] == "stop"
    assert state["recorded"] is False
    assert "ts_ist" in state


def test_no_stop_when_date_not_in_history(tmp_path):
    (tmp_path / "data").mkdir(parents=True)
    (tmp_path / "data" / "history.json").write_text(
        json.dumps({"published": [{"date": "2026-08-14", "slug": "x"}]}),
        encoding="utf-8")
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")

    art = _canonical_article(tmp_path, "2026-08-15", "todays-slug")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake)
    assert rc == writer_cli.EXIT_OK


def test_skip_stop_guard_bypasses_history(tmp_path):
    (tmp_path / "data").mkdir(parents=True)
    (tmp_path / "data" / "history.json").write_text(
        json.dumps({"published": [{"date": "2026-08-15", "slug": "x"}]}),
        encoding="utf-8")
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")

    art = _canonical_article(tmp_path, "2026-08-15", "todays-slug")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, skip_stop_guard=True, runner=fake)
    assert rc == writer_cli.EXIT_OK
    assert fake.calls  # the runner WAS used this time


# ---------------- step ordering ----------------

def test_all_step_ordering_happy_path(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")

    art = _canonical_article(tmp_path, "2026-08-15", "the-slug")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_OK
    names = [c[0] for c in fake.calls]
    # fetch is skipped (inbox already exists) -> select, ai_select, brief,
    # ai_research, ai_write, build, gate, citation_gate, docket, social
    # (record is not part of the Runner interface — it's called directly)
    assert names == [
        "engine_run", "ai_select", "engine_run", "ai_research", "ai_write",
        "engine_run", "gate", "citation_gate", "ai_docket", "ai_social",
    ]
    assert fake.calls[0] == ("engine_run", "select")
    assert fake.calls[2] == ("engine_run", "brief")
    assert fake.calls[5] == ("engine_run", "build")


def test_all_runs_fetch_when_inbox_missing(tmp_path):
    (tmp_path / "data").mkdir(parents=True)

    art = _canonical_article(tmp_path, "2026-08-15", "the-slug")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                       ledger=None, runner=fake)

    assert fake.calls[0] == ("engine_run", "fetch")
    assert fake.calls[1] == ("engine_run", "select")


# ---------------- retry budget ----------------

def test_gate_retry_budget_exhausted_returns_gate_fail(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")

    art1 = tmp_path / "a1.md"
    art2 = tmp_path / "a2.md"
    _write_article(art1, "slug-one")
    _write_article(art2, "slug-two")
    cfg = {"llm": {"max_retry_rewrites": 1},
           "site": {"base_url": "https://thetechdocket.com/"}}
    # gate fails both times -> exactly 1 + max_retries ai_write calls,
    # citation_gate never reached
    fake = FakeRunner([str(art1), str(art2)],
                       [(False, "gate report 1"), (False, "gate report 2")],
                       [])

    rc = writer_cli.run_all("2026-08-15", tmp_path, cfg, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_GATE_FAIL
    write_calls = [c for c in fake.calls if c[0] == "ai_write"]
    gate_calls = [c for c in fake.calls if c[0] == "gate"]
    cit_calls = [c for c in fake.calls if c[0] == "citation_gate"]
    assert len(write_calls) == 2          # initial + 1 retry, budget exhausted
    assert len(gate_calls) == 2
    assert cit_calls == []                # gate never passed -> citations skipped
    # second ai_write call carried the first gate's feedback
    assert write_calls[1][2] == "gate report 1"

    # record must NOT have run — no history.json at all
    assert not (tmp_path / "data" / "history.json").exists()

    state = json.loads(
        (tmp_path / "data" / "run-state" / "2026-08-15.json").read_text())
    assert state["status"] == "gate_fail"
    assert state["slug"] == "slug-two"   # final attempted slug
    assert state["recorded"] is False


def test_citation_retry_consumes_shared_budget_then_passes(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")

    art1 = _canonical_article(tmp_path, "2026-08-15", "slug-one")
    art2 = _canonical_article(tmp_path, "2026-08-15", "slug-two")
    cfg = {"llm": {"max_retry_rewrites": 1},
           "site": {"base_url": "https://thetechdocket.com/"}}
    fake = FakeRunner(
        [str(art1), str(art2)],
        [(True, None), (True, None)],
        [(False, {"reason": "unsupported"}), (True, None)],
    )

    rc = writer_cli.run_all("2026-08-15", tmp_path, cfg, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_OK
    write_calls = [c for c in fake.calls if c[0] == "ai_write"]
    assert len(write_calls) == 2
    assert json.loads(write_calls[1][2])["reason"] == "unsupported"

    # citations passed on the retry -> record runs against the FINAL slug
    hist = json.loads((tmp_path / "data" / "history.json").read_text())
    assert hist["published"][0]["slug"] == "slug-two"


def test_retry_budget_zero_means_no_second_attempt(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")
    art = tmp_path / "a1.md"
    _write_article(art, "slug-one")
    cfg = {"llm": {"max_retry_rewrites": 0},
           "site": {"base_url": "https://thetechdocket.com/"}}
    fake = FakeRunner([str(art)], [(False, "nope")], [])

    rc = writer_cli.run_all("2026-08-15", tmp_path, cfg, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_GATE_FAIL
    assert len([c for c in fake.calls if c[0] == "ai_write"]) == 1
    assert not (tmp_path / "data" / "history.json").exists()


# ---------------- best-effort docket/social ----------------

def test_docket_social_failure_does_not_change_exit_code(tmp_path, capsys):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")
    art = _canonical_article(tmp_path, "2026-08-15", "slug-one")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    def _boom(*a, **kw):
        raise RuntimeError("docket exploded")
    fake.ai_docket = _boom  # type: ignore[assignment]

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_OK
    out = capsys.readouterr().out
    assert "docket: skipped" in out


# ---------------- infra error path ----------------

def test_unexpected_exception_returns_infra_error(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")
    fake = FakeRunner([], [], [], write_raises=RuntimeError("boom"))

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_INFRA_ERROR
    assert not (tmp_path / "data" / "history.json").exists()

    state = json.loads(
        (tmp_path / "data" / "run-state" / "2026-08-15.json").read_text())
    assert state["status"] == "infra_error"
    assert state["slug"] is None
    assert state["recorded"] is False


# ---------------- record step (FIX 1) ----------------

def test_record_appends_history_entry_on_full_pass(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")
    art = _canonical_article(tmp_path, "2026-08-15", "the-slug", title="The Title")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_OK
    hist = json.loads((tmp_path / "data" / "history.json").read_text(encoding="utf-8"))
    assert len(hist["published"]) == 1
    entry = hist["published"][0]
    assert entry["slug"] == "the-slug"
    assert entry["title"] == "The Title"
    assert entry["keyword"] == "test keyword"
    assert entry["hub"] == "ai-tools"
    assert entry["date"] == "2026-08-15"
    assert entry["url"] == "https://thetechdocket.com/articles/the-slug/"
    assert entry["gate_report"] == "data/gate-reports/2026-08-15-the-slug.json"
    assert entry["review"]["facts_verified"] is True
    assert entry["review"]["sources_checked"] is True
    assert "published_at" in entry

    state = json.loads(
        (tmp_path / "data" / "run-state" / "2026-08-15.json").read_text())
    assert state["date"] == "2026-08-15"
    assert state["slug"] == "the-slug"
    assert state["status"] == "ok"
    assert state["recorded"] is True
    assert "ts_ist" in state


def test_record_replaces_existing_entry_for_same_slug(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")
    (tmp_path / "data").mkdir(exist_ok=True)
    (tmp_path / "data" / "history.json").write_text(json.dumps({
        "published": [{"date": "2026-08-01", "slug": "the-slug",
                        "title": "Stale"}],
    }), encoding="utf-8")

    art = _canonical_article(tmp_path, "2026-08-15", "the-slug", title="Fresh Title")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_OK
    hist = json.loads((tmp_path / "data" / "history.json").read_text())
    assert len(hist["published"]) == 1
    assert hist["published"][0]["title"] == "Fresh Title"


def test_record_skipped_with_no_record_flag(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")
    art = _canonical_article(tmp_path, "2026-08-15", "the-slug")
    fake = FakeRunner([str(art)], [(True, None)], [(True, None)])

    rc = writer_cli.run_all("2026-08-15", tmp_path, CFG, client=None,
                            ledger=None, runner=fake, record=False)

    assert rc == writer_cli.EXIT_OK
    assert not (tmp_path / "data" / "history.json").exists()

    state = json.loads(
        (tmp_path / "data" / "run-state" / "2026-08-15.json").read_text())
    assert state["status"] == "ok"
    assert state["slug"] == "the-slug"
    assert state["recorded"] is False


def test_record_not_written_when_citations_fail(tmp_path):
    (tmp_path / "data" / "inbox").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "2026-08-15.json").write_text("{}", encoding="utf-8")
    art1 = _canonical_article(tmp_path, "2026-08-15", "slug-one")
    art2 = _canonical_article(tmp_path, "2026-08-15", "slug-two")
    cfg = {"llm": {"max_retry_rewrites": 1},
           "site": {"base_url": "https://thetechdocket.com/"}}
    # gate always passes but citations never do -> retry budget exhausted
    fake = FakeRunner(
        [str(art1), str(art2)],
        [(True, None), (True, None)],
        [(False, {"reason": "unsupported"}), (False, {"reason": "still bad"})],
    )

    rc = writer_cli.run_all("2026-08-15", tmp_path, cfg, client=None,
                            ledger=None, runner=fake)

    assert rc == writer_cli.EXIT_GATE_FAIL
    assert not (tmp_path / "data" / "history.json").exists()

    state = json.loads(
        (tmp_path / "data" / "run-state" / "2026-08-15.json").read_text())
    assert state["status"] == "gate_fail"
    assert state["recorded"] is False


# ---------------- run_step ----------------

def test_run_step_select_happy_path(tmp_path):
    fake = FakeRunner([], [], [])
    rc = writer_cli.run_step("select", "2026-08-15", tmp_path, CFG, None, None,
                             runner=fake)
    assert rc == writer_cli.EXIT_OK
    assert fake.calls[0] == ("engine_run", "select")
    assert fake.calls[1][0] == "ai_select"


def test_run_step_citations_no_article_is_infra_error(tmp_path):
    (tmp_path / "content" / "articles").mkdir(parents=True)
    fake = FakeRunner([], [], [])
    rc = writer_cli.run_step("citations", "2026-08-15", tmp_path, CFG, None, None,
                             runner=fake)
    assert rc == writer_cli.EXIT_INFRA_ERROR


def test_run_step_citations_fail_exits_gate_fail(tmp_path):
    d = tmp_path / "content" / "articles"
    d.mkdir(parents=True)
    _write_article(d / "2026-08-15-the-slug.md", "the-slug")
    fake = FakeRunner([], [], [(False, {"reason": "bad"})])
    rc = writer_cli.run_step("citations", "2026-08-15", tmp_path, CFG, None, None,
                             runner=fake)
    assert rc == writer_cli.EXIT_GATE_FAIL


def test_run_step_record_appends_history(tmp_path):
    _canonical_article(tmp_path, "2026-08-15", "the-slug", title="The Title")
    fake = FakeRunner([], [], [])

    rc = writer_cli.run_step("record", "2026-08-15", tmp_path, CFG, None, None,
                             runner=fake)

    assert rc == writer_cli.EXIT_OK
    hist = json.loads((tmp_path / "data" / "history.json").read_text())
    assert hist["published"][0]["slug"] == "the-slug"
    assert hist["published"][0]["title"] == "The Title"

    state = json.loads(
        (tmp_path / "data" / "run-state" / "2026-08-15.json").read_text())
    assert state["slug"] == "the-slug"
    assert state["status"] == "ok"
    assert state["recorded"] is True


def test_run_step_record_no_article_is_infra_error(tmp_path):
    (tmp_path / "content" / "articles").mkdir(parents=True)
    fake = FakeRunner([], [], [])
    rc = writer_cli.run_step("record", "2026-08-15", tmp_path, CFG, None, None,
                             runner=fake)
    assert rc == writer_cli.EXIT_INFRA_ERROR
    assert not (tmp_path / "data" / "history.json").exists()


# ---------------- CLI parsing ----------------

def test_parse_args_requires_all_or_step():
    with pytest.raises(SystemExit):
        writer_cli._parse_args([])


def test_parse_args_all_and_fixture():
    args = writer_cli._parse_args(["--all", "--fixture", "--date", "2026-08-15"])
    assert args.all is True
    assert args.fixture is True
    assert args.date == "2026-08-15"


def test_parse_args_no_record_flag():
    args = writer_cli._parse_args(["--all", "--no-record"])
    assert args.no_record is True


def test_parse_args_record_defaults_on():
    args = writer_cli._parse_args(["--all"])
    assert args.no_record is False


def test_parse_args_step_record_is_a_valid_choice():
    args = writer_cli._parse_args(["--step", "record"])
    assert args.step == "record"


def test_already_published_helper(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "history.json").write_text(
        json.dumps({"published": [{"date": "2026-08-15"}]}), encoding="utf-8")
    assert writer_cli.already_published("2026-08-15", tmp_path) is True
    assert writer_cli.already_published("2026-08-16", tmp_path) is False


def test_already_published_no_history_file(tmp_path):
    assert writer_cli.already_published("2026-08-15", tmp_path) is False

"""Daily AI-writing pipeline orchestrator (Vertex/Gemini).

  python -m engine.ai.writer_cli --all [--date YYYY-MM-DD] [--fixture]
                                  [--skip-stop-guard] [--no-record]
  python -m engine.ai.writer_cli --step {select,research,write,citations,
                                  record,docket,social}
                                  [--date YYYY-MM-DD] [--fixture]

Contract: this module wires the zero-LLM engine (engine.run, invoked via
subprocess with sys.executable — never imported into this process) together
with the Gemini step modules (engine.ai.ai_select / ai_research / ai_write /
citation_gate / ai_docket / ai_social, each imported lazily so this file
stays importable while sibling modules are still under construction).

--all order: (0) STOP guard — today_ist already published in history.json
=> print STOP, exit 3 (bypass with --skip-stop-guard, staging/smoke only);
(1) ensure data/inbox/<date>.json exists, else `engine.run fetch`;
(2) `engine.run select`; (3) ai_select; (4) `engine.run brief`;
(5) ai_research; (6) ai_write; (7) citation_gate — flips
review.facts_verified/sources_checked + reviewed_at on PASS;
(8) `engine.run build`; (9) `engine.run gate`. Steps 7-9 run in THIS order
(citations before build/gate, not after) because engine/gates.py's G08 and
G11 need review.facts_verified/sources_checked/title_promise_check/etc all
true, and only the citation gate is allowed to flip the first two —
running compliance gates before citations ever run would deadlock every
fresh draft. Steps 6-9 share ONE retry budget (config
llm.max_retry_rewrites, total across citation + compliance failures, not
per-kind): on EITHER a citation or a compliance HARD failure, one
ai_write(retry_feedback=..., reuse_slug=<same slug>) call, then
citations -> build -> gate re-run from the top — a citation failure skips
straight to retry without wasting a build+gate cycle on a draft that can't
pass G11 yet anyway. `reuse_slug` (FIX D) makes the retried draft overwrite
the SAME content/articles/<date>-<slug>.md instead of a retry draft's
(possibly reworded) title minting a second, orphaned slug; the prior
attempt's stale docs/articles/<slug>/ build output is also removed before
the retry so a later build can't leave it behind. (10) record — ONLY once
BOTH citations and gate have passed, append the published entry to
data/history.json (same shape as engine.publish.publish); skipped with
`--no-record` (record defaults ON; staging PRs pass this so history.json
stays clean until a real merge to main). (11) docket + social, best-effort
— failures there are logged and never change the run's exit code or touch
the article.

Every exit path (ok / gate_fail / stop / infra_error) also writes
data/run-state/<date>.json — {date, slug, status, recorded, ts_ist,
link_warnings} — so CI can read the definitive slug for the day instead of
globbing for it. `link_warnings` (FIX E) surfaces any grounding-redirect
urls ai_write.py could not resolve to a real url (fail-open — never blocks
the run; see engine/ai/resolve_links.py).

No git commands are ever run here (publish stays `engine.run publish` / the
CI PR rail; `record` above only touches data/history.json, never git). One
Ledger + one GeminiClient are constructed per run and shared across every
step.

Exit codes: 0 ok · 1 gate/citation failure surviving the retry budget ·
2 infra error (client init, budget exceeded, model unavailable, any
unexpected exception) · 3 already-published STOP.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from ..util import ROOT, load_config, parse_article

IST = ZoneInfo("Asia/Kolkata")

EXIT_OK = 0
EXIT_GATE_FAIL = 1
EXIT_INFRA_ERROR = 2
EXIT_STOP = 3

STEPS = ("select", "research", "write", "citations", "record", "docket", "social")


def _now_ist() -> datetime:
    return datetime.now(IST)


def _today_ist() -> str:
    return _now_ist().strftime("%Y-%m-%d")


def _make_run_id() -> str:
    return _now_ist().strftime("%Y%m%dT%H%M%S%z")


# ---------------- runner: real subprocess/module calls ----------------
# Tests substitute a fake object exposing the same method surface so step
# ordering and retry-budget logic can be verified with zero network/gcloud
# and without depending on sibling modules being finished yet.

class Runner:
    def __init__(self, root: Path = ROOT):
        self.root = root

    def engine_run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "engine.run", *args],
            cwd=self.root, capture_output=True, text=True,
        )

    def ai_select(self, date_ist: str, client, cfg) -> dict:
        from .ai_select import run as _run
        return _run(date_ist, client, cfg)

    def ai_research(self, date_ist: str, slug_hint, client, cfg):
        from .ai_research import run as _run
        return _run(date_ist, slug_hint, client, cfg)

    def ai_write(self, date_ist: str, client, cfg, retry_feedback: str | None = None,
                 reuse_slug: str | None = None):
        from .ai_write import run as _run
        return _run(date_ist, client, cfg, retry_feedback=retry_feedback,
                    reuse_slug=reuse_slug, root=self.root)

    def gate(self, slug: str, date_ist: str) -> tuple[bool, str | None]:
        rc = self.engine_run("gate", "--slug", slug)
        passed = rc.returncode == 0
        if passed:
            return True, None
        report_path = self.root / "data" / "gate-reports" / f"{date_ist}-{slug}.json"
        if report_path.exists():
            feedback = report_path.read_text(encoding="utf-8")
        else:
            feedback = ((rc.stdout or "") + (rc.stderr or ""))[-4000:]
        return False, feedback

    def citation_gate(self, date_ist: str, slug: str, client, cfg) -> tuple[bool, str | None]:
        from .citation_gate import run as _run
        passed, report = _run(date_ist, slug, client, cfg)
        feedback = None if passed else json.dumps(report, ensure_ascii=False)
        return passed, feedback

    def ai_docket(self, date_ist: str, client, cfg):
        from .ai_docket import run as _run
        return _run(date_ist, client, cfg)

    def ai_social(self, date_ist: str, client, cfg):
        from .ai_social import run as _run
        return _run(date_ist, client, cfg)


# ---------------- helpers ----------------

def already_published(date_ist: str, root: Path = ROOT) -> bool:
    """STOP-guard check: does data/history.json already have this IST date?"""
    hist_path = root / "data" / "history.json"
    if not hist_path.exists():
        return False
    try:
        hist = json.loads(hist_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return any(str(p.get("date")) == date_ist for p in hist.get("published", []))


# ---------------- history (record step) ----------------
# Deliberately NOT engine.util.load_history/save_history — those hardcode
# ROOT, which breaks testing against tmp_path (same reason already_published
# above reads data/history.json by hand instead of using that helper).

def _load_history(root: Path) -> dict:
    path = root / "data" / "history.json"
    if not path.exists():
        return {"published": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"published": []}


def _save_history(root: Path, hist: dict) -> None:
    path = root / "data" / "history.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(hist, indent=2, ensure_ascii=False), encoding="utf-8")


def _record_entry(date_ist: str, slug: str, root: Path, cfg: dict) -> dict:
    """Append the published entry to data/history.json. Same shape as
    engine.publish.publish()'s entry — read from the article's front matter
    AFTER citation_gate has already flipped review.facts_verified /
    review.sources_checked to true on disk. Never touches git."""
    article_path = root / "content" / "articles" / f"{date_ist}-{slug}.md"
    meta = parse_article(article_path)
    entry = {
        "date": str(meta.get("date") or date_ist),
        "slug": slug,
        "title": meta.get("title", ""),
        "keyword": meta.get("keyword", ""),
        "hub": meta.get("hub"),
        "published_at": _now_ist().isoformat(),
        "review": meta.get("review", {}),
        "gate_report": f"data/gate-reports/{date_ist}-{slug}.json",
        "url": cfg["site"]["base_url"].rstrip("/") + f"/articles/{slug}/",
    }
    hist = _load_history(root)
    hist["published"] = [p for p in hist["published"] if p["slug"] != slug]
    hist["published"].append(entry)
    hist["published"].sort(key=lambda p: p["date"])
    _save_history(root, hist)
    return entry


# ---------------- run-state (data/run-state/<date>.json) ----------------
# Written on every --all exit path (and the slug-bearing single steps) so
# CI can read the definitive slug instead of globbing content/articles/.

def _read_link_warnings(root: Path, date_ist: str, slug: str | None) -> list:
    """FIX E: fold ai_write.py's grounding-redirect resolution warnings (if
    any) into run-state — a side file, same pattern as Runner.gate() reading
    the compliance gate-report back from disk instead of over the Runner
    boundary. Missing file (the common case: nothing to warn about, or no
    slug yet) -> []."""
    if not slug:
        return []
    path = root / "data" / "gate-reports" / f"{date_ist}-{slug}-link-warnings.json"
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _write_run_state(root: Path, date_ist: str, slug: str | None, status: str,
                      recorded: bool) -> None:
    path = root / "data" / "run-state" / f"{date_ist}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "date": date_ist,
        "slug": slug,
        "status": status,
        "recorded": recorded,
        "ts_ist": _now_ist().isoformat(),
        "link_warnings": _read_link_warnings(root, date_ist, slug),
    }
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def _slug_from_article(path) -> str:
    meta = parse_article(Path(path))
    slug = meta.get("slug")
    if not slug:
        raise ValueError(f"{path}: front matter missing 'slug'")
    return slug


def _find_slug_for_date(date_ist: str, root: Path) -> str | None:
    d = root / "content" / "articles"
    if not d.exists():
        return None
    for p in sorted(d.glob(f"{date_ist}-*.md")):
        return p.stem[len(date_ist) + 1:]
    return None


def _best_effort(fn, label: str) -> None:
    try:
        fn()
        print(f"{label}: ok")
    except Exception as e:  # noqa: BLE001 — step 10 must never fail the run
        print(f"{label}: skipped ({type(e).__name__}: {e})")


def _build_client_and_ledger(cfg: dict, root: Path, fixture: bool):
    from .gemini_client import GeminiClient
    from .ledger import Ledger
    run_id = _make_run_id()
    ledger = Ledger(cfg["llm"], run_id)
    fixture_dir = str(root / "tests" / "fixtures" / "ai") if fixture else None
    client = GeminiClient(cfg["llm"], ledger, fixture_dir=fixture_dir)
    return client, ledger


# ---------------- orchestration ----------------

def run_all(date_ist: str, root: Path, cfg: dict, client, ledger, *,
            skip_stop_guard: bool = False, runner: Runner | None = None,
            record: bool = True) -> int:
    if not skip_stop_guard and already_published(date_ist, root):
        print(f"STOP: {date_ist} is already published in history.json — "
              "refusing to run again today.")
        _write_run_state(root, date_ist, None, "stop", False)
        return EXIT_STOP

    r = runner or Runner(root)
    slug: str | None = None
    try:
        # (1) ensure inbox
        inbox_path = root / "data" / "inbox" / f"{date_ist}.json"
        if not inbox_path.exists():
            r.engine_run("fetch")

        # (2) + (3) select
        r.engine_run("select")
        r.ai_select(date_ist, client, cfg)

        # (4) + (5) brief + research
        r.engine_run("brief")
        r.ai_research(date_ist, None, client, cfg)

        # (6) write
        article_path = r.ai_write(date_ist, client, cfg)
        slug = _slug_from_article(article_path)

        # (7)-(9) citations / build / gate, sharing one retry budget. Order
        # matters (FIX A): citation_gate runs FIRST — it only needs the raw
        # article on disk — so it can flip review.facts_verified /
        # sources_checked to true before engine.run gate's G08/G11 checks
        # ever see them. Running compliance gates first would hard-fail
        # every fresh draft (they start with those flags false) before
        # citation_gate gets a chance to flip them, deadlocking the pipeline.
        max_retries = int(cfg["llm"]["max_retry_rewrites"])
        retries_used = 0
        gate_ok = False
        cit_ok = False
        while True:
            cit_ok, cit_feedback = r.citation_gate(date_ist, slug, client, cfg)
            gate_ok, gate_feedback = (False, None)
            if cit_ok:
                r.engine_run("build")
                gate_ok, gate_feedback = r.gate(slug, date_ist)
            if cit_ok and gate_ok:
                break
            if retries_used >= max_retries:
                break
            retries_used += 1
            feedback = cit_feedback if not cit_ok else gate_feedback
            # FIX D: clear the failed attempt's stale built page (if build
            # ran this round) before retrying, so a later build can't leave
            # an orphan docs/articles/<slug>/ page behind.
            docs_dir = root / "docs" / "articles" / slug
            if docs_dir.exists():
                shutil.rmtree(docs_dir, ignore_errors=True)
            # reuse_slug: the retry MUST overwrite this same article, never
            # mint a second slug from a reworded retry title.
            article_path = r.ai_write(date_ist, client, cfg, retry_feedback=feedback,
                                      reuse_slug=slug)
            slug = _slug_from_article(article_path)

        # (10) record — ONLY after both gate and citation_gate passed.
        recorded = False
        if gate_ok and cit_ok and record:
            _record_entry(date_ist, slug, root, cfg)
            recorded = True
            print(f"record: {slug} -> data/history.json")

        # (11) docket + social — best-effort, article-first invariant
        _best_effort(lambda: r.ai_docket(date_ist, client, cfg), "docket")
        _best_effort(lambda: r.ai_social(date_ist, client, cfg), "social")

        if gate_ok and cit_ok:
            print(f"ok: {slug} passed gates + citations after {retries_used} retry(ies)")
            _write_run_state(root, date_ist, slug, "ok", recorded)
            return EXIT_OK
        print(f"gate-fail: {slug} did not pass after {retries_used} retry(ies)")
        _write_run_state(root, date_ist, slug, "gate_fail", False)
        return EXIT_GATE_FAIL
    except Exception as e:  # noqa: BLE001 — BudgetExceeded/ModelUnavailable included
        print(f"infra error: {type(e).__name__}: {e}", file=sys.stderr)
        _write_run_state(root, date_ist, slug, "infra_error", False)
        return EXIT_INFRA_ERROR


def run_step(step: str, date_ist: str, root: Path, cfg: dict, client, ledger,
             runner: Runner | None = None) -> int:
    r = runner or Runner(root)
    try:
        if step == "select":
            r.engine_run("select")
            result = r.ai_select(date_ist, client, cfg)
        elif step == "research":
            result = r.ai_research(date_ist, None, client, cfg)
        elif step == "write":
            result = r.ai_write(date_ist, client, cfg)
            _write_run_state(root, date_ist, _slug_from_article(result), "ok", False)
        elif step == "citations":
            slug = _find_slug_for_date(date_ist, root)
            if not slug:
                print(f"infra error: no article found for {date_ist}", file=sys.stderr)
                _write_run_state(root, date_ist, None, "infra_error", False)
                return EXIT_INFRA_ERROR
            passed, feedback = r.citation_gate(date_ist, slug, client, cfg)
            result = {"passed": passed, "feedback": feedback}
            if not passed:
                print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
                _write_run_state(root, date_ist, slug, "gate_fail", False)
                return EXIT_GATE_FAIL
            _write_run_state(root, date_ist, slug, "ok", False)
        elif step == "record":
            slug = _find_slug_for_date(date_ist, root)
            if not slug:
                print(f"infra error: no article found for {date_ist}", file=sys.stderr)
                _write_run_state(root, date_ist, None, "infra_error", False)
                return EXIT_INFRA_ERROR
            result = _record_entry(date_ist, slug, root, cfg)
            _write_run_state(root, date_ist, slug, "ok", True)
        elif step == "docket":
            result = r.ai_docket(date_ist, client, cfg)
        elif step == "social":
            result = r.ai_social(date_ist, client, cfg)
        else:
            raise ValueError(f"unknown step: {step}")
        print(result if isinstance(result, str)
              else json.dumps(result, indent=2, ensure_ascii=False, default=str))
        return EXIT_OK
    except Exception as e:  # noqa: BLE001
        print(f"infra error: {type(e).__name__}: {e}", file=sys.stderr)
        if step in ("write", "citations", "record"):
            _write_run_state(root, date_ist, None, "infra_error", False)
        return EXIT_INFRA_ERROR


# ---------------- CLI ----------------

def _parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="engine.ai.writer_cli")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true",
                       help="Run the full daily pipeline (with STOP guard).")
    mode.add_argument("--step", choices=STEPS,
                       help="Run a single step in isolation.")
    ap.add_argument("--date", default=None,
                     help="YYYY-MM-DD (IST). Defaults to today (IST, zoneinfo).")
    ap.add_argument("--fixture", action="store_true",
                     help="Force fixture mode (TTD_AI_FIXTURE=1): zero network, zero gcloud.")
    ap.add_argument("--skip-stop-guard", action="store_true",
                     help="Bypass the already-published STOP guard. Staging/smoke only.")
    ap.add_argument("--no-record", action="store_true",
                     help="Skip the history.json record step even on a full pass "
                          "(--all only; keeps staging PRs free of history.json noise).")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = _parse_args(argv)
    root = ROOT
    date_ist = args.date or _today_ist()
    if args.fixture:
        os.environ["TTD_AI_FIXTURE"] = "1"

    try:
        cfg = load_config()
        client, ledger = _build_client_and_ledger(cfg, root, args.fixture)
    except Exception as e:  # noqa: BLE001
        print(f"infra error: could not initialize AI client/ledger: {e}", file=sys.stderr)
        return EXIT_INFRA_ERROR

    if args.all:
        return run_all(date_ist, root, cfg, client, ledger,
                        skip_stop_guard=args.skip_stop_guard,
                        record=not args.no_record)
    return run_step(args.step, date_ist, root, cfg, client, ledger)


if __name__ == "__main__":
    sys.exit(main())

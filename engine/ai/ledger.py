"""Append-only USD cost ledger for Gemini (Vertex) calls.

Contract: every GeminiClient.generate() call (fixture or live) calls
Ledger.record() exactly once — on success, on parse failure, and on fixture
replay — so data/costs/ledger.csv is a complete, honest spend log for the
day. precheck() is the enforcement point: GeminiClient calls it BEFORE any
HTTP request, and it raises BudgetExceeded once the day's recorded spend (or
a fixed per-run grounded-query / url-fetch cap) would be exceeded. Those
per-run caps are CODE-enforced here rather than trusted from the model.
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
ROOT = Path(__file__).resolve().parent.parent.parent

FIELDS = [
    "ts_ist", "date_ist", "run_id", "step", "model",
    "tokens_in", "tokens_out", "tokens_thinking",
    "grounded_queries", "url_fetches", "cost_usd", "note",
]

# Used when summing day_total(): a row with cost_usd = -1 (UNKNOWN model,
# see pricing.estimate()) counts as this pessimistic placeholder rather than
# $0, so an unpriced model can never be used to silently blow the budget.
UNKNOWN_COST_PLACEHOLDER_USD = 0.05


class BudgetExceeded(RuntimeError):
    """Raised by Ledger.precheck() when the daily budget or a per-run cap
    (max_grounded_queries_per_run / max_url_fetches_per_run) would be
    exceeded by the next step. Always raised BEFORE any HTTP call."""


class Ledger:
    """CSV-backed spend ledger. One instance is shared across all steps of a
    single writer_cli run (constructed with a shared run_id)."""

    def __init__(self, config: dict, run_id: str, root: str | Path | None = None):
        # NOTE: `root` is not in SPEC.md's literal `Ledger(config, run_id)`
        # signature. Added (optional, defaults to repo root) per SPEC.md's
        # own testing instructions ("modules should take a root path arg
        # defaulting to repo root — make them testable").
        self.config = config or {}
        self.run_id = run_id
        self.root = Path(root) if root else ROOT
        self.path = self.root / "data" / "costs" / "ledger.csv"
        self._ensure_header()
        self._grounded_queries_this_run = 0
        self._url_fetches_this_run = 0

    def _ensure_header(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with open(self.path, "w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow(FIELDS)

    def record(self, step: str, model: str, usage: dict, grounded_queries: int = 0,
               url_fetches: int = 0, cost_usd: float = -1.0, note: str = "") -> None:
        """Append one row. usage is {"in": int, "out": int, "thinking": int}.
        cost_usd of None or < 0 is written as -1.0 (UNKNOWN), never silently 0."""
        now = datetime.now(IST)
        usage = usage or {}
        cost = -1.0 if cost_usd is None else float(cost_usd)
        row = [
            now.isoformat(), now.strftime("%Y-%m-%d"), self.run_id, step, model,
            int(usage.get("in", 0)), int(usage.get("out", 0)), int(usage.get("thinking", 0)),
            int(grounded_queries or 0), int(url_fetches or 0),
            round(cost, 6),
            note,
        ]
        with open(self.path, "a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(row)
        self._grounded_queries_this_run += int(grounded_queries or 0)
        self._url_fetches_this_run += int(url_fetches or 0)

    def _rows(self) -> list[dict]:
        if not self.path.exists():
            return []
        with open(self.path, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def day_total(self, date_ist: str) -> float:
        """Sum of cost_usd for all rows on date_ist (YYYY-MM-DD). UNKNOWN
        rows (cost_usd < 0) count as UNKNOWN_COST_PLACEHOLDER_USD each."""
        total = 0.0
        for r in self._rows():
            if r.get("date_ist") != date_ist:
                continue
            try:
                cost = float(r.get("cost_usd", -1))
            except (TypeError, ValueError):
                cost = -1.0
            total += UNKNOWN_COST_PLACEHOLDER_USD if cost < 0 else cost
        return round(total, 6)

    def precheck(self, step: str, uses_grounding: bool = False,
                 uses_url_fetch: bool = False) -> None:
        """Raise BudgetExceeded if today's spend already meets/exceeds
        daily_budget_usd, or if THIS call is about to spend from a per-run
        cap it would actually draw on and that cap is already exhausted.

        uses_grounding / uses_url_fetch are the caller's declared intent for
        the upcoming call (GeminiClient.generate() derives them from its
        `tools` argument — googleSearch / urlContext respectively). The
        grounded-query and url-fetch caps are scoped to calls that actually
        request that tool: a non-grounded call (e.g. the writer or
        citation-check-verdict steps that don't set that tool) must never be
        blocked just because an earlier, unrelated call already used up the
        run's grounded-query or url-fetch budget — ai_research.py is
        designed to legitimately spend the *entire* per-run grounded-query
        cap, and that must not deadlock every later step in the same run.
        The daily USD budget check has no such scoping and always applies.
        """
        today = datetime.now(IST).strftime("%Y-%m-%d")
        budget = self.config.get("daily_budget_usd")
        if budget is not None:
            spent = self.day_total(today)
            if spent >= float(budget):
                raise BudgetExceeded(
                    f"daily budget ${budget} reached before step '{step}' "
                    f"(spent ${spent} on {today})")
        if uses_grounding:
            max_q = self.config.get("max_grounded_queries_per_run")
            if max_q is not None and self._grounded_queries_this_run >= int(max_q):
                raise BudgetExceeded(
                    f"run cap of {max_q} grounded queries reached before step '{step}' "
                    f"({self._grounded_queries_this_run} used)")
        if uses_url_fetch:
            max_f = self.config.get("max_url_fetches_per_run")
            if max_f is not None and self._url_fetches_this_run >= int(max_f):
                raise BudgetExceeded(
                    f"run cap of {max_f} url fetches reached before step '{step}' "
                    f"({self._url_fetches_this_run} used)")

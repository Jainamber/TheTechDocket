"""Pricing table and cost estimation for Gemini (Vertex) calls.

Contract: PRICES holds USD-per-1,000,000-token input/output rates for every
model the daily pipeline is allowed to call, plus a per-grounded-query
surcharge. estimate() turns (model, tokens_in, tokens_out, grounded_queries)
into a USD cost; an unpriced model returns -1.0 (never 0.0) so ledger.py
writes an honest UNKNOWN row rather than silently under-counting spend —
mirrors GeminiBridge/bridge.py's est_cost() cost-honesty convention.
"""
from __future__ import annotations

# USD per 1,000,000 tokens. Thinking tokens are billed as output tokens
# (Vertex generateContent), so callers pass tout = candidatesTokenCount +
# thoughtsTokenCount into estimate().
PRICES = {
    # Served on the owner's project (live-probed 2026-08-15 via GeminiBridge
    # oneshot). Promo pricing per Google's own launch announcement (grounded
    # in the 08-15 research run: $0.75/$3.75 through 2026-12-31, DOUBLING to
    # $1.50/$7.50 on 2027-01-01 — update this entry then, or earlier if the
    # official pricing page disagrees).
    "gemini-3.7-flash": {
        "in": 0.75,
        "out": 3.75,
        "as_of": "2026-08-15 (promo until 2026-12-31; then 1.50/7.50)",
        "source": "blog.google Gemini 3.7 Flash announcement via grounded research 2026-08-15",
    },
    "gemini-3.6-flash": {
        "in": 1.50,
        "out": 7.50,
        "as_of": "2026-08-15 — re-verify",
        "source": "third-party trackers via web recon 2026-08-15",
    },
    # Verified live probe of the owner's GCP project, location `global`,
    # 2026-08-15 (see SPEC.md "Verified facts").
    "gemini-3.5-flash": {
        "in": 1.50,
        "out": 9.00,
        "as_of": "2026-08-15",
        "source": "SPEC.md verified live probe of owner's GCP project, 2026-08-15",
    },
    # Not re-probed for this project; carried over from GeminiBridge's
    # PRICING table (same GCP project, dated 2026-07). Re-verify before
    # trusting for large-budget decisions.
    "gemini-2.5-pro": {
        "in": 1.25,
        "out": 10.00,
        "as_of": "2026-07 (GeminiBridge bridge.py PRICING) — re-verify",
        "source": "GeminiBridge/bridge.py PRICING table",
    },
    "gemini-2.5-flash": {
        "in": 0.30,
        "out": 2.50,
        "as_of": "2026-07 (GeminiBridge bridge.py PRICING) — re-verify",
        "source": "GeminiBridge/bridge.py PRICING table",
    },
    # SPEC.md flags this one explicitly as an ESTIMATE pending verification
    # ("~$0.30/$2.50 est — verify in pricing.py table with a dated comment").
    "gemini-2.5-flash-lite": {
        "in": 0.30,
        "out": 2.50,
        "as_of": "2026-08-15 (SPEC.md estimate, unverified) — confirm before trusting",
        "source": "SPEC.md verified facts (2026-08-15 probe) — estimate, not invoice-confirmed",
    },
}

# Vertex "grounding with Google Search" billing: $14 per 1,000 grounded
# prompts after a free monthly allotment (SPEC.md verified facts, 2026-08-15).
GROUNDING_USD_PER_QUERY = 0.014
GROUNDING_FREE_PROMPTS_PER_MONTH = 5000


def estimate(model: str, tin: int, tout: int, grounded_queries: int = 0) -> float:
    """Return estimated USD cost for one call, or -1.0 if model is unpriced.

    -1.0 (never 0.0) signals "unknown" so a caller (the ledger) never
    silently records a $0 cost for a model we have no confirmed rate for.
    grounded_queries adds GROUNDING_USD_PER_QUERY per query on top of the
    token cost — callers decide whether the free monthly allotment applies.
    """
    p = PRICES.get(model)
    if p is None:
        return -1.0
    cost = (max(tin, 0) / 1_000_000.0) * p["in"] + (max(tout, 0) / 1_000_000.0) * p["out"]
    cost += max(grounded_queries, 0) * GROUNDING_USD_PER_QUERY
    return round(cost, 6)

"""engine.ai — Gemini (Vertex) pipeline building blocks: client, pricing,
cost ledger.

The Vertex REST call shape is adapted from `GeminiBridge/bridge.py` (a
live-proven client for the same GCP project); see gemini_client.py's
docstring for exactly what was carried over. Every LLM call in this
package is budget-gated (engine.ai.ledger.Ledger.precheck) and can run in
fixture mode (env TTD_AI_FIXTURE=1) for $0, no-network tests.
"""
from __future__ import annotations

from .gemini_client import GeminiClient, GenResult, ModelUnavailable
from .ledger import BudgetExceeded, Ledger
from .pricing import (GROUNDING_FREE_PROMPTS_PER_MONTH, GROUNDING_USD_PER_QUERY,
                      PRICES, estimate)

__all__ = [
    "GeminiClient", "GenResult", "ModelUnavailable",
    "Ledger", "BudgetExceeded",
    "PRICES", "estimate", "GROUNDING_USD_PER_QUERY", "GROUNDING_FREE_PROMPTS_PER_MONTH",
]

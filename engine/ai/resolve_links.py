"""Resolve Vertex AI Search grounding-redirect URLs to their real final
destination before an article's citations are ever verified or published.

Gemini's `googleSearch` grounding tool returns citation URLs shaped like

    https://vertexaisearch.cloud.google.com/grounding-api-redirect/<opaque>

These are opaque redirect tokens. Google documents them as expiring after
roughly a month, so publishing one verbatim (in front-matter `sources[]`
or an inline body link) would silently rot that citation once the
redirect stops resolving — and citation_gate's `urlContext` check can't
meaningfully verify an opaque redirect anyway; it needs the real url.

This module finds every such url in a block of text (front matter + body
together — a plain string scan naturally covers both), resolves each
UNIQUE url exactly once (one HTTP GET following redirects, no retries),
and substitutes the final resolved url everywhere the original appeared.

Fail-open: a url that fails to resolve is left as-is in the text and
reported in the returned warnings list — this module never raises, so a
transient network hiccup here never hard-fails the writer run.

Fixture/test mode (TTD_AI_FIXTURE=1) does zero network by default; the
resolver function is also a plain injectable callable so tests can verify
substitution / failure-leaves-original behavior without any real HTTP
call, independent of the env-var gate.
"""
from __future__ import annotations

import os
import re

GROUNDING_REDIRECT_RE = re.compile(
    r"https://vertexaisearch\.cloud\.google\.com/grounding-api-redirect/"
    r"[^\s\)\]\"'>]+"
)


def http_resolve(url: str, timeout: float = 15.0) -> str:
    """Default resolver: one GET following redirects, return the final
    landing url. Raises on any network/HTTP-level failure — the caller
    decides the fail-open policy (leave the original url, log a warning)."""
    import requests

    resp = requests.get(url, timeout=timeout, allow_redirects=True)
    resp.close()
    return resp.url


def resolve_single(url: str, *, resolver=http_resolve,
                   fixture: bool | None = None) -> str | None:
    """Resolve ONE url directly — used by ai_research.py (FIX H) to
    resolve every grounding source URI it collects as soon as each
    research call returns, not just ones that happen to match the
    vertexaisearch redirect pattern (a grounding chunk's URI should always
    be resolved to its real destination regardless of shape, since the
    whole point is deep-link fidelity: the writer must never see, and so
    can never cite, an opaque redirect or a URL shortened down to a bare
    domain root).

    `fixture=None` (default) auto-detects TTD_AI_FIXTURE=1 — a no-op that
    returns `url` unchanged, zero network, matching every other module
    here. Pass `fixture=False` with an injected `resolver=` to test
    resolution logic without the real network or the env var.

    Returns the resolved url, or None (never raises) if a live resolution
    attempt fails — the caller decides the fail-open policy (ai_research.py
    buckets these into an 'unresolved' list rather than silently dropping
    or silently keeping the unresolved redirect as if it were safe to cite)."""
    if fixture is None:
        fixture = os.environ.get("TTD_AI_FIXTURE") == "1"
    if fixture:
        return url
    try:
        return resolver(url)
    except Exception:  # noqa: BLE001 — fail-open, caller decides what to do
        return None


def resolve_grounding_links(text: str, *, resolver=http_resolve,
                            fixture: bool | None = None) -> tuple[str, list[dict]]:
    """Find, resolve, and substitute every grounding-redirect url in
    `text`. Returns (new_text, warnings).

    `warnings` is a list of {"url": <original redirect url>, "error": str}
    for urls that failed to resolve — left unchanged in `new_text`, never
    raised.

    `fixture=None` (the default) auto-detects TTD_AI_FIXTURE=1 from the
    environment and skips resolution entirely (zero network) when set —
    matching every other module in this pipeline. Pass `fixture=False`
    explicitly (with an injected `resolver=`) to test substitution logic
    without touching the real network or the env var.
    """
    if fixture is None:
        fixture = os.environ.get("TTD_AI_FIXTURE") == "1"

    urls = sorted(set(GROUNDING_REDIRECT_RE.findall(text)))
    if not urls or fixture:
        return text, []

    warnings: list[dict] = []
    new_text = text
    for url in urls:
        try:
            resolved = resolver(url)
        except Exception as e:  # noqa: BLE001 — fail-open: never block the run
            warnings.append({"url": url, "error": f"{type(e).__name__}: {e}"})
            continue
        if resolved and resolved != url:
            new_text = new_text.replace(url, resolved)
    return new_text, warnings

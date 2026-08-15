"""Tests for engine.ai.citation_gate — the fail-closed citation gate.

Covers the four citation scenarios called out in SPEC.md:
  1. supported                        -> pass
  2. unsupported (fetchable)          -> HARD FAIL
  3. paywalled + corroborated         -> pass
  4. paywalled-only (no corroboration)-> HARD FAIL

Runs with TTD_AI_FIXTURE=1 semantics via the real engine.ai.gemini_client.
GeminiClient + engine.ai.ledger.Ledger, pointed at a fixture_dir passed
explicitly (so no env mutation / no network / no gcloud is ever needed).
Each source's canned verdict lives at
tests/fixtures/ai/citation_check_<i>.json under a per-test tmp_path root —
GeminiClient's fixture lookup is one JSON file per `step` name, and
citation_gate.py calls generate(step=f"citation_check_{i}", ...) once per
front-matter source (index i), so each source gets its own canned verdict.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from engine.ai.citation_gate import CitationGateError, _is_error_verdict, run
from engine.ai.gemini_client import GeminiClient
from engine.ai.ledger import Ledger

DATE = "2026-08-15"
SLUG = "test-article"

STYLE_MD = "# style\nBe accurate.\n"
CITATION_CHECK_MD = (
    "<!-- v1 | test fixture | placeholders: {{like_this}} -->\n"
    "{{style}}\n\nCheck whether {{url}} supports: {{claim}}\n"
)


def _cfg() -> dict:
    return {
        "llm": {
            "model_fast": "gemini-2.5-flash-lite",
            "location": "global",
            "daily_budget_usd": 100.0,
            "max_grounded_queries_per_run": 1000,
            "max_url_fetches_per_run": 1000,
        }
    }


def _make_root(tmp_path: Path) -> Path:
    (tmp_path / "prompts" / "v1").mkdir(parents=True, exist_ok=True)
    (tmp_path / "prompts" / "v1" / "_style.md").write_text(STYLE_MD, encoding="utf-8")
    (tmp_path / "prompts" / "v1" / "citation_check.md").write_text(
        CITATION_CHECK_MD, encoding="utf-8")
    (tmp_path / "content" / "articles").mkdir(parents=True, exist_ok=True)
    (tmp_path / "tests" / "fixtures" / "ai").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _write_article(root: Path, sources: list, body: str, description: str = "") -> Path:
    fm = {
        "title": "Test Article", "slug": SLUG, "date": DATE, "hub": "ai-tools",
        "description": description,
        "sources": sources,
        "review": {"facts_verified": False, "sources_checked": False,
                   "title_promise_check": True, "no_fabrication": True,
                   "policy_pass": True},
    }
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n" + body + "\n"
    path = root / "content" / "articles" / f"{DATE}-{SLUG}.md"
    path.write_text(text, encoding="utf-8")
    return path


def _write_sources_pool(root: Path, entries: list) -> None:
    p = root / "data" / "briefs" / f"{DATE}-sources.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries), encoding="utf-8")


# The four canonical scenario fixtures live at tests/fixtures/ai/ in the
# repo (SPEC.md: "citation fixtures cover: supported, unsupported->fail,
# paywalled-with-corroboration->pass, paywalled-only->fail") and are copied
# here into the per-run, per-source-index filename GeminiClient's fixture
# mode looks up (`citation_check_<i>.json`), since one gate run makes one
# generate() call per front-matter source and each needs its own verdict.
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ai"


def _use_canonical_fixture(root: Path, index: int, name: str) -> None:
    src = FIXTURES_DIR / f"citation_check_{name}.json"
    dst = root / "tests" / "fixtures" / "ai" / f"citation_check_{index}.json"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _write_verdict_fixture(root: Path, index: int, supported: bool, fetch_ok: bool,
                           quote: str = "", reason: str = "") -> None:
    """Ad-hoc verdict for edge cases the four canonical fixtures don't cover
    verbatim (kept alongside them, not a replacement)."""
    verdict = {"supported": supported, "quote": quote, "fetch_ok": fetch_ok,
               "reason": reason}
    payload = {
        "text": json.dumps(verdict), "usage": {"in": 10, "out": 10, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 1 if fetch_ok else 0,
        "sources": [], "finish_reason": "STOP", "model": "gemini-2.5-flash-lite",
    }
    (root / "tests" / "fixtures" / "ai" / f"citation_check_{index}.json").write_text(
        json.dumps(payload), encoding="utf-8")


def _client(root: Path) -> GeminiClient:
    ledger = Ledger(_cfg()["llm"], run_id="test-run", root=root)
    return GeminiClient(_cfg()["llm"], ledger,
                        fixture_dir=str(root / "tests" / "fixtures" / "ai"), root=root)


# ---------------- scenario 1: supported -> pass ----------------

def test_supported_source_passes(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Primary source", "url": "https://example.com/a", "primary": True}]
    body = "The company [raised $10 million](https://example.com/a) last week."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is True
    assert report["hard_failures"] == 0
    assert report["sources"][0]["supported"] is True
    # front matter was edited on pass
    updated = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(updated.split("---\n", 2)[1])
    assert fm["review"]["facts_verified"] is True
    assert fm["review"]["sources_checked"] is True
    assert "unverified" not in fm["sources"][0]
    # report file written
    rep_path = root / "data" / "gate-reports" / f"{DATE}-{SLUG}-citations.json"
    assert rep_path.exists()
    assert json.loads(rep_path.read_text(encoding="utf-8"))["passed"] is True


# ---------------- scenario 2: unsupported (fetchable) -> HARD FAIL ----------------

def test_unsupported_fetchable_source_fails(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Contradicted source", "url": "https://example.com/b"}]
    body = "The company [raised $10 million](https://example.com/b) last week."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "unsupported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is False
    assert report["hard_failures"] == 1
    assert report["failures"][0]["type"] == "unsupported"
    # front matter must NOT be edited on failure (fail-closed)
    original = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(original.split("---\n", 2)[1])
    assert fm["review"]["facts_verified"] is False


# ---------------- scenario 3: paywalled + corroborated -> pass ----------------

def test_paywalled_source_with_corroboration_passes(tmp_path):
    root = _make_root(tmp_path)
    sources = [
        {"title": "Paywalled outlet", "url": "https://paywalled.example.com/story"},
        {"title": "Open wire report", "url": "https://wire.example.com/story"},
    ]
    claim = "the company raised $50 million in new funding"
    body = (f"According to a paywalled report, [{claim}](https://paywalled.example.com/story). "
           f"A wire service independently reported [{claim}](https://wire.example.com/story).")
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "paywalled")
    _use_canonical_fixture(root, 1, "corroborating")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is True
    assert report["hard_failures"] == 0
    updated = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(updated.split("---\n", 2)[1])
    assert fm["review"]["facts_verified"] is True
    paywalled_src = next(s for s in fm["sources"] if s["url"] == "https://paywalled.example.com/story")
    assert paywalled_src["unverified"] == "paywalled"
    open_src = next(s for s in fm["sources"] if s["url"] == "https://wire.example.com/story")
    assert "unverified" not in open_src


# ---------------- scenario 4: paywalled-only -> HARD FAIL ----------------

def test_paywalled_only_source_fails(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Paywalled-only outlet", "url": "https://paywalled.example.com/lonely"}]
    body = "The company [raised $50 million in new funding](https://paywalled.example.com/lonely)."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "paywalled")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is False
    assert report["hard_failures"] == 1
    assert report["failures"][0]["type"] == "uncorroborated_paywalled"
    original = (root / "content" / "articles" / f"{DATE}-{SLUG}.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(original.split("---\n", 2)[1])
    assert fm["review"]["sources_checked"] is False


# ---------------- infra / edge cases ----------------

def test_missing_article_raises_infra_error(tmp_path):
    root = _make_root(tmp_path)
    with pytest.raises(CitationGateError):
        run(DATE, "no-such-slug", _client(root), _cfg(), root=root)


def test_malformed_verdict_json_is_fail_closed(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Weird source", "url": "https://example.com/weird"}]
    body = "As [reported](https://example.com/weird), the sky is blue."
    _write_article(root, sources, body)
    # not valid JSON -> _parse_verdict must fail closed, not raise/pass
    payload = {"text": "not json at all", "usage": {"in": 1, "out": 1, "thinking": 0},
              "grounded_queries": 0, "url_fetches": 0, "sources": [],
              "finish_reason": "STOP", "model": "gemini-2.5-flash-lite"}
    (root / "tests" / "fixtures" / "ai" / "citation_check_0.json").write_text(
        json.dumps(payload), encoding="utf-8")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is False
    assert report["sources"][0]["fetch_ok"] is False
    assert report["sources"][0]["supported"] is False


# ---------------- FIX F: no json_schema with urlContext + lenient parse ----------------

def test_check_call_never_passes_json_schema(tmp_path, monkeypatch):
    # Vertex 400s if json_schema + urlContext are combined — the
    # citation-check call site must never pass json_schema, full stop.
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/a"}]
    body = "The company [raised $10 million](https://example.com/a) last week."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")
    client = _client(root)

    captured = {}
    real_generate = client.generate

    def spy(*args, **kwargs):
        captured.update(kwargs)
        return real_generate(*args, **kwargs)

    monkeypatch.setattr(client, "generate", spy)

    run(DATE, SLUG, client, _cfg(), root=root)

    assert "json_schema" not in captured or captured["json_schema"] is None
    assert captured["tools"] == [{"urlContext": {}}]


def test_lenient_parse_accepts_markdown_fenced_json(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/fenced"}]
    body = "The company [raised $10 million](https://example.com/fenced) last week."
    _write_article(root, sources, body)
    verdict = {"supported": True, "quote": "raised $10 million", "fetch_ok": True,
               "reason": "matches"}
    payload = {
        "text": "```json\n" + json.dumps(verdict) + "\n```",
        "usage": {"in": 10, "out": 10, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 1, "sources": [],
        "finish_reason": "STOP", "model": "gemini-2.5-flash-lite",
    }
    (root / "tests" / "fixtures" / "ai" / "citation_check_0.json").write_text(
        json.dumps(payload), encoding="utf-8")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is True
    assert report["sources"][0]["supported"] is True
    assert report["sources"][0]["quote"] == "raised $10 million"


def test_lenient_parse_accepts_leading_and_trailing_commentary(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/chatty"}]
    body = "The company [raised $10 million](https://example.com/chatty) last week."
    _write_article(root, sources, body)
    verdict = {"supported": True, "quote": "raised $10 million", "fetch_ok": True,
               "reason": "matches"}
    payload = {
        "text": ("Sure, here is the verdict:\n" + json.dumps(verdict)
                 + "\nLet me know if you need anything else!"),
        "usage": {"in": 10, "out": 10, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 1, "sources": [],
        "finish_reason": "STOP", "model": "gemini-2.5-flash-lite",
    }
    (root / "tests" / "fixtures" / "ai" / "citation_check_0.json").write_text(
        json.dumps(payload), encoding="utf-8")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is True
    assert report["sources"][0]["supported"] is True


def test_lenient_parse_handles_brace_inside_quoted_string_value(tmp_path):
    # a brace inside a JSON string VALUE must not throw off the balanced-
    # brace scan
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/braces"}]
    body = "The formula [is {x=1}](https://example.com/braces) apparently."
    _write_article(root, sources, body)
    payload = {
        "text": '{"supported": true, "quote": "the value is {x=1} exactly", '
               '"fetch_ok": true, "reason": "ok"}',
        "usage": {"in": 10, "out": 10, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 1, "sources": [],
        "finish_reason": "STOP", "model": "gemini-2.5-flash-lite",
    }
    (root / "tests" / "fixtures" / "ai" / "citation_check_0.json").write_text(
        json.dumps(payload), encoding="utf-8")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is True
    assert report["sources"][0]["quote"] == "the value is {x=1} exactly"


def test_unparseable_verdict_reason_is_explicit(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/garbage"}]
    body = "As [reported](https://example.com/garbage), nothing useful here."
    _write_article(root, sources, body)
    payload = {"text": "I refuse to answer in JSON.", "usage": {"in": 1, "out": 1, "thinking": 0},
              "grounded_queries": 0, "url_fetches": 0, "sources": [],
              "finish_reason": "STOP", "model": "gemini-2.5-flash-lite"}
    (root / "tests" / "fixtures" / "ai" / "citation_check_0.json").write_text(
        json.dumps(payload), encoding="utf-8")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    assert passed is False
    assert "unparseable verdict" in report["sources"][0]["reason"]


# ---------------- FIX G: claim = sentence, not link anchor text ----------------

def test_claim_is_full_sentence_not_anchor_text(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/sentence"}]
    body = ("Intro paragraph, unrelated to the source.\n\n"
            "FixtureCorp announced a new product today, according to the "
            "[official blog](https://example.com/sentence). It ships next month.")
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    claims = report["sources"][0]["claims"]
    assert len(claims) == 1
    # the claim is NOT just the bare anchor text on its own...
    assert claims[0] != "official blog"
    # ...it's the full sentence, with the anchor text folded in as prose
    assert claims[0] == "FixtureCorp announced a new product today, according to the official blog."
    assert "It ships next month" not in claims[0]        # only the sentence WITH the link
    assert "[" not in claims[0] and "](" not in claims[0]  # markdown link syntax stripped


def test_claim_falls_back_to_whole_paragraph_when_no_sentence_boundary(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/nodot"}]
    # no terminal punctuation at all -> ambiguous -> whole paragraph
    body = "See [this page](https://example.com/nodot) for the full announcement"
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    claims = report["sources"][0]["claims"]
    assert claims == ["See this page for the full announcement"]


def test_claim_falls_back_to_paragraph_when_link_spans_a_false_split(tmp_path):
    # an abbreviation INSIDE the anchor text ("L.P. News") looks like a
    # sentence boundary to the naive splitter — the link's own span then
    # crosses that false boundary, which must fall back to the whole
    # paragraph rather than return a truncated, unclosed "[" fragment.
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/amb"}]
    body = ("This deal was reported by [Bloomberg L.P. News]"
           "(https://example.com/amb) on Tuesday. Analysts agreed.")
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    claims = report["sources"][0]["claims"]
    assert len(claims) == 1
    # ambiguous (the link's own span crosses a false split inside its
    # anchor text) -> falls all the way back to the WHOLE paragraph,
    # not a truncated fragment with a dangling unclosed "["
    assert claims[0] == ("This deal was reported by Bloomberg L.P. News "
                         "on Tuesday. Analysts agreed.")
    assert "[" not in claims[0]


def test_claims_capped_at_three_first_occurrences_deduped(tmp_path):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/repeat"}]
    body = "\n\n".join(
        f"Mention number {i} of the [source](https://example.com/repeat) here."
        for i in range(5)
    )
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    claims = report["sources"][0]["claims"]
    assert len(claims) == 3
    assert "Mention number 0" in claims[0]
    assert "Mention number 1" in claims[1]
    assert "Mention number 2" in claims[2]


def test_claim_falls_back_to_description_plus_sources_pool_title(tmp_path, monkeypatch):
    # a front-matter source never linked inline in the body — synthesize a
    # claim from the article's own description + the source pool's title
    root = _make_root(tmp_path)
    sources = [{"title": "Unlinked source", "url": "https://example.com/unlinked"}]
    body = "This paragraph never mentions the source url at all."
    _write_article(root, sources, body,
                  description="FixtureCorp launched a new benchmark this week.")
    _write_sources_pool(root, [
        {"url": "https://example.com/unlinked", "title": "FixtureCorp benchmark launch — official"},
    ])
    client = _client(root)

    captured = {}
    real_generate = client.generate

    def spy(*args, **kwargs):
        captured["contents"] = kwargs.get("contents")
        return real_generate(*args, **kwargs)

    monkeypatch.setattr(client, "generate", spy)
    _use_canonical_fixture(root, 0, "supported")

    passed, report = run(DATE, SLUG, client, _cfg(), root=root)

    assert report["sources"][0]["needs_corroboration"] is False
    claims = report["sources"][0]["claims"]
    assert len(claims) == 1
    assert "FixtureCorp launched a new benchmark this week" in claims[0]
    assert "FixtureCorp benchmark launch" in claims[0]
    # the model actually received the synthesized claim, not a blank one
    assert "FixtureCorp launched a new benchmark this week" in captured["contents"]


def test_needs_corroboration_when_no_claim_and_no_sources_pool_entry(tmp_path):
    # no body link, no data/briefs/<date>-sources.json entry, no other
    # verified source in the article -> HARD FAIL, never an invented claim
    root = _make_root(tmp_path)
    sources = [{"title": "Mystery source", "url": "https://example.com/mystery"}]
    body = "This paragraph never mentions the source url at all."
    _write_article(root, sources, body, description="Some description.")
    # no sources.json written at all

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    row = report["sources"][0]
    assert row["needs_corroboration"] is True
    assert row["claims"] == []
    assert passed is False
    assert report["failures"][0]["type"] == "needs_corroboration_unmet"


def test_needs_corroboration_passes_when_another_source_is_verified(tmp_path):
    # same as above, but a SECOND source in the article IS independently
    # fetch_ok+supported -> the needs_corroboration source is allowed
    # through (weak bar: the article has SOME independently-verified
    # backing), even though nothing backs this specific citation by name
    root = _make_root(tmp_path)
    sources = [
        {"title": "Mystery source", "url": "https://example.com/mystery2"},
        {"title": "Verified source", "url": "https://example.com/verified"},
    ]
    body = ("According to the [official announcement]"
           "(https://example.com/verified), the product shipped today.")
    _write_article(root, sources, body, description="Some description.")
    # source 0 (mystery2): never linked, no sources.json entry -> needs_corroboration
    # source 1 (verified): linked + will be scripted as supported
    _use_canonical_fixture(root, 1, "supported")

    passed, report = run(DATE, SLUG, _client(root), _cfg(), root=root)

    mystery_row = next(s for s in report["sources"] if s["url"] == "https://example.com/mystery2")
    assert mystery_row["needs_corroboration"] is True
    assert passed is True
    assert report["hard_failures"] == 0


# ---------------- FIX I: error-outcome retry (never re-verdict) ----------------

def test_is_error_verdict_classifies_call_errors_and_unparseable_as_error():
    assert _is_error_verdict({"reason": "gate call error: RuntimeError: boom"}) is True
    assert _is_error_verdict({"reason": "unparseable verdict: no JSON object found"}) is True


def test_is_error_verdict_does_not_classify_a_clean_verdict_as_error():
    assert _is_error_verdict({"reason": "source did not support the claim"}) is False
    assert _is_error_verdict({"reason": ""}) is False
    assert _is_error_verdict({"reason": "needs_corroboration: no claim could be constructed"}) is False


def test_error_then_success_is_retried_once_and_passes(tmp_path, monkeypatch):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/flaky"}]
    body = "The company [raised $10 million](https://example.com/flaky) last week."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "supported")
    client = _client(root)
    real_generate = client.generate

    calls: list[str] = []

    def flaky_generate(*args, **kwargs):
        calls.append(kwargs.get("note", ""))
        if len(calls) == 1:
            raise RuntimeError("transient network blip")
        return real_generate(*args, **kwargs)

    monkeypatch.setattr(client, "generate", flaky_generate)

    passed, report = run(DATE, SLUG, client, _cfg(), root=root)

    assert passed is True
    assert report["sources"][0]["supported"] is True
    assert len(calls) == 2           # initial attempt + exactly one retry
    assert calls[0] == ""            # first attempt: not tagged as a retry
    assert calls[1] == "retry"       # second attempt: tagged for the ledger


def test_error_then_error_fails_closed_after_exactly_one_retry(tmp_path, monkeypatch):
    root = _make_root(tmp_path)
    sources = [{"title": "Source", "url": "https://example.com/always-broken"}]
    body = "The company [raised $10 million](https://example.com/always-broken) last week."
    _write_article(root, sources, body)
    # deliberately NO citation_check_0.json fixture -> every call to the
    # real client.generate() raises "fixture mode: no fixture at ..."
    client = _client(root)
    real_generate = client.generate

    calls: list[str] = []

    def counting_generate(*args, **kwargs):
        calls.append(kwargs.get("note", ""))
        return real_generate(*args, **kwargs)

    monkeypatch.setattr(client, "generate", counting_generate)

    passed, report = run(DATE, SLUG, client, _cfg(), root=root)

    assert passed is False
    row = report["sources"][0]
    assert row["fetch_ok"] is False
    assert row["supported"] is False
    assert "gate call error" in row["reason"]
    assert len(calls) == 2           # initial attempt + exactly one retry, then stop
    assert calls == ["", "retry"]


def test_supported_false_verdict_is_never_retried(tmp_path, monkeypatch):
    root = _make_root(tmp_path)
    sources = [{"title": "Contradicted source", "url": "https://example.com/b"}]
    body = "The company [raised $10 million](https://example.com/b) last week."
    _write_article(root, sources, body)
    _use_canonical_fixture(root, 0, "unsupported")
    client = _client(root)
    real_generate = client.generate

    calls: list[str] = []

    def counting_generate(*args, **kwargs):
        calls.append(kwargs.get("note", ""))
        return real_generate(*args, **kwargs)

    monkeypatch.setattr(client, "generate", counting_generate)

    passed, report = run(DATE, SLUG, client, _cfg(), root=root)

    assert passed is False
    assert report["sources"][0]["supported"] is False
    # a genuine editorial supported=False verdict — must NOT be retried
    assert len(calls) == 1
    assert calls[0] == ""

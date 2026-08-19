"""Tests for engine.ai.resolve_links — grounding-redirect url resolution
(FIX E). Zero network: every test injects a fake resolver or exercises the
fixture-mode auto-skip; nothing here ever calls `requests` for real.
"""
from __future__ import annotations

from engine.ai.resolve_links import GROUNDING_REDIRECT_RE, resolve_grounding_links

REDIRECT_1 = ("https://vertexaisearch.cloud.google.com/grounding-api-redirect/"
              "AbCdEf123")
REDIRECT_2 = ("https://vertexaisearch.cloud.google.com/grounding-api-redirect/"
              "XyZ789")
REAL_1 = "https://real-source.example/article-one"
REAL_2 = "https://real-source.example/article-two"


def test_regex_matches_a_grounding_redirect_url():
    assert GROUNDING_REDIRECT_RE.search(REDIRECT_1)
    assert not GROUNDING_REDIRECT_RE.search("https://real-source.example/x")


def test_no_grounding_urls_present_is_a_noop():
    text = f"# Title\n\nSome text with a [normal link]({REAL_1}) and no redirects.\n"
    calls = []

    def resolver(url):
        calls.append(url)
        return REAL_1

    new_text, warnings = resolve_grounding_links(text, resolver=resolver, fixture=False)

    assert new_text == text
    assert warnings == []
    assert calls == []  # resolver never invoked — nothing to resolve


def test_substitutes_a_single_redirect_url_everywhere_it_appears():
    text = (
        "---\nsources:\n"
        f'  - {{title: "S", url: "{REDIRECT_1}"}}\n'
        "---\n\n"
        f"Body text with an inline [claim]({REDIRECT_1}) citing the same url.\n"
    )

    def resolver(url):
        assert url == REDIRECT_1
        return REAL_1

    new_text, warnings = resolve_grounding_links(text, resolver=resolver, fixture=False)

    assert warnings == []
    assert REDIRECT_1 not in new_text
    assert new_text.count(REAL_1) == 2  # both occurrences (front matter + body) replaced


def test_dedupes_and_resolves_each_unique_url_exactly_once():
    text = (
        f"[a]({REDIRECT_1}) [b]({REDIRECT_1}) [c]({REDIRECT_2})\n"
    )
    call_counts: dict[str, int] = {}

    def resolver(url):
        call_counts[url] = call_counts.get(url, 0) + 1
        return REAL_1 if url == REDIRECT_1 else REAL_2

    new_text, warnings = resolve_grounding_links(text, resolver=resolver, fixture=False)

    assert call_counts == {REDIRECT_1: 1, REDIRECT_2: 1}  # each unique url resolved ONCE
    assert warnings == []
    assert new_text.count(REAL_1) == 2
    assert new_text.count(REAL_2) == 1


def test_failure_to_resolve_leaves_original_url_and_reports_warning():
    text = f"See [source]({REDIRECT_1}) for details.\n"

    def resolver(url):
        raise TimeoutError("connection timed out")

    new_text, warnings = resolve_grounding_links(text, resolver=resolver, fixture=False)

    assert new_text == text  # unchanged — fail-open
    assert len(warnings) == 1
    assert warnings[0]["url"] == REDIRECT_1
    assert "TimeoutError" in warnings[0]["error"]
    assert "connection timed out" in warnings[0]["error"]


def test_partial_failure_resolves_the_good_url_and_warns_on_the_bad_one():
    text = f"[good]({REDIRECT_1}) [bad]({REDIRECT_2})\n"

    def resolver(url):
        if url == REDIRECT_2:
            raise ConnectionError("refused")
        return REAL_1

    new_text, warnings = resolve_grounding_links(text, resolver=resolver, fixture=False)

    assert REDIRECT_1 not in new_text
    assert REAL_1 in new_text
    assert REDIRECT_2 in new_text  # left as-is
    assert len(warnings) == 1
    assert warnings[0]["url"] == REDIRECT_2


def test_resolver_returning_same_url_is_not_treated_as_a_substitution():
    text = f"[x]({REDIRECT_1})\n"

    def resolver(url):
        return url  # redirect "resolves" to itself — nothing to substitute

    new_text, warnings = resolve_grounding_links(text, resolver=resolver, fixture=False)

    assert new_text == text
    assert warnings == []


def test_fixture_true_skips_resolution_even_with_urls_present():
    text = f"[x]({REDIRECT_1})\n"
    calls = []

    def resolver(url):
        calls.append(url)
        return REAL_1

    new_text, warnings = resolve_grounding_links(text, resolver=resolver, fixture=True)

    assert new_text == text
    assert warnings == []
    assert calls == []  # network resolver never invoked in fixture mode


def test_env_ttd_ai_fixture_auto_skips_when_fixture_kwarg_omitted(monkeypatch):
    monkeypatch.setenv("TTD_AI_FIXTURE", "1")
    text = f"[x]({REDIRECT_1})\n"
    calls = []

    def resolver(url):
        calls.append(url)
        return REAL_1

    new_text, warnings = resolve_grounding_links(text, resolver=resolver)

    assert new_text == text
    assert calls == []


def test_env_not_fixture_and_fixture_kwarg_omitted_does_resolve(monkeypatch):
    monkeypatch.delenv("TTD_AI_FIXTURE", raising=False)
    text = f"[x]({REDIRECT_1})\n"

    def resolver(url):
        return REAL_1

    new_text, warnings = resolve_grounding_links(text, resolver=resolver)

    assert REAL_1 in new_text
    assert warnings == []


def test_default_resolver_is_http_resolve_and_never_called_when_no_urls():
    # sanity: calling with the real default resolver but text with no
    # redirect urls must never attempt any network call (no exception,
    # no hang) — proves the "no urls -> skip entirely" short-circuit runs
    # before the resolver is ever touched.
    text = "Nothing to see here.\n"
    new_text, warnings = resolve_grounding_links(text, fixture=False)
    assert new_text == text
    assert warnings == []

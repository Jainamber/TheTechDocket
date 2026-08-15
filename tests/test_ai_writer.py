"""Tests for engine.ai.ai_select / ai_research / ai_write (SPEC.md Agent B).

Runs entirely in fixture mode (TTD_AI_FIXTURE=1 equivalent: GeminiClient is
constructed with an explicit fixture_dir) — zero network, zero gcloud, $0.
Uses the REAL engine.ai.gemini_client.GeminiClient + engine.ai.ledger.Ledger
(Agent A) against a tmp_path repo tree (via each module's `root` kwarg), so
these tests also exercise the real fixture-mode contract, not a hand-rolled
stand-in — except for the one retry-exhaustion case where a purpose-built
tiny fixture (in a separate tmp fixture dir) simulates two consecutive bad
drafts, which the shared canonical fixtures can't do since fixture replay is
stateless (same file, every call).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from engine.ai import ai_research, ai_select, ai_write
from engine.ai.gemini_client import GeminiClient, ModelUnavailable
from engine.ai.ledger import BudgetExceeded, Ledger

REPO_ROOT = Path(__file__).resolve().parent.parent
REAL_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "ai"
DATE = "2026-08-15"


def _llm_cfg(**overrides) -> dict:
    base = {
        "location": "global",
        "model_writer": "gemini-3.5-flash",
        "writer_thinking": "high",
        "writer_max_output": 65536,
        "model_writer_fallbacks": ["gemini-2.5-pro"],
        "model_research": "gemini-3.5-flash",
        "model_research_fallbacks": ["gemini-2.5-flash"],
        "model_fast": "gemini-2.5-flash-lite",
        "daily_budget_usd": 2.00,
        "max_grounded_queries_per_run": 12,
        "max_url_fetches_per_run": 25,
        "max_retry_rewrites": 1,
    }
    base.update(overrides)
    return {"llm": base}


def _client(tmp_path: Path, fixture_dir: Path = REAL_FIXTURE_DIR, **llm_overrides) -> GeminiClient:
    cfg = _llm_cfg(**llm_overrides)
    ledger = Ledger(cfg["llm"], run_id="test-run", root=tmp_path)
    return GeminiClient(cfg["llm"], ledger, fixture_dir=str(fixture_dir), root=tmp_path)


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------- ai_select

def _candidates(n=3) -> dict:
    return {
        "date": DATE,
        "use_evergreen": False,
        "candidates": [
            {"title": f"Candidate {i}", "score": 0.5 - i * 0.05, "sources": ["hn"],
             "geos": [], "evidence": []}
            for i in range(n)
        ],
    }


def test_ai_select_happy_override_rewrites_candidates(tmp_path):
    cand_path = tmp_path / "data" / "briefs" / f"{DATE}-candidates.json"
    _write_json(cand_path, _candidates())
    client = _client(tmp_path)
    cfg = _llm_cfg()

    result = ai_select.run(DATE, client, cfg, root=tmp_path)

    # select.json fixture returns pick_rank=1, override=true
    assert result["pick_rank"] == 1
    assert result["override"] is True
    assert "reason" in result

    out_path = tmp_path / "data" / "briefs" / f"{DATE}-ai-select.json"
    assert out_path.exists()
    assert json.loads(out_path.read_text(encoding="utf-8")) == result

    # override must be fed back into candidates.json so the unmodified
    # engine.brief.build_brief() picks it up
    rewritten = json.loads(cand_path.read_text(encoding="utf-8"))
    assert rewritten["pick"]["title"] == "Candidate 1"
    assert rewritten["selection_note"] == result["reason"]


def test_ai_select_missing_candidates_file_is_mechanical_and_never_blocks(tmp_path):
    cfg = _llm_cfg()
    result = ai_select.run(DATE, client=None, cfg=cfg, root=tmp_path)

    assert result["pick_rank"] == 0
    assert result["override"] is False
    assert "note" in result
    out_path = tmp_path / "data" / "briefs" / f"{DATE}-ai-select.json"
    assert out_path.exists()


def test_ai_select_use_evergreen_skips_model_call(tmp_path):
    cand_path = tmp_path / "data" / "briefs" / f"{DATE}-candidates.json"
    _write_json(cand_path, {"date": DATE, "use_evergreen": True, "candidates": []})
    # client=None proves the model is never invoked on this path
    result = ai_select.run(DATE, client=None, cfg=_llm_cfg(), root=tmp_path)
    assert result == {"pick_rank": 0, "override": False,
                      "reason": "use_evergreen or no candidates — ai_select skipped, mechanical pick used",
                      "note": "use_evergreen or no candidates — ai_select skipped, mechanical pick used"}


def test_ai_select_model_failure_falls_back_mechanically(tmp_path):
    cand_path = tmp_path / "data" / "briefs" / f"{DATE}-candidates.json"
    _write_json(cand_path, _candidates())
    # a fixture_dir with no select.json -> GeminiClient.generate() raises
    empty_fixtures = tmp_path / "empty_fixtures"
    empty_fixtures.mkdir()
    client = _client(tmp_path, fixture_dir=empty_fixtures)

    result = ai_select.run(DATE, client, _llm_cfg(), root=tmp_path)

    assert result["pick_rank"] == 0
    assert result["override"] is False
    assert "ai_select failed" in result["note"]
    # candidates.json must be untouched on failure
    unchanged = json.loads(cand_path.read_text(encoding="utf-8"))
    assert "selection_note" not in unchanged


# --------------------------------------------------------------- ai_research

def test_ai_research_happy_aggregates_notes_and_sources(tmp_path):
    brief_path = tmp_path / "data" / "briefs" / f"{DATE}.md"
    brief_path.parent.mkdir(parents=True, exist_ok=True)
    brief_path.write_text("# Article Brief\n\nSome brief text.\n", encoding="utf-8")
    client = _client(tmp_path, max_grounded_queries_per_run=3)

    pack = ai_research.run(DATE, "some-slug-hint", client, _llm_cfg(max_grounded_queries_per_run=3),
                           root=tmp_path)

    # The research.json fixture reports grounded_queries=2 per call, so the
    # ledger's own cumulative cap (3) is what actually stops the loop first
    # (after 2 calls = 4 used), before the code-level angle-count cap (3)
    # would have: this is exactly SPEC.md's "enforced by the ledger caps,
    # not by trusting the model" behavior.
    assert pack.queries_run == ["primary_source", "verify_numbers"]
    assert pack.grounded_queries_used == 2 * 2
    assert len(pack.sources) == 2  # deduped fixture sources
    assert all(s["url"].startswith("https://") for s in pack.sources)
    assert pack.notes_path.exists()
    assert "primary_source" in pack.notes_path.read_text(encoding="utf-8")
    assert json.loads(pack.sources_path.read_text(encoding="utf-8")) == pack.sources


def test_ai_research_stops_early_on_budget_and_keeps_partial_results(tmp_path):
    brief_path = tmp_path / "data" / "briefs" / f"{DATE}.md"
    brief_path.parent.mkdir(parents=True, exist_ok=True)
    brief_path.write_text("# Article Brief\n\nSome brief text.\n", encoding="utf-8")
    # ledger-level cap of 5: fixture reports grounded_queries=2/call, so the
    # 4th call's precheck (cumulative 6 >= 5) must raise BudgetExceeded
    # before the code-level cap (6, i.e. every angle) would have stopped it
    client = _client(tmp_path, max_grounded_queries_per_run=5)

    pack = ai_research.run(DATE, None, client, _llm_cfg(max_grounded_queries_per_run=5),
                           root=tmp_path)

    assert len(pack.queries_run) == 3
    assert pack.grounded_queries_used == 6
    assert "stopped at" in pack.note
    assert pack.notes_path.exists()  # partial results are still written


def test_ai_research_missing_brief_raises(tmp_path):
    client = _client(tmp_path)
    with pytest.raises(SystemExit):
        ai_research.run(DATE, None, client, _llm_cfg(), root=tmp_path)


# ------------------------------------------------------------------ ai_write

def _seed_write_inputs(tmp_path: Path) -> None:
    briefs = tmp_path / "data" / "briefs"
    briefs.mkdir(parents=True, exist_ok=True)
    (briefs / f"{DATE}.md").write_text("# Article Brief\n\nWrite about FixtureCorp Aurora.\n",
                                       encoding="utf-8")
    (briefs / f"{DATE}-research.md").write_text("## primary_source\n\nFixture notes.\n",
                                                encoding="utf-8")
    _write_json(briefs / f"{DATE}-sources.json",
               [{"url": "https://fixturecorp.example/blog/aurora-launch",
                 "title": "Introducing Aurora", "supports": True, "primary_guess": True}])


def test_ai_write_happy_path_writes_complete_valid_article(tmp_path):
    _seed_write_inputs(tmp_path)
    client = _client(tmp_path)

    out_path = ai_write.run(DATE, client, _llm_cfg(), root=tmp_path)

    assert out_path.exists()
    assert out_path.parent == tmp_path / "content" / "articles"
    raw = out_path.read_text(encoding="utf-8")
    m = ai_write.FM_RE.match(raw)
    assert m, "written article must be a valid ---front matter---\\nbody document"
    meta = yaml.safe_load(m.group(1))

    # placeholders resolved: real date, and a real (non-placeholder) slug
    assert meta["date"] == DATE
    assert meta["slug"] != "{{ARTICLE_SLUG}}"
    assert meta["slug"] in out_path.name
    assert out_path.name == f"{DATE}-{meta['slug']}.md"

    # required fields present and structurally sound
    for field in ["title", "hub", "description", "hero_alt", "keyword", "original_value"]:
        assert meta.get(field)
    assert meta["hub"] == "ai-tools"
    assert isinstance(meta["sources"], list) and meta["sources"]
    assert isinstance(meta["faq"], list) and meta["faq"]

    # review.* flags must be false in the draft (citation gate flips them)
    for k in ai_write.REVIEW_BOOL_KEYS:
        assert meta["review"][k] is False
    assert meta["review"]["reviewed_at"]

    body = raw.split("---\n", 2)[2] if raw.count("---\n") >= 2 else m.group(2)
    body = m.group(2)
    word_count = len(__import__("re").findall(r"\w+", body))
    assert word_count >= 900, f"fixture article body must be 900+ words, got {word_count}"
    assert body.count("## ") >= 3


def test_ai_write_slug_deduped_against_existing_articles(tmp_path):
    _seed_write_inputs(tmp_path)
    # pre-seed a colliding article on disk so dedupe must kick in; the
    # fixture's title slugifies to "fixturecorp-aurora-transparent-ai-coding"
    existing_dir = tmp_path / "content" / "articles"
    existing_dir.mkdir(parents=True, exist_ok=True)
    from engine.util import slugify
    from engine.ai.ai_write import PROMPT_PATH  # noqa: F401 (sanity: prompt file exists)
    colliding_slug = slugify("FixtureCorp Aurora: A More Transparent AI Coding Benchmark")
    (existing_dir / f"{DATE}-{colliding_slug}.md").write_text("placeholder", encoding="utf-8")

    client = _client(tmp_path)
    out_path = ai_write.run(DATE, client, _llm_cfg(), root=tmp_path)

    assert out_path.name != f"{DATE}-{colliding_slug}.md"
    assert out_path.name == f"{DATE}-{colliding_slug}-2.md"


def test_ai_write_retry_feedback_is_included_in_prompt(tmp_path, monkeypatch):
    _seed_write_inputs(tmp_path)
    client = _client(tmp_path)

    captured = {}
    real_generate_with_fallback = client.generate_with_fallback

    def spy(step, models, **kw):
        captured["contents"] = kw["contents"]
        return real_generate_with_fallback(step, models, **kw)

    monkeypatch.setattr(client, "generate_with_fallback", spy)

    ai_write.run(DATE, client, _llm_cfg(), retry_feedback="S07-word-count: too short",
                 root=tmp_path)

    prompt_text = captured["contents"][0]["parts"][0]["text"]
    assert "S07-word-count: too short" in prompt_text


def test_ai_write_raises_after_one_bounded_reask_on_bad_front_matter(tmp_path):
    _seed_write_inputs(tmp_path)
    # A dedicated fixture dir whose write.json is structurally invalid
    # (missing the review block) on every call — fixture replay is
    # stateless, so this proves the "exactly one retry, then raise" path.
    bad_fixtures = tmp_path / "bad_fixtures"
    bad_fixtures.mkdir()
    _write_json(bad_fixtures / "write.json", {
        "text": "```markdown\n---\ntitle: \"Too Short\"\nslug: \"{{ARTICLE_SLUG}}\"\n"
                "date: \"{{ARTICLE_DATE}}\"\n---\n\nNot enough front matter.\n```",
        "usage": {"in": 10, "out": 10, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 0, "sources": [],
        "finish_reason": "STOP", "model": "gemini-3.5-flash",
    })
    client = _client(tmp_path, fixture_dir=bad_fixtures)

    with pytest.raises(ai_write.WriteValidationError):
        ai_write.run(DATE, client, _llm_cfg(), root=tmp_path)

    # nothing should have been written to content/articles/
    assert not (tmp_path / "content" / "articles").exists() or \
        not list((tmp_path / "content" / "articles").glob("*.md"))


def test_ai_write_missing_brief_raises(tmp_path):
    client = _client(tmp_path)
    with pytest.raises(SystemExit):
        ai_write.run(DATE, client, _llm_cfg(), root=tmp_path)


def test_ai_write_review_flags_true_in_draft_is_rejected(tmp_path):
    _seed_write_inputs(tmp_path)
    bad_fixtures = tmp_path / "true_review_fixtures"
    bad_fixtures.mkdir()
    article = (
        '---\ntitle: "A Perfectly Fine Length Title For Testing Purposes Only"\n'
        'slug: "{{ARTICLE_SLUG}}"\ndate: "{{ARTICLE_DATE}}"\nhub: ai-tools\n'
        'tags: [x]\ndescription: "' + ("d" * 120) + '"\nhero_alt: "alt"\n'
        'keyword: "kw"\noriginal_value: "value"\nselection_note: ""\n'
        'sources:\n  - {title: "S", url: "https://fixturecorp.example/s", primary: true}\n'
        'faq:\n  - {q: "Q?", a: "A."}\n'
        'review:\n  facts_verified: true\n  sources_checked: false\n'
        '  title_promise_check: false\n  no_fabrication: false\n  policy_pass: false\n'
        '  reviewed_at: "2026-08-15T00:00:00+05:30"\n---\n\nBody text.\n'
    )
    _write_json(bad_fixtures / "write.json", {
        "text": "```markdown\n" + article + "\n```",
        "usage": {"in": 10, "out": 10, "thinking": 0},
        "grounded_queries": 0, "url_fetches": 0, "sources": [],
        "finish_reason": "STOP", "model": "gemini-3.5-flash",
    })
    client = _client(tmp_path, fixture_dir=bad_fixtures)

    with pytest.raises(ai_write.WriteValidationError, match="facts_verified"):
        ai_write.run(DATE, client, _llm_cfg(), root=tmp_path)

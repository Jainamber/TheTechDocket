"""Generate the daily article brief from the selected candidate.

The brief is the hand-off contract between the data pipeline and the
writer (the daily Claude session). It contains everything the writer
needs: the keyword, why it was picked, real search phrasings, market
signals, required structure, and the compliance rules the draft must
pass. The writer researches facts independently and MUST NOT invent
data not present in the brief or in cited sources.
"""
from __future__ import annotations

import json
from pathlib import Path

from .util import ROOT, all_articles, load_config, now_ist, today_str


def _autocomplete_lines(inbox: dict) -> str:
    lines = []
    for geo, block in (inbox.get("markets") or {}).items():
        for seed, sugg in (block.get("autocomplete") or {}).items():
            if sugg:
                lines.append(f"- [{geo}] \"{seed}\" → " + "; ".join(sugg[:8]))
    return "\n".join(lines) or "- (no autocomplete data available today)"


def _performance_lines() -> str:
    from .feedback import load_insights
    ins = load_insights()
    if not ins:
        return ("- (no performance data yet — set up analytics + Search Console, "
                "then run `python -m engine.run feedback`)")
    lines = []
    top_pages = sorted(ins.get("page_stats", {}).items(),
                       key=lambda x: -(x[1].get("clicks", 0) * 3
                                       + x[1].get("visits", 0)))[:5]
    for slug, s in top_pages:
        lines.append(f"- Top page: /articles/{slug}/ — clicks {s.get('clicks', 0)}, "
                     f"impressions {s.get('impressions', 0)}, visits {s.get('visits', 0)}")
    for q in ins.get("winning_queries", [])[:6]:
        lines.append(f"- Winning query: \"{q['query']}\" "
                     f"(clicks {q['clicks']}, impressions {q['impressions']})")
    hp = ins.get("hub_performance", {})
    if hp:
        best = max(hp.items(), key=lambda x: x[1])
        lines.append(f"- Strongest hub so far: {best[0]}")
    return "\n".join(lines) or "- (analytics connected, no meaningful data yet)"


def _internal_link_targets(hub_guess: str) -> str:
    arts = all_articles()
    if not arts:
        return "- (archive empty — internal-link gate is relaxed for the first 2 articles)"
    same_hub = [a for a in arts if a.get("hub") == hub_guess][:4]
    pool = same_hub or arts[:4]
    return "\n".join(f"- [{a['title']}](/articles/{a['slug']}/) — hub: {a.get('hub')}"
                     for a in pool)


def build_brief(selection: dict, inbox: dict) -> Path:
    cfg = load_config()
    day = today_str()
    pick = selection.get("pick")
    evergreen = selection.get("use_evergreen")
    hubs = ", ".join(f"`{k}` ({v})" for k, v in cfg["content"]["hubs"].items())
    analysis_heads = " / ".join(cfg["content"]["original_analysis_headings"])

    if evergreen or not pick:
        topic_block = (
            "## Selected topic: EVERGREEN (no strong trend today)\n\n"
            "No candidate cleared the minimum publish score "
            f"({cfg['scoring']['min_publish_score']}). Pick the most seasonally "
            "relevant idea from the evergreen backlog below, or a better one "
            "you identify from the candidate list:\n\n"
            + "\n".join(f"- {t}" for t in cfg["evergreen_backlog"])
        )
    else:
        news_ev = []
        for ev in pick["evidence"][:6]:
            news_ev.append(f"  - {json.dumps(ev, ensure_ascii=False)[:220]}")
        topic_block = (
            f"## Selected trend: **{pick['title']}**\n\n"
            f"- score: {pick['score']} | topic-fit: {pick['topic_fit']} | "
            f"corroboration: {pick['corroboration']} | markets: "
            f"{', '.join(pick['geos']) or 'global'}\n"
            f"- seen in: {', '.join(sorted(set(pick['sources'])))}\n"
            "- evidence snapshot:\n" + "\n".join(news_ev)
        )

    alternates = "\n".join(
        f"- {c['title']}  (score {c['score']}, {', '.join(c['geos']) or 'global'})"
        for c in selection.get("candidates", [])[1:6]) or "- none"

    brief = f"""# Article Brief — {day}

Generated {now_ist().strftime('%Y-%m-%d %H:%M IST')} by engine.brief

{topic_block}

## Alternates (use only if the pick is unwritable — log why in the front matter)
{alternates}

## How people are actually searching (real autocomplete data)
{_autocomplete_lines(inbox)}

## Audience & market notes
- Markets: India + Global mix (weights {[m['weight'] for m in cfg['markets']]}).
- Write for a smart general reader; explain jargon on first use.
- Include a dedicated **"The India angle"** section when the topic is global,
  or a **"Global context"** section when the topic is India-first.
- Demographic/lifestyle claims are ONLY allowed when backed by a cited source
  (e.g., a published survey or report found during research). Google Trends
  does not provide age/gender data — never fabricate audience statistics.

## Required structure (gates will verify)
1. H1 title, {cfg['seo']['title_min_chars']}–{cfg['seo']['title_max_chars']} chars,
   front-load the keyword, no clickbait, promise must match the body.
2. Immediately after the H1: a 2–4 sentence **direct answer/summary paragraph**
   (≥40 words) that fully answers the core question before any H2.
3. 3+ H2 sections, no skipped heading levels, short sections, use a table
   for any comparative data.
4. At least one original-analysis H2 from: {analysis_heads}.
5. A short FAQ section (2–4 real questions from the autocomplete data above).
6. {cfg['seo']['outbound_citations_min']}+ outbound citations to primary sources
   (official announcements, docs, papers, filings — not other blogs).
   EVERY statistic needs an inline link to its source in the same paragraph.
7. 2–4 internal links to related prior articles (see below), naturally in-body.
8. {cfg['content']['min_words']}–{cfg['content']['max_words']} words.
9. Hub: choose one of {hubs}.

## Internal-link candidates
{_internal_link_targets((pick or {}).get('hub', 'ai-models'))}

## What's been working (from data/insights.json — lean into proven demand)
{_performance_lines()}

## Compliance reminders (hard gates)
- People-first: would this be worth reading if Google didn't exist?
- No fabricated stats/quotes; no health/financial/security advice without a
  disclaimer + primary source (YMYL gate).
- Title, og description and body must tell the same story (no curiosity gap).
- This is analysis/journalism-lite, not a rewrite: add synthesis that no
  single source contains (comparison, context, implications, India angle).
"""
    out = ROOT / "data" / "briefs" / f"{day}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(brief, encoding="utf-8")
    return out

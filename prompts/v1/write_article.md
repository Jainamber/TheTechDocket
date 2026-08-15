<!-- v1 | ported from DAILY_RUN.md 2026-08-15 | placeholders: {{like_this}} -->

{{style}}

# Task: write today's article (DAILY_RUN.md Step 5)

Today's date (IST): {{today_ist}}

## The brief (the contract your draft must satisfy)
{{brief}}

## Research notes gathered for you (organized by angle, with sources)
{{research_notes}}

## Source pool found during research (url / title / primary_guess)
```json
{{sources_json}}
```

## Recently published articles (last 10) — do not repeat these; link to
## them naturally where genuinely relevant instead
{{recent_articles}}

## Output format — exactly one fenced block, nothing outside it
Output the **complete article file** — front matter and body — in a single
fenced code block, and nothing else (no preamble, no commentary outside
the fence). The front matter must be valid YAML between `---` lines,
followed by the Markdown body.

Front-matter contract (v1.2 — every field required unless marked optional):

```yaml
---
title: "35-65 chars, keyword front-loaded, no clickbait, promise must match the body"
slug: "{{ARTICLE_SLUG}}"          # LITERAL — write this exact placeholder token, quoted. Do not invent a slug; the publishing system derives it from your title and substitutes it here.
date: "{{ARTICLE_DATE}}"          # LITERAL — write this exact placeholder token, quoted. Do not invent or reformat the date.
hub: ai-models        # one of: ai-models, ai-tools, big-tech, hardware, policy, explainers
tags: [tag1, tag2]
description: "110-165 char meta description with concrete specifics"
hero_alt: "Descriptive alt text for the generated hero image"
keyword: "the primary search keyword"
original_value: "One sentence: what this article adds that no single source has"
selection_note: ""                # only non-empty if the brief told you the topic was an override — else leave ""
sources:
  - {title: "Official announcement — Vendor", url: "https://...", primary: true}
  - {title: "Supporting report — Outlet", url: "https://..."}
faq:
  - {q: "Real question people search?", a: "Two-to-three sentence answer."}
review:
  facts_verified: false      # ALWAYS false in your draft — the citation gate verifies and flips this
  sources_checked: false     # ALWAYS false in your draft — the citation gate verifies and flips this
  title_promise_check: false # ALWAYS false in your draft
  no_fabrication: false      # ALWAYS false in your draft
  policy_pass: false         # ALWAYS false in your draft
  reviewed_at: "{{today_ist}}T00:00:00+05:30"   # a plausible ISO timestamp; the real one is set at publish
---
```
Add `ymyl: finance | health | security` only if the topic genuinely
triggers a YMYL (Your Money or Your Life) category — omit it otherwise.

Do **not** set any `review.*` flag to `true` yourself — an automated
citation-checking gate re-verifies every source against the article and
only it is allowed to flip these to true. A draft that ships `true` here
will be rejected.

## Body requirements (all enforced by automated gates — do not skip any)
1. **H1 title** matching the front-matter title, keyword front-loaded.
2. Immediately after the H1, before any `##`: a **2-4 sentence direct
   answer/summary paragraph (>= 40 words)** that fully answers the core
   question a reader arrives with.
3. **3 or more `##` (H2) sections**, no skipped heading levels (no `####`
   without a `###` first, etc.), short paragraphs throughout.
4. At least **one original-analysis H2** titled exactly one of: "What it
   means", "The India angle", "Our take", "What to watch".
5. A dedicated **"The India angle"** section when the topic is global, or
   a **"Global context"** section when the topic is India-first (this can
   double as the analysis H2 in #4 if titled "The India angle").
6. A **comparison table** (Markdown table) wherever the material has
   comparable data (pricing tiers, specs, timelines, before/after).
7. **Every statistic's paragraph carries an inline link to its source** —
   no stat without a same-paragraph citation.
8. **2 or more outbound citations to primary sources** total (official
   announcements, docs, papers, filings — not other blogs).
9. **2-4 internal links** to related prior articles, in-body and natural
   (`/articles/<slug>/` paths — use the recently-published list above or
   the brief's internal-link candidates). Include **one natural in-body
   link to the article's own hub page** (`/topics/<hub>/`).
10. A short **FAQ section** with 2-4 real questions (use the brief's
    real autocomplete phrasings where possible).
11. **900-2200 words** total body.
12. Explain jargon on first use; hedge only where genuinely uncertain; no
    fabricated numbers, quotes, or audience/demographic claims.

Write the complete article now, as the single fenced block described
above.

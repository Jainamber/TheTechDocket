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
hero_icon: "cpu"                  # REQUIRED — one Tabler icon name that best represents the story's central object; choose from engine/icons.py ICON_NAMES (e.g. cpu, device-mobile, scale, gavel, coins, currency-rupee, shield-lock, sparkles, bug, rocket, tornado, chart-line, server-2, file-text, message-chatbot, world). It renders as the article's icon tile on every surface.
keyword: "the primary search keyword"
original_value: "One sentence: what this article adds that no single source has"
selection_note: ""                # only non-empty if the brief told you the topic was an override — else leave ""
sources:
  - {title: "Official announcement — Vendor", url: "https://...", primary: true}
  - {title: "Supporting report — Outlet", url: "https://..."}
faq:
  - {q: "Real question people search?", a: "Two-to-three sentence answer."}
review:
  facts_verified: false      # ALWAYS false in your draft — only the citation gate verifies sources and flips this
  sources_checked: false     # ALWAYS false in your draft — only the citation gate verifies sources and flips this
  title_promise_check: true  # YOU assert this — true only if your title obeys every rule in "Title rules" below
  no_fabrication: true       # YOU assert this — true only if you invented no fact, quote, statistic, or audience/demographic claim
  policy_pass: true          # YOU assert this — true only if the whole draft follows every rule in this brief
  reviewed_at: "{{today_ist}}T00:00:00+05:30"   # a plausible ISO timestamp; the real one is set at publish
---
```
Add `ymyl: finance | health | security` only if the topic genuinely
triggers a YMYL (Your Money or Your Life) category — omit it otherwise.

**review.\* flags — two different owners, both mechanically checked:**
`facts_verified` and `sources_checked` must stay `false` — a separate,
automated citation-checking gate re-verifies every source against the
article after your draft is submitted, and only it is allowed to flip
those two to `true`. `title_promise_check`, `no_fabrication`, and
`policy_pass` are the opposite: YOU are the only one who can certify them
(you are the author), so ship them as `true` — but only because they are
genuinely true. A draft is rejected if `facts_verified`/`sources_checked`
come back anything but `false`, or if `title_promise_check` /
`no_fabrication` / `policy_pass` come back anything but `true`.

### Title rules (gate G08 — checked mechanically; any violation is a hard
### fail, independent of what you write in `review.title_promise_check`)
- No run of 5+ consecutive uppercase letters (no ALL-CAPS words like
  "SHOCKING" or "AMAZING").
- At most one `!` in the title.
- None of these clickbait patterns, in any casing: "you won't believe",
  "will shock", "shocking truth", "blow your mind", "this one trick",
  "one weird", "secret(s) that/they", "they don't want you", "number
  <N> will", "gone wrong", "jaw-dropping".
- The title must be a plain, accurate promise the body actually delivers
  in full — this is exactly what `review.title_promise_check: true`
  certifies. If the title overpromises anything the body doesn't deliver,
  rewrite the title (or the body) until they match.

### Claim–source discipline (hard — every cited sentence is machine-verified against the ACTUAL PAGE)
After you write, an automated gate FETCHES every url you cite and checks whether
that specific page states the facts in the citing sentence. A single mismatch
fails the whole article. Therefore:
- A sentence may only assert what its linked page EXPLICITLY states. Not what
  the publication reported elsewhere, not what you infer, not background you
  know. The exact page, nothing more.
- Attribute each fact to the source that CONTAINS it. Pricing details belong to
  the page that lists them (often the announcement post, NOT the generic
  pricing page); benchmark numbers to the page showing those numbers.
- Never bundle an extra fact into a cited sentence unless the same page states
  that extra fact too — split it into its own sentence with its own source, or
  cut it.
- When unsure which source states a fact, check the research notes; if no
  listed source states it, CUT THE FACT. A shorter, fully-verified article
  always beats a richer one that fails verification.

### Citation rules (hard — checked mechanically, before any gate even runs)
The research pack above includes a **numbered list of resolved deep-link
sources** (see "Sources (numbered...)" at the end of the research notes,
and the same urls again in the source-pool JSON block). Every url you cite
— every front-matter `sources[].url` and every inline body link — MUST be
copied **VERBATIM** from that list:
- Never cite a bare domain homepage (e.g. `https://example.com/` or
  `https://example.com`) — always the specific deep article/page url from
  the list.
- Never shorten, "clean up", retype, or otherwise alter a listed url.
- Never invent a url, and never cite a page that isn't in the list —
  including a page you're confident exists but wasn't actually returned
  by research.
- **If a fact has no listed source to back it, cut the fact.** A vague or
  unsourced-but-plausible-sounding claim is worse than a shorter article.
A draft that cites a bare-domain homepage or any url not verbatim from the
numbered list is rejected and sent back for one corrective rewrite.

## Body requirements (all enforced by automated gates — do not skip any)
1. **No `# ` (H1) line anywhere in the body.** The page template renders
   the front-matter `title` as the page's one and only `<h1>` on its own
   — if the body also starts with a `# Title` line, the rendered page
   ends up with two `<h1>` elements and gate S03 (single-H1) hard-fails.
   Body headings start at `##` (H2); never emit a `# ` line.
2. The **first line of the body** (before any `##`): a **2-4 sentence
   direct answer/summary paragraph (>= 40 words)** that fully answers the
   core question a reader arrives with.
3. **3 or more `##` (H2) sections**, no skipped heading levels (no `####`
   without a `###` first, etc.), short paragraphs throughout.
4. At least **one original-analysis H2** titled exactly one of: "What it
   means", "The India angle", "Our take", "What to watch".
5. A dedicated **"The India angle"** section when the topic is global, or
   a **"Global context"** section when the topic is India-first (this can
   double as the analysis H2 in #4 if titled "The India angle").
6. A **comparison table** (Markdown table) wherever the material has
   comparable data (pricing tiers, specs, timelines, before/after).
7. **Stat-sourcing (gate G07 — checked mechanically, paragraph by
   paragraph):** any paragraph containing a percentage (e.g. "45%"), a
   currency amount (a `₹`/`$`/`€`/`£` symbol directly followed by a
   digit), or a number scaled in crore/lakh/million/billion/trillion MUST
   contain an inline markdown link to an **external** `http(s)://` source
   (not a link to this site's own pages) **within that exact same
   paragraph** — a citation in a different paragraph, even the very next
   one, does not satisfy the gate. If a paragraph has such a number and no
   natural external source to cite inline, rewrite the paragraph so the
   number either gets its own citation or is dropped.
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
  facts_verified: false      # ALWAYS false in your draft — only the citation gate verifies sources and flips this
  sources_checked: false     # ALWAYS false in your draft — only the citation gate verifies sources and flips this
  title_promise_check: true  # YOU assert this — true only if your title obeys every rule in "Title rules" below
  no_fabrication: true       # YOU assert this — true only if you invented no fact, quote, statistic, or audience/demographic claim
  policy_pass: true          # YOU assert this — true only if the whole draft follows every rule in this brief
  reviewed_at: "{{today_ist}}T00:00:00+05:30"   # a plausible ISO timestamp; the real one is set at publish
---
```
Add `ymyl: finance | health | security` only if the topic genuinely
triggers a YMYL (Your Money or Your Life) category — omit it otherwise.

**review.\* flags — two different owners, both mechanically checked:**
`facts_verified` and `sources_checked` must stay `false` — a separate,
automated citation-checking gate re-verifies every source against the
article after your draft is submitted, and only it is allowed to flip
those two to `true`. `title_promise_check`, `no_fabrication`, and
`policy_pass` are the opposite: YOU are the only one who can certify them
(you are the author), so ship them as `true` — but only because they are
genuinely true. A draft is rejected if `facts_verified`/`sources_checked`
come back anything but `false`, or if `title_promise_check` /
`no_fabrication` / `policy_pass` come back anything but `true`.

### Title rules (gate G08 — checked mechanically; any violation is a hard
### fail, independent of what you write in `review.title_promise_check`)
- No run of 5+ consecutive uppercase letters (no ALL-CAPS words like
  "SHOCKING" or "AMAZING").
- At most one `!` in the title.
- None of these clickbait patterns, in any casing: "you won't believe",
  "will shock", "shocking truth", "blow your mind", "this one trick",
  "one weird", "secret(s) that/they", "they don't want you", "number
  <N> will", "gone wrong", "jaw-dropping".
- The title must be a plain, accurate promise the body actually delivers
  in full — this is exactly what `review.title_promise_check: true`
  certifies. If the title overpromises anything the body doesn't deliver,
  rewrite the title (or the body) until they match.

### Claim–source discipline (hard — every cited sentence is machine-verified against the ACTUAL PAGE)
After you write, an automated gate FETCHES every url you cite and checks whether
that specific page states the facts in the citing sentence. A single mismatch
fails the whole article. Therefore:
- A sentence may only assert what its linked page EXPLICITLY states. Not what
  the publication reported elsewhere, not what you infer, not background you
  know. The exact page, nothing more.
- Attribute each fact to the source that CONTAINS it. Pricing details belong to
  the page that lists them (often the announcement post, NOT the generic
  pricing page); benchmark numbers to the page showing those numbers.
- Never bundle an extra fact into a cited sentence unless the same page states
  that extra fact too — split it into its own sentence with its own source, or
  cut it.
- When unsure which source states a fact, check the research notes; if no
  listed source states it, CUT THE FACT. A shorter, fully-verified article
  always beats a richer one that fails verification.

### Citation rules (hard — checked mechanically, before any gate even runs)
The research pack above includes a **numbered list of resolved deep-link
sources** (see "Sources (numbered...)" at the end of the research notes,
and the same urls again in the source-pool JSON block). Every url you cite
— every front-matter `sources[].url` and every inline body link — MUST be
copied **VERBATIM** from that list:
- Never cite a bare domain homepage (e.g. `https://example.com/` or
  `https://example.com`) — always the specific deep article/page url from
  the list.
- Never shorten, "clean up", retype, or otherwise alter a listed url.
- Never invent a url, and never cite a page that isn't in the list —
  including a page you're confident exists but wasn't actually returned
  by research.
- **If a fact has no listed source to back it, cut the fact.** A vague or
  unsourced-but-plausible-sounding claim is worse than a shorter article.
A draft that cites a bare-domain homepage or any url not verbatim from the
numbered list is rejected and sent back for one corrective rewrite.

## Body requirements (all enforced by automated gates — do not skip any)
1. **No `# ` (H1) line anywhere in the body.** The page template renders
   the front-matter `title` as the page's one and only `<h1>` on its own
   — if the body also starts with a `# Title` line, the rendered page
   ends up with two `<h1>` elements and gate S03 (single-H1) hard-fails.
   Body headings start at `##` (H2); never emit a `# ` line.
2. The **first line of the body** (before any `##`): a **2-4 sentence
   direct answer/summary paragraph (>= 40 words)** that fully answers the
   core question a reader arrives with.
3. **3 or more `##` (H2) sections**, no skipped heading levels (no `####`
   without a `###` first, etc.), short paragraphs throughout.
4. At least **one original-analysis H2** titled exactly one of: "What it
   means", "The India angle", "Our take", "What to watch".
5. A dedicated **"The India angle"** section when the topic is global, or
   a **"Global context"** section when the topic is India-first (this can
   double as the analysis H2 in #4 if titled "The India angle").
6. A **comparison table** (Markdown table) wherever the material has
   comparable data (pricing tiers, specs, timelines, before/after).
7. **Stat-sourcing (gate G07 — checked mechanically, paragraph by
   paragraph):** any paragraph containing a percentage (e.g. "45%"), a
   currency amount (a `₹`/`$`/`€`/`£` symbol directly followed by a
   digit), or a number scaled in crore/lakh/million/billion/trillion MUST
   contain an inline markdown link to an **external** `http(s)://` source
   (not a link to this site's own pages) **within that exact same
   paragraph** — a citation in a different paragraph, even the very next
   one, does not satisfy the gate. If a paragraph has such a number and no
   natural external source to cite inline, rewrite the paragraph so the
   number either gets its own citation or is dropped.
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

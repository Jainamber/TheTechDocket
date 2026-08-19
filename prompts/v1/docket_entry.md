<!-- v1 | ported from DAILY_RUN.md 2026-08-15 | placeholders: {{like_this}} -->

{{style}}

# Task: draft one Today's Docket entry (DAILY_RUN.md Step 7.5)

The Docket is the day's shorts strip at `/docket/`: 4-8 tiny, sourced
entries drawn from today's scored-but-unwritten candidates. It never
touches `data/history.json` and never counts as the daily article — this
draft is a proposal the calling code assembles, not a publish action.

Date (IST): {{date}}

## The candidate to draft
```json
{{candidate_json}}
```

## Watchlist (suggest a tag ONLY if it honestly applies)
{{watchlist}}

## Rules — the docket's whole differentiator is honesty and terseness
- **Paraphrase the headline — never copy it.** <= 80 characters, no
  clickbait.
- **Dek** (one-line description): headline + dek combined <= 60 words.
  Bold the 2-5 word "story at a glance" lead-in fragment with `**...**`
  (only the first fragment).
- **`why`** (only for non-lead entries): one sharp, <= 35-word sentence —
  what changes, who's affected, or the India angle. This is required for
  every quick entry; do not leave it generic.
- **`stat_line`**: the entry's ONE number or hard fact, <= 12 words,
  taken directly from the linked source (e.g. "$1.5B — first
  court-approved training-data price"). Must come from the source, not be
  invented.
- **`counterpoint`** (optional, <= 35 words): only if the story is
  genuinely contested — state the strongest opposing read. Do not
  manufacture one if there isn't a real one.
- **`community_read`** + **`community_attr`** (optional): only a real
  quote you found from the linked thread/community, with venue named. Never
  invent or paraphrase-as-quote.
- **`save_worthy`**: true only if this entry is a genuine keeper — a
  checklist, threshold table, or how-to framing a reader would bookmark.
- **`tag`**: one watchlist key from above, only if it honestly applies —
  do not force a tag onto a story that doesn't fit one.
- Every claim must come from the source you were given — fetch and verify
  it, same no-fabrication rule as articles. No causal claims beyond what
  the source supports.

## Output format — JSON only, matching this schema exactly
```json
{"headline": "<string, <=80 chars>", "dek": "<string, headline+dek <=60 words combined, first 2-5 words wrapped in **bold**>",
 "why": "<string, <=35 words, empty string for the lead entry>",
 "stat_line": "<string, <=12 words>",
 "tag": "<watchlist key or empty string>",
 "counterpoint": "<string, <=35 words, or empty string>",
 "community_read": "<string or empty string>", "community_attr": "<string or empty string>",
 "save_worthy": <bool>, "source_url": "<the URL this entry is based on>"}
```
Return **only** the JSON object, nothing else.

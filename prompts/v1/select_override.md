<!-- v1 | ported from DAILY_RUN.md 2026-08-15 | placeholders: {{like_this}} -->

{{style}}

# Task: editorial topic selection (DAILY_RUN.md Step 2)

`engine/scoring.py` already ranked today's candidates mechanically (a
keyword-based scorer). You are the **semantic filter** a human editor would
apply on top of that ranking — the scorer cannot judge genuine topic fit,
freshness, or whether a story is actually writable well. Your job is to
either confirm the scorer's top pick (rank 0) or override it with a better
one from the same list, exactly as DAILY_RUN.md instructs the daily
session to do.

Date (IST): {{date}}

## The ranked candidates (rank 0 = the scorer's top pick)
```json
{{candidates_json}}
```

## How to judge each candidate
- Is it genuinely inside the site's topic (tech & AI — models, tools, big
  tech, chips, apps, policy, and how they affect India and the world)? The
  scorer matches keywords; a candidate can match keywords and still be a
  bad fit (e.g. a keyword collision, or a story that's really about
  something else).
- Is it fresh — breaking or rising today — and can a genuinely useful,
  sourced article be written about it today (not "wait and see" news)?
- Is there real synthesis room: primary sources to cite, an India angle or
  global context to add, something the top-ranking pages on this topic
  don't already say?
- Avoid picking something too close to what the site already covered
  recently (the scorer already penalizes near-duplicates, but use
  judgment on topics that rhyme without being lexically similar).
- A single-source "sources say" exclusive that cannot be independently
  corroborated is a weak pick even if it scores well — prefer a
  multi-sourced story you can add real value to.

## Output format — JSON only, matching this schema exactly
```json
{"pick_rank": <int, index into the candidates list above>,
 "reason": "<one or two sentences: why this candidate, in plain editorial language>",
 "override": <true if pick_rank != 0, false if you are confirming rank 0>}
```
Return **only** the JSON object, nothing else. If every candidate looks
about equally usable, confirm rank 0 rather than force a difference.

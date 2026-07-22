# Fact-Verification: Chip Week Context (Google chip claim + Kimi K3 / Qwen3.8-Max)

**Research date:** 2026-07-22 (IST)
**Tool used:** WebSearch only (WebFetch / Python HTTP blocked per task instructions).

## BLOCKED — 0 of 12 budgeted searches executed

Both opening queries for Task A returned an identical hard stop from the WebSearch tool itself:

> "Web search was not performed: this session has used its web search budget (200 of 200 WebSearch calls). Continue with the information already gathered instead of issuing more searches. If more searches are genuinely needed, ask the user to raise CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION."

This is a session-wide cap, not specific to this task. Two sibling files already in this same output directory confirm other work earlier in this session consumed the full 200-search budget:
- `/home/claude/thetechdocket/data/research/2026-07-22/launch-verification.md` — logs 30+ queries spent verifying the Gemini 3.6 Flash launch.
- `/home/claude/thetechdocket/data/research/2026-07-22/reaction-context.md` — explicitly notes it ran out of budget before researching "Part 2 (Frozen v2 chip claim)" and "Part 3 (Kimi K3 / Qwen3.8-Max)," and recommends exactly this follow-up be run "once `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` is raised or in a new session."

That follow-up is what this task attempted. Result: **zero searches were possible**, so per instructions ("NEVER invent facts, URLs, or numbers") nothing new can be confirmed or denied here. No claim below has been checked by this task — absence of a search is not evidence the claim is false.

---

## Task A — Google "Frozen v2" chip, 6-10x TPU efficiency for Gemini inference

**Searches executed:** 0 of planned 4-6 (both attempted queries hit the exhausted-budget stop before any results returned).

**Verdict: NOT-FOUND** (more precisely: *unverifiable this session* — not "searched and absent," but "could not search at all"). Cannot be elevated to CONFIRMED-OFFICIAL, CONFIRMED-MULTI-OUTLET, or even SINGLE-SOURCE-UNVERIFIED, since no source of any quality was retrieved.

**Recommendation: drop the claim from the article.** This matches the task's own fallback instruction, and matches the prior session file's identical recommendation for the same claim.

---

## Task B — Kimi K3 and Qwen3.8-Max

**Searches executed:** 0 of planned 4-6.

### (1) Moonshot AI Kimi K3 — open-weight launch timing + reported subscription pause (GPU capacity)
- Fact 1 (open-weight launch timing): **NOT CONFIRMED** — no search run this task.
- Fact 2 (new-subscription pause due to GPU capacity, ~July 20-21, 2026, SCMP/Bloomberg): **NOT CONFIRMED** — no search run this task.
- One incidental, *unrelated* data point exists from the earlier `reaction-context.md` file (not produced by this task, and not addressing either fact above): a Techmeme aggregation of a Bloomberg report (reporter: Pei Li) stating Moonshot is closing a funding round at a $31.5B valuation with a further raise planned at $50B "to capitalize on Kimi K3 buzz before a Hong Kong IPO" — https://www.techmeme.com/260721/p23. Status if cited: **(c) single-source aggregator**, and it does not confirm the open-weight launch date or the subscription-pause/GPU-capacity claim — only that "Kimi K3" is a real, named, buzzed-about model tied to fundraising. Do not use this in place of the two specific facts requested.

### (2) Alibaba Qwen3.8-Max — reported 2.4-trillion-parameter flagship
- Fact 1: **NOT CONFIRMED** — no search run this task.
- Fact 2: **NOT CONFIRMED** — no search run this task.

**Recommendation:** Do not publish either Kimi K3 or Qwen3.8-Max facts from this task's output — none were independently verified. Re-run with a fresh/raised search budget using the queries below.

---

## Suggested queries for a follow-up pass (none executed yet)
- `Google "Frozen v2" chip`
- `Google custom AI chip Gemini efficiency July 2026`
- `Google new TPU announcement July 2026`
- `Google AI chip 6x efficiency Gemini inference`
- `Moonshot AI Kimi K3 open weight launch`
- `Kimi K3 subscriptions paused GPU capacity SCMP OR Bloomberg`
- `Alibaba Qwen3.8-Max 2.4 trillion parameters Bloomberg`
- `Qwen3.8-Max launch date Alibaba flagship model`

## Status legend
(a) official — from the company/entity itself
(b) 2+ outlets — independently corroborated
(c) single-source — only one outlet found
(d) / NOT-FOUND — not locatable, or in this case, not searchable this session

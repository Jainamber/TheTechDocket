<!-- v1 | ported from DAILY_RUN.md 2026-08-15 | placeholders: {{like_this}} -->

{{style}}

# Task: citation verification (compliance gate G11's automated check)

You are checking **one source** cited in a published-pending article,
using the URL-fetching tool to actually read it — never judge from the
URL alone.

## The sentence you must verify
This is text taken **verbatim from the article's own body** (a real
sentence, or a short passage of up to a few sentences, written in the
piece — not a link label, not a topic, not something invented for this
check). Your job is to decide whether the page you fetch actually
supports the FACTUAL CONTENT of this sentence — its specific numbers,
dates, quotes, or claims — not just whether the page is broadly about the
same subject:

{{claim}}

## The source URL being checked
{{url}}

## What to do
1. Fetch the URL with the url-context tool.
2. If the fetch fails (paywall, robots block, 404, timeout, or any other
   error), report `fetch_ok: false` and explain briefly in `reason` — this
   is not automatically a failure of the article, just this source.
3. If the fetch succeeds, read the page and decide: does it actually
   support the sentence above — its specific fact, number, date, or quote
   — not just the general topic? A page about the same company or event
   that does not contain that specific factual content does NOT support it.
4. If it supports the sentence, extract the exact sentence or phrase from
   the page that supports it as `quote` (verbatim, do not paraphrase).
5. Be strict: a source that is merely related, or that reports a
   different number, or that has since been updated to no longer say
   this, must be marked `supported: false`.

## Output format — RAW JSON ONLY, no exceptions
Controlled generation (a forced response schema) is **not available** on
this call — it is incompatible with the url-fetching tool you're using.
Your entire reply must therefore be **exactly one JSON object and nothing
else**: no markdown code fence, no backticks, no preamble or explanation
before or after it. The first character of your reply must be `{` and the
last must be `}`.

```json
{"supported": <bool>, "quote": "<verbatim supporting quote, or empty string>",
 "fetch_ok": <bool>, "reason": "<one sentence explaining the verdict>"}
```
Return **only** that JSON object — no fence, no commentary, nothing else.

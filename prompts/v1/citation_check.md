<!-- v1 | ported from DAILY_RUN.md 2026-08-15 | placeholders: {{like_this}} -->

{{style}}

# Task: citation verification (compliance gate G11's automated check)

You are checking **one source** cited in a published-pending article,
using the URL-fetching tool to actually read it — never judge from the
URL alone.

## The claim this source is attached to
{{claim}}

## The source URL being checked
{{url}}

## What to do
1. Fetch the URL with the url-context tool.
2. If the fetch fails (paywall, robots block, 404, timeout, or any other
   error), report `fetch_ok: false` and explain briefly in `reason` — this
   is not automatically a failure of the article, just this source.
3. If the fetch succeeds, read the page and decide: does it actually
   support the claim above — the specific fact, number, or quote — not
   just the general topic? A page about the same company or event that
   does not contain the specific claim does NOT support it.
4. If it supports the claim, extract the exact sentence or phrase from the
   page that supports it as `quote` (verbatim, do not paraphrase).
5. Be strict: a source that is merely related, or that reports a
   different number, or that has since been updated to no longer say
   this, must be marked `supported: false`.

## Output format — JSON only, matching this schema exactly
```json
{"supported": <bool>, "quote": "<verbatim supporting quote, or empty string>",
 "fetch_ok": <bool>, "reason": "<one sentence explaining the verdict>"}
```
Return **only** the JSON object, nothing else.

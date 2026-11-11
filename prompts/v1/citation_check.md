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
3. If the fetch succeeds, read the page and decide: does the page substantively
   confirm the core factual claims in the sentence (its specific numbers, dates,
   policies, or architectural facts)?
   - Substantive truth vs exact wording: Journalistic paraphrasing of equivalent
     concepts (e.g. "business/enterprise customers" vs "commercial organizations",
     or "data access control" vs "data segregation") IS supported if the underlying
     policy, rule, or technical fact is confirmed by the page.
   - Do NOT reject an accurate summary over minor synonym variations unless the
     article asserts a materially false, contradictory, or unmentioned claim
     (such as attributing a policy to the wrong company or stating a fabricated number).
   - Cited factual premise vs author analysis: Articles frequently combine a cited
     factual premise with editorial analysis in the same sentence (e.g. "Under
     [The DPDP Act](url), data fiduciaries must erase personal data upon consent
     withdrawal, creating compliance friction for enterprise retention models").
     You are verifying whether the source confirms the CITED FACTUAL PREMISE
     (e.g. that the Act mandates data erasure), NOT whether the source itself
     discusses or endorses the author's editorial synthesis or opinion ("creating friction").
     If the source confirms the underlying law, metric, or policy, mark supported: true.
   - Multi-clause or multi-source passages: When a passage combines multiple facts or
     features (or when multiple claims are separated by '---'), verify whether the fetched
     URL supports the SPECIFIC factual claim, feature, or announcement tied to this source.
     If the source confirms its part of the passage (e.g. confirms the product launch,
     pricing tiers, or architecture), mark supported: true, even if other clauses in the
     sentence originate from other sources. Do NOT reject an official source for omitting
     unrelated features from other clauses.
   - Landed-cost math, GST, and currency conversions: If the source confirms the underlying
     base price or subscription tier (e.g. $20/month or ₹1,950/month), and the author derives
     Indian landed-cost math, applies India's statutory 18% GST/IGST, or converts currency
     at prevailing rates, mark supported: true.
4. If it supports the sentence, extract the exact sentence or phrase from
   the page that supports it as `quote` (verbatim, do not paraphrase).
5. Be strict on real factual discrepancies: a source that is merely about the
   same general company, or reports a different number, or lacks the cited fact
   entirely, must be marked `supported: false`.

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

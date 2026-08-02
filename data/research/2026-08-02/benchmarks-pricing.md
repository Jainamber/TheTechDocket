# DeepSeek V4 Flash (0731) — Independent Benchmarks & Price/Performance Comparison

Research date: 2026-08-02. Model released: ~2026-07-31 ("DeepSeek V4 Flash 0731").
Primary independent benchmark source used throughout: Artificial Analysis (AA) Intelligence Index.

---

## IMPORTANT DATA-QUALITY NOTE (read before using any figure below)

While verifying, I found that Artificial Analysis's own **primary model pages** for DeepSeek V4 Flash appear **stale/not yet refreshed** for the 0731 release, even though search engines index them under the "0731" name:

- Direct fetch of https://artificialanalysis.ai/models/deepseek-v4-flash on 2026-08-02 returned a page headed **"DeepSeek V4 Flash (Reasoning, Max Effort)"** (no "0731" tag), Intelligence Index **40**, "Released April 24, 2026."
- Direct fetch of https://artificialanalysis.ai/models/deepseek-v4-flash-high returned **"DeepSeek V4 Flash (Reasoning, High Effort)"**, score **37**, same April 2026 release date, no "0731" marker.
- These are the scores for the **original (pre-0731) DeepSeek V4 Flash**, launched April 2026 — not the July 31 model this article is about.

The **current, corroborated score for the July 31 "0731" release is 50** — confirmed independently across AA's dedicated announcement article, an AA model-comparison page, two Artificial Analysis official X/Twitter posts, and two independent news write-ups (TechTimes, OfficeChai). See citations below. I'm flagging the stale-page issue so nobody re-fetches the bare AA model URL and reports "40" as current.

Similarly, the AA page for GPT-5.6 Luna (https://artificialanalysis.ai/models/gpt-5-6-luna) still shows **pre-price-cut** pricing ($1.00/$6.00) as of this fetch; the current post-cut price ($0.20/$1.20, effective July 30, 2026) comes from news coverage and a third-party aggregator, not yet from AA's own model page.

---

## Verified figures

### DeepSeek V4 Flash 0731 (subject model)

- **AA Intelligence Index score: 50** — a 10-point jump over the original April-2026 DeepSeek V4 Flash (40).
  Source: https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash (published 2026-07-31)
  Corroborated by: https://artificialanalysis.ai/models/comparisons/deepseek-v4-flash-vs-gpt-5-6-sol ; https://www.techtimes.com/articles/322513/20260731/deepseek-retrained-v4-flash-beats-its-flagship-pro-nine-agent-benchmarks.htm (2026-07-31) ; https://officechai.com/ai/deepseek-v4-flash-0731-scores-50-on-artificial-analysis-intelligence-index-creates-big-spike-on-pareto-frontier/ ; https://simonwillison.net/2026/Jul/31/deepseek-v4-flash-0731/ ("approximately 50")

- **Position vs. named competitors** (all stated in the same AA article above):
  - 6 points ahead of DeepSeek V4 Pro (44)
  - 1 point behind GPT-5.6 Luna (max, 51)
  - Roughly level with GLM-5.2 (max, 51) and tied with Gemini 3.6 Flash (50)
  - 1 point behind Muse Spark 1.1 (xhigh, 51)
  - Trails open-weights leader Kimi K3 (max, 57) by 7 points
  Source: https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash

- **"Top 3 open-weights models" on the AA leaderboard**, released under MIT license (open weights).
  Source: Artificial Analysis official X post — https://x.com/ArtificialAnlys/status/2083306229074739285

- **Pricing: $0.14/M input tokens, $0.28/M output tokens** — unchanged from the original DeepSeek V4 Flash ("shares identical architecture and pricing").
  Source: https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash ; corroborated by https://officechai.com/ai/deepseek-v4-flash-0731-scores-50-on-artificial-analysis-intelligence-index-creates-big-spike-on-pareto-frontier/
  - Cache-hit price: **$0.0028/M tokens** (~98% discount off input rate) — same sources.
  - Blended price (AA's 7:2:1 cache-hit:input:output ratio convention): **$0.06/M tokens** — https://artificialanalysis.ai/models/deepseek-v4-flash (note: this figure is on the stale-labeled page, but AA/officechai both state 0731 pricing is unchanged from the prior version, so the blended math should carry over).

- **Architecture:** 284B total parameters / 13B active (MoE), 1M-token context window, text in/out only.
  Sources: https://artificialanalysis.ai/models/deepseek-v4-flash ; https://officechai.com/ai/deepseek-v4-flash-0731-scores-50-on-artificial-analysis-intelligence-index-creates-big-spike-on-pareto-frontier/

- **Independent AA benchmark deltas (0731 vs. original V4 Flash):** GDPval-AA v2 Elo 1559 (up from 1189); Terminal-Bench 2.1 79% (up 17 pts, AA's own measurement); τ³-Bench Banking 31% (up 8 pts); AA-Omniscience Index -16 (up from -23, i.e., fewer hallucinations).
  Source: https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash

- **Output speed / latency (from AA's stale-labeled but architecture-identical model page):** 115.9 tokens/sec, time-to-first-token 1.30s.
  Source: https://artificialanalysis.ai/models/deepseek-v4-flash
  Per-provider breakdown from AA's provider-benchmarking subpage (titled "0731 (max)" in search index): DeepSeek native API 105.5 t/s, GMI 113.5 t/s, SiliconFlow (FP8) 102.6 t/s, Novita 102.4 t/s, Makora 289.8 t/s (fastest), DeepInfra (FP4) 11.4 t/s.
  Source: https://artificialanalysis.ai/models/deepseek-v4-flash/providers
  Caveat: this same subpage lists time-to-first-token values of 20–56 **seconds** across providers, which is implausibly high for a fast API and inconsistent with the 1.30s TTFT on the main page. Likely a benchmarking-methodology change (the page notes "Default performance benchmarking workload has updated to 10k input tokens") or an extraction artifact. Treat those specific TTFT-by-provider numbers as UNVERIFIED.

- **DeepSeek's own (self-reported) benchmark table** — Terminal-Bench 2.1: 82.7 (vs. DeepSeek V4 Pro Preview 72.1, vs. Claude Opus 4.8's 85.0); DeepSWE: 54.4 (a "645% jump," company claim); Agents' Last Exam: 25.2 (vs. Opus 4.8's 25.7); DSBench-FullStack: 68.7 (vs. V4 Pro Preview's 37.0).
  Source: https://www.techtimes.com/articles/322513/20260731/deepseek-retrained-v4-flash-beats-its-flagship-pro-nine-agent-benchmarks.htm
  **Important caveat directly from this source:** "the scores cannot currently be independently replicated" since DeepSeek's benchmark harness remains unreleased. This applies to DeepSeek's self-reported table only, NOT to the Artificial Analysis Intelligence Index score (50), which is an independent third-party measurement.

### GPT-5.6 Luna (closest scored competitor + price-war context)

- **AA Intelligence Index (max effort): 51**, rank #15 of 1,885 models tracked.
  Source: https://artificialanalysis.ai/models/gpt-5-6-luna
  Corroborated: https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash

- **Price cut confirmed, but NOT at the figure suggested in the task brief.** The task's assumption of "~$0.35/M input, cut Aug 1" does **not match** what I could verify. Verified instead:
  - **New price (effective 2026-07-30): $0.20/M input, $1.20/M output** — an "80% reduction across both rates."
    Sources: https://www.techtimes.com/articles/322305/20260730/openai-cuts-luna-80-sol-rewrote-its-own-inference-stack-fund-price-drop.htm ; https://basic-tutorials.com/news/gpt-5-6-openai-cuts-prices-luna-becomes-80-cheaper/
  - **Old price (in effect since 2026-07-09 launch): $1.00/M input, $6.00/M output.**
    Source: https://www.techtimes.com/articles/322305/20260730/openai-cuts-luna-80-sol-rewrote-its-own-inference-stack-fund-price-drop.htm
  - Third-party aggregator BenchLM.ai (page "last updated July 30, 2026") lists a cached-input rate of $0.02/M for GPT-5.6 Luna, consistent with a $0.20 standard input rate at a typical ~90%-off cache discount. Source: https://benchlm.ai/compare/deepseek-v4-flash-vs-gpt-5-6-luna
  - VentureBeat's parallel report of the same story (headline: "OpenAI cuts GPT-5.6 Luna prices by 80%") returned a 403 error on fetch and could not be directly verified, but is consistent with the two sources above. Listed here for transparency, not used as a cited figure.

- **Output speed: 215.1 tokens/sec.** Source: https://artificialanalysis.ai/models/gpt-5-6-luna
- **Latency (TTFT): page shows "103.52s"** — this is almost certainly an extraction error or stale/mismeasured figure (implausible for a 215 t/s model); marked UNVERIFIED. Source: https://artificialanalysis.ai/models/gpt-5-6-luna
- Blended price (7:2:1 ratio) at OLD pricing: $0.87/M. Source: https://artificialanalysis.ai/models/gpt-5-6-luna. No blended figure is available yet at the new post-cut price from any source I could verify.

### Gemini 3.6 Flash

- **AA Intelligence Index (high effort): 50**, rank #21 of 187.
  Source: https://artificialanalysis.ai/models/gemini-3-6-flash

- **Official price: $1.50/M input, $7.50/M output** (standard tier; output rate includes thinking/reasoning tokens).
  Sources: https://artificialanalysis.ai/models/gemini-3-6-flash ; https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ (official Google announcement, published 2026-07-21) ; https://www.eesel.ai/blog/gemini-3-6-flash-pricing
  - Batch/Flex tier: $0.75/M input, $3.75/M output. Source: https://www.eesel.ai/blog/gemini-3-6-flash-pricing
  - This is a 17% cut to the output rate vs. Gemini 3.5 Flash's $9.00/M output; input unchanged. Source: https://www.eesel.ai/blog/gemini-3-6-flash-pricing
  - Blended (7:2:1): $1.16/M. Source: https://artificialanalysis.ai/models/gemini-3-6-flash
- Output speed/latency: not published on the AA page ("Unknown"). Source: https://artificialanalysis.ai/models/gemini-3-6-flash

### Claude 4.5 Haiku (Anthropic's current cheapest model, as of Aug 2026)

- **AA Intelligence Index (non-reasoning): 24 (estimated)**, rank #26 of 71.
  Source: https://artificialanalysis.ai/models/claude-4-5-haiku
- **Price: $1.00/M input, $5.00/M output**, blended (7:2:1) $0.77/M. Same source.
- Output speed: 91.5 tokens/sec; TTFT: 0.93s. Same source.
- Released: 2026-10-15 — **note: this date as extracted is internally inconsistent (October 2025 is the model's actual known launch window per Anthropic's own "Introducing Claude Haiku 4.5" announcement; the AA page date format may have been misread).** Treat exact release date as UNVERIFIED; treat pricing/score/speed as verified from the same page.

### Kimi K3 (Moonshot AI) — open-weights intelligence leader

- **AA Intelligence Index (max): 57**, rank #4 of 1,865.
  Source: https://artificialanalysis.ai/models/kimi-k3
- **Price: $3.00/M input, $15.00/M output**, blended (7:2:1) $2.31/M. Same source.
- Output speed: 34.2 tokens/sec ("notably slow" per AA's own characterization). TTFT: 4.87s. Same source.

### Qwen (3.8 vs. 3.7 Max)

- **Qwen 3.8 Max Preview** launched 2026-07-19 but Alibaba "hasn't broken out a per-token rate" and there is no independent AA Intelligence Index score for it yet as of the source's publication. Source: https://techsy.io/en/blog/qwen-3-8
- Closest verified data point is the prior generation, **Qwen3.7 Max**:
  - AA Intelligence Index: **57**, rank #7 of 148. Source: https://artificialanalysis.ai/models/qwen3-7-max
  - Price: $2.50/M input, $7.50/M output, blended (7:2:1) $1.43/M. Same source.
  - Output speed: 205.7 tokens/sec; TTFT: 2.51s. Same source.
  - A secondary source (techsy.io) cites Qwen3.7 Max at "56.6, 5th overall" rather than AA's page figure of 57/#7 — a minor discrepancy likely from different leaderboard snapshot dates (the leaderboard shifts as new models are added). Source: https://techsy.io/en/blog/qwen-3-8

### DeepSeek V4 Pro (prior/sibling flagship model, for context)

- **AA Intelligence Index (max): 44**, rank #3 of 93 (open-weight models). Source: https://artificialanalysis.ai/models/deepseek-v4-pro
- Price: $0.43/M input, $0.87/M output, blended (7:2:1) $0.18/M. Same source.
- Output speed: 71.7 tokens/sec (rank #25/93); TTFT: 1.77s. Same source.

### DeepSeek V3.2 (previous generation — CONFLICTING figures found, see note)

- AA dedicated model page: Intelligence Index **32** (non-reasoning), rank #12 of 43; price $0.50/M input, $1.60/M output, blended (3:1 ratio) $0.78/M; "Released December 2025." Source: https://artificialanalysis.ai/models/deepseek-v3-2
- AA's own model-comparison tool (DeepSeek V4 Flash 0731 vs. DeepSeek V3.2) instead shows V3.2 at Intelligence Index **"25 (estimated)"** and a blended price of **$0.29/M** — inconsistent with the dedicated page above. Source: https://artificialanalysis.ai/models/comparisons/deepseek-v4-flash-vs-deepseek-v3-2
- An older Artificial Analysis X post (dated prior to this research window) put V3.2 at Intelligence Index **66**. This is almost certainly on an older/different version of AA's Intelligence Index methodology (AA periodically rescales the index as it adds harder benchmarks) and is NOT comparable to the current 32/25 figures. Source: https://x.com/ArtificialAnlys/status/1996110256628539409
- **I could not reconcile these three figures for V3.2 with the sources available; all three are reported above with their exact URLs rather than picking one.**

---

## Comparison table

Scores are Artificial Analysis Intelligence Index unless noted. "—" = not verified / not available from a fetched source.

| Model | AA Intelligence Index (rank) | Input $/M | Output $/M | Blended $/M (7:2:1) | Output speed (tok/s) | Notes |
|---|---|---|---|---|---|---|
| **DeepSeek V4 Flash 0731** (subject) | **50** | $0.14 | $0.28 | $0.06 | 115.9 (main page) / 105–290 by provider | Open weights (MIT), 1M ctx, 284B/13B MoE. Released 2026-07-31. |
| GPT-5.6 Luna (max) | 51 (#15/1885) | $0.20 (post-cut, eff. 2026-07-30; was $1.00) | $1.20 (post-cut; was $6.00) | — (not recalculated post-cut) | 215.1 | OpenAI's cheap tier; 80% price cut same week as DeepSeek's release. |
| Gemini 3.6 Flash (high) | 50 (#21/187) | $1.50 | $7.50 | $1.16 | — | Batch/Flex tier: $0.75/$3.75. |
| Kimi K3 (max) | 57 (#4/1865) | $3.00 | $15.00 | $2.31 | 34.2 (slow) | Open-weights intelligence leader; DeepSeek trails it by 7 pts. |
| Qwen3.7 Max | 57 (#7/148) | $2.50 | $7.50 | $1.43 | 205.7 | Qwen 3.8 Max Preview exists (launched 2026-07-19) but has no published price or independent AA score yet. |
| Claude 4.5 Haiku (non-reasoning) | 24 est. (#26/71) | $1.00 | $5.00 | $0.77 | 91.5 | Anthropic's current cheapest self-serve model. |
| DeepSeek V4 Pro (max) | 44 (#3/93) | $0.43 | $0.87 | $0.18 | 71.7 | Prior DeepSeek flagship; V4 Flash 0731 now scores 6 pts higher. |
| DeepSeek V3.2 (non-reasoning) | 32 (#12/43) *(see conflicting-figures note above; comparison tool shows 25 est.)* | $0.50 | $1.60 | $0.78 *(comparison tool shows $0.29 blended)* | — | Two AA pages disagree; both cited above. |

---

## Unverified

- **Qwen 3.8 Max Preview pricing and independent AA Intelligence Index score** — not published by Alibaba / not yet benchmarked by AA as of source publication. https://techsy.io/en/blog/qwen-3-8
- **GPT-5.6 Luna TTFT of "103.52s"** on the AA model page — almost certainly wrong/stale/an extraction artifact given the model's 215 t/s output speed; do not publish this number without independent confirmation. https://artificialanalysis.ai/models/gpt-5-6-luna
- **DeepSeek V4 Flash 0731 per-provider TTFT of 20–56 seconds** on AA's provider-benchmarking subpage — implausibly high, possibly reflects a changed benchmarking workload (10k input tokens) rather than true latency; do not publish without confirmation. https://artificialanalysis.ai/models/deepseek-v4-flash/providers
- **DeepSeek V3.2's Intelligence Index score** — three different AA-linked figures found (32, 25 "estimated", and an older 66 from a differently-scaled index vintage); could not reconcile. See conflicting-figures note above.
- **Blended price for GPT-5.6 Luna at its new post-cut rate** — no source has recalculated this; only the old $0.87 blended figure exists.
- **Claude 4.5 Haiku's exact release date** — the AA page extraction returned "October 15, 2025," which may be a misparse; not independently re-confirmed against Anthropic's own announcement page in this pass.
- **The task's assumed "$0.35/M input" figure for GPT-5.6 Luna's Aug-1 price cut** — could not verify; the actual, twice-corroborated figure is $0.20/M input effective July 30, 2026 (not Aug 1). Treat the task's original figure as incorrect.
- **DeepSeek V4 Flash 0731's overall numeric leaderboard rank** (e.g., "#N of M" across all models, not just open-weights) — sources only state "top 3 open weights models," never a full-field rank number.
- **DeepSeek's self-reported benchmark table** (Terminal-Bench 2.1: 82.7, DeepSWE 645% jump, Agents' Last Exam 25.2, DSBench-FullStack 68.7) — explicitly flagged by TechTimes as not independently replicable; DeepSeek's benchmark harness is unreleased. Treat as company-reported, not independent.

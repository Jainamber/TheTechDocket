# Competitive Context: AI API Pricing Landscape (as of 2026-08-01)

Research pulled for: OpenAI's GPT-5.6 Luna (~-80%) / Terra (~-20%) API price cuts, announced/effective July 30, 2026. Purpose: comparison table + price-war narrative for The Tech Docket.

All numbers below carry their source URL on the same line/row. "Official" = vendor's own pricing/docs page. "Secondary" = press, aggregator, or third-party pricing-tracker site.

---

## (a) Pricing Table — Input & Output USD per 1M Tokens

### OpenAI (the subject of the cut — included for the comparison table)

| Provider | Model | Input $/1M | Output $/1M | Source URL | Official? |
|---|---|---|---|---|---|
| OpenAI | GPT-5.6 Sol (unchanged) | $5.00 | $30.00 | https://openai.com/index/gpt-5-6/ | Official |
| OpenAI | GPT-5.6 Terra — pre-cut | $2.50 | $15.00 | https://www.infoworld.com/article/4203865/openai-drops-gpt-5-6-luna-and-terra-api-prices-by-up-to-80.html | Secondary |
| OpenAI | GPT-5.6 Terra — post-cut (eff. Jul 30, 2026, ~20% cut) | $2.00 | $12.00 | https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/ | Official |
| OpenAI | GPT-5.6 Luna — pre-cut | $1.00 | $6.00 | https://www.infoworld.com/article/4203865/openai-drops-gpt-5-6-luna-and-terra-api-prices-by-up-to-80.html | Secondary |
| OpenAI | GPT-5.6 Luna — post-cut (eff. Jul 30, 2026, ~80% cut) | $0.20 | $1.20 | https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/ | Official |

Cross-checked (all agree on post-cut Luna $0.20/$1.20, Terra $2.00/$12.00, Sol unchanged $5/$30): https://www.axios.com/2026/07/30/openai-cuts-prices-gpt-terra-luna5 (Secondary) ; https://finance.yahoo.com/technology/ai/articles/openai-just-cut-gpt-5-013753910.html (Secondary) ; https://mlq.ai/news/openai-slashes-gpt-56-luna-prices-80-undercutting-deepseek-as-ai-price-war-intensifies/ (Secondary) ; https://www.aipricing.guru/openai-pricing/ (Secondary)

### Rivals

| Provider | Model | Input $/1M | Output $/1M | Source URL | Official? |
|---|---|---|---|---|---|
| Google | Gemini 3.1 Pro Preview (≤200k ctx) | $2.00 | $12.00 | https://ai.google.dev/gemini-api/docs/pricing | Official |
| Google | Gemini 3.1 Pro Preview (>200k ctx) | $4.00 | $18.00 | https://ai.google.dev/gemini-api/docs/pricing | Official |
| Google | Gemini 3.6 Flash | $1.50 | $7.50 | https://ai.google.dev/gemini-api/docs/pricing | Official |
| Google | Gemini 3.5 Flash | $1.50 | $9.00 | https://ai.google.dev/gemini-api/docs/pricing | Official |
| Google | Gemini 3.5 Flash-Lite (budget) | $0.30 | $2.50 | https://ai.google.dev/gemini-api/docs/pricing | Official |
| Google | Gemini 2.5 Flash-Lite (budget) | $0.10 (text) | $0.40 | https://ai.google.dev/gemini-api/docs/pricing | Official |
| Anthropic | Claude Opus 4.8 (flagship) | $5.00 | $25.00 | https://platform.claude.com/docs/en/about-claude/pricing | Official |
| Anthropic | Claude Sonnet 5 (intro, through Aug 31 2026) | $2.00 | $10.00 | https://platform.claude.com/docs/en/about-claude/pricing | Official |
| Anthropic | Claude Sonnet 5 (standard, from Sep 1 2026) | $3.00 | $15.00 | https://platform.claude.com/docs/en/about-claude/pricing | Official |
| Anthropic | Claude Haiku 4.5 (budget) | $1.00 | $5.00 | https://platform.claude.com/docs/en/about-claude/pricing | Official |
| Anthropic | Claude Fable 5 (premium tier) | $10.00 | $50.00 | https://platform.claude.com/docs/en/about-claude/pricing | Official |
| DeepSeek | DeepSeek-V4-Pro (cache miss) | $0.435 | $0.87 | https://api-docs.deepseek.com/quick_start/pricing/ | Official |
| DeepSeek | DeepSeek-V4-Pro (cache hit) | $0.003625 | $0.87 | https://api-docs.deepseek.com/quick_start/pricing/ | Official |
| DeepSeek | DeepSeek-V4-Flash (budget, cache miss) | $0.14 | $0.28 | https://api-docs.deepseek.com/quick_start/pricing/ | Official |
| DeepSeek | DeepSeek-V4-Flash (cache hit) | $0.0028 | $0.28 | https://api-docs.deepseek.com/quick_start/pricing/ | Official |
| Moonshot AI | Kimi K3 (`moonshotai/kimi-k3`) | $3.00 | $15.00 | https://openrouter.ai/moonshotai/kimi-k3 | Secondary (OpenRouter aggregator; could not confirm on a moonshot.cn/moonshot.ai first-party page this session) |
| Mistral | Mistral Large 3 (25-12) — flagship | $0.50 | $1.50 | https://docs.mistral.ai/models/model-cards/mistral-large-3-25-12 | Official |
| Mistral | Ministral 3B — budget | $0.10 | $0.10 | https://www.cloudzero.com/blog/mistral-api-pricing/ | Secondary (corroborated by https://www.aipricing.guru/mistral-ai-pricing/, also Secondary) |
| xAI | Grok 4.5 (flagship, launched Jul 8 2026) | $2.00 | $6.00 | https://www.sentisight.ai/how-much-does-grok-4-5-cost/ | Secondary |
| xAI | Grok 4.3 (prior tier, still sold as lower-cost option) | $1.25 | $2.50 | https://www.sentisight.ai/how-much-does-grok-4-5-cost/ | Secondary |
| Amazon | Nova 2.0 Pro Preview (non-reasoning) — newest flagship | $1.25 | $10.00 | https://artificialanalysis.ai/models/nova-2-0-pro | Secondary |
| Amazon | Nova Pro 1.0 (prior-gen, still listed) | $0.80 | $3.20 | https://pricepertoken.com/pricing-page/model/amazon-nova-pro-v1 | Secondary |
| Amazon | Nova Micro (budget) | $0.035 | $0.14 | https://devtk.ai/en/models/nova-micro/ | Secondary (cites AWS Bedrock as source; official AWS page https://aws.amazon.com/bedrock/pricing/ has the same data behind a collapsed UI panel I could not expand via fetch) |

---

## (b) AI Price-War Timeline

- **Jan 2025** — DeepSeek releases R1, priced "roughly 90-95% cheaper than comparable offerings from OpenAI and Anthropic," triggering the first wave of the price war. Source: https://siliconcanals.com/sc-n-chinas-deepseek-triggers-global-ai-price-war-as-tech-giants-slash-api-costs/ (Secondary). Same piece: OpenAI responded by "slashing prices on its GPT-4o mini model and accelerat[ing] the rollout of cheaper API tiers," Google DeepMind made "Gemini 1.5 Flash significantly more affordable," and Anthropic "introduced new batch processing options" — no exact dates given for these three responses in this source.

- **Feb 6, 2025** — Google ships Gemini 2.0 Flash at $0.10 input / $0.40 output per 1M tokens, explicitly undercutting DeepSeek-R1 (then $0.14–$0.55 input / $2.19 output per 1M) — source frames it as "Budget Gemini 2.0 takes aim at DeepSeek pricing." Source: https://cybernews.com/tech/google-releases-gemini-with-lower-price-tag-than-deepseek/ (Secondary).

- **Apr 27–28, 2026** — DeepSeek announces V4 (beta) pricing at ~97% below OpenAI's GPT-5.5 (DeepSeek cached-input ~$0.0036/1M under a temporary 75% discount vs. GPT-5.5's $0.5/1M cached input); DeepSeek says the reduced input-cache pricing (down to ~$0.14/1M standard) will be "permanent." Source: https://www.scmp.com/tech/tech-trends/article/3351595/chinas-deepseek-prices-new-v4-ai-model-97-below-openais-gpt-55 (Secondary, South China Morning Post). Around this same news cycle, investor Michael Burry posted on X: "the real news is OpenAI slashing and burning its prices to prepare for this" (referring to OpenAI's own recent cuts ahead of DeepSeek's V4 beta). Source: https://stocktwits.com/news-articles/markets/equity/openai-explains-why-it-cut-prices-michael-burry-real-news-deepseek-v4-models/cZN4ghERJPV (Secondary).

- **May 25, 2026** — DeepSeek cuts V4-Pro pricing ~75%: output falls from $3.48 to $0.87 per 1M tokens (cache-hit input from $0.0145 to $0.003625); promotional pricing (through May 31, 2026) is stated to become the permanent rate afterward. An unnamed analyst quoted in the piece said "high-margin, high-consumption token pricing models from Anthropic and OpenAI are becoming harder to justify for many enterprise workloads." Source: https://www.infoworld.com/article/4176709/deepseeks-steep-v4-pro-price-cut-escalates-ai-pricing-war.html (Secondary). Note: this may be the same discount episode as the Apr 27–28 SCMP item extended/re-covered a month later (the cache-hit figures are near-identical, ~$0.0036 vs $0.003625) rather than a fully separate second cut — flagged in section (d).

- **Jul 30, 2026** — OpenAI cuts GPT-5.6 Luna 80% (to $0.20/$1.20) and Terra 20% (to $2.00/$12.00); flagship Sol untouched at $5/$30. OpenAI's own stated rationale: efficiency gains "across every layer" (routing, hardware productivity, production software, context management), including GPT-5.6 Sol autonomously cutting serving costs ~20% and improving token-generation efficiency ~15%. Source: https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/ (Official). One outlet frames the cut as OpenAI "undercutting DeepSeek" on Luna's input price specifically ($0.20 vs. DeepSeek V4 Pro's discounted $0.435) while DeepSeek stays cheaper on output. Source: https://mlq.ai/news/openai-slashes-gpt-56-luna-prices-80-undercutting-deepseek-as-ai-price-war-intensifies/ (Secondary).

---

## (c) Analyst / Press Interpretation of the July 30, 2026 Cut

**Forbes — "OpenAI Cuts GPT-5.6 Pricing Up To 80%, As AI Costs Come Under Scrutiny" (Rachel Wells)**
URL: https://www.forbes.com/sites/rachelwells/2026/07/31/openai-cuts-gpt-56-pricing-up-to-80-as-ai-costs-come-under-scrutiny/ (Secondary)
- Frames the cut against a broader backdrop of enterprise AI-budget blowouts: cites Uber exhausting its full 2026 AI budget in Q1 after Claude Code usage scaled across 5,000 engineers, and Microsoft halting Claude Code usage when bills exceeded annual budgets within months.
- Quote, **Matteo Cellini** (Chief Marketing Officer and board advisor): "Here is the calculation seducing every boardroom right now: a model completes in seconds a task that takes an employee thirty minutes." Cellini's broader argument is that the *true* cost of AI systems often exceeds the cost of the employee-hours replaced once QA/accountability overhead is counted.
- Cites a **Harness survey** of ~700 finops/engineering leaders: 29% of organizations attribute >25% of total cloud spend to AI; 42% review AI costs only quarterly despite weekly spend swings; 40%+ still track AI costs via spreadsheets.
- Notes Microsoft's proposed shift from per-seat to per-seat-plus-consumption pricing, which would effectively raise enterprise AI budgets.
- Does not contain specific OpenAI pricing figures or direct competitor price comparisons — the piece's substance is enterprise cost-governance, using the OpenAI cut as its news hook.

**InfoWorld — "OpenAI drops GPT-5.6 Luna and Terra API prices by up to 80%"**
URL: https://www.infoworld.com/article/4203865/openai-drops-gpt-5-6-luna-and-terra-api-prices-by-up-to-80.html (Secondary)
- Quote, **Pareekh Jain** (Pareekh Consulting): "Lower prices make it easier to move pilots into production, expand AI across more employees and business processes."
- **Chandrika Dutt** (Avasant) said the savings will likely go toward "increasingly sophisticated agentic workflows that were previously difficult to justify economically."
- Attributes the cut to "improvements in serving efficiency that allow it to deliver more intelligence per dollar," citing training/inference stack optimizations and GPT-5.6 Sol's role in optimizing production GPU kernels. Mentions Anthropic, Google, and Microsoft as rival model providers but does not mention DeepSeek by name.

**Yahoo Finance — "OpenAI Just Cut GPT-5.6 Luna's Price by 80 Percent – and That Tells You Where the Pressure Is Coming From" (byline: Lena Park)**
URL: https://finance.yahoo.com/technology/ai/articles/openai-just-cut-gpt-5-013753910.html (Secondary; also mirrored at https://forkast.news/openai-just-cut-gpt-5-6-lunas-price-by-80-percent-and-that-tells-you-where-the-pressure-is-coming-from/)
- Core argument: the cut reflects "eroding pricing power" from intense inference-market competition; by cutting mid/low-tier pricing while leaving flagship Sol untouched, OpenAI is defending its mid-tier volume business while preserving premium-tier margin.
- Cites a **CNBC investigation** (not independently verified by this research session — CNBC's own page 403'd on fetch) claiming Chinese models captured 46% of US enterprise token usage on OpenRouter.
- Lays out DeepSeek V4 Pro at $0.435/$0.87 per 1M (with a 75% promotional discount) and Kimi K3 at $3/$15 per 1M as the Chinese-model comparison set undercutting OpenAI.
- No named analyst quotes in this piece — analysis is the author's own, built on the CNBC data point.

**Decrypt — "OpenAI Wants a Price War With Anthropic—Is It Proving DeepSeek Right?"**
URL: https://decrypt.co/370854/openai-price-war-anthropic-deepseek-china (Secondary)
- Argues a Western (OpenAI vs. Anthropic) price war may be strategically futile because Chinese open-weight models (DeepSeek, etc.) already undercut both by roughly 13x.
- Financial data cited: OpenAI's adjusted operating margin was **-122% in Q1 2026**; Anthropic's annualized revenue rose from **$9B (end of 2025) to $47B (May 2026)** — a 422% increase in five months — and Anthropic posted its first profitable quarter in Q2 2026. Also notes ChatGPT's global generative-AI traffic share fell from 77.6% (May 2025) to 53.7% (April 2026), and that more companies now pay Anthropic than OpenAI per the Ramp AI Index.
- Quote, **Sam Altman**: "I think we'll have a lot of ways we can help people get more value for less spend."
- Unattributed line in the piece on why Chinese labs can undercut structurally: "The model is the single biggest cost an inference provider has, and they get it for free" (referring to open-weight Chinese models).

**Axios — "OpenAI discounts GPT-5.6 Luna and Terra, but not [Sol]"**
URL: https://www.axios.com/2026/07/30/openai-cuts-prices-gpt-terra-luna5 (Secondary)
- OpenAI quote: it can now deliver "substantially more intelligence per dollar through efficiency improvements."
- Notes the cut lands just three weeks after GPT-5.6's original launch — reads it as an aggressive, fast repositioning move — and ties it to pressure from "cheaper Chinese open-weight models" generally (no specific DeepSeek figures in this piece).

**Stocktwits — on Michael Burry's reaction (see timeline entry above for the quote)**
URL: https://stocktwits.com/news-articles/markets/equity/openai-explains-why-it-cut-prices-michael-burry-real-news-deepseek-v4-models/cZN4ghERJPV (Secondary)
- Also carries OpenAI's own framing (from around the April 2026 cut cycle, not the July 30 one): lower prices "make artificial intelligence more broadly accessible," expanding the range of economically viable tasks customers can automate, generating demand that funds next-generation model development.

---

## (d) OpenAI Scale / Financial Data Tied to the Cut

All figures below are third-party estimates/reporting on a private company — OpenAI does not publicly disclose full financials. Treat as directional, not audited.

- **$25B ARR** as of end of February 2026, up 17% from **$21.4B** at end of 2025 — originally reported by **The Information**, relayed via https://incrypted.com/en/openais-annual-revenue-surpasses-25-billion-report/ (Secondary).
- **~$2B/month** revenue run-rate; **$13.1B** actual booked revenue for full-year 2025; **$30B** internal revenue target for full-year 2026; **-122% non-GAAP operating margin** in Q1 2026 ("lost about $1.22 for every dollar of revenue booked"). Source: https://valueaddvc.com/blog/openai-revenue-2026-25b-arr-2b-month-and-the-path-to-profitability (Secondary, analyst blog).
- **$122B raised on March 31, 2026 at an $852B valuation.** Source: https://valueaddvc.com/blog/openai-revenue-2026-25b-arr-2b-month-and-the-path-to-profitability (Secondary).
- **Stargate infrastructure commitment — contested figure, see (d) conflicts below.** Most-recent figure found: pledge cut from an original **$1.4 trillion over 8 years** (Altman, late 2025) down to **$600 billion through 2030**, announced to investors in Feb 2026 after CFO Sarah Friar said she "was not certain whether the company's revenue growth would support those commitments"; OpenAI is reportedly shifting toward renting compute rather than building it. Source: https://www.techtimes.com/articles/316807/20260519/openai-cut-stargates-spending-pledge-14-trillion-600-billion-now-renting-what-it-vowed-build.htm (Secondary).
- **~$13B Microsoft compute-partnership commitment** cited alongside the Stargate figure. Source: https://valueaddvc.com/blog/openai-revenue-2026-25b-arr-2b-month-and-the-path-to-profitability (Secondary).
- For comparative context: **Anthropic's ARR reached $47B by mid-May 2026**, having overtaken OpenAI's revenue run-rate on some measures. Source: https://decrypt.co/370854/openai-price-war-anthropic-deepseek-china (Secondary).

---

## (e) Uncertain / Conflicting Data — Flag Before Publishing

1. **Mistral Large 3 pricing is genuinely conflicting across sources.** Official Mistral docs model card (https://docs.mistral.ai/models/model-cards/mistral-large-3-25-12 — Official) states $0.50 input / $1.50 output, matching https://www.cloudzero.com/blog/mistral-api-pricing/ (Secondary). But https://tokenmix.ai/blog/mistral-api-pricing (Secondary) and https://www.aipricing.guru/mistral-ai-pricing/ (Secondary, dated 2026-08-01) both show $2.00/$6.00 for "Mistral Large" — and the official https://mistral.ai/pricing/ FAQ text itself uses a "$2/$6" example for "Mistral Large" (ambiguous whether that's legacy Large 2 or stale copy). **Recommend using $0.50/$1.50 (the model-card-specific page) as the Large 3 figure**, but this is not fully reconciled — the $2/$6 figure may reflect a still-listed older "Mistral Large 2" tier rather than an error.

2. **Stargate compute-commitment figure is inconsistent across outlets.** Found variously as $500B (https://cryptobriefing.com/openai-stargate-data-center-expansion-2026/ and OpenAI's own https://openai.com/index/five-new-stargate-sites/, both not independently re-verified by fetch this session beyond the search snippet) vs. an explicit $1.4T-pledge-cut-to-$600B narrative (Techtimes, above, which does cite specific investor-communication context and a date). Unclear if $500B is a rounded or superseded figure, or a different tranche/JV entity than the $600B "through 2030" figure.

3. **DeepSeek's Apr 27–28, 2026 (SCMP) and May 25, 2026 (InfoWorld) price-cut stories may describe the same discount episode rather than two distinct cuts** — the reported cache-hit input prices are nearly identical (~$0.0036 vs. $0.003625), and both reference a temporary promo becoming permanent. Timeline entry above notes this; do not double-count as two separate cuts in copy.

4. **Amazon Nova "flagship" is ambiguous.** Nova 2.0 Pro is the newest generation (still labeled "Preview" as of the source date) at $1.25/$10.00 (https://artificialanalysis.ai/models/nova-2-0-pro — Secondary), while the longer-established Nova Pro 1.0 ($0.80/$3.20) may still be what's generally available/quoted by default. Table above includes both — pick based on which AWS is billing as GA vs. preview at publish time.

5. **Kimi K3 pricing sourced only from OpenRouter (aggregator), not a Moonshot first-party page.** Could not locate/fetch a moonshot.cn or moonshot.ai official pricing page in this session; treat $3/$15 as reliable-but-secondary. (BenchLM.ai's aggregator page independently shows the same $3/$15 figure, which corroborates but doesn't upgrade the sourcing tier.)

6. **The "46% of Chinese-model share of US enterprise OpenRouter tokens" statistic** (used by the Yahoo Finance/Forkast analytical piece to explain competitive pressure) traces to a CNBC investigation that returned a 403 error on direct fetch (https://www.cnbc.com/2026/07/30/open-ai-price-cut-gpt.html) — reported here only second-hand via Yahoo Finance and not independently confirmed against the CNBC original.

7. **xAI's "budget" tier is not a purpose-built low-cost model** — Grok 4.3 is simply the prior flagship generation still being sold alongside the newer, pricier Grok 4.5, unlike the dedicated nano/mini/lite tiers other vendors offer. Worth a caveat if the table is presented as flagship-vs-budget apples-to-apples.

8. **GPT-5.6 Terra/Luna pre-cut prices** come from InfoWorld's reporting (Secondary), not an archived OpenAI page — I could not locate an OpenAI-official page still showing pre-cut pricing (the live official launch page https://openai.com/index/gpt-5-6/ , checked this session, still displayed what reads as original launch pricing: Sol $5/$30, Terra $2.50/$15, Luna $1/$6 — consistent with the "pre-cut" figures used above, which somewhat re-confirms them, but note this page may simply be stale/uncached rather than a snapshot of history).

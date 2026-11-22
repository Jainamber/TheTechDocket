---
title: 'Cursor Weighs Dropping Chinese AI as Sarvam Sells DeepSeek'
slug: cursor-chinese-open-weight-models-sarvam-deepseek
date: '2026-11-22'
hub: ai-models
tags: [ai-models, open-source, cursor, india-ai, deepseek]
description: A 50-page US House report reveals Cursor, Airbnb, and DoorDash rely on Chinese open-weight models, even as India's Sarvam hosts DeepSeek at 450B tokens daily.
hero_alt: Split diagram showing US House committee report on Chinese open-weight AI models alongside India domestic inference servers
hero_icon: globe
keyword: Chinese open-weight AI models
original_value: Contrasts the November 2026 US House investigation into Cursor, Airbnb, and DoorDash with India's Sarvam Token Factory strategy, calculating the exact USD-to-INR token cost gap that drives developer adoption.
selection_note: ''
sources:
- {title: 'Airbnb handles 80,000 chats a day with Alibaba''s open-weight Qwen — MACCUS', url: 'https://maccus.fr/en/chinese-ai-models-house-report/', primary: true}
- {title: 'Cursor may drop Chinese AI models as India''s Sarvam starts selling them — The Next Web', url: 'https://thenextweb.com/news/cursor-chinese-ai-models-house-report-sarvam-deepseek', primary: true}
- {title: 'Cursor May Drop Chinese AI Models: House Report Explained — explainx.ai', url: 'https://explainx.ai/blog/cursor-spacex-may-phase-out-chinese-open-weight-models-house-report-kimi-composer-2-2026'}
- {title: 'House report urges removal of Chinese open-weight AI models — AI Chat Daily', url: 'https://www.aichatdaily.com/ai-security/house-report-urges-removal-chinese-open-weight-ai-models'}
- {title: 'USD to INR Exchange Rate History — Wise', url: 'https://wise.com/in/currency-converter/usd-to-inr-rate/history'}
faq:
- {q: 'Why is Cursor considering phasing out Chinese open-weight AI models?', a: 'Anysphere, the developer of Cursor now owned by SpaceX, informed two US House committees that it plans to explore phasing out Chinese-developed open-weight models over geopolitical risk after building its Composer 2 model on Moonshot AI Kimi base weights.'}
- {q: 'How do Airbnb and DoorDash use Chinese open-weight models?', a: 'According to the joint US House report, Airbnb runs customized versions of Alibaba Qwen on US servers to handle customer chats and summarize support tickets, while DoorDash evaluated or deployed models across multiple Chinese open-weight families.'}
- {q: 'Why is India''s Sarvam hosting DeepSeek and Moonshot models?', a: 'Sarvam launched its Token Factory platform using privately funded chips to serve open-weight models like DeepSeek and Moonshot inside Indian data centers, keeping developer prompts and customer data within India while offering low-cost token inference.'}
review: {facts_verified: true, sources_checked: true, title_promise_check: true, no_fabrication: true, policy_pass: true, reviewed_at: '2026-11-22T06:05:00+05:30'}
---

SpaceX-owned coding platform Cursor has told US lawmakers it will explore phasing out Chinese open-weight models after building Composer 2 on Moonshot AI's Kimi K2.5, according to a 50-page joint US House committee report detailed by [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/) and [The Next Web](https://thenextweb.com/news/cursor-chinese-ai-models-house-report-sarvam-deepseek). The report reveals that Airbnb handles 80,000 chats daily on Alibaba's Qwen and DoorDash deployed 25 Chinese model families, while in India, sovereign AI startup Sarvam is moving the opposite way—serving over 450 billion tokens a day on DeepSeek V4.1 Flash from domestic servers.

## Inside the 50-Page US House Investigation Into Cursor, Airbnb, and DoorDash

Released on November 20, 2026, by the House Committee on Homeland Security and the House Select Committee on China, the 50-page report titled *Beijing's AI Playbook* documents how deeply Chinese open-weight models sit inside top US software companies, as summarized by [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/). Following formal inquiry letters sent on April 29 and July 31, 2026, Airbnb, DoorDash, and Cursor developer Anysphere turned over internal engineering records showing that a six-to-30-fold price advantage drove them to Chinese weights.

For Anysphere, which SpaceX acquired in August 2026 at an implied $60 billion equity valuation according to [explainx.ai](https://explainx.ai/blog/cursor-spacex-may-phase-out-chinese-open-weight-models-house-report-kimi-composer-2-2026), the scrutiny centered on Composer 2, Cursor's proprietary coding model. The committees noted that Anysphere trained Composer 2 on top of Moonshot AI's Kimi K2.5, a lineage that became public only in March 2026 after an external developer identified the base architecture, per [AI Chat Daily](https://www.aichatdaily.com/ai-security/house-report-urges-removal-chinese-open-weight-ai-models). Anysphere informed lawmakers it plans to explore phasing out Chinese-developed open-weight models over geopolitical risk, though it has set no timeline or replacement model.

The consumer disclosures in the report are even more concrete. Airbnb runs customized versions of Alibaba's Qwen models on US servers to power an assistant handling roughly 80,000 guest and host conversations daily and a second pipeline summarizing 250,000 daily support cases and calls, according to [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/). DoorDash told the committees it authorized and deployed 25 Chinese model families, each with at least $5,000 in compute spend, and estimated that ripping out one deeply integrated model would take up to six months.

We have tracked this steady migration across [AI Models](/ai-models/) all year, from the release wave we covered in [Chinese AI Models Surge: Kimi K3, Qwen 3.8](/articles/chinese-ai-models-surge-kimi-qwen/) and [Qwen3.8-Max](/articles/qwen3-8-max-what-alibaba-launched/) to the developer cost push behind [Claude Code vs Pi](/articles/claude-code-pi-developers-swapping-terminal-agents/).

## The 6x to 30x Token Economics Driving Open-Weight Adoption

According to the benchmark table compiled in the House report and verified by [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/), a standard workload of 1 million input tokens plus 1 million output tokens costs $1.15 on Alibaba's Qwen3-235B and $2.74 on DeepSeek-R1, compared with $30.00 on Anthropic's Claude Opus 4.8 and $35.00 on OpenAI's GPT-5.5. That pricing gap explains why Chinese weights accounted for 41% of all Hugging Face downloads over the trailing 12 months cited in the report, and why six Chinese models ranked ahead of the top US open-weight model (10th place) in the September 2026 Artificial Analysis rankings.

| Model / Workload Benchmark | 1M Input + 1M Output (USD) | India Effective Cost (INR incl. Taxes) | Key House Report / Market Finding |
| :--- | :--- | :--- | :--- |
| **Alibaba Qwen3-235B (Open-Weight)** | $1.15 ([MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/)) | ₹130.17 ([Wise FX](https://wise.com/in/currency-converter/usd-to-inr-rate/history)) | Powers 80,000 chats & 250,000 summaries/day at Airbnb |
| **DeepSeek-R1 (Open-Weight)** | $2.74 ([MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/)) | ₹310.14 ([Wise FX](https://wise.com/in/currency-converter/usd-to-inr-rate/history)) | Barred in US federal civilian agencies since July/Oct 2026 |
| **Moonshot AI Kimi K2.6 / K2.5** | $4.95 ([MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/)) | ₹560.29 ([Wise FX](https://wise.com/in/currency-converter/usd-to-inr-rate/history)) | Kimi K2.5 served as base model for Cursor Composer 2 |
| **Anthropic Claude Opus 4.8 (Closed)** | $30.00 ([MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/)) | ₹3,395.67 ([Wise FX](https://wise.com/in/currency-converter/usd-to-inr-rate/history)) | 6x to 26x more expensive per 2M-token combined bundle |
| **OpenAI GPT-5.5 (Closed)** | $35.00 ([MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/)) | ₹3,961.62 ([Wise FX](https://wise.com/in/currency-converter/usd-to-inr-rate/history)) | 30x cost of Qwen3-235B; Revolut cut coding bill 90% via GLM |

*Note: India effective USD API cost calculated at the November 21, 2026 spot rate of ₹92.683 per USD ([Wise](https://wise.com/in/currency-converter/usd-to-inr-rate/history)) plus 3.5% bank forex markup and 18% IGST on USD card billing.*

The savings are not theoretical. As noted by [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/), digital bank Revolut self-hosts Zhipu's open-weight GLM model for internal software engineering and reported that its AI coding bill dropped to one-tenth (a 90% reduction) of what it previously paid Anthropic and OpenAI.

## Why US Lawmakers Say Local Hosting Is Not Enough

Hosting Chinese open-weight models on domestic US servers stops prompt data from flowing to Beijing, yet the House committees argue that local hosting cannot fix embedded model behavior or supply-chain lock-in, producing 12 policy recommendations detailed by [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/). The report cites CrowdStrike testing showing DeepSeek's reasoning model was up to 50% more likely to generate code with severe security flaws when prompts touched topics politically sensitive to Beijing, alongside an Anthropic and NIST analysis where $4,400 of compute stripped Zhipu GLM-5.3's safety refusals from 95% down to 3%–6%.

Commercial licensing traps also worry lawmakers. Moonshot AI's Kimi K3 license requires any commercial SaaS provider exceeding $20 million in trailing 12-month revenue to negotiate a separate paid agreement with Moonshot, according to [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/). To break that dependency, the committees recommend extending the October 2026 federal DeepSeek ban across all Chinese models (and fine-tuned or quantized derivatives) in federal contracts and critical infrastructure, mandating a NIST "AI bill of materials," and funding a national US open-weight initiative.

## The India Angle

While Washington debates banning Chinese weights, Indian sovereign AI unicorn Sarvam has launched its "Token Factory" service hosting DeepSeek, Moonshot, and Z.ai models on Indian servers, already processing more than 450 billion tokens per day on DeepSeek V4.1 Flash alone, according to Bloomberg reporting cited by [The Next Web](https://thenextweb.com/news/cursor-chinese-ai-models-house-report-sarvam-deepseek). The move sparked immediate debate in India because Sarvam receives subsidized compute backing under the government's IndiaAI Mission and recently signed a defence ministry AI contract, though co-founders Pratyush Kumar and Vivek Raghavan stated that Token Factory runs on chips funded entirely by private capital.

For Indian engineering teams, the arithmetic explains why Sarvam's domestic hosting is drawing 450 billion tokens a day. At the November 21, 2026 exchange rate of ₹92.683 per US dollar reported by [Wise](https://wise.com/in/currency-converter/usd-to-inr-rate/history), an Indian startup processing 500 million input tokens and 500 million output tokens per month on a USD-billed closed frontier API like OpenAI GPT-5.5 ($35.00 per 1M+1M bundle per [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/)) pays $17,500 before fees, which balloons to ₹19,80,810 per month (₹2.38 crore per year) once a 3.5% bank forex markup and 18% IGST are applied.

Running that exact same 1-billion-token monthly workload on Qwen3-235B ($1.15 per 1M+1M bundle) or DeepSeek-R1 ($2.74 per bundle) cuts the effective cost to ₹65,085 or ₹1,55,070 per month respectively—a 92% to 96.7% cost reduction, using the [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/) benchmark rates and [Wise](https://wise.com/in/currency-converter/usd-to-inr-rate/history) spot FX. When served domestically in rupees by an Indian provider like Sarvam, teams also eliminate the 3.5% foreign-card fee, claim full 18% GST input tax credit, and keep customer prompts inside Indian jurisdiction under the DPDP Act rules we analyzed in [The Real Cost of Running AI](/articles/real-cost-of-running-ai/) and [DeepSeek API Price Hike](/articles/deepseek-api-price-hike/).

## What to Watch

Three near-term checkpoints will show whether Washington's crackdown reshapes global developer tooling or accelerates a split between US federal compliance stacks and the rest of the world:

1. **Cursor's Composer 3 Base-Model Decision:** Watch whether SpaceX-backed Cursor migrates Composer off Moonshot's Kimi K2.5 onto a Grok base model, a new US open-weight release like Reflection AI's Beam or Thinking Machines Lab's [Inkling 2 Mini](/articles/inkling-2-mini-looped-transformer-laptops/), or keeps Kimi for non-federal commercial tiers, as tracked by [explainx.ai](https://explainx.ai/blog/cursor-spacex-may-phase-out-chinese-open-weight-models-house-report-kimi-composer-2-2026).
2. **NIST's AI Bill of Materials & Federal Contractor Rules:** Indian IT services exporters and SaaS startups serving US federal agencies or US critical infrastructure must audit their fine-tuned and quantized models now; if Congress adopts the House report's derivative-model ban reported by [MACCUS](https://maccus.fr/en/chinese-ai-models-house-report/), any wrapper built on Qwen, Kimi, or DeepSeek weights will require a six-month swap plan.
3. **IndiaAI Mission Policy on Dual-Track Hosting:** Watch whether India's Ministry of Electronics and Information Technology (MeitY) issues formal provenance guidelines separating publicly subsidized sovereign model training from privately funded domestic inference clouds like Sarvam's 450-billion-token-per-day DeepSeek service reported by [The Next Web](https://thenextweb.com/news/cursor-chinese-ai-models-house-report-sarvam-deepseek).

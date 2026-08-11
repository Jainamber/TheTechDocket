---
title: "Muse Glimmer: Meta's Open 30B Model, and the U-Turn Behind It"
slug: "muse-glimmer-meta-open-model"
date: 2026-08-11
hub: ai-models
tags: [meta, open-source, ai-agents, zuckerberg, local-ai, india]
description: "Meta's Muse Glimmer puts a 30B open-weight agent model on one consumer GPU, under Apache 2.0. What shipped, what the benchmarks hide, and why Meta flipped back."
hero_alt: "A small glowing chip sits unlocked on a desk while a larger sealed vault model looms in the background."
keyword: "muse glimmer"
original_value: "Places the Glimmer release inside Meta's dated open-closed-open zigzag, separates Meta's self-reported benchmark wins from independent measurements, and tests the open-weights pitch against India's own sovereign-model bets — Sarvam's Apache 2.0 releases and Krutrim's retreat."
sources:
  - {title: "Introducing Muse Glimmer — Meta AI Research (official)", url: "https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model", primary: true}
  - {title: "The Future Is for Everyone — Mark Zuckerberg, Meta (official)", url: "https://www.meta.com/thefutureisforeveryone/", primary: true}
  - {title: "Introducing Muse Spark 1.1 — Meta AI (official)", url: "https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/", primary: true}
  - {title: "Open Source AI Is the Path Forward — Meta, July 2024 (official)", url: "https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/", primary: true}
  - {title: "Personal Superintelligence for Everyone — Meta, July 2025 (official)", url: "https://about.fb.com/news/2025/07/personal-superintelligence-for-everyone/", primary: true}
  - {title: "Meta returns to open source with Muse Glimmer — VentureBeat", url: "https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now"}
  - {title: "Meta debuts first major AI model since Alexandr Wang deal — CNBC, April 2026", url: "https://www.cnbc.com/2026/04/08/meta-debuts-first-major-ai-model-since-14-billion-deal-to-bring-in-alexandr-wang.html"}
  - {title: "Meta releases Muse Glimmer, takes swipe at OpenAI, Anthropic — CNBC", url: "https://www.cnbc.com/2026/08/10/meta-muse-glimmer-open-weight-ai.html"}
  - {title: "Muse Glimmer — Meta AI Releases 30B Open-Weights Agentic Model — MarkTechPost", url: "https://www.marktechpost.com/2026/08/10/meta-ai-releases-muse-glimmer/"}
  - {title: "Muse Glimmer on Ollama (official library listing)", url: "https://ollama.com/library/muse-glimmer", primary: true}
  - {title: "Meta's Muse Glimmer beats Gemma4-31B on most benchmarks — OfficeChai", url: "https://officechai.com/ai/metas-releases-muse-glimmer-local-model-beats-googles-gemma4-31b-on-most-benchmarks/"}
  - {title: "Muse Glimmer analysis — Artificial Analysis (independent benchmarks)", url: "https://artificialanalysis.ai/articles/muse-glimmer"}
  - {title: "Zuckerberg reveals AI plans in lengthy manifesto — Yahoo Finance", url: "https://finance.yahoo.com/technology/article/metas-zuckerberg-reveals-ai-plans-in-lengthy-manifesto-derides-rivals-for-concentrating-power-152245348.html"}
  - {title: "Zuckerberg surprised AI discourse 'so filled with doom' — Variety", url: "https://variety.com/2026/biz/news/meta-ai-manifesto-mark-zuckerberg-1236831435/"}
  - {title: "Mark Zuckerberg's AI manifesto is exactly why people don't like AI — TechCrunch", url: "https://techcrunch.com/2026/08/10/mark-zuckerbergs-ai-manifesto-is-exactly-why-people-dont-like-ai/"}
  - {title: "Zuckerberg on open-source models, Q2 2026 earnings call — Yahoo Finance", url: "https://finance.yahoo.com/technology/ai/articles/mark-zuckerberg-says-cant-rely-053051819.html"}
  - {title: "Inside Meta's pivot from open source — Bloomberg, December 2025", url: "https://www.bloomberg.com/news/articles/2025-12-10/inside-meta-s-pivot-from-open-source-to-money-making-ai-model"}
  - {title: "Introducing gpt-oss — OpenAI (official)", url: "https://openai.com/index/introducing-gpt-oss/", primary: true}
  - {title: "The open-weight models that matter, June 2026 — OpenRouter (official data)", url: "https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026/", primary: true}
  - {title: "Open-Sourcing Sarvam 30B and 105B — Sarvam AI (official)", url: "https://www.sarvam.ai/blogs/sarvam-30b-105b", primary: true}
  - {title: "Sarvam's new models are a major bet on open source AI — TechCrunch", url: "https://techcrunch.com/2026/02/18/indian-ai-lab-sarvams-new-models-are-a-major-bet-on-the-viability-of-open-source-ai/"}
  - {title: "India to deploy 38,000 GPUs under IndiaAI — Tribune India", url: "https://www.tribuneindia.com/news/business/india-to-deploy-38000-gpus-set-up-600-data-labs-to-strengthen-ai-ecosystem-meity"}
  - {title: "Krutrim pauses model and chip work, pivots to AI cloud — MediaNama", url: "https://www.medianama.com/2026/05/223-krutrim-ai-cloud-chip-ai-model-work/"}
  - {title: "Meta-Reliance strategic partnership for Llama-based enterprise AI — Meta (official)", url: "https://about.fb.com/news/2025/08/accelerating-indias-ai-adoption-a-strategic-partnership-with-reliance-industries-to-build-llama-based-enterprise-ai-solutions/", primary: true}
  - {title: "India is the largest market for Meta AI usage — TechCrunch, 2024", url: "https://techcrunch.com/2024/07/31/india-is-the-largest-market-for-meta-ai-usage"}
  - {title: "RTX 4090 graphics card listings, India — PrimeABGB", url: "https://www.primeabgb.com/buy-online-price-india/geforce-rtx-4090-graphic-card/"}
faq:
  - {q: "What is Meta's Muse Glimmer?", a: "Muse Glimmer is a 30-billion-parameter AI model that Meta released on August 10, 2026 with its weights openly downloadable under an Apache 2.0 license. It is built for running AI agents — software that plans, uses tools and completes multi-step tasks — entirely on a local machine, without a cloud connection."}
  - {q: "Is Muse Glimmer free for commercial use?", a: "Yes. Apache 2.0 is a standard permissive software license, so companies can use, modify and redistribute the model commercially with no user cap. Meta's earlier Llama models used a custom license that made the very largest platforms negotiate a separate agreement; Glimmer drops that restriction."}
  - {q: "What do you need to run Muse Glimmer locally?", a: "The compressed 4-bit build is about an 18 GB download and is designed to fit on a 24 GB graphics card, such as an RTX 4090-class GPU, or a Mac or AI PC with similar unified memory. Full precision needs more than 55 GB of memory, which puts it beyond most consumer hardware."}
  - {q: "Is Muse Glimmer better than Qwen or Gemma?", a: "It depends on the task and on whose numbers you trust. Meta's own comparison table shows Glimmer leading Gemma4-31B and Qwen3.6-27B on agentic benchmarks like MCP-Atlas, while trailing Qwen on terminal and computer-use tests. Independent measurement by Artificial Analysis also flags a high hallucination rate, so treat the marketing table as a starting point, not a verdict."}
review:
  facts_verified: true
  sources_checked: true
  title_promise_check: true
  no_fabrication: true
  policy_pass: true
  reviewed_at: "2026-08-11T08:05:00+05:30"
---

Meta released Muse Glimmer on August 10 — a 30-billion-parameter model whose weights anyone can [download and use commercially under an Apache 2.0 license](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model), built to run AI agents on a single consumer graphics card with no cloud connection. It is Meta's first open release since the company went fully proprietary with Muse Spark in April, and it arrived with a 6,500-word Mark Zuckerberg essay arguing that concentrated control of AI, not AI itself, is the real danger. The model is real and downloadable today; the strategy behind it has reversed twice in two years.

## What Meta actually shipped

Muse Glimmer is a dense model — every parameter activates on every token, unlike the mixture-of-experts designs most large models now use — [distilled from Muse Spark, Meta's closed flagship](https://www.cnbc.com/2026/08/10/meta-muse-glimmer-open-weight-ai.html). Distillation means the smaller model is trained to imitate the bigger one's outputs, so Meta is effectively open-sourcing a compressed copy of its best work while keeping the original behind its API.

The design target is what Meta calls "always-on local agent workflows": coding agents, tool calling, long multi-step tasks and failure recovery, running on hardware you own. [A 30B model normally needs over 55 GB of memory at full precision](https://www.marktechpost.com/2026/08/10/meta-ai-releases-muse-glimmer/); Meta ships a 4-bit compressed build, paired with a small "DFlash" drafter model that speeds up generation, sized to fit a 24 GB graphics card. On [Ollama's official listing](https://ollama.com/library/muse-glimmer), the 4-bit download is roughly 18 GB, and the higher-quality 8-bit build about 31 GB. The weights are on Hugging Face, with day-one support from NVIDIA, AMD and Apple Silicon toolchains.

The license is the quiet headline. Meta's Llama models shipped under a custom "community license" that, among other restrictions, required companies with more than 700 million monthly users to negotiate separately. Glimmer's Apache 2.0 license has no such cap — the same standard terms [OpenAI chose for its gpt-oss models](https://openai.com/index/introducing-gpt-oss/) in August 2025 and Google adopted for Gemma 4 this April. On licensing, at least, the open-model camp has converged.

## The benchmarks, with the asterisks attached

Meta's announcement compares Glimmer to the two open models closest in size, and the pattern is consistent: Glimmer wins the agent tests, loses the computer-driving tests.

| Benchmark (what it measures) | Muse Glimmer | Gemma4-31B | Qwen3.6-27B |
|---|---|---|---|
| MCP-Atlas (tool orchestration) | **75.5** | 54.2 | 62.5 |
| DeepSearch QA (research with tools) | **74.6** | 61.7 | 71.1 |
| SWE-Bench Pro (real coding fixes) | **51.2** | 36.9 | — |
| TerminalBench 2.1 (command line) | 51.7 | 43.4 | **60.7** |
| OSWorld-Verified (operating a desktop) | 65.9 | — | **75.6** |

These are [Meta's own reported numbers](https://officechai.com/ai/metas-releases-muse-glimmer-local-model-beats-googles-gemma4-31b-on-most-benchmarks/), and they deserve the standard caveats: Meta ran the rival models itself rather than using each vendor's best published scores, so independent replication is still pending. The first outside measurements add a sharper one — [Artificial Analysis flags an 82% hallucination rate](https://artificialanalysis.ai/articles/muse-glimmer) in its testing, against 49% for Qwen3.6-27B, meaning Glimmer answers confidently even when it should say it does not know. For an "always-on" agent acting on your behalf, that trade-off matters more than a leaderboard rank.

## Two years of zigzag, in five dates

Glimmer only makes sense against the timeline it reverses. In July 2024, Zuckerberg published ["Open Source AI Is the Path Forward"](https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/), committing Meta to open frontier models. A year later, [the commitment softened](https://about.fb.com/news/2025/07/personal-superintelligence-for-everyone/) — Meta would be "careful about what we choose to open source." By December 2025, [Bloomberg reported Meta was building a closed, revenue-focused model](https://www.bloomberg.com/news/articles/2025-12-10/inside-meta-s-pivot-from-open-source-to-money-making-ai-model) codenamed Avocado, and in [April 2026 Muse Spark launched](https://www.cnbc.com/2026/04/08/meta-debuts-first-major-ai-model-since-14-billion-deal-to-bring-in-alexandr-wang.html) as exactly that: Meta's first fully proprietary flagship, later [monetized through a paid API](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/) in July.

As recently as Meta's July 30 earnings call, Zuckerberg was hedging: asked about relying on open models, he said ["the open-source models are not as strong as the frontier models, so no is the basic answer"](https://finance.yahoo.com/technology/ai/articles/mark-zuckerberg-says-cant-rely-053051819.html) — while promising Meta would "get back to releasing some open source models" soon. Eleven days later, Glimmer shipped, and Meta says weights for Muse Spark 1.2 — the bigger model — will follow "in the coming weeks." That promise, not Glimmer itself, is the real test of the U-turn: so far the open release is the distilled copy, and the flagship stays closed.

The competitive logic is not subtle. Chinese open models have spent 2026 setting the pace — [Alibaba's Qwen3.8-Max](/articles/qwen3-8-max-what-alibaba-launched/) at the top of the size ladder, and [DeepSeek's V4 Flash](/articles/deepseek-v4-flash-0731/) shipping MIT-licensed weights with API prices that undercut everyone, part of the same price war behind [OpenAI's steep API price cut](/articles/gpt-5-6-luna-price-cut/) this month. Meta's essay explicitly argues the answer to Chinese open-model momentum is better American open models, not restrictions.

## The manifesto and the pushback

The essay, titled ["The Future Is for Everyone"](https://www.meta.com/thefutureisforeveryone/), is organized around one claim: who controls superintelligence matters more than any specific capability risk. "The notion that AI is so dangerous that the only safe path is an extreme concentration of power seems inherently problematic," Zuckerberg writes, arguing that "rather than centralizing superintelligence, we should distribute it widely and give every person the ability to direct it," as [reported by Yahoo Finance](https://finance.yahoo.com/technology/article/metas-zuckerberg-reveals-ai-plans-in-lengthy-manifesto-derides-rivals-for-concentrating-power-152245348.html). In an interview, he added he was surprised the discourse from other labs is ["so filled with doom"](https://variety.com/2026/biz/news/meta-ai-manifesto-mark-zuckerberg-1236831435/).

[CNBC's coverage called it a swipe at OpenAI and Anthropic](https://www.cnbc.com/2026/08/10/meta-muse-glimmer-open-weight-ai.html), which is accurate in spirit but imprecise in letter: the essay criticizes only unnamed "other labs" that build "for companies, governments, or other institutions." The reception was not kind everywhere. [TechCrunch's same-day response](https://techcrunch.com/2026/08/10/mark-zuckerbergs-ai-manifesto-is-exactly-why-people-dont-like-ai/) argued the essay leans on hazy generalities about empowerment while demonstrating, paragraph by paragraph, why the public stopped trusting tech executives to deliver it. Critics also noted the awkward fit between "AI frees your time" rhetoric and Meta's own internal messaging discouraging staff from asking whether AI productivity gains might mean more time off.

There is a fair way to score this: the argument for distributing capability widely is serious, and open weights genuinely do transfer power to people who could never pay for frontier APIs. It is also, simultaneously, the argument that best fits Meta's business — a company that monetizes attention, not model access, loses little by giving weights away and gains an ecosystem. Both things are true at once.

## The India angle

Nothing in the release is India-specific — the weights are a geography-agnostic download, and Indian coverage on launch day mirrored the global story. But India is one of the clearest test markets for the open-weights argument, in both directions.

The government's sovereign-AI program is itself a bet on open weights. [Sarvam AI released its 30B and 105B models under Apache 2.0](https://www.sarvam.ai/blogs/sarvam-30b-105b) this year, trained from scratch on subsidized compute from the [roughly ₹10,372-crore IndiaAI Mission](https://techcrunch.com/2026/02/18/indian-ai-lab-sarvams-new-models-are-a-major-bet-on-the-viability-of-open-source-ai/), which has [empanelled more than 38,000 GPUs](https://www.tribuneindia.com/news/business/india-to-deploy-38000-gpus-set-up-600-data-labs-to-strengthen-ai-ecosystem-meity) against an original target of 10,000. The cautionary case sits next to it: [Ola's Krutrim paused its foundation-model and chip work in May](https://www.medianama.com/2026/05/223-krutrim-ai-cloud-chip-ai-model-work/) to pivot toward cloud infrastructure — training your own base model is brutally expensive, which is exactly why free, commercially usable weights like Glimmer's find eager takers here. Meta knows this: its [enterprise joint venture with Reliance](https://about.fb.com/news/2025/08/accelerating-indias-ai-adoption-a-strategic-partnership-with-reliance-industries-to-build-llama-based-enterprise-ai-solutions/) was built on Llama's open models, and India was already [Meta AI's largest usage market back in 2024](https://techcrunch.com/2024/07/31/india-is-the-largest-market-for-meta-ai-usage).

Two practical notes temper the enthusiasm. First, hardware: the 4-bit build targets a 24 GB GPU, and [Indian retail listings put RTX 4090-class cards at roughly ₹1.7 lakh and up](https://www.primeabgb.com/buy-online-price-india/geforce-rtx-4090-graphic-card/) — local AI is cheap to license and expensive to host, which is why India's developer adoption may run through rented cloud GPUs first. Second, language: Meta says Glimmer trained on more than 100 languages but publishes no Indic-language support list or benchmark — a gap worth noticing when Sarvam's models ship with a tokenizer built for 22 scheduled Indian languages. For Indian builders, Glimmer is a strong new option for agentic English-first workloads, not yet a proven one for Indic-language products.

## What to watch

Whether Muse Spark 1.2's weights actually arrive "in the coming weeks," and under what license — that is the difference between a strategic return to open AI and a one-off distilled goodwill drop. Whether independent evaluations confirm Meta's agent-benchmark wins and how far the hallucination number moves under real testing. Whether Alibaba's promised Qwen3.8-27B, due imminently, resets the size class again. And the adoption scoreboard: [OpenRouter's data shows open-weight models at 29% of routed tokens but under 4% of spend](https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026/) as of June — open models are winning volume while closed models keep the revenue, which is precisely the split Meta's business can live with and its rivals cannot. The [rest of our AI models coverage](/topics/ai-models/) tracks each of these threads as they move.

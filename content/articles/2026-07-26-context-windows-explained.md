---
title: "Context Windows Explained: What the Token Number Means"
slug: "context-windows-explained"
date: 2026-07-26
hub: explainers
tags: [context window, tokens, llm, benchmarks, rag]
description: "What a context window really is, why a million-token label rarely means a million usable tokens, and the cost math behind long prompts — with sources."
hero_alt: "Illustration of a long scroll of text being fed into a language model with only portions highlighted as reliably attended"
keyword: "context window explained"
original_value: "SEO explainers report the advertised ceiling as the story. This piece cites the effective-context evidence by name — RULER, NoLiMa, Chroma's Context Rot, Fiction.liveBench — runs live cost math (8k vs 200k input is ~18x on current GPT-5.5 prices), and covers why vendors resize windows at all."
selection_note: "Owner-directed explainers batch (2026-07-26); demand+gap validated in 02-research/research-explainer-factbases-2026-07-26.md."
sources:
  - {title: "What are tokens and how to count them — OpenAI Help", url: "https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them", primary: true}
  - {title: "GPT-5.5 model page (context and pricing) — OpenAI API docs", url: "https://developers.openai.com/api/docs/models/gpt-5.5", primary: true}
  - {title: "Claude models and pricing — Anthropic docs", url: "https://platform.claude.com/docs/en/about-claude/pricing", primary: true}
  - {title: "RULER: What's the Real Context Size of Your Long-Context Language Models? (NVIDIA)", url: "https://arxiv.org/abs/2404.06654", primary: true}
  - {title: "NoLiMa: Long-Context Evaluation Beyond Literal Matching (Adobe Research)", url: "https://arxiv.org/abs/2502.05167", primary: true}
  - {title: "Context Rot: How Increasing Input Tokens Impacts LLM Performance — Chroma Research", url: "https://www.trychroma.com/research/context-rot", primary: true}
  - {title: "Lost in the Middle: How Language Models Use Long Contexts", url: "https://arxiv.org/abs/2307.03172", primary: true}
  - {title: "Context windows data insight — Epoch AI", url: "https://epoch.ai/data-insights/context-windows", primary: true}
  - {title: "Introducing Contextual Retrieval — Anthropic", url: "https://www.anthropic.com/news/contextual-retrieval", primary: true}
  - {title: "Llama 4 multimodal intelligence — Meta AI blog", url: "https://ai.meta.com/blog/llama-4-multimodal-intelligence/", primary: true}
faq:
  - {q: "How many words is 100,000 tokens?", a: "Roughly 75,000 English words, using OpenAI's rule of thumb that one token is about three-quarters of a word — around 300 book pages. Non-English and non-Latin scripts often consume noticeably more tokens per word because tokenizers are trained on English-heavy data."}
  - {q: "Does a bigger context window mean the AI has better memory?", a: "Not proportionally. Benchmarks that go beyond simple retrieval — RULER, NoLiMa, Chroma's Context Rot — consistently show accuracy degrading well before the advertised limit, sometimes by half at 32,000 tokens. The label is a ceiling, not a performance promise."}
  - {q: "What happens when I exceed the context limit?", a: "Raw API calls are typically rejected outright, while chat products quietly truncate or compress the oldest parts of the conversation — which is exactly why a long chat 'forgets' things you said early on."}
  - {q: "Should I paste a whole document in, or use retrieval?", a: "Anthropic's own guidance draws the line around 200,000 tokens — roughly 500 pages: below that, pasting everything with prompt caching is reasonable; above it, retrieval wins. Even below the line, focused context is cheaper and often more accurate than a stuffed prompt."}
review:
  facts_verified: true
  sources_checked: true
  title_promise_check: true
  no_fabrication: true
  policy_pass: true
  reviewed_at: "2026-07-26T21:50:00+05:30"
---

A context window is the total amount of text — measured in tokens — that a model can consider at once, covering your prompt, the conversation so far, and the reply it is writing. One token is roughly three-quarters of an English word ([OpenAI Help](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)), so a "1M context" label suggests about 750,000 words of working memory. The number on the box is real, but three other facts matter more: models usually can't use the whole window reliably, long prompts cost real money, and vendors resize these limits — up and down — for economic reasons they rarely explain.

## The label, decoded

Advertised windows in July 2026 run from 200,000 tokens (Claude Haiku 4.5) through the million-token class — GPT-5.5 lists 1,050,000 input tokens with 128,000 max output ([OpenAI API docs](https://developers.openai.com/api/docs/models/gpt-5.5)); Claude's current Opus, Sonnet and Fable models list 1,000,000 ([Anthropic docs](https://platform.claude.com/docs/en/about-claude/pricing)) — up to Meta's Llama 4 Scout, which advertises 10 million tokens while its own announcement notes the model was trained at 256,000-token lengths and extrapolated beyond ([Meta AI](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)). That gap between trained length and marketed length is the theme of this entire subject. Epoch AI's dataset across 123 models puts the marketing pace bluntly: advertised maximum context has grown roughly 30-fold per year since mid-2023 ([Epoch AI](https://epoch.ai/data-insights/context-windows)).

One accounting note: whether "context" includes the model's output varies by vendor page, and the same company sometimes lists it both ways across model cards — architecturally, prompt and response share one budget, so read the specific model's card rather than assuming.

## Advertised versus usable: what the benchmarks show

The famous "needle in a haystack" demo — hide one sentence in a long document, ask for it back — is the easy case, and modern models ace it. Harder, more realistic tests tell a different story. NVIDIA's RULER benchmark found that of 17 models advertising 32,000 tokens or more, only about half held up at even 32,000 when tasks required tracking and aggregating information ([RULER](https://arxiv.org/abs/2404.06654)). Adobe's NoLiMa removed word-overlap cues so the model must reason rather than pattern-match: ten of twelve models fell to half their short-context accuracy by 32,000 tokens — GPT-4o slid from 99.3% to 69.7% ([NoLiMa](https://arxiv.org/abs/2502.05167)). Chroma's 2025 "Context Rot" study across 18 models showed performance degrading non-uniformly as input grows even on trivially simple tasks ([Chroma Research](https://www.trychroma.com/research/context-rot)), and the foundational "Lost in the Middle" result — models attend best to the start and end of a prompt, worst to the middle — still replicates in newer work ([Liu et al.](https://arxiv.org/abs/2307.03172)). Progress is genuine: Epoch AI measured the input length at which top models keep 80% accuracy rising over 250-fold in nine months — yet at that mid-2025 snapshot, the best model cleared the bar only at 8,000 tokens. The practical translation: treat the advertised number as a hard ceiling and assume reliable performance at some fraction of it, especially for reasoning over scattered facts.

## Why the number keeps changing

Long context is expensive to serve. Every generated token attends to everything before it, and the memory holding that state — the KV cache — grows with length; for a 70-billion-parameter model it can reach tens of gigabytes per long session, which is GPU memory no one else can use. That economics shows up in pricing: GPT-5.5 charges a long-context surcharge beyond 272,000 input tokens, Google's Pro-tier pricing steps up past 200,000 tokens, while Anthropic currently prices its 1M window flat — proof the surcharge is a choice, not physics ([OpenAI API docs](https://developers.openai.com/api/docs/models/gpt-5.5); [Anthropic docs](https://platform.claude.com/docs/en/about-claude/pricing)). It also shows up as quiet product changes: earlier this month we reported [Codex's advertised context being halved](/articles/codex-context-window-cut/) with no changelog entry — the clearest recent case of a limit moving downward under load economics, consistent with the token-budget "compaction" machinery visible in that product's release notes. Serving costs ultimately trace back to hardware and electricity, a chain we unpacked in [the real cost of running AI](/articles/real-cost-of-running-ai/).

Even when the window is huge and the price acceptable, stuffing it has its own bill. On GPT-5.5's current rates ([OpenAI API docs](https://developers.openai.com/api/docs/models/gpt-5.5)), the same question asked over an 8,000-token excerpt versus a 200,000-token dump costs about $0.055 versus $1.015 — roughly 18 times more — before any surcharge kicks in, purely from input scaling. Multiply by a team's daily usage and "just paste everything" becomes a line item.

## What it means for your prompts and your bill

Put the material that matters at the start or end of a long prompt, never buried in the middle — that single habit tracks directly with the Lost-in-the-Middle evidence. For document work, follow the line Anthropic itself draws: under roughly 200,000 tokens (about 500 pages), including everything with prompt caching is defensible; beyond it, retrieval — fetching only relevant chunks — is both cheaper and more accurate, and their measured retrieval setup cut failure rates by 49% over naive approaches ([Anthropic](https://www.anthropic.com/news/contextual-retrieval)). When a chat assistant "forgets" your instructions from an hour ago, that's overflow management, not attitude: products truncate or compress old turns rather than refuse. And when comparing models — including [the free tiers we compared](/articles/free-ai-tiers-compared/), where Gemini's free window is 32,000 tokens against Claude's 200,000 — weigh the usable window, the price curve and the reset limits together, because a giant number you can't afford to fill, or that decays past 32k, is a spec-sheet victory only.

Context windows are the rare AI spec that is simultaneously real, oversold and unstable. Read the number, then ask the three questions that matter: how much of it holds up under load, what does filling it cost, and how quietly can it change. For more evidence-first guides, browse our [how-to and explainers](/topics/explainers/) hub.

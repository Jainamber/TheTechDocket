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
selection_note: "Owner-directed explainers batch (2026-07-26); demand+gap validated in 02-research/research-explainer-factbases-2026-07-26.md. Rewritten same day in plain language on owner feedback."
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
  reviewed_at: "2026-07-27T01:15:00+05:30"
---

A context window is simply how much text an AI model can "hold on its desk" at one time — your question, the conversation so far, any pasted documents, and the answer it's writing, all counted together in tokens (a token is about three-quarters of an English word, per [OpenAI's own rule of thumb](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)). Three things about that desk matter more than its advertised size: the model doesn't use the whole desk equally well, a bigger desk costs real money to use, and companies quietly change desk sizes for business reasons.

## Tokens, translated

| Tokens | Roughly… |
|---|---|
| 1,000 | 750 words — a long email |
| 32,000 | ~80 pages — a thesis chapter |
| 200,000 | ~500 pages — a full novel |
| 1,000,000 | ~2,500 pages — an encyclopedia volume |

Today's advertised windows sit at the big end: GPT-5.5 lists just over a million input tokens ([OpenAI API docs](https://developers.openai.com/api/docs/models/gpt-5.5)), Claude's current models list a million ([Anthropic docs](https://platform.claude.com/docs/en/about-claude/pricing)), and Meta's Llama 4 Scout advertises ten million — while Meta's own announcement notes it was *trained* at 256,000 and stretched from there ([Meta AI](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)). Keep that trained-versus-marketed gap in mind; it's the whole story in miniature. Across 123 models, the advertised maximum has grown about 30-fold per year since 2023 ([Epoch AI](https://epoch.ai/data-insights/context-windows)).

One caveat for Indian readers: the word-count rules of thumb above are for English. Tokenizers — the software that chops text into tokens — are trained mostly on English, so Hindi, Tamil, Bengali and other non-Latin scripts typically get split into more pieces per word. The same letter or document costs more tokens, which means it fills the window faster and costs more to process. No vendor publishes a reliable per-language multiplier, so we won't invent one — just budget extra headroom when working in Indian languages.

## The number on the box vs the number that works

Here's the part the spec sheets skip: **models get worse as the desk fills up.** The evidence, by name:

- **RULER** (NVIDIA): of 17 models claiming 32k+ contexts, only about half performed acceptably *at* 32k on realistic tasks ([RULER](https://arxiv.org/abs/2404.06654)).
- **NoLiMa** (Adobe): when the test removes word-matching shortcuts, 10 of 12 models lost half their accuracy by 32k tokens — GPT-4o fell from 99.3% to 69.7% ([NoLiMa](https://arxiv.org/abs/2502.05167)).
- **Context Rot** (Chroma): performance degrades as input grows even on absurdly simple tasks, across 18 models ([Chroma Research](https://www.trychroma.com/research/context-rot)).
- **Lost in the Middle**: models remember the start and end of a prompt best, and the middle worst ([Liu et al.](https://arxiv.org/abs/2307.03172)).

Models are improving fast — the length at which top models stay above 80% accuracy grew over 250-fold in nine months ([Epoch AI](https://epoch.ai/data-insights/context-windows)) — but at that snapshot the best still only cleared the bar at 8,000 tokens. Rule of thumb: trust the advertised number as a hard limit, and expect *reliable* performance at some fraction of it.

## Why the limit keeps changing (follow the money)

Serving a long conversation forces the provider to keep a growing "memory scratchpad" for you on a GPU — for a big model, tens of gigabytes per long session. That cost shows up in two ways:

1. **Pricing steps.** GPT-5.5 charges extra beyond 272,000 input tokens; Google's Pro pricing steps up past 200,000; Anthropic currently prices its full million flat ([OpenAI API docs](https://developers.openai.com/api/docs/models/gpt-5.5); [Anthropic docs](https://platform.claude.com/docs/en/about-claude/pricing)). The surcharge is a choice, not physics.
2. **Quiet cuts.** Limits can shrink without an announcement — as we reported when [Codex's context was halved](/articles/codex-context-window-cut/) with nothing in the changelog. When serving costs bite, the desk gets smaller. The electricity and hardware behind all this is its own story: [the real cost of running AI](/articles/real-cost-of-running-ai/).

And filling a big window costs *you* too: the same question over an 8,000-token excerpt versus a 200,000-token dump runs about $0.055 versus $1.015 on current GPT-5.5 rates ([OpenAI API docs](https://developers.openai.com/api/docs/models/gpt-5.5)) — roughly 18 times more, before any surcharge.

## What it means for your prompts and your bill

Five habits that follow directly from the evidence:

1. **Put the important stuff first or last.** Never bury the key instruction in the middle of a long prompt.
2. **Paste less, not more.** A focused excerpt usually beats the full dump on both accuracy and cost.
3. **Use the 500-page rule.** Under ~200,000 tokens of material, pasting it all is defensible; beyond that, use retrieval — Anthropic's measured setup cut retrieval failures by 49% ([Anthropic](https://www.anthropic.com/news/contextual-retrieval)).
4. **Expect forgetting in long chats.** Products silently trim old turns when full. Re-state what matters.
5. **Compare usable windows, not label windows** — especially on free tiers, where [the gap between 32k and 200k](/articles/free-ai-tiers-compared/) is the difference between chunking a PDF and swallowing it whole.

The context window is the rare AI spec that's real, oversold and unstable all at once. Read the number, then ask: how much of it works, what does filling it cost, and how quietly can it shrink? More evidence-first guides on our [how-to and explainers](/topics/explainers/) hub.

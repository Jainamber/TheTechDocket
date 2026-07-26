---
title: "Free AI in 2026: ChatGPT, Gemini, Claude and Copilot Compared"
slug: "free-ai-tiers-compared"
date: 2026-07-26
hub: explainers
tags: [chatgpt, gemini, claude, copilot, free tier, pricing]
description: "What the free tiers of ChatGPT, Gemini, Claude and Copilot actually include in July 2026 — limits, context, training defaults, and India's ₹399 tiers."
hero_alt: "Four-column comparison chart of ChatGPT, Gemini, Claude and Copilot free tiers with locks on paywalled features"
keyword: "free ai chatbot comparison"
original_value: "Every claim here comes from an official vendor page accessed on 26 July 2026, with vendors' deliberately vague wording quoted rather than converted into invented numbers — plus the two things roundups skip: data-training defaults (opt-out vs opt-in) and India's ₹399 tiers."
selection_note: "Owner-directed explainers batch (2026-07-26); highest demand+gap score in topic validation, see 02-research/research-explainer-factbases-2026-07-26.md."
sources:
  - {title: "ChatGPT pricing — OpenAI", url: "https://chatgpt.com/pricing", primary: true}
  - {title: "What is ChatGPT Go — OpenAI Help", url: "https://help.openai.com/en/articles/11989085-what-is-chatgpt-go", primary: true}
  - {title: "Data Controls FAQ — OpenAI Help", url: "https://help.openai.com/en/articles/7730893-data-controls-faq", primary: true}
  - {title: "Gemini plans and features — Google support", url: "https://support.google.com/gemini/answer/16275805", primary: true}
  - {title: "Google AI Plus in India — Google India blog", url: "https://blog.google/intl/en-in/company-news/technology/do-more-with-ai-for-less-google-ai-plus-now-in-india/", primary: true}
  - {title: "Gemini Apps activity and data — Google support", url: "https://support.google.com/gemini/answer/13594961", primary: true}
  - {title: "Claude pricing — Anthropic", url: "https://claude.com/pricing", primary: true}
  - {title: "Is my data used for model training? — Anthropic privacy center", url: "https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training", primary: true}
  - {title: "Copilot Free vs Copilot in Microsoft 365 — Microsoft Support", url: "https://support.microsoft.com/en-us/topic/what-s-the-difference-between-microsoft-copilot-free-and-copilot-in-microsoft-365", primary: true}
faq:
  - {q: "Which free AI chatbot can handle the longest document?", a: "On stated numbers, Claude — its free tier lists the same 200,000-token context as Pro, roughly 500 pages, though the rolling five-hour usage cap limits how much you can do with it. Gemini's free tier is explicitly 32,000 tokens, and OpenAI and Microsoft publish no free-tier figure at all."}
  - {q: "Do free AI chatbots train on my conversations by default?", a: "ChatGPT and Gemini do unless you opt out — via Data Controls in ChatGPT and the Keep Activity setting in Gemini. Claude is the exception: training is off unless you switch on Model Improvement. Microsoft publishes no equivalent consumer disclosure on its comparison pages."}
  - {q: "What do the ₹399 plans in India actually buy?", a: "Both sit one notch above free: ChatGPT Go, which launched India-first in August 2025, raises message, upload and image limits over Free, while Google AI Plus, in India since December 2025, roughly doubles free limits and unlocks more Pro-model access — with an introductory half-price period for new Indian subscribers. Neither includes the full reasoning models or agent features of the twenty-dollar-class plans."}
  - {q: "Is there still a free Gemini or ChatGPT plan for students in India?", a: "Not as of July 2026. Google's free student offer for Gemini Pro ended on 11 March 2026, and no live nationwide student free tier from OpenAI or Microsoft was verifiable on official pages — treat student-offer listicles as stale until a vendor page says otherwise."}
review:
  facts_verified: true
  sources_checked: true
  title_promise_check: true
  no_fabrication: true
  policy_pass: true
  reviewed_at: "2026-07-26T21:35:00+05:30"
---

The four big free AI tiers are genuinely usable in mid-2026, but they differ in ways the marketing pages won't put side by side: only Google states a hard free context number — 32,000 tokens ([Google support](https://support.google.com/gemini/answer/16275805)) — only Anthropic leaves model training off by default, Microsoft publishes almost no numbers at all, and India, uniquely, gets two official ₹399 middle tiers that don't exist in most markets. Everything below comes from the vendors' own pages, accessed on 26 July 2026, with their vague wording quoted as-is; these limits shift often, so treat the date stamp as part of the data.

## What each free tier actually includes

**ChatGPT Free** currently gives "limited access to GPT-5.5 Instant," with "limited messages and uploads," "limited and slower image generation," "limited memory and context," and — notably — "limited deep research," which many people assume is paywalled ([OpenAI pricing](https://chatgpt.com/pricing)). No message count or token figure appears anywhere official.

**Gemini Free** names its models — Flash-Lite, Flash and capped access to Pro — and is the only one of the four to publish a hard context number: 32,000 tokens free versus 1 million on paid tiers. Google also concedes in writing that free prompts can be capped "within a specific timeframe" and that Deep Research "may be unavailable during periods of high demand" — an official admission of load-based throttling ([Google support](https://support.google.com/gemini/answer/16275805)). Free users get image generation and Gemini Live voice.

**Claude Free** lists a 200,000-token context — "same as Pro" — but never states a message count; usage resets on a rolling five-hour window and varies with message length and attachments ([Claude pricing](https://claude.com/pricing)). Voice mode is available on every plan including Free. There's no image generation on any Claude tier — the feature doesn't exist — and Research is a paid addition.

**Copilot Free** is the least documented: Microsoft's own comparison pages say "usage limits apply" and little else, reserving agents like Researcher and Analyst for paid plans ([Microsoft Support](https://support.microsoft.com/en-us/topic/what-s-the-difference-between-microsoft-copilot-free-and-copilot-in-microsoft-365)). The message caps that circulate online trace to press coverage and Wikipedia, not to any live Microsoft page — we could not verify them, so we won't repeat them as fact.

## The training-default split nobody prints

The single biggest hidden difference is what happens to your conversations. OpenAI trains on free-tier chats unless you turn off "Improve the model for everyone" under Data Controls ([OpenAI Help](https://help.openai.com/en/articles/7730893-data-controls-faq)). Google's Keep Activity setting governs whether chats improve its AI, with retained activity auto-deleting after 18 months by default ([Google support](https://support.google.com/gemini/answer/13594961)). Anthropic inverts the model: training is off across Free, Pro and Max unless you enable Model Improvement ([Anthropic privacy center](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training)). Microsoft's consumer pages state no equivalent default clearly. If the privacy default is your deciding factor, that asymmetry — opt-out at OpenAI and Google, opt-in at Anthropic — is the comparison, and it's worth pairing with our deeper guide to [what AI chatbots know about you](/articles/ai-chatbot-data-privacy/).

## Four everyday tasks, honestly scored

Summarizing a 100-page PDF in one pass — roughly 50,000–75,000 tokens — is plausible on Claude Free's 200k context, impossible in one shot on Gemini Free's 32k, and unknowable on ChatGPT and Copilot because neither states a figure. Generating a few images: Gemini and ChatGPT free tiers both can (ChatGPT "slower"), Claude can't at any price, Copilot's current allowance isn't officially stated. Voice conversation: free on Claude and Gemini; ChatGPT's help pages still describe free voice as capped daily on an older model — wording that looks stale against its GPT-5.5 branding, which is itself a lesson in how fast these pages drift. A multi-step research task: free-tier ChatGPT and Gemini both offer capped versions; Claude and Copilot hold research features behind payment.

Context size matters less than the number suggests, by the way — advertised windows and usable windows are different things, as our companion piece on [context windows](/articles/context-windows-explained/) shows with benchmark data.

## The ₹399 middle tier India actually got

India is the rare market with two official sub-$5 tiers. ChatGPT Go launched India-first in August 2025 — $8 in the US, widely reported at ₹399 in India — adding higher message, upload and image limits over Free, but explicitly not the full reasoning models, deep-research allowance or agent mode of Plus ([OpenAI Help](https://help.openai.com/en/articles/11989085-what-is-chatgpt-go)). Google AI Plus arrived in India on 10 December 2025 at ₹399 a month — ₹199 for the first six months for new subscribers — roughly doubling free limits and expanding Pro-model and Deep Research access ([Google India blog](https://blog.google/intl/en-in/company-news/technology/do-more-with-ai-for-less-google-ai-plus-now-in-india/)). Anthropic and Microsoft list no India-specific pricing at all, which is itself a useful signal of where each company sees its next hundred million users. One expiry worth flagging because listicles keep it alive: Google's free student Gemini offer ended on 11 March 2026.

## Our take: how to choose, and what to re-check

If your workload is long documents, start with Claude Free and watch the five-hour window. If you want images, live voice and a stated context number, Gemini Free is the most transparent deal. If you need occasional deep research without paying, ChatGPT Free and Gemini Free are the only games in town. If a vendor won't publish its limits — Microsoft, conspicuously — assume they can change under you without notice. And whatever you pick, spend your first minute in the data settings, not the prompt box: the defaults, not the model names, are where free tiers differ most. These numbers will drift — we'll refresh this page as the official pages change, and you can find more guides on our [how-to and explainers](/topics/explainers/) hub.

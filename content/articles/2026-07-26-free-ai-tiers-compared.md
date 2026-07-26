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
selection_note: "Owner-directed explainers batch (2026-07-26); highest demand+gap score in topic validation, see 02-research/research-explainer-factbases-2026-07-26.md. Rewritten same day in plain language on owner feedback."
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
  - {q: "Is there still a free Gemini or ChatGPT plan for students in India in 2026?", a: "Not as of July 2026. Google's free student offer for Gemini Pro ended on 11 March 2026, and no live nationwide student free tier from OpenAI or Microsoft was verifiable on official pages — treat student-offer listicles as stale until a vendor page says otherwise."}
review:
  facts_verified: true
  sources_checked: true
  title_promise_check: true
  no_fabrication: true
  policy_pass: true
  reviewed_at: "2026-07-27T01:05:00+05:30"
---

All four big AI chatbots are genuinely usable for free in mid-2026 — the real differences hide in three places the marketing never puts side by side: how much text each can handle at once, whether your chats train their models by default, and what India's special ₹399 tiers add. Every number below comes from the vendors' own pages, checked on 26 July 2026 ([Google support](https://support.google.com/gemini/answer/16275805)); where a vendor refuses to give a number, we say so instead of inventing one. These pages change often — the date is part of the data.

## The 30-second comparison

| | **ChatGPT Free** | **Gemini Free** | **Claude Free** | **Copilot Free** |
|---|---|---|---|---|
| Model you get | GPT-5.5 Instant, "limited" | Flash models + capped Pro | not stated | not stated |
| Message limits | "limited" — no number | can be capped at busy times | resets every 5 hours | "usage limits apply" |
| Memory per chat (context) | not stated | **32k tokens (~80 pages)** | **200k tokens (~500 pages)** | not stated |
| Images | yes, slower | yes | no (feature doesn't exist) | unclear |
| Voice | yes, capped | yes (Gemini Live) | yes, all plans | unclear |
| Deep research | yes, limited | yes, throttled when busy | no — paid only | no — paid only |
| **Trains on your chats by default?** | **yes** (opt-out) | **yes** (opt-out) | **no** (opt-in) | not disclosed |
| India budget tier | ChatGPT Go ₹399/mo | AI Plus ₹399/mo | none | none |

Sources for every row: [OpenAI pricing](https://chatgpt.com/pricing), [Google support](https://support.google.com/gemini/answer/16275805), [Claude pricing](https://claude.com/pricing), [Microsoft Support](https://support.microsoft.com/en-us/topic/what-s-the-difference-between-microsoft-copilot-free-and-copilot-in-microsoft-365).

## What "free" is hiding

Four catches, in plain words:

- **The limits are deliberately fuzzy.** Only Google publishes a hard context number. OpenAI says "limited," Anthropic says your allowance "will vary," Microsoft says "usage limits apply" — and any precise Copilot number you see online traces to old press coverage, not a live Microsoft page.
- **Free means last in the queue.** Google admits free Deep Research "may be unavailable during periods of high demand," and Anthropic sells Pro partly as "priority access" — meaning free users get throttled exactly when everyone's online.
- **The privacy default is the biggest hidden difference.** OpenAI and Google use your chats for training unless you switch it off ([OpenAI Data Controls](https://help.openai.com/en/articles/7730893-data-controls-faq); [Gemini activity settings](https://support.google.com/gemini/answer/13594961)). Anthropic doesn't unless you switch it on ([Anthropic privacy center](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training)). Full walkthrough of every toggle: [what chatbots keep about you](/articles/ai-chatbot-data-privacy/).
- **Student freebies expire quietly.** Google's free student offer ended on 11 March 2026 — but "free AI for students" listicles will keep recommending it for months.
- **New features skip Free selectively.** OpenAI's July 2026 release notes show the pattern in one place: the "ChatGPT Work" launch went to every paid plan *except* Free and Go, while the same month's search and dictation upgrades went to everyone ([OpenAI release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)). Free tiers get the upgrades that make the product stickier, not the ones that make it more powerful.

## Which one for your task?

- **Long documents** (contracts, reports, theses): **Claude** — its free 200k context is the only one that can plausibly swallow a 100-page PDF whole. Why the fine print still matters: see our [context windows explainer](/articles/context-windows-explained/).
- **Images + voice + a stated context number:** **Gemini** — the most transparent free package.
- **Occasional research tasks without paying:** **ChatGPT or Gemini** — the only two with free deep research.
- **Inside Word/Excel:** **Copilot** — but know it publishes the least about what you're getting.

## India's ₹399 shortcut

India is the rare market with two official middle tiers between free and the $20 plans. **ChatGPT Go** launched India-first in August 2025 — more messages, uploads and images than Free, but not the full reasoning models or agents ([OpenAI Help](https://help.openai.com/en/articles/11989085-what-is-chatgpt-go)). **Google AI Plus** arrived on 10 December 2025 at ₹399 a month — ₹199 for the first six months — roughly doubling free limits with more Pro access ([Google India blog](https://blog.google/intl/en-in/company-news/technology/do-more-with-ai-for-less-google-ai-plus-now-in-india/)). Anthropic and Microsoft offer no India pricing at all — a telling gap.

## Our take: how to choose, and what to re-check

Spend your first minute in the settings, not the chat box — the training default matters more than the model name. Match the tool to the task using the list above rather than picking one "best" app; they're free, so use two. And re-check the table's facts if you're reading this months from now: free-tier terms are the most frequently, quietly edited pages in AI. We'll refresh this piece as they move.

**How to re-check any of this yourself, in two minutes.** Go straight to the vendor's own pricing page and help center — the four we used are listed in the sources below — and ignore third-party roundups entirely; even our own research pass caught a cached copy of an official page still describing a years-old free tier, which is exactly how stale numbers spread. If a limit isn't stated on an official page, treat it as "can change any time without notice," because it can and does. That single habit — primary page, check the date, distrust anything precise that the vendor itself won't say — will keep you ahead of ninety percent of the comparison articles on this topic. More guides on our [how-to and explainers](/topics/explainers/) hub.

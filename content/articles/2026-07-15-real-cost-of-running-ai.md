---
title: "The Real Cost of Running AI: Tokens, GPUs, Power"
slug: "real-cost-of-running-ai"
date: 2026-07-15
updated: 2026-07-19
update_note: "Relaunched at thetechdocket.com; added an in-body link to the Chips & Hardware hub."
hub: hardware
tags: [gpus, ai costs, tokens, data centers]
description: "OpenAI, Google and Anthropic's live per-token prices, GPU purchase and rental costs, and IEA electricity data, lined up to show what AI really costs to run."
hero_alt: "A data center aisle of GPU servers with a rising electricity meter and dollar-per-token price tags overlaid on the racks"
keyword: "cost of running ai"
original_value: "This piece lines up live per-token prices from OpenAI, Google and Anthropic against real GPU purchase and rental costs, IEA electricity data, and India's subsidized compute program in one comparable, fully sourced framework."
sources:
  - {title: "OpenAI API Pricing", url: "https://developers.openai.com/api/docs/pricing", primary: true}
  - {title: "Gemini Developer API Pricing — Google AI for Developers", url: "https://ai.google.dev/gemini-api/docs/pricing", primary: true}
  - {title: "Claude Platform Pricing — Anthropic", url: "https://platform.claude.com/docs/en/about-claude/pricing", primary: true}
  - {title: "GPU Cloud Pricing — Lambda", url: "https://lambda.ai/pricing", primary: true}
  - {title: "Energy and AI: Executive Summary — IEA", url: "https://www.iea.org/reports/energy-and-ai/executive-summary", primary: true}
  - {title: "Measuring the Environmental Impact of AI Inference — Google Cloud Blog", url: "https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference", primary: true}
  - {title: "IndiaAI Mission Expands AI Ecosystem with Affordable Compute and Startup Support — PIB, Government of India", url: "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2245069&reg=3&lang=1", primary: true}
  - {title: "The cost of running a top-tier AI query dropped 280-fold — Silicon Canals, citing Stanford's AI Index Report", url: "https://siliconcanals.com/the-cost-of-running-a-top-tier-ai-query-dropped-280-fold-in-roughly-18-months-from-20-per-million-tokens-in-late-2022-to-seven-cents-by-late-2024-a-price-collapse-with-no-real-parallel-in/"}
faq:
  - {q: "What is a token in AI pricing, and why does it matter?", a: "A token is the small chunk of text an AI model reads or writes, roughly three quarters of a word in English. Providers charge separately for the input tokens you send and the output tokens the model generates, and pricing differs enough between models that the same conversation can cost very different amounts depending on which model answers it."}
  - {q: "Why is AI output priced higher than input per token?", a: "Generating new text token by token, a process called inference, takes more computation on the provider's chips than simply reading a prompt, since each new word depends on everything generated before it. That extra computation is why output pricing across major providers runs several times higher than input pricing on the same model."}
  - {q: "Is running AI models actually getting cheaper?", a: "For a fixed level of quality, yes: independent researchers have tracked steep drops in the price of matching older flagship performance, driven by competition between providers and more efficient chips and software. Overall spending is still climbing for many companies, though, because usage and model sizes are growing faster than per-unit prices are falling."}
  - {q: "How much electricity does one AI query actually use?", a: "A single typical text prompt uses a small fraction of a watt hour of electricity, according to one major provider's own published accounting, roughly comparable to running a television for well under a minute. Multiplied across huge daily prompt volumes worldwide, though, that usage adds up to enough electricity to show up in national energy statistics, which is why data centers now draw scrutiny from grid planners."}
review:
  facts_verified: true
  sources_checked: true
  title_promise_check: true
  no_fabrication: true
  policy_pass: true
  reviewed_at: "2026-07-15T16:30:00+05:30"
---

Running a large language model costs money in three separate places, and most explanations only cover one. There is the per-token price an API charges every time a prompt goes in and an answer comes out; the graphics processing units, or GPUs, that must be bought or rented to do the underlying math; and the electricity that keeps those chips running around the clock. Put together, these three layers explain why a "free" chatbot reply is never actually free — someone, somewhere, is paying for the tokens, the silicon, and the power that produced it.

## What a token actually costs

A token is the basic unit AI providers bill for: roughly three-quarters of an English word, so a short sentence like this one runs about a dozen tokens. Every API call is billed twice — once for the tokens you send in (the prompt, plus any attached documents or chat history) and again, usually at a much higher rate, for the tokens the model writes back. Generating that reply is called inference; building the model in the first place, a far more expensive one-time process, is called training.

Prices differ enormously by model tier and change often, so treat any figure here as a snapshot rather than a constant. As of July 2026, this is what the three largest API providers charge per 1M tokens, on their own official pricing pages:

| Model | Input ($ per 1M tokens) | Output ($ per 1M tokens) |
|---|---|---|
| OpenAI GPT-5.6 Sol (flagship) | $2.50 | $15.00 |
| OpenAI GPT-5.4 Nano (smallest) | $0.10 | $0.625 |
| Google Gemini 3.1 Pro (up to 200k context) | $2.00 | $12.00 |
| Google Gemini 2.5 Flash-Lite | $0.10 | $0.40 |
| Anthropic Claude Opus 4.8 | $5.00 | $25.00 |
| Anthropic Claude Haiku 4.5 | $1.00 | $5.00 |

Sourced from [OpenAI's pricing page](https://developers.openai.com/api/docs/pricing), [Google's Gemini API pricing page](https://ai.google.dev/gemini-api/docs/pricing), and [Anthropic's Claude pricing page](https://platform.claude.com/docs/en/about-claude/pricing). Anthropic is also running introductory pricing of $2 input and $10 output per 1M tokens on its newest Sonnet 5 model through the end of August 2026, reverting to a standard $3/$15 afterward — a reminder that even official rate cards carry expiry dates.

Both Google and Anthropic also sell batch processing — queuing a request instead of demanding an instant reply — at roughly half the standard price, and OpenAI offers a comparable discounted asynchronous tier, according to [the same official pricing pages](https://ai.google.dev/gemini-api/docs/pricing). That gap alone can make overnight or non-urgent workloads dramatically cheaper than live chat traffic.

## The hardware bill: buying or renting GPUs

Behind every API call sits a graphics processing unit — a chip originally built for video games, repurposed because it handles the parallel arithmetic neural networks need. Two figures matter here: what the chip costs, and how much power it draws at full load, known as its thermal design power, or TDP — the wattage the chip is engineered to dissipate as heat while running flat out.

### Buying: still expensive at the high end

Nvidia's H100, the workhorse chip of the last few training cycles, lists for roughly [$25,000 to $40,000 per unit](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide) depending on configuration and vendor discount, with an eight-GPU server running about $216,000 in bulk. Its TDP runs close to 700 watts per chip, before counting the cooling and networking that surround it in a data center rack. The newer H200 costs $31,000 to $32,000 per chip, with a full eight-GPU DGX system — including the surrounding CPUs, chassis, and networking — reaching $400,000 to $500,000, per the same industry pricing guide.

### Renting: cheaper, but it adds up

Buying hardware only makes sense at scale, which is why most startups rent GPU time by the hour instead. [Lambda](https://lambda.ai/pricing), a large GPU cloud provider, lists on-demand H100 instances at $3.99 an hour and its newer B200 chips at $6.69 an hour. Rates vary widely elsewhere: a 2026 comparison of cloud vendors found H100 rental rates from $1.49 an hour on Vast.ai to $6.98 an hour on Microsoft Azure, with AWS and Google Cloud priced in between, according to [IntuitionLabs' cloud GPU price comparison](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison). Renting one H100 around the clock for a month at Lambda's on-demand rate works out to roughly $2,870 — before storage, networking, or the engineers needed to keep it busy.

## Electricity: the meter that never stops

Every GPU-hour shows up on an electricity bill, and multiplied across the industry, that bill is now large enough to appear in national energy statistics. The [International Energy Agency](https://www.iea.org/reports/energy-and-ai/executive-summary) estimates data centers consumed about 415 terawatt-hours of electricity in 2024 — around 1.5% of global electricity use — with demand growing roughly 12% a year since 2017, more than four times faster than overall electricity consumption. The agency projects data center demand will reach roughly 945 terawatt-hours by 2030, comparable to Japan's entire current electricity use, with the United States alone driving nearly half of that increase.

Individual queries look tiny by comparison. Google reports that the median Gemini text prompt now uses about 0.24 watt-hours of electricity under its full accounting — equivalent to running a television for under nine seconds — and that this figure fell 33-fold over the twelve months to May 2025 as models and chips grew more efficient, according to [Google's own environmental accounting of AI inference](https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference). Multiply that small number across the enormous volume of daily prompts worldwide, though, and the aggregate is exactly what shows up in the IEA's terawatt-hour figures above.

## Why inference costs are falling — and where they aren't

By one widely cited measure, the cost of querying a model at a fixed quality bar — matching GPT-3.5's score on the MMLU benchmark, the model that powered ChatGPT's original 2022 launch — fell 280-fold in about two years: from $20 per 1M tokens in November 2022 to $0.07 per 1M tokens by October 2024, according to Stanford's 2025 AI Index Report, which drew on data from Epoch AI and Artificial Analysis, as [reported by Silicon Canals](https://siliconcanals.com/the-cost-of-running-a-top-tier-ai-query-dropped-280-fold-in-roughly-18-months-from-20-per-million-tokens-in-late-2022-to-seven-cents-by-late-2024-a-price-collapse-with-no-real-parallel-in/). Three forces drive that curve: competition among OpenAI, Google, Anthropic, and Chinese labs pushes prices toward cost; more efficient architectures and quantization squeeze more answers out of the same chip; and smaller distilled models now handle tasks that once needed a flagship model.

That last trend is why a wave of compact, on-device models has emerged — small enough to run offline on a phone rather than in a data center. PrismML's [Bonsai 27B compressed on-device model](/articles/bonsai-27b-ai-model-phone/) is one example: pushing inference onto the device itself eliminates the per-token bill and the data-center electricity draw at once, shifting the cost to a chip the user already owns.

Costs are not falling everywhere, though. Frontier "reasoning" models that work through multiple steps before answering — the category Opus 4.8 and Gemini 3.1 Pro belong to — carry a premium because they generate far more output tokens per answer than older chat models did, which can offset the per-token price drops entirely. Training the next frontier model also keeps getting more expensive even as serving a finished one gets cheaper, since labs are racing to build larger systems faster than they can learn to shrink them.

None of this makes inference free, which matters for how "free" AI products actually work. Every message sent to a no-cost chatbot still consumes real tokens, GPU-hours, and electricity somewhere — one reason free tiers quietly monetize conversations in other ways, whether through advertising, model training, or data sharing, as [our explainer on what chatbots do with user data](/articles/ai-chatbot-data-privacy/) lays out. Cheaper inference has a parallel effect on media, too: generating a synthetic image or short clip now costs a fraction of what it did three years ago, part of why so much AI-generated content circulates online — and why [learning to spot AI-generated images and videos](/articles/spot-ai-generated-images-videos/) has become an everyday skill rather than a niche one.

## The India angle

For Indian startups, the arithmetic above carries two extra layers: import costs and the rupee. Nvidia does not manufacture GPUs in India, so H100s and H200s arrive priced in dollars before customs and logistics are added on top — at [₹96.3 to the dollar](https://www.xe.com/en-us/currencyconverter/convert/?Amount=1&From=USD&To=INR) in mid-July 2026, even the lower end of that $25,000 H100 price band already works out to roughly ₹24 lakh before any markup.

That is why the government's own compute program matters so much locally. The IndiaAI Mission, backed by a ₹10,372 crore outlay, has onboarded more than 38,000 GPUs — including H100s, H200s, and older A100s — through empanelled providers such as E2E Networks, NxtGen, and Yotta Data Services, offering access that mission materials describe as up to 40% below market cost, according to the [Press Information Bureau's mission update](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2245069&reg=3&lang=1) and [IndiaAI's own compute capacity page](https://indiaai.gov.in/hub/indiaai-compute-capacity).

Subsidized local compute changes the build-versus-rent calculus for training or fine-tuning smaller models inside India. It does less for the token bill, though: calls to GPT-5.6, Gemini 3.1, or Claude are still billed in dollars by providers based in the US, so a founder's per-token cost rises and falls with the rupee no matter how cheap domestic GPUs get. That is one more reason on-device and smaller open-weight models matter disproportionately for cost-sensitive Indian products — every prompt handled locally is one that never touches a dollar-denominated bill. The silicon side of that equation — GPUs, memory prices, and the supply chains behind them — is what we follow day to day in [chips and hardware](/topics/hardware/).

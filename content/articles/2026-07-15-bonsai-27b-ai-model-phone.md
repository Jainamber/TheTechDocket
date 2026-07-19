---
title: "Bonsai 27B: The 27B AI Model That Runs on a Phone, Explained"
slug: "bonsai-27b-ai-model-phone"
date: 2026-07-15
updated: 2026-07-19
update_note: "Relaunched at thetechdocket.com; added an in-body link to the AI Models hub."
hub: ai-models
tags: [on-device AI, small models, quantization, PrismML, Qwen]
description: "PrismML's Bonsai 27B squeezes a 27B-parameter AI model into 3.9 GB to run on flagship phones. What's verified, what's hype, and which phones in India can run it."
hero_alt: "Stylized graphic card reading Bonsai 27B, a 27-billion-parameter AI model compressed to run on a smartphone"
keyword: "bonsai 27b"
original_value: "Synthesizes verified specs, conflicting benchmark numbers and community pushback into one assessment, and adds the India angle no outlet covered: which phones sold in India can actually run it."
sources:
  - {title: "PrismML — Bonsai 27B announcement", url: "https://prismml.com/news/bonsai-27b", primary: true}
  - {title: "PrismML — Bonsai 27B technical documentation", url: "https://docs.prismml.com/models/bonsai-27b", primary: true}
  - {title: "Hugging Face — Bonsai 27B model collection", url: "https://huggingface.co/collections/prism-ml/bonsai-27b", primary: true}
  - {title: "MarkTechPost — technical breakdown of the 1-bit and ternary builds", url: "https://www.marktechpost.com/2026/07/14/prismml-releases-bonsai-27b-1-bit-and-ternary-builds-of-qwen3-6-27b-that-run-on-laptops-and-phones/"}
  - {title: "AppleInsider — PrismML confirms talks with Apple (via CNBC)", url: "https://appleinsider.com/articles/26/07/14/prismml-confirms-it-is-in-talks-with-apple-about-ai-model-shrinking-tech"}
  - {title: "9to5Mac — release coverage and Apple-talks skepticism", url: "https://9to5mac.com/2026/07/14/prismml-releases-bonsai-27b-claiming-first-major-ai-model-of-its-size-fit-for-iphone/"}
  - {title: "OfficeChai — benchmark drops and demo caveat", url: "https://officechai.com/ai/prismml-announces-bonsai27b-the-first-27-billion-parameter-model-that-can-run-on-an-iphone/"}
  - {title: "Hacker News — community discussion", url: "https://news.ycombinator.com/item?id=48910545"}
faq:
  - {q: "Can my phone run Bonsai 27B?", a: "Realistically, only recent flagships. PrismML's own guidance points to phones with about 12 GB of RAM, which leave roughly 6 GB free for apps. Most budget and mid-range phones ship with 4 to 6 GB of RAM, which is not enough for the full model."}
  - {q: "Is Bonsai 27B free to use?", a: "Yes. The weights are released under the permissive Apache 2.0 license and can be downloaded from Hugging Face. PrismML also launched an iOS app called Locally AI and a limited free developer preview of its API."}
  - {q: "Is the 1-bit version as good as the original model?", a: "No. By PrismML's own numbers it retains roughly nine-tenths of the full-precision model's benchmark performance, and independent commenters flagged larger drops on tool-calling and multi-step agent tasks. The ternary version gives up less quality for a larger download."}
  - {q: "Does on-device AI keep my data private?", a: "Largely yes for the model itself: prompts, photos and documents processed on the phone never leave it. You still need to trust the app around the model, since apps can sync data for other reasons."}
review:
  facts_verified: true
  sources_checked: true
  title_promise_check: true
  no_fabrication: true
  policy_pass: true
  reviewed_at: "2026-07-15T13:20:00+05:30"
---

A 27-billion-parameter AI model on a phone was, until this week, a contradiction in terms — models of that class normally need a workstation GPU. On July 14, Pasadena startup PrismML [released Bonsai 27B](https://prismml.com/news/bonsai-27b), an open-weight compression of Alibaba's Qwen3.6-27B that shrinks the model to as little as 3.9 GB, small enough to load on a flagship smartphone. The release is real and downloadable today, but the headline carries fine print: you need a high-end phone, quality drops on some tasks, and the most-shared demo wasn't fully live. Here is what actually happened, and what it means if you're reading this in India.

## What PrismML actually released

Bonsai 27B is not a new model trained from scratch. PrismML's own [technical documentation](https://docs.prismml.com/models/bonsai-27b) is explicit that it is "a low-bit representation of Qwen3.6-27B, not a new pretrain" — the architecture, a dense hybrid-attention design from Alibaba's Qwen family, is unchanged. What PrismML built is an extreme compression of it, in two flavors, both released under the Apache 2.0 open-source license on [Hugging Face](https://huggingface.co/collections/prism-ml/bonsai-27b):

- A **1-bit ("binary") variant**, where every weight is either −1 or +1, working out to about 1.125 effective bits per weight and a 3.9 GB download, per [PrismML's announcement](https://prismml.com/news/bonsai-27b).
- A **ternary variant**, where weights can be −1, 0 or +1 (about 1.71 effective bits per weight), at roughly 5.9 GB with noticeably better quality retention.

For scale: the same model in its native FP16 precision weighs about 54 GB, and even a conventional 4-bit quantization runs to roughly 18 GB, according to [PrismML's release notes](https://prismml.com/news/prismml-releases-bonsai-27b) — so the 1-bit build is about 14 times smaller than the original.

The model keeps Qwen3.6's multimodal abilities (text plus image input), tool calling, a reasoning mode, and an unusually large 262K-token context window, and runs on llama.cpp, Apple's MLX, CUDA and even, PrismML claims, inside a browser via WebGPU, per the [docs](https://docs.prismml.com/models/bonsai-27b).

## How 27 billion parameters fit into 3.9 GB

The interesting part is not that quantization exists — hobbyists have squeezed models for years — but how the quality survives it. Squeezing 27 billion parameters into a few gigabytes normally wrecks a model, because rounding every weight to one of two values destroys information the model needs, as coverage at [MarkTechPost](https://www.marktechpost.com/2026/07/14/prismml-releases-bonsai-27b-1-bit-and-ternary-builds-of-qwen3-6-27b-that-run-on-laptops-and-phones/) explains.

PrismML's answer is **quantization-aware training (QAT)**: instead of compressing the finished model after the fact, the low-bit constraint is enforced during training itself, so the network learns to be accurate *within* the 1-bit or ternary format. Weights are grouped (one shared FP16 scale per 128 weights), the vision tower is kept at 4-bit, and a custom speculative-decoding scheme the company calls DSpark adds a claimed 1.37× decoding speedup on server GPUs, per the same [MarkTechPost breakdown](https://www.marktechpost.com/2026/07/14/prismml-releases-bonsai-27b-1-bit-and-ternary-builds-of-qwen3-6-27b-that-run-on-laptops-and-phones/).

One nuance the headlines skip, flagged in [MarkTechPost's analysis](https://www.marktechpost.com/2026/07/14/prismml-releases-bonsai-27b-1-bit-and-ternary-builds-of-qwen3-6-27b-that-run-on-laptops-and-phones/): the 3.9 GB figure is the *weights only*. Using the full 262K context would add about 17.2 GB of KV-cache memory at FP16 (about 4.3 GB even with a 4-bit cache) — so on a phone you get the model, not the model at maximum context.

## The fine print: speed, quality and a not-quite-live demo

How fast is it? The one number that is consistent across [PrismML's site](https://prismml.com/news/prismml-releases-bonsai-27b) and independent write-ups is **11 tokens per second on an iPhone 17 Pro Max** for the 1-bit build — usable for chat, slow for long documents. On bigger hardware, PrismML advertises up to 163 tokens per second on an RTX 5090 and 87 on an Apple M5 Max, though [MarkTechPost's benchmark table](https://www.marktechpost.com/2026/07/14/prismml-releases-bonsai-27b-1-bit-and-ternary-builds-of-qwen3-6-27b-that-run-on-laptops-and-phones/) lists a lower 66.4 tokens per second for the same M5 Max test — a discrepancy neither party has explained, likely down to benchmark methodology.

Quality is the bigger caveat. PrismML claims the ternary build retains about 95% of the original model's performance across 15 benchmarks, and the 1-bit build about 90%, per its [announcement](https://prismml.com/news/bonsai-27b) — but those averages hide the weak spot. On tool-calling and agentic benchmarks, [OfficeChai reports](https://officechai.com/ai/prismml-announces-bonsai27b-the-first-27-billion-parameter-model-that-can-run-on-an-iphone/) scores falling from 80.0 (full precision) to 74.0 (ternary) to 66.0 (1-bit) — exactly the capability that matters for the agent-style assistants everyone wants to run locally.

The community reception reflects that mix. The [Hacker News thread](https://news.ycombinator.com/item?id=48910545) crossed 400 points within a day, with genuine excitement alongside three recurring complaints: benchmark skepticism ("fair comparison plots" were demanded), reproducibility friction (several users couldn't get the GGUF or MLX builds running in LM Studio on day one), and warnings about "doom loop" behavior in multi-turn agent use. [OfficeChai](https://officechai.com/ai/prismml-announces-bonsai27b-the-first-27-billion-parameter-model-that-can-run-on-an-iphone/) also reported that the viral iPhone demo used cached, prefilled image context rather than a fully live end-to-end run. And there's a corporate subplot: PrismML's CEO told CNBC that Apple is "really evaluating our technology right now," per [AppleInsider](https://appleinsider.com/articles/26/07/14/prismml-confirms-it-is-in-talks-with-apple-about-ai-model-shrinking-tech), while [9to5Mac notes](https://9to5mac.com/2026/07/14/prismml-releases-bonsai-27b-claiming-first-major-ai-model-of-its-size-fit-for-iphone/) that real Apple negotiations rarely get talked about publicly — read the Apple angle as unconfirmed.

## How it compares with other phone-scale AI models

The "AI on your phone" race did not start this week. What is new is the *size class* — everything phone-viable until now sat in the roughly 1B–8B range or leaned on sparse tricks. A snapshot of the field, with sources per row:

| Model (release) | Size | Phone footprint | What stands out |
|---|---|---|---|
| **Bonsai 27B** (PrismML, Jul 2026) | ~27B dense | 3.9–5.9 GB weights; ~6 GB free RAM needed | Largest dense model shown running on a phone; open weights ([PrismML](https://docs.prismml.com/models/bonsai-27b)) |
| **Apple AFM 3 Core Advanced** (Jun 2026) | 20B sparse, 1–4B active | Undisclosed; devices unconfirmed | Closed; ships inside Apple Intelligence ([Apple](https://machinelearning.apple.com/research/introducing-third-generation-of-apple-foundation-models)) |
| **Liquid AI LFM2.5-8B-A1B** (May 2026) | 8B MoE, ~1B active | Runs in under 6 GB; ~30 tok/s on mobile | Efficiency-first mixture-of-experts ([Liquid AI](https://www.liquid.ai/blog/lfm2-5-8b-a1b)) |
| **Google Gemma 3n** (2025) | 5–8B, acts like 2–4B | 2–3 GB dynamic footprint | Co-designed with phone chipmakers ([Google](https://developers.googleblog.com/en/introducing-gemma-3n/)) |
| **Qwen3.5 0.8B/2B** (2026) | 0.8–2B | Minimal; browser-capable | Built for battery-constrained devices ([VentureBeat](https://venturebeat.com/technology/alibabas-small-open-source-qwen3-5-9b-beats-openais-gpt-oss-120b-and-can-run)) |
| **Llama 3.2 1B/3B quantized** (2024) | 1–3B | ~1–2 GB | The early mobile milestone ([Meta](https://ai.meta.com/blog/meta-llama-quantized-lightweight-models/)) |

Two honest qualifiers to PrismML's "first" framing: Apple's 20B sparse model predates it by a month (though Apple has never confirmed which devices run it), and "dense 27B on a phone" is PrismML's own category definition. The defensible version of the claim is narrower but still notable — this is the largest open-weight model anyone has demonstrated generating usable output on a standard flagship phone.

## The India angle

No major outlet covered what this means for the world's largest smartphone market by volume, so let's do it here.

**Most phones sold in India can't run it — yet.** Bonsai's ternary build wants roughly 6 GB of free app memory, which in practice means a phone with about 12 GB of total RAM. Budget bestsellers in India — the segment that moves the most units — ship with 4 or 6 GB (Galaxy M17 5G, Moto G45, POCO M7 Pro, realme P3x and similar), per [91mobiles' current budget listings](https://www.91mobiles.com/list-of-phones/best-budget-smartphones). You only reliably get 12–16 GB in the premium tier — devices like the Vivo X300 Pro at the top of [Cashify's 2026 flagship list](https://www.cashify.in/best-phones-to-buy-in-2026). The smaller 1-bit build softens this, but its quality drop is the price. For most Indian users, phone-class frontier AI arrives with their *next* phone, not the current one.

**Why on-device matters more in India than the discourse suggests.** It isn't data cost — India has some of the world's cheapest mobile data, with long-validity plans working out to roughly ₹0.22–0.27 per GB on [BSNL's annual plans](https://www.cashify.in/unlimited-data-plans-in-india-jio-airtel-bsnl). The stronger arguments are reliability (connectivity is far from uniform outside metros), and increasingly, regulation. India's DPDP regime restricts using personal data for AI training without purpose-specific consent, constrains cross-border transfers to an approved-country list, and carries penalties up to ₹250 crore, per [this DPDP compliance guide](https://www.levo.ai/resources/blogs/the-dpdp-india-2026-handbook---the-complete-guide-to-indias-new-data-protection-era). A model that processes your documents entirely on your phone sidesteps most of that surface area by never moving the data at all — a genuinely attractive property for Indian fintech and health apps, and a sharp contrast with [what free cloud chatbots do with your conversations](/articles/ai-chatbot-data-privacy/).

**The sovereign-AI question.** India's own model-builders, most visibly [Sarvam AI](https://www.sarvam.ai/models) with its Indian-language speech and text models (22 Indian languages for translation and speech recognition), have so far targeted servers and APIs. Bonsai's technique — QAT compression of an existing strong model — is exactly the kind of approach that could put an Indian-language model of serious size on mid-range hardware. Whoever does that first gets a distribution advantage no app store can match.

## What to watch

Three things will tell us within weeks whether this was a milestone or a demo. First, **independent benchmarks**: as of today, every quality number traces back to PrismML's own whitepaper; no neutral lab has reproduced them. Second, **the reproducibility gap**: if the day-one failures reported on [Hacker News](https://news.ycombinator.com/item?id=48910545) persist, "runs on a phone" stays theoretical for most people. Third, **who licenses the technique**: the Apple conversation is unconfirmed, but QAT-style compression being courted by device makers is the real story — the value may end up less in Bonsai the model and more in Bonsai the proof that flagship phones are now a viable deployment target for 27B-class intelligence.

The safe conclusion: extreme-compression on-device AI graduated from research papers to shipping software this week. The unsafe conclusion — that your current phone is about to replace ChatGPT — will need cheaper RAM, better tool-calling retention, and probably one more hardware generation. For why on-device inference is such an economic unlock in the first place, see our breakdown of [the real cost of running AI](/articles/real-cost-of-running-ai/). We will keep following Bonsai and the rest of the compression race in our [AI models](/topics/ai-models/) coverage as independent numbers land.

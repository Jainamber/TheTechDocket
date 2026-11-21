---
title: 'Inkling 2 Mini: 26B Looped AI Model Built for Laptops'
slug: inkling-2-mini-looped-transformer-laptops
date: '2026-11-21'
hub: ai-models
tags: [ai-models, local-ai, open-source, coding-tools]
description: Thinking Machines Lab releases Inkling 2 Mini, an Apache 2.0 26.4B looped transformer scoring 79.2% on SWE-bench Verified in a 20GB laptop footprint.
hero_alt: Architectural diagram of Thinking Machines Lab Inkling 2 Mini 24-layer looped transformer running on a laptop
hero_icon: cpu
keyword: Inkling 2 Mini
original_value: Explains how Inkling 2 Mini's middle-layer looping architecture delivers 48-layer reasoning inside a 20GB laptop footprint, benchmarks it against Qwen3.8-27B and Muse Glimmer, and models the India hardware-versus-cloud-API break-even math.
selection_note: ''
sources:
- {title: 'Introducing Inkling 2 Mini — Thinking Machines Lab', url: 'https://thinkingmachines.ai/news/inkling-2-mini/', primary: true}
- {title: 'thinkingmachines/Inkling-2-Mini — Hugging Face Model Card', url: 'https://huggingface.co/thinkingmachines/Inkling-2-Mini', primary: true}
- {title: 'USD to INR Exchange Rate History — Wise', url: 'https://wise.com/in/currency-converter/usd-to-inr-rate/history'}
- {title: 'NVIDIA DGX Spark Price in India 2026 — AceCloud', url: 'https://acecloud.ai/blog/nvidia-dgx-spark-price/'}
- {title: 'NVIDIA DGX Spark 4TB India Listing — nationalPC', url: 'https://nationalpc.in/ai-supercomputers/nvidia-dgx-spark-4tb-ai-supercomputer'}
- {title: 'MacBook Pro 16-inch M5 Pro 48GB — Apple India', url: 'https://www.apple.com/in/shop/buy-mac/macbook-pro/16-inch-space-black-standard-display-apple-m5-pro-chip-18-core-cpu-20-core-gpu-48gb-memory-1tb-storage'}
- {title: 'MacBook Pro M5 Pro India MRP — IndiaiStore', url: 'https://www.indiaistore.com/macbook-pro-m5-41-cm'}
faq:
- {q: 'What makes Inkling 2 Mini a looped transformer?', a: 'Inkling 2 Mini stores 24 transformer layers in memory but runs its middle 12 layers three times per token with shared weights. That design delivers 48 layer passes of serial reasoning per token while keeping the total weight footprint around 20GB.'}
- {q: 'What hardware is required to run Inkling 2 Mini locally?', a: 'Thinking Machines Lab recommends an Apple Silicon Mac with at least 32GB of unified memory, a single NVIDIA DGX Spark, or a discrete GPU with 32GB or more of VRAM. The Apache 2.0 weights run via llama.cpp, Ollama, vLLM, SGLang, and Unsloth.'}
- {q: 'Does Inkling 2 Mini beat Qwen3.8-27B on coding benchmarks?', a: 'In Thinking Machines Lab self-reported evaluations, Inkling 2 Mini leads Qwen3.8-27B on SWE-bench Verified, DeepSWE v1.1, and SWE-bench Pro v2 Hard, while trailing slightly on Terminal Bench v2.1. Full figures and primary source links appear in the benchmark table above.'}
review: {facts_verified: true, sources_checked: true, title_promise_check: true, no_fabrication: true, policy_pass: true, reviewed_at: '2026-11-21T22:52:00+05:30'}
---

Thinking Machines Lab has released [Inkling 2 Mini](https://thinkingmachines.ai/news/inkling-2-mini/) on November 20, 2026, an Apache 2.0 open-weight multimodal model that packs 26.4 billion total parameters into a 20GB checkpoint small enough for a 32GB laptop. By looping its middle 12 layers three times per token, the model hits 79.2% on SWE-bench Verified and 48.2% on DeepSWE v1.1 in vendor benchmarks, giving developers a fast local alternative to metered cloud coding APIs.

## How the Looped Transformer Architecture Works

Inkling 2 Mini stores 24 transformer layers on disk but executes 48 layer applications per token by running its middle 12 layers three times with shared weights, according to the [Thinking Machines Lab technical announcement](https://thinkingmachines.ai/news/inkling-2-mini/). Instead of expanding parameter count to buy deeper reasoning, the architecture reuses existing weights to compute longer serial chains before emitting each token.

The model is a sparse Mixture-of-Experts (MoE) network with 26.4 billion total parameters and 3.4 billion active parameters per single pass, routing each token to 8 of 128 experts per layer, as detailed on the [Hugging Face model card](https://huggingface.co/thinkingmachines/Inkling-2-Mini). Because the middle blocks execute three times, each extra loop adds roughly 1.0 billion effective active parameters, bringing total compute to 5.4 billion effective active parameters per token across a context window of up to 1 million tokens.

To keep the local footprint near 20GB without post-training degradation, Thinking Machines Lab trained and deployed 20 layers natively in 4-bit NVFP4 precision and the final four layers in 8-bit MXFP8 precision, eliminating conversion loss at release time per the [Thinking Machines Lab post](https://thinkingmachines.ai/news/inkling-2-mini/). Mid-training, the team also pruned two-thirds of its original 384 experts down to 128 and healed the model on 1 trillion distilled tokens followed by 2.2 trillion tokens of reinforcement learning.

In scaling tests reported by [Thinking Machines Lab](https://thinkingmachines.ai/news/inkling-2-mini/), an equivalent non-looping baseline cost 7.5% less compute to train but required 140% more inference compute to match the looped model's loss on 512,000-token agentic traces. That trade-off favors local [AI Models](/ai-models/) deployments where memory bandwidth and VRAM ceilings matter far more than one-time pretraining spend, echoing the compression push we covered in [Bonsai 27B](/articles/bonsai-27b-ai-model-phone/).

## Benchmark Comparison Against Sub-100B Open Models

In self-reported evaluations published by [Thinking Machines Lab](https://thinkingmachines.ai/news/inkling-2-mini/), Inkling 2 Mini leads comparable open-weight models under 100 billion parameters on agentic coding and tool-use suites while activating a fraction of their parameters per token. All scores below are vendor-reported from the official release table and should be read alongside independent runtime testing as community harnesses catch up.

| Benchmark / Metric | Inkling 2 Mini (5.4B / 26.4B) | Qwen3.8-27B (27.0B dense) | Muse Glimmer (30.0B dense) | Nemotron 3.5 Super VL (12.0B / 124.5B) |
| :--- | :--- | :--- | :--- | :--- |
| **SWE-bench Verified (bash)** | 79.2% | 77.8% | 76.0% | 71.1% |
| **DeepSWE v1.1** | 48.2% | 42.2% | 4.4% | 24.7% |
| **SWE-bench Pro v2 (Hard)** | 77.9% | 73.8% | 44.3% | 44.1% |
| **Terminal Bench v2.1** | 71.6% | 73.0% | 51.7% | 60.7% |
| **BrowseComp / DeepSearchQA** | 79.0% / 85.3% | 61.6% / 79.7% | 63.9% / 74.6% | 78.9% / 77.7% |
| **MCP Atlas (Tool Use)** | 82.7% | 77.3% | 75.5% | 67.7% |
| **AA-Omniscience Non-Hallucination** | 63.4% | 71.4% | 16.4% | 69.5% |

*Source: Self-reported evaluation table on the [Thinking Machines Lab release page](https://thinkingmachines.ai/news/inkling-2-mini/) and [Hugging Face model card](https://huggingface.co/thinkingmachines/Inkling-2-Mini).*

Energy efficiency is where the sparse looped layout widens the gap. Early testing by researchers at Stanford's Hazy Research Lab and Scaling Intelligence Lab on an NVIDIA DGX Spark (128GB) measured Inkling 2 Mini at 0.703 on their intelligence-per-joule metric, ahead of Qwen3.6-35B-A3B at 0.430, Gemma-4-26B-A4B at 0.159, and Qwen3.5-27B at 0.036, according to [Thinking Machines Lab](https://thinkingmachines.ai/news/inkling-2-mini/).

The release notes are blunt about where looping does not help. Reusing weights three times improves serial reasoning and long-context retrieval, yet it cannot store extra world knowledge inside 26.4 billion parameters, leaving Inkling 2 Mini at a 63.4% non-hallucination rate on AA-Omniscience v1.1 behind Qwen3.8-27B's 71.4%, as shown on the [Hugging Face model card](https://huggingface.co/thinkingmachines/Inkling-2-Mini). It also trails Qwen3.8-27B on multi-turn chat (`MultiChallenge` 50.0%) and can enter repetitive debugging loops unless developers cap output tokens and agent turns.

## Local Hardware, Runtimes, and Safety Trade-Offs

Inkling 2 Mini runs offline on Apple Silicon Macs with 32GB or more of unified memory, a single NVIDIA DGX Spark, or discrete GPUs with at least 32GB of VRAM, according to the [Hugging Face model card](https://huggingface.co/thinkingmachines/Inkling-2-Mini). Thinking Machines Lab demonstrated the model building a playable flight simulator in airplane mode on a 48GB M5 Pro MacBook Pro, and day-one runtime support spans `llama.cpp`, Ollama, vLLM, SGLang, Unsloth, and Exo Labs.

Because looped models perform extra internal computation before writing tokens, researchers have worried that looping could hide reasoning from chain-of-thought monitors. Alongside Inkling 2 Mini, [Thinking Machines Lab](https://thinkingmachines.ai/news/inkling-2-mini/) released a variable-loop research checkpoint (`TML-d24-varloop-research`) showing that no-CoT task horizon rose from 16 seconds at one pass to 37 seconds at three passes without increasing covert sabotage rates (8.3% internal covert misbehavior versus 33.2% for Qwen3.8-27B and 45.6% for [Muse Glimmer](/articles/muse-glimmer-meta-open-model/)). Still, the model card explicitly advises sandboxing agentic runs and requiring human confirmation before file deletion or writes.

## The India Angle

For Indian software engineers and startups paying for cloud coding agents in US dollars, a 20GB Apache 2.0 model that hits 79.2% on SWE-bench Verified changes the buy-versus-rent math immediately. At the November 21, 2026 spot rate of ₹92.68 per US dollar reported by [Wise](https://wise.com/in/currency-converter/usd-to-inr-rate/history), a $200 monthly USD coding API or subscription bill incurs a typical 3.5% bank forex markup plus 18% IGST, bringing the real out-of-pocket cost to ₹22,638 per month (₹2.72 lakh per year) before enterprise seat overages like the $13-per-day averages we analyzed in [Claude Code vs Pi](/articles/claude-code-pi-developers-swapping-terminal-agents/).

| Setup / Cost Dimension | US Price (USD) | India Retail / Effective Cost (INR) | Break-Even / Markup Note |
| :--- | :--- | :--- | :--- |
| **Apple 24GB to 48GB RAM Upgrade** | Hardware tier step | ₹72,000 ([Apple India](https://www.apple.com/in/shop/buy-mac/macbook-pro/16-inch-space-black-standard-display-apple-m5-pro-chip-18-core-cpu-20-core-gpu-48gb-memory-1tb-storage)) | Pays back in ~3.2 months vs. $200/mo USD API |
| **MacBook Pro 16" M5 Pro (48GB / 1TB)** | Full laptop purchase | ₹3,59,900 MRP ([IndiaiStore](https://www.indiaistore.com/macbook-pro-m5-41-cm)) | ₹3,44,900 with ₹15,000 bank card cashback |
| **NVIDIA DGX Spark (128GB / 4TB)** | $6,950 ([AceCloud](https://acecloud.ai/blog/nvidia-dgx-spark-price/)) | ₹7,89,990 incl. GST ([nationalPC](https://nationalpc.in/ai-supercomputers/nvidia-dgx-spark-4tb-ai-supercomputer)) | ~3.9% India channel markup over ₹7,60,069 US+18% GST base |
| **Cloud Coding API ($200/mo USD)** | $200 / month | ₹22,638 / month (incl. 3.5% forex + 18% IGST) | Recurring FX + tax drag; ₹2.72 lakh/year ([Wise](https://wise.com/in/currency-converter/usd-to-inr-rate/history)) |

On Apple's Indian storefront, stepping up a MacBook Pro from 24GB to 48GB of unified memory costs ₹72,000 on top of the base machine, per [Apple India](https://www.apple.com/in/shop/buy-mac/macbook-pro/16-inch-space-black-standard-display-apple-m5-pro-chip-18-core-cpu-20-core-gpu-48gb-memory-1tb-storage), while a 16-inch M5 Pro 48GB configuration carries an MRP of ₹3,59,900 (₹3,44,900 after card cashback) via [IndiaiStore](https://www.indiaistore.com/macbook-pro-m5-41-cm). For small Indian engineering teams looking at dedicated desk-side inference, the 128GB NVIDIA DGX Spark listed at $6,950 in the US per [AceCloud](https://acecloud.ai/blog/nvidia-dgx-spark-price/) converts to a ₹7,60,069 landed base after 18% GST at ₹92.68 per dollar, putting Indian reseller pricing of ₹7,89,990 at [nationalPC](https://nationalpc.in/ai-supercomputers/nvidia-dgx-spark-4tb-ai-supercomputer) at a modest 3.9% channel markup with GST input-tax credit eligibility.

Running an Apache 2.0 model locally also addresses client data-residency clauses for Indian IT services firms and fintech teams adapting to India's DPDP Act rules, a trade-off we examined in [On-Device AI vs Cloud AI](/articles/on-device-ai-vs-cloud-ai/) and [The Real Cost of Running AI](/articles/real-cost-of-running-ai/). Source code, internal schemas, and customer logs stay on the workstation rather than crossing borders to a metered US endpoint.

## What to Watch

Three practical questions will determine whether Inkling 2 Mini replaces cloud coding models in daily workflows over the next 30 days. First, independent developers need to verify real-world tokens-per-second throughput on 32GB and 48GB Macs using quantized GGUF builds, since [Thinking Machines Lab](https://huggingface.co/thinkingmachines/Inkling-2-Mini) notes that looped-layer runtime support is brand new and speed varies across inference engines.

Second, expect open-source coding harnesses like Pi, Aider, and OpenHands to test whether Inkling 2 Mini's repetitive-loop failure mode can be contained with strict turn budgets without hurting its 79.2% SWE-bench Verified score reported by [Thinking Machines Lab](https://thinkingmachines.ai/news/inkling-2-mini/). Third, if looped transformers reliably halve memory requirements at comparable coding accuracy, rival labs building sub-30B local models will face pressure to adopt weight-sharing loops in their next 2027 releases.
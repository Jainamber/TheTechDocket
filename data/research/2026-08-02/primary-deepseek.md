# DeepSeek V4 Flash (Official Release, build "0731") — Primary Source Research

Research date: 2026-08-02. Scope: DeepSeek's own published materials only (official API docs, Hugging Face model cards, DeepSeek's own X/Twitter account). Third-party coverage (MarkTechPost, TechNode, Caixin, OfficeChai, XenoSpectrum, etc.) was used only to find which official pages to check, and is NOT used as a source for any fact below unless explicitly labeled otherwise.

Two distinct DeepSeek-published model cards exist and are NOT identical — this doc keeps them separate throughout:
- **DeepSeek-V4-Flash** (preview) — released as part of the April 24, 2026 V4 preview.
- **DeepSeek-V4-Flash-0731** — released ~July 31, 2026, described by DeepSeek as "the official release of DeepSeek-V4-Flash, superseding the preview version."

---

## Verified facts

### What it is / what changed
- DeepSeek-V4-Flash-0731's Hugging Face model card describes it as: "DeepSeek-V4-Flash-0731 is the official release of DeepSeek-V4-Flash, superseding the preview version, with substantially enhanced agentic capabilities," and states it "outperforms DeepSeek-V4-Pro (Preview) on benchmarks listed below despite its far smaller activated parameter count." — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731
- On DeepSeek's own official X/Twitter account (@deepseek_ai), a post states: "DeepSeek-V4-Flash-0731 keeps the exact same model architecture and size as the preview version. Today's upgrade applies ONLY to the DeepSeek-V4-Flash API. The DeepSeek-V4-Pro API and App/Web models remain unchanged for now. The official release of DeepSeek-V4-Pro is coming ASAP!" — meaning the improvement is from retraining/post-training, not an architecture change, and the chat.deepseek.com app/web product was NOT updated to V4-Flash-0731 at the time of this post. — https://x.com/deepseek_ai/status/2083084419515220191 (verified via search-result snippet only; direct page fetch was blocked by X's robots.txt, so the full surrounding thread/context could not be independently re-confirmed — treat as high-confidence but not page-rendered-and-read by me)
- DeepSeek-V4-Flash-0731's model card states it "includes a speculative decoding module (DSpark)" and has the "Same model structure as DeepSeek-V4-Flash-DSpark." — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731

### Architecture, context window, modalities (preview version, released April 24, 2026)
- DeepSeek's official April 24, 2026 API-docs announcement states V4-Flash is "284B total / 13B active params," part of the same release where "V4-Pro: 1.6T total / 49B active params." — https://api-docs.deepseek.com/news/news260424/
- The Hugging Face model card for the preview build confirms: Total parameters 284 billion, Activated parameters 13 billion, Mixture-of-Experts (MoE) structure, Context length 1 million tokens, mixed FP4 (MoE expert parameters) + FP8 (most other parameters) precision. — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash
- Architecture upgrades named on the same card: a hybrid attention design combining "Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA)," "Manifold-Constrained Hyper-Connections (mHC)," and the "Muon Optimizer"; pre-trained on "more than 32T diverse and high-quality tokens." — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash
- The linked DeepSeek technical paper (title: "DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence," DeepSeek-AI authorship) independently states the same 284B-total/13B-active figure for V4-Flash and 1.6T-total/49B-active for V4-Pro, and claims "DeepSeek-V4-Pro requires only 27% of single-token inference FLOPs and 10% of KV cache compared with DeepSeek-V3.2" at million-token context. — https://huggingface.co/papers/2606.19348 (mirror of arXiv:2606.19348)
- Modality: text generation / conversational only — no vision or audio mentioned on either DeepSeek-V4-Flash or DeepSeek-V4-Flash-0731 model cards. — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash and https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731

### Architecture / context window (0731 build specifically)
- DeepSeek-V4-Flash-0731's own model card states "Total Parameters: 304B" and lists tensor types BF16, I64, F32, F8_E4M3, I8 among the published weight files; License = MIT with a `LICENSE` file in the repo. — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731
- The 0731 card does not itself restate a context-window figure in prose (its title references "Million-Token Context Intelligence" but no explicit number is given on-card). — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731
- DeepSeek's official pricing page lists context length as 1M tokens for the `deepseek-v4-flash` API model (the same API endpoint DeepSeek's X post says now serves the -0731 weights), with a recommended maximum output of 384K tokens. — https://api-docs.deepseek.com/quick_start/pricing
- The 0731 model card recommends: "For local deployment, we recommend setting the sampling parameters to `temperature = 1.0`, with `top_p = 0.95` for agentic scenarios and `top_p = 1.0` otherwise. For the `high` and `max` reasoning effort levels, we recommend a maximum output length of 384K tokens." — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731
- The 0731 card states the `reasoning_effort` API parameter "now supports three levels — `low`, `high`, and `max` — which control how much deliberation the model spends before answering." — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731

> Note on the parameter-count discrepancy (284B vs. 304B): see "Unverified/unclear" below — this is flagged, not silently resolved.

### License
- DeepSeek-V4-Flash-0731 weights are released under the MIT License, per the model card and the repo's `LICENSE` file link. — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 (LICENSE file at https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/tree/main/LICENSE)
- The preview DeepSeek-V4-Flash model card also lists MIT License. — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash

### Official API pricing (per 1M tokens)
Per DeepSeek's official pricing page, for model `deepseek-v4-flash`:
- Input, cache hit: $0.0028 per 1M tokens — https://api-docs.deepseek.com/quick_start/pricing
- Input, cache miss: $0.14 per 1M tokens — https://api-docs.deepseek.com/quick_start/pricing
- Output: $0.28 per 1M tokens — https://api-docs.deepseek.com/quick_start/pricing
For comparison, `deepseek-v4-pro` on the same page: input cache hit $0.003625, input cache miss $0.435, output $0.87 per 1M tokens. — https://api-docs.deepseek.com/quick_start/pricing
- Same page states context length 1M tokens and max output 384K tokens for both models; concurrency limits of 2,500 requests (Flash) vs. 500 (Pro); base URLs `https://api.deepseek.com` (OpenAI-compatible format) and `https://api.deepseek.com/anthropic` (Anthropic-compatible format); billing formula "expense = number of tokens × price," deducted from topped-up or granted balance (granted balance prioritized). — https://api-docs.deepseek.com/quick_start/pricing
- The page does not list any off-peak/discount pricing tier at the time of this research (no such tier is mentioned on the page). — https://api-docs.deepseek.com/quick_start/pricing
- Note: the pricing page identifies the model only as `deepseek-v4-flash` / `DeepSeek-V4-Flash` — it does not print the string "0731." The connection between this pricing and the -0731 build rests on DeepSeek's own X post (above) stating the V4-Flash API now serves the -0731 checkpoint.

### Official benchmark claims (DeepSeek-V4-Flash-0731 model card)
Exact table as published (model card gives DeepSeek-V4-Flash-0731 alongside DeepSeek's own comparison figures for DeepSeek-V4-Flash Preview, DeepSeek-V4-Pro Preview, GLM-5.2, and Opus-4.8):

| Benchmark | V4-Flash-0731 | V4-Flash (Preview) | V4-Pro (Preview) | GLM-5.2 | Opus-4.8 |
|---|---|---|---|---|---|
| Terminal Bench 2.1 | 82.7 | 61.8 | 72.1 | 81.0 | 85.0 |
| NL2Repo | 54.2 | 39.4 | 38.5 | 48.9 | 69.7 |
| Cybergym | 76.7 | 38.7 | 52.7 | – | 83.1 |
| DeepSWE | 54.4 | 7.3 | 12.8 | 46.2 | 58.0 |
| Toolathlon-Verified | 70.3 | 49.7 | 55.9 | 59.9 | 76.2 |
| Agents' Last Exam | 25.2 | 15.8 | 16.5 | 23.8 | 25.7 |
| AutomationBench Public | 25.1 | 10.8 | 12.8 | 12.9 | 27.2 |
| DSBench-FullStack † | 68.7 | 37.0 | 41.8 | 61.8 | 71.6 |
| DSBench-Hard † | 59.6 | 25.8 | 31.1 | 54.5 | 71.7 |

Source for entire table: https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 (verified via two independent fetches of the same page, figures identical both times)

Separately, on the preview DeepSeek-V4-Flash card, DeepSeek publishes: MMLU (5-shot) 88.7%, MMLU-Pro (5-shot) 68.3%, HumanEval (0-shot) 69.5%, GSM8K (8-shot) 90.8%, LongBench-V2 (1-shot) 44.7%. — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash

### Availability
- Weights: downloadable from Hugging Face at `deepseek-ai/DeepSeek-V4-Flash-0731`, MIT licensed, safetensors in BF16/F32/F8_E4M3/I8 (plus the bundled DSpark speculative-decoding draft module). — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731
- API: available now via `api.deepseek.com` under model name `deepseek-v4-flash` (OpenAI ChatCompletions-compatible and Anthropic-compatible endpoints). — https://api-docs.deepseek.com/quick_start/pricing and https://api-docs.deepseek.com/news/news260424/
- App/Web (chat.deepseek.com): per DeepSeek's own X post, NOT updated to the -0731 build as of that post — "The DeepSeek-V4-Pro API and App/Web models remain unchanged for now." — https://x.com/deepseek_ai/status/2083084419515220191 (search-snippet-verified only, see caveat above)
- The model card links out to a vLLM recipe and an SGLang cookbook for self-hosted deployment, and an in-repo `inference/README.md`. — https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731

### Legacy model-name mapping (from the April 24, 2026 official changelog, still relevant context)
- DeepSeek's official changelog states the model parameter should be set to `deepseek-v4-pro` or `deepseek-v4-flash`; the legacy names `deepseek-chat` and `deepseek-reasoner` currently map to V4-Flash's non-thinking and thinking modes respectively, and were slated for discontinuation on 2026-07-24 (three months after the April 24, 2026 entry). — https://api-docs.deepseek.com/updates/

---

## Unverified/unclear

- **Exact release date/time of "0731" is not confirmed on any DeepSeek-owned changelog page.** As of this research (fetched 2026-08-02), DeepSeek's own API changelog at https://api-docs.deepseek.com/updates/ still shows 2026-04-24 (the V4 preview) as its newest entry — there is no DeepSeek-published changelog entry for V4-Flash-0731 yet. The "July 31, 2026" date is inferred only from the "0731" naming convention and from third-party reporting (e.g., TechNode, MarkTechPost, dated 2026-07-31) — NOT from a DeepSeek-owned dated announcement page. UNVERIFIED as a DeepSeek-stated date.
- **Total parameter count conflict: 284B vs. 304B.** The preview `DeepSeek-V4-Flash` card and DeepSeek's own April 24 news page both say 284B total / 13B active params (cross-confirmed by the DeepSeek technical paper at https://huggingface.co/papers/2606.19348). The official-release `DeepSeek-V4-Flash-0731` card instead shows "304B params" and does not restate an activated-parameter count. DeepSeek's own X post says -0731 "keeps the exact same model architecture and size as the preview version," which conflicts with the raw 284B-vs-304B figures unless the 304B figure on Hugging Face includes the bundled DSpark speculative-decoding draft module's extra weights (the card does say -0731 "includes a speculative decoding module (DSpark)"). This explanation is my own plausible inference, NOT a statement DeepSeek has made explicitly — flag as UNVERIFIED and recommend a human visually check the live Hugging Face page before publishing a specific total-parameter number for the -0731 build.
- **Hugging Face org page (`huggingface.co/deepseek-ai`) listing figures don't match the model cards.** A fetch of the org's model listing showed "DeepSeek-V4-Flash" tagged at "158B parameters" (vs. 284B stated in that same model's own card) and "DeepSeek-V4-Pro" at "862B" (vs. 1.6T stated elsewhere). These are likely mis-reads of the page by the fetch tool rather than real DeepSeek-published figures, since they contradict the model's own card — excluded from "Verified facts" above; do not use 158B/862B in the article. UNVERIFIED / likely extraction artifact.
- **Currency symbol on the pricing page was inconsistently reported across repeated fetches** (one fetch said no currency symbol was present; two others quoted "$" explicitly). Figures ($0.0028 / $0.14 / $0.28 per 1M tokens) are consistent across all fetches and match independent third-party reporting (e.g., a widely-quoted "$0.14/$0.28 per 1M tokens" figure attributed to DeepSeek-V4-Flash-0731 circulating in press coverage), so treat the numbers as solid but the "$" as reasonably-inferred rather than triple-confirmed verbatim. Recommend a quick manual glance at https://api-docs.deepseek.com/quick_start/pricing before publishing to confirm the $ sign renders on the live page.
- **Could not access directly (blocked in this environment), so not used as sources:** https://deepseek.com (homepage — repeated PROVENANCE_REQUIRED/permission-timeout errors), https://github.com/deepseek-ai (org page — same error), https://arxiv.org/abs/2606.19348 (direct arXiv page — same error; used the Hugging Face paper mirror instead), full X/Twitter thread pages under x.com/deepseek_ai (blocked by robots.txt; only search-engine snippets of specific posts could be captured). If the article needs anything from these specifically, it should be re-fetched with direct user/browser access rather than this tool.
- **Whether DeepSeek-V4-Pro has also received an "official release" build (vs. still being "Preview") is unresolved.** DeepSeek's own X post explicitly says "The official release of DeepSeek-V4-Pro is coming ASAP" (future tense, as of the -0731 post) — so as of 2026-08-02, V4-Pro should still be preview-only. Not independently re-confirmed beyond that one quoted post.
- **No DeepSeek-stated exact figure for how much better -0731 is "vs V3.x"** — all official comparison figures found are against V4-Flash (Preview) and V4-Pro (Preview), not against V3.x models. Any V3-vs-V4 comparison in the article should either be sourced separately or marked UNVERIFIED.

# Docket Fact-Verification — 2026-08-02

Method: WebSearch (to establish fetch permission) → WebFetch each URL. Where a
target blocked WebFetch's AI-summarization step gave inconsistent results across
passes, the raw source was re-fetched and/or cross-checked against a second
independent fetch until figures were verbatim-confirmed. Only figures that
appear in a fetched source are reported as VERIFIED; anything that could not be
matched to source text is marked UNVERIFIED.

---

## Item 1 — Chrome blog: "fixed more Chrome bugs in June than over past two years, thanks to AI"

Source: https://blog.google/security/chrome-stronger-with-every-update/

**VERIFIED facts:**
- Blog post title: "Stronger with every update: How we're making Chrome and the web safer in the AI Era" — https://blog.google/security/chrome-stronger-with-every-update/
- Byline/date (verbatim): "Jul 30, 2026 | Chrome Security Team" — https://blog.google/security/chrome-stronger-with-every-update/
- Verbatim quote: "In Chrome 149 and 150, we have fixed 1072 security bugs" — surpassing "the total number of security bugs fixed across the prior 23 milestones combined." — https://blog.google/security/chrome-stronger-with-every-update/
- Chrome versions 149 and 150 were both released in June 2026, and the prior 23 milestones (spanning roughly the past two years) totaled **1,036** fixes combined — reported by two independent secondary sources: https://techcrunch.com/2026/07/30/google-says-it-fixed-more-chrome-bugs-in-june-than-over-the-past-two-years-thanks-to-ai/ and https://tech.yahoo.com/cybersecurity/articles/google-says-fixed-more-chrome-185758392.html
- AI system credited: **Gemini**. Quote attributed to Chrome engineering director Doug Turner: "By applying models like Gemini, we are preemptively fixing vulnerabilities, outpacing our adversaries." — https://techcrunch.com/2026/07/30/google-says-it-fixed-more-chrome-bugs-in-june-than-over-the-past-two-years-thanks-to-ai/ (Google also names two other AI systems in its own post: **Naptime**, built with Project Zero in 2024, and **Big Sleep**, built with DeepMind and Project Zero in 2025 — https://blog.google/security/chrome-stronger-with-every-update/)
- Single most striking number: **1,072** security bugs fixed in just two Chrome milestones (149 & 150), exceeding the combined total from the prior 23 milestones (~2 years) — https://blog.google/security/chrome-stronger-with-every-update/
- Other exact figures stated in the post: a vulnerability "quietly survived in our codebase for more than 13 years" before being found; "In May alone, we blocked over 20 vulnerabilities from reaching production"; bug reports in March 2026 alone exceeded the entirety of 2025; Chrome has "more than 2,300 third-party dependencies," of which "about 1,700... are shipped to users"; "97% of first-party Chrome code compiles cleanly" — https://blog.google/security/chrome-stronger-with-every-update/

**UNVERIFIED:** The word "June" and the figure "1,036" (for the prior-23-milestone total) could not be pulled as a verbatim quote directly from blog.google's own text in repeated extraction passes — they are confirmed only via secondary reporting (TechCrunch, Yahoo), not a direct quote lifted from the primary post itself.

---

## Item 2 — arXiv 2607.27197: "The Maxwell Conjecture Is False (GPT 5.6 Sol)"

Source: https://arxiv.org/abs/2607.27197 (PDF cross-check: https://arxiv.org/pdf/2607.27197)

**VERIFIED facts:**
- Conjecture: Maxwell's conjecture (proposed by physicist James Clerk Maxwell) — that the electrostatic potential of n point charges has at most (n−1)² critical points, all non-degenerate. — https://arxiv.org/abs/2607.27197
- Result: The paper exhibits a configuration of **five** point charges in space whose potential has **at least 24** non-degenerate critical points, exceeding the conjectured maximum of (5−1)² = **16** — disproving the conjecture. — https://arxiv.org/abs/2607.27197
- AI model's exact stated role (found in the paper's "Tool and computational resource disclosure" section, not in the abstract itself): **"The idea behind this construction was suggested by an LLM (OpenAI's GPT5.6 Sol)."** The authors state they verified the mathematical details and wrote the argument themselves; computer algebra software (Mathematica and Maple) was used for verification/visualization. — https://arxiv.org/pdf/2607.27197
- Author count: **3** — Philip Arathoon (Babson College, MA), Gavin Ball (University of Missouri, Columbia, MO), Matthew D. Kvalheim (University of Maryland, Baltimore County, MD). — https://arxiv.org/pdf/2607.27197
- Date: submitted **July 29, 2026** (arXiv:2607.27197v1). — https://arxiv.org/abs/2607.27197 ; https://arxiv.org/pdf/2607.27197

**UNVERIFIED:** The abstract section proper does not mention any AI model at all — confirmed by two independent fetches of the abstract page. The "GPT-5.6 Sol" credit is real but located in the paper's disclosure section (body text), not the abstract, so a claim that "the abstract states GPT-5.6 Sol's role" would be inaccurate.

---

## Item 3 — github.com/sqliteai/waste: "Run Kimi K3 using 29 GB of RAM at 0.50 tok/s"

Source: https://github.com/sqliteai/waste (README fetched directly)

**VERIFIED facts:**
- Repo/purpose: **waste** — "WASTE — Weight-Aware Streaming Tensor Engine," a dependency-free, embeddable C inference engine that keeps a model's "trunk" resident in RAM and streams activated expert weights directly from NVMe disk, letting a model larger than available RAM run. — https://github.com/sqliteai/waste
- Model: **Kimi K3**, 2.78 trillion parameters — "the complete open-weights Kimi K3 model... This is not a distilled, pruned, or reduced variant," converted into a 982 GiB container (from a 1.42 TB / 96-safetensors-shard original). — https://github.com/sqliteai/waste
- RAM figure: minimum **29.05 GB** to open K3 at 4K context (rising to 30.54 GB at 32K, 35.63 GB at 128K, 83.21 GB at 1M context); resident trunk alone is 27.28 GB. — https://github.com/sqliteai/waste
- Speed figures: overall stated decode range is **0.45–0.62 tok/s "at the default budget"** on a 64 GB MacBook Pro M5 Pro. The README's detailed benchmark table gives per-budget decode speed: 32 GB budget → **0.50 tok/s** (0% expert-cache hit rate); 46 GB → 0.53–0.55 tok/s; 52 GB → 0.04–0.15 tok/s ("not reproducible"); 58 GB → 0.02–0.03 tok/s. — https://github.com/sqliteai/waste
- Humor/utility angle: "Why the name" section — "Every token answered by a cloud service is paid for twice: once on the invoice, and once in the electricity of a datacenter running a model that would fit — barely, awkwardly, but genuinely — on hardware already sitting on a desk. WASTE means to be the first concrete step toward ending that waste of tokens. The acronym came second." Also explicitly self-deprecating: "It is also slow — half a token per second, twenty-six seconds for the sentence above," which the README insists "should not be read as a disclaimer." — https://github.com/sqliteai/waste
- Other exact numbers: alternative model Kimi-Linear 48B runs from a 19 GiB container, 1.87 GB minimum RAM, at 10.7 tok/s (78% cache hit, 8 GB budget); conversion takes ~4.7 hours (3 processes, M5 Pro) or 23.7 hours with a pure-torch encoder; internal SSD measured at 12.78 GB/s vs. 0.94 GB/s over a USB enclosure; output logits agree with the PyTorch reference to 3.6e-06; vision tower (401M-parameter, 27-layer ViT) matches its oracle to 2.3e-06; experts are quantized at 3.00 bits/weight; 92 MoE layers, 16 experts read per token; "read-ahead" gives ~1.6x speed-up and raises cache hit rate from 14% to 38%; License: Apache 2.0, Copyright 2026 SQLite Cloud, Inc. — https://github.com/sqliteai/waste

**UNVERIFIED / flagged discrepancy:** The claim pairs "29 GB of RAM" with "0.50 tok/s" as if it's one data point, but the README does not state them together. **29.05 GB is the minimum RAM floor just to open the model** (no throughput figure is given at exactly that budget); **0.50 tok/s is the decode speed measured at a 32 GB budget** (a higher, distinct configuration), per the benchmark table. Both individual numbers are real and appear in the source, but not paired as the claim implies. (Hacker News discussion reproduces the claim's exact wording: https://news.ycombinator.com/item?id=49123386 — not independently re-verified beyond the title text seen in search results.)

---

## Item 4 — WSJ: "Situational Awareness (fund) down 67% in July in AI stock rout"

Primary URL attempted: https://www.wsj.com/finance/investing/situational-awareness-down-67-in-july-in-ai-stock-rout-cd19901f — **fetch failed** (permission/paywall error). Per instructions, used a secondary source instead of retrying WSJ directly.

Secondary source used: https://thecurrency.news/articles/235211/situational-awareness-down-67-in-july-in-ai-stock-rout/ (dated July 31, 2026), cross-checked against WSJ's own excerpt of the story posted to X: https://x.com/WSJ/status/2083047583807672678

**VERIFIED facts:**
- Fund: **Situational Awareness** (a hedge-fund firm). — https://thecurrency.news/articles/235211/situational-awareness-down-67-in-july-in-ai-stock-rout/
- Whose fund: founded/run by **Leopold Aschenbrenner**. — https://thecurrency.news/articles/235211/situational-awareness-down-67-in-july-in-ai-stock-rout/
- Down in July: WSJ's own posted excerpt states the firm "is down around **67%** so far in July after incurring heavy losses on AI stocks, according to a person who saw a letter the firm sent to investors Thursday." — https://x.com/WSJ/status/2083047583807672678
- Why: heavy losses on AI-related stock holdings amid a broader AI stock sell-off ("AI stock rout"). — https://thecurrency.news/articles/235211/situational-awareness-down-67-in-july-in-ai-stock-rout/
- Key numbers: the firm attempted to sell **$3.5 billion** in Anthropic shares (a deal it later backed out of); it sold a bulk of its stock holdings to Ken Griffin's **Citadel** to meet margin calls; Aschenbrenner told investors in a letter, "We let you down this month." — https://thecurrency.news/articles/235211/situational-awareness-down-67-in-july-in-ai-stock-rout/

**UNVERIFIED:** None of the key figures above were left unconfirmed; the direct WSJ article text itself (beyond its own posted excerpt) could not be fetched due to the paywall/permission error.

---

## Item 5 — Quanta Magazine: "Is AI Reasoning Right for the Wrong Reasons?"

Source: https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/

**VERIFIED facts:**
- Author: **John Pavlus**. — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
- Publication date: **July 31, 2026** (per byline and URL date stamp). — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
- Dek/sub-headline (verbatim): "The idea that artificial intelligence can 'reason' is more intuitive than ever. But intuitions can be wrong, and the science is far from settled." — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
- Core question: whether AI "reasoning" models actually reason via the chains of thought they display, or arrive at correct answers through different, poorly understood mechanisms while the visible "thinking" is largely decorative/non-causal. — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
- Key findings/studies with figures:
  1. Northeastern University and UC Berkeley (2025): "between 30% and 60% of their 'thinking steps' had 'minimal causal impact'" on the model's final answer. — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
  2. New York University (2024): "meaningless filler tokens" (e.g., strings of dots) could function as effectively as legible chains of thought. — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
  3. An OpenAI general-purpose reasoning model "solved a famous open mathematical research problem in one shot" in May 2026. — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
  4. Google DeepMind, with Terence Tao (2026): rediscovered or improved solutions to **67 problems** spanning mathematical analysis, combinatorics, geometry, and number theory. — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
  5. Large reasoning models achieved gold-medal-level results at the International Mathematical Olympiad in 2025; separately, Apple researchers published the "Illusion of Thinking" paper critiquing reasoning reliability, and Santa Fe Institute research found models rely on "surface-level shortcuts." — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/
- One-line conclusion: AI reasoning models frequently produce correct answers, but whether — and how — their visible "thought process" causally drives those answers remains scientifically unsettled (per ASU's Subbarao Kambhampati, chains of thought may be closer to "mumblings" than reasoning). — https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/

**UNVERIFIED:** None — figures above were confirmed consistently across two independent fetch passes of the same article.

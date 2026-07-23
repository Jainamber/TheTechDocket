# Research Notes: Chinese Open-Weight AI Models — Adoption, the Analyst Debate, and the India Angle

Compiled 2026-07-23. Scope: (A) adoption evidence for Chinese open-weight models (Qwen, Kimi, DeepSeek, GLM, etc.), (B) the Ben Thompson/Stratechery vs. werd.io analyst debate plus counter-arguments, (C) India-specific angle — companies, government stance, data privacy.

Method note: WebSearch first, WebFetch only on URLs returned in search results. Several outlets blocked direct fetch (CNBC.com direct article 403'd twice; Tom's Hardware 403'd; hn.algolia.com API rejected as a hand-typed/non-provenance URL) — in those cases I relied on corroborating outlets that did fetch successfully (Slashdot's syndication of the CNBC/lawmakers story, MIT Tech Review's independent reporting, etc.) or on the search-result snippet/headline only, which is flagged inline.

---

## A. ADOPTION EVIDENCE

### Hugging Face (primary platform data)

- Chinese open-weight models captured **41% of global downloads** on Hugging Face, surpassing US models for the first time, per Hugging Face's own "State of Open Source on Hugging Face: Spring 2026" report.
  — SOURCE: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026 (corroborated: https://finance.biggo.com/news/309a4fab-5b28-4605-b0e0-e0ad42e5d3df)
- Alibaba's **Qwen family has over 113,000 derivative models** on the Hub (ballooning to "over 200,000" including all tagged versions) — more derivatives than Google and Meta combined.
  — SOURCE: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026
- **DeepSeek-R1 is the "most liked" model on the Hub**, displacing Meta's Llama family from the top spot it held the prior year.
  — SOURCE: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026
- Chinese lab release-cadence growth: **Baidu went from zero releases in 2024 to over 100 in 2025**; **ByteDance and Tencent each increased releases roughly 8–9x**.
  — SOURCE: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026
- "The majority of trending models" on the Hub in 2025 were either developed in China or derivatives of Chinese models.
  — SOURCE: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026
- Hugging Face hosts nearly 3 million public models and 1 million datasets; a new repository is created roughly every 7 seconds; half of Fortune 500 companies have deployed models via the platform.
  — SOURCE: https://finance.biggo.com/news/309a4fab-5b28-4605-b0e0-e0ad42e5d3df
- Quote, Hugging Face CEO Clem Delangue: **"If China continues to lead in open-source, it could achieve overall AI leadership within one to two years."**
  — SOURCE: https://finance.biggo.com/news/309a4fab-5b28-4605-b0e0-e0ad42e5d3df

### OpenRouter (public token-share rankings) — multiple snapshots, present separately, do not average

Different outlets cite different snapshot dates/methodologies (weekly vs. average, top-10-only vs. all models). Treating each as a distinct dated data point rather than a single consistent number:

- **Top six most-used models on OpenRouter are all Chinese** (Tencent, Xiaomi, DeepSeek, MiniMax, Z.ai/Zhipu); Anthropic's Claude Opus 4.7 ranks 7th. Reported as of mid-July 2026.
  — SOURCE: https://techcrunch.com/2026/07/14/the-real-ai-race-may-no-longer-be-at-the-frontier-open-models-hugging-face/
- CNBC investigation (published **July 7, 2026**): Chinese-origin models' weekly OpenRouter token share hit a **peak of 46%** by mid-2026, up from **4.5% in H1 2025** and averaging **11% over the prior 12 months**; weekly share has stayed above 30% since **February 8, 2026**. Same snapshot breaks out **DeepSeek at 17.6%** (5.13 trillion tokens/week) and **Alibaba Qwen at 13.9%** (2.77 trillion tokens/week); combined Chinese-origin **46.4% vs. US-origin 35.7%** (Anthropic alone 14.8%). Total OpenRouter volume grew from ~5 trillion tokens/week (April 2025) to 20+ trillion tokens/week (April 2026).
  — SOURCE: https://aicommission.org/2026/07/chinese-ai-models-now-capture-up-to-46-of-us-enterprise-token-usage/ (citing CNBC, July 7, 2026)
- Separate framing: "Chinese-developed language models now account for roughly **61% of token consumption among the top 10 models** on OpenRouter," up from under 1.2% of weekly consumption in late 2024, ~13% average through 2025 (peaking near 30%), and **51% in an April 2026 snapshot**. Programming/agentic workloads specifically climbed from ~11% to over 50% through 2025.
  — SOURCE: https://www.kucoin.com/news/flash/openrouter-data-shows-61-of-token-consumption-by-chinese-ai-models
- Separate framing: **US models' (Google+OpenAI+Anthropic combined) OpenRouter share collapsed from ~70% in June 2025 to ~30% in June 2026**. Same source: DeepSeek commands 16.3% of all token volume (single highest provider); Chinese providers combined ~44% of top-10 token volume; DeepSeek V4 Flash led all models by token volume in June 2026; Chinese open-source models occupy six of the top ten spots.
  — SOURCE: https://officechai.com/ai/share-of-us-models-being-used-on-openrouter-has-collapsed-from-70-to-30-over-the-past-year/
- Jefferies analysis of OpenRouter data (cited by Business Today, June 2026): Chinese AI models processed **21.37 trillion tokens** in the week ended June 21 [2026], vs. **5.76 trillion tokens** for leading US models. Same piece: Zhipu's **GLM-5.2 costs roughly one-quarter the per-token price of Anthropic's leading systems**.
  — SOURCE: https://www.businesstoday.in/technology/artificial-intelligence/story/chinas-ai-price-war-is-exposing-indias-biggest-weakness-why-india-needs-its-own-deepseek-539573-2026-06-29
- **Vercel platform data**: open-weight models handled **nearly one-third of AI requests** on Vercel in June 2026. Separately, Rest of World reports DeepSeek's token share on Vercel jumped from under 1% to **17% by May 2026**, though its revenue share stayed near 1% (reflecting its much lower price per token).
  — SOURCE: https://techcrunch.com/2026/07/14/the-real-ai-race-may-no-longer-be-at-the-frontier-open-models-hugging-face/ ; — SOURCE: https://restofworld.org/2026/when-americans-choose-chinese-ai/

### a16z / enterprise adoption survey data

- Martin Casado, general partner at Andreessen Horowitz, in an interview with **The Economist (published August 21, 2025)**: **"I'd say 80% chance (they are) using a Chinese open-source model."**
  — SOURCE: https://officechai.com/ai/80-chance-that-startups-we-see-are-using-chinese-ai-models-andreessen-horowitz-partner/
- **Important clarification**: Casado subsequently clarified on X that the 80% figure referred to 80% of the roughly 20–30% of new applicants who run open-source models at all — not 80% of all startups a16z sees. That maps to roughly **16–24% of all startups** using a Chinese open model, not 80% of all startups.
  — SOURCE: https://officechai.com/ai/80-chance-that-startups-we-see-are-using-chinese-ai-models-andreessen-horowitz-partner/
- This 80% framing was picked up and, per HN commenters, arguably over-extended by other outlets/commentary (see Section B) without the clarifying context — flagging as a case where a soundbite outran its nuance.
  — SOURCE: https://news.ycombinator.com/item?id=48979269 (comment thread)

### Congressional/regulatory scrutiny as an adoption proxy

- **House Committee on Homeland Security** and the **House Select Committee on China** opened a joint investigation (announced April 2026) into corporate exposure to Chinese AI models, sending initial letters to **Cursor/Anysphere** (in the process of a reported $60B SpaceX acquisition) and **Airbnb** regarding their use of Chinese open models.
  — SOURCE: https://news.slashdot.org/story/26/07/09/1947218/lawmakers-probe-growing-use-of-chinese-ai-models-in-us-companies
- Committee chairman Andrew Garbarino: **"Chinese open-weight model can match leading U.S. models in vulnerability discovery,"** warning the "Chinese Communist Party is racing to close the gap in capabilities shaping cybersecurity."
  — SOURCE: https://news.slashdot.org/story/26/07/09/1947218/lawmakers-probe-growing-use-of-chinese-ai-models-in-us-companies
- Named companies reported adopting Chinese open models for cost reasons: **Lindy** (SF-based, switched from Anthropic to DeepSeek, "saving millions"), **Airbnb** (Qwen, Kimi), **Cursor/Anysphere** (Chinese open models in infrastructure). Lindy founder Flo Crivello and Coinbase's Brian Armstrong are named as publicly supportive of using Chinese models to cut costs.
  — SOURCE: https://restofworld.org/2026/when-americans-choose-chinese-ai/ ; — SOURCE: https://news.slashdot.org/story/26/07/09/1947218/lawmakers-probe-growing-use-of-chinese-ai-models-in-us-companies
- Illustrative cost quote (Rest of World, developer Stu Clott, on Chinese-model pricing): coding tasks that cost roughly **$10 on Claude cost under $0.50 on DeepSeek**.
  — SOURCE: https://restofworld.org/2026/when-americans-choose-chinese-ai/

### Broader context (Stanford AI Index 2026 — not open-weight-specific, but relevant baseline)

- China produced **30 "notable" AI models in 2025 vs. the US's 50**; the top-closed-model-vs-top-open-model performance gap widened to **3.3%** (from 0.5% in August 2024); the US–China top-model performance gap narrowed to **2.7%** (from 17.5–31.6% in May 2023); the US spends **23x more on private AI investment** than China (**$285.9B vs. $12.4B**).
  — SOURCE: https://thenextweb.com/news/stanford-ai-index-2026-china-us-performance-gap (Stanford HAI 2026 AI Index Report)
- Note: the report chapter itself (hai.stanford.edu) did not yield extractable percentage breakdowns on open-weight-specifically via WebFetch — the above figures are via TheNextWeb's summary of the same report, UNVERIFIED against the primary PDF directly.

---

## B. THE ANALYST DEBATE

### 1. Ben Thompson, Stratechery — "Who's Afraid of Chinese Models?" (published **July 20, 2026**)
— SOURCE: https://stratechery.com/2026/whos-afraid-of-chinese-models/

Core argument (opinion, Thompson's):
- Panic over Chinese models (triggered by Kimi K3) is overblown for the frontier labs specifically: Thompson argues Anthropic and OpenAI "will be fine" because compute scarcity currently gives them pricing power and they can "make it up in volume" as inference markets grow.
- Chinese strategy is to **"commoditize your complement"** — flooding the market with cheap/free open-weight intelligence to erode the moat and margins of US frontier labs, since intelligence itself (not tokens) is the actual commodity being competed on.
- Concrete pricing numbers cited: **Kimi K3 at $3/million input tokens, $15/million output tokens**, vs. Anthropic's "Sol" at **$5/million input, $30/million output**.
- Policy recommendation (his prescription, not a neutral fact): the US should **legalize distillation** ("bars terms of service that forbid distillation," make clear that "collecting data for training models is fair use") and **loosen Fable/Sol export restrictions specifically for cybersecurity use**, arguing current restrictions ironically leave US cyber-defenders dependent on Chinese models because they can't access the best US ones. Verbatim: **"the best defense — the only viable defense, in fact — will be to make sure defenders have access to the best models as well."**

### 2. Ben Werdmuller, werd.io — "American AI is locked down and proprietary. It's losing." (a.k.a. "China's open-weights AI strategy is winning" on Hacker News)
— SOURCE: https://werd.io/american-ai-is-locked-down-and-proprietary-its-losing/

Core argument (opinion, Werdmuller's):
- **"Open almost always wins when it comes to infrastructure adoption."** AI models have no durable technical moat beyond brand loyalty, so open distribution wins on ecosystem effects that centralized/closed services can't match.
- Cites the Casado/a16z **"80% chance"** startups-use-Chinese-models line (see Section A caveat above) as his headline evidence.
- U.S. export controls on GPUs are framed as **backfiring**: they stop Chinese firms from running centralized global cloud services, but open-weight distribution lets Chinese models bypass that limitation entirely via portability — anyone can download and self-host.
- Verbatim: **"Locked-down business practices for a technology with no real moat but significant potential ecosystem benefits is an obviously losing strategy."** and **"It's American companies that are keeping tight control of their technology rather than releasing it as openly as possible."**
- Economic-risk framing: **"If the bottom falls out of that spending — and I think it clearly will, given the dynamics — the outcome could be severe"** (referring to AI capex).

**On the "1114 points on HN" figure**: I directly fetched the Hacker News item page. As verified at time of this research, the thread shows **223 points and 193 comments** at https://news.ycombinator.com/item?id=48979269 (title on HN: "China's open-weights AI strategy is winning"). **I could not find or corroborate a figure of 1114 points anywhere** — flagging that specific number as **UNVERIFIED/likely inaccurate** as given in the brief; 223/193 is the actual verified reading. (Point counts can fluctuate with flags/vouches, but 223 is what direct fetch returned, sourced from a search-result URL, not hand-typed.)

Top HN comment themes (per direct fetch of the thread):
- Skepticism that the 80% Casado stat is being used without the clarifying context (eval use vs. production use).
- A recurring "developers use US frontier models for coding, Chinese models get shipped into cost-sensitive production features" split.
- Argument that adoption is cost-driven, not ideologically pro-open-source.
- Debate over whether Meta's Llama disproves the "open wins" thesis (open-sourced, but limited commercial payoff for Meta).
- Censorship debate: whether it's baked into weights vs. an API-layer-only filter, and whether that even matters for something you can self-host and modify.
  — SOURCE: https://news.ycombinator.com/item?id=48979269

### 3. The strongest counter-arguments in credible coverage

**Security / IP theft:**
- CSIS: OpenAI and Anthropic have **"accused Chinese labs (DeepSeek, Moonshot, and MiniMax) of stealing their products via 24,000 fraudulent accounts"** used to harvest outputs for distillation; CSIS also notes Chinese developers' "model security tests are more limited compared to U.S. models."
  — SOURCE: https://www.csis.org/analysis/what-know-about-chinese-ai-models
- The US Center for AI Standards and Innovation (CAISI) found **DeepSeek V4 Pro "about eight months behind the leading U.S. models"** — a benchmark-skepticism data point cutting against claims of parity.
  — SOURCE: https://www.csis.org/analysis/what-know-about-chinese-ai-models
- US State Department spokesperson, on the Congressional probe: **"AI models are designed to advance Beijing's narratives, censor dissent, and reflect CCP ideology."**
  — SOURCE: https://news.slashdot.org/story/26/07/09/1947218/lawmakers-probe-growing-use-of-chinese-ai-models-in-us-companies

**Censorship / propaganda baked into models (most concrete counter-evidence found):**
- A study funded by the **Swedish Psychological Defence Agency (published February 2026)**, alongside the **Estonian Foreign Intelligence Service's 2026 International Security Report** and non-profit auditor **Policy Genome**, tested 10 Chinese-model companies across 8 languages. Findings: **"None of the ten tested companies' models were completely free of Chinese information guidance."** Estonia's report found DeepSeek **"conceals key information and inserts Chinese propaganda into its answers"** on Estonia-security topics; on the Bucha atrocities, DeepSeek gave "vague acknowledgments" while adding "China has consistently supported peace and dialogue." Policy Genome found Russian-language DeepSeek responses **"endorsed Kremlin talking points or introduced misleading details"** while English versions were largely accurate. Internal directives were found instructing **Qwen** to keep answers about China **"positive and constructive, avoid criticism."**
  — SOURCE: https://cepa.org/article/chinese-ai-models-spread-propaganda-globally/
- Same source, an adoption data point: Alibaba's Qwen models logged **over 9.5 million downloads (Oct–Nov 2025)** and underpin roughly **2,800 derivative applications**.
  — SOURCE: https://cepa.org/article/chinese-ai-models-spread-propaganda-globally/

**Political/policy split inside the US (shows the debate isn't just China vs. US, it's US-internal too):**
- MIT Technology Review (July 20, 2026): Moonshot's free Kimi model has fractured Trump's AI advisors. Anton Leicht: Kimi poses **"a threat for an administration that really doesn't want more economic bad news."** David Sacks (former AI czar) criticized companies that **"want the government to eliminate their open source competition,"** i.e., arguing against banning Chinese open models to protect US commercial incumbents. Opposing camp (Pentagon-aligned, incl. Emil Michael) wants government vetting/control on national-security grounds; Michael reportedly called a rival advisor a "supreme village idiot" over the soft-power approach. Same piece flags the April 2026 Trump administration "crackdown" response to the distillation allegations above.
  — SOURCE: https://www.technologyreview.com/2026/07/20/1140675/chinas-ai-models-have-trumps-ai-world-at-war-with-itself/

**Ironic complication — China may restrict its own open-weight strategy:**
- China's Ministry of Commerce (MOFCOM) is **consulting Alibaba, ByteDance, and Zhipu/Z.ai** on export controls that could restrict **foreign/overseas access to advanced model weights** (Qwen, DeepSeek V4 Pro, GLM series, Kimi/Moonshot systems named as potentially affected), shifting future frontier releases toward API-only access for non-domestic users while older/already-released weights remain freely available (can't be un-released). **Not yet decided; no timeline set**, per reporting as of July 21–22, 2026. President Xi Jinping had called for countries to **"encourage open source, openness, collaboration and sharing"** at the World AI Conference (July 17, 2026), which ASPI analysts say referred to sharing AI resources broadly, not a commitment to keep releasing open weights.
  — SOURCE: https://www.techtimes.com/articles/321270/20260722/china-weighs-locking-ai-model-weights-download-what-you-use-right-now.htm

---

## C. THE INDIA ANGLE

### C1. Indian companies/startups building ON Chinese open-weight models — named examples

Real, sourced examples found (not invented):

- **Yotta Data Services' "myShakti"** — described as "India's first sovereign B2C GenAI chatbot," runs on an **open-source DeepSeek model**, hosted entirely on Yotta's **NM1 data center in India** (16 nodes / 128 Nvidia H100 GPUs), with all data processing kept on Indian servers. Launched **February 4, 2025**. Chairman & co-founder **Darshan Hiranandani**: **"Yotta has been committed to democratizing AI by making it accessible to every Indian while ensuring data sovereignty."** CEO **Sunil Gupta**: **"The integration of DeepSeek is a true game-changer—its open-source nature and low compute requirements drastically reduce costs, accelerating AI adoption."** Available in beta at myShakti.ai.
  — SOURCE: https://yotta.com/press-releases/yotta-launches-myshakti-indias-first-sovereign-b2c-gen-ai-chatbot-utilizes-deepseek-open-source-ai-model/
  — **Note**: I could not find a July 2026 update on myShakti's current user numbers/status; last confirmed status is the Feb 2025 launch. Flagging currency as unconfirmed rather than assuming it's still operating at the same scale.
- **Schmooze**, an Elevation Capital-backed Indian dating app, **uses Alibaba's Qwen models**. Quote from Schmooze's **Vidya Madhavan**: **"Our approach has been to use solutions from Google, OpenAI, Anthropic...then use a combination of open source plus our tuning to achieve the same outcome and save money."**
  — SOURCE: https://kr-asia.com/indian-companies-look-to-chinese-llms-as-ai-costs-bite (published July 21, 2026)
- More broadly, Business Standard (July 2026) reports Indian startups and enterprises currently **"utilize models from OpenAI, Anthropic, Google and Meta alongside China's Qwen and DeepSeek,"** selected case-by-case on capability, cost, and performance — i.e., mixed-stack adoption rather than exclusive reliance.
  — SOURCE: https://www.business-standard.com/technology/tech-news/china-ai-model-export-limit-us-anthropic-fable-5-claude-code-india-rethink-strategy-126070901378_1.html
- **Sridhar Vembu, founder of Zoho**, publicly advocates Indian firms embrace smaller/open models, stating organizations should adopt **"both Indian and Chinese open source ones."**
  — SOURCE: https://techcrunch.com/2026/06/13/as-anthropic-suspends-access-to-new-models-india-debates-its-ai-future/
- Cost comparison cited for the Indian market (KrAsia): DeepSeek via Microsoft Foundry runs **$0.19–1.74/million input tokens, $0.51–5.40/million output tokens**; Moonshot's Kimi up to **$0.95 input / $4 output per million tokens** — vs. OpenAI GPT-5.5 at **$5–12 input / $30–54 output per million tokens**.
  — SOURCE: https://kr-asia.com/indian-companies-look-to-chinese-llms-as-ai-costs-bite

**Explicitly NOT built on Chinese open-weight models** — worth stating clearly per the "don't invent examples" instruction:
- **Sarvam AI**'s February 2026 flagship release (30B and 105B parameter models, unveiled at the Delhi AI Impact Summit) was **"trained from scratch rather than fine-tuned on existing open source systems,"** per TechCrunch, using ~16 trillion tokens (30B model). No Chinese base model is mentioned anywhere in TechCrunch's or Business Standard's coverage of this release. Sarvam co-founder Pratyush Kumar said the 105B model **"performs well on most benchmarks"** and is **"cheaper than Google's Gemini Flash while outperforming it on several benchmarks."** Sarvam has raised **$40M+** from Lightspeed, Khosla Ventures, and Peak XV.
  — SOURCE: https://techcrunch.com/2026/02/18/indian-ai-lab-sarvams-new-models-are-a-major-bet-on-the-viability-of-open-source-ai/ ; — SOURCE: https://www.business-standard.com/technology/tech-news/india-ai-impact-summit-2026-sovereign-models-sarvam-bharatgen-gnani-126021900417_1.html
  — Note: Sarvam's *earlier* efforts (its OpenHathi project and SarvamM model, pre-2026) were separately reported to adapt Meta's Llama and Mistral bases — https://restofworld.org/2026/india-frugal-ai-sarvam-krutrim-sovereign/ — again, no Chinese base model reported for Sarvam at any point in its history across either source.
- **Krutrim** (Ola founder Bhavish Aggarwal's AI venture) is reported to train its own models (2 trillion tokens, 22 Indian languages) rather than fine-tune a Chinese base; TechCrunch separately notes Krutrim has "shifted to cloud services" as a business pivot.
  — SOURCE: https://restofworld.org/2026/india-frugal-ai-sarvam-krutrim-sovereign/ ; — SOURCE: https://techcrunch.com/2026/06/13/as-anthropic-suspends-access-to-new-models-india-debates-its-ai-future/
- **BharatGen's Param2** (17B multilingual MoE, one of the 3 sovereign models unveiled at the Feb 2026 Delhi summit) was built **in partnership with Nvidia** using Nvidia's AI software stack — no Chinese base model mentioned. **Gnani.ai's Vachana** (TTS/voice-cloning, 12 Indian languages, MOS 4.23) is likewise not reported as China-based.
  — SOURCE: https://www.business-standard.com/technology/tech-news/india-ai-impact-summit-2026-sovereign-models-sarvam-bharatgen-gnani-126021900417_1.html

### C2. Indian government stance — chronology (DeepSeek advisories and current status)

- **January 30, 2025**: India **approved hosting DeepSeek's models on domestic servers** — described by TechCrunch as "a rare opening for Chinese technology in India" — contingent on data-localization. IT Minister **Ashwini Vaishnaw**: **"You have seen what DeepSeek has done — $5.5 million and a very, very powerful model,"** and **"Data privacy issues regarding DeepSeek can be addressed by hosting open source models on Indian servers."** This is tied to India's new AI Compute Facility (18,693 GPUs, ~13,000 Nvidia H100s + ~1,500 H200s, ~10,000 ready for immediate deployment).
  — SOURCE: https://techcrunch.com/2025/01/30/india-to-host-china-deepseek-ai-model-locally-in-rare-tech-approval
- **February 5, 2025**: India's **Finance Ministry** directed officers not to use "AI tools and AI apps (such as ChatGPT, DeepSeek etc)" on office computers/devices, stating: **"It has been determined that AI tools and AI apps (such as ChatGPT, DeepSeek etc) in the office computers and devices pose risks for confidentiality of Govt, data and documents."** Scoped to Finance Ministry officers' official devices only, citing cross-border data-transfer/confidentiality risk. Comparable restrictions cited in Australia, Italy, and Taiwan around the same period.
  — SOURCE: https://inc42.com/buzz/finance-ministry-asks-employees-to-not-use-chatgpt-deepseek-report/
- **April 11, 2025**: Asked directly whether India was considering a TikTok-style ban on DeepSeek, External Affairs Minister **S. Jaishankar**, at the 9th Carnegie Global Tech Summit: **"I will be deeply evasive about the answer. My honest answer is, I don't think at this time there is any determination."**
  — SOURCE: https://www.tribuneindia.com/news/world/i-dont-think-there-is-any-determination-eam-jaishankar-on-possibility-of-ban-on-deepseek/amp
- **March 2025** (per Medianama's later summary): the Centre told Parliament **"there was no blanket ban on AI tools in government offices,"** with guidance instead to use only "approved AI platforms for sensitive work."
  — SOURCE: https://www.medianama.com/2026/07/223-government-asks-ministries-pause-deployment-openai-anthropic-ai-models/
- Separately, a **Congress MP publicly demanded a ban on DeepSeek** — headline-level finding only (not deep-fetched); flagging as reported but not independently expanded here.
  — SOURCE: https://www.deccanherald.com/india/congress-mp-demands-ban-on-chinese-ai-app-deepseek-3441653
- **Current status, as reported in July 2026**: No blanket Indian government ban on DeepSeek or other Chinese open models has been enacted, based on everything found in this research. The most recent related story is actually about the *opposite* direction — MeitY reportedly (per ThePrint, relayed by Medianama, **dated July 2026**) advised ministries to **pause deployment of OpenAI and Anthropic models** "for cybersecurity and related functions for now" — which the Press Information Bureau (PIB) then **denied**, stating on X that MeitY had **"not issued any such direction or advisory prohibiting Ministries from using OpenAI or Anthropic."** This is about US models, not Chinese ones, but shows the government's vendor-diversification/security posture is live and contested as of this month. **Disputed/UNVERIFIED authenticity** per PIB's denial.
  — SOURCE: https://www.medianama.com/2026/07/223-government-asks-ministries-pause-deployment-openai-anthropic-ai-models/
- Adding to the current-month complexity: China's own potential export restrictions on model weights (Section B) could, if enacted, **cut off Indian companies' access to Qwen/DeepSeek/GLM** just as US restrictions (Anthropic's Fable 5/Mythos 5 suspension for foreign nationals, restored July 1, 2026 after a Commerce Department dispute) already created a wobble in Indian firms' access to US frontier models — squeezing India from both sides and re-energizing the sovereign-AI argument.
  — SOURCE: https://www.digit.in/news/general/china-may-restrict-access-to-its-ai-models-for-indian-users-here-is-why.html ; — SOURCE: https://www.business-standard.com/technology/tech-news/china-ai-model-export-limit-us-anthropic-fable-5-claude-code-india-rethink-strategy-126070901378_1.html

### C3. IndiaAI Mission — sovereign-model push, funding, and status (July 2026)

- **Total programme funding: Rs 10,371.92 crore (~$1.25 billion)**; **Rs 4,563.36 crore earmarked for compute infrastructure** over five years.
  — SOURCE: https://www.abhs.in/blog/indiaai-mission-34000-gpus-cheap-compute-developers-2026
- **GPU capacity**: 34,000 GPUs currently available under the Mission, with a target of **100,000 GPUs by end of 2026**. Pricing: standard GPUs at **Rs 115.85/GPU-hour**, H100-class at **Rs 150/GPU-hour** — described as "roughly 42% below market rates," with eligible projects getting up to 40% additional subsidy (effective rate below Rs 100/hour). Chennai facility: 30 MW operational; Mumbai facility: 40 MW planned.
  — SOURCE: https://www.abhs.in/blog/indiaai-mission-34000-gpus-cheap-compute-developers-2026
- **Three sovereign AI models were unveiled at the India AI Impact Summit in Delhi (dated around February 19, 2026)**: Sarvam AI's 30B/105B LLMs, Gnani.ai's Vachana (voice cloning TTS across 12 Indian languages), and BharatGen's Param2 (17B multilingual MoE, built with Nvidia). Sarvam is described as the **first startup selected under the IndiaAI Mission programme**.
  — SOURCE: https://www.business-standard.com/technology/tech-news/india-ai-impact-summit-2026-sovereign-models-sarvam-bharatgen-gnani-126021900417_1.html ; — SOURCE: https://www.abhs.in/blog/indiaai-mission-34000-gpus-cheap-compute-developers-2026
- **Scale-up proposal (not yet enacted)**: Investor and former Infosys executive **Mohandas Pai** proposed a **₹500 billion (~$5B) annual AI fund** plus a **₹2 trillion (~$21B) credit guarantee** for AI infrastructure — a figure he explicitly frames as dwarfing the existing ~₹103.72 billion IndiaAI Mission. This followed the Anthropic Fable 5/Mythos 5 access suspension for foreign nationals in June 2026, which Activate AI founder **Aakrit Vaish** said **"completely changes things... this materially changes the way all of us should be thinking about sovereign AI in India."**
  — SOURCE: https://techcrunch.com/2026/06/13/as-anthropic-suspends-access-to-new-models-india-debates-its-ai-future/
- Additional named voices from the same TechCrunch piece: **Vijay Rayapati** (Atomicwork CEO) warns teams with non-US citizens face disadvantages when frontier access is geopolitically gated. **Prasanto Roy** (policy expert): **"American AI models are bound to American geopolitics."** Anthropic and OpenAI reportedly regard **India as their second-largest market**.
  — SOURCE: https://techcrunch.com/2026/06/13/as-anthropic-suspends-access-to-new-models-india-debates-its-ai-future/

### C4. Data-privacy dimension — hosted Chinese apps vs. self-hosted open weights

- The core legal distinction found: **using DeepSeek's own hosted app/API means data is processed on China-based servers** (Estonian intelligence framing: DeepSeek "transfers personal data to 'Chinese data processors' and stores it on servers in China" — per IAPP, partially paywalled) — **vs. self-hosting the open-weight model on domestic infrastructure**, which is exactly what Yotta's myShakti and India's Jan 2025 "host DeepSeek on Indian servers" approval both do, keeping data within Indian jurisdiction.
  — SOURCE: https://iapp.org/news/a/deepseek-and-the-china-data-question-direct-collection-open-source-and-the-limits-of-extraterritorial-enforcement (partial/gated) ; — SOURCE: https://yotta.com/press-releases/yotta-launches-myshakti-indias-first-sovereign-b2c-gen-ai-chatbot-utilizes-deepseek-open-source-ai-model/
- Indian law-firm analysis (S&R Associates) states the distinction directly: **"If an LLM is available on an open-source basis (such as Deepseek's models), future deployers can implement the required safeguards themselves"** — i.e., the open-weight/self-hosting route is explicitly framed as a way to sidestep the China-data-transfer risk that using DeepSeek's own hosted chatbot carries. Regulatory analysis is framed around India's **DPDP Act** treating chatbot operators as "data fiduciaries," regardless of deployment location — the piece does **not** fully resolve whether self-hosted deployments face different compliance obligations than hosted ones; flagged as a gap in current legal clarity, not a settled answer.
  — SOURCE: https://www.snrlaw.in/indias-concerns-about-deepseek-and-possible-regulatory-responses/
- Regional comparison point: **Taiwan banned Chinese AI systems, including DeepSeek, from government use over security risks** (reported November 20, 2025) — offered as a contrast to India's approach of approving *local hosting* of DeepSeek rather than banning it outright.
  — SOURCE: https://www.newsonair.gov.in/taiwan-bans-chinese-ai-systems-in-government-over-security-risks

---

## Real user questions seen

Actual question-style phrasings encountered in article titles, headlines, and reported quotes during this research (i.e., what real search/reader intent looks like on this topic right now):

- "Is Deepseek Banned In India?" — https://openaimaster.com/is-deepseek-banned-in-india/
- "Is DeepSeek Banned in India? Current Status for Users and Businesses" — https://chat-deep.ai/privacy-security/is-deepseek-banned-in-india/
- "Are Chinese AI Models Safe? Data, Privacy & Censorship (2026)" — https://pickurai.ai/ai-industry/are-chinese-ai-models-safe
- "Is DeepSeek Safe to Use in 2026?" — https://lumichats.com/blog/is-deepseek-safe-to-use-2026-usa
- "Is DeepSeek safe to use? Chat vs. R1 explained" — https://surfshark.com/blog/is-deepseek-safe
- "Are Chinese AI Models Risky?" — https://www.rickmanelius.com/p/are-chinese-ai-models-risky
- "DeepSeek vs Qwen: Which AI Model Should You Use in 2026?" — https://chat-deep.ai/comparison/qwen/
- "China may restrict access to its AI models for Indian users: Here is why" — https://www.digit.in/news/general/china-may-restrict-access-to-its-ai-models-for-indian-users-here-is-why.html
- "Which countries have banned DeepSeek and why?" — https://www.aljazeera.com/news/2025/2/6/which-countries-have-banned-deepseek-and-why
- A journalist directly asking EAM Jaishankar "whether the Indian government was considering banning the Chinese AI platform DeepSeek (similar to the TikTok ban)" at the 9th Carnegie Global Tech Summit, April 11, 2025 — https://www.tribuneindia.com/news/world/i-dont-think-there-is-any-determination-eam-jaishankar-on-possibility-of-ban-on-deepseek/amp
- "Congress MP demands ban on Chinese AI app DeepSeek" (implicit "should DeepSeek be banned in India" framing) — https://www.deccanherald.com/india/congress-mp-demands-ban-on-chinese-ai-app-deepseek-3441653

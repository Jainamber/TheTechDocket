# Research Notes: EU AI Act — What Legally Changed on 2 August 2026 (Primary-Source Fact Check)

Compiled 2026-08-03. Mission: nail down, from primary sources, exactly what became applicable/enforceable on 2 Aug 2026 under the EU AI Act, and what is delayed (Digital Omnibus). Method: WebSearch first, then WebFetch on returned URLs. Two EC presscorner fetches (ec.europa.eu/commission/presscorner) returned metadata-only (JS-rendered page/ROBOTS_DISALLOWED on retry); content recovered via digital-strategy.ec.europa.eu mirror (same EC text) and independent syndication mirrors (pubaffairsbruxelles.eu, ieu-monitoring.com — both reproduce the EC release near-verbatim). zpravy.kurzy.cz fetch blocked by robots.txt. All figures below are cross-checked across ≥2 sources except where flagged UNVERIFIED/SINGLE-SOURCE.

---

## HEADLINE ANSWER (read this first)

2 August 2026 is the EU AI Act's **general application date** (Art. 113 chapeau: "It shall apply from 2 August 2026"). On this date: (1) the Commission's AI Office + national authorities **formally began enforcement** of the whole Regulation; (2) **Article 50 transparency rules** (chatbot disclosure, deepfake labelling, AI-content marking) became legally live; (3) the Commission's **own enforcement/investigation/fining powers over GPAI providers (Article 101)** switched on, ending GPAI providers' one-year "supervision-free" adjustment period (substantive GPAI duties themselves have applied since 2 Aug 2025). **What did NOT happen on 2 Aug 2026: high-risk Annex III obligations did not go live.** The "Digital Omnibus on AI" was fully adopted and is already in force as law (Regulation (EU) 2026/1744, in force since 27 July 2026) and it pushed stand-alone high-risk (Annex III) obligations to **2 December 2027** and product-embedded high-risk (Annex I/Art. 6(1)) obligations to **2 August 2028**. This is not a "proposal" or "political agreement" anymore as of 2 Aug 2026 — it is enacted, published, in-force EU law.

---

## Q1: What became applicable/enforceable on 2 Aug 2026 — precisely which obligations?

- **General application date confirmed**: Article 113 of Regulation (EU) 2024/1689, quoted verbatim from the European Commission's own AI Act Service Desk: *"This Regulation shall enter into force on the twentieth day following that of its publication in the Official Journal of the European Union. It shall apply from 2 August 2026. However: (a) Chapters I and II shall apply from 2 February 2025; (b) Chapter III Section 4, Chapter V, Chapter VII and Chapter XII and Article 78 shall apply from 2 August 2025, with the exception of Article 101; (c) Article 6(1) and the corresponding obligations in this Regulation shall apply from 2 August 2027."* (ai-act-service-desk.ec.europa.eu — NOTE: this is the ORIGINAL 2024 text; see "Discrepancy" note below on whether the service-desk page itself has been updated post-Omnibus.) (ec.europa.eu / ai-act-service-desk.ec.europa.eu)
  - Reading this: everything not specifically carved out by (a)/(b)/(c) — which includes the Annex III high-risk chapters (Chapter III Sections 1–3) — falls under the general "2 August 2026" chapeau. That is *why* 2 Aug 2026 was originally the high-risk trigger date, and why the Digital Omnibus had to specifically legislate a new date for it (see Q3).
- **Enforcement itself begins**: EC press release/mirror, verbatim: *"From 2 August 2026, the European Commission's AI Office, together with national authorities, will begin enforcing the Artificial Intelligence (AI) Act."* (digital-strategy.ec.europa.eu, mirroring ec.europa.eu/commission/presscorner/detail/en/ip_26_1714)
- **Transparency rules (Article 50) go live**, verbatim: *"On the same date, new transparency rules will start to apply, requiring certain AI systems to tell users when they are interacting with AI and when content has been generated or altered by it."* (digital-strategy.ec.europa.eu)
  - Specific Art. 50 duties now legally binding (full verbatim text pulled from artificialintelligenceact.eu, a text-mirror source; corroborated by digital-strategy.ec.europa.eu FAQ):
    - **Art. 50(1)** — providers of AI systems designed to interact directly with people must ensure people are told they're interacting with an AI, "unless this is obvious." Carve-out for law-enforcement-authorised systems.
    - **Art. 50(2)** — providers of AI (incl. GPAI systems) generating synthetic audio/image/video/text must mark outputs in a machine-readable, detectable format. Carve-out for assistive/standard-editing functions that don't substantially alter input.
    - **Art. 50(3)** — deployers of emotion-recognition or biometric-categorisation systems must inform exposed individuals, per GDPR/EUDPR/LED.
    - **Art. 50(4)** — deployers of deepfake-generating/manipulating systems must disclose the content is artificial ("upon first exposure at the latest"); lighter-touch disclosure for evidently artistic/satirical work. Separately, deployers of AI-generated/manipulated **text on matters of public interest** must disclose this unless it underwent human editorial review with a named responsible party.
    - **Art. 50(5)** — disclosure must be clear, distinguishable, and given at latest at first interaction/exposure; must meet accessibility requirements.
  - **Grace period nuance (important, often confused in coverage)**: Art. 50(2) marking obligation itself is not deferred — but Regulation (EU) 2026/1744's Recital 38 gives a **4-month transitional period** for systems/content **already placed on the market before 2 Aug 2026**, i.e. practical full-compliance deadline **2 December 2026**. New systems placed on market from 2 Aug 2026 onward must comply immediately. (eur-lex.europa.eu — Regulation 2026/1744 full text; corroborated by compliancehub.wiki and Gibson Dunn coverage citing the same 2 Dec 2026 date)
- **High-risk Annex III obligations did NOT go live on 2 Aug 2026** — deferred to 2 Dec 2027 by the Digital Omnibus (see Q3). Multiple sources (Freshfields, Gibson Dunn, compliancehub.wiki, fpf.org, EUR-Lex Recital 40) agree.
- **Enforcement/supervisory architecture split**, verbatim from EC-release mirrors: the **AI Office** enforces rules for GPAI model providers and for AI systems offered by GPAI providers or integrated into very large online platforms; **national competent authorities** enforce for other AI systems; the **European Data Protection Supervisor (EDPS)** oversees AI systems used by EU institutions/bodies/agencies. (pubaffairsbruxelles.eu and ieu-monitoring.com, both mirroring the EC release)
- **Support/reporting infrastructure now operating**: AI Act **Complaints Tool**, a confidential **Whistleblower Tool**, and a dedicated **complaints channel for downstream providers** to flag issues with upstream GPAI model providers. A **60-member Scientific Panel** of independent AI experts supports enforcement; **Prof. Alessandro Abate (Oxford)** is named Lead Scientific Adviser. (digital-strategy.ec.europa.eu; pubaffairsbruxelles.eu; ieu-monitoring.com)
- **Code of Practice on Transparency of AI-generated Content**: EC-run voluntary code supporting Art. 50 compliance. Official EC page confirms: *"By the end of July 2026, about 190 companies organisations have signed the code."* Timeline per same EC page: kick-off 5 Nov 2025 → first draft 17 Dec 2025 → second draft 3 Mar 2026 → final code published 10 June 2026. Code adherence is voluntary; *"the transparency requirements under article 50 of the AI Act are legal obligations"* regardless. (digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) — NOTE: the EC press-release mirrors say "over 180" signatories; the EC's own dedicated CoP page says "about 190" as of end-July 2026 — treat ~180–190 as the range, both EC-sourced, likely just different snapshot dates.
- **National authorities / member-state readiness — UNVERIFIED at precise 2 Aug 2026 count, but incomplete on available evidence**: Article 70 required member states to designate national competent authorities by 2 Aug 2025. Secondary-source snapshots found: **8 of 27** member states had done so as of ~25 Mar 2026 (aiacto.eu, quoting "only 8 member states out of 27 met that deadline"); **17 of 27** as of a ~July 2026 roundup (cubbbix.com — flagged lower-confidence, see Discrepancies below). No EC-official count as of exactly 2 Aug 2026 was found — **mark exact current count UNVERIFIED**. This is directly relevant to "member-state penalties/national authorities" in the question: enforcement uniformity across the bloc is not guaranteed even though the legal obligation and the AI Office's own (direct) GPAI enforcement power are unaffected by member-state designation delays.
- **Regulatory sandboxes**: Article 57 originally required each member state to have at least one national AI regulatory sandbox operational by 2 Aug 2026. The Digital Omnibus pushed this to **2 August 2027** (fpf.org comparison table, and Gibson Dunn/compliancehub coverage); i.e. this is a second deadline that did *not* land on 2 Aug 2026 despite being widely listed as an original Art. 113-general-date item.

---

## Q2: GPAI — obligations since 2 Aug 2025 vs. Commission ENFORCEMENT powers/fines from 2 Aug 2026

- **What applied from 2 Aug 2025** (Chapter V substantive duties, per Art. 113(b)): GPAI model providers must maintain technical documentation, provide information to downstream providers, adopt a copyright-compliance policy, and publish a publicly available summary of training content (Arts. 53, 55); providers of GPAI models with **systemic risk** face added duties (adversarial testing, serious-incident reporting, model evaluation, cybersecurity). (digital-strategy.ec.europa.eu GPAI FAQ; artificialintelligenceact.eu Chapter V page)
- **What is new/switched on 2 Aug 2026 — the Commission's ENFORCEMENT power specifically**: Article 113(b) *explicitly excepts Article 101* from the 2 Aug 2025 application date, meaning Article 101 (Commission fines on GPAI providers) falls under the **general 2 Aug 2026** date, not the earlier GPAI-obligations date. Direct quote from artificialintelligenceact.eu's Chapter V enforcement page: *"the providers are given an adjustment period of one year before the Commission may start exercising its supervision and enforcement powers."* (artificialintelligenceact.eu/enforcement-of-chapter-v-under-the-eu-ai-act/)
  - This is corroborated independently by a secondary news source (techtimes.com, citing an EC official quote from 31 July 2026 re: OpenAI/Anthropic contacts) framing 2 Aug 2026 as when *"the European Commission gains authority to investigate GPAI providers, mandate corrective actions, and levy fines"* — and by spacedaily.com's framing: *"the European Union's rulebook for artificial intelligence stops being a set of deadlines on paper and starts having teeth"* on 2 Aug 2026, marking *"the end of a one-year grace period."*
  - **Commission's exclusive enforcement powers (Article 88)** include: Article 91 information requests (providers may not supply "incorrect, incomplete or misleading information"); Article 92 evaluations of compliance/systemic risk, with independent-expert assistance; Article 93 corrective measures including requiring risk mitigation or market withdrawal/recall. (artificialintelligenceact.eu Chapter V page)
- **Fine amount (Article 101)**, verbatim from the EC's own AI Act Service Desk: the Commission may fine GPAI providers **"3 % of their annual total worldwide turnover in the preceding financial year or EUR 15 000 000, whichever is higher."** Process safeguard: *"the Commission shall communicate its preliminary findings to the provider of the general-purpose AI model and give it an opportunity to be heard"*; fines reviewable by the Court of Justice. (ai-act-service-desk.ec.europa.eu/en/ai-act/article-101)
- **Two-tier GPAI system** (context, secondary source spacedaily.com, UNVERIFIED precise figures beyond what's stated): all GPAI providers must publish a training-data summary via mandatory template updated every six months; providers of **systemic-risk** models (compute > 10^25 FLOPs, per Art. 51) face the heavier duties above. Per techjacksolutions.com (citing "Epoch AI's April 2026 Frontier Compute Report," single-source, flag as such): **12 models** currently exceed the 10^25 FLOP threshold, naming OpenAI/Google/Anthropic/Meta/Mistral as "representative, not exhaustive" of labs in scope. **Mark the "12 models" figure UNVERIFIED/single-secondary-source** — not confirmed by an EC primary source in this research pass.
- **Discrepancy flagged**: One EC-FAQ WebFetch summary (digital-strategy.ec.europa.eu GPAI FAQ page) rendered as *"Powers became effective with the obligations on 2 August 2025"* — this appears to **conflict** with the explicit Art. 113(b) carve-out text ("with the exception of Article 101") and with every other source consulted (artificialintelligenceact.eu, techtimes.com, spacedaily.com), all of which place Commission enforcement/fining power at 2 Aug 2026. Treating the Art. 113(b) statutory text (directly quoted from an EC source) plus the multi-source corroboration as controlling; **flagging the single conflicting FAQ paraphrase as likely a summarization artifact, not to be relied on.**

---

## Q3: Digital Omnibus / "stop-the-clock" — exact legal status as of 2 Aug 2026

**THIS IS NOW ENACTED LAW, NOT A PROPOSAL.** Confirmed directly via EUR-Lex:

- **Official citation** (eur-lex.europa.eu/eli/reg/2026/1744/oj/eng, fetched directly): *"Regulation (EU) 2026/1744 of the European Parliament and of the Council of 8 July 2026 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 as regards the simplification of the implementation of harmonised rules on artificial intelligence (Digital Omnibus on AI)"*
- **Legislative timeline** (cross-checked, Council + Freshfields + lawandtechnology.eu):
  - Political agreement: 6–7 May 2026 (Council/Parliament negotiators), confirmed by member-state representatives 13 May 2026
  - European Parliament vote: 16 June 2026
  - **Council final adoption ("final green light")**: **29 June 2026** — official Council source, verbatim: *"Given that provisions on high-risk AI systems were due to enter into force on 2 August 2026, the co-legislators treated this part of the package with utmost priority."* (consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/)
  - Signed: 8 July 2026
  - **Published in Official Journal: 24 July 2026** (lawandtechnology.eu, confirmed via EUR-Lex URL structure)
  - **Entry into force: 27 July 2026** (third day after publication — both eur-lex.europa.eu direct fetch and lawandtechnology.eu agree)
- **Conclusion for Q3**: as of 2 Aug 2026, the Digital Omnibus is fully in force, adopted EU law — it is **not** still "pending," "proposed," or merely a "political agreement." Any coverage describing it as such as of Aug 2026 is out of date (some secondary sources found in this search — e.g., Gibson Dunn's piece and an early compliancehub.wiki draft — still carried "expected adoption" language, apparently written before the 29 June/8 July/24 July milestones landed; **treat those specific "expected" framings as stale, superseded by the Council/EUR-Lex primary sources above**).

### Exactly which deadlines were deferred, and to when (source: EUR-Lex Regulation 2026/1744 Recitals 38 & 40, direct fetch; cross-checked against Freshfields, Gibson Dunn, compliancehub.wiki, fpf.org)

| Provision | Original date | New date | Source |
|---|---|---|---|
| Stand-alone high-risk AI systems (Art. 6(2) + Annex III — e.g. employment, credit scoring, education, law enforcement, migration/border, biometrics) | 2 Aug 2026 | **2 December 2027** | EUR-Lex Reg. 2026/1744 Recital 40 (direct); Freshfields; Gibson Dunn; compliancehub.wiki; fpf.org |
| High-risk AI embedded in regulated products (Art. 6(1) + Annex I — e.g. machinery, medical devices, toys, lifts, aviation) | 2 Aug 2027 (NOT 2026 — original Art. 113(c) already set this at 2027) | **2 August 2028** | EUR-Lex Reg. 2026/1744 Recital 40 (direct); ai-act-service-desk.ec.europa.eu Art. 113 (confirms original 2027 baseline); Gibson Dunn; compliancehub.wiki |
| AI regulatory sandboxes (Art. 57), ≥1 per member state | 2 Aug 2026 | **2 August 2027** | fpf.org (direct quote: "Member States must ensure that their competent authorities establish at least one AI regulatory sandbox, operational by this date" [2 Aug 2027]); compliancehub.wiki; Gibson Dunn |
| Art. 50(2) marking, for systems/content already on market pre-2 Aug 2026 | 2 Aug 2026 | **2 December 2026** (4-month transition; new deployments still bound from 2 Aug 2026) | EUR-Lex Reg. 2026/1744 Recital 38 (direct) |
| New prohibition: AI-generated/manipulated non-consensual intimate imagery + CSAM (new Art. 5 ground) | n/a — newly added by the Omnibus | **2 December 2026** | Freshfields; compliancehub.wiki; Gibson Dunn (penalty for breach: up to €35M/7% global turnover, i.e. treated as an Art. 5 prohibited-practice tier) |

- **Unchanged by the Omnibus**: Article 50 transparency obligations (core disclosure duties) — direct quote, Gibson Dunn: *"The Article 50 transparency obligations for AI systems largely remain on the original schedule."* Also unchanged: the general 2 Aug 2026 application date itself (Art. 113 chapeau untouched); GPAI Chapter V duties/dates; the AI Office's operational status; the Article 99/101 penalty ceilings (amounts not altered by this Omnibus, per research pass — no source found claiming otherwise).
- **Other Omnibus changes** (context, lower priority for this brief): AI-literacy duty (Art. 4) softened from a "guarantee" to a "support the development of" standard (Gibson Dunn); simplified Annex IV technical-documentation template extended to small mid-cap companies, not just SMEs (fpf.org).
- **Discrepancy flagged**: The EC's own official timeline page (ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act), fetched directly on 3 Aug 2026, still describes 2 Aug 2026 as the date "high-risk AI systems rules activate" and 2 Aug 2027 as when "rules for high-risk AI embedded in regulated products apply" — i.e., it reads as the **pre-Omnibus** timeline, not reflecting the Dec 2027/Aug 2028 dates confirmed directly in the Official Journal text. This looks like an EC webpage that has not yet been updated to reflect Regulation 2026/1744 (which only entered into force 27 July 2026, six days before this fetch) — **flagging this explicitly since it's exactly the kind of "official but stale" trap that could mislead a fact-checker relying on that one EC page alone.** Treat the EUR-Lex Regulation 2026/1744 primary text (which we fetched directly, containing the actual amending recitals) as authoritative over this apparently-unrefreshed EC timeline widget.

---

## Q4: The EC statement dated ~1–2 Aug 2026 announcing enforcement start

- **Primary release**: European Commission press release, titled **"Commission starts enforcing AI Act rules and new transparency requirements on 2 August"** — URL: https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1714 (reference IP_26_1714). Mirrored in full at https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august and as a dated post at https://commission.europa.eu/news-and-media/news/safer-and-more-transparent-ai-2026-08-02_en ("Safer and more transparent AI," dated 2026-08-02). NOTE: direct WebFetch of the ec.europa.eu/commission/presscorner URL returned only page metadata (JS-rendered body not captured by the fetch tool) both times it was tried; the quotes below are recovered from the digital-strategy.ec.europa.eu mirror (identical EC-authored text) and independent syndication mirrors that reproduce the release.
- **Key lines, verbatim**:
  - *"From 2 August 2026, the European Commission's AI Office, together with national authorities, will begin enforcing the Artificial Intelligence (AI) Act."*
  - *"On the same date, new transparency rules will start to apply, requiring certain AI systems to tell users when they are interacting with AI and when content has been generated or altered by it."*
  - Interactive systems (chatbots) "must disclose their artificial nature to users rather than posing as humans"; deepfakes (images/video/audio) "require labeling"; AI-generated/modified content must carry "detectable technical markers."
  - Enforcement split confirmed again here: AI Office → GPAI providers + systems bundled with GPAI models or integrated into very large online platforms; national competent authorities → other AI systems; EDPS → EU-institution systems. (pubaffairsbruxelles.eu / ieu-monitoring.com mirrors)
  - Governance detail: 60-member Scientific Panel; Lead Scientific Adviser Prof. Alessandro Abate (Oxford); Complaints Tool, Whistleblower Tool, downstream-provider complaints channel all live. (same mirrors)
  - ~180–190 organisations signed the Code of Practice on Transparency of AI-generated Content (see Q1 for the two slightly different EC-sourced figures/dates).
- **Quote attributed to Commissioner Henna Virkkunen** (EVP for Tech Sovereignty, Security and Democracy) — **SINGLE-SOURCE, via techtimes.com, not independently confirmed against the EC release text itself; flag as UNVERIFIED-PRIMARY-ATTRIBUTION**: *"As enforcement begins, we are taking an important step towards AI that people and businesses can understand and trust."*
- **Adjacent, separately-sourced color (single-source, techtimes.com, NOT an EU institutional source — flag clearly as unverified/tangential)**: an EC official is quoted (31 July 2026) saying of contacts with OpenAI and Anthropic over reported incidents, *"We have been informed by the two providers of incidents bilaterally before they become public. We are in contact with them."* The same article's specific incident claims (an OpenAI model allegedly escaping an evaluation sandbox; Anthropic evaluation runs allegedly touching production systems) and its Tier-3-penalty figure of "1.5%" (which **contradicts** the EC's own Article 99(5) text of **1%**, see Q6) were **not corroborated by any other source in this research pass — treat as UNVERIFIED / possibly inaccurate, do not publish the 1.5% figure or the incident specifics as fact without independent confirmation.**

---

## Q5: Timeline table (every row sourced)

| Date | What applies/happens | Legal basis | Source(s) |
|---|---|---|---|
| 1 Aug 2024 | AI Act enters into force (published in OJ; 20-day-after-publication rule) | Art. 113 opening clause | digital-strategy.ec.europa.eu; ai-act-service-desk.ec.europa.eu |
| 2 Feb 2025 | Chapters I–II apply: general provisions, definitions, AI-literacy duty, and **Art. 5 prohibited practices** (manipulation, exploitation of vulnerabilities, social scoring, some predictive-policing, untargeted facial-recognition scraping, emotion recognition at work/school, biometric categorisation by sensitive attribute, real-time remote biometric ID in public by law enforcement, subject to exceptions) | Art. 113(a) | ai-act-service-desk.ec.europa.eu (Art. 113 text); digital-strategy.ec.europa.eu overview |
| 2 Aug 2025 | Chapter III Section 4 (notified bodies), **Chapter V (GPAI obligations)**, Chapter VII (governance: AI Office, AI Board, Scientific Panel), Chapter XII (penalties framework) *except Art. 101*, and Art. 78 (confidentiality) apply. Member states were due to have designated national competent authorities (Art. 70) by this date. | Art. 113(b) | ai-act-service-desk.ec.europa.eu (Art. 113 text); digital-strategy.ec.europa.eu GPAI FAQ |
| **2 Aug 2026** | **General application date** for the remainder of the Regulation not otherwise carved out: enforcement of the whole Act begins (AI Office + national authorities); **Art. 50 transparency duties go live**; Commission's **Art. 101 GPAI enforcement/fining power** switches on (ending the 1-yr adjustment period). Annex III high-risk obligations, which would otherwise have defaulted to this date under the Art. 113 chapeau, are **deferred** by Regulation 2026/1744 (see next rows). Sandboxes deadline (Art. 57) also deferred off this date. | Art. 113 chapeau; Reg. (EU) 2026/1744 | ec.europa.eu/commission/presscorner/ip_26_1714; digital-strategy.ec.europa.eu; eur-lex.europa.eu Reg. 2026/1744 |
| 2 Dec 2026 | New Art. 5 prohibition on AI-generated non-consensual intimate imagery/CSAM takes effect; Art. 50(2) marking transition period ends for pre-2 Aug 2026 systems (full compliance required) | Reg. (EU) 2026/1744, Recitals 38/new Art. 5 provision | eur-lex.europa.eu Reg. 2026/1744; Freshfields; compliancehub.wiki |
| 2 Aug 2027 | AI regulatory sandboxes (≥1 per member state) now required to be operational (deferred 1 year from original 2 Aug 2026 date) | Reg. (EU) 2026/1744 amending Art. 57 timeline | fpf.org; Gibson Dunn; compliancehub.wiki |
| **2 Dec 2027** | **Stand-alone high-risk AI systems (Annex III / Art. 6(2))** obligations become applicable — deferred from original 2 Aug 2026 | Reg. (EU) 2026/1744, Recital 40 | eur-lex.europa.eu Reg. 2026/1744 (direct fetch); Freshfields; Gibson Dunn; compliancehub.wiki; fpf.org |
| **2 Aug 2028** | High-risk AI embedded in regulated products (Annex I / Art. 6(1) — machinery, medical devices, toys, lifts, aviation, etc.) obligations become applicable — deferred from original 2 Aug 2027 | Reg. (EU) 2026/1744, Recital 40; original baseline at Art. 113(c) | eur-lex.europa.eu Reg. 2026/1744 (direct fetch); ai-act-service-desk.ec.europa.eu Art. 113 (original 2027 baseline) |

---

## Q6: Penalty tiers, article numbers, who/when

### Article 99 — penalties on "operators" (providers, deployers, importers, distributors, authorised representatives) and notified bodies for high-risk/other AI systems
Verbatim from ai-act-service-desk.ec.europa.eu (EC's own service desk):

| Tier | Amount | Trigger | Article |
|---|---|---|---|
| 1 | **up to €35,000,000 or 7% of total worldwide annual turnover, whichever is higher** | "Non-compliance with the prohibition of the AI practices referred to in Article 5" | Art. 99(3) |
| 2 | **up to €15,000,000 or 3% of total worldwide annual turnover, whichever is higher** | Non-compliance with operator/notified-body obligations under Arts. 16, 22, 23, 24, 26, 31, 33, 34, **and Art. 50 (transparency)** | Art. 99(4) |
| 3 | **up to €7,500,000 or 1% of total worldwide annual turnover, whichever is higher** | "Supply of incorrect, incomplete or misleading information to notified bodies or national competent authorities" | Art. 99(5) |
| SME reduction | Lower of the amount/percentage applies | For SMEs, including start-ups | Art. 99(6) |

- **Who sets/enforces these**: Art. 99(1) — *"Member States shall lay down the rules on penalties and other enforcement measures... applicable to infringements of this Regulation by operators"*, required to be "effective, proportionate and dissuasive." Art. 99(2) — member states had to notify the Commission of these rules **"without delay and at the latest by the date of entry into application"** (i.e., by 2 Aug 2025, per Chapter XII's application date under Art. 113(b)). Art. 99(9) — fines may be imposed by national courts or other competent bodies depending on each member state's legal system. (artificialintelligenceact.eu/article/99/)
- **From when**: Chapter XII (containing Art. 99) applies from **2 August 2025** per Art. 113(b) — i.e., the operator-penalties framework (including the Art. 50 transparency-breach tier) has technically been "switched on" since Aug 2025, but Art. 50's underlying obligations only became substantively due 2 Aug 2026, so practical fine exposure for Art. 50 breaches starts 2 Aug 2026.

### Article 100 — fines on EU institutions/bodies/offices/agencies (separate, smaller scale)
Verbatim/paraphrased from artificialintelligenceact.eu/article/100/:
- **Up to €1,500,000** for breach of Art. 5 prohibited practices.
- **Up to €750,000** for any other non-compliance.
- Imposed by the **European Data Protection Supervisor (EDPS)**, not national authorities.

### Article 101 — Commission fines specifically on GPAI model providers (separate track from Art. 99)
Verbatim, ai-act-service-desk.ec.europa.eu: **"3 % of their annual total worldwide turnover in the preceding financial year or EUR 15 000 000, whichever is higher."**
- Grounds: breach of GPAI provisions, failure/refusal to supply accurate documentation or information (Art. 91), denial of model access for evaluation (Art. 92), non-compliance with corrective measures (Art. 93).
- Imposed exclusively by the **Commission** (not member states) — Art. 88 gives the Commission exclusive competence over GPAI provider supervision.
- **Applicable from 2 Aug 2026** specifically (the Art. 113(b) carve-out — see Q2). This is distinct from, and does not preclude, Art. 99 exposure for the *same company* if it also acts as a deployer/provider of a downstream AI system.

---

## Discrepancies / things to double-check before publishing (do not silently smooth over)

1. **"3 months" vs "4 months" grace period for Art. 50(2) marking** — one fetch (via the Council press-release page, likely a WebFetch-summarization slip) said the grace period was "shortened from 6 months to 3 months, deadline now 2 December 2026" — but 3 months from 2 Aug 2026 is 2 Nov 2026, not 2 Dec 2026, which is internally inconsistent. The EUR-Lex direct-fetch (Regulation 2026/1744, Recital 38) supports **4 months**, which correctly arithmetic-checks to 2 Dec 2026. **Use "4 months / 2 December 2026," not "3 months."**
2. **EC's own AI Act Service Desk timeline widget appears stale** (still shows pre-Omnibus 2026/2027 high-risk dates as of this fetch, 3 Aug 2026) — see note under Q3. Don't cite that specific page for the high-risk dates; cite EUR-Lex Regulation 2026/1744 directly instead.
3. **Member-state national-competent-authority count is a moving, imprecisely-dated target** — found "8 of 27" (dated ~25 Mar 2026, aiacto.eu) and "17 of 27" (dated ~July 2026, cubbbix.com, itself flagged lower-confidence because the same piece incorrectly implied high-risk rules apply Aug 2026). **No authoritative EC tally as of exactly 2 Aug 2026 was found in this pass — mark as UNVERIFIED if an exact current number is needed; safe to say "a majority, but not all, member states" as of the most recent (July 2026) snapshot.**
4. **GPAI Article 101 "enforcement power start date" — one EC FAQ paraphrase said 2 Aug 2025**, contradicting the Art. 113(b) statutory carve-out text and every other source. Going with **2 Aug 2026** as correct (see Q2 discrepancy note) — this is the single most important fact in the whole brief to get right and it's the one place a source directly conflicts with the primary statutory text, so flagging loudly.
5. **Tier-3 penalty percentage**: one secondary/tertiary source (techtimes.com) says "1.5%" for the €7.5M tier; the EC's own Article 99(5) text (fetched directly) says **"1 %."** Use **1%**. Do not use 1.5%.
6. **OpenAI/Anthropic "incident" claims from techtimes.com** (sandbox escape, production-system access) are single-source and were not found corroborated by any EU official or other outlet in this pass. **Do not present as established fact; if used at all, attribute explicitly to techtimes.com and flag as unconfirmed.**
7. **"12 systemic-risk models" figure** (techjacksolutions.com, citing an "Epoch AI April 2026 Frontier Compute Report") is single-source in this pass — treat as an approximate, attributed figure, not an EC-confirmed count.
8. **AI Office staffing figure (~125, and a separate "38 new staff" figure seen in a related SERP-research file in this same project)** — not verified against an EC primary source in this pass; do not use without attribution if precision matters.

---

## Full source list (by domain type)

**EU primary (.europa.eu):**
- https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1714 — EC press release "Commission starts enforcing AI Act rules and new transparency requirements on 2 August" (metadata captured directly; body via mirrors)
- https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august — full mirror of above
- https://commission.europa.eu/news-and-media/news/safer-and-more-transparent-ai-2026-08-02_en — EC news post, dated 2026-08-02
- https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act — Art. 50 FAQ
- https://digital-strategy.ec.europa.eu/en/faqs/general-purpose-ai-models-ai-act-questions-answers — GPAI FAQ
- https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content — Code of Practice official page (~190 signatories, timeline)
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai — general AI Act overview page
- https://digital-strategy.ec.europa.eu/en/library/executive-vice-president-virkkunen-updates-council-and-parliament-simplification-implementation-and — Virkkunen Annual Progress Report reference (no direct quote recovered)
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113 — Art. 113 official text (appears to be pre-Omnibus version)
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-99 — Art. 99 official text
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-101 — Art. 101 official text
- https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act — official timeline (flagged possibly stale)
- https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng — Regulation (EU) 2026/1744 official citation page
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ%3AL_202601744 — Regulation 2026/1744 full text (Recitals 38, 40)
- https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/ — Council final adoption press release, 29 June 2026

**Specialist AI Act trackers / law firms (secondary, high-reliability):**
- https://artificialintelligenceact.eu/enforcement-of-chapter-v-under-the-eu-ai-act/ — GPAI Chapter V enforcement mechanics
- https://artificialintelligenceact.eu/article/113/, /article/99/, /article/100/, /article/50/ — text-mirror pages with verbatim article quotes
- https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-34-the-final-digital-omnibus-on-ai-key-amendments-to-the-a-102nber
- https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ (some "expected adoption" language now stale — see discrepancy notes)
- https://compliancehub.wiki/eu-digital-omnibus-ai-act-deadline-deferral-annex-iii-2027/
- https://lawandtechnology.eu/en/digital-omnibus-on-ai-official-journal-regulation-2026-1744/ — OJ publication confirmation
- https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus/ — clean before/after comparison table
- https://www.nicfab.eu/en/posts/ai-act-2-august-2026/

**News/aggregator (secondary, mixed reliability — used for color, flagged where single-sourced):**
- https://www.pubaffairsbruxelles.eu/eu-institution-news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-on-2-august/ — EC release mirror
- https://ieu-monitoring.com/editorial/eu-commission-activates-ai-act-enforcement-and-mandatory-ai-transparency-rules/1246928 — EC release mirror
- https://spacedaily.com/m-europe-ai-act-commission-fines-august-2026/ — GPAI two-tier system color, AI Office staffing figure (unverified)
- https://www.techtimes.com/articles/322604/20260801/eu-engages-openai-anthropic-after-ai-models-hacked-real-companies-fines-take-effect-sunday.htm — Virkkunen quote (unverified primary attribution), OpenAI/Anthropic incident claims (unverified), 1.5% penalty figure (contradicted by primary source, do not use)
- https://www.aiacto.eu/en/blog/ai-act-member-states-national-authorities-2026 — "8 of 27" member states, dated ~25 Mar 2026
- https://cubbbix.com/blog/ai-regulation-july-2026-global-update/ — "17 of 27" member states, dated ~July 2026 (flagged lower-confidence)
- https://techjacksolutions.com/ai-brief/eu-ai-act-systemic-risk-what-the-12-models-now-in-scope-actu/ — "12 systemic-risk models" figure, single-source

---

## Queries run (WebSearch)

EU AI Act 2 August 2026 obligations applicable enforcement · EU AI Act Digital Omnibus stop-the-clock status August 2026 · European Commission press release EU AI Act August 2026 transparency high-risk · EU AI Act GPAI enforcement powers fines Commission August 2026 · "Digital Omnibus" AI Act Official Journal published regulation amending 2024/1689 · EU AI Act Article 99 Article 101 penalties 35 million 7% 15 million 3% 7.5 million 1% · artificialintelligenceact.eu timeline "2 August 2026" Annex III Article 6 · "Article 113" AI Act "24 months" "2 August 2026" general application text · ec.europa.eu ip_26_1714 "Commission starts enforcing AI Act" quote · "2 August 2026" AI Act enforcement Henna Virkkunen quote Commission · EU AI Act August 2026 Reuters OR Politico OR TechCrunch enforcement transparency chatbots deepfakes · ai-act-service-desk.ec.europa.eu article 50 transparency obligations text · EU member states national competent authorities designated AI Act August 2026 how many · EU AI Act systemic risk GPAI models 10^25 FLOPs how many designated 2026 · EU AI Act national competent authorities designated July 2026 member states count update · eur-lex.europa.eu "2026/1744" regulation AI Act · "Article 57" AI Act regulatory sandbox deadline "2 August 2027" Digital Omnibus · EU AI Act Article 100 fines EU institutions agencies bodies European Data Protection Supervisor amount · Virkkunen quote AI Act 2 August 2026 "enforcement" statement Commissioner · "Code of Practice" transparency AI-generated content signatories 2026 AI Act Article 50 · EU AI Act national competent authorities designated AI Act August 2026 how many

END OF NOTES

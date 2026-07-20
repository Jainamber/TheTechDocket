# India Angle: EU's 16 July 2026 DMA Decisions on Google (Android/AI rivals + Search data sharing)

Research compiled: 2026-07-20
Scope: India-specific context for TheTechDocket coverage of the European Commission's 16 July 2026 DMA specification decisions ordering Google to (a) give rival AI assistants Android-level access comparable to Gemini's, and (b) share Search data with rival search engines/AI chatbots.

---

## 1. THE EU DECISION ITSELF (baseline facts, for reference)

- On 16 July 2026 the European Commission issued two binding DMA "specification decisions" against Google:
  1. **AI interoperability on Android** — third-party AI assistants must get access to Android OS features/hooks currently reserved for Gemini (e.g., activation via voice command like "Hey Google", delegated tasks such as booking a taxi, suggesting chat replies, answering questions about a recently visited place), subject to privacy/security/device-integrity safeguards.
  2. **Search data sharing** — Google must share (multi-layer-anonymized, GDPR/DMA-compliant) search data with rival search engines and "AI chatbots offering search functionalities," matching the data Google uses internally, under a fair-pricing/transparent-access regime; Google may screen requesters for cybersecurity/data-protection risk.
  - Source (official): [Commission provides guidance to Google for AI interoperability on Android and sharing of Google Search data under the DMA](https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en) (European Commission DMA portal, dated 2026-07-16)
- **Geographic scope is explicit and EU-only**: the Commission's own page states the measures "apply to European users and the EU market." No implementation deadline is stated in the page content retrieved; the Commission says it "may amend" the decision going forward. (Same source as above.)
  - Secondary coverage (MediaNama) separately reported implementation timelines of **January 2027** (search data sharing) and **July 2027** (Android AI feature access) — flagged here as MediaNama's reporting, not independently confirmed against the primary EC text I could retrieve. Source: [MediaNama, "EU orders Google to open Android, search data to AI rivals"](https://www.medianama.com/2026/07/223-eu-orders-google-open-android-search-data-ai-rivals/) (2026-07, exact day not shown in fetch)
- Google opposed the decision on privacy/security grounds (per the same MediaNama piece).
- **Important finding: MediaNama's own dedicated write-up of this specific decision contains NO mention of India, the CCI, or any India-specific angle whatsoever** — confirmed by direct fetch and read of the full article. India angle has to be assembled from adjacent/related coverage (see §5).
- Related but distinct EU action, useful for India comparisons: on **3 July 2026**, the EU's highest court upheld a separate **€4.1 billion** fine against Google for Android/search-dominance abuse (the long-running 2018 Android case, on appeal) — this is the ruling most Indian outlets actually connected to India, not the 16 July DMA specification decisions. Source: [Business Standard, "EU upholds Google Android fine: Why the ruling matters beyond Europe"](https://www.business-standard.com/technology/tech-news/eu-upholds-google-android-fine-why-the-ruling-matters-beyond-europe-126070300631_1.html) (2026-07-03). Do not conflate the two EU actions when writing — they are different proceedings roughly two weeks apart.

---

## 2. ANDROID'S MOBILE OS MARKET SHARE IN INDIA

- **Android: 93.05%** | iOS: 6.86% | Unknown: 0.04% | KaiOS: 0.03% | Linux: 0.03% | Windows: 0%
- **Source:** [StatCounter Global Stats — Mobile Operating System Market Share India](https://gs.statcounter.com/os-market-share/mobile/india), data month **June 2026** (based on StatCounter's stated methodology of "over 3 billion monthly page views")
- Cross-reference: Business Standard (2026-07-03, cited above) independently states "More than 95 per cent of smartphones in India run on Android" — a rounder, commonly-cited figure in Indian press; treat 93.05% (StatCounter, June 2026) as the precise, dated, citable number and ">95%" as the loose figure Indian outlets tend to quote.

---

## 3. CCI'S OCTOBER 2022 ANDROID RULING — FULL HISTORY

### The order
- **Date:** 20 October 2022
- **Fine: ₹1,337.76 crore** — confirmed consistently across [Bar & Bench](https://www.barandbench.com/news/litigation/cci-imposes-1337-crore-penalty-google-anti-competitive-practices-android-mobile-devices), [LiveLaw](https://www.livelaw.in/ibc-cases/supreme-court-google-appeal-nclat-cci-penalty-android-os-abuse-231495), [Digit.in](https://www.digit.in/features/general/google-antitrust-cases-in-india-a-brief-history.html), [Vaish Associates Advocates](https://www.vaishlaw.com/google-loses-appeal-against-ccis-android-order-in-india/), and Business Standard's 2026-07-03 piece above. (Penalty basis: 10% of Google's average relevant turnover for the three preceding financial years — per Vaish Associates.)
- CCI order page exists at cci.gov.in (https://www.cci.gov.in/antitrust/press-release/details/261) but could not be fetched directly (robots.txt/TLS block on the tool side) — relying on the secondary legal/journalistic sources below for order content, all of which independently corroborate each other.

### Conduct penalized (abuse of dominance across 5 relevant markets: licensable OS for smart mobile devices, Android app stores, general web search, non-OS mobile browsers, online video hosting)
Per [Vaish Associates](https://www.vaishlaw.com/google-loses-appeal-against-ccis-android-order-in-india/):
1. Mandatory pre-installation of the full Google Mobile Services (GMS) suite on OEMs, with no option to uninstall — unfair condition (Sections 4(2)(a)(i) and 4(2)(d), Competition Act).
2. Android Compatibility Commitment (ACC) / Anti-Fragmentation Agreement (AFA) restricting OEMs from building/selling devices on forked Android versions (Section 4(2)(b)(ii)).
3. Revenue Sharing Agreements (RSAs) that foreclosed competing search apps from pre-installation (Section 4(2)(c)).
4. Leveraging Play Store dominance to protect Google's position in search, Chrome (browser) and YouTube (video) (Section 4(2)(e)).

### Remedies ordered (2022, original)
Cease-and-desist plus four specific market-correction directions: (i) allow OEMs/app stores to distribute via Play Store, (ii) stop restricting app sideloading, (iii) give non-disadvantaged access to Play Services APIs for competitors/forks, (iv) allow users to uninstall pre-installed Google apps. Broader behavioral remedies (see §6) included a default search-engine choice screen.

### NCLAT appeal — 29 March 2023
- **Upheld:** all findings of abuse of dominance across all five markets and all Section 4(2) violations; the ₹1,337.76 crore penalty itself (and removed its "provisional" tag, making it final).
- **Set aside:** the four specific market-correction directions above (paras 617.3, 617.7, 617.9, 617.10 of the CCI order), per [SCC Online's NCLAT summary](https://www.scconline.com/blog/post/2023/03/29/penalty-on-google-nclat-sets-aside-certain-directions-by-cci-but-upholds-inr-1337-crore-penalty-on-google-for-abuse-of-dominant-position-in-android-mobile-device-ecosystem-legal-news-legal-researc-up/) and Vaish Associates.
- Earlier, on **19 January 2023**, the Supreme Court had refused Google's request for an interim stay on the CCI order, giving Google one extra week to comply and remanding to NCLAT with a 31 March 2023 deadline to decide the appeal. Source: [TechCrunch, "India's top court rejects Google plea to block Android antitrust ruling"](https://techcrunch.com/2023/01/19/india-supreme-court-rejects-google-plea-to-block-android-antitrust-ruling/) (2023-01-19).

### Supreme Court appeal (against NCLAT's March 2023 order) — status
- Google appealed NCLAT's order to the Supreme Court (filed ~June 2023).
- **7 July 2023:** SC first took up the cross-appeals (Google and CCI both appealed different parts).
- **22 January 2024:** SC listed the matter for hearing on 30 April 2024. Source: [Business Standard, "SC to hear Google's plea against CCI fine of Rs 1,337.76 crore on April 30"](https://www.business-standard.com/companies/news/sc-to-hear-google-s-plea-against-cci-fine-of-rs-1-337-76-crore-on-april-30-124012200742_1.html) (2024-01-22).
- **19 September 2024:** Case mentioned again before a bench led by then-CJI D.Y. Chandrachud; senior advocate Harish Salve said the hearing could take 5-6 days; hearing was **postponed** to accommodate other pending matters; the Court had appointed a nodal counsel (Sameer Bansal) to prepare digital pleadings. Source: [Business Standard, "Google's plea against CCI order in android mobile case mentioned in SC"](https://www.business-standard.com/technology/tech-news/google-s-plea-against-cci-order-in-android-mobile-case-mentioned-in-sc-124091900733_1.html) (2024-09-19); corroborated by [Digit.in](https://www.digit.in/news/general/googles-antitrust-hearing-postponed-supreme-court-to-hear-the-case-on-a-later-date.html).
- **No confirmed final verdict or new hearing date found beyond September 2024** for this specific (₹1,337.76 crore, "Android bundling," Case No. 39/2018) matter, despite extensive searching. The most recent reference I could find, from July 2026, treats the case as **still pending**: "the CCI imposed a ₹1,337 crore penalty... Google spent years arguing the CCI was wrong... Now the EU's own highest court has confirmed those problems are real" — implying the SC appeal remains open as of publication. Source: [IndiaHerald, "Google's €4.1 Billion Android Defeat in Europe — Can It Still Escape CCI's ₹1,337 Crore Penalty in India?"](https://www.indiaherald.com/Business/Read/994895339/Google-Android-Fine-EU-Ruling-Impact-on-CCI-India-Penalty) (2026-07, exact day not shown in fetch; low-tier aggregator outlet, treat as directional not authoritative).
- **UNVERIFIED:** a precise, current (2025-2026) hearing date or disposition for the ₹1,337.76 crore Android bundling case specifically. Flag this gap explicitly if the piece needs "latest status" — best supportable claim is "pending before the Supreme Court, last confirmed active as of July 2026 reporting."

### Do not confuse with the SEPARATE Play Store billing case
A different CCI matter (Case No. 07/2020, Play Store billing/in-app payment practices) has its own, more recently active track — useful context but NOT the same case as the ₹1,337.76 crore Android bundling order:
- Original CCI fine (Oct 2022): ₹936.44 crore.
- NCLAT (28 March 2025): partly upheld findings, **reduced penalty to ₹216.69 crore**; clarification order (1 May 2025) reinstated two directions on billing-data transparency and data-use restrictions.
- Google appealed to Supreme Court **21 July 2025**; SC admitted cross-appeals from Google, CCI and the Alliance of Digital India Foundation (ADIF) on **8 August 2025**; hearing scheduled for **November 2025**.
- Sources: [LawChakra](https://lawchakra.in/supreme-court/google-android-supreme-court-nclat/) (2025-07-24), [BestMediaInfo](https://bestmediainfo.com/mediainfo/mediainfo-digital/google-cci-adif-clash-in-supreme-court-over-play-store-antitrust-ruling-9647227) (2025-08-11), [ForumIAS](https://forumias.com/blog/supreme-court-to-hear-cci-and-google-android-case/) (2025-08-12).
- **UNVERIFIED:** outcome of the November 2025 hearing (my search did not surface a post-hearing result).

---

## 4. INDIA'S DIGITAL COMPETITION BILL (DMA-style ex-ante law) — STATUS AS OF MID-2026

Timeline, fully sourced:
- **12 March 2024:** Committee on Digital Competition Law (CDCL) submitted its final report + draft "Digital Competition Bill, 2024" to the Ministry of Corporate Affairs (MCA). Core proposal: ex-ante regulation of "Systemically Significant Digital Enterprises" (SSDEs) — search engines, OS, browsers, social networks etc. — enforced by a strengthened CCI/Director General, with civil penalties up to 10% of global turnover (shift away from criminal penalties). Source: [PRS India, "Digital Competition Law"](https://prsindia.org/policy/report-summaries/digital-competition-law); draft bill text: [MediaNama-hosted PDF](https://www.medianama.com/wp-content/uploads/2024/03/DRAFT-DIGITAL-COMPETITION-BILL-2024.pdf).
- **12 March – 15 May 2024:** Public consultation window; June 2024, additional MeitY stakeholder consultations. Over 100 stakeholders submitted input. Source: [India Briefing, "India's Digital Competition Bill Advances with Industry Insights"](https://www.india-briefing.com/news/indias-digital-competition-bill-advances-with-industry-insights-36536.html/).
- **26 September 2024:** Reports the Centre was "mulling" withdrawal; industry split — India SME Forum and MSMEs favoured withdrawal (citing burden on targeted-advertising/single-sign-on/exclusive-deal practices); ~40 Indian startups (Matrimony.com, TrulyMadly, Innov8 among them) publicly supported keeping ex-ante rules as a check on Big Tech. Source: [Storyboard18, "Industry endorses withdrawal of draft Digital Competition Bill"](https://www.storyboard18.com/digital/industry-endorses-withdrawal-of-draft-digital-competition-bill-43211.htm) (2024-09-26).
- **August 2025:** Parliamentary **Standing Committee on Finance's 25th Report** recommended pausing/reconsidering the ex-ante approach — citing (a) broad scope/rigid ex-ante obligations risking undue burden, (b) risk of stifling innovation/deterring foreign investment/high compliance costs for startups & MSMEs, (c) unclear SSDE thresholds unsuited to India's market diversity, (d) overlap with IT Act, consumer-protection law, and sectoral regulators, and (e) fast-moving tech (explicitly citing ChatGPT's disruption of Google's search dominance) meaning rigid rules risk regulating markets that may not exist by the time they're enforced. Source: [MediaNama, "Why India Withdrew the Digital Competition Bill 2024"](https://www.medianama.com/2025/08/223-india-digital-competition-bill-2024-withdrawal/) (2025-08-16).
  - Government's recalibrated path per the same piece: lean on existing Competition Act enforcement tools; design India-specific tiered obligations rather than copying the EU; sequence after DPDPA (data protection law) rules are in place; build CCI capacity first.
- **12 November 2025:** MCA issued an **RFP to commission a market study** re-evaluating the qualitative/quantitative thresholds in Clause 3 of the draft Bill and the 9 proposed "core digital services" categories — explicitly a reassessment/preparatory step, not a re-introduction. Sources: [MediaNama, "MCA Issues RFP to Reassess Digital Competition Rules"](https://www.medianama.com/2025/11/223-mca-rfp-digital-competition-bill/) (title/URL confirmed via search; direct fetch blocked by 403) and [Business Today, "MCA plans market study on thresholds for Big Tech companies and core digital services"](https://www.businesstoday.in/tech-today/news/story/mca-plans-market-study-on-thresholds-for-big-tech-companies-and-core-digital-services-501911-2025-11-12) (2025-11-12, successfully fetched, corroborates).
- **January 2026 retrospective:** "Momentum notably slowed" through 2025; CCI advised to focus on institutional capacity, coordination with the Data Protection Board, and its ongoing (non-legislative) investigations into Apple's iOS ecosystem and e-commerce platforms rather than push the ex-ante bill. Source: [MediaNama, "How Did The CCI Handle The Digital Competition Domain In 2025? And What Should It Do In 2026?"](https://www.medianama.com/2026/01/223-cci-digital-competition-2025-what-should-it-do-2026/) (2026-01).

**Bottom line status (as of 2026-07-20, my research date): the Digital Competition Bill has NOT been introduced in Parliament and has NOT been formally, officially withdrawn either.** It is in a "recalibration"/market-study limbo — paused since the August 2025 Standing Committee report, with MCA now re-studying thresholds (RFP issued Nov 2025) before any decision on reviving it. No news I found states a 2026 introduction date. Treat any claim that it has been "passed," "introduced," or "shelved outright" as **UNVERIFIED/likely false** based on this research.

### CCI's own AI-specific work (separate from the Bill)
- **October 2025:** CCI published a **market study on Artificial Intelligence and Competition**, taking a "light-touch" approach — flags algorithmic-collusion and self-preferencing risks across the AI stack but recommends **self-audits and voluntary transparency** rather than binding ex-ante rules. Sources (titles/dates confirmed via search, not all individually fetched due to repeated 403s on MediaNama): [Concurrences summary](https://www.concurrences.com/en/bulletin/news-issues/october-2025/the-indian-competition-authority-adopts-a-light-touch-approach-in-its-ai-market) (fetch blocked, 403); primary CCI document: [Market study on Artificial Intelligence and Competition (PDF)](https://www.cci.gov.in/images/marketstudie/en/market-study-on-artificial-intelligence-and-competition1759752172.pdf) (URL from search, not independently fetched — flag as unverified content, verified-to-exist URL only).

### MeitY / government statements on AI regulation in 2026 (broader than just gatekeepers, but relevant)
- **11 June 2026:** IT Minister **Ashwini Vaishnaw** told PTI "there is a requirement for a new law because the world of AI is very different from the world when the IT Act was enacted in 2000" — a reversal of his own 2023 parliamentary statement that government was "not considering bringing a law or regulating the growth of artificial intelligence." Source: [MediaNama, "Ashwini Vaishnaw says India needs new AI law, reversing MeitY's position"](https://www.medianama.com/2026/06/223-vaishnaw-new-ai-law-contradicting-meitys-position-2023-parliamentary-reply/) (2026-06-11/fetched successfully).
- **9 July 2026:** MeitY Secretary **S. Krishnan**, speaking at CII's GCC Business Summit in New Delhi, said the ministry will "start discussing in various groups as to what the stakeholders feel about it [AI regulation] and... start a process of drafting"; noted ~762 suggestions received from various ministries on AI use. Source: [MediaNama, "MeitY to discuss separate AI regulation law: S Krishnan"](https://www.medianama.com/2026/07/223-meity-start-stakeholder-discussions-separate-law-ai-regulation-s-krishnan/) (2026-07-09, fetched successfully).
- **Important distinction for the piece:** these 2026 statements are about a general AI **safety/harms** law (akin to an "AI Act"), a track that is **separate from** the paused, DMA-style, gatekeeper-focused Digital Competition Bill. As of this research, **I found no MeitY/CCI statement specifically proposing DMA-style interoperability or data-sharing mandates for AI assistants** (i.e., nothing India-side that mirrors the EU's 16 July decision in substance). Mark this absence explicitly if the story claims India is "following the EU's lead" on AI-assistant gatekeeping — that claim is not supported by what I found.

---

## 5. INDIAN COVERAGE OF THE EU'S 16 JULY 2026 DECISION SPECIFICALLY

- **MediaNama's direct report** on the decision ([link](https://www.medianama.com/2026/07/223-eu-orders-google-open-android-search-data-ai-rivals/)) — confirmed to exist via my own WebSearch, then fetched — is essentially a rewrite of the EU story with **no India-specific analysis or CCI mention** at all. This is itself a notable gap/finding for the piece: India's leading tech-policy outlet covered the decision as pure EU news.
- The India-angle commentary I could find instead clusters around the **related, earlier (3 July 2026) CJEU ruling** upholding the €4.1bn fine — which Indian outlets did connect to India:
  - **Business Standard, "EU upholds Google Android fine: Why the ruling matters beyond Europe"** (2026-07-03): explicitly states "More than 95 per cent of smartphones in India run on Android, making Google's business practices highly relevant for smartphone manufacturers," cites CCI's ₹1,337.76 crore penalty and the same MADA/AFA-style agreements, and frames the EU ruling as validating India's regulatory approach — implicitly bullish on the (paused) Digital Competition Bill's rationale. Link: https://www.business-standard.com/technology/tech-news/eu-upholds-google-android-fine-why-the-ruling-matters-beyond-europe-126070300631_1.html
  - **IndiaHerald** (aggregator, lower editorial bar — treat as directional colour, not primary): two pieces framing (a) the EU rulings as strengthening CCI's hand in Google's pending Supreme Court appeal ("Google spent years arguing that the CCI was wrong to see the same problems the EU saw. Now the EU's own highest court has confirmed those problems are real" — quoting unnamed "competition law analysts"), and (b) Google's AI/search strategy shift against the backdrop of "India's 700 million smartphones." Links: https://www.indiaherald.com/Business/Read/994895339/Google-Android-Fine-EU-Ruling-Impact-on-CCI-India-Penalty and https://www.indiaherald.com/Technology/Read/994899297/Google-AI-India-Search-Strategy-Impact-2026
- **I could not locate dedicated Economic Times, Mint (Livemint), or Business Standard pieces specifically analysing the 16 July DMA specification decisions (AI-interoperability/search-data-sharing) through an India lens** — direct site-restricted searches on economictimes.indiatimes.com and livemint.com returned no results. **Mark as UNVERIFIED/not found**, not as "no such coverage exists" — it may exist behind paywalls or simply didn't surface in search; a follow-up manual check of ET Tech and Mint's tech section is recommended before the piece claims "ET/Mint said nothing."
- No statement from the CCI, MCA, or MeitY reacting specifically to the 16 July 2026 EU decision was found. **Mark as UNVERIFIED/not found** (searched specifically; nothing surfaced).

---

## 6. PRACTICAL USER IMPACT: WILL THIS REACH INDIAN ANDROID USERS?

### Google's documented past pattern (precedent, fully sourced)
After the CCI's 2022 order, Google rolled out **India-specific** changes in **January 2023**, not an automatic extension of EU remedies:
1. Default **search-engine choice screen** during Android device setup for Indian users — described by MediaNama as "similar to the choice screen Google shows in the EU," i.e., Google built an India-specific instance modelled on the EU mechanism, in direct response to the CCI order (not the DMA itself, and not automatically triggered by any EU action).
2. OEMs allowed to license individual Google apps rather than the full GMS suite.
3. Android compatibility rules loosened to permit forked Android variants.
4. Sideloading process/warnings updated.
5. Third-party billing systems allowed alongside Play billing, at a **4% reduced commission**.
- Google did **not** implement everything the CCI originally ordered — it did not allow rival app stores to be listed inside Play Store, did not remove all pre-installed-app restrictions, and contested anti-steering provisions. Source: [MediaNama, "What Google is (and isn't) changing in Android and Play Store to comply with India's antitrust orders"](https://www.medianama.com/2023/01/223-google-android-play-changes-cci-order/) (2023-01).

### Will the 16 July 2026 DMA remedies specifically reach India?
- **No evidence of automatic extension.** The European Commission's own page for the 16 July decision states the AI-interoperability and search-data-sharing measures "apply to European users and the EU market" — i.e., **explicitly EU-scoped**, unlike some other Google product changes that have occasionally gone global. Source: same EC DMA page as §1.
- Historically, DMA-mandated **choice screens have stayed EU-only**; India got its own, CCI-ordered choice screen on a separate legal track (see above) — so the mechanism for reaching Indian users has been **domestic enforcement, not EU spillover**.
- Given the Digital Competition Bill (India's own DMA-equivalent) is currently paused/under re-study (§4), and the CCI's ₹1,337.76 crore Android case remains on appeal at the Supreme Court with no verdict (§3), **there is currently no active Indian legal mechanism that would force Google to replicate the 16 July 2026 AI-interoperability or search-data-sharing remedies in India.** This is my own synthesis from the sourced facts above, not a claim from any single source — flag it as analysis if used in the piece, and consider getting an on-record quote from an Indian competition lawyer to firm it up before publishing.

### Gemini / Google AI usage numbers touching India
- **Global Gemini app: 750 million+ monthly active users**, reported on Google's Q4 2025 earnings call, **4 February 2026**; no India-specific breakout found in this report. Source: [TechCrunch, "Google's Gemini app has surpassed 750M monthly active users"](https://techcrunch.com/2026/02/04/googles-gemini-app-has-surpassed-750m-monthly-active-users/).
- **"AI Mode" (Google Search's AI-chat feature): "over 100 million monthly active users"** in "**the U.S. and, more recently, India**" combined (not India-only) — stated by Sundar Pichai on Google's **Q2 2025 earnings call, 23 July 2025**. Source: [TechCrunch, "Google's AI Overviews have 2B monthly users, AI Mode 100M in the US and India"](https://techcrunch.com/2025/07/23/googles-ai-overviews-have-2b-monthly-users-ai-mode-100m-in-the-us-and-india/). Note this figure is now a year old relative to the current date (July 2026) and is a **combined US+India** number, not India-only.
- **UNVERIFIED:** any India-only, 2026-dated Gemini/AI Mode user count. Not found despite multiple searches across stats-aggregator blogs (getpanto, fatjoe, omnibound, electroiq, etc. — none break out India specifically; these are also low-authority SEO content sites and shouldn't be cited as primary sources regardless).

### YouGov survey on AI assistants vs. search engines in India — VERIFIED, exists, but flag a numbers discrepancy
Confirmed real, matches the task's description of "~2026-07-10, Business Today." Two Indian outlets covered it with a caveat: **the exact statistics differ between the two write-ups, likely reflecting different cuts of YouGov's research (India-specific report vs. a global/19-country comparative report) — a copy editor should pull the primary YouGov PDF before quoting exact percentages.**

- **Business Today** (2026-07-10): [AI assistants close in on search engines as India's online discovery habits shift: YouGov](https://www.businesstoday.in/technology/artificial-intelligence/story/ai-assistants-close-in-on-search-engines-as-indias-online-discovery-habits-shift-yougov-542181-2026-07-10)
  - Sample: "950+ online searchers"; fieldwork 21 April – 29 May 2026; **19 countries** covered.
  - India: **89%** "now qualify as AI searchers" vs **48%** in the US.
  - Search engines still lead usage at **65%**; AI assistants/chatbots close behind at **57%**.
  - **66%** of Indians search online at least once daily; **43%** search 6+ times/day; **76%** primarily via smartphone.
  - AI use is complementary, not a replacement: **27%** start their search with AI, **36%** use AI after other searches, **26%** alternate.
  - Top AI use cases: direct answers (49%), verifying info (44%), summarizing/comparing (43%).
  - Trust: AI assistants **69%** (third place) vs. maps/navigation and search engines tied at **75%**.
  - Two-thirds expect to use AI more over the next year; 75% of current AI users have 12+ months of experience with it.
- **Business Standard** (2026-07-15): [AI tools emerge as mainstream search option for users in India: Survey](https://www.business-standard.com/technology/artificial-intelligence/ai-tools-emerge-as-mainstream-search-option-for-users-in-india-survey-126071501287_1.html)
  - Sample: **1,004 Indian adults (18+)**, YouGov.
  - "**More than 50%**" of Indian users now rely on AI tools for information.
  - **27%** begin their search with AI (matches Business Today's figure).
  - **36%** use AI after trying other search methods (matches Business Today's figure).
  - AI "enjoys a high level of trust... ahead of marketplaces, news websites, video platforms, online communities and social media" (directionally consistent with Business Today's trust numbers, not identical framing).
- **YouGov's own India report landing page** ([link](https://yougov.com/reports/55100-india-websearch-ai-report-2026)) describes a sample of "over 1,000 Indian adults" (matches Business Standard's 1,004, not Business Today's 950+/19-country figure) — suggesting Business Today may be citing YouGov's separate global comparative dataset (see [YouGov's US/global report](https://yougov.com/en-us/reports/55071-us-websearch-ai-report-2026)) for the 89%-vs-48%-US and 19-country stats, while Business Standard is citing the India-specific 1,004-person report for the "50%+", "27%", "36%" figures. **Both are legitimate YouGov output, likely just different questions/waves — cite each figure with its exact source as done above, don't merge them into one unattributed stat block.**
- Other Indian outlets that also covered this same YouGov research (not independently fetched, listed for completeness/further pull if needed): [Social Samosa, "Three in five Indians start at least one daily search with AI assistants: YouGov"](https://www.socialsamosa.com/report/three-in-five-indians-start-atleast-one-daily-search-with-ai-assistants-12167226); [Apeejay Newsroom, "More than half of Indians now use AI tools to search for information: Survey"](https://apeejay.news/more-than-half-of-indians-now-use-ai-tools-to-search-for-information-survey/).

---

## SUMMARY TABLE OF KEY CITABLE NUMBERS

| Fact | Number | Source | Date |
|---|---|---|---|
| Android share of India mobile OS market | 93.05% | gs.statcounter.com/os-market-share/mobile/india | June 2026 data |
| Android share of India smartphones (rounded, press usage) | >95% | Business Standard | 2026-07-03 |
| CCI Android fine | ₹1,337.76 crore | Bar & Bench / LiveLaw / Digit.in / Vaish Associates | Order: 2022-10-20 |
| CCI Play Store billing fine (separate case) | ₹936.44 crore → reduced to ₹216.69 crore | LawChakra | Order 2022-10; NCLAT reduction 2025-03-28 |
| Gemini app global MAU | 750 million+ | TechCrunch | Reported 2026-02-04 (Q4 2025 data) |
| Google "AI Mode" MAU, US+India combined | 100 million+ | TechCrunch | Reported 2025-07-23 (Q2 2025 data) |
| YouGov India: AI "searchers" | 89% (vs 48% US) | Business Today | Published 2026-07-10 |
| YouGov India: rely on AI tools for info | >50% | Business Standard | Published 2026-07-15 |
| YouGov India: start search with AI | 27% | Business Today & Business Standard (matching) | Published 2026-07-10/15 |

---

## ITEMS EXPLICITLY MARKED UNVERIFIED (do not use without further checking)

1. **Final Supreme Court verdict/current hearing date on the ₹1,337.76 crore CCI Android bundling case** — last confirmed activity is 19 September 2024 (postponed); a July 2026 secondary source treats it as still pending, but no definitive 2025/2026 hearing date or verdict was located.
2. **Outcome of the November 2025 Supreme Court hearing in the separate Play Store billing case** (₹216.69 crore, post-NCLAT) — hearing was scheduled but no post-hearing result found.
3. **Dedicated Economic Times or Mint/Livemint analysis of the 16 July 2026 DMA decision through an India lens** — not found in search; may exist but did not surface.
4. **Any official CCI/MCA/MeitY reaction or statement specifically about the 16 July 2026 EU decision** — not found.
5. **India-only (not combined with US) 2026 user numbers for Gemini or Google AI Mode** — not found; only global (750M) and US+India-combined (100M, and that's from mid-2025) figures exist.
6. **CCI's October 2025 AI market study content** — URL and existence confirmed via search (CCI's own hosted PDF, plus a Concurrences summary), but I could not fetch either due to access blocks, so specific claims about its content beyond "light-touch, recommends self-audits, flags algorithmic collusion/self-preferencing risk" (which came from the search snippet, not a full read) should be treated as provisional pending a direct read of the primary PDF at https://www.cci.gov.in/images/marketstudie/en/market-study-on-artificial-intelligence-and-competition1759752172.pdf.
7. **Precise reconciliation of the two different YouGov sample sizes/stats** (950+/19-country vs 1,004/India-only) — both are genuine YouGov output per my research, but I could not confirm from a single primary source how they relate to each other; treat as two distinct citable data points, not one.

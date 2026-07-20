# Research Notes: EU DMA Decisions (16 July 2026) — Rivals & Technical Implications

Compiled 2026-07-20. Topic: EU forces Google to open Android to rival AI assistants (equal access vs Gemini) and to share Search data with rival search engines/AI chatbots.

---

## 1. THE DECISION ITSELF — core facts

- On 16 July 2026 the European Commission adopted two binding "specification decisions" under DMA Article 6(7)/6(11) against Alphabet/Google: one on AI interoperability on Android (case DMA.100220), one on sharing of Google Search data (case DMA.100209).
  Source: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en ; case numbers and 27 July statutory deadline context from https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm

- Proceedings were opened 27 January 2026 with six-month statutory deadlines; Commission sent preliminary findings to Google on 27 April 2026 demanding "free and effective interoperability" for third-party AI developers.
  Source: https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm

- Rationale cited by Commission: roughly 60% of EU users are on Android devices and currently lack meaningful alternatives to Google's AI/Gemini and Search.
  Source: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en (also repeated at https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/ — "affecting approximately 427 million devices")

- Android interoperability: **11 specific mandated features** across four categories — Invocation (long-press home button/nav handle, always-on hotword detection incl. concurrent multi-assistant activation), Context (centralized on-device app-data access equivalent to Google's AppSearch; context-aware/screen-content-based suggestions with consent; ambient mic/camera/screen/speaker sensor streams), Action (App Functions framework access to Gmail/Calendar/Drive/Docs/Maps/YouTube/Messages/Phone; background screen automation in virtual windows; OS-level control of brightness/media/DND/Bluetooth), and Resource (equal access to on-device Gemini Nano models with performance guarantees; equal hardware/background-execution conditions).
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en

- Google may impose "objective, non-discriminatory" eligibility/certification criteria for the invocation/context features on privacy-security grounds; certification decisions must be issued within four weeks of a developer application; documentation/testing support must be free.
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en

- Implementation deadlines: **most Android features by Android 18, 1 August 2027**; concurrent/simultaneous hotword detection specifically pushed to **Android 19, 1 August 2028**.
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
  NOTE — secondary press gives inconsistent shorthand dates for the "Android" deadline: "July 2027" (MacRumors: https://www.macrumors.com/2026/07/16/eu-google-ai-apps-android-access/ ), "June 2027" (SiliconANGLE: https://siliconangle.com/2026/07/16/eu-orders-google-share-search-data-rivals-broaden-android-feature-access/ ), "August 1, 2027" (TechRepublic: https://www.techrepublic.com/article/news-eu-google-android-ai-search-data-rules-emea/ ). Treat the official DMA developer-portal page's "Android 18 by 1 August 2027 / Android 19 by 1 August 2028" as authoritative.

- Search data sharing: Google must give eligible rival search engines and AI chatbots-with-search anonymized query, click, ranking and view data "matching what it uses to optimize its own search," via a multi-layered anonymization method built with internal/external privacy experts, subject to a FRAND-style pricing formula and annual audits; recipients may use data only to improve search, not for ad personalization or general AI training; Google can assess "serious cyber security and data protection risks" before granting access. Access reported to begin **January 2027**.
  Source: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en ; January 2027 start and FRAND/audit detail also at https://www.unite.ai/eu-compels-google-to-share-android-and-search-data-with-rival-ai-assistants/ and https://siliconangle.com/2026/07/16/eu-orders-google-share-search-data-rivals-broaden-android-feature-access/

- Non-compliance risk: fines of up to 10% of Alphabet's total worldwide annual turnover (potentially >$35bn); appeals do not suspend the compliance obligation.
  Source: https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm ; appeals-don't-suspend point from https://www.techtimes.com/articles/320760/20260716/eu-gives-rival-ai-assistants-system-level-access-google-reserved-gemini.htm [also indexed as https://www.techtimes.com/articles/320760/20260716/eu-gives-rival-ai-assistants-system-level-android-access-google-reserved-gemini.htm]

- EU official quote: Executive Vice-President Henna Virkkunen said the Commission wants to see "emerging alternatives to Google Search and Google's AI services, such as Gemini," giving users "more choice," and "we want to support innovation and diversity in the European Union."
  Source: (Virkkunen "emerging alternatives"/"more choice") https://www.techrepublic.com/article/news-eu-google-android-ai-search-data-rules-emea/ ; ("support innovation and diversity") https://michaelparekh.substack.com/p/ai-europes-dma-rulings-set-tough

---

## 2. COMPANIES THAT STAND TO BENEFIT — what they have SAID on record

### Google (the target, not a beneficiary, but essential on-record reaction)
- Kent Walker, President of Global Affairs, Google & Alphabet, in an official Google blog post dated 16 July 2026:
  > "Today's decisions risk undermining vital privacy and security guardrails for millions of Europeans."
  > On Android: "This Android ruling threatens device security by granting external apps sensitive and powerful device permissions without these safeguards."
  > On search sharing: "Europeans' private searches would be exposed to unfamiliar companies, without adequate anonymisation of the data and without user knowledge or consent."
  Source: https://blog.google/company-news/inside-google/around-the-globe/google-europe/the-dma-should-not-undercut-security-privacy-for-europeans/

- Additional Kent Walker phrasing reported by press (paraphrase + partial quotes, treat as secondary): claims the rules "bypass critical hardware-level security guardrails," create "a meaningful attack surface on users' devices," and that sharing search data would "weaken citizen privacy, risk business trade secrets and endanger national security"; Google says it offered alternative solutions but the EU "discount[ed] extensive evidence of user harm."
  Source: https://www.androidauthority.com/eu-android-ai-google-search-mandates-3688186/ (attack surface/vetting) ; https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/ (business trade secrets/national security) ; https://siliconangle.com/2026/07/16/eu-orders-google-share-search-data-rivals-broaden-android-feature-access/ ("discount... evidence of user harm")

- Sameer Samat, President of Android Ecosystem, reportedly posted on X/Twitter that the Commission "is on the wrong track" with its rules, arguing users can already independently switch default assistants.
  Source: https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/
  UNVERIFIED — could not locate the primary X/Twitter post itself to confirm exact wording; relying on CNN-syndicated (BNN Bloomberg mirror) paraphrase+quote.

- Google is complying rather than withdrawing Gemini features from the EU (contrast with Apple/Siri, see below).
  Source: https://www.digitaltrends.com/phones/eu-is-forcing-google-to-give-ai-rivals-a-fair-shot-on-android-and-your-wallet-might-benefit/

### OpenAI
- **No on-record statement specifically about the 16 July 2026 DMA decision was found** in any source searched (checked CNBC, TechRepublic, MacRumors, TechCrunch, Android Authority, SiliconANGLE, Medianama, Unite.AI, The Register [blocked], Techmeme aggregation for 16-17 July 2026). UNVERIFIED / NOT FOUND.
- Context only: ChatGPT can already be set as a default/secondary assistant on Android today (a Google Assistant-API-level integration, not full Gemini-parity), per consumer how-to coverage — this is existing functionality, not a reaction to the ruling.
  Source: https://www.tomsguide.com/ai/chatgpt/how-to-make-chatgpt-your-default-assistant-on-android-instead-of-gemini
- Analyst framing (ICLE's Dirk Auer, see §5) states ChatGPT "accounts for roughly 70 per cent of EU chatbot use" — relevant to why OpenAI is a major beneficiary even without a direct quote.
  Source: https://laweconcenter.org/eus-android-ai-mandate-could-leave-europeans-with-less-choice/

### Perplexity
- **No on-record Perplexity statement specifically about the 16 July 2026 DMA decision was found.** UNVERIFIED / NOT FOUND.
- Past public complaints about Android default-assistant restrictions (well documented, pre-dates this ruling):
  - CEO Aravind Srinivas posted on X (~11 March 2025): "hearing incidents of Google secretly switching the assistant back to Google from Perplexity without the Perplexity user's consent."
    Source: https://techissuestoday.com/perplexity-ceo-google-switching-android-digital-assistant-settings/ (also covered at https://www.androidpolice.com/phone-assistant-defaults-to-google-from-perplexity/ )
    Note: that same coverage cautions the cause may have been "a bug with Android and/or Perplexity" rather than deliberate action — i.e., not proven as intentional obstruction by Google.
  - Perplexity Chief Business Officer Dmitry Shevelenko testified under oath in the US v. Google antitrust remedies trial (23-24 April 2025, before Judge Amit Mehta) that Google's contract terms prevented Motorola (owned by Lenovo) from setting Perplexity as the default assistant: "[Motorola] can't get out of their Google obligations and so they are unable to change the default assistant on the device." Perplexity's app would be preloaded but not placed prominently on the home screen.
    Source: https://dataconomy.com/2025/04/24/googles-terms-kept-perplexity-off-motorolas-home-screen/ (original Bloomberg reporting: https://www.bloomberg.com/news/articles/2025-04-23/perplexity-executive-says-google-blocked-motorola-s-use-of-ai-assistant — paywalled, not directly fetched)
  - Perplexity blog post "Choice is the Remedy" (21 April 2025 — about the US DOJ Google antitrust remedies case, NOT the EU/DMA): "If a phone maker wants to include any of Google's apps like Google Maps or the Play Store, they're required to include all of them... They also have to preload Google Search and Google Assistant as required defaults and limit alternatives for their users." And: "Let people choose. Let phone makers and carriers offer their customers what they want—choice—without fearing financial penalties or access restrictions." And positioning: "We're not a competitor to Google. We're building something different...a choice: search that answers, assistants that work."
    Source: https://www.perplexity.ai/hub/blog/choice-is-the-remedy
    IMPORTANT: this post does not mention the EU or DMA at all — it is US-context only. Flagging clearly so it isn't misread as a reaction to the EU ruling.

### Meta AI
- **No on-record Meta/Meta AI statement about this decision, or about Android assistant access generally, was found in any searched source.** UNVERIFIED / NOT FOUND.

### Anthropic
- **No on-record Anthropic statement about this decision was found.** UNVERIFIED / NOT FOUND.
- Context only (analyst-sourced, not Anthropic's own words): ICLE's Dirk Auer states "Anthropic has grown faster than any rival over the past year" in the EU chatbot market — cited as a reason Google, not Anthropic/OpenAI, is the actual competitively disadvantaged party.
  Source: https://laweconcenter.org/eus-android-ai-mandate-could-leave-europeans-with-less-choice/

### DuckDuckGo / Ecosia / Qwant (search data-sharing beneficiaries)
- **No statement specifically reacting to the 16 July 2026 decision found for any of the three.** UNVERIFIED / NOT FOUND for this specific ruling.
- DuckDuckGo CEO Gabriel Weinberg and Chief Communications/Policy Officer Kamyl Bazbaz made on-record statements ~26 May 2026 (about Google's I/O 2026 AI Search overhaul generally, not this DMA decision):
  > Weinberg: "Google is force-feeding AI with no way to opt out. As a result, their results are getting worse, not better."
  > Weinberg: "Not only do we respect user choice, but also user privacy. Everything you do in DuckDuckGo is private, we don't collect search histories or chats and nothing is used for AI training."
  > Bazbaz: "People just want a choice."
  Source: https://techcrunch.com/2026/05/26/duckduckgo-installs-are-up-30-as-users-reject-being-force-fed-googles-ai-search/ (DuckDuckGo installs reportedly up 30% in the period, per TechCrunch)
- Joint standing position from Ecosia CEO Christian Kroll, DuckDuckGo CEO Gabriel Weinberg, and Qwant President Corinne Lejbowicz (originally 5 July 2022, updated 18 April 2024 — predates this ruling by years, but establishes their consistent long-standing ask): "It remains unnecessarily difficult to switch away from gatekeeper default settings," and gatekeepers "should globally roll out fair choice screens and effective switching mechanisms now" (i.e., these three have long argued for global, not EU-only, remedies).
  Source: https://blog.ecosia.org/fair-choice-dma/

---

## 3. TECHNICAL REALITY CHECK — what rivals can't do on Android today vs Gemini

- **Hotword/"Hey Google" activation**: Android's `VoiceInteractionService` architecture supports always-on hotword detection via a DSP-level `AlwaysOnHotwordDetector` (low CPU, requires hardware support + sound-model enrollment) or a software fallback requiring `MediaRecorder.AudioSource.HOTWORD` + the `CAPTURE_AUDIO_HOTWORD` permission. Critically, **voice interaction apps must be "pre-installed, system-signed APKs" to receive certain signature-level permissions that users cannot grant themselves** — a structural barrier to any non-preinstalled third-party assistant matching Gemini's hotword access.
  Source: https://source.android.com/docs/automotive/voice/voice_interaction_guide/app_development (AOSP official documentation)

- **Default assistant slot / lock-screen access**: Google Assistant (and by extension Gemini) has documented, supported lock-screen access via a dedicated settings toggle ("Get Google Assistant on your Android lock screen"). The EU's own decision explicitly targets closing this gap by mandating comparable long-press-home-button and nav-handle invocation rights for rivals.
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en

- **In-app actions / App Functions API**: Android's AppFunctions platform API (Android 16+, plus a Jetpack library) lets apps expose capabilities as callable "tools" for AI agents/assistants — Android's rough equivalent of the Model Context Protocol (MCP), but on-device. Access is gated by the `EXECUTE_APP_FUNCTIONS` permission. As of the source's data (~May 2026), **Gemini's integration with AppFunctions was itself still in "private preview" with only "trusted testers,"** and the docs state that "to carefully evaluate the quality of the overall experience during this experimental phase, only a limited number of apps and system agents can access the entire pipeline" — meaning even Gemini's own deep AppFunctions access was still being rolled out gradually, while third parties needed a separate Early Access Program application.
  Source: https://developer.android.com/ai/appfunctions

- **Reading screen/mic/camera context**: The EU decision explicitly lists this as one of the 11 gaps to be closed — "ambient data" (real-time sensor streams from microphone, camera, screen, speakers) and "context-aware intelligence" (proactive suggestions based on screen contents) are enumerated as Gemini-exclusive capabilities today that rivals must be given equivalent access to, with consent.
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en

- **Background execution**: Gemini reportedly enjoys different (less-restricted) background-execution conditions than third-party apps, which are more aggressively suspended by Android's battery/OS management when inactive/screened-off; the decision mandates "transparent, non-discriminatory rules" for equal background execution.
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en

- Independent technical framing (Android Authority, citing the Commission): rival assistants today have "limited access to key functionalities" that prevents them competing with Google's vertically integrated stack.
  Source: https://www.androidauthority.com/eu-android-ai-google-search-mandates-3688186/

- Yale economist Fiona Scott Morton (on-record support for the Commission's technical framing): the specification "correctly identifies the four access points" — invocation surfaces, screen context, cross-app task execution, hardware resources — that determine whether "a rival AI assistant can function as a genuine device-level service."
  Source: https://www.techtimes.com/articles/320760/20260716/eu-gives-rival-ai-assistants-system-level-android-access-google-reserved-gemini.htm
  UNVERIFIED (secondary sourcing) — could not independently confirm this quote against a primary Scott Morton statement/paper; flagging as reported-by-TechTimes only.

---

## 4. PRECEDENT — March 2025 Apple DMA interoperability decisions

- **19 March 2025**: European Commission adopted two specification decisions ordering Apple, under DMA interoperability obligations, to: (1) open **nine iOS connectivity features** to third-party device makers/developers — covering smartwatches, headphones, and TVs, including faster peer-to-peer Wi-Fi data transfer, NFC features, and simplified device pairing; and (2) improve its interoperability request-handling process (better technical documentation access, faster communication/status updates, more predictable review timelines). Preceded by a public consultation launched 18 December 2024.
  Source: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-under-digital-markets-act-facilitate-development-innovative-products-2025-03-19_en ; https://techcrunch.com/2025/03/19/eu-sends-apple-first-dma-interoperability-instructions-for-apps-and-connected-devices/

- **Apple's reaction (19 March 2025)**: "Today's decisions wrap us in red tape, slowing down Apple's ability to innovate for users in Europe and forcing us to give away our new features for free to companies who don't have to play by the same rules." Apple also argued the rules would force exposure of unencrypted user data (e.g., notification contents, Wi-Fi network details) to third parties, discourage EU-market feature development, single Apple out unfairly among gatekeepers, and prevented Apple from warning users about risks.
  Source: https://techcrunch.com/2025/03/19/eu-sends-apple-first-dma-interoperability-instructions-for-apps-and-connected-devices/

- **Current status / appeal outcome**: Apple challenged its DMA gatekeeper designation and related obligations at the EU General Court (Cases T-1079/23, T-1080/23, T-214/24). On **8 July 2026**, the General Court **ruled against Apple**, rejecting its arguments that (a) Article 6(7) DMA violates EU Charter property rights [court found this wasn't the legal basis for gatekeeper designation], (b) Apple's multiple national App Stores aren't a single "core platform service" [court held they serve "the same purpose... to intermediate between end users and business users"], and (c) iMessage's classification as a number-independent communications service was wrongly applied [ruled inadmissible on procedural grounds since iMessage wasn't named an "important gateway" in the original designation]. The ruling also established what competition lawyers call a "sequencing rule": gatekeepers cannot pre-emptively challenge specification/enforcement decisions in court before the Commission actually issues them — Apple's broader interoperability complaints were told to "come back in another case." This closed Apple's (and by extension Google's) route to delay the AI-interoperability and search-data orders via injunction.
  Source: https://www.eff.org/deeplinks/2026/07/european-court-apple-can-not-shirk-its-interoperability-requirements ; sequencing-rule characterization and Google implication also at https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm
  Additional confirming coverage: https://legalblogs.wolterskluwer.com/competition-blog/the-general-court-rejects-apples-appeal-on-its-designation-decision-cases-t-107923-t-108023-and-t-21424/ ; https://www.courthousenews.com/apple-loses-eu-court-fight-over-big-tech-gatekeeper-rules/

- **Related Apple/AI angle**: Facing DMA-driven demands that Apple give "any virtual assistant direct access to users' private data," Apple has **not launched its new Siri AI in the EU with iOS 27**, with no timeline given for EU availability — Apple proposed a "Trusted System Agent" model to grant safe device access while preserving privacy, which was rejected/not accepted as sufficient.
  Source: https://www.macrumors.com/2026/07/16/eu-google-ai-apps-android-access/ ; iOS 27/Siri AI EU non-launch also confirmed at https://www.digitaltrends.com/phones/eu-is-forcing-google-to-give-ai-rivals-a-fair-shot-on-android-and-your-wallet-might-benefit/

---

## 5. ANALYST/EXPERT COMMENTARY — Gemini's distribution advantage & EU-only vs. global pattern

- **Dirk Auer, Director of Competition Policy, International Center for Law & Economics (ICLE)** — critical of the decision: argues Google is actually the *weaker* player in AI assistants ("ChatGPT accounts for roughly 70 per cent of EU chatbot use, while Anthropic has grown faster than any rival over the past year") and that Gemini's Android integration is Google's "main differentiator." His view: "The decision strips the trailing player of its main differentiator and favours firms that never needed one." He warns of an Apple-style pattern repeating: "Apple faced a similar demand and kept Siri AI off European iPhones entirely" and predicts Google may similarly restrict Gemini capabilities in the EU, so users could "get less, not more."
  Source: https://laweconcenter.org/eus-android-ai-mandate-could-leave-europeans-with-less-choice/

- **Runar Bjorhovde, analyst, Omdia** — on competitive stakes for Google: "The question is what the implications for Google or the consumer might be if the user can utilize ChatGPT to book an Uber, completely bypassing the need to engage with Android."
  Source: https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/

- **Calli Schroeder, Electronic Privacy Information Center (EPIC)** — skeptical of Google's/Apple's privacy defenses, suggesting scrutiny of the companies' own historical privacy practices before accepting their objections at face value.
  Source: https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/

- **Michael Parekh (independent analyst/newsletter)** — calls the rulings "big, show-stopping" with "far-reaching consequences" for Google's Android position; frames the EU's approach (mandating openness, driving Apple to withhold Siri AI from the EU) as contributing to a broader **"balkanization of AI markets"** beyond the fragmentation already seen with China.
  Source: https://michaelparekh.substack.com/p/ai-europes-dma-rulings-set-tough

- **EU-only vs. global pattern — Google's history**: Confirmed concrete precedent that Google applies DMA remedies EU-only rather than globally. Google **removed the Android "Choice Screen"** (lets users pick a default search engine at device setup) **in Switzerland** while keeping it across the EEA/UK. Switzerland's competition authority (WEKO) opened a preliminary investigation on 14 July 2026 into whether this violates Swiss cartel law, noting: "Default settings play a crucial role in digital markets... eliminating this feature could restrict the visibility of search engines that compete with Google during device setup, thereby increasing barriers to market entry." Timeline: EU/Google agreed to EEA+UK-wide choice screens in March 2020; Google was designated a DMA gatekeeper in September 2023; choice screens were expanded to meet DMA requirements in March 2024; Switzerland (no DMA-equivalent law) had assumed Google would voluntarily extend the same standard, but it did not.
  Source: https://www.euronews.com/next/2026/07/14/google-gives-swiss-android-users-fewer-search-options-than-their-eu-counterparts-regulator
  This directly supports the "EU-only, not global" pattern referenced in the assignment — Google's default posture with DMA-driven changes (choice screens) has been geographic/jurisdiction-limited compliance, not voluntary worldwide rollout.

- **Consumer/pricing angle**: Coverage speculates that opening Android could let users run ChatGPT or Claude with Gemini-level integration without switching phones, and notes cheaper Chinese models (DeepSeek, Kimi, MiniMax) are "ten to a hundred times cheaper" than incumbents — implying downward price pressure — but premium tiers across all providers will likely remain paywalled. This is speculative commentary, not a quantified forecast from a named analyst.
  Source: https://www.digitaltrends.com/phones/eu-is-forcing-google-to-give-ai-rivals-a-fair-shot-on-android-and-your-wallet-might-benefit/

---

## SOURCES CONSULTED BUT FAILED / UNUSABLE
- https://www.cnbc.com/2026/07/16/google-required-to-open-up-to-ai-search-engine-rivals-under-eu-mandated-changes.html — 403 error, could not fetch
- https://www.euronews.com/my-europe/2026/07/16/eu-orders-google-to-share-search-data-open-android-to-ai-rivals-competitors — returned corrupted/unreadable content
- https://www.cnn.com/2026/07/19/tech/apple-google-ai-eu-regulations — robots.txt disallowed (used BNN Bloomberg's syndicated mirror of the same CNN Business story instead)
- https://www.theregister.com/software/2026/07/16/eu-forces-google-to-share-its-toys-with-the-other-ai-and-search-kids/5273819 — 403 error
- https://news.ycombinator.com/item?id=43776512 — 429 rate-limited
- https://m.hi-network.com/google-stopped-motorola-from-using-perplexity-as-default-assistant.html — robots.txt/SSL error (used dataconomy.com account of the same Bloomberg trial testimony instead)
- https://www.bloomberg.com/news/articles/2025-04-23/perplexity-executive-says-google-blocked-motorola-s-use-of-ai-assistant — not directly fetched (paywalled); relied on dataconomy.com's account of this reporting

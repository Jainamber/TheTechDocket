# Research Notes: EC's 16 July 2026 Google DMA Specification Decisions

Compiled 2026-07-20. Topic: European Commission decisions requiring Google to (a) give rival AI assistants equal access to Android features, and (b) share Google Search data with third-party search engines/AI chatbots, under DMA "specification proceedings."

Methodology note: WebSearch used to find sources; WebFetch used only on URLs returned by search. The WebFetch tool summarizes pages through an intermediate model rather than returning raw HTML, so wording on "verbatim" quotes was cross-checked across multiple independent fetches/outlets before being treated as reliable; discrepancies are flagged inline.

---

## 1. Official EC decision — overview

- On 16 July 2026 the European Commission issued **two binding "specification measures"/"specification decisions"** to Google under the DMA: one on AI interoperability on Android, one on sharing of Google Search data. Source: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en
- Official EC mirror of the same announcement (Shaping Europe's Digital Future / DG CNECT): https://digital-strategy.ec.europa.eu/en/news/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data — meta description confirms: "Today, the European Commission has issued two sets of binding specification measures to Google under the Digital Markets Act."
- The official EC press release carries reference number **IP/26/1634**, titled identically. URL confirmed to exist and title/meta verified, but body text was not retrievable through the fetch tool (returned only metadata): https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1634
- Proceedings were **opened 27 January 2026** (per the EC's own interoperability case-detail page) and the **final decisions were adopted 16 July 2026**. Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
- A related January 2026 EC opening announcement exists at reference IP/26/202, "Commission opens proceedings to assist Google in complying with interoperability and online search data sharing obligations under the Digital Markets Act" — found via search, not fetched for body text: https://ec.europa.eu/commission/presscorner/detail/en/ip_26_202
- Interim EC steps referenced in search results (titles only, not fetched): IP/26/887 "Commission seeks feedback on measures to ensure interoperability with Google's Android" and IP/26/825 "Commission proposes measures to Google on sharing search engine data with third parties" — both appear to be intermediate draft-measure/consultation steps between the January opening and the July final decision.
- A statutory deadline of **27 July 2026** existed for the Commission to adopt these two specification decisions (six months after the 27 January 2026 opening); the Commission acted on 16 July 2026, ahead of that deadline. Source: https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm

## 2. Decision A — AI interoperability on Android

- **Legal basis: Article 6(7) DMA**, which requires Google to provide free, effective interoperability with hardware/software features controlled by Google/Android. Case reference: **DMA.100220**. Source: https://bratby.law/dma-specification-decisions-google/ (case number corroborated independently at https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm)
- Google's own Android President Sameer Samat referred to the rule directly as "**DMA 6.7**" in his public response (see Quotes section), corroborating the article number. Source: https://x.com/ssamat/status/2078151405550903797
- Purpose per the EC: ensure competing AI services (rivals to Google's own Gemini) can access the same key Android OS functionalities Gemini has. Source: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en
- The measures cover **11 named Android features**, organized (per the EC's developer-portal case page) into four groups:
  1. **Invocation**: long-press of the home button/navigation handle to trigger a third-party assistant; always-on hotword detection (voice wake-words) — concurrent multi-assistant hotword support deferred to Android 19 by 1 August 2028.
  2. **Context**: centralized (not per-app) access to on-device app data; context-aware/proactive intelligence with user consent; "ambient data" — real-time sensor input including microphone, camera, screen contents, speakers.
  3. **Actions**: structured on-device integration with apps (Gmail, Calendar, Drive, Docs, Maps, YouTube, Messages, Phone); background/screen automation mimicking user behavior; system-level OS controls (brightness, media, do-not-disturb, Bluetooth).
  4. **Resources**: access to system-level on-device models (Gemini Nano); ability to install alternative third-party on-device models on equal hardware/background terms; background execution independent of screen state.
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
- Of the 11 features, The Hacker News' reporting frames **6 as unrestricted** (ambient data/mic/camera/screen/location/sensors; always-on hotword; long-press invocation; system-level on-device models; third-party model implementation; background execution) and **5 as subject to a certification/eligibility regime** (centralized app-data access/AppSearch; context-aware intelligence/"Magic Cue"; structured on-device integration/App Actions; screen automation/"Computer Control"; system integration covering settings, media, screenshots, notifications, power). Source: https://thehackernews.com/2026/07/eu-orders-google-to-open-android-mic.html
- For the five certification-gated features: Google must publish **draft program/certification terms by 1 February 2027**, **final terms and open applications by 1 May 2027**, and Google must issue certification decisions **within four weeks** of an application. Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en (deadline dates corroborated independently at https://bratby.law/dma-specification-decisions-google/)
- Full rollout deadline: **Android 18, by 1 August 2027** (concurrent/simultaneous hotword listening for multiple assistants deferred to **Android 19 by 1 August 2028**). Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
- Some secondary outlets round this differently — e.g., "July 2027" (medianama, https://www.medianama.com/2026/07/223-eu-orders-google-open-android-search-data-ai-rivals/) or a generic "one year from the order" framing (techi.com, https://www.techi.com/eu-google-ai-interoperability-android-dma/). Treat "1 August 2027 / Android 18" (the official EC case page) as authoritative; these are rounded paraphrases of the same date, not a contradiction requiring separate verification.
- General mandate: interoperability must be provided **free of charge** across the Android ecosystem, must be "equally effective" to Google's own solution with no unnecessary user friction, with full documentation/testing/technical support, and new functionality must reach third parties **simultaneously** with Google's own. Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
- Eligibility/security conditions are explicitly allowed for the five sensitive features, and the EC states the measures "incorporate robust safeguards to ensure that the privacy of users, device integrity and security are protected." Source: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en
- The Commission will monitor Google's implementation for **two years** via regular progress reports. Source: https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
- Concrete use-case examples given by the EC/reporting: activating a preferred AI assistant by voice ("Hey Google"-style invocation); booking a taxi; getting chat-reply suggestions; asking for location information; drafting emails; adding shopping-list items; live translation/speech-to-text; proactively surfacing a flight number during a conversation; multi-step food-ordering automation. Sources: https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en ; https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
- Context stat: **roughly 60% of EU mobile users are on Android**, cited by the EC/reporting as the basis for Google's competitive advantage. Sources: https://www.medianama.com/2026/07/223-eu-orders-google-open-android-search-data-ai-rivals/ ; https://www.techtimes.com/articles/320760/20260716/eu-gives-rival-ai-assistants-system-level-android-access-google-reserved-gemini.htm
- A separate figure — "**approximately 427 million EU smartphones**" fall under the mandate — appears in July 19 coverage of the Google/Apple dispute (see §6). Source: https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/ — UNVERIFIED against an official EC figure; treat as a single-source secondary claim.

## 3. Decision B — Google Search data sharing

- **Legal basis: Article 6(11) DMA**, requiring Google to grant third-party search-engine providers access to anonymized ranking, query, click and view data on FRAND terms. Case reference: **DMA.100209**. Source: https://bratby.law/dma-specification-decisions-google/
- Data types covered: "ranking, query, click and view data" generated by end users on both free and paid Google Search results, including queries, query metadata (language, device type), viewed URLs, user interactions with results, and ranking positions. Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
- Excluded from sharing: user account information, full search histories, precise timestamps, very long queries, rare-term queries, paid-ad result URLs, and precise interaction durations. Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
- **Eligible recipients**: providers of genuine online search-engine services, explicitly **including AI chatbots that offer search functionality**. Must have operated in the EU 2+ years (or <2 years with €50M+ capital investment), maintain 50,000+ monthly average EU users, not be sanctioned/high-risk-country-controlled entities, and process data in the EEA or an equivalent jurisdiction. Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
- **Use restriction**: recipients may use the data only to develop/optimize their own search technology/services — explicitly barred from training general-purpose AI models, improving non-search services, or systematically replicating Google's results. Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
- **Anonymization** uses a three-step, "multi-layered" method developed with privacy experts: (1) removal of direct identifiers (usernames, IPs, timestamps, filters, input format); (2) suppression of rare/sensitive terms (names, passwords, addresses, bank details) and unusually long queries; (3) **k-anonymity** with metadata generalized so each user appears in groups of a minimum **1,000 users** sharing identical location/device/language (at a 95% threshold, groups reach 29,000+ users). Plus contractual safeguards: ringfenced data environments, no third-party disclosure or re-identification, retention limits, mandatory independent audits (initial audit within 6 months, then annual). Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
- **Latency/duration**: data shared no sooner than **7 days** after the query, and no slower than Google's own internal latency where feasible; maximum access duration of **5 years per beneficiary** from first access.
- **Pricing**: Google may charge to recover incremental costs (data prep, storage, transmission/onboarding) plus a reasonable return capped at Alphabet's WACC; an exceptional operating-margin-based charge is allowed only if Alphabet shows it can't otherwise recover costs or the beneficiary operates at very large scale — **this exceptional margin does not apply to micro/small/medium enterprises**. Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
- **Implementation timeline** (per official EC case page):
  - End of **August 2026**: eligibility application form live; Google publishes a beneficiary-information webpage.
  - **September 2026**: template license agreements and test-data samples provided.
  - **November 2026**: anonymized dataset finalized; latency/data-detector technical info submitted.
  - **January 2027**: final pricing offer communicated to Commission and beneficiaries.
  Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
  - Secondary reporting summarizes this as "data sharing begins/must start January 2027" — consistent with, but a simplification of, the staged official timeline above. Sources: https://www.medianama.com/2026/07/223-eu-orders-google-open-android-search-data-ai-rivals/ ; https://ppc.land/eu-forces-90-dominant-google-to-share-its-search-data/
- Compliance/audit: independent verification audit required before access begins; annual audits thereafter; Commission can order ad hoc audits; biennial review of the measure itself; Article 8(9) DMA allows the Commission to reopen the proceeding on material fact changes. Source: https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
- Context stat: Google Search has held **90%+ market share** in the EU "for decades," per secondary reporting. Source: https://ppc.land/eu-forces-90-dominant-google-to-share-its-search-data/ — UNVERIFIED against an official EC figure in the primary decision pages (the official pages did not state a specific market-share percentage in the content retrieved).

## 4. DMA penalties for non-compliance (verified against official source)

- Official DMA framework (Article 30 DMA, general, not specific to this Google case): **fines of up to 10% of a company's total worldwide annual turnover** for non-compliance, **up to 20% for repeated infringement**, and **periodic penalty payments of up to 5% of average daily turnover**. Beyond fines, the Commission can impose behavioral/structural remedies, including divestiture as a last resort. Source: https://digital-markets-act.ec.europa.eu/about-dma_en
- Applied to this case specifically: non-compliance with the two specification decisions "carries fines of up to 10% of Alphabet's worldwide annual turnover." Source: https://bratby.law/dma-specification-decisions-google/
- Multiple outlets note the 16 July 2026 items are **specification decisions, not non-compliance/fine findings** — no fine was levied by these two decisions themselves; they set forward-looking binding technical requirements, and financial penalties would only apply for future non-compliance with them. Sources: https://dig.watch/updates/eu-commission-google-android-search-under-dma (dated 18 July 2026, states "No financial penalties imposed" and explicitly labels these "specification decisions, not breach determinations") ; https://ieu-monitoring.com/editorial/eu-commission-sets-binding-rules-for-google-on-android-ai-interoperability-and-search-data-sharing/1245838 ; https://www.techtimes.com/articles/319587/20260703/eu-court-seals-41b-google-android-fine-triggering-damages-threat-rivals.htm

## 5. Commissioner quotes (verbatim, cross-checked across sources)

**Teresa Ribera**, Executive Vice-President for a Clean, Just and Competitive Transition and Commissioner for Competition (exact title confirmed independently at her official EC bio: https://commission.europa.eu/about/organisation/college-commissioners/teresa-ribera_en):

> "Society is going through a profound digital transformation. We need to keep that process fair and ensure that our citizens have choice."

Sourced to the official EC mirror https://digital-strategy.ec.europa.eu/en/news/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data , and corroborated independently (same quote, near-identical wording) by two secondary outlets: https://ieu-monitoring.com/editorial/eu-commission-sets-binding-rules-for-google-on-android-ai-interoperability-and-search-data-sharing/1245838 and https://ppc.land/eu-forces-90-dominant-google-to-share-its-search-data/ (latter renders it split across two sentences: "Society is going through a profound digital transformation" ... helping "smaller competitors ... to compete and provide that choice, while protecting user's privacy").

Note: one outlet (Brussels Signal, https://brusselssignal.eu/2026/07/eu-orders-google-to-share-search-data-and-open-android-to-ai-rivals/) rendered a differently-worded line attributed to Ribera ("Unlock innovation and choice for businesses and consumers while ensuring companies controlling key digital platforms could not leverage their dominant position to exclude rivals") — this reads as a paraphrase rather than a direct quote and could not be independently corroborated verbatim elsewhere; treat that specific phrasing as UNVERIFIED. Also note: several secondary sources (Brussels Signal, digital-strategy.ec.europa.eu fetch, thenextweb) render her name "Ribiera" — this is confirmed a misspelling; correct spelling is **Ribera** (verified via her official EC biography page and Wikipedia).

**Henna Virkkunen**, Executive Vice-President for Tech Sovereignty, Security and Democracy:

> "Thanks to these measures, we hope to see emerging alternatives to Google Search and Google's AI services, such as Gemini, and that users in the EU can enjoy greater choice of services."

This exact wording is sourced to the **AP wire story** (confirmed AP byline, see §7) as republished by ABC News: https://abcnews.com/Technology/wireStory/eu-forces-google-share-search-data-open-android-134811713 — and corroborated in substance by https://digital-strategy.ec.europa.eu/en/news/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data (official EC mirror, rendered there as "With today's measures, we want to support innovation and diversity in the European Union, enabling fair competition in the markets of AI assistant for Android devices and search engines") and by Brussels Signal. The two renderings (EC mirror vs. AP) look like different sentences from the same longer quote block rather than conflicting statements — likely: "With today's measures, we want to support innovation and diversity in the European Union, enabling fair competition in the markets of AI assistants for Android devices and search engines. Thanks to these measures, we hope to see emerging alternatives to Google Search and Google's AI services, such as Gemini, and that users in the EU can enjoy greater choice of services." This reconstruction is a reasonable inference from convergent partial quotes, not a directly-read single verbatim block — flagged accordingly.

## 6. Google's official response

**Kent Walker**, President of Global Affairs, Google & Alphabet — blog post "The DMA should not undercut security & privacy for Europeans," published 16 July 2026 on blog.google:
https://blog.google/company-news/inside-google/around-the-globe/google-europe/the-dma-should-not-undercut-security-privacy-for-europeans/

> "This Android ruling threatens device security by granting external apps sensitive and powerful device permissions without these safeguards."

> "Europeans' private searches would be exposed to unfamiliar companies, without adequate anonymisation of the data and without user knowledge or consent."

> "Today's decisions risk undermining vital privacy and security guardrails for millions of Europeans."

> "We have repeatedly offered solutions to safeguard users while satisfying the DMA's goals, but these rulings discount extensive evidence of user harm."

A fuller version of the search-data line, per the AP wire story (https://abcnews.com/Technology/wireStory/eu-forces-google-share-search-data-open-android-134811713):

> "Europeans' private searches would be exposed to unfamiliar companies, without adequate anonymization of the data and without user knowledge or consent. This would weaken citizens' privacy, risk business trade secrets, and endanger national security."

**Sameer Samat**, Android President (title per BNN Bloomberg/CNN syndication) — posted directly on X on/around 16 July 2026:
https://x.com/ssamat/status/2078151405550903797

> "The EC is on the wrong track with DMA 6.7 and is steering toward a much worse experience for Android users. Android is far more open than any other mobile OS. Device makers can decide which assistant(s) to preload. Users can switch to any assistant that they select. This is how..." [post continues beyond what the search preview captured; full text not independently re-fetched]

This "on the wrong track" framing is also referenced secondhand at https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/ and https://www.thenews.com.pk/latest/1409594-google-and-apple-are-clashing-with-the-eu-over-ai-assistants-what-to-know , both dated 19 July 2026, noting Samat "stated the Commission 'is on the wrong track' with its rules, noting users can independently switch default assistants."

**Clare Kelly**, described as Google's senior competition counsel — quoted in coverage dated 16 July 2026:

> "Android is open by design, and we're already licensing Search data to competitors under the DMA. However, we are concerned that further rules which are often driven by competitor grievances rather than the interest of consumers, will compromise user privacy, security, and innovation."

Source: https://9to5google.com/2026/07/16/eu-dma-google-search-data-android-access-decisions/ — Note: Medianama's coverage frames this same Clare Kelly quote with the word "Earlier" (https://www.medianama.com/2026/07/223-eu-orders-google-open-android-search-data-ai-rivals/), suggesting it may originate from an earlier stage of the proceeding (e.g., the April 2026 consultation) and simply be recirculated in 16 July coverage rather than being a fresh reaction to the final decision. Flagged as a minor date-provenance uncertainty, not a fabrication risk (quote itself is corroborated across two outlets).

One further Google line, from the 19 July CNN/BNN Bloomberg coverage, attributed to Google generally (not a named individual) regarding the Android decision: Google "suggested Samsung would make key decisions regarding agent permissions, rather than Google itself." Source: https://www.thenews.com.pk/latest/1409594-google-and-apple-are-clashing-with-the-eu-over-ai-assistants-what-to-know — UNVERIFIED as a direct quote (reported as paraphrase, no direct quotation marks in the source material retrieved).

## 7. Wire-service coverage (AP)

- Confirmed AP wire story, byline "By The Associated Press," dateline **Brussels, 16 July 2026, 8:02 AM**, republished by ABC News under its wireStory syndication path: https://abcnews.com/Technology/wireStory/eu-forces-google-share-search-data-open-android-134811713
- The same AP story was found syndicated at multiple additional outlets (titles matched, not independently re-fetched for content): Rochester First (labeled "AP-EU forces Google..."), BNN Bloomberg, Audacy, Broadband Breakfast, US News. Example: https://www.rochesterfirst.com/news/tech-news/ap-eu-forces-google-to-share-search-data-and-open-android-to-rival-ai-companies/
- Direct attempts to fetch apnews.com and reuters.com original URLs did not surface a direct-domain hit in search results; the AP content was only located via syndication partners. Treat "read directly on apnews.com" as NOT achieved — content was read via the ABC News syndication mirror instead, which explicitly self-identifies as AP wire copy.
- A **Reuters-bylined original was not located** in available search results (searches returned EC/DMA and secondary-outlet pages, not a reuters.com URL). Mark Reuters coverage as **UNVERIFIED/not found**.
- CNBC coverage exists (https://www.cnbc.com/2026/07/16/google-required-to-open-up-to-ai-search-engine-rivals-under-eu-mandated-changes.html, confirmed via search) but direct fetch returned a 403 error; content could not be verified firsthand. Do not cite CNBC facts beyond the headline/URL.
- Euronews coverage exists (https://www.euronews.com/my-europe/2026/07/16/eu-orders-google-to-share-search-data-open-android-to-ai-rivals-competitors, confirmed via search, and explicitly requested by task brief) but the fetch tool returned corrupted/unparseable content on two attempts; content could not be verified firsthand. Do not cite Euronews facts beyond the headline/URL.
- New York Times: no nytimes.com URL was surfaced in any search performed; NYT coverage of this specific story is **UNVERIFIED/not found** in available results.

## 8. Reactions — policy/industry circles (not company-to-company rivals)

- **Daniel Castro**, President of ITIF (Information Technology and Innovation Foundation, a US think tank), press release dated 16 July 2026: https://itif.org/publications/2026/07/16/eu-latest-action-against-google-harmful-expansion-dma-says-itif/
  > "The Commission is turning it into a tool for dictating how successful technology companies must design and operate their products."
  > "By stretching the DMA into areas that were not its intended focus, the Commission is effectively making AI policy on the fly."
  > "Such mandates also create difficult tradeoffs involving privacy, security, and innovation that deserve careful consideration."
  Castro also warned continued perceived discriminatory treatment of US tech companies could prompt US policymakers to invoke Section 301 trade-retaliation tools (per the fetch summary; not a direct quotation).

- **Dirk Auer**, International Center for Law & Economics (ICLE) — predicted the ruling could mean *fewer* AI assistant choices for Europeans (not more), noted Google is an AI-market challenger rather than leader (citing ChatGPT holding roughly 70% EU chatbot usage share — unverified beyond this single source), warned of surveillance/credential-theft risk from mandatory access, and cited Apple's Siri-AI delay in the EU as precedent for defensive product withdrawal. Source: https://brusselssignal.eu/2026/07/eu-orders-google-to-share-search-data-and-open-android-to-ai-rivals/

- **Kay Jebelli**, Chamber of Progress — flagged privacy risks and predicted legal challenges could prompt service withdrawals. Source: https://brusselssignal.eu/2026/07/eu-orders-google-to-share-search-data-and-open-android-to-ai-rivals/

- **Daniel Friedlaender**, CCIA Europe — warned privacy concerns were being treated as secondary implementation questions, risking harm to European users. Source: https://brusselssignal.eu/2026/07/eu-orders-google-to-share-search-data-and-open-android-to-ai-rivals/

- **Calli Schroeder**, described as senior counsel for an AI & Human Rights program — cautioned against taking tech companies' privacy arguments at face value: "we have to take these tech companies' arguments with a grain of salt." Source: https://www.thenews.com.pk/latest/1409594-google-and-apple-are-clashing-with-the-eu-over-ai-assistants-what-to-know (dated 19 July 2026)

- **Rival AI/search companies (OpenAI, Anthropic, Perplexity, Microsoft, DuckDuckGo, Qwant, Ecosia)**: despite multiple targeted searches, **no on-the-record statement from any of these companies welcoming or reacting to the 16 July 2026 decisions was found** in available sources as of 20 July 2026. This is a genuine gap in coverage, not an omission — flagged as UNVERIFIED/NOT FOUND rather than assumed silence.

## 9. Developments after 16 July 2026 (17–20 July window)

- **19 July 2026**: CNN Business published "Google and Apple are clashing with the EU over the future of AI assistants," syndicated widely (BNN Bloomberg, KESQ, KTEN, ABC17News, thenews.com.pk). Direct CNN.com fetch was blocked by robots.txt; content read via syndication mirrors:
  - https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/
  - https://www.thenews.com.pk/latest/1409594-google-and-apple-are-clashing-with-the-eu-over-ai-assistants-what-to-know
  - Key content: Apple's context is folded into the same story — Apple announced in June 2026 it would **not launch its new Siri AI assistant on EU iPhones/iPads** citing DMA requirements, arguing the rules would "give any virtual assistant direct access to users' private data," while saying it had proposed alternative solutions that were rejected by regulators (one fetch rendered this as "rejected by U.S. authorities," which appears to be a tool-summarization error given the context is EU regulation — treat "rejected by regulators" as the safer, corroborated framing and the "U.S. authorities" detail as UNVERIFIED/likely erroneous).
  - Sameer Samat's "wrong track" quote (see §6) is referenced in this 19 July coverage, alongside Kent Walker's "sensitive and powerful device permissions" line — indicating this is a rounder follow-up on both companies' resistance rather than a new development from Google itself.
- **No formal Google legal appeal to the EU General Court had been announced** in any source found as of 20 July 2026. Bratby Law's analysis (published in the days after 16 July) explicitly states: "Google has publicly objected but had not announced a General Court challenge at the time of publication." Source: https://bratby.law/dma-specification-decisions-google/. Status as of 20 July 2026: UNVERIFIED/NOT YET FILED per available sources — could change without warning.
- **Separate "record" DMA fine (self-preferencing/anti-steering) — NOT the same action as the two specification decisions**: multiple sources reported the Commission was expected to also fine Google in the "hundreds of millions of euros" for (1) Google Search self-preferencing of Shopping/Flights/Hotels (alleged Article 6(5) violation) and (2) Google Play Store anti-steering restrictions (alleged Article 5(5) violation), potentially exceeding the prior €500 million DMA record, with the Commission said to be targeting a decision before its August summer recess. Source: https://www.techtimes.com/articles/320759/20260716/eu-fires-record-dma-fine-google-over-search-play-store-violations.htm (published 16 July 2026, framed as imminent/expected, NOT yet confirmed issued). No source found in this research confirms this fine was actually announced/issued between 17–20 July 2026 — status: UNVERIFIED/PENDING. Do not conflate with the two specification decisions that are the main subject of this file — different legal articles (6(5)/5(5) vs. 6(7)/6(11)), different case type (fine for past conduct vs. forward-looking binding measures).

## 10. Related but separate background context (do not conflate with the July 16 decisions)

- **€4.1 billion Google Android antitrust fine** (originally €4.34bn in 2018, reduced to €4.125bn by the General Court in 2022, case C-738/22 P) was **confirmed as legally final by the Court of Justice of the EU on 2 July 2026**, closing all appeals. This is a wholly separate, older Article 102/TFEU-type case about Android bundling/exclusivity/anti-fragmentation practices predating the DMA specification proceedings, not a DMA specification matter. Source: https://www.techtimes.com/articles/319587/20260703/eu-court-seals-41b-google-android-fine-triggering-damages-threat-rivals.htm
- **8 July 2026**: EU General Court (Eighth Chamber) dismissed all three of **Apple's** legal challenges to its own DMA gatekeeper designation, establishing what the source calls a "sequencing rule" — gatekeepers cannot seek judicial review of DMA obligations before the Commission issues a specific enforcement/specification decision. This ruling is about Apple, not Google, but is cited as the reason Google could not obtain a pre-emptive injunction to delay the 16 July Google decisions. Source: https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm

---

## Source list (all URLs actually read via WebFetch, or relied upon for direct quoted search-snippet text)

Official EU sources:
1. https://digital-markets-act.ec.europa.eu/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data-under-2026-07-16_en
2. https://digital-markets-act.ec.europa.eu/developer-portal/interoperability/alphabet-specification-proceedings-interoperability-ai-services_en
3. https://digital-markets-act.ec.europa.eu/developer-portal/data-access/alphabet-specification-proceedings-sharing-google-search-data_en
4. https://digital-markets-act.ec.europa.eu/about-dma_en
5. https://digital-strategy.ec.europa.eu/en/news/commission-provides-guidance-google-ai-interoperability-android-and-sharing-google-search-data
6. https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1634 (metadata only)
7. https://commission.europa.eu/about/organisation/college-commissioners/teresa-ribera_en (title verification)

Google primary sources:
8. https://blog.google/company-news/inside-google/around-the-globe/google-europe/the-dma-should-not-undercut-security-privacy-for-europeans/
9. https://x.com/ssamat/status/2078151405550903797

Wire/news outlets read directly:
10. https://abcnews.com/Technology/wireStory/eu-forces-google-share-search-data-open-android-134811713 (AP wire)
11. https://thehackernews.com/2026/07/eu-orders-google-to-open-android-mic.html
12. https://9to5google.com/2026/07/16/eu-dma-google-search-data-android-access-decisions/
13. https://www.techi.com/eu-google-ai-interoperability-android-dma/
14. https://www.medianama.com/2026/07/223-eu-orders-google-open-android-search-data-ai-rivals/
15. https://brusselssignal.eu/2026/07/eu-orders-google-to-share-search-data-and-open-android-to-ai-rivals/
16. https://bratby.law/dma-specification-decisions-google/
17. https://www.techtimes.com/articles/320760/20260716/eu-gives-rival-ai-assistants-system-level-android-access-google-reserved-gemini.htm
18. https://www.techtimes.com/articles/320759/20260716/eu-fires-record-dma-fine-google-over-search-play-store-violations.htm
19. https://www.techtimes.com/articles/320011/20260709/eu-court-ruling-gives-google-18-days-open-android-ai-layer-blocks-last-legal-defense.htm
20. https://www.techtimes.com/articles/319587/20260703/eu-court-seals-41b-google-android-fine-triggering-damages-threat-rivals.htm
21. https://dig.watch/updates/eu-commission-google-android-search-under-dma
22. https://ieu-monitoring.com/editorial/eu-commission-sets-binding-rules-for-google-on-android-ai-interoperability-and-search-data-sharing/1245838
23. https://ppc.land/eu-forces-90-dominant-google-to-share-its-search-data/
24. https://itif.org/publications/2026/07/16/eu-latest-action-against-google-harmful-expansion-dma-says-itif/
25. https://www.macrumors.com/2026/07/16/eu-google-ai-apps-android-access/
26. https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/07/19/google-and-apple-are-clashing-with-the-eu-over-the-future-of-ai-assistants/
27. https://www.thenews.com.pk/latest/1409594-google-and-apple-are-clashing-with-the-eu-over-ai-assistants-what-to-know

Attempted but NOT successfully read (do not treat as sources for any fact above):
- CNN.com direct (robots.txt blocked): https://www.cnn.com/2026/07/19/tech/apple-google-ai-eu-regulations
- CNBC (403 error on fetch): https://www.cnbc.com/2026/07/16/google-required-to-open-up-to-ai-search-engine-rivals-under-eu-mandated-changes.html
- Euronews (fetch returned corrupted/unparseable content twice): https://www.euronews.com/my-europe/2026/07/16/eu-orders-google-to-share-search-data-open-android-to-ai-rivals-competitors
- TechRadar "not collaborative" quote page (proxy rejected the request): https://www.techradar.com/vpn/vpn-privacy-security/google-is-not-collaborative-and-not-in-the-spirit-of-complying-with-this-regulation-can-the-eu-commission-strong-arm-google-into-levelling-the-playing-field-of-the-search-engine-market-and-is-this-really-in-the-interest-of-your-privacy

## Explicit UNVERIFIED / not-found list

1. Reuters original article on this topic — not found in search results.
2. New York Times original article on this topic — not found in search results.
3. Euronews article content — URL confirmed to exist, but content unreadable via available tools (garbled fetch twice).
4. CNBC article content — URL confirmed to exist, but fetch blocked (403).
5. Whether the separate "record" self-preferencing/anti-steering DMA fine was actually issued between 17–20 July 2026 — reported as imminent/expected on 16 July, no confirmation of issuance found.
6. Whether Google has filed (or announced intent to file) a formal General Court appeal against either specification decision — not found as of 20 July 2026; Bratby Law explicitly notes none had been announced at time of its publication.
7. Any on-the-record reaction from OpenAI, Anthropic, Perplexity, Microsoft, DuckDuckGo, Qwant, or Ecosia — none found.
8. The precise verbatim EC press-release paragraph containing the Ribera and Virkkunen quotes side-by-side — reconstructed from convergent partial quotations across 4 sources (official EC mirror + AP wire + 2 secondary outlets) rather than read as one continuous primary-source block, since the official presscorner ip_26_1634 page and the digital-markets-act.ec.europa.eu page both returned only summarized/partial content through the fetch tool.
9. Brussels Signal's alternate phrasing of the Ribera quote ("Unlock innovation and choice for businesses and consumers...") — could not be corroborated verbatim elsewhere; likely a paraphrase rather than a direct quote.
10. ChatGPT's "~70% EU chatbot usage share" figure cited by ICLE's Dirk Auer — single-sourced, not independently verified against market-data.
11. "427 million EU smartphones" figure (BNN Bloomberg/CNN syndication, 19 July) — single-sourced, not corroborated against an official EC figure.
12. Google's "Samsung would make key decisions regarding agent permissions" line — reported as paraphrase, not a direct quotation; attribution to a named Google spokesperson unclear.

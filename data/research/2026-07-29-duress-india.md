# Research: GrapheneOS Duress Wipe / US Border Search Case — India + Global Angle (2026-07-29)

Context anchor: Samuel (Sam) Tunick, an Atlanta resident, is being federally prosecuted after his
GrapheneOS phone's "duress password" feature allegedly wiped the device during a CBP secondary
inspection at Hartsfield-Jackson Atlanta International Airport on **January 24, 2025**. The case became
national news around **July 24-28, 2026** when TechCrunch and others reported on it. This file covers the
technical/legal/India research requested, organized by the six assignment sections.

Confidence key: every fact has its source URL inline. **PRIMARY** = official
documentation/government/company source. Items I could not verify or that are explicitly flagged as
unconfirmed in the reporting itself are marked **UNVERIFIED**.

---

## 0. The news case itself (context anchor, not a numbered research item but needed throughout)

- Defendant: **Samuel ("Sam") Tunick**, described as an Atlanta activist/resident. Detained in secondary
  inspection at **Hartsfield-Jackson Atlanta International Airport** on **January 24, 2025**, returning
  from overseas travel (Dominican Republic, per one source).
  https://techcrunch.com/2026/07/24/us-accuses-american-of-allegedly-wiping-his-phone-using-a-duress-password-during-border-search/
  https://www.medianama.com/2026/07/223-us-grapheneos-duress-password-case/
  — Note: one secondary source (CyberInsider) states "January 2024," which conflicts with the two more
  detailed reports (TechCrunch, MediaNama) both citing January 24, **2025**. Treat 2025 as correct;
  flagging the discrepancy. https://cyberinsider.com/grapheneos-defends-security-model-after-us-prosecutors-target-user/
- CBP agents said they were searching for child exploitation imagery; Tunick's defense argues the real
  motive was his alleged connection to "Stop Cop City" environmental/police-training-facility activism,
  and that he'd been placed on a watchlist for that. https://techcrunch.com/2026/07/24/us-accuses-american-of-allegedly-wiping-his-phone-using-a-duress-password-during-border-search/
- What happened: after Tunick allegedly entered his duress passcode, "the screen went blank, flashed
  several times and the phone appeared to restart." Agents seized the device anyway before releasing him.
  https://techcrunch.com/2026/07/24/us-accuses-american-of-allegedly-wiping-his-phone-using-a-duress-password-during-border-search/
- Charge: federal statute against knowingly destroying property to prevent its lawful seizure — this is
  **18 U.S.C. § 2232** ("Destruction or removal of property to prevent seizure"), max penalty **fine
  and/or up to 5 years imprisonment** (uniform across subsections (a)-(e)).
  https://www.law.cornell.edu/uscode/text/18/2232
  — His federal public defender, Matthew Dodge, called use of this statute in an indictment "incredibly
  rare" / "highly unusual." https://techcrunch.com/2026/07/24/us-accuses-american-of-allegedly-wiping-his-phone-using-a-duress-password-during-border-search/
  https://www.medianama.com/2026/07/223-us-grapheneos-duress-password-case/
- Tunick has pleaded not guilty; a suppression ruling is expected later in 2026. Defense also alleges he
  was denied attorney access and not read his rights during the stop.
  https://www.ibtimes.co.uk/us-federal-case-duress-passcodes-border-1810655
- Security researchers (Runa Sandvik of Granitt, Bill Budington of EFF) say they know of **no prior
  prosecution** involving alleged duress-password wiping — this is described as a first-of-its-kind case.
  Both warned the prosecution could chill secure-device practices among at-risk travelers (journalists,
  activists). https://www.medianama.com/2026/07/223-us-grapheneos-duress-password-case/
- **UNVERIFIED / worth a caveat if used**: IBTimes UK reporting mentions "similar enforcement patterns
  reportedly emerging in France and Spain against journalists and lawyers using GrapheneOS" — this was
  not independently cross-verified against a second source in this research pass; treat as a claim to
  verify separately before publishing. https://www.ibtimes.co.uk/us-federal-case-duress-passcodes-border-1810655
- GrapheneOS project's public defense of the feature (via project statement, reported by CyberInsider):
  > "this feature is only one component of its broader security model and is not required to protect
  > user data from extraction." The project said "the primary defenses are hardware-backed encryption,
  > secure authentication, exploit mitigations, and physical attack protections, with the duress feature
  > simply providing an additional option for users who determine it is appropriate for their own threat
  > model." https://cyberinsider.com/grapheneos-defends-security-model-after-us-prosecutors-target-user/
  — GrapheneOS's own documentation separately warns: "some jurisdictions could interpret a triggered
  wipe as evidence destruction rather than the use of a preconfigured security tool" (per MediaNama's
  paraphrase of GrapheneOS docs). https://www.medianama.com/2026/07/223-us-grapheneos-duress-password-case/
- Other press covering the case for cross-referencing/quotes if needed: Cybernews
  (https://cybernews.com/privacy/atlanta-man-border-search-prosecuted-grapheneos/), Slashdot
  (https://yro.slashdot.org/story/26/07/28/1652243/grapheneos-defends-data-wiping-function-that-blocked-us-border-search),
  Android Authority (https://www.androidauthority.com/grapheneos-duress-pin-us-prosecution-3691271/),
  Neowin (https://www.neowin.net/news/man-charged-for-wiping-grapheneos-phone-using-duress-password-during-airport-checks/),
  Yahoo/Tech (https://tech.yahoo.com/phones/article/can-you-be-prosecuted-for-wiping-your-phone-at-the-border-180334326.html),
  CP24 (https://www.cp24.com/news/world/2026/07/28/american-activist-charged-after-phone-wiped-during-airport-search-in-entirely-unprecedented-case/),
  US News "Decision Points" (https://www.usnews.com/news/u-s-news-decision-points/articles/2026-07-27/border-battle-when-wiping-your-own-phone-is-a-crime — fetch blocked by 403 in this session, but confirmed live/indexed via WebSearch, worth a manual check).

---

## 1. GrapheneOS Duress PIN/Password — OFFICIAL documentation **[PRIMARY: grapheneos.org]**

Source fetched directly: **https://grapheneos.org/features** (official GrapheneOS features page).

- **What it does, verbatim from the docs**: "GrapheneOS provides users with the ability to set a duress
  PIN/Password that will irreversibly wipe the device (along with any installed eSIMs) once entered
  anywhere where the device credentials are requested." **PRIMARY** — https://grapheneos.org/features
- **What gets wiped**: device contents (all hardware-keystore encryption keys, rendering OS data
  unrecoverable — per secondary explainer corroborating the official page, see below) plus any installed
  **eSIMs**. **PRIMARY (device+eSIM claim)** — https://grapheneos.org/features
- **Speed / irreversibility**: "The wipe does not require a reboot and cannot be interrupted." This is
  explicitly contrasted with a standard/normal device wipe, which typically requires a reboot to
  complete. **PRIMARY** — https://grapheneos.org/features
  — GrapheneOS's own official X/Twitter announcement of the feature used near-identical framing: "It
  near instantly wipes and shuts down." (Quoted in WebSearch snippet of the GrapheneOS X account post
  announcing the release; X post itself blocked by robots.txt for direct fetch in this session, but the
  quote appeared verbatim in indexed search results.) https://x.com/GrapheneOS/status/1797273954119282884
- **Setup location** (official): Settings > Security & privacy > Device unlock > Duress Password, within
  the owner profile. **PRIMARY** — https://grapheneos.org/features
- **Separate PIN vs. password handling**: GrapheneOS maintains distinct duress credentials — one PIN for
  PIN-entry contexts, one password for password-entry contexts; both must be configured to enable the
  feature. The duress PIN also triggers a wipe if used as the two-factor fingerprint-unlock PIN, but
  **not** when entered as a SIM PIN. **PRIMARY** — https://grapheneos.org/features
- **Safety caveat (official)**: if the duress credential happens to match the real/authentic unlock
  credential, the authentic unlock takes precedence — preventing accidental self-wipe. **PRIMARY** —
  https://grapheneos.org/features
- **When it was added**: Feature shipped in **GrapheneOS release version 2024053100** (GrapheneOS
  versions encode the release date as YYYYMMDDxx, so this is late May 2024; a build/release tracking
  site cites the effective release date as **June 2, 2024**). GrapheneOS's own X announcement called it
  "the long awaited duress PIN/password implementation," indicating it had been a long-requested feature
  before shipping. https://www.nobsbitcoin.com/grapheneos-v2024053100/ and
  https://x.com/GrapheneOS/status/1797273954119282884 (secondary confirmation, not grapheneos.org itself,
  since the public releases changelog page as fetched in this session only showed recent 2026 entries
  and didn't scroll back far enough to independently confirm — flagging the exact date as
  **sourced from a secondary release-tracking site, not directly re-verified on grapheneos.org/releases
  in this session**).
- **What the project says it's for**: a security tool for users under coercion — "situations where a
  user is forced to provide access under threat or coercion" (per secondary paraphrase of official
  framing). GrapheneOS's defense statement in the Tunick case (see Section 0) frames it as one optional
  layer among several, "for users who determine it is appropriate for their own threat model" — i.e.
  explicitly NOT positioned as the primary defense (hardware encryption is), but as an extra opt-in tool
  for high-risk users (journalists, activists, domestic-violence survivors, people facing forced device
  handover). https://cyberinsider.com/grapheneos-defends-security-model-after-us-prosecutors-target-user/
- Independent user account (Android Authority) corroborating the official description: "a complete and
  irreversible wipe of your device," happening "instantly," described as a "silent and irreversible
  factory reset in the background," with "no confirmation prompts, no announcements, and no obvious
  signs that the wipe was intentional." https://www.androidauthority.com/grapheneos-duress-pin-3584795/

## 2. What GrapheneOS is (brief)

- Security- and privacy-focused **Android Open Source Project (AOSP) fork**. Hardens the OS via things
  like hardened memory allocator/exploit mitigations, sandboxed Google Play Services (optional), strict
  permission controls, and more frequent security patching than most OEMs.
  https://en.wikipedia.org/wiki/GrapheneOS ; official project homepage: https://grapheneos.org/
- **Device support**: currently **Google Pixel devices only** (hardware requirements — verified boot
  with alternate OS support, secure element, etc.). Notably, **in March 2026 GrapheneOS announced a
  partnership with Motorola** to bring official support to future flagship Snapdragon devices, expected
  Q4 2026/Q1 2027 — so "Pixel-only" is accurate as of today (July 2026) but changing soon.
  https://en.wikipedia.org/wiki/GrapheneOS
- **History**: founded April 2019 as a successor project to CopperheadOS; the nonprofit GrapheneOS
  Foundation (Canadian) was formally established March 2023; principal developer is Daniel Micay.
  Reported ~400,000 active users as of April 2026 (Wikipedia, sourcing not independently re-verified
  beyond the Wikipedia citation in this pass — flag as secondary-sourced figure).
  https://en.wikipedia.org/wiki/GrapheneOS
- **Who uses it**: privacy-conscious users generally, journalists, activists, and security researchers;
  popular in the "de-Google" community. Notable endorsement: Edward Snowden tweeted in 2019, "If I were
  configuring a smartphone today, I'd use @DanielMicay's @GrapheneOS as the base operating system."
  https://en.wikipedia.org/wiki/GrapheneOS

## 3. Do stock Android or iOS have anything similar?

**iOS — "Erase Data" option (official Apple documentation)** **[PRIMARY: support.apple.com]**
- Source: https://support.apple.com/guide/security/passcodes-and-passwords-sec20230a10d/web
- Exact official language: "If the Erase Data option is turned on for iPad, iPhone, or Apple Vision Pro
  (in Settings > [Optic ID/Face ID/Touch ID] & Passcode), after **10 consecutive incorrect attempts** to
  enter the passcode, all content and settings are removed from storage."
- It is **opt-in** (off by default; user must enable it).
- "Consecutive attempts of the same incorrect passcode don't count toward the limit" — i.e., only
  distinct wrong codes increment the counter.
- MDM/enterprise device management can enforce this at a lower failed-attempt threshold.
- **Key difference from GrapheneOS duress feature**: this is a brute-force-lockout wipe (triggered by
  repeated *wrong* guesses), not a "type this specific different code to secretly self-destruct while
  looking like you complied" duress mechanism. There is no dedicated Apple-documented "duress
  code/decoy password that wipes on demand" feature found in official Apple docs in this research pass.

**Android — Theft Protection features (official Google documentation)** **[PRIMARY: support.google.com, android.com]**
- Sources: https://support.google.com/android/answer/15146908?hl=en and
  https://www.android.com/intl/en_in/articles/android-theft-protection/ (the second is Google's own
  India-locale page, i.e. equally official)
- Features documented: **Theft Detection Lock** (AI/sensor-based — detects phone being snatched via
  motion/Wi-Fi/Bluetooth signals and auto-locks the screen); **Offline Device Lock** (auto-locks screen
  after extended offline period, up to twice per 24 hours); **Remote Lock** (lock via phone number at
  android.com/lock, optional security question); **Factory Reset Protection / FRP** (Google account
  required to reactivate a phone after factory reset, deterring resale of stolen phones); **Find My
  Device** remote erase.
- **Notable absence, explicitly confirmed by fetching both official pages**: neither page mentions any
  duress PIN, panic-button, or auto-wipe-on-specific-code feature. Google's stock approach is oriented
  toward **theft deterrence and remote recovery/control**, not a self-triggered destructive wipe under
  coercion. This is a genuine and citable point of contrast with GrapheneOS.

**OEM-level duress features**: no official Samsung/OnePlus/etc. documentation of a duress-PIN-style
wipe feature was found in this research pass (not deeply searched beyond stock Android/Google — flagging
as a gap if the piece wants OEM-by-OEM comparison; recommend a follow-up search if needed).

## 4. INDIA ANGLE

### 4(a) — Indian travel/visa volume to the US

- **Indian visits to the US: 2 million+** in the **Jan-Nov 2024** period, per the **U.S. International
  Trade Administration** (cited by Skift), up **26%** year-on-year vs. the same period in 2023, and above
  pre-COVID levels (1.37 million Indian visitors in the same Jan-Nov window of 2019).
  https://skift.com/2025/01/06/u-s-records-over-2-million-indian-visits-surpassing-pre-covid-numbers-india-report/
  — Note: a separate 2025 report (Travel Span) headlines a **6% dip** in Indian visitor numbers in 2025
  after years of growth, and Forbes reported a **15% drop in August 2025** amid geopolitical tensions —
  useful if the piece wants a "numbers are large but softening" framing, though these weren't deep-fetched
  for exact figures in this pass. https://travelspan.in/indian-visitor-numbers-to-the-united-states-dip-6-in-2025-after-years-of-growth/
  https://www.forbes.com/sites/suzannerowankelleher/2025/09/18/indian-tourists-us-dropped-august-geopolitical-tensions-trade-deal/
- **H-1B visas**: Indians received **73% of all H-1B approvals** in fiscal year 2023, per **Pew Research
  Center**'s analysis of USCIS data — "roughly three-quarters (73%) of H-1B workers whose applications
  were approved in fiscal 2023 were born in India," and a majority of approvals every year since 2010
  have gone to India-born workers. https://www.pewresearch.org/short-reads/2025/03/04/what-we-know-about-the-us-h-1b-visa-program/
  — More recent figure: **283,772 H-1B visa approvals for Indians in FY2025**, per Business Standard
  (citing USCIS data). https://www.business-standard.com/amp/immigration/india-s-283-772-h-1b-visa-approvals-in-fy25-spark-fresh-us-jobs-debate-126050600401_1.html
  (secondary source; USCIS primary report also surfaced but not fetched directly:
  https://www.uscis.gov/sites/default/files/document/reports/ola_signed_h1b_characteristics_congressional_report_FY24.pdf)
- **Indian students**: **363,019 Indian students** enrolled in US colleges/universities in the **2024-25
  academic year**, per the **Institute of International Education's (IIE) Open Doors 2025 report** — a
  **10% increase** from the prior year's 331,602. Indians made up **30.8%** of all 1,177,766
  international students in the US, making India the top source country for the second consecutive year.
  https://theprint.in/india/education/17-drop-in-new-international-students-in-us-in-fall-2025-indians-remain-largest-cohort-open-doors/2785710/
  (original data source: https://opendoorsdata.org/annual-release/international-students/ — IIE, not
  independently re-fetched in this pass but is the report the news article cites)

### 4(b) — Does India have a law on phone searches at its own borders? Does DPDP Act 2023 apply to state agencies at borders?

- **Customs Act, 1962** is India's operative border-search law. Its search powers (Chapter XIII,
  Sections 100-102) are about **physical search of persons and goods** for smuggling/contraband — e.g.
  Section 100 lets a "proper officer" search any person reasonably believed to be concealing goods liable
  to confiscation or related documents; Section 101 covers specified high-value goods (gold, diamonds,
  watches, etc.); Section 102 sets procedural safeguards (right to be taken before a gazetted officer/
  magistrate, requirement for independent witnesses, female searched only by a female).
  https://www.eximguru.com/exim/indian-customs/customs-acts-1962/chapter-xiii-searches-seizure-and-arrest.aspx
  Primary legislative text: https://www.indiacode.nic.in/bitstream/123456789/15359/1/the_customs_act,_1962.pdf
  — **Important finding**: unlike the US (CBP directive), UK (RIPA), Australia (3LA), or New Zealand
  (Customs and Excise Act), **the Customs Act 1962's search provisions were not found to contain any
  explicit, dedicated language about electronic devices, encryption, or compelling disclosure of
  passcodes** — its search powers were written around physical contraband, not digital data. This is a
  genuine legal gap/gray-zone worth flagging editorially: **India does not appear to have a clear,
  dedicated statutory power (or equivalent limit) explicitly governing digital device searches/decryption
  demands at its own borders**, in contrast to the four jurisdictions in Section 5 below. Treat the
  "no dedicated digital-search law" framing as this researcher's synthesis from the primary text, not a
  direct quote from any single source — flagging as **researcher-inference, worth a lawyer's sanity check
  before publishing as a firm claim**.
- **DPDP Act 2023 and state/border agencies**: **Section 17(2)(a)** lets the **Central Government notify
  any "instrumentality of the State"** as exempt from the Act's obligations "in the interests of
  sovereignty and integrity of India, security of the State" (among other grounds) — a blanket,
  government-defined carve-out. Separately, **Section 17(1)(c)** exempts processing of personal data
  "in the interest of prevention, detection, investigation or prosecution of any offence" generally
  (not agency-specific). PRIMARY-ish text (via a legal-explainer site quoting the section):
  https://www.dpdpa.com/dpdpa2023/chapter-4/section17.html
  — **Short answer to "does DPDP apply to state agencies at borders"**: the Act does **not name customs,
  immigration, or border agencies specifically**, but its structure gives the Central Government broad
  discretion to exempt any state instrumentality (which would include Customs/Immigration/CISF at
  airports) from consent and data-protection obligations on sovereignty/security grounds, and separately
  exempts crime-investigation-related processing outright. In practice this means Indian data-protection
  law is unlikely to meaningfully constrain Indian customs/immigration data collection at the border.
  Analysis/commentary corroborating this reading: MediaNama
  (https://www.medianama.com/2023/08/223-dpdp-bill-2023-government-exemptions-3/ — quotes Justice B.N.
  Srikrishna criticizing the exemption's vagueness: "These are just broad words. What is the sovereignty
  of the nation?") and Scroll.in
  (https://scroll.in/article/1054722/indias-data-protection-law-does-little-for-privacy-while-bolstering-the-states-surveillance-powers).
  A law-journal piece also specifically interrogates this exemption:
  https://www.ijllr.com/post/state-exemptions-under-the-digital-personal-data-protection-act-2023-testing-section-17-2-a-agai
  (not fetched directly in this pass, but appears to be exactly on-point — recommend a follow-up fetch
  if a deeper legal citation is needed).

### 4(c) — Reported cases of Indian travelers' devices searched at US borders / official Indian advisories

- **No confirmed, named, on-the-record case of an Indian traveler's device being searched at a US
  border was found in this research pass.** This is a genuine gap — flagging explicitly rather than
  papering over it.
- **UNVERIFIED / explicitly caveated even by the outlet that reported it**: A July 2, 2026 American
  Bazaar article describes a **viral WhatsApp post** claiming an Indian student was denied US entry after
  CBP examined their phone and found WhatsApp group memberships (ride-share/academic groups). The article
  itself stresses: "the post lacks verification—no location, student identity, or official CBP
  confirmation exists regarding why entry was actually refused." Treat this as an unverified viral claim,
  not a documented case — but it's a legitimate "climate of concern" data point (immigration advisers
  quoted are telling students CBP can inspect "messages, photos, contacts and other digital content" and
  advising them to separate personal/academic communications on their devices).
  https://americanbazaaronline.com/2026/07/02/viral-whatsapp-post-alarms-indian-students-traveling-to-america-483966/
- Comparable (non-Indian) documented case for context/pattern: a **Pakistani national ("Dhakil")** was
  denied entry at Houston in 2019 and banned from the US for 5 years after CBP found a WhatsApp-forwarded
  image on his phone during a device search; CBP held him "responsible for all the contents on his
  phone" despite his explanation it was an unsolicited forward.
  https://techcrunch.com/2019/09/02/denied-entry-united-states-whatsapp/amp
- **Broader CBP device-search statistics (not India-specific, but useful base-rate context)**: per BNN
  Bloomberg (citing CBP data), **non-U.S. citizens made up roughly 78% of those subjected to device
  searches**; CBP conducted **14,899 electronic device searches** (incl. 1,075 "advanced" searches)
  between April-July 2025 — the highest quarterly total since late 2018, nearly double the ~8,000
  searches in the same period of FY2018. CBP itself characterizes these as "rare," affecting "just 0.01%
  of the more than 400 million passengers" who arrived at US ports of entry in the last fiscal year.
  **No breakdown by nationality/India specifically was available in this source.**
  https://www.bnnbloomberg.ca/business/international/2025/08/23/electronic-device-searches-by-us-border-officials-are-on-the-rise-data-shows/
- **No dedicated Indian government (MEA) advisory specifically about US device/phone searches was
  found.** I checked: (i) the Indian Embassy Washington DC's official "Guidelines for Indian Students in
  the United States" page — covers visa compliance, work-hour limits, safety, fraud, health insurance,
  but **contains no mention of border procedures, device searches, or customs privacy**
  (https://indianembassyusa.gov.in/extra?id=127); (ii) MEA statements on the ~1,080 Indians deported from
  the US since January 2025 (of whom 62% returned via commercial flights) — spokesperson Randhir Jaiswal
  discussed deportation cooperation and student-visa merit consideration, but **made no statement about
  device searches or border detentions specifically**
  (https://www.tribuneindia.com/news/world/since-jan-2025-1080-indians-have-been-deported-62-have-come-on-commercial-flights-mea-on-us-deportations).
  This absence-of-advisory is itself a citable, accurate point for the piece (i.e., "no dedicated MEA
  guidance exists on this specific risk, unlike Canada, which has publicly warned its citizens about
  US border agents' device-search authority" — Canada's advisory referenced in a search result title,
  https://www.aol.com/canada-warns-travelers-us-border-180040508.html, not independently fetched in this
  pass but flagged for a possible comparative line).

## 5. GLOBAL CONTEXT — key-disclosure / device-search laws in other countries

**United Kingdom — RIPA 2000, Part III, Section 49**
- Empowers authorities to compel disclosure of encryption keys or decryption of encrypted data via a
  "Section 49 Notice."
- Refusing/failing to comply: **maximum 2 years' imprisonment** in the general case.
- Enhanced penalty: **up to 5 years' imprisonment** in national-security cases (per 2006 Terrorism Act
  amendment) or child-indecency cases (per 2009 Policing and Crime Act amendment).
- Recipients of a notice can also be barred from telling anyone else about it (a "tipping-off" gag
  provision), aside from their lawyer.
- At least **three people have been prosecuted and convicted** in the UK for refusing to surrender
  encryption keys; one received a 13-month sentence.
  https://wiki.openrightsgroup.org/wiki/Regulation_of_Investigatory_Powers_Act_2000/Part_III
  (cross-referenced) https://wikimili.com/en/Key_disclosure_law

**Australia — Crimes Act 1914, Section 3LA ("assistance orders")**
- Lets law enforcement obtain an order compelling "a person with knowledge of a computer or a computer
  system" to provide "information or assistance that is reasonable and necessary" to access, copy, or
  convert data into intelligible form.
  https://sherloc.unodc.org/cld/en/legislation/aus/crimes_act_1914/part_iaa/sections_3e-3la/sections_3e-3la.html
  (fetch of full official text failed — AustLII returned 403/robots-blocked in this session; official
  primary source for a future direct check: https://www.austlii.edu.au/cgi-bin/viewdoc/au/legis/cth/consol_act/ca191482/s3la.html)
- Maximum penalty for non-compliance: **2 years' imprisonment**, per a secondary compilation (Wikimili's
  key-disclosure-law summary). **Flag: this figure came from a secondary/tertiary source because the
  primary AustLII legislative text was blocked from direct fetch in every attempt this session (403 /
  JS-redirect on multiple mirrors); I was not able to independently confirm whether this penalty has
  been amended upward since the law's original passage (e.g., by the 2018 Assistance and Access Act).
  Recommend the writer verify the current penalty figure directly against legislation.gov.au
  (https://www.legislation.gov.au/Details/C2019C00014) or AustLII before publishing a specific number.**
  https://wikimili.com/en/Key_disclosure_law

**New Zealand — Customs and Excise Act 2018**
- Took effect around October 2018. Authorizes border officials to demand "codes, passwords, and
  encryption keys" for travelers' digital devices.
- Refusal to provide a password/unlock a device: fine of **up to NZ$5,000 (≈US$3,284** at the time of
  reporting**)**.
- Officials need "reasonable cause to suspect" to conduct a "full" search (device may be detained,
  cloned, or its data copied/reviewed/evaluated).
- Reported at the time as the **first country to impose a specific financial penalty** for non-compliance
  with a digital device search at the border (other countries, including the US, already had
  seizure/search powers but not this kind of dedicated fine).
  https://time.com/5413621/new-zealand-digital-devices-password-fine/

**United States — for comparison (already covered under Section 0/CBP)**: 18 U.S.C. § 2232 (up to 5
years for destroying property to prevent seizure — the statute used against Tunick) is not itself a
"key disclosure law," but functions as the closest analog: it's the government's route to punishing an
uncooperative digital response, absent a direct compelled-decryption statute at the federal border.
https://www.law.cornell.edu/uscode/text/18/2232

## 6. Practical protective measures for travelers (from EFF / reputable security guidance)

Primary source consulted: EFF's border-security guidance ecosystem (https://www.eff.org/issues/border-searches,
https://www.eff.org/wp/digital-privacy-us-border-2017) plus a guide that explicitly cites and synthesizes
EFF/ACLU/Freedom of the Press Foundation recommendations, **activistchecklist.org**
(https://activistchecklist.org/travel/), used here because direct EFF PDF/guide fetches were blocked or
returned only navigation chrome in this session (multiple attempts hit 403s or stripped content — noting
this as a sourcing limitation; the underlying claims are standard, widely-corroborated EFF-style guidance
but the direct primary quote extraction failed for the EFF pages themselves).

- **Dedicated/secondary travel device**: carry a secondary phone containing minimal data for border
  crossings, rather than your primary device with your full digital life on it — reduces what's exposed
  if a device is inspected or seized.
- **Data minimization before travel**: uninstall apps with sensitive data (email, messaging, social
  media, documents); delete specific message threads/photos beforehand. Guidance line: "The less you have
  on your device, the better."
- **Cloud-backup-then-wipe approach** (alternative to a second device): back up your primary phone to
  **local** storage (not cloud, to avoid the backup itself being accessible/seizable in transit), factory
  reset the phone for the trip, then restore from backup after crossing.
- **Power off before the checkpoint — the AFU vs. BFU distinction**: "Your data is most secure when your
  phone/laptop is shut down before it's been unlocked the first time" — i.e., a device in **Before First
  Unlock (BFU)** state (fully powered off, not yet unlocked since boot) has its encryption keys not yet
  loaded into memory and is far harder to forensically extract than a device in **After First Unlock
  (AFU)** state (already unlocked once since boot, keys resident in memory, more vulnerable to forensic
  tools like Cellebrite/GrayKey). Practical takeaway: power the phone all the way off before reaching the
  border/checkpoint.
- **Encryption**: full-disk encryption should be on for laptops (FileVault on macOS, Device Encryption on
  Windows) — "encryption is an essential part of these defenses. Without it, your password and other
  steps are basically meaningless if the state seizes your device."
- **Strong passcodes over biometrics at the border**: recommends long random passcodes (8-10 digits) —
  cited estimate: an 8-digit random passcode takes "40+ years" to brute-force vs. "less than 24 hours"
  for a weak/guessable 6-digit code. (General security-community consensus, not explicitly re-verified
  against a primary crypto source in this pass, but consistent with well-known password-entropy math.)
  https://activistchecklist.org/travel/
- Additional related read (not deep-fetched, EFF's own recent piece specifically on this topic, useful
  if the writer wants a direct EFF quote): "A Journalist Security Checklist: Preparing Devices for Travel
  Through a US Border," EFF, June 2025 —
  https://www.eff.org/deeplinks/2025/06/journalist-security-checklist-preparing-devices-travel-through-us-border
- Also relevant: EFF is actively litigating for a warrant requirement on device searches — "EFF to Third
  Circuit: Electronic Device Searches at the Border Require a Warrant," March 2026 —
  https://www.eff.org/deeplinks/2026/03/eff-third-circuit-electronic-device-searches-border-require-warrant
  (shows this is a live, unsettled legal fight in the US right now, good "why this matters now" framing).

---

## Gaps / things flagged as UNVERIFIED or needing a follow-up check before publication

1. Exact date GrapheneOS shipped the duress feature — sourced to a secondary release-tracker
   (nobsbitcoin.com) and a GrapheneOS X/Twitter post quote surfaced via search snippet, not independently
   re-confirmed by scrolling grapheneos.org/releases back to mid-2024 in this session.
2. Australia Crimes Act 3LA penalty (2 years) — sourced from a secondary compilation (Wikimili) after
   every attempt to fetch the primary AustLII/legislation.gov.au text was blocked (403 or JS-redirect).
   Possible the penalty has been amended since original enactment — needs a direct primary-source check.
3. IBTimes UK's claim of "similar enforcement patterns emerging in France and Spain against journalists
   and lawyers using GrapheneOS" — single-source, not cross-verified.
4. No confirmed, named case of an Indian traveler's device being searched at a US border — the one
   circulating claim (viral WhatsApp post, American Bazaar, July 2026) is explicitly unverified by the
   outlet that reported it.
5. CyberInsider's "January 2024" date for the Tunick stop conflicts with TechCrunch/MediaNama's
   "January 24, 2025" — going with 2025 as the better-corroborated date, flagging the conflict.
6. US News "Decision Points" article (2026-07-27) on the case could not be fetched (403) — appears in
   search index and may have additional useful detail/quotes; worth a manual look before publishing.
7. OEM-level (Samsung, etc.) duress-style features were not deeply researched — only stock
   Android/Google and iOS/Apple were confirmed via official docs, per the assignment's specific ask.

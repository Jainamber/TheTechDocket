# Research Brief — Dense Plasma Focus Physics & Fuse Energy Neutron-Yield Record

Prepared: 2026-08-15 IST | For: article on Fuse Energy's DPF neutron-yield claim (Aug 2026)
Method: WebSearch only (WebFetch egress-blocked), 19 queries run. Every claim below has a URL from search results. Items I could not verify are listed at the end — avoid stating those as fact.

---

## 0. The story itself — what Fuse Energy actually claimed

- Fuse Energy Technologies' megajoule-class dense plasma focus device **FAETON-X** produced a peak yield of **1.27 trillion (1.27×10¹²) neutrons in a single deuterium-deuterium (D-D) shot**, drawn from roughly **1 megajoule of stored capacitor energy**. Fuse says this is the first fusion company (private or commercial) to publicly document a neutron yield in the 10¹² range — a level "previously only attained by U.S. national laboratories."
  Sources: [PowerMag](https://www.powermag.com/fuse-touts-highest-neutron-yield-by-any-fusion-company/), [Research Square preprint](https://www.researchsquare.com/article/rs-10657590/v1), [The Fusion Report](https://thefusionreport.substack.com/p/this-weeks-fusion-news-august-14)
- Fuse's own comparison: this is **~40% more neutrons per megajoule than LLNL's MJOLNIR** facility — Fuse cites MJOLNIR's best as 1.2×10¹² neutrons from 1.3 MJ, vs. FAETON-X's 1.27×10¹² from ~1 MJ.
  Source: [PowerMag](https://www.powermag.com/fuse-touts-highest-neutron-yield-by-any-fusion-company/)
- FAETON-X technical specs (per the preprint): 500 µF capacitor bank (20 capacitors × 25 µF/100 kV), storing 1 MJ at 65 kV charge voltage, peak discharge current >4.5 MA, static inductance 55 nH, figure of merit 4.5 MA/MJ — "the highest reported for any MJ-class DPF." Built as a dual-fuel (D-D and D-T capable) platform for fusion R&D and radiation-effects/nuclear-effects testing.
  Source: [Research Square preprint "Exceeding 10¹² D-D flash neutrons in the 4.5-MA 1-MJ dense plasma focus FAETON-X"](https://www.researchsquare.com/article/rs-10657590/v1)
- **Caveat: this is a Research Square preprint, not yet peer-reviewed** as of this research date — flag as such in the article, don't call it a published/peer-reviewed result.
- Fuse Energy Technologies: founded 2019 in Silicon Valley/California by CEO **JC Btaiche** (founded the company at 19). ~$100M total funding to date, backers include Lowercarbon Capital, Balderton Capital, and Nico Rosberg (former F1 champion). Earlier hardware: a first DPF at 0.5 MA, then a device called "MU" that fired 3,000 shots and earned the first private Canadian Nuclear Safety Commission (CNSC) license. A smaller 100 kV device, FAETON-I, has separately been published in Scientific Reports.
  Sources: [OODAloop company profile](https://oodaloop.com/company-profiles/energy/fuse-energy-technologies/), [Fuse Energy — JC Btaiche bio](https://www.f.energy/jc-btaiche-founder-ceo-fuse-energy), [StartupIntros](https://startupintros.com/orgs/fuse-energy), [Nature Scientific Reports — FAETON-I](https://www.nature.com/articles/s41598-025-07939-x)

---

## 1. Dense plasma focus (DPF) explained

- **Invention**: independently invented in the early 1960s by **J.W. Mather** (United States) and **N.V. Filippov** (USSR). Filippov's original observation traces to 1954, while working on earlier linear pinch machines, where certain electrode/tube arrangements caused the plasma to reshape into a focused column.
  Source: [HandWiki — Dense plasma focus](https://handwiki.org/wiki/Physics:Dense_plasma_focus), [Plasma-Universe.com](https://www.plasma-universe.com/dense-plasma-focus/)
- **Mather vs. Filippov geometry**: they differ mainly in radial-to-axial electrode aspect ratio and in radial vs. coaxial plasma initiation; a Mather-type shot runs a few to ~10 microseconds, a Filippov-type has a much shorter axial phase.
  Source: [HandWiki — Dense plasma focus](https://handwiki.org/wiki/Physics:Dense_plasma_focus)
- **Original purpose vs. actual fate**: DPF was originally pursued as a fusion *power* device from the early 1960s, but scaling laws showed it would not work for commercial power generation; since the 1980s it has mainly served as a teaching system and as a **neutron and X-ray source**, not an energy machine.
  Source: [HandWiki — Dense plasma focus](https://handwiki.org/wiki/Physics:Dense_plasma_focus)
- **How it works (plain language), phase by phase**:
  1. A charged capacitor bank discharges across two coaxial cylindrical electrodes, ionizing/breaking down the fill gas and forming a current sheath.
  2. The J×B (Lorentz) force lifts the sheath and accelerates it down the axis between the electrodes ("axial rundown"), sweeping up and ionizing more gas as it goes, gaining mass and density.
  3. At the open end of the electrodes, the radial current and its self-generated azimuthal magnetic field compress the sheath inward — the "pinch" — forming a very hot, very dense, short-lived plasma column.
  4. Instabilities in the pinch column accelerate ion and electron beams and emit bursts of electromagnetic radiation; if the fill gas is deuterium, beam-target and thermonuclear-like fusion reactions in the pinch produce a short burst of fusion **neutrons** (nanosecond-to-microsecond scale).
  Source: [ResearchGate — "The Dense Plasma Focus: A Versatile Dense Pinch for Diverse Applications"](https://www.researchgate.net/publication/258657964_The_Dense_Plasma_Focus_A_Versatile_Dense_Pinch_for_Diverse_Applications), [arXiv 1610.09092 — Seeding the m=0 instability](https://arxiv.org/pdf/1610.09092), [arXiv 1408.4887 — sheath velocity bounds](https://arxiv.org/pdf/1408.4887)
- **DPF is a compact coaxial "plasma gun" that completes its discharge as a Z-pinch** — LLNL's own characterization of the device class.
  Source: [OSTI 1988207 — Comprehensive Review of DPF-based Flash Neutron Radiography Viability](https://www.osti.gov/biblio/1988207)
- **Why DPF is a neutron SOURCE, not a net-energy machine**: the pinch is a brief, small-volume, non-equilibrium plasma column driven by beam-target and turbulent/kinetic effects, not a self-sustaining thermonuclear burn — the device converts a small, unreproducible fraction of stored electrical energy into fusion reactions and yields a neutron pulse, with no claim of net energy gain anywhere in the literature. (See Section 2 arithmetic below for why this matters for the Fuse story specifically.)
- **Applications**: radiation-effects/nuclear-effects testing, flash neutron radiography, and — per NNSS — DPF facilities are "among the highest-priority missions in Stockpile Stewardship experimentation," used as pulsed neutron/radiation sources for radiation-detector development and studying material properties like radiation hardness.
  Source: [Krell Institute — DOE NNSA LRGF / NNSS](https://www.krellinst.org/lrgf/doe-lab-residency/nnss), [NNSS — Stockpile Stewardship Program](https://nnss.gov/mission/stockpile-stewardship-program/u1a-complex/)

---

## 2. Neutron yield vs. energy gain — why 1.27 trillion neutrons is NOT "ignition" or net energy

- **D-D vs. D-T neutron output**: a D-T fusion reaction's cross-section is **roughly 100 times greater than D-D's** at achievable plasma temperatures (below ~10 keV) — first measured at Purdue in 1943 and confirmed in modern ENDF cross-section data. This is why D-T is the preferred fuel for reactors like ITER, despite tritium not existing naturally on Earth. D-T neutrons also carry far more energy per neutron (14.1 MeV) than D-D neutrons.
  Source: [UT Austin plasma physics notes](https://farside.ph.utexas.edu/teaching/plasma1/Fusionhtml/node6.html), [OSTI 2338005 / Fusion Science & Technology — Early Nuclear Fusion Cross-Section Advances](https://www.osti.gov/pages/biblio/2338005), [MIT DSpace — D-T/D-D yield measurements in ignition-scalable implosions](https://dspace.mit.edu/entities/publication/186540db-5c94-488f-9103-04c506d3b792)
- **D-D reaction energy**: the D+D reaction has two equally probable (50/50) branches: D+D → T + p (releases 4.03 MeV) and D+D → ³He + n (releases 3.27 MeV). The **average energy release across both branches is 3.65 MeV per D-D fusion reaction**.
  Source: [MDPI — Classical Thermodynamic Analysis of Deuterium-Based Fusion Reactions](https://www.mdpi.com/2673-4141/3/1/4), [Fiveable nuclear physics study guide](https://fiveable.me/nuclear-physics/unit-10/fusion-reactions-energy-production/study-guide/4l3X7rC35tkJZC1V)
- **DERIVED ARITHMETIC (calculated by this brief, not a directly-quoted source figure — inputs are individually sourced above)**:
  Only the ³He+n branch produces a neutron, and it's 50% of all D-D reactions, so 1.27×10¹² detected neutrons implies roughly **2.5×10¹² total D-D fusion reactions** in the shot. At 3.65 MeV average per reaction:
  `2.54×10¹² reactions × 3.65 MeV ≈ 9.3×10¹² MeV ≈ 1.5 joules of fusion energy released.`
  (A more conservative version that skips the branching correction — treating the neutron count itself as the reaction count — gives ≈0.7 joules. Either way, order of magnitude is **~1 joule**.)
  Against the **~1,000,000 joules (1 MJ)** of capacitor energy that drove the shot, that's a fusion energy output of roughly **one- to two-millionths of the electrical input** — i.e., an energy gain Q on the order of **10⁻⁶**, about six orders of magnitude short of scientific breakeven (Q=1). **This is the single most important framing fact for the article**: a record neutron count is a real, verifiable diagnostic achievement, but it is not evidence of net energy gain, and nothing about the announcement claims otherwise.

---

## 3. The benchmark everyone knows: NIF (a different approach — laser inertial confinement)

- NIF uses **laser-driven inertial confinement fusion (ICF)** — 192 lasers compress a millimeter-scale fuel capsule — a fundamentally different approach from DPF's pulsed-power pinch. Clarify this distinction explicitly in the article; comparing DPF neutron counts to NIF energy-gain numbers is an apples-to-oranges trap.
  Source: [LLNL — Achieving Fusion Ignition](https://lasers.llnl.gov/science/achieving-fusion-ignition)
- **Dec 5, 2022 — first ignition**: 2.05 MJ of laser energy delivered → **3.15 MJ of fusion energy out** (gain ≈1.54, i.e., ~54% more energy out than was delivered to the target). First net energy gain from fusion outside a thermonuclear detonation.
  Source: [LLNL — Achieving Fusion Ignition](https://lasers.llnl.gov/science/achieving-fusion-ignition), [Science/AAAS](https://www.science.org/content/article/historic-explosion-long-sought-fusion-breakthrough), [AIP.org](https://www.aip.org/fyi/2022/national-ignition-facility-achieves-long-sought-fusion-goal)
- **NIF record progression since**:
  - July 30, 2023: 3.88 MJ out (same ~2.05 MJ laser input)
  - Feb 10, 2024: 5.2 MJ out, target gain ≈2.3
  - Feb 23, 2025 (7th ignition): 2.05 MJ in → 5.0 MJ out, gain 2.44
  - **Apr 7, 2025: 2.08 MJ in → 8.6 MJ out, target gain >4 (≈4.13) — the current record for highest yield and gain**, crossing the "gain > 4" milestone
  - June 20, 2026 (11th ignition, most recent found): 7.9 MJ yield, gain ≈3.8 — a later shot but *not* a new record; the April 2025 shot (8.6 MJ / gain 4.13) remains the best result found in this research pass.
  Sources: [LLNL — NIF Sets Power and Energy Records](https://lasers.llnl.gov/about/keys-to-success/nif-sets-power-energy-records), [LLNL — Target Breakthrough Enabled Fusion Record at NIF](https://lasers.llnl.gov/news/target-breakthrough-enabled-fusion-record-nif), [Interesting Engineering](https://interestingengineering.com/energy/us-laser-nuclear-fusion-achieves-energy-records)
- **Important qualifier for "gain" claims generally**: even NIF's target gain (fusion output ÷ laser energy delivered to the target) is NOT the same as plant-level (engineering) breakeven — NIF's laser system reportedly draws on the order of ~300 MJ of wall-plug electricity from the grid per shot to deliver ~2 MJ to the target, i.e., NIF still consumes far more total energy than it produces even at its best "gain 4" shots. Treat the ~300 MJ wall-plug figure as approximate/secondary-sourced (see gaps section) but the underlying point — target gain ≠ plant gain — is solid and directly useful for the breakeven section.
  Source: [search aggregation incl. LLNL/independentnews.com coverage](https://www.independentnews.com/news/livermore_news/livermore-lab-breaks-fusion-record-again/article_926d3f7f-59c4-4eb0-b6fa-33119b5784cd.html)

---

## 4. Scientific breakeven vs. engineering breakeven vs. commercial viability

- **Fusion energy gain factor (Q)**: ratio of fusion power produced to the power required to maintain/heat the plasma.
  Source: [Wikipedia/HandWiki — Fusion energy gain factor](https://en.wikipedia.org/wiki/Fusion_energy_gain_factor) (cross-referenced against LLNL/PPPL technical notes below)
- **Scientific breakeven** = Q ≈ 1: fusion yield equals the external (laser/driver) energy delivered into the fuel. This is the NIF Dec-2022 milestone. Achieving it does **not** mean the whole reactor produces net energy — a system at Q=1 still consumes more total power than it produces once all inefficiencies (laser wall-plug efficiency, etc.) are counted.
  Source: [LLNL/PPPL — Scientific Breakeven for Fusion Energy (fire.pppl.gov)](https://fire.pppl.gov/ICF_Scientific_Breakeven_LLNL2.pdf), [LLNL/PPPL — Scientific Feasibility for Fusion Energy](https://fire.pppl.gov/ICF_Scientific_Feasibility_LLNL.pdf)
- **Engineering breakeven**: extends the power balance to the *entire power plant* — ratio of electrical power produced to electrical power consumed by the whole system (including laser/driver inefficiency, cooling, etc.). A plant can in principle reach engineering breakeven even below scientific breakeven if downstream equipment is efficient enough, though in practice it's the harder target because drivers like NIF's lasers are only ~1% wall-plug efficient.
  Source: [same fire.pppl.gov technical notes](https://fire.pppl.gov/ICF_Scientific_Breakeven_LLNL2.pdf)
- **Self-heating/practical threshold**: because fusion products carry away energy the plasma can't recapture, self-sustaining operation typically isn't expected until Q≈5, and a genuinely useful power plant is usually described as needing Q in the 5–10 range.
  Source: [Fusion energy gain factor overview](https://en.wikipedia.org/wiki/Fusion_energy_gain_factor)
- **Commercial viability** is a step beyond engineering breakeven again — it additionally requires the plant to be built, maintained, licensed, and to produce power at a competitive cost; none of the DOE/PPPL sources found frame the Fuse announcement, or even NIF's Q>4 shots, as being anywhere near this bar.

---

## 5. Neutron-source market context: who needs intense pulsed neutron sources

- **NNSA stockpile stewardship**: DPF facilities are used as pulsed neutron/radiation sources for radiation-detector development and to study material radiation hardness and reactivity — described by NNSS as among its highest-priority Stockpile Stewardship missions. NNSA also operates other pulsed-power neutron/radiation simulators for this mission, e.g. Sandia's HERMES (prompt gamma simulation) and the Saturn and Z facilities, alongside NIF.
  Source: [Krell Institute / DOE NNSA LRGF](https://www.krellinst.org/lrgf/doe-lab-residency/nnss), [NNSS Stockpile Stewardship Program](https://nnss.gov/mission/stockpile-stewardship-program/u1a-complex/), [OSD Nuclear Matters Handbook ch.9](https://www.acq.osd.mil/ncbdp/nm//NMHB2020rev/chapters/chapter9.html)
- **Electronics/aerospace radiation testing**: NIF has separately demonstrated capability to expose weapon-relevant materials and **electronics** to thermonuclear-spectrum neutron fluences via its cryogenic X-ray/neutron/blast snout (CryoXNBS) diagnostic — illustrating the broader category of "expose hardware to a realistic pulsed fusion-neutron spectrum" that DPF machines like FAETON-X are also pitched for (Fuse explicitly markets FAETON-X for "commercial aerospace testing, defense infrastructure" radiation-effects work).
  Source: [LLNL — Ignition experiment advances stockpile stewardship mission](https://www.llnl.gov/article/49576/ignition-experiment-advances-stockpile-stewardship-mission), [PowerMag](https://www.powermag.com/fuse-touts-highest-neutron-yield-by-any-fusion-company/)
- **Materials qualification for future fusion reactors**: this is a genuine, well-documented gap in the field — fission reactors' ~2 MeV neutron spectrum is inadequate for qualifying fusion first-wall materials because it falls below the ~3 MeV threshold needed to reproduce fusion-relevant transmutation/gas-generation damage, and **no existing facility can produce the needed 14 MeV fusion-spectrum neutron fluence at scale**. This is exactly why IFMIF-DONES (accelerator-based D-Li neutron source, under construction in Spain, aiming for 10¹⁴–10¹⁵ n/cm²/s at 14 MeV) is being built as dedicated materials-irradiation infrastructure for DEMO-class fusion reactors.
  Source: [IOPscience — IFMIF-DONES fusion oriented neutron source](https://iopscience.iop.org/article/10.1088/1741-4326/ac318f), [EUROfusion — IFMIF-DONES construction phase](https://euro-fusion.org/related/ifmif-dones/international-materials-facility-ifmif-dones-starts-construction-phase/), [IFMIF/EVEDA project page](https://www.ifmif.org/public/)
- **Market-size figures (LOW CONFIDENCE — generic market-research-firm estimates, not DOE/IAEA numbers; treat with caution or omit)**: one vendor pegs the "Neutron Source Generator Market" at ~$150M (2025) growing to ~$250M by 2034 (CAGR 6.2%); another cites the portable neutron generator segment at ~$300M (2024) to ~$500M by 2033; a third cites stationary neutron generators at ~$116M (2021) to ~$296M by 2033. These come from different market-research vendors with unclear methodology and inconsistent baselines — do not present as authoritative in the article.
  Source: [Verified Market Reports — Neutron Source Generator Market](https://www.verifiedmarketreports.com/product/neutron-source-generator-market/), [Verified Market Reports — Portable Neutron Generator Market](https://www.verifiedmarketreports.com/product/portable-neutron-generator-market/), [Business Research Insights — Stationary Neutron Generators Market](https://www.businessresearchinsights.com/market-reports/stationary-neutron-generators-market-111341)

---

## 6. LLNL's own DPF program (for fairly framing the "beat LLNL" comparison)

- LLNL's flagship DPF is **MJOLNIR** (MegaJOuLe Neutron Imaging Radiography), built/commissioned around 2018, purpose-built for flash neutron radiography as well as high-yield operation.
  Source: [OSTI 1860821 — First Experiments and Radiographs on MJOLNIR](https://www.osti.gov/biblio/1860821), [LLNL Science & Technology Review — "Dense Plasma Focus Back in the Spotlight"](https://str.llnl.gov/2021-02/schmidt)
- **Published yield progression**: initial shots reached 2.5×10¹⁰ neutrons; design/pulsed-power optimization pushed this to ~4×10¹¹ neutrons per pulse at 2.2 MA peak current; most recently reported results show **up to 1.2×10¹² neutrons per discharge at 3.7 MA peak current**, with stored energy reported at 1.2 MJ in one source and 1.3 MJ in another (sources are slightly inconsistent on this specific figure — Fuse's own comparison used 1.3 MJ).
  Source: [ResearchGate — MJOLNIR Rebuild and High Current Experiments](https://www.researchgate.net/publication/384653200_MegaJOuLe_Neutron_Imaging_Radiography_MJOLNIR_Dense_Plasma_Focus_Rebuild_and_High_Current_Experiments), [IEEE Xplore — same paper](https://ieeexplore.ieee.org/document/10705961/), [LLNL — Radiography innovation shows new promise](https://www.llnl.gov/article/50001/radiography-innovation-shows-new-promise-experimental-dense-plasma-focus-milestone)
- LLNL has operated MJOLNIR up to 1.3 MJ of stored energy (vs. a prior record of 1.0 MJ) and states plans to eventually use the full 2 MJ the machine is rated for — which would be **the highest energy level ever applied to a DPF**, i.e., LLNL's own roadmap already anticipates going beyond where FAETON-X currently sits. Useful context: this is an active, funded government program, not a static benchmark Fuse is racing against a finished result.
  Source: [ResearchGate — MJOLNIR Rebuild](https://www.researchgate.net/publication/384653200_MegaJOuLe_Neutron_Imaging_Radiography_MJOLNIR_Dense_Plasma_Focus_Rebuild_and_High_Current_Experiments)
- Fair framing for the article: Fuse's claim is specifically a **neutrons-per-megajoule efficiency** claim (1.27×10¹²/MJ vs. MJOLNIR's 1.2×10¹²/1.3MJ ≈0.92×10¹²/MJ), not a claim of higher absolute yield or higher stored energy — MJOLNIR's total energy budget (rated to 2 MJ) exceeds FAETON-X's ~1 MJ shot.

---

## Could NOT verify — avoid stating these as fact in the article

- The precise energy carried by a single D-D neutron (commonly cited elsewhere as ~2.45 MeV) — no direct URL confirming this specific figure turned up in this research pass. Stick to the sourced reaction-energy figures (3.27 / 4.03 / 3.65 MeV) instead.
- The exact ~300 MJ "wall-plug energy per NIF shot" figure — widely repeated in secondary/aggregator coverage but not traced to a primary LLNL/DOE document in this pass. The underlying point (NIF's total grid draw far exceeds its target-level "gain") is well supported directionally; treat the specific number as approximate.
- Whether MJOLNIR's 1.2×10¹² figure corresponds to 1.2 MJ or 1.3 MJ stored energy — sources conflict; Fuse's own press comparison uses 1.3 MJ.
- Any independent/peer-reviewed confirmation of Fuse's FAETON-X result — as of this research date it is only documented in a Research Square preprint plus trade press citing that preprint; no peer-reviewed publication found.
- Specific, authoritative (DOE/IAEA-grade) market-size figures for pulsed neutron sources — only generic market-research-vendor estimates were found; flagged above as low confidence.

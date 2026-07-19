> **Note (2026-07-19):** brand + domain in this doc are superseded — PulseFold → **The Tech Docket** (thetechdocket.com); GoatCounter code `thetechdocket`; repo `jainamber/thetechdocket`. Phases, KPIs, gates and cadence rules are unchanged. Deploy record: HANDOFF4.md in the owner folder. T0 = actual launch date (2026-07-19).

# PulseFold — 90-Day Operating Plan (Max Reach, Max ROI)

**Written:** 2026-07-15 · **T0 (launch target):** 2026-07-20 · **Horizon:** T0 + 13 weeks (~Oct 20, 2026)
**Owner:** Saurab Jain · **Engine:** automated daily pipeline (see README.md, DAILY_RUN.md)
**Fact base:** research/monetization_2026.md, research/seo_2026.md, research/google_policies.md, research/data_sources.md — all numbers below trace to those files; estimates are marked.

---

## 1. Strategic thesis

PulseFold's edge is **speed + consistency + policy-cleanliness on freshly-searched topics**, not head-term SEO (a new domain cannot win "best AI tools" in 90 days — that's a month 6-12 fight). The 90-day game is to stack five reach engines in order of time-to-payoff, and let three compounding loops run:

**Reach engines, by when they pay:**

| Engine | Pays from | Why it works for us | Ceiling in 90 days |
|---|---|---|---|
| 1. Long-tail freshness SERPs | Week 1-3 | New model names, error messages, launch specifics have zero entrenched competition; our answer-first format targets exactly these | 100s of visits/day |
| 2. Community distribution (Reddit/HN/LinkedIn) | Day 1 (manual) | Immediate, free, also seeds the crawl + first backlinks | Spiky; 1 good HN/Reddit hit = 5-20k visits |
| 3. Google Discover | Week 4-10 (if at all) | Feb 2026 Discover update rewards exactly our profile: fresh, original, non-clickbait, big images, fast pages; 70%+ of Discover clicks come within 24h of publish — a daily publisher gets 90 lottery tickets a quarter | The viral channel: single articles can do 10-100k impressions |
| 4. AI-search citations (AI Overviews, ChatGPT, Perplexity, Copilot) | Week 3+ | Answer-first paragraphs + tables + open robots policy are the top measured citation factors; Bing indexing (via IndexNow) feeds Copilot | Steady trickle, brand-building |
| 5. Owned audience (RSS + email) | Week 2, compounds | Converts every spike into permanent baseline; the only channel no algorithm can take away | 300-800 subs by day 90 is a strong result |

**Compounding loops already built into the engine:**
- *Performance loop:* GoatCounter + Search Console → `insights.json` → scoring boosts + brief guidance → content shifts toward what's demonstrably working (weekly, automatic).
- *Authority loop:* every article adds 2-4 internal links into hubs → topical depth → better rankings on the whole cluster (the #3 measured AI-citation factor).
- *Trust loop:* gates enforce E-E-A-T + accuracy daily → survives core updates that kill careless AI sites → longevity is itself a ranking asset.

**The ROI equation to optimize:** `Revenue ≈ Sessions × (geo mix × RPM) + affiliate wins + newsletter value`. Two facts from the monetization research dominate it: **US/UK traffic monetizes at roughly 3-4× India traffic** (tech display RPM ~$5-20 US vs ~$2-5 India, estimates), and **ad-network ladders gate on sessions and geo** (Mediavine Journey: 1,000 sessions/30d; Raptive: 25k pageviews AND ≥50% US/UK/CA/AU/NZ AND 6-month domain age). Implication: keep the India angle as our differentiator *inside* articles, but let topic selection lean global — the config markets weights move from 0.5/0.5 to **0.45 IN / 0.55 US** in Phase 2 unless India data outperforms.

**Honest framing:** Q1 (these 90 days) is an **asset-building quarter with first revenue**, not a profit quarter. The assets: an indexed ~95-article archive, Discover eligibility earned, ad-network gates crossed, an email list, and a feedback-trained engine. Revenue inflection is Q2. Anyone promising more from a 90-day-old domain is selling something.

---

## 2. Current state (T-5)

**Done:** engine (fetch→score→brief→write→gate→build→publish), 41-gate compliance suite, 4 gated articles live in the build, PulseFold brand (2× collision-checked), analytics + feedback loop wired, GitHub Actions (trend pre-fetch, IndexNow/WebSub pings), hub-aware site with E-E-A-T pages.

**Blocking launch (owner actions):**
1. Buy **pulsefold.com** (~₹1,000-1,300/yr). Do this first — Raptive's 6-month domain-age clock and all SEO history start here. Skip .in as primary (hard geotargets to India; hurts the global half). Optionally grab pulsefold.in defensively.
2. Create public GitHub repo `pulsefold` + fine-grained PAT (Contents R/W + Workflows R/W) → hand to Claude.
3. GoatCounter account (code: `pulsefold`) + API token → hand to Claude.
4. 10 minutes of profile work: LinkedIn + X profiles list "Founder/Editor, PulseFold" with the site link (entity signals + first policy-safe backlinks).

**Then Claude (one session):** push repo → you enable Pages (Settings→Pages→main`/docs`) → set real `base_url` + CNAME → rebuild/re-gate → DNS records for domain + Search Console domain-property TXT → create the 6:30 IST daily scheduled task → dry-run day 1.

---

## 3. Phase 1 — LAUNCH & INDEX (Weeks 0-4, ~Jul 20 → Aug 16)

**Objective:** everything indexed, daily cadence flawless, first long-tail wins, distribution habits set. Target by day 30: **34+ articles live, >90% of submitted URLs indexed, 300-800 impressions/day in Search Console, 50-150 email subscribers, zero gate violations.**

### Week 0-1 — Launch sequence
- Day 1: domain + repo + Pages + custom domain attached with HTTPS enforced **before** sharing any URL anywhere (GitHub Pages cannot 301 later; never build equity on the github.io URL).
- Day 1: Search Console **domain property** (DNS TXT — covers www/non-www/http/https), submit sitemap.xml. Then Bing Webmaster Tools → "Import from Search Console" (feeds Copilot).
- Day 1: Google Publisher Center — note: there is **no submission process anymore** (removed Apr 2024); News/Discover inclusion is automatic on policy compliance. Nothing to do beyond staying clean. Do NOT pay anyone who offers "Google News submission."
- Day 2: scheduled task live (05:45 UTC Action pre-fetch → 06:30 IST writing session). First 3 days: Saurab reads each article end-to-end (calibration week — flag anything off-tone; the engine's editorial instructions get tuned from your notes).
- Day 2-3: apply for the **official Google Trends API alpha** (free, invite-only, weeks-long lead time — costs nothing to be in the queue; upgrades our most fragile data source).
- Day 3-7: request-indexing via Search Console URL Inspection for each day's article (1/day is normal usage) until crawl cadence establishes itself (daily-updated sites get crawled more often within ~2 weeks).

### Content operations (Weeks 1-4)
- Cadence: **1 trend article/day, no exceptions the gates don't force.** Weak-trend days auto-fall back to the evergreen backlog — never skip silently; a hole in the cadence resets crawler expectations.
- Fill the two empty hubs (Big Tech, Policy & Society) by Week 2 — the engine's scorer naturally covers them; if not, force one evergreen each (nav shows hubs only when filled, so no user-facing gap meanwhile).
- Every article already ships with FAQ-from-real-queries, comparison tables, answer-first paragraph — these are the AI-citation levers; no change, just enforcement.
- Week 4: first **evergreen refresh check** — any article where facts changed (pricing, versions) gets a substantive update + visible "Updated" date (never a date bump without a real diff; that's the pattern the Feb 2026 Discover update punished).

### Distribution (manual, ~30 min/day for Saurab in month 1, then taper)
Rules from the research (violating them burns the account, not just the post):
- **Reddit:** participate genuinely in r/artificial, r/LocalLLaMA, r/developersIndia, r/india (tech threads) for 1-2 weeks *before* first self-post. Then ≤1 self-link/week/subreddit, always disclosed ("I wrote this"), always 9:1 participation ratio. Text posts referencing the article outperform bare links.
- **Hacker News:** submit only genuinely HN-worthy pieces (deep technical explainers, original analysis) — 1-2/month max, original URL, no tracking params, author comment early. One front-page hit is worth a month of other distribution.
- **LinkedIn:** 3 posts/week — the day's strongest insight as a native text post, link in the post (LinkedIn tolerates links better than X). India tech-LinkedIn is an underexploited distribution surface for exactly our content.
- **X:** organic link posts get ~0% reach for non-Premium accounts (verified Aug 2025 data; a reversal is being tested — reassess Week 6). Until then: text-first threads with the link in a reply, low effort, low expectation.
- **Syndication (Week 3+):** republish the week's 2 best pieces to Medium + Dev.to **with canonical URL pointing home** (both platforms still support this; Dev.to needs "mark RSS source as canonical" enabled). Free reach + a legitimate backlink each, zero duplicate-content risk.

### Owned audience (Week 2)
- Stand up **beehiiv free tier** (2,500 subs, custom domain on free — best free-tier economics of 2026). Subscribe CTA is a **styled plain link to the beehiiv-hosted subscribe page** in the site footer + article footer (engine template change, one line) — NOT beehiiv's embed, which is JS-only and violates the zero-JS article rule (verified in `REVIEW-2026-07-15.md` §6.4, action #9b; correction written back 2026-07-16). In-article capture placement is specced in `V2.1-ADDENDUM-INTEREST-VIRALITY-2026-07-16.md` §3.2.
- Weekly digest, sent Thursday: the engine generates `data/digest/<week>.md` (top pieces + one exclusive paragraph of "what the data says people searched this week" — content only we have). Saurab pastes + sends: 10 min/week. (Free tiers don't automate RSS-to-email; not worth $9/mo until the list proves out.)

### Phase 1 gates (day 30 review)
| Signal | Green | Yellow → action |
|---|---|---|
| Indexed / published | >90% | <70% → crawl diagnosis session (internal links, sitemap, quality pattern) |
| Search impressions/day | 300+ | <100 → audit titles vs actual queries; shift longer-tail |
| Community referrals | 10+/day baseline | ~0 → distribution rules review; try different subreddits |
| Gate failures requiring intervention | 0-2 total | Recurring same-gate failures → tune DAILY_RUN instructions |
| Email subs | 50+ | <20 → move signup above the fold on articles |

---

## 4. Phase 2 — MOMENTUM & FIRST MONEY (Weeks 5-8, ~Aug 17 → Sep 13)

**Objective:** let the data reshape the engine; cross the first monetization gates. Target by day 60: **65+ articles, 1,000+ sessions/30d (Mediavine Journey gate), 1-3k impressions/day, AdSense approved, 150-300 email subs, first Discover impressions observed.**

### Learn & adapt goes live for real
- Weekly: `python -m engine.run feedback` output reviewed (it runs daily in the Action; the *decisions* are weekly). The three moves it can trigger:
  1. **Hub mix shift** — a hub with 2× median CTR or impressions gets +1 weekly slot via scoring; the weakest hub loses one.
  2. **Query mining** — winning queries from Search Console become new `news_seed_queries` and FAQ targets (people are telling us the exact phrasing they use — feed it back verbatim).
  3. **Geo tilt** — if US-heavy pieces outperform on revenue-weighted traffic, markets weight moves to 0.45/0.55 (config change, logged). India-angle sections stay mandatory either way — that's the moat, not the constraint.
- Add the **2 pillar pages** for the strongest hub (e.g., "The state of on-device AI, updated monthly" / a living comparison table). Pillars are the internal-linking anchors everything else feeds — and living pages legitimately earn `dateModified` freshness.

### Google Discover watch (the reach lottery)
- Everything Discover wants is already enforced by gates (1200px 16:9 heroes, max-image-preview:large, no clickbait, CWV, E-E-A-T pages). Anecdotal 2025-26 evidence: new sites that get Discover traction typically see it **4-10 weeks after** consistent indexed publishing — inside this phase.
- When the first Discover impressions appear in Search Console: shift publish-time-sensitive topics earlier (Discover is a 24-hour game), and prioritize story-driven headlines over explainer headlines for 2 weeks as a controlled test.
- If zero Discover by day 60: not a failure signal yet (it's probabilistic), but run the checklist once: image quality, `og:site_name`, headline style, entity pages.

### Monetization step 1 (display ads — carefully)
- **Day ~30-35: apply to AdSense** (no traffic minimum; India: mailed PIN at $10 earnings, $100 payout threshold, IFSC+SWIFT details; treat earnings as business income — a CA conversation, not this doc's advice). Approval typically 3-7 days clean / 2-4 weeks flagged. Our editorial-policy + about + contact pages and original-analysis gates are exactly what approval reviewers look for.
- Placement policy (protects the SEO that funds everything): **manual placements only, no Auto Ads** — one in-content unit after the 2nd H2, one at article end. Every slot gets a CSS `min-height` reservation (CLS protection — layout shift is the #1 way ads silently kill Discover eligibility). Ad density stays under ~20% (the Feb 2026 Discover update favored low-ad-density sites).
- Parallel: **Newor Media "Elevate!"** (no stated minimum) as the comparison/backup rung. Ezoic is off the table (250k monthly users minimum since Feb 2026). 
- At 1,000 sessions/30d: **apply Mediavine Journey** (better RPMs than AdSense at small scale). Raptive noted for Q2+ (25k pv + ≥50% US/UK-cluster traffic + 6-month domain — our geo mix decides whether it's ever the right ladder).

### Phase 2 gates (day 60 review)
Decision: if sessions <500/30d → diagnose before monetizing further (indexation? CTR? distribution?); if 1,000+ → Journey application; if a Discover spike happened → double down on freshness cadence (consider the Phase 3 second daily slot early).

---

## 5. Phase 3 — SCALE & MONETIZE (Weeks 9-13, ~Sep 14 → Oct 20)

**Objective:** convert proven demand into scaled output and layered revenue. Target by day 90: **95-110 articles, 8-15k sessions/mo run-rate, display ads live, affiliate layer live, 300-800 subs, Q2 plan decided by data.**

### Cadence decision gate (the only scaling that matters)
Go to **2 articles/day** ONLY if all four hold for the trailing 2 weeks: gates pass rate >95% without intervention; indexation >90%; zero Search Console manual actions/messages; Saurab's weekly skim finds nothing embarrassing. The second slot is a **morning evergreen/explainer** (searches don't expire) — trend slot stays singular. This is the scaled-content-abuse guardrail: scale output only as fast as verifiable quality holds. If any pillar wobbles, stay at 1/day — a 90-article clean archive beats a 150-article flagged one, permanently.

### Monetization step 2 (affiliate — the engine change)
- Flip `allow_affiliate: true` behind new engine rules (build task for a Claude session): auto `rel="sponsored"` on affiliate domains, a visible per-article disclosure block, gate G23 v2 (affiliate link present → disclosure present, else hard fail), and an affiliate-domain allowlist in config.
- Program priorities from the research: **SaaS/tools, not hardware** — Semrush (up to $450/sale), Jasper-class AI tools (25% recurring ×12mo), NordVPN-class (100% first month) vs Amazon India mobiles at 0-1% (dead). Rule: affiliate links only where the article would name the tool anyway — contextual, never steering. YMYL security/finance articles keep zero affiliate links.
- Expectation-setting: affiliate at our scale is **lumpy** — ₹0 most weeks, then a $200-450 SaaS conversion. Model it as bonus, not baseline.

### Monetization step 3 (newsletter as product)
- 300+ subs: digest gets a "tools we actually checked this week" section (affiliate-eligible, disclosed).
- 2,500 subs unlocks the beehiiv Ad Network (tech newsletter CPMs ~$75-250 under 5k subs, estimate) — realistically a Q2 milestone; the Q1 job is list growth only.

### Engine upgrades this phase (Claude build sessions, ~one each)
1. **Search Console API feedback** (service account) — replaces manual CSV drops; free, 2-3 day lag. The full loop becomes autonomous.
2. **Social snippet generator** — every publish emits ready-to-paste LinkedIn post + X thread + Reddit text-post draft into `data/social/` (cuts your distribution time to paste-and-judge).
3. **Evergreen refresh command** — `engine.run refresh --slug X` flow with update-note enforcement.
4. If Trends API alpha access lands: swap the RSS fetcher to the official API (5-yr consistent-scaled data unlocks real seasonality analysis).

### Day-90 review → Q2 decision tree
- **Sessions >15k/mo or Discover active:** scale play — 2/day standard, Raptive-track geo strategy, consider dedicated writer-hours budget from revenue.
- **5-15k/mo:** stay the course, deepen pillars, push newsletter; revenue follows traffic ~1 quarter behind.
- **<5k/mo:** diagnostic pivot — the engine is cheap to retarget (`config.yaml topic:`); test a tighter sub-niche (e.g., "AI tools for Indian SMBs") where topical authority concentrates faster. The infrastructure transfers 100%.

---

## 6. Weekly operating rhythm (Saurab: ~60-90 min/week after month 1)

| When | What | Time |
|---|---|---|
| Daily (month 1 only) | Skim the day's article; note tone/fact issues | 10 min |
| Mon | Community: 1 Reddit text-post or HN submit if the week has a worthy piece; approve any hub-mix change the data suggests | 20 min |
| Thu | Paste + send the digest; glance at subscriber curve | 10 min |
| Sun | Metrics glance: Search Console (impressions, CTR, coverage, *messages tab* — manual actions land here), GoatCounter top pages; one line of notes back to Claude | 15 min |
| Monthly | Corrections inbox check; evergreen refresh approvals; ROI snapshot vs this plan | 30 min |

Everything else — research, writing, gating, publishing, pinging, insights — is automated. Your irreplaceable jobs: taste (does this feel like a publication you're proud of), community presence (algorithms distrust ghosts), and the monetization/legal decisions.

---

## 7. ROI model (day-90 run-rate scenarios; estimates, USD→₹ at ~96)

Assumptions from research: blended RPM = 60% India traffic @ ~$3 + 40% US/global @ ~$10 ≈ **$5.8/1,000 pageviews**; pageviews ≈ 1.3× sessions; affiliate lumpy; costs ≈ domain ₹1,300/yr + ₹0 hosting/analytics/email (all free tiers) + existing Claude subscription.

| Scenario | Sessions/mo (day 90) | Display/mo | Affiliate/mo | Total/mo run-rate | What had to go right |
|---|---|---|---|---|---|
| Conservative | 3,000 | ~$23 (₹2.2k) | $0 | **~₹2k** | Cadence held; no Discover; long-tail only |
| Base | 12,000 | ~$90 (₹8.6k) | ~$50 avg | **~₹13k** | Indexation clean + 2-3 community hits + Journey RPMs |
| Upside | 40,000+ (Discover active) | ~$300+ (₹29k+) | ~$150 avg | **~₹43k+** | Discover adoption + one viral cycle + geo tilt worked |

The number that actually matters at day 90 is not the ₹ — it's **which curve you're on**. All three scenarios have identical costs (~₹200/mo amortized). The asset either way: ~100 indexed articles compounding, an email list, crossed ad-network gates, and a self-improving engine. This is not financial advice; it's a planning model with labeled assumptions.

---

## 8. Risk register

| Risk | Likelihood | Blast radius | Mitigation (mostly already built) |
|---|---|---|---|
| Google core/spam update reclassifies AI-assisted sites | Med | High | Gates enforce the exact published criteria (originality, review logs, E-E-A-T); 1/day restraint; diversified channels (email, Bing, AI-search) |
| Discover never arrives | Med | Med (upside lost, base intact) | Plan's base case assumes zero Discover; everything Discover-required is also good general SEO |
| Trends RSS/unofficial endpoints break | High (eventually) | Low | Multi-source inbox + WebSearch fallback + Trends API alpha application in queue |
| Reddit/HN account flagging | Med | Low-Med | Strict norms (disclosure, 9:1, frequency caps); accounts warm up before linking |
| AdSense rejection round 1 | Med | Low | Fix cited issue, reapply in 2-4 wks; Newor parallel; revenue timeline slips, nothing else |
| X link-penalty persists | High | Low | Already planned around (text-first, LinkedIn priority) |
| Trademark surprise on PulseFold | Low | Med | Registries weren't fully searchable; if the brand gains value, spend on a proper attorney search (~month 2) — cheap insurance |
| Owner time drought | Med | Med | Engine runs unattended; the 60-min weekly rhythm is the floor — protect it on the calendar |

---

## 9. 13-week calendar (one line each)

| Wk | Focus |
|---|---|
| 0 | Domain, repo, Pages, Search Console, schedule live — first automated publish |
| 1 | Calibration reads daily; request-indexing routine; community warm-up (no links yet) |
| 2 | beehiiv + signup boxes; first Reddit text-post; both empty hubs filled |
| 3 | First syndication pair (Medium/Dev.to canonical); Trends-API application done |
| 4 | Day-30 gate review; first evergreen refresh pass; first HN-worthy submit if earned |
| 5 | AdSense application; feedback-loop decisions begin (hub mix v1) |
| 6 | Pillar page #1; reassess X link policy; query-mining into seed queries |
| 7 | Pillar page #2; Discover checklist audit; Newor comparison if AdSense lags |
| 8 | Day-60 review; Mediavine Journey if 1k sessions; geo-tilt decision |
| 9 | Affiliate engine build + first contextual placements; ad-placement CWV audit |
| 10 | Cadence gate evaluation → 2/day trial if all-green |
| 11 | Search Console API automation; social snippet generator |
| 12 | Newsletter product section; evergreen refresh round 2 |
| 13 | Day-90 review → Q2 decision tree; this document's successor written from data |

---

*Working doc — the daily engine session reads this file's current phase for context. Revise at each phase gate, not mid-week. All third-party numbers dated July 2026; recheck before relying on any single one for a spend decision.*

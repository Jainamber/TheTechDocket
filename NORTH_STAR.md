# NORTH STAR METRIC — CONSTITUTIONAL LAW

**Season:** Q4 2026 (Launch & Growth Season)  
**Site:** `thetechdocket.com` (`mytechdocket.com`)  
**Owner:** Saurab Jain  
**Binding Date:** November 8, 2026  
**Status:** ACTIVE · PERMANENT HARD GATE  

---

## 1. The Supreme Law

> **"We do the actions and ONLY those actions (or changes) which improve the North Star Metric. Else we simply do not do it."**

All work performed by:
1. **The Owner** (human strategic, distribution, or operational choices),
2. **AI Agents** (Cline, Claude Code, Gemini CLI, background autonomous pipelines),
3. **Automated scheduled pipelines & GitHub Actions**,

is strictly subordinate to and governed by the consequence on this single metric.

Any task, refactoring, re-architecture, cosmetic polish, speculative feature, or internal tool that cannot demonstrate a clear, causal, near-term link to increasing or measuring this metric is **banned from execution**.

---

## 2. The Metric Definition

* **North Star Metric (NSM):** **Number of Visitors per Week (`Weekly Visitors`)**
* **Time Boundary:** Monday 00:00 IST through Sunday 23:59 IST (weekly roll-up).
* **Unit of Measure:**
  * **Primary:** Unique Weekly Visitors / Active Sessions visiting `thetechdocket.com` (or `mytechdocket.com`).
  * **Leading Operational Metric:** Weekly Organic Search & Discover Impressions + Referring Distribution Clicks.

### Sources of Truth for Measurement
1. **GoatCounter Analytics (`thetechdocket.goatcounter.com`):**
   * Real-time, zero-cookie, server-logged unique visitors and path visits (`engine/feedback.py`).
2. **Google Analytics 4 (Property ID `G-7M4KPLZK1B`):**
   * Active Users, Session volume, Traffic acquisition channels (Organic Search, Referral, Direct, Organic Social), and Geographic breakdown (US, IN, Global).
3. **Google Search Console (`data/search-console/` & GSC API):**
   * Weekly Clicks, Impressions, Average CTR, Average Position, and Total Indexed URL count.

---

## 3. The Growth Equation (The Only 4 Permitted Action Levers)

Weekly Visitors cannot be wished into existence; they are the mathematical result of exactly four levers:

$$\text{Weekly Visitors} = \Big(\text{Search \& Discover Impressions} \times \text{SERP/Discover CTR}\Big) + \text{External Direct / Social Referrals} + \text{Returning Subscribed Readers}$$

Therefore, **an action is ONLY valid if it directly impacts one of the following 4 levers or unblocks its measurement:**

```
                                  WEEKLY VISITORS
                                         │
     ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
     ▼                   ▼                               ▼                   ▼
 [LEVER 1]           [LEVER 2]                       [LEVER 3]           [LEVER 4]
INDEXATION &        TOPIC DEMAND &                  DISTRIBUTION &       RETENTION &
CADENCE             CLICK-THROUGH (CTR)             REFERRALS            RETURN VISITS
- Daily publish     - Trending topic scoring        - Reddit / HN posts  - Newsletter capture
- GSC index push    - Answer-first formatting       - LinkedIn / X posts - Daily /docket/ habit
- Clean crawl paths - Compelling titles (no bait)   - Social carousels   - RSS & bookmark
```

### Lever 1: Indexation & Cadence (Eligible Impressions Pool)
* Google cannot send visitors to URLs it has not indexed.
* **Permitted actions:**
  * Keeping the daily publication cadence alive (1 high-quality article/day without failure).
  * Auto-submitting URLs to IndexNow (Bing/Copilot/Yandex) and Google Search Console (Sitemap + Request Indexing).
  * Fixing any crawling/indexation bottleneck, sitemap error, or Google-policy compliance gate failure.
  * Ensuring the autonomous pipeline (`daily-pipeline.yml`, local ADC runner) never misses a daily cycle.

### Lever 2: Topic Selection & CTR (Winning the Click)
* High search demand + high click-through rate converts SERP impressions into site visitors.
* **Permitted actions:**
  * Mining real same-day search demand via Google Trends (IN + US) and Google Autocomplete (`engine/fetchers.py`, `scoring.py`).
  * Optimizing Title tags ({35–65} chars) and Meta Descriptions ({110–165} chars) for maximum organic CTR without clickbait.
  * Structuring hero cards and Discover-eligible image crops (16:9, 4:3, 1:1 ≥1200px) to trigger Google Discover feeds.
  * Tuning `insights.json` and `feedback.py` to boost topic keywords that already bring verified clicks.

### Lever 3: External Distribution & Referrals (Immediate Reach)
* New domains have low initial crawl priority; external links provide immediate visits AND teach Google to crawl faster.
* **Permitted actions:**
  * Generating ready-to-share social text snippets, LinkedIn posts, and X/Twitter threads for published articles.
  * Exporting high-engagement Instagram/LinkedIn carousel slides via `engine.run social` (`data/social/`).
  * Seeding relevant articles into niche communities (Hacker News, Reddit r/technology, r/artificial, r/LocalLLaMA) where the content provides genuine answers.

### Lever 4: Retention & Return Loops (Compounding Baseline)
* Converting one-time searchers into recurring weekly visitors prevents the site from having to earn every single visit from scratch.
* **Permitted actions:**
  * Activating the newsletter subscription form (`Buttondown` / `beehiiv`) on the homepage, articles, and docket.
  * Maintaining "Today's Docket" (`/docket/` and `/deck/`) as a 60-second daily reading habit.
  * Adding natural in-body internal links so each visitor reads multiple pages per visit.

### Support Lever: Measurement & Auth Unblockers
* Any action strictly required to measure the NSM (e.g. verifying GA4 tag firing, GSC credentials) or authenticate the publishing pipeline (e.g. GCP Vertex AI project ID, ADC token exchange, Workload Identity Federation) is permitted as an **enabler** of Levers 1–4.


---

## 4. The Action Filter Protocol (Mandatory Gate)

Before writing any code, modifying configurations, or proposing an action, the agent or owner must run the **North Star Impact Check**:

```markdown
### North Star Impact Check
1. Target Lever: [Lever 1: Indexation | Lever 2: CTR | Lever 3: Distribution | Lever 4: Retention | Enabler]
2. Causal Mechanism: [State in 1 sentence HOW this action creates more weekly visitors]
3. Expected Payoff Window: [Immediate (24–48h) | Short-Term (7–14d) | Medium-Term (30d)]
4. Verdict: [PROCEED / REJECT]
```

**If the check returns REJECT, the task is dropped immediately.**

---

## 5. The "DO NOT DO" Blacklist (The Traps That Steal Time)

The August 2026 strategic review proved that the project's main failure mode was **over-engineering the factory while distribution and audience sat at zero**. During this growth season, the following are strictly prohibited:

1. ❌ **No visual or CSS overhauls:** No restyling fonts, redesigning layouts, or redoing color palettes unless a measured Core Web Vital or mobile bounce rate failure demands it.
2. ❌ **No internal-tool proliferation:** No building new frameworks, sub-agents, or CLI dashboards unless they directly produce content published to the public web or distributed to readers.
3. ❌ **No architectural refactoring for "elegance":** If an existing script, gate, or builder works and passes its tests, it is left alone. Code is only touched to fix bugs, adapt to breaking APIs, or accelerate the publication of visitor-earning pages.
4. ❌ **No premature monetization complexity:** No spending hours negotiating or implementing complex ad networks before the site hits the visitor threshold required to join them (e.g., Mediavine Journey's 1,000 sessions/mo).
5. ❌ **No stealth work:** No tasks executed without stating which NSM lever they serve.

---

## 6. Current Season Milestones

| Target Date | Weekly Visitors (Sessions/Week) | Key Drivers |
|---|---|---|
| **Week 1–2 (Nov 15–22, 2026)** | **150 – 300 visitors/week** | Daily publishing restored + Google Search Console indexing sweep + first community posts |
| **Week 3–4 (Nov 23–Dec 6, 2026)** | **500 – 1,000 visitors/week** | Indexed archive hits 50+ articles + first Discover impressions + social snippets live |
| **Week 5–8 (Dec 7–Dec 31, 2026)** | **2,000 – 3,500 visitors/week** | Compounding search long-tail + newsletter return visits + topical authority in Tech & AI |

---

*Every line of code and every minute of attention must answer to this document.*


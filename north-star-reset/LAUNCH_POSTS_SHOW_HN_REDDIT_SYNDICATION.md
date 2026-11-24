# Distribution Launch Kit — Watchlist-100 & India/Global Workforce Tracker
**Author:** Amber Jain (`thetechdocket.com`)  
**Target Lever:** Lever 3 (External Referrals & Syndication) + Lever 4 (Buttondown Retention)  
**Rule:** Zero clickbait, zero AI-slop phrasing, native value first, link cleanly at the bottom.

---

## 1. Hacker News — `Show HN` (Post on Day 3: Wed Nov 25, 18:30–20:30 IST / 8:00–10:00 AM EST)

**Title (<=80 chars):**
`Show HN: Direct-ATS tech jobs & statutory layoff audit (71 feeds, zero-JS)`

**URL:**
`https://thetechdocket.com/topics/jobs/`

**First Comment (Post immediately as Amber_Jain):**
> Hi HN — I built this solo as part of The Tech Docket because almost every tech layoff tracker and job board mixes completely different signals together.
>
> Two problems kept bugging me when tracking Global and India tech employment over the last two years:
> 1. **Layoff numbers mix apples and oranges:** Commercial trackers routinely sum involuntary layoffs, voluntary buyout *eligibility* pools (e.g., 60k eligible != 60k departed), annual 10-K net headcount drops (which include hiring freezes and natural attrition), and Global + regional India slices of the same round.
> 2. **Job boards are flooded with ghost jobs and staffing clones:** Open listings on aggregators rarely match actual hiring velocity.
>
> So I built two static, zero-JS companion views backed by machine-readable JSON feeds:
> - **Audited Layoffs & Hiring Map** (`/topics/jobs/`, JSON at `/data/jobs-map.json`): Strictly separates Tier 1–2 statutory/corporate filings (SEC 8-K Item 2.05, state WARN logs, BLS CES, SEBI Reg 30) from Tier 3–4 media estimates, which stay visibly quarantined and excluded from confirmed KPI totals. Also scores 10 economies on statutory observability vs. media distortion (for example, India has no public white-collar layoff registry, and a Sept 17, 2026 EPFO wage-ceiling jump from Rs. 15k to Rs. 25k/mo creates a structural break in monthly payroll data).
> - **Direct-ATS Fresh Openings** (`/topics/jobs/openings/`, JSON at `/data/openings.json`): Polls 71 direct corporate ATS endpoints (Greenhouse, Lever, Ashby, SmartRecruiters) using Python stdlib only on a weekly GitHub Action, auto-expiring anything older than 25 days while logging `first_seen_date` in the background to measure >90-day ghost-job ratios across a 100-company Global + India watchlist (6,397 active roles in our latest crawl).
>
> Everything renders as static HTML on GitHub Pages with inline CSS and zero third-party ad/tracker bloat. Happy to hear critique on the methodology, missing statutory feeds (especially EU/APAC), or ATS edge cases.

---

## 2. Reddit — `r/developersIndia` (Post on Day 5: Fri Nov 27, 10:00–12:00 IST)

**Title:**
`I audited 2026 India IT layoffs vs. GCC hiring using filings, EPFO rules & 71 direct ATS feeds — here is what the headlines miss`

**Body (Native data first, single link at the end):**
> Everyone's feed right now is either "IT is completely dead" or "massive GCC hiring boom." Both sides usually quote numbers that don't measure what they claim to measure.
>
> I spent the last few weeks separating **confirmed statutory/corporate numbers** from **rumors and hiring pledges** for India and global tech. Four findings that stood out:
>
> 1. **Net headcount drop != layoffs:** Headlines treated TCS's FY26 net headcount drop (-23,460) and the top 5 Indian IT firms' combined FY26 net decline (-6,981) as pure layoffs. In reality, net headcount change equals `Hires + M&A - (Attrition + Retirements + Layoffs + Divestitures)`. Hiring freezes + tighter bench policies shrink headcount massively without formal retrenchment.
> 2. **Why India has "silent layoffs" while the US has public WARN logs:** Under India's Industrial Relations Code, 2020 (effective Nov 21, 2025; Central Rules May 8, 2026), formal retrenchment approval starts at 300+ workers and supervisory staff earning above Rs. 18,000/month sit outside the statutory "worker" definition. So white-collar IT/startup cuts almost never hit a government registry — they happen via PIPs, forced resignations, and off-roll vendor cuts (Quess/TeamLease/Randstad staff at GCCs).
> 3. **Watch out for a hidden Sept 2026 EPFO data trap:** Effective Sept 17, 2026 (Notification S.O. 5109(E)), the mandatory EPFO wage ceiling jumped from Rs. 15,000 to Rs. 25,000/month. Existing employees in that salary band were newly mandated into EPF, creating an artificial jump in Sept–Nov 2026 payroll additions that can look like a hiring surge or hide senior-level cuts unless adjusted.
> 4. **Where real hiring actually shows up:** Instead of relying on press-release hiring pledges or Naukri/LinkedIn duplicates, we cross-checked Grade-A commercial office leasing (GCCs leased 19.2M sq ft in H1 2026 — roughly 80–100 sq ft per seat as a 6–12 month physical proxy) and polled 71 direct company ATS feeds (Greenhouse/Ashby/Lever/SmartRecruiters), surfacing 6,397 active Watchlist-100 roles and filtering out listings older than 25 days.
>
> **Summary Split (2026):**
> - **Traditional Listed IT Services:** Net headcount flat-to-down; fresher targets (e.g., 20k–25k) are *pledges*, not realized payroll additions until onboarded.
> - **MNC GCCs & Global AI Firms in India:** Expanding physical seats and mid-career specialized hiring, though vendor/contract staff still absorb silent churn.
> - **Private Indian Startups:** Low statutory transparency; single-source layoff estimates need EPFO establishment or MCA AOC-4 cross-checks before being treated as confirmed.
>
> I put the full audited breakdown, interactive Global + India map, and the <=25-day direct-ATS openings list (free, no login, JSON open) here if anyone wants to dig into the sources:
> - India IT vs. GCC split: https://thetechdocket.com/articles/india-it-headcount-gcc-hiring-2026-divergence/
> - Live <=25-day direct-ATS openings: https://thetechdocket.com/topics/jobs/openings/
>
> Curious what people inside Bengaluru/Hyderabad/Pune/NCR GCCs are seeing on the ground right now — especially around vendor-payroll vs. full-time hiring freezes.

---

## 3. Canonical Syndication Header (Dev.to & Hashnode — Days 4 & 9)

Paste this exact front-matter at the top of each syndicated article on **Dev.to** (and set the equivalent `Canonical URL` field in **Hashnode** settings) so Google credits 100% of SEO equity to `thetechdocket.com`:

```yaml
---
title: "Watchlist-100 Audit: 6,397 Live Tech Roles vs. Layoff Noise"
published: true
description: "What 71 direct corporate ATS feeds and statutory filings show about real tech hiring vs. layoff headlines in late 2026."
tags: tech, career, ai, data
canonical_url: https://thetechdocket.com/articles/watchlist-100-ats-hiring-velocity-vs-layoff-headlines-2026/
---
```

Add one clean footer line at the bottom of syndicated copies:
> *Originally published with interactive filters and open JSON datasets by Amber Jain on [The Tech Docket](https://thetechdocket.com/topics/jobs/).*

---

## 4. LinkedIn Post (By Amber Jain — Day 4 & Day 11)

> Most layoff trackers and job boards have the same fatal flaw: they mix **headlines** with **verified payroll reality**.
>
> This week on The Tech Docket, we audited our **Top-100 Global + India Tech Watchlist** by polling **71 direct corporate ATS endpoints** (Greenhouse, Lever, Ashby, SmartRecruiters) and cross-checking SEC 8-K, WARN, and SEBI disclosures.
>
> Three numbers that contradict the doomscrolling:
> 1. **6,397 active Watchlist-100 roles** are live right now across verified direct company boards (and we auto-expire anything >25 days old on our public openings board to cut ghost jobs).
> 2. **US nonfarm payrolls rose +885,000** over the 12 months ending Oct 2026 (BLS CES), even while the Information sector shed 119,000 roles — capital is rotating, not vanishing.
> 3. **In India, top 5 IT services shed 6,981 net roles in FY26**, while MNC GCCs leased **19.2M sq ft** of Grade-A office space in H1 2026.
>
> We keep Tier 3 rumors, voluntary buyout eligible pools (like 60,000 eligible != 60,000 laid off), and hiring pledges strictly quarantined from confirmed totals.
>
> Explore the open dataset & <=25-day direct-apply openings (no login, zero affiliate links):
> https://thetechdocket.com/topics/jobs/

---

## 5. Buttondown Weekly Digest Template — Issue #1 (Send Sunday Nov 29, 19:00 IST)

**Subject:** `The Tech Docket Weekly: 6,397 verified live roles vs. November layoff noise`  
**From:** Amber Jain — The Tech Docket

> Hi — here is this week's verified signal from The Tech Docket (zero rumors, zero affiliate links, primary filings only).
>
> **1. Confirmed Watchlist-100 Layoffs (Tier 1–2 Only)**
> - [Insert verified SEC 8-K / WARN / SEBI Reg 30 entries from Sunday's Task 1B run, or write: "Zero new Tier 1–2 statutory layoff filings across the Watchlist-100 this week; N media reports remain quarantined pending primary confirmation."]
>
> **2. Direct-ATS Hiring Velocity (<=25 Days Old)**
> - Top 3 surging Watchlist-100 employers from Sunday's `data/openings.json` refresh: [Company A], [Company B], [Company C].
> - Browse all fresh direct-apply roles: https://thetechdocket.com/topics/jobs/openings/
>
> **3. One Viral Claim We Quarantined This Week**
> - [Insert 2-line explanation of 1 viral headline/pledge/VEP pool rejected from confirmed totals and why.]
>
> **4. Top Reads This Week**
> - Watchlist-100 Audit: 6,397 Live Tech Roles vs. Layoff Noise — https://thetechdocket.com/articles/watchlist-100-ats-hiring-velocity-vs-layoff-headlines-2026/
> - India IT Headcount vs. GCC Hiring in 2026 — https://thetechdocket.com/articles/india-it-headcount-gcc-hiring-2026-divergence/
> - Global Tech Layoffs 2026: Statutory Filings vs. Headlines — https://thetechdocket.com/articles/global-tech-layoffs-2026-filings-vs-headlines/
>
> — Amber Jain  
> https://thetechdocket.com

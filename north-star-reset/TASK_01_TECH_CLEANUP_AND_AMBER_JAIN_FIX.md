# TASK 01 — Technical Blockers Cleanup & Unified "Amber Jain" Identity Pass

**Project:** The Tech Docket (`thetechdocket.com` / `github.com/Jainamber/TheTechDocket`)  
**Owner & Canonical Author:** Amber Jain (`slug: amber-jain`)  
**North Star Impact Check:**
- **Target Lever:** Lever 1 (Classic & AI Search Retrieval) + Enabler (Telemetry)
- **Causal Mechanism:** Eliminates automated 404 deletions, fixes author/HTTP canonical splits, resolves a failing hard gate, and restores the GSC feedback loop so crawl budget and scoring directly compound Weekly Visitors.
- **Expected Payoff Window:** Immediate (24-48h) to Short-Term (7-14d)
- **Verdict:** PROCEED

---

## 1. Standardize Owner & Author Name Everywhere to `Amber Jain`
1. Verify `config.yaml` has:
   - `author.name: "Amber Jain"`
   - `author.slug: "amber-jain"`
   - `author.bio_verified: true`
   - `author.photo_alt: "Amber Jain, founder and editor of The Tech Docket"`
2. Update `Owner:` / byline references from `Saurab Jain` -> `Amber Jain` in:
   - `NORTH_STAR.md`
   - `STRATEGY-90D.md` (and root copy if mirrored)
   - Any active templates or static pages (`/about/`, `/editorial-policy/`, `/contact/`) that hardcode the old name.
3. **Preserve Indexed Equity (Zero 404 on Old Author URL):**
   - Because Google currently indexes `https://thetechdocket.com/authors/saurab-jain/`, generate a lightweight static HTML redirect stub at `docs/authors/saurab-jain/index.html` (and ensure `engine/build.py` preserves it on rebuild) containing:
     - `<meta http-equiv="refresh" content="0; url=https://thetechdocket.com/authors/amber-jain/">`
     - `<link rel="canonical" href="https://thetechdocket.com/authors/amber-jain/">`
     - `<meta name="robots" content="noindex, follow">`
     - A clean fallback anchor link to `/authors/amber-jain/`.
   - Do **not** include `/authors/saurab-jain/` in `sitemap.xml`.

## 2. Disable `prune-old-content.yml` & Restore High-Value URLs
1. Edit `.github/workflows/prune-old-content.yml`:
   - Remove the `schedule: - cron: '0 2 * * 0'` block so weekly automated deletions stop immediately. Keep `workflow_dispatch:` only if you ever want manual dry-runs.
2. Restore high-traffic / indexed articles removed during recent pruning from Git history (starting with `free-ai-tiers-compared`, which is #2 in `data/insights.json`, plus any July/August `ai-models` articles that had search visibility), OR if a hub like `/topics/ai-tools/` is permanently retired, emit a static HTML redirect stub at `docs/topics/ai-tools/index.html` -> `https://thetechdocket.com/topics/ai-models/` (with `rel="canonical"` + `noindex, follow`) so Google doesn't hit a hard 404.
3. Policy going forward: **Refresh aged winners in place** using `updated: YYYY-MM-DD` and `update_note:` (gate `G05-real-update`) instead of deleting indexed pages.

## 3. Fix Gate Failure, Re-Sync `data/history.json`, and Lock 1-Article/Day Cap
1. Fix `content/articles/2026-11-22-what-rises-when-tech-jobs-fall-2027-shifts.md` so **`G22-ymyl` passes** (0 hard failures):
   - Either rephrase the two security-trigger terms (`vulnerability`, `fraud`) if the piece is finance/career-focused, OR add `ymyl: security` compliance (primary security source + disclaimer) per `engine/gates.py`.
   - Re-run `python -m engine.run build && python -m engine.run gate --slug what-rises-when-tech-jobs-fall-2027-shifts` and confirm `passed: true, hard_failures: 0`.
2. Re-sync `data/history.json`:
   - Audit every markdown file in `content/articles/` against `data/history.json`. Add missing live published entries (including `what-rises-when-tech-jobs-fall-2027-shifts`, `cursor-chinese-open-weight-models-sarvam-deepseek`, and `gemini-4-neon-benchmarks-pricing-antigravity-desync`) so `engine/feedback.py` hub aggregation and deduplication work accurately.
3. Audit `data/jobs-map.json` against the Verification SOP:
   - Fix `oracle-2026-09-in` (no fabricated midpoint: `headcount_exact: null`, `headcount_min: 1000`, `headcount_max: 3000`, `confidence_tier: "Tier 3"`, `quarantined: true`).
   - Change `event_type` on `cognizant-hiring-2026-in`, `infosys-hiring-2026-in`, and `anthropic-hiring-2026-eu` from `realized_payroll_hires_net_change` to `announced_hiring_intent`.
   - Ensure secondary trackers (`Computerworld`, `Weekday`, `Intellizence`, `Macrotrends`) are replaced with primary SEC/WARN/SEBI/corporate URLs on Tier 1-2 rows, or demoted to `Tier 3` (`quarantined: true`).
4. Enforce strict **1 article/day** publishing cadence (no multi-article bursts).

## 4. Clean Repo Bloat (`openings-history.json` & `BACKUP_*` Files)
1. In `engine/openings_fetch.py`: store ONLY Watchlist-100 matched requisitions (`watchlist_slug is not None`) in `data/openings-history.json` (and prune vanished reqs older than 120 days) so the file stays lightweight (<200 KB) instead of 2.9 MB in Git history.
2. Move all root `BACKUP_*` files (`BACKUP_jobs_hub_v1..v11`, `BACKUP_build_py_v2..v6`, `BACKUP_config_*`, etc.) out of the repo root into a gitignored local archive folder (`_local_backups/`).

## 5. Manual Owner Actions (10 Minutes Total)
- [ ] **Cloudflare DNS + GitHub Pages:** Enable **Always Use HTTPS** so `http://thetechdocket.com/docket/` permanently redirects `301` to `https://thetechdocket.com/docket/`.
- [ ] **Google Search Console:** Export `Pages.csv` and `Queries.csv` (last 28 days) into `data/search-console/`, then run `python -m engine.feedback` to populate `data/insights.json` and refresh `data/reports/analytics-latest.html`.
- [ ] **Entity Profiles:** Add official LinkedIn Page, X handle, Dev.to, and Hashnode URLs to `config.yaml -> site.twitter_handle` and `site.social_profiles`, then rebuild and push.

## Verification Command Checklist
```bash
python -m engine.run build
python -m engine.run gate --slug what-rises-when-tech-jobs-fall-2027-shifts
python -m engine.feedback
pytest -q
```
Confirm: 0 hard failures, `Amber Jain` everywhere, redirect stubs present, `history.json` in sync, then commit and push.

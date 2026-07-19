# The Tech Docket — Trend-Driven Daily Content Engine

An automated publishing system that mines **same-day search-demand data**
(Google Trends India + US, news momentum, tech-community signals), picks the
strongest genuinely-relevant topic in its configured niche, and publishes one
deeply-researched, SEO-complete article per day to a static site — with
Google-policy compliance enforced by machine-checkable gates.

**Broad topic is user-configurable** (`config.yaml → topic`). Currently:
*Tech & AI*, markets *India + Global*.

## How a day works

```
00:15 UTC  GitHub Action `fetch-trends` pulls raw signals with open internet
           (Trends RSS IN/US, Google News RSS, autocomplete, Hacker News,
            Wikipedia pageviews, outlet feeds) → commits data/inbox/DATE.json

01:00 UTC  Scheduled Cowork session (the editorial brain) wakes up:
(06:30 IST)  select   → scores/filters candidates against topic + history
             brief    → data/briefs/DATE.md (the writing contract)
             research → WebSearch/WebFetch: primary sources, India+global angle
             write    → content/articles/DATE-slug.md (front-matter + markdown)
             build    → docs/ static site (hero images auto-generated)
             gate     → 40+ compliance & SEO checks (below) — hard-fail = no publish
             publish  → git push → GitHub Pages deploys
             docket   → Today's Docket: 4–8 tiny sourced shorts at /docket/
                        from the day's remaining scored candidates (own gate
                        suite D01–D09; optional — never blocks the article)

on push    GitHub Action `on-publish` pings IndexNow (Bing ecosystem) and
           WebSub (instant feed notification). Google indexes via sitemap/feed.
```

## What "SEO built in" means here (July 2026 state of the art)

- Answer-first structure (the top factor for AI Overview/ChatGPT citation),
  clean H-hierarchy, comparison tables, FAQ from real autocomplete queries.
- Full metadata: title/meta-desc length gates, canonical, OG + Twitter cards,
  `max-image-preview:large`, BlogPosting + BreadcrumbList + Organization +
  ProfilePage JSON-LD with 3-crop image arrays (16:9, 4:3, 1:1 — all ≥1200px,
  auto-generated) — Discover-eligible by design.
- Core Web Vitals by construction: static HTML, inline critical CSS, system
  fonts, zero JS, explicit image dimensions, `fetchpriority="high"` hero.
- Discovery plumbing: sitemap.xml (accurate lastmod only), RSS + WebSub hub,
  IndexNow, robots.txt welcoming classic + AI-search crawlers, topic hubs,
  internal-link gates, HTML sitemap (no orphans).
- Deliberately omitted (verified obsolete/ineligible in 2026): FAQ/HowTo
  rich-result chasing, llms.txt, Google Indexing API, news sitemap.

## Google-policy compliance (the gates)

`engine/gates.py` enforces ~40 checks before any publish, derived from
Google's spam policies, people-first content guidance, E-E-A-T docs and
Discover requirements (research notes in `research/`). Highlights:

- **Scaled-content-abuse guards:** one article/day, originality check vs own
  archive, required original-analysis section, "never force a post" (weak
  trend days fall back to an evergreen explainer or skip).
- **E-E-A-T:** real named author + ProfilePage, visible/structured dates that
  never bump without a logged substantive update, editorial-policy + about +
  contact pages, per-article "How this article was made" AI disclosure.
- **Accuracy:** every statistic requires an inline source link in the same
  paragraph; ≥2 authoritative citations; logged review checklist per article.
- **No clickbait** (Discover policy), **YMYL handling** (finance/health/
  security topics require disclaimer + primary source), **no affiliate/
  sponsored content** in v1, **no third-party bylines**.

## Repo layout

```
config.yaml            ← topic, markets, author, scoring, SEO thresholds
engine/                ← fetchers, scoring, brief, images, build, gates, publish
engine/templates/      ← Jinja2 HTML (inline CSS, zero JS)
content/articles/      ← one markdown file per article (front-matter contract)
data/inbox/            ← raw daily trend signals (committed for auditability)
data/briefs/           ← daily briefs + scored candidate lists
data/docket/           ← Today's Docket entries (daily shorts strip, /docket/)
data/gate-reports/     ← per-publish compliance reports
data/history.json      ← publish log (dedup memory)
docs/                  ← BUILT SITE (GitHub Pages serves this)
DAILY_RUN.md           ← operating manual for the daily editorial session
.github/workflows/     ← fetch-trends (00:15 UTC), on-publish (pings)
```

## Local / manual run

```bash
pip install -r requirements.txt
python -m engine.run fetch     # needs open internet (or write inbox manually)
python -m engine.run select && python -m engine.run brief
# … write content/articles/DATE-slug.md per DAILY_RUN.md …
python -m engine.run build
python -m engine.run gate --slug your-slug
python -m engine.run publish --slug your-slug --no-push
```

## Deploy checklist (one-time)

1. Create a **public** GitHub repo; push this folder.
2. Repo Settings → Pages → Source: `main` branch, `/docs` folder.
3. Set `site.base_url` in `config.yaml` to the Pages URL; set
   `seo.indexnow_key` to a random 32-hex string; rebuild; push.
4. Create the daily scheduled task (Cowork) with a fine-grained PAT
   (Contents: Read/Write on this repo only).
5. [Google Search Console](https://search.google.com/search-console): verify
   the property, submit `sitemap.xml`. Then Bing Webmaster Tools → "Import
   from Google Search Console".
6. Optional accelerators: link the site from your GitHub profile/LinkedIn/X;
   custom domain later (update `base_url`, add `CNAME` file to docs/).

## Retargeting the engine to another niche

Edit `config.yaml`: `topic` (name/description/allow/deny keywords),
`news_seed_queries`, `evergreen_backlog`, `content.hubs`, site name/tagline.
Everything else adapts automatically.

## Realistic expectations

New domains typically see first meaningful Search impressions in 3–6 months;
long-tail/freshness queries can land in days. Discover traffic (the viral
channel) usually requires ~a few weeks of consistent, indexed, policy-clean
publishing. The engine's edge is consistency + freshness + policy safety.

## Roadmap

- Apply for the official **Google Trends API alpha** (invite-only; replaces
  the unofficial RSS when granted).
- **Search Console API feedback loop** once verified: feed real
  impression/click data back into topic scoring.
- Keyword Planner volumes (needs Google Ads account + token approval).
- Social auto-drafts (X/LinkedIn/Reddit-safe snippets) per article.

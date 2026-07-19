"""Pre-publish gate suite: Google-policy compliance + SEO checks.

Derived from Google's spam policies (scaled content abuse), people-first
content guidance, E-E-A-T documentation, Discover requirements and the
2026 SEO implementation checklist (see research/ in the repo).

Usage:  python -m engine.run gate --slug <slug>
Exit code 0 = all HARD gates pass. Report written to data/gate-reports/.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from PIL import Image

from .util import (ROOT, all_articles, jaccard, load_config, load_history,
                   now_ist, shingles, tokenize)

HARD, SOFT = "hard", "soft"

CLICKBAIT_RE = re.compile(
    r"you won'?t believe|will shock|shocking truth|blow your mind|"
    r"this one trick|one weird|secret(?:s)? (?:that|they)|"
    r"they don'?t want you|number \d+ will|gone wrong|jaw.?dropping", re.I)

STAT_RE = re.compile(
    r"(\d+(?:\.\d+)?\s?%)|([₹$€£]\s?\d)|(\b\d[\d,]*(?:\.\d+)?\s?"
    r"(?:crore|lakh|million|billion|trillion)\b)", re.I)


class GateRunner:
    def __init__(self, slug: str):
        self.cfg = load_config()
        self.slug = slug
        self.arts = all_articles()
        self.article = next((a for a in self.arts if a.get("slug") == slug), None)
        if not self.article:
            raise SystemExit(f"no article with slug '{slug}' in content/articles/")
        out = ROOT / self.cfg["publishing"]["output_dir"]
        self.page_path = out / "articles" / slug / "index.html"
        if not self.page_path.exists():
            raise SystemExit("built page missing — run `python -m engine.run build` first")
        self.html = self.page_path.read_text(encoding="utf-8")
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.body = self.soup.find("article", class_="post")
        self.out_dir = out
        self.results: list[dict] = []

    def check(self, gid: str, level: str, ok: bool, detail: str = ""):
        self.results.append({"gate": gid, "level": level,
                             "ok": bool(ok), "detail": detail[:300]})

    # ---------- helpers ----------
    def _jsonld(self, at_type: str) -> dict | None:
        for s in self.soup.find_all("script", type="application/ld+json"):
            try:
                d = json.loads(s.string or "")
            except json.JSONDecodeError:
                continue
            if d.get("@type") == at_type:
                return d
        return None

    def _own_host(self) -> str:
        return urlparse(self.cfg["site"]["base_url"]).netloc

    # ---------- gates ----------
    def run(self) -> dict:
        cfg, a, soup = self.cfg, self.article, self.soup
        seo = cfg["seo"]

        # G1-2 byline & author identity
        bp = self._jsonld("BlogPosting")
        self.check("G01-byline", HARD,
                   bp is not None and bp.get("author", {}).get("name")
                   == cfg["author"]["name"]
                   and cfg["author"]["name"] in soup.get_text(),
                   "visible byline + JSON-LD author must equal config author")
        self.check("G02-author-name-plain", HARD,
                   bp is not None and bp.get("author", {}).get("name",
                   "").strip() == cfg["author"]["name"].strip())
        author_page = (self.out_dir / "authors" / cfg["author"]["slug"]
                       / "index.html")
        self.check("G03-author-page", HARD,
                   author_page.exists() and
                   f"authors/{cfg['author']['slug']}/" in self.html)
        self.check("G13-bio-verified", HARD,
                   bool(cfg["author"].get("bio_verified")),
                   "config author.bio_verified must be attested true by the owner")

        # G4-5 dates
        today = now_ist().date()
        adate = a["date"] if not isinstance(a["date"], str) else \
            datetime.strptime(a["date"], "%Y-%m-%d").date()
        self.check("G04-date-valid", HARD,
                   adate <= today and bp is not None
                   and bp.get("datePublished", "").startswith(str(adate)),
                   f"date {adate} must not be future & must match JSON-LD")
        if a.get("updated"):
            self.check("G05-real-update", HARD, bool(a.get("update_note")),
                       "updated: set but update_note: missing — no silent date bumps")
        else:
            self.check("G05-real-update", HARD,
                       bp is not None and bp.get("dateModified")
                       == bp.get("datePublished"),
                       "dateModified must equal datePublished when never updated")

        # G6 citations
        own = self._own_host()
        ext_links = {urlparse(x.get("href", "")).netloc
                     for x in (self.body.find_all("a", href=True) if self.body else [])
                     if x.get("href", "").startswith("http")
                     and urlparse(x["href"]).netloc
                     and own not in urlparse(x["href"]).netloc}
        social = {"twitter.com", "www.linkedin.com", "wa.me",
                  "www.reddit.com", "news.ycombinator.com"}
        cite_hosts = {h for h in ext_links if h not in social}
        n_sources = len(a.get("sources", []))
        self.check("G06-citations", HARD,
                   len(cite_hosts) >= seo["outbound_citations_min"]
                   and n_sources >= seo["outbound_citations_min"],
                   f"{len(cite_hosts)} external citation domains, "
                   f"{n_sources} listed sources (need ≥{seo['outbound_citations_min']})")

        # G7 stats sourced
        unsourced = []
        for p in (self.body.find_all("p") if self.body else []):
            if p.find_parent(class_="share") or p.find_parent(class_="methodology"):
                continue
            txt = p.get_text()
            if STAT_RE.search(txt):
                has_ext = any(x.get("href", "").startswith("http")
                              and own not in x["href"]
                              for x in p.find_all("a", href=True))
                if not has_ext:
                    unsourced.append(txt[:90])
        self.check("G07-stats-sourced", HARD, not unsourced,
                   "stat paragraphs missing inline source link: "
                   + " | ".join(unsourced[:3]))

        # G8 clickbait
        title = a["title"]
        self.check("G08-no-clickbait", HARD,
                   not CLICKBAIT_RE.search(title)
                   and title.count("!") <= 1
                   and not re.search(r"\b[A-Z]{5,}\b", title)
                   and bool(a.get("review", {}).get("title_promise_check")
                            in (True, "pass")),
                   "clickbait pattern / caps / missing review.title_promise_check")

        # G9 originality vs own archive
        toks = shingles(tokenize(a["_body_md"]))
        max_sim, worst = 0.0, ""
        for other in self.arts:
            if other["slug"] == a["slug"]:
                continue
            sim = jaccard(toks, shingles(tokenize(other["_body_md"])))
            if sim > max_sim:
                max_sim, worst = sim, other["slug"]
        self.check("G09-originality", HARD, max_sim < 0.30,
                   f"max 5-gram overlap {max_sim:.2f} vs '{worst}' (limit .30)")

        # G10 original value
        heads = [h.get_text().strip().lower()
                 for h in (self.body.find_all(["h2", "h3"]) if self.body else [])]
        markers = [m.lower() for m in cfg["content"]["original_analysis_headings"]]
        self.check("G10-original-analysis", HARD,
                   bool(str(a.get("original_value", "")).strip())
                   and any(any(m in h for m in markers) for h in heads),
                   "front-matter original_value + an analysis H2 "
                   f"({', '.join(cfg['content']['original_analysis_headings'])}) required")

        # G11 review block
        rev = a.get("review") or {}
        needed = ["facts_verified", "sources_checked", "title_promise_check",
                  "no_fabrication", "policy_pass"]
        self.check("G11-review-log", HARD,
                   all(rev.get(k) in (True, "pass") for k in needed)
                   and bool(rev.get("reviewed_at")),
                   f"front-matter review block needs {needed} + reviewed_at")

        # G12 AI disclosure
        self.check("G12-ai-disclosure", HARD,
                   "How this article was made" in self.html
                   and (self.out_dir / "editorial-policy" / "index.html").exists())

        # G14-18 images
        img_dir = self.out_dir / "articles" / self.slug
        crops_ok, detail = True, []
        for label, (w, h) in {"16x9": (1200, 675), "4x3": (1200, 900),
                              "1x1": (1200, 1200)}.items():
            f = img_dir / f"{self.slug}-{label}.jpg"
            if not f.exists():
                crops_ok, detail = False, detail + [f"missing {f.name}"]
                continue
            iw, ih = Image.open(f).size
            if (iw, ih) != (w, h):
                crops_ok = False
                detail.append(f"{f.name} is {iw}x{ih} not {w}x{h}")
        self.check("G14-hero-crops", HARD, crops_ok, "; ".join(detail))
        hero = self.body.select_one("figure.hero img") if self.body else None
        self.check("G16-hero-img-tag", HARD,
                   hero is not None and hero.get("fetchpriority") == "high"
                   and hero.get("width") and hero.get("height")
                   and (hero.get("alt") or "").strip() != "")
        robots = soup.find("meta", attrs={"name": "robots"})
        self.check("G15-max-image-preview", HARD,
                   robots is not None
                   and "max-image-preview:large" in robots.get("content", ""))
        og_img = soup.find("meta", property="og:image")
        self.check("G17-og-image", HARD,
                   og_img is not None and self.slug in og_img.get("content", ""))
        lazy_bad = [i.get("src", "")[:60] for i in
                    (self.body.find_all("img") if self.body else [])
                    if i is not hero and i.get("loading") != "lazy"]
        self.check("G18-below-fold-lazy", SOFT, not lazy_bad,
                    "non-lazy below-fold imgs: " + ", ".join(lazy_bad[:3]))

        # G19 JSON-LD completeness
        ld_ok = (bp is not None and len(bp.get("image", [])) == 3
                 and "+05:30" in bp.get("datePublished", "")
                 and len(bp.get("headline", "")) <= 110
                 and bp.get("publisher", {}).get("logo", {}).get("url")
                 and self._jsonld("BreadcrumbList") is not None)
        self.check("G19-jsonld", HARD, bool(ld_ok),
                   "BlogPosting needs 3 images, tz dates, headline<=110, "
                   "publisher logo; BreadcrumbList required")

        # G20 indexability
        canonical = soup.find("link", rel="canonical")
        expected = cfg["site"]["base_url"].rstrip("/") + f"/articles/{self.slug}/"
        self.check("G20-indexable", HARD,
                   robots is not None and "noindex" not in robots.get("content", "")
                   and canonical is not None
                   and canonical.get("href") == expected,
                   f"canonical must be {expected}")

        # G21 page-weight proxies (CWV)
        html_kb = len(self.html.encode()) / 1024
        hero_kb = ((img_dir / f"{self.slug}-16x9.jpg").stat().st_size / 1024
                   if (img_dir / f"{self.slug}-16x9.jpg").exists() else 999)
        self.check("G21-page-weight", SOFT,
                   html_kb <= 90 and hero_kb <= 320,
                   f"html {html_kb:.0f}KB (<=90), hero {hero_kb:.0f}KB (<=320)")

        # G22 YMYL
        body_l = a["_body_md"].lower()
        trig = {k: [t for t in terms if t in body_l]
                for k, terms in (("finance", cfg["ymyl"]["finance_terms"]),
                                 ("health", cfg["ymyl"]["health_terms"]),
                                 ("security", cfg["ymyl"]["safety_terms"]))}
        hits = {k: v for k, v in trig.items() if len(v) >= 2}
        if hits:
            has_primary = any(s.get("primary") for s in a.get("sources", []))
            # rendered element, not substring: 'disclaimer' appears in every
            # page's CSS, which made this clause vacuous (finding F3b, 07-16)
            disclaimer_el = (self.body.select_one("div.disclaimer")
                             if self.body else None)
            self.check("G22-ymyl", HARD,
                       a.get("ymyl") in hits.keys() and has_primary
                       and disclaimer_el is not None,
                       f"YMYL terms {hits} → front-matter ymyl: "
                       f"{list(hits)[0]}, a primary:true source and rendered "
                       "disclaimer are required")
        else:
            self.check("G22-ymyl", HARD, True, "no YMYL trigger")

        # G23 affiliates
        aff = re.search(r"amzn\.to|tag=amazon|affid=|utm_medium=affiliate|"
                        r'rel="sponsored"', self.html, re.I)
        self.check("G23-no-affiliate", HARD,
                   (not cfg["content"]["allow_affiliate"]) and not aff,
                   "v1 forbids monetized links")

        # G24 site trust pages
        need = ["about/index.html", "editorial-policy/index.html",
                "sitemap/index.html", "404.html", ".nojekyll", "robots.txt",
                "sitemap.xml", "feed.xml", "favicon.svg"]
        missing = [n for n in need if not (self.out_dir / n).exists()]
        self.check("G24-site-pages", HARD, not missing,
                   "missing: " + ", ".join(missing))

        # P01: static/trust pages must meet the same meta-description bounds
        # as articles — they were previously ungated and shipped truncated
        # (finding F3d, 07-16). Fails until `build` is re-run with the
        # sentence-aware _meta_desc().
        seo_cfg = cfg["seo"]
        bad_meta = []
        static_pages = [p for p in ["about/index.html",
                                    "editorial-policy/index.html"]
                        if (self.out_dir / p).exists()]
        static_pages += [str(p.relative_to(self.out_dir))
                         for p in self.out_dir.glob("authors/*/index.html")]
        for rel in static_pages:
            psoup = BeautifulSoup((self.out_dir / rel).read_text(
                encoding="utf-8"), "html.parser")
            md_tag = psoup.find("meta", attrs={"name": "description"})
            mlen = len(md_tag.get("content", "")) if md_tag else 0
            if not (seo_cfg["meta_desc_min_chars"] <= mlen
                    <= seo_cfg["meta_desc_max_chars"]):
                bad_meta.append(f"{rel}({mlen})")
        self.check("P01-static-meta", HARD, not bad_meta,
                   "static pages with out-of-bounds meta description: "
                   + ", ".join(bad_meta))

        # G25 first-party only
        self.check("G25-first-party", HARD,
                   not a.get("guest_author"), "single first-party byline only")

        # ---------- SEO gates ----------
        t = soup.title.get_text() if soup.title else ""
        base_title = t.rsplit(" — ", 1)[0]
        self.check("S01-title-length", HARD,
                   seo["title_min_chars"] <= len(base_title)
                   <= seo["title_max_chars"],
                   f"title {len(base_title)} chars "
                   f"(need {seo['title_min_chars']}–{seo['title_max_chars']})")
        desc = soup.find("meta", attrs={"name": "description"})
        dlen = len(desc.get("content", "")) if desc else 0
        self.check("S02-meta-desc", HARD,
                   seo["meta_desc_min_chars"] <= dlen
                   <= seo["meta_desc_max_chars"],
                   f"meta description {dlen} chars")
        h1s = self.body.find_all("h1") if self.body else []
        self.check("S03-single-h1", HARD, len(h1s) == 1)

        # answer-first paragraph: first rendered <p> of the article body
        # (after byline/hero) must be >=40 words and precede any h2
        first_p = None
        if self.body:
            for el in self.body.find_all(["p", "h2"]):
                if el.name == "h2":
                    break
                if el.name == "p" and not el.find_parent(
                        ["figure", "div"], class_=["byline", "share",
                                                   "methodology", "disclaimer"]):
                    first_p = el
                    break
        wc_first = len((first_p.get_text() if first_p else "").split())
        self.check("S04-answer-first", HARD, wc_first >= 40,
                   f"first paragraph {wc_first} words (need ≥40 before any H2)")

        # count only the article's OWN H2s — the template injects Sources,
        # FAQ and Related headings unconditionally, which previously made
        # this gate unfailable (finding F3a, 07-16)
        h2s = [h for h in (self.body.find_all("h2") if self.body else [])
               if h.get("id") not in ("faq", "sources")
               and not h.find_parent("section", class_="sources")
               and not h.find_parent("section", class_="related")]
        self.check("S05-h2-count", HARD, len(h2s) >= 3,
                   f"{len(h2s)} body H2 sections excl. template chrome (need ≥3)")
        levels = [int(h.name[1]) for h in
                  (self.body.find_all(["h1", "h2", "h3", "h4"]) if self.body else [])]
        skips = any(levels[i + 1] - levels[i] > 1 for i in range(len(levels) - 1))
        self.check("S06-heading-hierarchy", HARD, not skips)

        words = len(re.findall(r"\w+", a["_body_md"]))
        self.check("S07-word-count", HARD,
                   cfg["content"]["min_words"] <= words
                   <= cfg["content"]["max_words"],
                   f"{words} words (need {cfg['content']['min_words']}–"
                   f"{cfg['content']['max_words']})")

        self.check("S08-slug", HARD,
                   bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+){1,9}", self.slug)))
        # every previously-published slug must still exist (renaming/deleting a
        # published article's slug breaks its live URL — GitHub Pages can't 301)
        hist = load_history()
        current_slugs = {x.get("slug") for x in self.arts}
        orphaned = [p["slug"] for p in hist["published"]
                    if p["slug"] not in current_slugs]
        self.check("S08b-slug-stable", HARD, not orphaned,
                   "published slugs missing from content/: " + ", ".join(orphaned))

        n_arts = len(self.arts)
        internal = [x for x in (self.body.find_all("a", href=True)
                                if self.body else [])
                    if "/articles/" in x["href"] and self.slug not in x["href"]]
        min_int = seo["internal_links_min"] if n_arts >= 3 else 0
        self.check("S09-internal-links", HARD, len(internal) >= min_int,
                   f"{len(internal)} internal article links (need ≥{min_int})")
        # in-body only: breadcrumb, hub-chip and nav guarantee a page-wide hub
        # link on every page, which made this gate unfailable (finding F3c,
        # 07-16). The writing contract now requires one natural in-body hub
        # link (see DAILY_RUN.md).
        hub_link = any(f"/topics/{a.get('hub')}/" in x.get("href", "")
                       for x in (self.body.find_all("a", href=True)
                                 if self.body else [])
                       if not x.find_parent("nav", class_="crumbs")
                       and not x.find_parent("div", class_="byline"))
        self.check("S10-hub-link", HARD, hub_link,
                   "one in-body link to the article's hub page required "
                   "(nav/breadcrumb/chip links don't count)")

        og_need = ["og:type", "og:site_name", "og:title", "og:description",
                   "og:url", "og:image", "og:image:width", "og:image:height",
                   "og:image:alt", "og:locale", "article:published_time",
                   "article:author", "article:section"]
        og_missing = [p for p in og_need if not soup.find("meta", property=p)]
        self.check("S11-open-graph", HARD, not og_missing,
                   "missing: " + ", ".join(og_missing))
        tw = soup.find("meta", attrs={"name": "twitter:card"})
        self.check("S12-twitter-card", HARD,
                   tw is not None and tw.get("content") == "summary_large_image")

        alt_missing = [i.get("src", "")[:50] for i in
                       (self.body.find_all("img") if self.body else [])
                       if not (i.get("alt") or "").strip()]
        self.check("S13-img-alts", HARD, not alt_missing)

        sm = (self.out_dir / "sitemap.xml").read_text(encoding="utf-8") \
            if (self.out_dir / "sitemap.xml").exists() else ""
        feed = (self.out_dir / "feed.xml").read_text(encoding="utf-8") \
            if (self.out_dir / "feed.xml").exists() else ""
        url = f"articles/{self.slug}/"
        self.check("S14-in-sitemap-feed", HARD, url in sm and url in feed)

        self.check("S15-desc-not-title", SOFT,
                   (desc.get("content", "") if desc else "") != a["title"],
                   "meta description should not simply repeat the title")

        return self.report()

    def report(self) -> dict:
        hard_fail = [r for r in self.results if r["level"] == HARD and not r["ok"]]
        soft_fail = [r for r in self.results if r["level"] == SOFT and not r["ok"]]
        rep = {"slug": self.slug, "checked_at": now_ist().isoformat(),
               "passed": not hard_fail,
               "hard_failures": len(hard_fail), "soft_warnings": len(soft_fail),
               "results": self.results}
        out = ROOT / "data" / "gate-reports"
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"{now_ist().date()}-{self.slug}.json"
        path.write_text(json.dumps(rep, indent=2, ensure_ascii=False),
                        encoding="utf-8")
        for r in self.results:
            mark = "PASS" if r["ok"] else ("WARN" if r["level"] == SOFT else "FAIL")
            line = f"[{mark}] {r['gate']}"
            if not r["ok"] and r["detail"]:
                line += f" — {r['detail']}"
            print(line)
        print(f"\n{'ALL HARD GATES PASSED' if rep['passed'] else 'HARD GATE FAILURES: ' + str(len(hard_fail))}"
              f" ({len(soft_fail)} soft warnings) → {path}")
        return rep


def run_gates(slug: str) -> dict:
    return GateRunner(slug).run()

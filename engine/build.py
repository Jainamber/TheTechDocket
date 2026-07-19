"""Static site builder — renders content/ into docs/ (GitHub Pages root).

Implements the July-2026 SEO checklist: full meta/OG/Twitter sets,
BlogPosting + BreadcrumbList + Organization + ProfilePage JSON-LD,
max-image-preview:large, 3-crop hero images, sitemap.xml (lastmod only),
RSS feed with WebSub hub, robots.txt with explicit AI-crawler policy,
inline critical CSS, system fonts, zero JavaScript.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import urlparse

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from . import images
from .docket import all_dockets
from .util import IST, ROOT, all_articles, load_config, now_ist

MD = md.Markdown(extensions=["tables", "fenced_code", "sane_lists", "smarty"])


def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(ROOT / "engine" / "templates"),
        autoescape=select_autoescape(["html"]))
    return env


def base_path(cfg) -> str:
    p = urlparse(cfg["site"]["base_url"]).path or "/"
    return p if p.endswith("/") else p + "/"


def abs_url(cfg, path: str) -> str:
    return cfg["site"]["base_url"].rstrip("/") + "/" + path.lstrip("/")


def _publish_dt(cfg, a: dict, key: str = "date") -> datetime:
    d = a[key] if key in a and a[key] else a["date"]
    if isinstance(d, str):
        d = datetime.strptime(d, "%Y-%m-%d").date()
    return datetime(d.year, d.month, d.day,
                    cfg["publishing"]["publish_hour_ist"], 0, 0, tzinfo=IST)


def _human(dt: datetime) -> str:
    # NB: no %-d — that strftime flag is glibc-only and raises ValueError on
    # Windows (review finding F2a, 2026-07-16). Compose portably instead.
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def _meta_desc(text: str, lo: int = 110, hi: int = 165) -> str:
    """Sentence-aware meta description within [lo, hi] chars.

    Replaces blind [:160] slices that produced mid-sentence truncation and
    sub-minimum descriptions on static pages (review finding F3d, 2026-07-16).
    Strips markdown markers, joins whole text, cuts at the last sentence end
    past `lo` when possible, else at a word boundary with an ellipsis.
    """
    plain = re.sub(r"[*_`#>\[\]]+", " ", text or "")
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) <= hi:
        return plain
    cut = plain[: hi]
    sentence_end = max((m.end() for m in re.finditer(r"[.!?](?=\s|$)", cut)),
                       default=0)
    if sentence_end >= lo:
        return cut[:sentence_end].strip()
    space = cut[: hi - 1].rfind(" ")
    return (cut[: space] if space >= lo else cut[: hi - 1]).rstrip(" ,;:") + "…"


def render_markdown(cfg, text: str) -> str:
    MD.reset()
    out = MD.convert(text)
    bp = base_path(cfg)
    # root-relative internal links -> project base path
    out = re.sub(r'(href|src)="/(?!/)', rf'\1="{bp}', out)
    # external links: open safely
    out = re.sub(r'<a href="(https?://[^"]+)"',
                 r'<a href="\1" rel="noopener" target="_blank"', out)
    return out


def article_context(cfg, a: dict, arts: list[dict]) -> dict:
    hubs = cfg["content"]["hubs"]
    slug = a["slug"]
    hub = a.get("hub", "ai-models")
    published = _publish_dt(cfg, a)
    modified = _publish_dt(cfg, a, "updated") if a.get("updated") else published
    canonical = abs_url(cfg, f"articles/{slug}/")
    author = cfg["author"]
    author_url = abs_url(cfg, f"authors/{author['slug']}/")
    img_base = f"articles/{slug}/{slug}"
    image_abs = [abs_url(cfg, f"{img_base}-16x9.jpg"),
                 abs_url(cfg, f"{img_base}-4x3.jpg"),
                 abs_url(cfg, f"{img_base}-1x1.jpg")]

    blogposting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "headline": a["title"][:110],
        "description": a["description"],
        "image": image_abs,
        "datePublished": published.isoformat(),
        "dateModified": modified.isoformat(),
        "author": {"@type": "Person", "name": author["name"],
                   "url": author_url, "sameAs": author.get("sameAs", [])},
        "publisher": {"@type": "Organization", "name": cfg["site"]["name"],
                      "url": cfg["site"]["base_url"],
                      "logo": {"@type": "ImageObject",
                               "url": abs_url(cfg, "assets/logo-112x112.png"),
                               "width": 112, "height": 112}},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": cfg["site"]["base_url"]},
            {"@type": "ListItem", "position": 2, "name": hubs.get(hub, hub),
             "item": abs_url(cfg, f"topics/{hub}/")},
            {"@type": "ListItem", "position": 3, "name": a["title"]},
        ],
    }
    faq_jsonld = None
    if a.get("faq"):
        faq_jsonld = {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                           for f in a["faq"]]}

    related = [r for r in arts
               if r["slug"] != slug and r.get("hub") == hub][:3]
    if len(related) < 3:
        seen = {r["slug"] for r in related} | {slug}
        related += [r for r in arts if r["slug"] not in seen][:3 - len(related)]

    ymyl_map = {
        "finance": ("This article covers financial technology for general "
                    "information only — it is not investment, tax or financial "
                    "advice. Consult a qualified adviser before financial decisions."),
        "health": ("This article covers health technology for general information "
                   "only — it is not medical advice. Consult a qualified medical "
                   "professional for health decisions."),
        "security": ("This article discusses security topics for awareness and "
                     "defense only. Follow official vendor advisories for "
                     "remediation steps."),
    }

    return {
        "title": a["title"], "slug": slug, "hub": hub,
        "hub_name": hubs.get(hub, hub),
        "tags": a.get("tags", []),
        "description": a["description"],
        "page_title": f"{a['title']} — {cfg['site']['name']}",
        "meta_description": a["description"],
        "canonical": canonical, "og_type": "article",
        "og_title": a["title"],
        "og_image": image_abs[0], "og_image_alt": a.get("hero_alt", a["title"]),
        "published_iso": published.isoformat(),
        "modified_iso": modified.isoformat(),
        "published_human": _human(published),
        "updated_human": _human(modified) if a.get("updated") else None,
        "date_human": _human(published),
        "author_url": author_url,
        "hero_jpg": abs_url(cfg, f"{img_base}-16x9.jpg"),
        "hero_webp": abs_url(cfg, f"{img_base}-16x9.webp"),
        "hero_alt": a.get("hero_alt", a["title"]),
        "sources": a.get("sources", []),
        "faq": a.get("faq"),
        "ymyl_disclaimer": ymyl_map.get(a.get("ymyl")) if a.get("ymyl") else None,
        "blogposting_jsonld": Markup(json.dumps(blogposting, ensure_ascii=False)),
        "breadcrumb_jsonld": Markup(json.dumps(breadcrumb, ensure_ascii=False)),
        "faq_jsonld": Markup(json.dumps(faq_jsonld, ensure_ascii=False)) if faq_jsonld else None,
        "body_html": Markup(render_markdown(cfg, a["_body_md"])),
        "read_min": max(2, round(len(a["_body_md"].split()) / 220)),
        "related": [article_summary(cfg, r) for r in related],
    }


def article_summary(cfg, a: dict) -> dict:
    slug = a["slug"]
    published = _publish_dt(cfg, a)
    return {"slug": slug, "title": a["title"],
            "description": a.get("description", ""),
            "hub": a.get("hub"), "hub_name":
                cfg["content"]["hubs"].get(a.get("hub"), a.get("hub")),
            "date_human": _human(published),
            "hero_jpg": abs_url(cfg, f"articles/{slug}/{slug}-16x9.jpg"),
            "hero_webp": abs_url(cfg, f"articles/{slug}/{slug}-16x9.webp"),
            "hero_alt": a.get("hero_alt", a["title"])}


def _date_dt(cfg, date_str: str) -> datetime:
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return datetime(d.year, d.month, d.day,
                    cfg["publishing"]["publish_hour_ist"], 0, 0, tzinfo=IST)


def docket_context(cfg, d: dict) -> dict:
    """Render-ready context for one docket day (Today's Docket)."""
    hubs = cfg["content"]["hubs"]
    dk_cfg = cfg.get("docket") or {}
    items = []
    for it in d.get("items", []):
        url = str(it.get("url") or "")
        external = url.startswith("http")
        href = url if external else base_path(cfg) + url.lstrip("/")
        items.append({
            "hub": it.get("hub", "explainers"),
            "hub_name": hubs.get(it.get("hub"), it.get("hub", "")),
            "headline": str(it.get("headline") or ""),
            "dek": str(it.get("dek") or ""),
            "source": str(it.get("source") or ""),
            "lead": bool(it.get("lead")),
            "rank": it.get("rank"),
            "external": external,
            "href": href,
            "abs_url": url if external else abs_url(cfg, url),
        })
    date_human = _human(_date_dt(cfg, d["date"]))
    itemlist = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": f"Today's Docket — {date_human}",
        "numberOfItems": len(items),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "name": e["headline"], "url": e["abs_url"]}
            for i, e in enumerate(items)],
    }
    # NB key is "entries", not "items" — dict.items collides with the method
    # under Jinja attribute lookup
    return {"date": d["date"], "date_human": date_human, "entries": items,
            "pool": int(d.get("pool") or 12),
            "show_chips": bool(dk_cfg.get("show_chips")),
            "itemlist_jsonld": Markup(json.dumps(itemlist, ensure_ascii=False))}


def _analytics_snippet(cfg) -> Markup:
    a = cfg.get("analytics") or {}
    if a.get("provider") == "goatcounter" and a.get("goatcounter_code"):
        return Markup(
            f'<script data-goatcounter="https://{a["goatcounter_code"]}'
            f'.goatcounter.com/count" async src="https://gc.zgo.at/count.js">'
            f'</script>')
    if a.get("provider") == "ga4" and a.get("ga4_id"):
        gid = a["ga4_id"]
        return Markup(
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag()'
            f'{{dataLayer.push(arguments);}}gtag("js",new Date());'
            f'gtag("config","{gid}");</script>')
    return Markup("")


def _common(cfg, nav_hubs=None, **kw) -> dict:
    org = {"@context": "https://schema.org", "@type": "Organization",
           "name": cfg["site"]["name"], "url": cfg["site"]["base_url"],
           "logo": abs_url(cfg, "assets/logo-112x112.png"),
           "email": cfg["site"]["contact_email"],
           "sameAs": cfg["site"].get("social_profiles", [])}
    if nav_hubs is None:  # nav shows only hubs that actually have articles
        active = {a.get("hub") for a in all_articles()}
        nav_hubs = {h: n for h, n in cfg["content"]["hubs"].items()
                    if h in active}
    # brand wordmark: split CamelCase site name for the two-tone logo text
    _name = cfg["site"]["name"]
    if " " in _name:
        _head, _, _tail = _name.rpartition(" ")
        brand_a, brand_b = _head + " ", _tail
    else:
        m = re.match(r"^([A-Z][a-z0-9]+)([A-Z].*)$", _name)
        brand_a, brand_b = (m.group(1), m.group(2)) if m else (_name, "")
    dk_dir = ROOT / "data" / "docket"
    has_docket = (bool((cfg.get("docket") or {}).get("enabled", True))
                  and dk_dir.exists()
                  and any(re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem)
                          for p in dk_dir.glob("*.md")))
    d = {"site": cfg["site"], "author": cfg["author"],
         "hubs": cfg["content"]["hubs"],
         "nav_hubs": nav_hubs,
         "has_docket": has_docket,
         "brand_a": brand_a, "brand_b": brand_b,
         "base_path": base_path(cfg), "year": now_ist().year,
         "analytics_snippet": _analytics_snippet(cfg),
         "org_jsonld": Markup(json.dumps(org, ensure_ascii=False))}
    d.update(kw)
    return d


def _write(out: Path, content: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


# ---------------- static page bodies ----------------

def _about_md(cfg) -> str:
    return f"""
**{cfg['site']['name']}** is an independent publication covering
**{cfg['topic']['name']}** for readers in India and worldwide:
{cfg['topic']['description']}

We publish one carefully researched article every day. What we cover is chosen
from real, same-day search-demand and community-interest data — so we write
about what people are actually trying to understand right now, and we add the
context, comparisons and India-vs-global perspective that a search results
page can't.

## Who is behind this site

{cfg['site']['name']} is written and edited by **[{cfg['author']['name']}](/authors/{cfg['author']['slug']}/)**.
{cfg['author']['bio']}

## Contact

- Email: [{cfg['site']['contact_email']}](mailto:{cfg['site']['contact_email']})
- Corrections: email with subject "Correction" — see our [editorial policy](/editorial-policy/).

*Publisher information: {cfg['site']['name']} is a first-party publication;
all articles are produced under our own editorial process. We currently run
no advertising, sponsored content, or affiliate links.*
"""


def _policy_md(cfg) -> str:
    return f"""
This page explains **who** produces {cfg['site']['name']}, **how** every
article is made, and **why** — following Google's people-first
"Who, How, Why" disclosure framework.

## Who

Every article is published under the byline of
[{cfg['author']['name']}](/authors/{cfg['author']['slug']}/), who sets the
editorial standards, owns the site, and is accountable for its accuracy.

## How our articles are made (AI disclosure)

We are transparent about our process, which combines data, AI assistance and
defined quality gates:

1. **Topic selection is data-driven.** Each morning the engine collects
   same-day search-trend data (Google Trends for India and the US), news
   headlines, and tech-community momentum signals (e.g. Hacker News). Topics
   are scored for relevance, corroboration across independent sources, and
   India + global interest. We cover the strongest genuine trend — we do not
   manufacture urgency.
2. **Research and drafting use AI assistance.** Articles are researched and
   drafted with AI tools working from the day's verified sources. Every
   statistic must carry an inline citation to its source; fabricating numbers,
   quotes or "audience data" is prohibited by our gates.
3. **Automated editorial gates run before publish.** Each draft must pass
   checks for: source citations (minimum two primary/authoritative sources),
   originality against our own archive, headline-to-body accuracy (no
   clickbait), disclosure requirements, and sensitive-topic (finance/health/
   security) handling with disclaimers. Failing drafts are not published.
4. **Corrections.** If we get something wrong, email
   [{cfg['site']['contact_email']}](mailto:{cfg['site']['contact_email']})
   with subject "Correction". Substantive fixes are made in the article with a
   visible "Updated" date; we never bump dates without a real change.

## Why

We publish to help readers quickly understand what's moving in tech and AI and
what it means for them — not to game search rankings. One article per day,
each with original analysis, is a deliberate quality choice.

## What we don't do

- No sponsored posts, affiliate links or third-party contributed content.
- No health, financial or legal advice — sensitive topics carry disclaimers
  and rely on primary sources.
- No recycled or scraped content; no date-bumping without substantive updates.
"""


def _author_md(cfg) -> str:
    a = cfg["author"]
    links = "\n".join(f"- <{u}>" for u in a.get("sameAs", []))
    return f"""
{a['bio']}

All articles on {cfg['site']['name']} are published under
{a['name']}'s editorial standards — see the
[editorial policy](/editorial-policy/) for exactly how each piece is produced.

{('## Elsewhere' + chr(10) + links) if links else ''}

## Latest articles

See [all articles](/sitemap/).
"""


# ---------------- feeds / sitemap / robots ----------------

def _sitemap_xml(cfg, arts: list[dict]) -> str:
    urls = [(cfg["site"]["base_url"], now_ist().date().isoformat())]
    for a in arts:
        lastmod = str(a.get("updated") or a["date"])
        urls.append((abs_url(cfg, f"articles/{a['slug']}/"), lastmod))
    active = {a.get("hub") for a in arts}
    for hub in cfg["content"]["hubs"]:
        if hub in active:  # empty hubs stay out of the sitemap until filled
            urls.append((abs_url(cfg, f"topics/{hub}/"), None))
    # dated docket pages are the canonical daily-shorts units
    if (cfg.get("docket") or {}).get("enabled", True):
        for d in all_dockets():
            urls.append((abs_url(cfg, f"docket/{d['date']}/"), d["date"]))
    for p in ("about/", "editorial-policy/", "sitemap/",
              f"authors/{cfg['author']['slug']}/"):
        urls.append((abs_url(cfg, p), None))
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in urls:
        e = f"  <url><loc>{html.escape(loc)}</loc>"
        if lastmod:
            e += f"<lastmod>{lastmod}</lastmod>"
        parts.append(e + "</url>")
    parts.append("</urlset>")
    return "\n".join(parts)


def _feed_xml(cfg, arts: list[dict]) -> str:
    items = []
    for a in arts[:20]:
        pub = format_datetime(_publish_dt(cfg, a))
        link = abs_url(cfg, f"articles/{a['slug']}/")
        items.append(f"""  <item>
    <title>{html.escape(a['title'])}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <pubDate>{pub}</pubDate>
    <description><![CDATA[{a['description']}]]></description>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{html.escape(cfg['site']['name'])}</title>
  <link>{cfg['site']['base_url']}</link>
  <description>{html.escape(cfg['site']['tagline'])}</description>
  <language>{cfg['site']['language']}</language>
  <atom:link href="{abs_url(cfg, 'feed.xml')}" rel="self" type="application/rss+xml"/>
  <atom:link href="https://pubsubhubbub.appspot.com/" rel="hub"/>
{chr(10).join(items)}
</channel>
</rss>
"""


def _robots_txt(cfg) -> str:
    return f"""# {cfg['site']['name']} — maximum-reach crawler policy.
# Classic search + AI citation/search crawlers are all welcome.
# (Training-only crawlers are also allowed by choice; blocking them would not
#  affect AI-search citation visibility — see editorial policy.)

User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

Sitemap: {abs_url(cfg, 'sitemap.xml')}
"""


# ---------------- main build ----------------

def build_site() -> Path:
    cfg = load_config()
    env = _env()
    out = ROOT / cfg["publishing"]["output_dir"]
    arts = all_articles()
    author = cfg["author"]

    # ensure site assets
    images.generate_site_assets(cfg["site"]["name"], out / "assets")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    key = cfg["seo"]["indexnow_key"]
    if key and key != "REPLACED_AT_SETUP":
        (out / f"{key}.txt").write_text(key, encoding="utf-8")
    cname = cfg["site"].get("cname", "")
    if cname:
        (out / "CNAME").write_text(cname.strip() + "\n", encoding="utf-8")

    # articles
    tpl = env.get_template("article.html")
    for a in arts:
        slug = a["slug"]
        art_dir = out / "articles" / slug
        hero16 = art_dir / f"{slug}-16x9.jpg"
        if not hero16.exists():
            images.generate_hero(a["title"], slug, a.get("hub", "ai-models"),
                                 cfg["site"]["name"], art_dir)
        ctx = _common(cfg, current_hub=a.get("hub"),
                      **article_context(cfg, a, arts))
        _write(art_dir / "index.html", tpl.render(**ctx))

    summaries = [article_summary(cfg, a) for a in arts]

    # Today's Docket — daily shorts strip (/docket/<date>/ canonical,
    # /docket/ = latest alias, homepage strip). Separate content class:
    # never touches history.json, never counts as the daily article.
    dockets = all_dockets() if (cfg.get("docket") or {}).get("enabled", True) else []
    docket_strip = None
    if dockets:
        dk_tpl = env.get_template("docket.html")
        latest_date = dockets[0]["date"]
        for d in dockets:
            ctx_d = docket_context(cfg, d)
            dk_dir_out = out / "docket" / d["date"]
            card16 = dk_dir_out / f"docket-{d['date']}-16x9.jpg"
            if not card16.exists():
                images.generate_docket_card(d["date"], ctx_d["date_human"],
                                            cfg["site"]["name"], dk_dir_out)
            prev = [{"date": x["date"],
                     "date_human": _human(_date_dt(cfg, x["date"]))}
                    for x in dockets if x["date"] != d["date"]][:14]
            meta = _meta_desc(
                f"Today in tech, {ctx_d['date_human']}: "
                + " · ".join(e["headline"] for e in ctx_d["entries"][:4]))
            page_kw = dict(
                page_title=(f"Today's Docket, {ctx_d['date_human']} — "
                            f"{cfg['site']['name']}"),
                meta_description=meta,
                og_image=abs_url(cfg, f"docket/{d['date']}/docket-{d['date']}-16x9.jpg"),
                og_image_alt=f"Today's Docket — {ctx_d['date_human']}",
                current_hub="_docket", dk=ctx_d, prev=prev,
                canonical=abs_url(cfg, f"docket/{d['date']}/"))
            _write(dk_dir_out / "index.html",
                   dk_tpl.render(**_common(cfg, **page_kw)))
            if d["date"] == latest_date:
                # /docket/ serves the same content; canonical stays on the
                # dated page (GitHub Pages cannot 301)
                _write(out / "docket" / "index.html",
                       dk_tpl.render(**_common(cfg, **page_kw)))
                docket_strip = {
                    "date_human": ctx_d["date_human"],
                    "entries": [e for e in ctx_d["entries"]
                                if not e["lead"]][:4]}

    # home
    home_img = (summaries[0]["hero_jpg"] if summaries
                else abs_url(cfg, "assets/logo-512.png"))
    _write(out / "index.html", env.get_template("index.html").render(**_common(
        cfg,
        page_title=f"{cfg['site']['name']} — {cfg['site']['tagline']}",
        meta_description=(f"{cfg['site']['name']}: {cfg['topic']['description']} "
                          "One deeply researched, data-picked article every day."),
        canonical=cfg["site"]["base_url"], og_image=home_img,
        og_image_alt=cfg["site"]["name"],
        feature=summaries[0] if summaries else None,
        docket=docket_strip,
        articles=summaries[1:13] if len(summaries) > 1 else [])))

    # hubs
    for hslug, hname in cfg["content"]["hubs"].items():
        hub_arts = [s for s in summaries if s["hub"] == hslug]
        _write(out / "topics" / hslug / "index.html",
               env.get_template("list.html").render(**_common(
                   cfg, current_hub=hslug,
                   page_title=f"{hname} — {cfg['site']['name']}",
                   meta_description=f"All {cfg['site']['name']} coverage of {hname}: daily, data-picked articles for India and the world.",
                   canonical=abs_url(cfg, f"topics/{hslug}/"),
                   og_image=home_img, og_image_alt=hname,
                   heading=hname, intro=None, articles=hub_arts)))

    # static pages
    pages = [
        ("about/", "About", _about_md(cfg), None),
        ("editorial-policy/", "Editorial policy: who, how and why",
         _policy_md(cfg), None),
    ]
    profile_jsonld = {
        "@context": "https://schema.org", "@type": "ProfilePage",
        "dateModified": now_ist().date().isoformat(),
        "mainEntity": {"@type": "Person", "name": author["name"],
                       "description": author["bio"],
                       "url": abs_url(cfg, f"authors/{author['slug']}/"),
                       "sameAs": author.get("sameAs", [])}}
    for path, heading, body_md, extra in pages:
        _write(out / path / "index.html", env.get_template("page.html").render(
            **_common(cfg, page_title=f"{heading} — {cfg['site']['name']}",
                      meta_description=_meta_desc(body_md),
                      canonical=abs_url(cfg, path), og_image=home_img,
                      og_image_alt=heading, heading=heading,
                      body_html=Markup(render_markdown(cfg, body_md)),
                      extra_jsonld=extra)))
    _write(out / "authors" / author["slug"] / "index.html",
           env.get_template("page.html").render(**_common(
               cfg, page_title=f"{author['name']} — {cfg['site']['name']}",
               meta_description=_meta_desc(author["bio"]),
               canonical=abs_url(cfg, f"authors/{author['slug']}/"),
               og_image=home_img, og_image_alt=author["name"],
               heading=author["name"],
               body_html=Markup(render_markdown(cfg, _author_md(cfg))),
               extra_jsonld=Markup(json.dumps(profile_jsonld, ensure_ascii=False)))))

    # HTML sitemap (orphan insurance)
    _write(out / "sitemap" / "index.html", env.get_template("list.html").render(
        **_common(cfg, page_title=f"All articles — {cfg['site']['name']}",
                  meta_description=f"Complete archive of {cfg['site']['name']} articles.",
                  canonical=abs_url(cfg, "sitemap/"), og_image=home_img,
                  og_image_alt="All articles", heading="All articles",
                  intro="Every article we've published, newest first.",
                  articles=summaries)))

    # 404
    _write(out / "404.html", env.get_template("page.html").render(**_common(
        cfg, page_title=f"Page not found — {cfg['site']['name']}",
        meta_description="Page not found.", canonical=cfg["site"]["base_url"],
        og_image=home_img, og_image_alt=cfg["site"]["name"],
        heading="That page doesn't exist",
        body_html=Markup(
            f'<p>The link may be old or mistyped. Try the '
            f'<a href="{base_path(cfg)}">homepage</a> or the '
            f'<a href="{base_path(cfg)}sitemap/">full article list</a>.</p>'))))

    # machine files
    _write(out / "sitemap.xml", _sitemap_xml(cfg, arts))
    _write(out / "feed.xml", _feed_xml(cfg, arts))
    _write(out / "robots.txt", _robots_txt(cfg))
    print(f"built {len(arts)} article(s) -> {out}")
    return out


if __name__ == "__main__":
    build_site()

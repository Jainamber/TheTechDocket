"""Trend/keyword ingestion.

Designed to run on an unrestricted-egress host (the GitHub Actions runner).
Every source degrades gracefully: failures are recorded in `sources_status`
and never abort the run. Output: data/inbox/<date>.json

In restricted environments (e.g. the Cowork cloud container) most sources
will fail — that is expected; the daily Claude session then gathers
equivalent data via its own WebSearch/WebFetch tools and writes the same
inbox schema. See DAILY_RUN.md.
"""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

import requests

from .util import ROOT, load_config, today_str

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 thetechdocket-engine/1.0")
UA_POLITE = "thetechdocket-engine/1.0 (trend research; contact: jainamber88@gmail.com)"
TIMEOUT = 20
TRENDS_NS = {"ht": "https://trends.google.com/trending/rss"}


def _get(url: str, ua: str = UA) -> requests.Response:
    r = requests.get(url, headers={"User-Agent": ua}, timeout=TIMEOUT)
    r.raise_for_status()
    return r


# ---------------- sources ----------------

def google_trends_rss(geo: str) -> list[dict]:
    r = _get(f"https://trends.google.com/trending/rss?geo={geo}")
    root = ET.fromstring(r.content)
    items = []
    for item in root.findall(".//item"):
        news = []
        for ni in item.findall("ht:news_item", TRENDS_NS):
            news.append({
                "headline": ni.findtext("ht:news_item_title", namespaces=TRENDS_NS),
                "source": ni.findtext("ht:news_item_source", namespaces=TRENDS_NS),
                "url": ni.findtext("ht:news_item_url", namespaces=TRENDS_NS),
            })
        items.append({
            "title": (item.findtext("title") or "").strip(),
            "approx_traffic": item.findtext("ht:approx_traffic", namespaces=TRENDS_NS),
            "pub_date": item.findtext("pubDate"),
            "news": news,
        })
    return items


def google_news_rss(query: str, params: str) -> list[dict]:
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&{params}"
    r = _get(url)
    root = ET.fromstring(r.content)
    return [{
        "title": i.findtext("title"),
        "source": i.findtext("source"),
        "pub_date": i.findtext("pubDate"),
    } for i in root.findall(".//item")[:25]]


def autocomplete(seed: str, hl: str = "en") -> list[str]:
    url = ("https://suggestqueries.google.com/complete/search"
           f"?client=firefox&hl={hl}&q={requests.utils.quote(seed)}")
    r = _get(url)
    data = r.json()
    return list(data[1]) if isinstance(data, list) and len(data) > 1 else []


def hn_stories() -> list[dict]:
    out = []
    for params in ("tags=front_page",
                   "query=AI&tags=story&numericFilters=points%3E40"):
        r = _get(f"https://hn.algolia.com/api/v1/search_by_date?{params}"
                 if "query" in params else
                 f"https://hn.algolia.com/api/v1/search?{params}")
        for h in r.json().get("hits", [])[:30]:
            out.append({
                "title": h.get("title"),
                "url": h.get("url"),
                "points": h.get("points"),
                "comments": h.get("num_comments"),
                "created_at": h.get("created_at"),
            })
    return out


def wikipedia_top(project: str = "en.wikipedia") -> list[dict]:
    d = date.today() - timedelta(days=2)
    url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
           f"{project}/all-access/{d:%Y}/{d:%m}/{d:%d}")
    r = _get(url, ua=UA_POLITE)
    arts = r.json()["items"][0]["articles"][:50]
    return [{"article": a["article"], "views": a["views"], "rank": a["rank"]}
            for a in arts]


OUTLET_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
}


def outlet_headlines() -> list[dict]:
    out = []
    for name, feed in OUTLET_FEEDS.items():
        try:
            r = _get(feed)
            root = ET.fromstring(r.content)
            # RSS 2.0 <item> or Atom <entry>
            nodes = root.findall(".//item") or root.findall(
                ".//{http://www.w3.org/2005/Atom}entry")
            for n in nodes[:15]:
                title = (n.findtext("title") or
                         n.findtext("{http://www.w3.org/2005/Atom}title") or "")
                out.append({"outlet": name, "title": title.strip()})
        except Exception as e:  # noqa: BLE001
            out.append({"outlet": name, "error": str(e)[:120]})
    return out


# ---------------- assembly ----------------

def fetch_all() -> dict:
    cfg = load_config()
    day = today_str()
    inbox: dict = {"date": day, "generated_by": "engine.fetchers",
                   "sources_status": {}, "markets": {}}

    def attempt(key: str, fn, *a, **kw):
        try:
            data = fn(*a, **kw)
            inbox["sources_status"][key] = "ok"
            return data
        except Exception as e:  # noqa: BLE001
            inbox["sources_status"][key] = f"failed: {type(e).__name__}: {str(e)[:140]}"
            return None

    seeds = cfg["news_seed_queries"]
    rotation = date.today().timetuple().tm_yday % len(seeds)
    day_queries = [seeds[rotation], seeds[(rotation + 1) % len(seeds)]]

    for m in cfg["markets"]:
        geo = m["geo"]
        block = {"label": m["label"]}
        block["trends_rss"] = attempt(f"trends_rss_{geo}", google_trends_rss, geo)
        block["news"] = {}
        for q in day_queries:
            block["news"][q] = attempt(
                f"news_{geo}_{q[:12]}", google_news_rss, q, m["news_params"])
        hl = "en-IN" if geo == "IN" else "en"
        block["autocomplete"] = {}
        for seed in ["ai", "chatgpt", "new phone", cfg["topic"]["name"].lower()]:
            block["autocomplete"][seed] = attempt(
                f"suggest_{geo}_{seed[:10]}", autocomplete, seed, hl)
        inbox["markets"][geo] = block

    inbox["hacker_news"] = attempt("hn", hn_stories)
    inbox["wikipedia_top"] = attempt("wiki_en", wikipedia_top)
    inbox["outlet_headlines"] = attempt("outlets", outlet_headlines)
    return inbox


def write_inbox(inbox: dict) -> Path:
    out = ROOT / "data" / "inbox" / f"{inbox['date']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inbox, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    box = fetch_all()
    path = write_inbox(box)
    ok = sum(1 for v in box["sources_status"].values() if v == "ok")
    total = len(box["sources_status"])
    print(f"inbox written: {path} ({ok}/{total} sources ok)")
    if ok == 0:
        print("WARNING: no sources reachable — daily session must gather "
              "data via WebSearch/WebFetch (see DAILY_RUN.md)")
        sys.exit(0)

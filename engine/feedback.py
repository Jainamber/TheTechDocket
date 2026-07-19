"""Learn & adapt: turn real traffic data into scoring boosts + brief guidance.

Inputs (both optional, both graceful):
  1. GoatCounter API  — needs env GOATCOUNTER_TOKEN + config analytics.goatcounter_code
                        (works from the GitHub Actions runner; the Cowork
                        container's egress usually blocks it — that's fine).
  2. Google Search Console CSV exports — drop the "Pages" and/or "Queries"
     CSVs from GSC's Performance report into data/search-console/.

Output: data/insights.json
  - page_stats:      per-slug clicks/impressions/visits
  - hub_performance: aggregated per hub
  - winning_queries: top real search queries hitting the site
  - keyword_boost:   term -> weight, consumed by engine/scoring.py
"""
from __future__ import annotations

import csv
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from .util import ROOT, load_config, load_history, now_ist, tokenize

INSIGHTS = ROOT / "data" / "insights.json"
GSC_DIR = ROOT / "data" / "search-console"

STOP = {"the", "a", "an", "of", "to", "in", "on", "for", "and", "is", "are",
        "what", "how", "why", "vs", "with", "your", "my", "you", "it", "ai"}


def _slug_from_path(path: str) -> str | None:
    m = re.search(r"/articles/([a-z0-9-]+)/?", path or "")
    return m.group(1) if m else None


def fetch_goatcounter(cfg) -> dict[str, int]:
    """Return {slug: visit_count} from the GoatCounter API, or {} on any failure."""
    code = cfg["analytics"].get("goatcounter_code")
    token = os.environ.get("GOATCOUNTER_TOKEN")
    if not (code and token and cfg["analytics"].get("provider") == "goatcounter"):
        return {}
    try:
        import requests
        r = requests.get(
            f"https://{code}.goatcounter.com/api/v0/stats/hits",
            headers={"Authorization": f"Bearer {token}"},
            params={"limit": 100}, timeout=20)
        r.raise_for_status()
        out: dict[str, int] = {}
        for hit in r.json().get("hits", []):
            slug = _slug_from_path(hit.get("path", ""))
            if slug:
                out[slug] = out.get(slug, 0) + int(hit.get("count", 0))
        return out
    except Exception as e:  # noqa: BLE001
        print(f"goatcounter: skipped ({type(e).__name__}: {str(e)[:120]})")
        return {}


def _read_gsc_csvs() -> tuple[dict, list]:
    """Parse GSC 'Pages' and 'Queries' CSV exports (flexible headers)."""
    pages: dict[str, dict] = {}
    queries: list[dict] = []
    if not GSC_DIR.exists():
        return pages, queries
    for f in GSC_DIR.glob("*.csv"):
        try:
            with open(f, encoding="utf-8-sig", newline="") as fh:
                for row in csv.DictReader(fh):
                    low = {k.strip().lower(): (v or "").strip()
                           for k, v in row.items() if k}
                    clicks = int(float(low.get("clicks", 0) or 0))
                    imps = int(float(low.get("impressions", 0) or 0))
                    page = low.get("top pages") or low.get("page") or low.get("url")
                    query = low.get("top queries") or low.get("query")
                    if page:
                        slug = _slug_from_path(page)
                        if slug:
                            s = pages.setdefault(slug, {"clicks": 0, "impressions": 0})
                            s["clicks"] += clicks
                            s["impressions"] += imps
                    elif query:
                        queries.append({"query": query, "clicks": clicks,
                                        "impressions": imps})
        except Exception as e:  # noqa: BLE001
            print(f"gsc csv {f.name}: skipped ({e})")
    return pages, queries


def build_insights() -> dict:
    cfg = load_config()
    hist = {p["slug"]: p for p in load_history()["published"]}
    visits = fetch_goatcounter(cfg)
    pages, queries = _read_gsc_csvs()

    page_stats: dict[str, dict] = defaultdict(
        lambda: {"clicks": 0, "impressions": 0, "visits": 0})
    for slug, v in visits.items():
        page_stats[slug]["visits"] = v
    for slug, s in pages.items():
        page_stats[slug]["clicks"] += s["clicks"]
        page_stats[slug]["impressions"] += s["impressions"]

    # hub aggregation via publish history
    hub_perf: dict[str, int] = defaultdict(int)
    for slug, s in page_stats.items():
        hub = (hist.get(slug) or {}).get("hub")
        if hub:
            hub_perf[hub] += s["clicks"] * 3 + s["visits"] + s["impressions"] // 20

    # winning queries -> keyword boost weights
    min_imp = cfg["feedback"]["min_impressions"]
    cap = cfg["feedback"]["keyword_boost_cap"]
    strong = [q for q in queries
              if q["impressions"] >= min_imp or q["clicks"] > 0]
    strong.sort(key=lambda q: (q["clicks"], q["impressions"]), reverse=True)
    kw_weight: dict[str, float] = defaultdict(float)
    for rank, q in enumerate(strong[:40]):
        for tok in tokenize(q["query"]):
            if tok not in STOP and len(tok) > 2:
                kw_weight[tok] += max(0.01, 0.05 - 0.001 * rank)
    keyword_boost = {t: round(min(w, cap), 4)
                     for t, w in sorted(kw_weight.items(),
                                        key=lambda x: -x[1])[:30]}

    insights = {
        "generated_at": now_ist().isoformat(),
        "page_stats": dict(page_stats),
        "hub_performance": dict(hub_perf),
        "winning_queries": strong[:20],
        "keyword_boost": keyword_boost,
        "notes": "keyword_boost feeds engine/scoring.py; winning_queries and "
                 "top pages feed the daily brief's performance section.",
    }
    INSIGHTS.parent.mkdir(parents=True, exist_ok=True)
    INSIGHTS.write_text(json.dumps(insights, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"insights: {INSIGHTS} "
          f"(pages={len(page_stats)}, queries={len(strong)}, "
          f"boost_terms={len(keyword_boost)})")
    return insights


def load_insights() -> dict:
    if INSIGHTS.exists():
        try:
            return json.loads(INSIGHTS.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}

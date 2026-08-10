#!/usr/bin/env python3
"""Assemble data/inbox/2026-08-10.json from session part files.

Environment note (2026-08-10): this scheduled session's egress proxy blocks
all direct WebFetch (trends.google.com, hn.algolia.com, outlet feeds), so
the inbox is WebSearch-derived. Part files:
  - session-trends-2026-08-10.json     (trends RSS — blocked, statuses kept)
  - session-hn-outlets-2026-08-10.json (HN + outlet feeds — blocked, statuses kept)
  - session-news-2026-08-10.json       (WebSearch news sweep — primary signal)
  - session-cn-radar-2026-08-10.json   (Monday CN Trend Radar)
News stories are mapped into markets.{IN,US}.news query buckets so
engine.scoring.extract_candidates picks them up (title/source keys).
"""
import json
from pathlib import Path

P = Path(__file__).parent
OUT = P.parent / "2026-08-10.json"

def load(name):
    f = P / name
    if not f.exists():
        return {}
    return json.loads(f.read_text(encoding="utf-8"))

trends = load("session-trends-2026-08-10.json")
hn = load("session-hn-outlets-2026-08-10.json")
news = load("session-news-2026-08-10.json")
cn = load("session-cn-radar-2026-08-10.json")

IN_TERMS = ("india", "indian", "micron sanand", "jio", "isro", "upi", "modi",
            "bengaluru", "delhi", "mumbai", "hyderabad", "vizag", "tcs",
            "infosys", "flipkart", "airtel", "rupee", "gujarat")

in_bucket, us_bucket = [], []
for s in news.get("stories", []):
    item = {"title": s.get("headline", ""), "source": s.get("source", ""),
            "pub_date": s.get("date", ""), "url": s.get("url", ""),
            "note": s.get("note", "")}
    text = (item["title"] + " " + item["note"]).lower()
    (in_bucket if any(t in text for t in IN_TERMS) else us_bucket).append(item)

sources_status = {}
for part in (trends, hn, news, cn):
    sources_status.update(part.get("sources_status", {}))

inbox = {
    "date": "2026-08-10",
    "generated_by": "daily-session-websearch",
    "sources_status": sources_status,
    "markets": {
        "IN": {"label": "India",
               "trends_rss": trends.get("IN", []),
               "news": {"websearch tech india": in_bucket},
               "autocomplete": {}},
        "US": {"label": "Global (US proxy)",
               "trends_rss": trends.get("US", []),
               "news": {"websearch tech global": us_bucket},
               "autocomplete": {}},
    },
    "hacker_news": hn.get("hacker_news", []),
    "outlet_headlines": hn.get("outlet_headlines", []),
    "wikipedia_top": [],
    "cn_incubator": cn.get("cn_incubator", []),
}

OUT.write_text(json.dumps(inbox, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {OUT}: IN news {len(in_bucket)}, US news {len(us_bucket)}, "
      f"HN {len(inbox['hacker_news'])}, outlets {len(inbox['outlet_headlines'])}, "
      f"cn {len(inbox['cn_incubator'])}")

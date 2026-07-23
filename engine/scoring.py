"""Candidate extraction + scoring from the daily inbox.

Turns raw trend signals into a ranked list of article candidates,
filtered to the configured broad topic, deduplicated against recent
publishes, and blended across markets (India + Global).
"""
from __future__ import annotations

import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

from .util import ROOT, jaccard, load_config, load_history, today_str, tokenize


def _match_score(text: str, terms: list[str]) -> float:
    t = " " + text.lower() + " "
    hits = [term for term in terms if term in t]
    if not hits:
        return 0.0
    # longer/more matched terms => stronger fit, saturating
    return min(1.0, 0.4 + 0.2 * len(hits) + 0.02 * max(len(h) for h in hits))


def _traffic_to_num(s: str | None) -> float:
    if not s:
        return 0.0
    m = re.search(r"([\d,.]+)\s*([KMB]?)", str(s).replace("+", ""), re.I)
    if not m:
        return 0.0
    n = float(m.group(1).replace(",", ""))
    return n * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2).upper()]


def _intent_bonus(title: str) -> float:
    t = title.lower()
    if re.search(r"\b(how|why|what|which|vs|versus|best|explained|guide)\b", t):
        return 1.0
    return 0.0


def _hours_ago(iso: str | None) -> float:
    if not iso:
        return 24.0
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return max(0.0, (datetime.now(timezone.utc) - dt).total_seconds() / 3600)
    except ValueError:
        return 24.0


def extract_candidates(inbox: dict, cfg: dict) -> list[dict]:
    """Flatten every signal into candidate dicts with raw evidence attached."""
    cands: dict[str, dict] = {}

    def add(title: str, source: str, geo: str | None, momentum: float,
            evidence: dict):
        if not title or len(title) < 4:
            return
        key = " ".join(tokenize(title)[:6])
        if not key:
            return
        c = cands.setdefault(key, {
            "title": title.strip(), "sources": [], "geos": set(),
            "momentum_raw": 0.0, "evidence": []})
        c["sources"].append(source)
        if geo:
            c["geos"].add(geo)
        c["momentum_raw"] = max(c["momentum_raw"], momentum)
        c["evidence"].append({"source": source, **evidence})

    for geo, block in (inbox.get("markets") or {}).items():
        for it in (block.get("trends_rss") or []):
            traffic = _traffic_to_num(it.get("approx_traffic"))
            add(it["title"], f"gtrends:{geo}", geo,
                min(1.0, math.log10(traffic + 1) / 6),
                {"traffic": it.get("approx_traffic"),
                 "news": (it.get("news") or [])[:3]})
        for q, items in (block.get("news") or {}).items():
            for n in (items or [])[:10]:
                add(n.get("title") or "", f"gnews:{geo}", geo, 0.25,
                    {"query": q, "outlet": n.get("source")})

    for h in (inbox.get("hacker_news") or []):
        pts = h.get("points") or 0
        velocity = pts / max(2.0, _hours_ago(h.get("created_at")))
        add(h.get("title") or "", "hn", None,
            min(1.0, math.log10(pts + 1) / 3 + min(0.3, velocity / 100)),
            {"points": pts, "comments": h.get("comments"), "url": h.get("url")})

    for o in (inbox.get("outlet_headlines") or []):
        if o.get("title"):
            add(o["title"], f"outlet:{o.get('outlet')}", None, 0.2,
                {"outlet": o.get("outlet")})

    for w in (inbox.get("wikipedia_top") or [])[:30]:
        name = (w.get("article") or "").replace("_", " ")
        add(name, "wikipedia", None,
            min(0.6, math.log10((w.get("views") or 1)) / 8), {"views": w.get("views")})

    # CN Trend Radar (proposal 2026-07-23): weekly RED/Bilibili early signals
    # land in the inbox under `cn_incubator`. HARD rule: an uncorroborated CN
    # signal is a hypothesis, never a candidate — RED's algorithm rewards
    # legible sameness and can manufacture trend-shaped noise, so a second,
    # non-CN-platform source URL is the price of entry. The corroborating
    # source is added as its own evidence line (it is a real, verified second
    # source — that's what corroboration_url MEANS), which is what feeds the
    # scorer's corroboration term.
    for c in (inbox.get("cn_incubator") or []):
        title = str(c.get("title") or "")
        corro = str(c.get("corroboration_url") or "").strip()
        if not corro:
            print(f"CN-RADAR blocked (no corroboration_url): {title[:70]}")
            continue
        platform = str(c.get("platform") or "cn").strip().lower()
        add(title, f"cn:{platform}", None, 0.35,
            {"platform": platform, "url": str(c.get("url") or ""),
             "provenance": str(c.get("provenance") or ""),
             "origin": "cn-incubator"})
        add(title, "corroboration", None, 0.2,
            {"url": corro, "origin": "cn-incubator"})

    return list(cands.values())


def score_candidates(cands: list[dict], cfg: dict) -> list[dict]:
    from .feedback import load_insights
    allow = cfg["topic"]["allow_keywords"]
    deny = cfg["topic"]["deny_keywords"]
    W = cfg["scoring"]["weights"]
    kw_boost = load_insights().get("keyword_boost", {})
    hist = load_history()
    recent = [p for p in hist["published"]
              if (datetime.now(timezone.utc)
                  - datetime.fromisoformat(p["published_at"])).days
              <= cfg["scoring"]["dedup_window_days"]] if hist["published"] else []
    recent_tokens = [set(tokenize(p["title"] + " " + p.get("keyword", "")))
                     for p in recent]

    scored = []
    for c in cands:
        text = c["title"] + " " + json.dumps(c["evidence"])[:400]
        if any(d in (" " + text.lower() + " ") for d in deny):
            continue
        fit = _match_score(text, allow)
        if fit == 0.0:
            continue
        distinct = {s.split(":")[0] for s in c["sources"]}
        corroboration = min(1.0, (len(distinct) - 1) / 2)
        # markets[].weight was documented as controlling the IN/US blend but
        # never read (finding F4, 07-16). geo_spread is now coverage-weighted:
        # both markets → 1.0 and no market → 0.4 (unchanged); a single market
        # → 0.4 + 0.6·weight (0.7 at 0.5/0.5; the Phase-2 0.45/0.55 shift now
        # actually favours US-only over IN-only candidates).
        mw = {m["geo"]: float(m.get("weight", 0.0))
              for m in cfg.get("markets", [])}
        cov = sum(mw.get(g, 0.0) for g in set(c["geos"]))
        geo_spread = 0.4 + 0.6 * min(1.0, cov)
        score = (W["momentum"] * c["momentum_raw"]
                 + W["corroboration"] * corroboration
                 + W["topic_fit"] * fit
                 + W["freshness"] * 1.0          # inbox is same-day by contract
                 + W["geo_spread"] * geo_spread
                 + W["intent"] * _intent_bonus(c["title"]))
        # dedup penalty vs recently published
        toks = set(tokenize(c["title"]))
        sim = max((jaccard(toks, rt) for rt in recent_tokens), default=0.0)
        if sim >= cfg["scoring"]["dedup_max_similarity"]:
            continue
        score *= (1.0 - 0.5 * sim)
        # learn & adapt: boost candidates matching queries that already
        # earn this site impressions/clicks (data/insights.json)
        if kw_boost:
            bonus = min(cfg["feedback"]["keyword_boost_cap"],
                        sum(w for t, w in kw_boost.items() if t in toks))
            score *= (1.0 + bonus)
        c2 = dict(c)
        c2["geos"] = sorted(c2["geos"])
        c2["score"] = round(score, 4)
        c2["topic_fit"] = round(fit, 3)
        c2["corroboration"] = round(corroboration, 3)
        scored.append(c2)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def select(inbox_path: Path | None = None) -> dict:
    cfg = load_config()
    day = today_str()
    inbox_path = inbox_path or ROOT / "data" / "inbox" / f"{day}.json"
    if not inbox_path.exists():
        raise SystemExit(
            f"No inbox at {inbox_path}. Run `python -m engine.run fetch` on an "
            "unrestricted host, or have the daily session write the inbox from "
            "WebSearch/WebFetch data (see DAILY_RUN.md).")
    inbox = json.loads(inbox_path.read_text(encoding="utf-8"))
    ranked = score_candidates(extract_candidates(inbox, cfg), cfg)
    # visibility only — blocked CN signals are recorded, never scored
    cn_blocked = [str(c.get("title") or "")[:90]
                  for c in (inbox.get("cn_incubator") or [])
                  if not str(c.get("corroboration_url") or "").strip()]
    result = {
        "date": day,
        "candidates": ranked[:12],
        "pick": ranked[0] if ranked else None,
        "use_evergreen": (not ranked
                          or ranked[0]["score"] < cfg["scoring"]["min_publish_score"]),
    }
    if cn_blocked:
        result["cn_blocked"] = cn_blocked
    out = ROOT / "data" / "briefs" / f"{day}-candidates.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result

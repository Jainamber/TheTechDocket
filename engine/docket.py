"""Today's Docket — the daily shorts strip (data, gates, publish).

The docket is a separate content class from articles: 4-8 tiny, sourced,
editor-written entries per day rendered at /docket/ (latest) and
/docket/<date>/ (canonical archive). It harvests the day's scored-but-
unwritten candidates (data/briefs/<date>-candidates.json) — zero new data
collection, one new writing + rendering step.

Hard rules (mirroring the article spine):
  * The docket NEVER touches data/history.json and never counts as the
    daily article (the 1-article/day discipline is untouched).
  * A docket failure never blocks or reverts an article publish — publish
    the article first, docket after, in the same session.
  * Entries are observations with sources — no causal claims, no stats
    absent from the linked source, no copied headlines, no clickbait.

Gate namespace: D01-D09 (report: data/gate-reports/<date>-docket.json).
Momentum chips (config docket.show_chips) stay OFF until the corroboration-
accuracy fix from the Signal Box batch lands (V2.1 recheck §4.1).

Usage:
  python -m engine.run docket-draft            # pre-draft from candidates
  python -m engine.run docket [--date D]       # run D-gates on built pages
  python -m engine.run docket-publish [--date D] [--no-push]
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

from .gates import CLICKBAIT_RE, HARD, SOFT
from .util import ROOT, all_articles, load_config, now_ist, today_str

DOCKET_DIR = ROOT / "data" / "docket"
DATE_NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------- data ----------------

def parse_docket(path: Path) -> dict:
    """A docket file is a YAML document, optionally ----fenced."""
    raw = path.read_text(encoding="utf-8-sig").strip()
    m = re.match(r"^---\s*\n(.*?)\n---\s*$", raw, re.DOTALL)
    d = yaml.safe_load(m.group(1) if m else raw) or {}
    d["date"] = str(d.get("date") or path.stem)
    d["items"] = d.get("items") or []
    d["_path"] = str(path)
    return d


def all_dockets() -> list[dict]:
    """All docket data files, newest first. Draft files are ignored."""
    out = []
    if not DOCKET_DIR.exists():
        return out
    for p in sorted(DOCKET_DIR.glob("*.md")):
        if not DATE_NAME_RE.match(p.stem):
            continue  # e.g. 2026-07-19-draft.md
        try:
            out.append(parse_docket(p))
        except Exception as e:  # noqa: BLE001 — one bad file must not kill the build
            print(f"WARN: skipping docket {p}: {e}")
    out.sort(key=lambda d: d["date"], reverse=True)
    return out


def suggest_tag(title: str, cfg: dict) -> str:
    """First watchlist key whose match-terms hit the title (suggestion only —
    the daily session confirms or clears every tag)."""
    t = (title or "").lower()
    for key, spec in ((cfg.get("docket") or {}).get("watchlist") or {}).items():
        terms = [x.strip().lower() for x in str(spec.get("match", "")).split(",")]
        if any(term and term in t for term in terms):
            return key
    return ""


def write_draft(date_str: str | None = None) -> Path:
    """Pre-draft today's docket from the day's scored candidates.

    The daily session edits this into data/docket/<date>.md: pick 4-8,
    paraphrase headlines, write a <=60-word item, keep the source URL.
    """
    day = date_str or today_str()
    cfg = load_config()
    cand_path = ROOT / "data" / "briefs" / f"{day}-candidates.json"
    if not cand_path.exists():
        raise SystemExit(f"no candidates file for {day} — run `select` first")
    sel = json.loads(cand_path.read_text(encoding="utf-8"))
    cands = sel.get("candidates") or []
    wl_keys = "|".join(((cfg.get("docket") or {}).get("watchlist") or {}))
    lines = ["---", f"date: {day}", f"pool: {len(cands)}",
             "items:",
             "  # Item 1 must be today's article (lead: true). Then pick 3-7 of",
             "  # the candidates below: paraphrase the headline (never copy),",
             "  # write a 1-2 sentence dek (<=60 words total, no clickbait,",
             "  # no claims absent from the source), keep the source URL.",
             f"  # tag: ONE watchlist key ({wl_keys}) — only where it honestly",
             "  #   applies; suggestions below are keyword guesses, confirm or",
             "  #   clear them. Target >=half tagged; 1-3 wildcards stay open.",
             "  # pick: true on up to 2 standout entries (\"Short of the day\"),",
             "  #   placed immediately after the lead.",
             "  - hub: <hub-of-today's-article>",
             "    lead: true",
             "    rank: 1",
             "    tag: \"\"",
             "    headline: \"<paraphrase of today's article>\"",
             "    dek: \"<why it matters, 1-2 sentences>\"",
             "    url: /articles/<today's-slug>/",
             "    source: \"The Tech Docket\""]
    for i, c in enumerate(cands[1:], start=2):
        url = next((e.get("url") for e in c.get("evidence", [])
                    if e.get("url")), "")
        host = urlparse(url).netloc.replace("www.", "") if url else "?"
        tag = suggest_tag(c.get("title", ""), cfg)
        lines += [f"  # --- candidate rank {i}: {c.get('title', '')[:90]}",
                  "  # - hub: <ai-models|ai-tools|big-tech|hardware|policy|explainers>",
                  f"  #   rank: {i}",
                  f"  #   tag: \"{tag}\"" + ("   # suggested" if tag else ""),
                  "  #   headline: \"\"",
                  "  #   dek: \"\"",
                  f"  #   url: {url}",
                  f"  #   source: \"{host}\""]
    lines += ["---", ""]
    DOCKET_DIR.mkdir(parents=True, exist_ok=True)
    out = DOCKET_DIR / f"{day}-draft.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ---------------- gates (D-namespace) ----------------

class DocketGateRunner:
    """D01-D09. Same report shape and location as the article gate suite."""

    def __init__(self, date_str: str | None = None):
        self.cfg = load_config()
        self.dk_cfg = self.cfg.get("docket") or {}
        self.date = date_str or today_str()
        path = DOCKET_DIR / f"{self.date}.md"
        if not path.exists():
            raise SystemExit(f"no docket data file: {path}")
        self.data = parse_docket(path)
        out = ROOT / self.cfg["publishing"]["output_dir"]
        self.out_dir = out
        self.dated_path = out / "docket" / self.date / "index.html"
        self.latest_path = out / "docket" / "index.html"
        self.results: list[dict] = []

    def check(self, gid: str, level: str, ok: bool, detail: str = ""):
        self.results.append({"gate": gid, "level": level,
                             "ok": bool(ok), "detail": detail[:300]})

    def run(self) -> dict:
        from bs4 import BeautifulSoup
        items = self.data["items"]
        own = urlparse(self.cfg["site"]["base_url"]).netloc

        # D01 both pages built, carrying this docket's date
        built = self.dated_path.exists() and self.latest_path.exists()
        dated_soup = latest_soup = None
        if built:
            dated_soup = BeautifulSoup(
                self.dated_path.read_text(encoding="utf-8"), "html.parser")
            latest_soup = BeautifulSoup(
                self.latest_path.read_text(encoding="utf-8"), "html.parser")
        dated_ol = dated_soup.select_one("ol.docketlist") if dated_soup else None
        self.check("D01-docket-built", HARD,
                   built and dated_ol is not None
                   and dated_ol.get("data-date") == self.date,
                   "docs/docket/<date>/ + docs/docket/ must exist and carry "
                   f"data-date={self.date} — run `build` first")

        # D02 item count
        lo = int(self.dk_cfg.get("min_items", 4))
        hi = int(self.dk_cfg.get("max_items", 8))
        self.check("D02-item-count", HARD, lo <= len(items) <= hi,
                   f"{len(items)} items (need {lo}-{hi})")

        # D03 every item sourced; non-lead items must link an external source
        bad = []
        for i, it in enumerate(items, 1):
            url = str(it.get("url") or "")
            if not url or not str(it.get("source") or "").strip():
                bad.append(f"item {i}: missing url/source")
            elif not it.get("lead"):
                host = urlparse(url).netloc
                if not url.startswith("http") or not host or own in host:
                    bad.append(f"item {i}: non-lead url must be external ({url[:50]})")
        self.check("D03-item-sources", HARD, not bad, "; ".join(bad[:4]))

        # D04 no clickbait headlines
        bad = [f"item {i}" for i, it in enumerate(items, 1)
               if CLICKBAIT_RE.search(str(it.get("headline") or ""))
               or str(it.get("headline") or "").count("!") > 1
               or re.search(r"\b[A-Z]{5,}\b", str(it.get("headline") or ""))]
        self.check("D04-no-clickbait", HARD, not bad,
                   "clickbait/caps headlines: " + ", ".join(bad[:4]))

        # D05 tiny format is enforced, not aspirational. headline + dek is the
        # core "short"; the optional why/counterpoint lines are each separately
        # capped so the Brief layer can't quietly turn a short into an essay.
        max_h = int(self.dk_cfg.get("max_headline_chars", 80))
        max_w = int(self.dk_cfg.get("max_item_words", 60))
        max_why = int(self.dk_cfg.get("max_why_words", 35))
        bad = []
        for i, it in enumerate(items, 1):
            h = str(it.get("headline") or "")
            dek = str(it.get("dek") or "").replace("**", "")
            words = len((h + " " + dek).split())
            if len(h) > max_h:
                bad.append(f"item {i}: headline {len(h)}ch (max {max_h})")
            if words > max_w:
                bad.append(f"item {i}: {words} words (max {max_w})")
            for field in ("why", "counterpoint"):
                fw = len(str(it.get(field) or "").split())
                if fw > max_why:
                    bad.append(f"item {i}: {field} {fw} words (max {max_why})")
        self.check("D05-tiny-format", HARD, not bad, "; ".join(bad[:4]))

        # D06 lead item is first, internal, and points at a real article
        lead_ok, detail = False, "item 1 must be lead: true and link /articles/<slug>/"
        if items:
            first = items[0]
            m = re.search(r"/articles/([a-z0-9-]+)/?", str(first.get("url") or ""))
            leads = [i for i, it in enumerate(items) if it.get("lead")]
            if first.get("lead") and m and leads == [0]:
                slug = m.group(1)
                lead_ok = any(a.get("slug") == slug for a in all_articles())
                detail = f"lead slug '{slug}' not found in content/articles/"
        self.check("D06-lead-is-article", HARD, lead_ok, detail)

        # D07 zero JS beyond JSON-LD + the approved analytics snippet
        rogue = []
        for s in (dated_soup.find_all("script") if dated_soup else []):
            if s.get("type") == "application/ld+json":
                continue
            if (s.get("src") or "").startswith("https://gc.zgo.at/"):
                continue  # GoatCounter — the one approved analytics exception
            rogue.append((s.get("src") or "inline")[:60])
        self.check("D07-zero-js", HARD, built and not rogue,
                   "unexpected scripts: " + ", ".join(rogue[:3]))

        # D08 page weight (same proxy budget as G21)
        kb = (len(self.dated_path.read_bytes()) / 1024) if built else 999
        self.check("D08-page-weight", SOFT, kb <= 90, f"html {kb:.0f}KB (<=90)")

        # D10 watchlist tags valid + picks bounded and ordered
        wl = set(((self.cfg.get("docket") or {}).get("watchlist") or {}))
        max_picks = int(self.dk_cfg.get("max_picks", 2))
        bad = [f"item {i}: unknown tag '{it.get('tag')}'"
               for i, it in enumerate(items, 1)
               if str(it.get("tag") or "").strip()
               and str(it.get("tag")).strip() not in wl]
        picks = [i for i, it in enumerate(items) if it.get("pick")]
        if len(picks) > max_picks:
            bad.append(f"{len(picks)} picks (max {max_picks})")
        if any(items[i].get("lead") for i in picks):
            bad.append("lead entry cannot also be a pick")
        expected = list(range(1, 1 + len(picks)))
        if picks and picks != expected:
            bad.append("picks must sit immediately after the lead "
                       f"(positions {picks} != {expected})")
        self.check("D10-tags-picks", HARD, not bad, "; ".join(bad[:4]))

        # D11 watchlist coverage — a soft TARGET, never a filter:
        # serendipity slots are the docket's differentiation
        tagged = sum(1 for it in items if str(it.get("tag") or "").strip())
        self.check("D11-watch-quota", SOFT, tagged * 2 >= len(items),
                   f"{tagged}/{len(items)} entries tagged "
                   "(target >=half; wildcards are allowed and encouraged)")

        # D12 stakes coverage — the Brief layer's point is that every quick
        # item earns a "Why it matters" line. SOFT by design: the lead links
        # to the full article (its own analysis), so a missing lead `why` is
        # fine; a missing why on a *quick* item just warns, never blocks the
        # unattended run.
        no_why = [i for i, it in enumerate(items, 1)
                  if not it.get("lead") and not str(it.get("why") or "").strip()]
        self.check("D12-stakes-line", SOFT, not no_why,
                   f"quick items without a Why-it-matters line: {no_why} "
                   "(recommended on every non-lead entry)")

        # D09 canonicals + sitemap: dated page is the canonical unit
        expected = (self.cfg["site"]["base_url"].rstrip("/")
                    + f"/docket/{self.date}/")
        c_dated = dated_soup.find("link", rel="canonical") if dated_soup else None
        c_latest = latest_soup.find("link", rel="canonical") if latest_soup else None
        sm_path = self.out_dir / "sitemap.xml"
        sm = sm_path.read_text(encoding="utf-8") if sm_path.exists() else ""
        latest_all = all_dockets()
        is_latest = bool(latest_all) and latest_all[0]["date"] == self.date
        latest_ok = (not is_latest) or (
            c_latest is not None and c_latest.get("href") == expected)
        self.check("D09-canonicals", HARD,
                   c_dated is not None and c_dated.get("href") == expected
                   and latest_ok and f"docket/{self.date}/" in sm,
                   f"dated canonical must be {expected}, /docket/ must point at "
                   "the latest dated page, and the dated URL must be in sitemap.xml")

        return self.report()

    def report(self) -> dict:
        hard_fail = [r for r in self.results if r["level"] == HARD and not r["ok"]]
        soft_fail = [r for r in self.results if r["level"] == SOFT and not r["ok"]]
        rep = {"slug": f"docket-{self.date}", "checked_at": now_ist().isoformat(),
               "passed": not hard_fail,
               "hard_failures": len(hard_fail), "soft_warnings": len(soft_fail),
               "results": self.results}
        out = ROOT / "data" / "gate-reports"
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"{self.date}-docket.json"
        path.write_text(json.dumps(rep, indent=2, ensure_ascii=False),
                        encoding="utf-8")
        for r in self.results:
            mark = "PASS" if r["ok"] else ("WARN" if r["level"] == SOFT else "FAIL")
            line = f"[{mark}] {r['gate']}"
            if not r["ok"] and r["detail"]:
                line += f" — {r['detail']}"
            print(line)
        print(f"\n{'ALL DOCKET GATES PASSED' if rep['passed'] else 'DOCKET GATE FAILURES: ' + str(len(hard_fail))}"
              f" ({len(soft_fail)} soft warnings) → {path}")
        return rep


def run_docket_gates(date_str: str | None = None) -> dict:
    return DocketGateRunner(date_str).run()


# ---------------- publish ----------------

def docket_publish(date_str: str | None = None, push: bool = True) -> None:
    """Gate → commit → push. Never touches data/history.json (asserted)."""
    from .publish import _git  # same git plumbing as article publish
    day = date_str or today_str()
    rep = run_docket_gates(day)
    if not rep["passed"]:
        raise SystemExit("DOCKET hard-gate failures — refusing to publish the "
                         "docket. The article publish is unaffected.")
    hist = ROOT / "data" / "history.json"
    before = hist.read_bytes() if hist.exists() else b""
    _git("add", "-A")
    after = hist.read_bytes() if hist.exists() else b""
    if before != after:
        raise SystemExit("docket publish would modify data/history.json — "
                         "refusing (the docket never counts as the daily article)")
    status = _git("status", "--porcelain")
    if not status:
        print("nothing to commit")
        return
    cfg = load_config()
    _git("-c", "user.name=content-engine",
         "-c", "user.email=engine@users.noreply.github.com",
         "commit", "-m", f"Docket: {day}")
    if push:
        branch = cfg["publishing"]["git_branch"]
        try:
            _git("pull", "--rebase", cfg["publishing"]["git_remote"], branch)
        except RuntimeError as e:
            print(f"note: pull skipped ({e})")
        _git("push", cfg["publishing"]["git_remote"], f"HEAD:{branch}")
        print(f"pushed → {cfg['site']['base_url'].rstrip('/')}/docket/{day}/")
    else:
        print("committed locally (push skipped)")

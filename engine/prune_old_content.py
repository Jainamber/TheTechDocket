"""Auto-prune aged AI Models articles (>45 days) and Docket/Deck files (>90 days).

Keeps content/articles/, data/history.json, data/docket/, and docs/ in sync so
all build & S08b-slug-stable gates remain green.

Usage:
    python -m engine.prune_old_content           # apply deletions
    python -m engine.prune_old_content --dry-run # preview only
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "content" / "articles"
DOCKET_DIR = ROOT / "data" / "docket"
HISTORY_PATH = ROOT / "data" / "history.json"
DOCS_ARTICLES = ROOT / "docs" / "articles"
DOCS_DOCKET = ROOT / "docs" / "docket"

IST = timezone(timedelta(hours=5, minutes=30))
AI_MODELS_MAX_DAYS = 45
DECK_MAX_DAYS = 90
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def _parse_frontmatter(path: Path) -> dict:
    try:
        txt = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    m = FM_RE.match(txt)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def _parse_date(val) -> datetime.date | None:
    if not val:
        return None
    s = str(val).strip()[:10]
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def prune(dry_run: bool = False) -> dict:
    today = datetime.now(IST).date()
    ai_cutoff = today - timedelta(days=AI_MODELS_MAX_DAYS)
    deck_cutoff = today - timedelta(days=DECK_MAX_DAYS)

    removed_slugs: set[str] = set()
    removed_articles: list[str] = []
    removed_dockets: list[str] = []

    # 1. Prune AI Models articles older than 45 days
    if ARTICLES_DIR.exists():
        for md in sorted(ARTICLES_DIR.glob("*.md")):
            fm = _parse_frontmatter(md)
            if fm.get("hub") != "ai-models":
                continue
            dt = _parse_date(fm.get("date"))
            if dt is None:
                m = re.match(r"^(\d{4}-\d{2}-\d{2})-", md.name)
                dt = _parse_date(m.group(1)) if m else None
            if dt and dt < ai_cutoff:
                slug = str(fm.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", md.stem))
                removed_slugs.add(slug)
                removed_articles.append(md.name)
                if not dry_run:
                    md.unlink(missing_ok=True)
                    built = DOCS_ARTICLES / slug
                    if built.exists():
                        shutil.rmtree(built, ignore_errors=True)

    # Also prune any history.json ai-models entries older than 45 days
    if HISTORY_PATH.exists():
        try:
            hist = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        except Exception:
            hist = {}
        pub = hist.get("published") or []
        kept = []
        for entry in pub:
            slug = entry.get("slug") or ""
            dt = _parse_date(entry.get("date"))
            is_old_ai = entry.get("hub") == "ai-models" and dt and dt < ai_cutoff
            if slug in removed_slugs or is_old_ai:
                removed_slugs.add(slug)
                continue
            kept.append(entry)
        if not dry_run and len(kept) != len(pub):
            hist["published"] = kept
            HISTORY_PATH.write_text(json.dumps(hist, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # 2. Prune Docket / Deck markdown files older than 90 days
    if DOCKET_DIR.exists():
        for md in sorted(DOCKET_DIR.glob("*.md")):
            dt = _parse_date(md.stem)
            if dt and dt < deck_cutoff:
                removed_dockets.append(md.name)
                if not dry_run:
                    md.unlink(missing_ok=True)
                    built = DOCS_DOCKET / md.stem
                    if built.exists():
                        shutil.rmtree(built, ignore_errors=True)

    if DOCS_DOCKET.exists():
        for sub in sorted(DOCS_DOCKET.iterdir()):
            if not sub.is_dir():
                continue
            dt = _parse_date(sub.name)
            if dt and dt < deck_cutoff and not dry_run:
                shutil.rmtree(sub, ignore_errors=True)

    mode = "DRY RUN" if dry_run else "PRUNED"
    print(
        f"[{mode}] AI Models (< {ai_cutoff}, >{AI_MODELS_MAX_DAYS}d): {len(removed_articles)} articles | "
        f"Decks (< {deck_cutoff}, >{DECK_MAX_DAYS}d): {len(removed_dockets)} dockets"
    )
    return {"removed_articles": removed_articles, "removed_dockets": removed_dockets}


def main() -> None:
    ap = argparse.ArgumentParser(description="Prune aged AI Models articles (>45d) and Dockets/Decks (>90d)")
    ap.add_argument("--dry-run", action="store_true", help="Report what would be deleted without modifying files")
    args = ap.parse_args()
    prune(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

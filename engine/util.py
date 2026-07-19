"""Shared helpers: config, slugs, front-matter, history."""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
IST = timezone(timedelta(hours=5, minutes=30))


def load_config() -> dict:
    with open(ROOT / "config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    # allow/deny keyword lists are comma-separated strings for readability
    for key in ("allow_keywords", "deny_keywords"):
        flat = []
        for line in cfg["topic"].get(key, []):
            flat.extend(t.strip().lower() for t in line.split(",") if t.strip())
        cfg["topic"][key] = flat
    return cfg


def now_ist() -> datetime:
    return datetime.now(IST)


def today_str() -> str:
    return now_ist().strftime("%Y-%m-%d")


def slugify(text: str, max_words: int = 8) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).lower().strip()
    words = [w for w in re.split(r"[\s-]+", text) if w]
    stop = {"a", "an", "the", "of", "to", "in", "on", "for", "and", "is", "are",
            "was", "what", "why", "how", "its", "it", "vs"}
    kept = [w for w in words if w not in stop][:max_words] or words[:max_words]
    return "-".join(kept)


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def shingles(tokens: list[str], n: int = 5) -> set[tuple]:
    if len(tokens) < n:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------- front matter ----------------

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_article(path: Path) -> dict:
    # utf-8-sig: a BOM-prefixed file otherwise fails FM_RE and is silently
    # skipped by all_articles() (review finding F2b, 2026-07-16)
    raw = path.read_text(encoding="utf-8-sig")
    m = FM_RE.match(raw)
    if not m:
        raise ValueError(f"{path}: missing YAML front matter block")
    meta = yaml.safe_load(m.group(1)) or {}
    meta["_body_md"] = m.group(2).strip()
    meta["_path"] = str(path)
    return meta


def all_articles() -> list[dict]:
    arts = []
    for p in sorted((ROOT / "content" / "articles").glob("*.md")):
        try:
            arts.append(parse_article(p))
        except Exception as e:  # noqa: BLE001
            print(f"WARN: skipping {p}: {e}")
    arts.sort(key=lambda a: str(a.get("date", "")), reverse=True)
    return arts


# ---------------- history ----------------

HISTORY = ROOT / "data" / "history.json"


def load_history() -> dict:
    if HISTORY.exists():
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    return {"published": []}


def save_history(h: dict) -> None:
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(h, indent=2, ensure_ascii=False), encoding="utf-8")

"""Syndication & 1-click social distribution engine.

Generates ready-to-paste distribution kits for Hacker News, Reddit,
X (Twitter), Bluesky, and canonical cross-posting (Dev.to / Hashnode).
Optionally opens submission tabs directly in the user's default browser.

Usage:
  python -m engine.run share [--slug SLUG] [--date YYYY-MM-DD] [--open]
"""
from __future__ import annotations

import os
import subprocess
import sys
import urllib.parse
import webbrowser
from pathlib import Path

from .util import ROOT, all_articles, load_config, load_history, today_str


def _copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard using Windows clip.exe or pbcopy."""
    try:
        if os.name == "nt":
            subprocess.run(["clip.exe"], input=text.encode("utf-8"), check=True)
            return True
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
    except Exception:
        pass
    return False


def _suggest_subreddits(hub: str) -> list[str]:
    mapping = {
        "ai-models": ["r/artificial", "r/LocalLLaMA", "r/MachineLearning", "r/technology"],
        "ai-tools": ["r/technology", "r/programming", "r/pcmasterrace", "r/developersIndia"],
        "big-tech": ["r/technology", "r/business", "r/developersIndia"],
        "hardware": ["r/hardware", "r/pcmasterrace", "r/buildapc"],
        "policy": ["r/technology", "r/privacy", "r/india"],
        "explainers": ["r/technology", "r/programming", "r/explainlikeimfive"],
    }
    return mapping.get(hub, ["r/technology", "r/programming"])


def build_share_kit(slug: str | None = None, date_str: str | None = None,
                    open_browser: bool = False) -> dict:
    cfg = load_config()
    arts = all_articles()
    if not arts:
        raise ValueError("no articles found in content/articles/")

    target = None
    if slug:
        target = next((a for a in arts if a.get("slug") == slug), None)
        if not target:
            raise ValueError(f"article with slug '{slug}' not found")
    elif date_str:
        target = next((a for a in arts if str(a.get("date")) == date_str), None)
        if not target:
            raise ValueError(f"article with date '{date_str}' not found")
    else:
        # Default to latest published in history, else newest in arts
        hist = load_history().get("published", [])
        if hist:
            latest_slug = hist[-1].get("slug")
            target = next((a for a in arts if a.get("slug") == latest_slug), arts[0])
        else:
            target = arts[0]

    art_slug = target["slug"]
    art_date = str(target.get("date") or today_str())
    art_title = target["title"]
    art_desc = target.get("description", "")
    art_hub = target.get("hub", "ai-tools")
    base_url = cfg["site"]["base_url"].rstrip("/")
    canonical_url = f"{base_url}/articles/{art_slug}/"
    subreddits = _suggest_subreddits(art_hub)

    # Prepare platform payloads
    hn_query = urllib.parse.urlencode({"u": canonical_url, "t": art_title})
    hn_url = f"https://news.ycombinator.com/submitlink?{hn_query}"

    x_text = f"{art_title}\n\n{art_desc}"[:240]
    x_query = urllib.parse.urlencode({"text": x_text, "url": canonical_url})
    x_url = f"https://x.com/intent/tweet?{x_query}"

    reddit_query = urllib.parse.urlencode({"url": canonical_url, "title": art_title})
    reddit_url = f"https://www.reddit.com/submit?{reddit_query}"

    clipboard_payload = f"""{art_title}

{art_desc}

Read the full breakdown on The Tech Docket:
{canonical_url}
"""

    share_doc = f"""# Distribution Kit — {art_date} ({art_slug})

**Canonical URL:** {canonical_url}  
**Title:** {art_title}  
**Hub:** {art_hub}  

---

## 1. Hacker News
* **Direct Submit Link:** [Submit to HN]({hn_url})
* **Title:** `{art_title}`
* **Discussion Hook / Starter Comment:**
> We analyzed the background shift behind this: {art_desc} Full breakdown with benchmarks and architectural comparison at {canonical_url}.

---

## 2. Reddit
* **Recommended Subreddits:** {", ".join(subreddits)}
* **Direct Link Submit:** [Submit to Reddit]({reddit_url})
* **Markdown Discussion Starter (auto-copied to clipboard with --open):**
```markdown
**{art_title}**

{art_desc}

**Key takeaways:**
- Published today on The Tech Docket with inline source benchmarks.
- Full architectural breakdown and performance comparisons: {canonical_url}
```

---

## 3. X / Twitter
* **1-Click Tweet Intent:** [Post on X]({x_url})
* **Draft Post:**
```
{art_title}

{art_desc}

Full breakdown: {canonical_url}
```

---

## 4. Bluesky
* **Post Copy:**
```
{art_title}

{art_desc}

{canonical_url}

#TechNews #AI #TheTechDocket
```

---

## 5. Dev.to / Hashnode (Canonical Syndication)
* **Canonical URL to set:** `{canonical_url}`
* **Front matter template:**
```yaml
---
title: "{art_title}"
published: true
description: "{art_desc}"
tags: {art_hub}, tech, programming, webdev
canonical_url: "{canonical_url}"
---
```
*(Copy the markdown body from `content/articles/{art_date}-{art_slug}.md` under this front matter to syndicate with 100% canonical SEO credit).*
"""

    out_dir = ROOT / "data" / "social" / art_date
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "share-kit.md"
    out_path.write_text(share_doc, encoding="utf-8")

    opened = False
    if open_browser:
        _copy_to_clipboard(clipboard_payload)
        webbrowser.open_new_tab(hn_url)
        webbrowser.open_new_tab(x_url)
        webbrowser.open_new_tab(reddit_url)
        opened = True

    return {
        "slug": art_slug,
        "date": art_date,
        "path": str(out_path),
        "opened": opened,
        "hn_url": hn_url,
        "x_url": x_url,
        "reddit_url": reddit_url,
    }

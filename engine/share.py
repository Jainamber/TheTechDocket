"""Syndication & 1-click social distribution engine.

Generates ready-to-paste distribution kits for Hacker News, Reddit,
X (Twitter), Bluesky, and canonical cross-posting (Dev.to / Hashnode).
Optionally opens submission tabs directly in the user's default browser.

Usage:
  python -m engine.run share [--slug SLUG] [--date YYYY-MM-DD] [--open]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
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
        "ai-models": ["LocalLLaMA", "artificial", "MachineLearning", "technology", "developersIndia"],
        "ai-tools": ["developersIndia", "pcmasterrace", "programming", "technology", "Windows11"],
        "big-tech": ["technology", "business", "developersIndia", "programming"],
        "hardware": ["hardware", "pcmasterrace", "buildapc", "IndianGaming"],
        "policy": ["technology", "privacy", "india", "developersIndia"],
        "explainers": ["programming", "technology", "explainlikeimfive", "developersIndia"],
    }
    return mapping.get(hub, ["technology", "programming", "developersIndia"])


SUBREDDIT_FLAIRS = {
    "developersIndia": "News",
    "pcmasterrace": "Discussion",
    "Windows11": "News / Discussion",
    "programming": "Discussion",
    "technology": "Discussion",
    "LocalLLaMA": "Discussion",
    "IndianGaming": "Discussion",
    "hardware": "News",
    "buildapc": "Discussion",
    "artificial": "Discussion",
    "MachineLearning": "Discussion",
    "privacy": "News",
    "india": "Non-Political",
}


def _get_flair(sub: str) -> str:
    return SUBREDDIT_FLAIRS.get(sub, "Discussion")


def _extract_table(body_md: str) -> str:
    """Extract the first Markdown table block from body text."""
    lines = (body_md or "").splitlines()
    table_lines = []
    in_table = False
    for line in lines:
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table:
            break
    return "\n".join(table_lines)


def _human_reddit_post(target: dict, canonical_url: str) -> tuple[str, str]:
    """Return (conversational_title, markdown_body) in a natural, first-person voice."""
    title = target["title"]
    desc = target.get("description", "")
    slug = target["slug"]
    table = _extract_table(target.get("_body_md", ""))
    table_block = f"\n\nHere's the benchmark comparison from the post:\n\n{table}\n\n" if table else "\n\n"

    if "discord" in slug and "rust" in slug:
        human_title = "Discord's CTO just demoed a native Rust rebuild on Windows 11 — boots in <1s and uses ~290MB RAM (with 2 accounts active)"
        body = f"""Saw this clip from Discord's CTO (Stanislav Vishnevskiy) comparing their new experimental client built in Rust side-by-side against the current Electron build on two ThinkPads, and the difference is pretty wild.

The legacy Electron app took about 5 seconds to load, sat on a dark screen and the "Starting..." splash, and ate around 1GB of RAM. The Rust build faded in within a second with the full friends list ready and sat at 290.2MB of RAM on Task Manager (with two accounts signed in simultaneously).
{table_block}A lot of developers and students here in India are still on 8GB Windows 11 laptops where the OS alone eats 4GB right after boot. When you open Discord + Slack + VS Code + browser tabs, the machine basically starts swapping to disk and choking.

I put together a full breakdown with the benchmarks, memory numbers, and architectural comparison here if anyone wants a deep dive:
{canonical_url}

Curious what you all think — do you think other apps (Slack, Teams, VS Code) will follow suit and ditch Electron, or is web-wrapper development velocity too convenient for companies to walk away from?"""
    elif "openai" in slug and "training" in slug:
        human_title = "OpenAI quietly paused frontier RL training for two weeks after Astra showed misalignment signs"
        body = f"""OpenAI confirmed that frontier reinforcement learning runs were paused after unreleased models showed unexpected degrees of misalignment during cyber safety evaluations.
{table_block}I wrote up a breakdown of what was actually put on hold, why safety thresholds triggered the pause, and the wider infrastructure context here:
{canonical_url}

What's your take on whether RL post-training scaling is hitting a safety ceiling before compute ceilings?"""
    else:
        human_title = f"{title}"
        body = f"""{desc}
{table_block}Key context and architectural breakdown:
{canonical_url}

Curious to hear your perspectives on how this impacts the broader developer and hardware ecosystem."""

    return human_title, body


def fetch_hn_warmup_threads(limit: int = 4) -> list[dict]:
    """Fetch live rising and active discussions from Hacker News for karma building."""
    url = "https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=points>25&hitsPerPage=12"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TheTechDocket-Engine/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", [])
            valid = [h for h in hits if h.get("points", 0) >= 30 and h.get("num_comments", 0) >= 10][:limit]
            return valid
    except Exception:
        return []


def build_share_kit(slug: str | None = None, date_str: str | None = None,
                    chosen_sub: str | None = None,
                    open_browser: bool = False,
                    include_hn_warmup: bool = False) -> dict:
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
    primary_sub = chosen_sub or subreddits[0]
    primary_flair = _get_flair(primary_sub)

    # Build human conversational copy
    human_reddit_title, human_reddit_body = _human_reddit_post(target, canonical_url)

    # 1. Reddit Direct Text Submit URL (Pre-selects community + pre-populates title & body)
    reddit_params = urllib.parse.urlencode({
        "type": "TEXT",
        "title": human_reddit_title,
        "text": human_reddit_body,
    })
    reddit_direct_url = f"https://www.reddit.com/r/{primary_sub}/submit?{reddit_params}"

    reddit_sub_links = []
    for s in subreddits:
        p = urllib.parse.urlencode({"type": "TEXT", "title": human_reddit_title, "text": human_reddit_body})
        reddit_sub_links.append(f"- [Post to r/{s}](https://www.reddit.com/r/{s}/submit?{p})")

    # 2. Hacker News
    hn_query = urllib.parse.urlencode({"u": canonical_url, "t": human_reddit_title})
    hn_url = f"https://news.ycombinator.com/submitlink?{hn_query}"

    # 3. X / Twitter
    x_post_text = f"""{human_reddit_title}

{canonical_url}

• Cold boot under 1s
• 290MB RAM with 2 accounts signed in (~70% less memory)
• Full architectural breakdown on what changed under the hood"""
    x_query = urllib.parse.urlencode({"text": x_post_text})
    x_url = f"https://x.com/intent/tweet?{x_query}"

    # 4. HN Warmup Threads
    hn_warmup_section = ""
    hn_threads = fetch_hn_warmup_threads(limit=4) if include_hn_warmup else []
    if hn_threads:
        hn_warmup_section = "\n## Hacker News Karma Warmup (Live Active Threads)\n"
        hn_warmup_section += "> Post a constructive comment on 1–2 of these active threads to build initial karma before submitting external links:\n\n"
        for t in hn_threads:
            hn_warmup_section += f"- **[{t.get('title')}](https://news.ycombinator.com/item?id={t.get('objectID')})** ({t.get('points')} pts, {t.get('num_comments')} comments)\n"

    share_doc = f"""# Community Distribution Kit — {art_date} ({art_slug})

**Canonical URL:** {canonical_url}  
**Hub:** {art_hub}  

---

## 1. Reddit (Auto-Fills Community, Title & Body Text)
* **Primary Target:** `r/{primary_sub}`
* **Required Post Flair:** Select **`{primary_flair}`** (Click "Add flair and tags*" -> choose "{primary_flair}" -> Apply)
* **Direct Submit Link:** [Open Pre-Filled Submit Tab in r/{primary_sub}]({reddit_direct_url})
* **Other Subreddit Links:**
{chr(10).join(reddit_sub_links)}

### Pre-Filled Content:
**Title:**
```
{human_reddit_title}
```

**Body Text (auto-copied to clipboard with --open):**
```markdown
{human_reddit_body}
```

---

## 2. Hacker News
* **Direct Submit Link:** [Submit to HN]({hn_url})
*(Note: If your account is brand new with 1 karma, HN requires earning ~5 karma from comments first to clear `fnop=toonew`. See warmup threads below).*
* **Profile Setup:** Set your `about:` field at `https://news.ycombinator.com/user?id=Amber_Jain` to:
  `Data & AI systems engineer. Writing data-backed notes at https://thetechdocket.com`
{hn_warmup_section}
---

## 3. X / Twitter
* **Direct 1-Click Tweet:** [Open Pre-Filled Post on X]({x_url})
* **Post Copy:**
```
{x_post_text}
```

---

## 4. Dev.to / Hashnode (Canonical Cross-Posting)
* **Canonical URL:** `{canonical_url}`
* **Front Matter Template:**
```yaml
---
title: "{art_title}"
published: true
description: "{art_desc}"
tags: {art_hub}, tech, programming, windows
canonical_url: "{canonical_url}"
---
```
"""

    out_dir = ROOT / "data" / "social" / art_date
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "share-kit.md"
    out_path.write_text(share_doc, encoding="utf-8")

    # Render interactive distribution launchpad HTML
    launchpad_path = out_dir / "launchpad.html"
    try:
        from jinja2 import Environment, FileSystemLoader
        tmpl_dir = ROOT / "engine" / "templates"
        if (tmpl_dir / "launchpad.html").exists():
            env = Environment(loader=FileSystemLoader(str(tmpl_dir)), autoescape=True)
            template = env.get_template("launchpad.html")
            sub_dict = {
                s: {
                    "flair": _get_flair(s),
                    "url": f"https://www.reddit.com/r/{s}/submit?" + urllib.parse.urlencode({
                        "type": "TEXT",
                        "title": human_reddit_title,
                        "text": human_reddit_body,
                    })
                } for s in subreddits
            }
            html_content = template.render(
                title=art_title,
                date=art_date,
                slug=art_slug,
                canonical_url=canonical_url,
                hub=art_hub,
                subreddits=subreddits,
                primary_sub=primary_sub,
                primary_flair=primary_flair,
                reddit_url=reddit_direct_url,
                human_title=human_reddit_title,
                human_body=human_reddit_body,
                human_title_json=json.dumps(human_reddit_title),
                human_body_json=json.dumps(human_reddit_body),
                x_url=x_url,
                x_text=x_post_text,
                x_text_json=json.dumps(x_post_text),
                hn_url=hn_url,
                hn_threads=hn_threads,
                sub_data_json=json.dumps(sub_dict),
            )
            launchpad_path.write_text(html_content, encoding="utf-8")
            latest_lp = ROOT / "data" / "social" / "latest_launchpad.html"
            latest_lp.write_text(html_content, encoding="utf-8")
    except Exception:
        pass

    opened = False
    if open_browser:
        _copy_to_clipboard(human_reddit_body)
        if launchpad_path.exists():
            try:
                webbrowser.open_new_tab(launchpad_path.resolve().as_uri())
            except Exception:
                pass
        webbrowser.open_new_tab(reddit_direct_url)
        webbrowser.open_new_tab(x_url)
        if not include_hn_warmup:
            webbrowser.open_new_tab(hn_url)
        else:
            for t in hn_threads[:2]:
                webbrowser.open_new_tab(f"https://news.ycombinator.com/item?id={t.get('objectID')}")
        opened = True

    return {
        "slug": art_slug,
        "date": art_date,
        "path": str(out_path),
        "launchpad_path": str(launchpad_path) if launchpad_path.exists() else None,
        "opened": opened,
        "primary_sub": primary_sub,
        "flair": primary_flair,
        "reddit_url": reddit_direct_url,
        "x_url": x_url,
        "hn_url": hn_url,
        "human_title": human_reddit_title,
        "human_body": human_reddit_body,
        "hn_threads": hn_threads,
    }


SHARED_ARTICLES_FILE = Path.home() / ".ttd" / "shared_articles.json"
REPO_SHARED_FILE = ROOT / "data" / "social" / "shared.json"


def get_shared_slugs() -> set[str]:
    """Retrieve set of slugs that have already been launched locally."""
    slugs = set()
    for p in [SHARED_ARTICLES_FILE, REPO_SHARED_FILE]:
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                for s in data.get("shared", []):
                    slugs.add(s)
            except Exception:
                pass
    return slugs


def mark_as_shared(slug: str) -> None:
    """Record that an article's distribution tabs have been launched locally."""
    slugs = list(get_shared_slugs())
    if slug not in slugs:
        slugs.append(slug)
    payload = {"shared": slugs, "last_shared_at": today_str()}
    for p in [SHARED_ARTICLES_FILE, REPO_SHARED_FILE]:
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except Exception:
            pass


def run_catchup(force: bool = False, chosen_sub: str | None = None) -> dict | None:
    """Pull remote publishes and launch the Guided Browser Flow for any unshared articles."""
    print("[*] Checking for new publishes from cloud pipeline...")
    try:
        subprocess.run(["git", "pull", "--rebase", "origin", "main"],
                       cwd=str(ROOT), capture_output=True, timeout=15)
    except Exception:
        pass

    hist = load_history().get("published", [])
    if not hist:
        print("[!] No published articles found in data/history.json.")
        return None

    shared_slugs = get_shared_slugs()
    recent = hist[-7:]  # Evaluate last 7 days of publications
    unshared = [a for a in recent if a.get("slug") not in shared_slugs]

    if not unshared and not force:
        print(f"[OK] All recent articles ({len(recent)}) have already been shared.")
        print("     To re-launch today's distribution tabs anyway, pass --force.")
        return None

    target = unshared[-1] if unshared else hist[-1]
    target_slug = target["slug"]
    print(f"[*] Launching Guided Browser Flow for: '{target_slug}' ({target.get('date')})...")

    res = build_share_kit(slug=target_slug, chosen_sub=chosen_sub,
                          open_browser=True, include_hn_warmup=True)
    mark_as_shared(target_slug)

    print(f"[OK] Launched Launchpad UI + Reddit, X, and Hacker News tabs!")
    print(f"     Target Subreddit: r/{res['primary_sub']} (Flair: {res['flair']})")
    print(f"     Reddit body text has been copied to your system clipboard.")
    if res.get("launchpad_path"):
        print(f"     Launchpad Dashboard: {res['launchpad_path']}")
    return res

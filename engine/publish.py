"""Publish step: gate → record in history → git commit/push.

Never commits if hard gates fail. The on-publish GitHub Action then
handles IndexNow + WebSub pings from an unrestricted network.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from .gates import run_gates
from .util import ROOT, all_articles, load_config, load_history, now_ist, save_history


def _git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:400]}")
    return r.stdout.strip()


def publish(slug: str, push: bool = True) -> dict:
    cfg = load_config()
    rep = run_gates(slug)
    if not rep["passed"]:
        raise SystemExit("HARD gate failures — refusing to publish. "
                         "Fix the article and re-run build + gate.")
    art = next(a for a in all_articles() if a["slug"] == slug)

    hist = load_history()
    entry = {
        "date": str(art["date"]), "slug": slug, "title": art["title"],
        "keyword": art.get("keyword", ""), "hub": art.get("hub"),
        "published_at": now_ist().isoformat(),
        "review": art.get("review", {}),
        "gate_report": f"data/gate-reports/{now_ist().date()}-{slug}.json",
        "url": cfg["site"]["base_url"].rstrip("/") + f"/articles/{slug}/",
    }
    hist["published"] = [p for p in hist["published"] if p["slug"] != slug]
    hist["published"].append(entry)
    hist["published"].sort(key=lambda p: p["date"])
    save_history(hist)

    _git("add", "-A")
    status = _git("status", "--porcelain")
    if status:
        _git("-c", "user.name=content-engine",
             "-c", "user.email=engine@users.noreply.github.com",
             "commit", "-m", f"Publish: {art['title']}")
        if push:
            branch = cfg["publishing"]["git_branch"]
            try:
                _git("pull", "--rebase", cfg["publishing"]["git_remote"], branch)
            except RuntimeError as e:
                print(f"note: pull skipped ({e})")
            _git("push", cfg["publishing"]["git_remote"], f"HEAD:{branch}")
            print(f"pushed → {entry['url']}")
        else:
            print("committed locally (push skipped)")
    else:
        print("nothing to commit")
    return entry

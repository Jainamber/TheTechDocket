"""Automated Reddit API publisher with auto-flair attachment.

Uses Reddit's official OAuth API to submit posts programmatically,
querying the subreddit's flair templates and attaching the matching
flair_id so posts never fail with 'Your post must contain post flair'.

Requires environment variables:
  REDDIT_CLIENT_ID
  REDDIT_CLIENT_SECRET
  REDDIT_USERNAME
  REDDIT_PASSWORD
"""
from __future__ import annotations

import base64
import json
import os
import urllib.parse
import urllib.request


def is_configured() -> bool:
    return all(os.environ.get(k) for k in (
        "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"
    ))


def get_reddit_token() -> str:
    client_id = os.environ["REDDIT_CLIENT_ID"].strip()
    client_secret = os.environ["REDDIT_CLIENT_SECRET"].strip()
    username = os.environ["REDDIT_USERNAME"].strip()
    password = os.environ["REDDIT_PASSWORD"].strip()

    auth_str = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_str}",
        "User-Agent": "TheTechDocket-Publisher/1.0 (by /u/Amber_Jain)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = urllib.parse.urlencode({
        "grant_type": "password",
        "username": username,
        "password": password,
    }).encode()

    req = urllib.request.Request("https://www.reddit.com/api/v1/access_token", data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if "access_token" in res:
            return res["access_token"]
        raise RuntimeError(f"Reddit OAuth failed: {res}")


def get_subreddit_flairs(token: str, subreddit: str) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "TheTechDocket-Publisher/1.0 (by /u/Amber_Jain)",
    }
    url = f"https://oauth.reddit.com/r/{subreddit}/api/link_flair_v2"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []


def find_matching_flair_id(flairs: list[dict], desired: str = "News") -> str | None:
    desired_l = desired.lower()
    for f in flairs:
        text = str(f.get("text", "")).lower()
        if desired_l in text or text in desired_l:
            return f.get("id")
    for fallback in ("discussion", "article", "resource", "project"):
        for f in flairs:
            if fallback in str(f.get("text", "")).lower():
                return f.get("id")
    return flairs[0].get("id") if flairs else None


def submit_reddit_post(subreddit: str, title: str, text: str, desired_flair: str = "News") -> dict:
    if not is_configured():
        return {
            "ok": False,
            "error": "Reddit API credentials not set. Set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD.",
        }

    token = get_reddit_token()
    flairs = get_subreddit_flairs(token, subreddit)
    flair_id = find_matching_flair_id(flairs, desired_flair)

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "TheTechDocket-Publisher/1.0 (by /u/Amber_Jain)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "api_type": "json",
        "sr": subreddit,
        "kind": "self",
        "title": title,
        "text": text,
    }
    if flair_id:
        payload["flair_id"] = flair_id

    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request("https://oauth.reddit.com/api/submit", data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            json_data = res.get("json", {})
            errors = json_data.get("errors", [])
            if errors:
                return {"ok": False, "error": f"Reddit API error: {errors}"}
            post_data = json_data.get("data", {})
            return {
                "ok": True,
                "url": post_data.get("url"),
                "flair_id": flair_id,
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}

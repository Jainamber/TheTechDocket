"""Pull today's IST article & docket markdown from Google Drive for cloud auto-publishing.

Designed to run inside `.github/workflows/drive-auto-publish.yml` without interfering
with the local Windows `Auto-Publish.ps1` fallback.

Auth:
    Reads service-account JSON from `GDRIVE_SA_KEY` (falls back to `VERTEX_SA_KEY`).
    Requires only `google-auth` (plus stdlib `urllib.request`).

3-Day Trial Circuit Breaker (2026-11-25 .. 2026-11-27):
    Tracks daily cloud publish outcomes in `data/cloud-publish-trial.json`.
    After `TRIAL_END_DATE` (2026-11-27), if fewer than 2 trial days succeeded,
    cloud auto-publishing automatically halts (exit 0) so the local fallback takes over.

Usage:
    python -m engine.drive_sync pull [--date YYYY-MM-DD]
    python -m engine.drive_sync check-trial [--date YYYY-MM-DD]
    python -m engine.drive_sync record --date YYYY-MM-DD --status success|failed [--note "..."]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "content" / "articles"
DOCKET_DIR = ROOT / "data" / "docket"
TRIAL_STATE_PATH = ROOT / "data" / "cloud-publish-trial.json"

ARTICLES_FOLDER_ID = os.environ.get("GDRIVE_ARTICLES_FOLDER_ID", "1nqTLDLhB5vIKR7KG8XyEdqStPI2AX_ZR")
DOCKET_FOLDER_ID = os.environ.get("GDRIVE_DOCKET_FOLDER_ID", "1xs4awkRS1CHuEWniCgPrMFofrSZGETby")

TRIAL_START_DATE = "2026-11-25"
TRIAL_END_DATE = "2026-11-27"
MIN_TRIAL_SUCCESSES = 2

IST = timezone(timedelta(hours=5, minutes=30))
DRIVE_SCOPE = ["https://www.googleapis.com/auth/drive.readonly"]


def today_ist() -> str:
    return datetime.now(IST).strftime("%Y-%m-%d")


def _load_trial_state() -> dict:
    if TRIAL_STATE_PATH.exists():
        try:
            return json.loads(TRIAL_STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "trial_start": TRIAL_START_DATE,
        "trial_end": TRIAL_END_DATE,
        "min_successes_required": MIN_TRIAL_SUCCESSES,
        "halted": False,
        "runs": {},
    }


def _save_trial_state(state: dict) -> None:
    TRIAL_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRIAL_STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_trial_allowed(run_date: str) -> tuple[bool, str]:
    """Return (allowed, reason). Auto-halts after TRIAL_END_DATE if trial failed."""
    state = _load_trial_state()
    if state.get("halted"):
        return False, "Cloud auto-publish trial previously halted; leaving local Auto-Publish.ps1 fallback in charge."

    if run_date <= TRIAL_END_DATE:
        return True, f"Within 3-day trial window ({TRIAL_START_DATE}..{TRIAL_END_DATE})."

    runs = state.get("runs") or {}
    trial_successes = sum(
        1
        for d, info in runs.items()
        if TRIAL_START_DATE <= d <= TRIAL_END_DATE and info.get("status") == "success"
    )
    if trial_successes >= MIN_TRIAL_SUCCESSES:
        return True, f"3-day trial PASSED ({trial_successes}/3 days succeeded). Cloud auto-publish active."

    state["halted"] = True
    state["halted_at"] = run_date
    state["halt_reason"] = f"3-day trial ended with {trial_successes}/{MIN_TRIAL_SUCCESSES} required successes."
    _save_trial_state(state)
    return False, f"HALTED: {state['halt_reason']} Stopping cloud auto-publish; local fallback remains active."


def record_trial_run(run_date: str, status: str, note: str = "") -> dict:
    state = _load_trial_state()
    runs = state.setdefault("runs", {})
    runs[run_date] = {
        "status": status,
        "recorded_at_ist": datetime.now(IST).isoformat(timespec="seconds"),
        "note": note,
    }
    _save_trial_state(state)
    return state


def _get_access_token() -> str:
    raw = (os.environ.get("GDRIVE_SA_KEY") or os.environ.get("VERTEX_SA_KEY") or "").strip()
    if not raw:
        raise RuntimeError("Missing GDRIVE_SA_KEY (or VERTEX_SA_KEY) secret.")
    info = json.loads(raw)
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    creds = service_account.Credentials.from_service_account_info(info, scopes=DRIVE_SCOPE)
    creds.refresh(Request())
    return creds.token


def _drive_list(token: str, folder_id: str, name_prefix: str) -> list[dict]:
    q = f"'{folder_id}' in parents and trashed = false and name contains '{name_prefix}'"
    params = urllib.parse.urlencode({
        "q": q,
        "fields": "files(id,name,modifiedTime,mimeType)",
        "orderBy": "modifiedTime desc",
        "pageSize": 20,
    })
    url = f"https://www.googleapis.com/drive/v3/files?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("files") or []


def _drive_download(token: str, file_id: str) -> bytes:
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def pull_today(run_date: str) -> dict:
    token = _get_access_token()
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    DOCKET_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_articles: list[str] = []
    downloaded_dockets: list[str] = []

    # Pull latest matching article(s) YYYY-MM-DD-*.md
    seen_art_names: set[str] = set()
    for f in _drive_list(token, ARTICLES_FOLDER_ID, f"{run_date}-"):
        name = f["name"]
        if not name.startswith(f"{run_date}-") or not name.endswith(".md") or name in seen_art_names:
            continue
        seen_art_names.add(name)
        content = _drive_download(token, f["id"])
        target = ARTICLES_DIR / name
        target.write_bytes(content)
        downloaded_articles.append(name)

    # Pull latest matching docket YYYY-MM-DD.md
    for f in _drive_list(token, DOCKET_FOLDER_ID, f"{run_date}.md"):
        if f["name"] == f"{run_date}.md":
            content = _drive_download(token, f["id"])
            target = DOCKET_DIR / f"{run_date}.md"
            target.write_bytes(content)
            downloaded_dockets.append(f["name"])
            break

    result = {
        "date": run_date,
        "articles": downloaded_articles,
        "dockets": downloaded_dockets,
    }
    print(json.dumps(result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync today's article & docket from Google Drive for cloud auto-publish.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_chk = sub.add_parser("check-trial")
    p_chk.add_argument("--date", default=today_ist())

    p_pull = sub.add_parser("pull")
    p_pull.add_argument("--date", default=today_ist())

    p_rec = sub.add_parser("record")
    p_rec.add_argument("--date", default=today_ist())
    p_rec.add_argument("--status", choices=["success", "failed"], required=True)
    p_rec.add_argument("--note", default="")

    args = parser.parse_args()
    if args.cmd == "check-trial":
        allowed, reason = check_trial_allowed(args.date)
        print(reason)
        sys.exit(0 if allowed else 2)
    elif args.cmd == "pull":
        pull_today(args.date)
    elif args.cmd == "record":
        record_trial_run(args.date, args.status, args.note)
        print(f"Recorded trial run {args.date}: {args.status}")


if __name__ == "__main__":
    main()

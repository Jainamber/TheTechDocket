"""Fetch fresh global tech & AI openings (max 25 days old) for TheTechDocket /topics/jobs/openings/.

Ported from JobEngine's read-only ATS (Greenhouse, Ashby, Lever, SmartRecruiters, Workable),
Himalayas, and Jobicy fetchers — zero external pip dependencies (Python stdlib only).

Phase 1A additions:
- Loads `data/watchlist-100.json` (50 Global + 50 India) and tags every opening with `watchlist_slug`
  when its company matches the Top 100 Watchlist.
- Persists requisition-age tracking in `data/openings-history.json` (`id -> {first_seen_date,
  last_seen_date, company, watchlist_slug, title, source}`) across all live fetched reqs,
  computes weekly `ghost_job_ratio` (% of active watchlist reqs open >90 days), and keeps the
  public `/topics/jobs/openings/` feed strictly capped at `max_age_days: 25`.
- Supports `--validate-watchlist` to live-probe Greenhouse, Lever, Ashby, and SmartRecruiters
  tokens from `data/watchlist-100.json` and append ONLY tokens returning HTTP 200 with real jobs
  into `data/openings-watchlist.json` (preserving all existing working sources intact).

Usage:
    python -m engine.openings_fetch
    python -m engine.openings_fetch --validate-watchlist
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
import json
import re
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCHLIST_PATH = ROOT / "data" / "openings-watchlist.json"
TOP100_PATH = ROOT / "data" / "watchlist-100.json"
HISTORY_PATH = ROOT / "data" / "openings-history.json"
OUT_PATH = ROOT / "data" / "openings.json"

MAX_AGE_DAYS = 25
GHOST_JOB_THRESHOLD_DAYS = 90
MAX_OPENINGS = 300
TIMEOUT_S = 14
UA = "TheTechDocket-OpeningsBot/1.0 (+https://thetechdocket.com/topics/jobs/openings/)"

ATS_ENDPOINTS = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/%s/jobs?content=true",
    "lever": "https://api.lever.co/v0/postings/%s?mode=json",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/%s?includeCompensation=true",
    "smartrecruiters": "https://api.smartrecruiters.com/v1/companies/%s/postings",
    "workable": "https://apply.workable.com/api/v1/widget/accounts/%s?details=true",
}
VALIDATABLE_ATS = ("greenhouse", "lever", "ashby", "smartrecruiters")
HIMALAYAS_API = "https://himalayas.app/jobs/api?limit=100"
JOBICY_API = "https://jobicy.com/api/v2/remote-jobs?count=50"

TAG_RE = re.compile(r"<[^>]+>")
EXP_RANGE_RE = re.compile(r"\b(\d{1,2})\s*(?:\+|to|-|–)\s*(\d{1,2})?\s*\+?\s*(?:years?|yrs?)\b", re.I)
EXP_MIN_RE = re.compile(r"\b(\d{1,2})\s*\+\s*(?:years?|yrs?)\b", re.I)
EXP_PLAIN_RE = re.compile(r"\b(?:minimum|at least|requires?)\s+(\d{1,2})\s*(?:years?|yrs?)\b", re.I)
CORP_SUFFIX_RE = re.compile(
    r"\b(inc|corp|corporation|ltd|limited|llc|plc|co|company|technologies|technology|systems|solutions|services|platforms|holdings|group|labs|software|india|global)\b",
    re.I,
)

COUNTRY_PATTERNS = [
    ("India", r"\b(india|bengaluru|bangalore|hyderabad|pune|mumbai|chennai|noida|gurgaon|gurugram|delhi|ncr|kolkata)\b"),
    ("United States", r"\b(united states|usa|u\.s\.a?\.|san francisco|new york|nyc|seattle|austin|boston|los angeles|chicago|mountain view|palo alto|menlo park|remote\s*[-–(]*\s*us)\b"),
    ("United Kingdom", r"\b(united kingdom|uk|u\.k\.|london|manchester|edinburgh|cambridge,?\s*uk|bristol)\b"),
    ("Canada", r"\b(canada|toronto|vancouver|montreal|ottawa|waterloo)\b"),
    ("Germany", r"\b(germany|berlin|munich|münchen|frankfurt|hamburg|stuttgart)\b"),
    ("Singapore", r"\b(singapore)\b"),
    ("Australia", r"\b(australia|sydney|melbourne|brisbane)\b"),
    ("Japan", r"\b(japan|tokyo|osaka)\b"),
    ("France", r"\b(france|paris|lyon)\b"),
    ("Netherlands", r"\b(netherlands|amsterdam|rotterdam|eindhoven)\b"),
    ("Ireland", r"\b(ireland|dublin|cork)\b"),
    ("Sweden", r"\b(sweden|stockholm|gothenburg)\b"),
    ("Switzerland", r"\b(switzerland|zurich|zürich|geneva)\b"),
    ("Spain", r"\b(spain|madrid|barcelona)\b"),
    ("Poland", r"\b(poland|warsaw|krakow|kraków)\b"),
    ("Brazil", r"\b(brazil|são paulo|sao paulo|rio de janeiro)\b"),
    ("Mexico", r"\b(mexico|mexico city|guadalajara|monterrey)\b"),
    ("Israel", r"\b(israel|tel aviv|herzliya)\b"),
    ("UAE", r"\b(uae|united arab emirates|dubai|abu dhabi)\b"),
    ("South Korea", r"\b(south korea|seoul)\b"),
    ("Remote / Global", r"\b(worldwide|global|anywhere|remote|emea|apac|latam|americas|europe)\b"),
]

AI_TOOL_PATTERNS = [
    ("LLMs / GenAI", r"\b(llm|llms|large language model|generative ai|genai|foundation model|gpt-?4|gpt-?5|claude|gemini|llama|mistral)\b"),
    ("AI Agents", r"\b(ai agent|agentic|multi-agent|autonomous agent|tool use|mcp|model context protocol)\b"),
    ("PyTorch", r"\b(pytorch)\b"),
    ("TensorFlow / JAX", r"\b(tensorflow|jax|keras)\b"),
    ("RAG / Vector DB", r"\b(rag|retrieval[- ]augmented|vector database|pinecone|weaviate|qdrant|pgvector|faiss|milvus)\b"),
    ("LangChain / LangGraph", r"\b(langchain|langgraph|llamaindex|crewai|autogen)\b"),
    ("OpenAI / Anthropic API", r"\b(openai api|anthropic|claude api|bedrock|vertex ai|azure openai)\b"),
    ("CUDA / GPU Infra", r"\b(cuda|triton|tensorrt|vllm|sglang|gpu cluster|hpc|nccl|infiniBand)\b"),
    ("MLOps / Evals", r"\b(mlops|llm eval|evals|mlflow|weights\s*&\s*biases|wandb|kubeflow|ray|sagemaker)\b"),
    ("Fine-Tuning / RLHF", r"\b(fine[- ]?tuning|rlhf|dpo|lora|qlora|post[- ]training|pre[- ]training|transformers|hugging\s*face)\b"),
    ("AI Coding Tools", r"\b(cursor|github copilot|claude code|codex|devin|windsurf|ai-augmented)\b"),
    ("Machine Learning / NLP", r"\b(machine learning|deep learning|nlp|computer vision|reinforcement learning|neural network)\b"),
]


def _norm_company(text: str) -> str:
    s = re.sub(r"\([^)]*\)", " ", text or "")
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return s


def _norm_company_core(text: str) -> str:
    s = _norm_company(text)
    s = CORP_SUFFIX_RE.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_top100_watchlist(path: Path = TOP100_PATH) -> tuple[list[dict], dict[str, str]]:
    """Load data/watchlist-100.json and return (entries, normalized_name_to_slug_map)."""
    if not path.exists():
        return [], {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return [], {}
    entries = list(raw.get("global_watchlist") or []) + list(raw.get("india_watchlist") or [])
    lookup: dict[str, str] = {}
    for item in entries:
        slug = (item.get("slug") or "").strip().lower()
        comp = (item.get("company") or "").strip()
        if not slug:
            continue
        candidates = {slug, slug.replace("-", " "), slug.replace("-", "")}
        if comp:
            candidates.add(_norm_company(comp))
            core = _norm_company_core(comp)
            if len(core) >= 3:
                candidates.add(core)
            # Extract parenthetical aliases like "(TCS)", "(AWS)", "(Google)", "(Devin)"
            for paren in re.findall(r"\(([^)]+)\)", comp):
                for part in re.split(r"[/,]", paren):
                    p = re.sub(r"[^a-z0-9]+", " ", part.lower()).strip()
                    if len(p) >= 2:
                        candidates.add(p)
            # Split slash-separated brand names like "Alphabet (Google)" or "Zomato / Eternal"
            for part in re.split(r"[/|]", re.sub(r"\([^)]*\)", "", comp)):
                p = re.sub(r"[^a-z0-9]+", " ", part.lower()).strip()
                if len(p) >= 3:
                    candidates.add(p)
        for key in candidates:
            if key and key not in lookup:
                lookup[key] = slug
    return entries, lookup


def match_watchlist_slug(company: str, token: str = "", lookup: dict[str, str] | None = None) -> str | None:
    """Return canonical watchlist_slug from data/watchlist-100.json if matched, else None."""
    if not lookup:
        return None
    probes = []
    if token:
        t = token.strip().lower()
        probes.extend([t, t.replace("-", " "), t.replace("_", " ")])
    if company:
        probes.append(_norm_company(company))
        probes.append(_norm_company_core(company))
        for paren in re.findall(r"\(([^)]+)\)", company):
            probes.append(re.sub(r"[^a-z0-9]+", " ", paren.lower()).strip())
    for p in probes:
        if p and p in lookup:
            return lookup[p]
    return None


def _fetch_json_with_status(url: str) -> tuple[int, object | None]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            status = getattr(resp, "status", 200)
            return status, json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def _fetch_json(url: str):
    status, data = _fetch_json_with_status(url)
    return data if status == 200 else None


def _count_ats_jobs(ats: str, data: object) -> int:
    if not data:
        return 0
    if ats == "greenhouse" and isinstance(data, dict):
        return len(data.get("jobs") or [])
    if ats == "ashby" and isinstance(data, dict):
        return len(data.get("jobs") or [])
    if ats == "lever" and isinstance(data, list):
        return len(data)
    if ats == "smartrecruiters" and isinstance(data, dict):
        return len(data.get("content") or [])
    if ats == "workable" and isinstance(data, dict):
        return len(data.get("jobs") or [])
    return 0


def validate_watchlist_tokens(
    top100_path: Path = TOP100_PATH,
    watchlist_path: Path = WATCHLIST_PATH,
    write: bool = True,
) -> dict:
    """Live-probe candidate ATS tokens from watchlist-100.json before enabling any new board.

    Preserves all existing working entries in data/openings-watchlist.json intact.
    Appends ONLY Greenhouse, Lever, Ashby, or SmartRecruiters boards returning HTTP 200
    with >= 1 real job.
    """
    top100_entries, _ = load_top100_watchlist(top100_path)
    existing: list[dict] = []
    if watchlist_path.exists():
        existing = json.loads(watchlist_path.read_text(encoding="utf-8"))
    existing_keys = {(str(e.get("ats") or "").lower(), str(e.get("token") or "").lower()) for e in existing}

    candidates = []
    for item in top100_entries:
        ats = (item.get("ats_provider") or "").strip().lower()
        if ats not in VALIDATABLE_ATS:
            continue
        token = (item.get("ats_token") or item.get("slug") or "").strip().lower()
        if not token or (ats, token) in existing_keys:
            continue
        candidates.append((item, ats, token))

    added: list[dict] = []
    rejected: list[dict] = []
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _probe(cand):
        item, ats, token = cand
        url = ATS_ENDPOINTS[ats] % token
        status, data = _fetch_json_with_status(url)
        job_count = _count_ats_jobs(ats, data) if status == 200 else 0
        return item, ats, token, status, job_count

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for item, ats, token, status, job_count in pool.map(_probe, candidates):
            if status == 200 and job_count > 0:
                entry = {
                    "name": item["company"],
                    "ats": ats,
                    "token": token,
                    "watchlist_slug": item["slug"],
                    "job_count_at_curation": job_count,
                    "segment": item.get("sector", "watchlist-100"),
                    "verified_on": today_iso,
                }
                existing.append(entry)
                existing_keys.add((ats, token))
                added.append({"slug": item["slug"], "ats": ats, "token": token, "jobs": job_count})
            else:
                rejected.append({"slug": item["slug"], "ats": ats, "token": token, "http_status": status, "jobs": job_count})

    if write and added:
        watchlist_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = {
        "existing_before": len(existing) - len(added),
        "probed": len(candidates),
        "added_count": len(added),
        "rejected_count": len(rejected),
        "total_watchlist_boards": len(existing),
        "added": added,
        "rejected": rejected,
    }
    print(
        f"ATS Validation: probed {len(candidates)} watchlist-100 candidates -> "
        f"added {len(added)} (HTTP 200 w/ jobs), skipped {len(rejected)}, total boards={len(existing)}"
    )
    return summary


def _strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", html.unescape(text or ""))).strip()


def _parse_when(val) -> datetime | None:
    if not val:
        return None
    if isinstance(val, (int, float)):
        ts = val / 1000.0 if val > 1e12 else float(val)
        try:
            return datetime.fromtimestamp(ts, timezone.utc)
        except Exception:
            return None
    s = str(val).strip()
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    try:
        dt = parsedate_to_datetime(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _detect_country(location: str, workplace: str = "") -> str:
    hay = f"{location or ''} {workplace or ''}"
    for name, pat in COUNTRY_PATTERNS:
        if re.search(pat, hay, re.I):
            return name
    return "Global / Other"


def _detect_work_mode(location: str, workplace: str = "", title: str = "") -> str:
    hay = f"{location} {workplace} {title}".lower()
    if "remote" in hay or "worldwide" in hay or "anywhere" in hay:
        return "Remote"
    if "hybrid" in hay:
        return "Hybrid"
    return "Onsite"


def _detect_experience(title: str, desc: str) -> tuple[str, int | None]:
    text = f"{title} {desc[:2500]}"
    years = None
    for pat in (EXP_MIN_RE, EXP_PLAIN_RE, EXP_RANGE_RE):
        m = pat.search(text)
        if m:
            y = int(m.group(1))
            if 0 <= y <= 25:
                years = y
                break
    t_low = (title or "").lower()
    if years is not None:
        if years <= 2:
            return "0–2 yrs", years
        if years <= 5:
            return "2–5 yrs", years
        if years <= 8:
            return "5–8 yrs", years
        return "8+ yrs", years
    if any(k in t_low for k in ("intern", "new grad", "graduate", "junior", "entry")):
        return "0–2 yrs", None
    if any(k in t_low for k in ("principal", "staff", "distinguished", "director", "vp ", "head of", "architect")):
        return "8+ yrs", None
    if any(k in t_low for k in ("senior", "sr.", "sr ", "lead")):
        return "5–8 yrs", None
    return "Not specified", None


def _detect_ai_tools(title: str, desc: str, tags: list[str]) -> list[str]:
    hay = f"{title} {' '.join(tags)} {desc[:3000]}"
    found = [label for label, pat in AI_TOOL_PATTERNS if re.search(pat, hay, re.I)]
    return found


def _make_record(
    source: str,
    company: str,
    title: str,
    url: str,
    posted_dt: datetime | None,
    location: str,
    salary: str,
    tags: list[str],
    desc: str,
    workplace: str = "",
    watchlist_slug: str | None = None,
    now_dt: datetime | None = None,
) -> dict | None:
    """Build a normalized opening record (does NOT drop >25d reqs yet so history tracks age >90d)."""
    if not title or not url or not posted_dt:
        return None
    now = now_dt or datetime.now(timezone.utc)
    age_days = max(0, int((now - posted_dt).total_seconds() // 86400))
    clean_title = re.sub(r"\s+", " ", title).strip()[:140]
    clean_co = re.sub(r"\s+", " ", company).strip()[:80]
    clean_loc = re.sub(r"\s+", " ", location or "Remote").strip()[:90]
    exp_bucket, exp_min = _detect_experience(clean_title, desc)
    ai_tools = _detect_ai_tools(clean_title, desc, tags)
    jid = hashlib.sha1(f"{source}|{url}".encode("utf-8")).hexdigest()[:12]
    return {
        "id": jid,
        "source": source,
        "company": clean_co,
        "watchlist_slug": watchlist_slug,
        "title": clean_title,
        "apply_url": url,
        "posted_at": posted_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "posted_date": posted_dt.strftime("%Y-%m-%d"),
        "valid_through": (posted_dt + timedelta(days=30)).strftime("%Y-%m-%d"),
        "age_days": age_days,
        "location": clean_loc,
        "country": _detect_country(clean_loc, workplace),
        "work_mode": _detect_work_mode(clean_loc, workplace, clean_title),
        "exp_bucket": exp_bucket,
        "exp_min_years": exp_min,
        "ai_tools": ai_tools,
        "is_ai_role": bool(ai_tools),
        "salary": (salary or "").strip()[:60],
        "summary": (desc or "")[:240].strip(),
    }


def update_openings_history(
    live_jobs: list[dict],
    history_path: Path = HISTORY_PATH,
    today: date | None = None,
    ghost_threshold_days: int = GHOST_JOB_THRESHOLD_DAYS,
) -> tuple[dict[str, dict], dict]:
    """Persist `id -> {first_seen_date, last_seen_date, ...}` and compute ghost_job_ratio.

    Ghost Job Ratio = % of currently active Top-100 watchlist requisitions whose observed open
    duration `(today - first_seen_date)` exceeds `ghost_threshold_days` (default 90 days).
    """
    today_d = today or datetime.now(timezone.utc).date()
    today_iso = today_d.isoformat()

    history: dict[str, dict] = {}
    if history_path.exists():
        try:
            loaded = json.loads(history_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                history = loaded.get("requisitions", loaded) if "requisitions" in loaded else loaded
        except Exception:
            history = {}

    active_ids: set[str] = set()
    active_watchlist_ids: set[str] = set()
    ghost_watchlist_ids: set[str] = set()

    for j in live_jobs:
        jid = j["id"]
        active_ids.add(jid)
        prev = history.get(jid)
        if prev and prev.get("first_seen_date"):
            first_seen = prev["first_seen_date"]
        else:
            first_seen = today_iso
        try:
            first_d = date.fromisoformat(first_seen)
            tracked_days = max(0, (today_d - first_d).days)
        except ValueError:
            first_seen = today_iso
            tracked_days = 0

        history[jid] = {
            "first_seen_date": first_seen,
            "last_seen_date": today_iso,
            "company": j.get("company") or "",
            "watchlist_slug": j.get("watchlist_slug"),
            "title": j.get("title") or "",
            "source": j.get("source") or "",
        }
        j["first_seen_date"] = first_seen
        j["tracked_age_days"] = tracked_days

        if j.get("watchlist_slug"):
            active_watchlist_ids.add(jid)
            if tracked_days > ghost_threshold_days:
                ghost_watchlist_ids.add(jid)

    active_wl_count = len(active_watchlist_ids)
    ghost_count = len(ghost_watchlist_ids)
    ghost_ratio = round((ghost_count / active_wl_count) * 100.0, 2) if active_wl_count > 0 else 0.0
    first_dates = [v.get("first_seen_date") for v in history.values() if v.get("first_seen_date")]
    tracking_since = min(first_dates) if first_dates else today_iso

    history_payload = {
        "schema_version": "1.0",
        "updated_at": today_iso,
        "ghost_threshold_days": ghost_threshold_days,
        "requisitions": history,
    }
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ghost_stats = {
        "threshold_days": ghost_threshold_days,
        "active_watchlist_reqs": active_wl_count,
        "ghost_reqs_over_90d": ghost_count,
        "ghost_job_ratio_pct": ghost_ratio,
        "active_total_reqs": len(active_ids),
        "history_tracked_total": len(history),
        "tracking_since": tracking_since,
    }
    return history, ghost_stats


def _fetch_ats_company(entry: dict, wl_lookup: dict[str, str]) -> list[dict]:
    ats = entry.get("ats")
    token = entry.get("token")
    name = entry.get("name") or token
    if ats not in ATS_ENDPOINTS or not token:
        return []
    data = _fetch_json(ATS_ENDPOINTS[ats] % token)
    if not data:
        return []
    wslug = entry.get("watchlist_slug") or match_watchlist_slug(name, token, wl_lookup)
    out = []
    try:
        if ats == "greenhouse":
            for j in data.get("jobs", []):
                rec = _make_record(
                    "greenhouse", name, j.get("title") or "", j.get("absolute_url") or "",
                    _parse_when(j.get("first_published") or j.get("updated_at")),
                    (j.get("location") or {}).get("name") or "", "",
                    [(d or {}).get("name", "") for d in (j.get("departments") or [])],
                    _strip_html(j.get("content") or ""),
                    watchlist_slug=wslug,
                )
                if rec:
                    out.append(rec)
        elif ats == "ashby":
            for j in data.get("jobs", []):
                locs = [j.get("location") or ""] + [(s or {}).get("location", "") for s in (j.get("secondaryLocations") or [])]
                comp = ((j.get("compensation") or {}).get("compensationTierSummary") or "")
                rec = _make_record(
                    "ashby", name, j.get("title") or "", j.get("jobUrl") or j.get("applyUrl") or "",
                    _parse_when(j.get("publishedAt")), ", ".join(x for x in locs if x), comp,
                    [j.get("department") or "", j.get("team") or ""],
                    _strip_html(j.get("descriptionHtml") or ""),
                    "remote" if j.get("isRemote") else "",
                    watchlist_slug=wslug,
                )
                if rec:
                    out.append(rec)
        elif ats == "lever":
            for j in (data if isinstance(data, list) else []):
                cats = j.get("categories") or {}
                rec = _make_record(
                    "lever", name, j.get("text") or "", j.get("hostedUrl") or "",
                    _parse_when(j.get("createdAt")), cats.get("location") or "", "",
                    [cats.get(k) or "" for k in ("team", "department", "commitment")],
                    j.get("descriptionPlain") or "", (j.get("workplaceType") or "").lower(),
                    watchlist_slug=wslug,
                )
                if rec:
                    out.append(rec)
        elif ats == "workable":
            for j in data.get("jobs", []):
                loc = ", ".join(x for x in (j.get("city"), j.get("state"), j.get("country")) if x)
                rec = _make_record(
                    "workable", name, j.get("title") or "", j.get("url") or "",
                    _parse_when(j.get("published_on")), loc, "",
                    [j.get("department") or ""], _strip_html(j.get("description") or ""),
                    "remote" if j.get("telecommuting") else "",
                    watchlist_slug=wslug,
                )
                if rec:
                    out.append(rec)
        elif ats == "smartrecruiters":
            for j in data.get("content", []):
                loc = j.get("location") or {}
                loc_str = ", ".join(x for x in (loc.get("city"), loc.get("country")) if x)
                if loc.get("remote"):
                    loc_str = ("Remote " + loc_str).strip()
                uid = j.get("id") or j.get("uuid") or ""
                url = f"https://jobs.smartrecruiters.com/{token}/{uid}" if uid else ""
                rec = _make_record(
                    "smartrecruiters", name, j.get("name") or "", url,
                    _parse_when(j.get("releasedDate")), loc_str, "",
                    [(j.get("department") or {}).get("label", "")], "",
                    "remote" if loc.get("remote") else "",
                    watchlist_slug=wslug,
                )
                if rec:
                    out.append(rec)
    except Exception:
        pass
    return out


def _fetch_himalayas(wl_lookup: dict[str, str]) -> list[dict]:
    data = _fetch_json(HIMALAYAS_API)
    if not data or "jobs" not in data:
        return []
    out = []
    for it in data["jobs"]:
        co = it.get("companyName") or ""
        locs = it.get("locationRestrictions")
        loc = "Worldwide" if (isinstance(locs, list) and not locs) else ", ".join(locs or [])
        lo, hi = it.get("minSalary"), it.get("maxSalary")
        cur = it.get("currency") or "USD"
        sal = ""
        if lo:
            hi = hi or lo
            sal = f"${int(lo):,}–${int(hi):,}" if cur == "USD" else f"{cur} {int(lo):,}–{int(hi):,}"
        rec = _make_record(
            "himalayas", co, it.get("title") or "",
            it.get("applicationLink") or it.get("guid") or "",
            _parse_when(it.get("pubDate")), loc or "Worldwide", sal,
            list(it.get("categories") or []) + list(it.get("seniority") or []),
            _strip_html(it.get("description") or it.get("excerpt") or ""), "remote",
            watchlist_slug=match_watchlist_slug(co, "", wl_lookup),
        )
        if rec:
            out.append(rec)
    return out


def _fetch_jobicy(wl_lookup: dict[str, str]) -> list[dict]:
    data = _fetch_json(JOBICY_API)
    if not data or "jobs" not in data:
        return []
    out = []
    for it in data["jobs"]:
        co = it.get("companyName") or ""
        sal = ""
        if it.get("annualSalaryMin"):
            lo = int(it["annualSalaryMin"])
            hi = int(it.get("annualSalaryMax") or lo)
            cur = it.get("salaryCurrency") or "USD"
            sal = f"${lo:,}–${hi:,}" if cur == "USD" else f"{cur} {lo:,}–{hi:,}"
        rec = _make_record(
            "jobicy", co, it.get("jobTitle") or "",
            it.get("url") or "", _parse_when(it.get("pubDate")),
            it.get("jobGeo") or "Remote", sal,
            list(it.get("jobIndustry") or []) + list(it.get("jobType") or []),
            _strip_html(it.get("jobExcerpt") or ""), "remote",
            watchlist_slug=match_watchlist_slug(co, "", wl_lookup),
        )
        if rec:
            out.append(rec)
    return out


def run() -> dict:
    watchlist = []
    if WATCHLIST_PATH.exists():
        watchlist = json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
    _, wl_lookup = load_top100_watchlist(TOP100_PATH)

    all_live_jobs: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(_fetch_ats_company, entry, wl_lookup) for entry in watchlist]
        futs.append(pool.submit(_fetch_himalayas, wl_lookup))
        futs.append(pool.submit(_fetch_jobicy, wl_lookup))
        for f in concurrent.futures.as_completed(futs):
            try:
                all_live_jobs.extend(f.result())
            except Exception:
                pass

    # Persist requisition-age history across ALL live reqs & compute >90d ghost_job_ratio
    _, ghost_stats = update_openings_history(all_live_jobs, HISTORY_PATH)

    # Public /topics/jobs/openings/ feed remains strictly capped at MAX_AGE_DAYS (25 days)
    fresh_jobs = [j for j in all_live_jobs if j["age_days"] <= MAX_AGE_DAYS]

    # Deduplicate by apply_url and (company, title, country)
    seen_urls, seen_keys, deduped = set(), set(), []
    for j in sorted(fresh_jobs, key=lambda x: (x["age_days"], not x["is_ai_role"], not bool(x["salary"]))):
        u = j["apply_url"].split("?")[0].rstrip("/").lower()
        k = (j["company"].lower(), j["title"].lower(), j["country"].lower())
        if u in seen_urls or k in seen_keys:
            continue
        seen_urls.add(u)
        seen_keys.add(k)
        deduped.append(j)

    trimmed = deduped[:MAX_OPENINGS]
    countries = sorted({j["country"] for j in trimmed})
    ai_tools = sorted({t for j in trimmed for t in j["ai_tools"]})
    watchlist_matched = sum(1 for j in trimmed if j.get("watchlist_slug"))
    payload = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "max_age_days": MAX_AGE_DAYS,
        "update_cadence": "Refreshed weekly (roles older than 25 days auto-expire)",
        "sources_polled": len(watchlist) + 2,
        "total_openings": len(trimmed),
        "watchlist_100_matched": watchlist_matched,
        "ghost_job_ratio": ghost_stats["ghost_job_ratio_pct"],
        "ghost_job_stats": ghost_stats,
        "countries": countries,
        "ai_tools": ai_tools,
        "openings": trimmed,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Saved {len(trimmed)} fresh openings (<= {MAX_AGE_DAYS}d, {watchlist_matched} watchlist-100 matched, "
        f"ghost_job_ratio={ghost_stats['ghost_job_ratio_pct']}%) from {len(watchlist)+2} sources -> {OUT_PATH}"
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch fresh tech/AI openings & track watchlist-100 ghost-job ratio.")
    parser.add_argument(
        "--validate-watchlist",
        action="store_true",
        help="Live-probe Greenhouse/Lever/Ashby/SmartRecruiters tokens from data/watchlist-100.json and add only HTTP 200 boards with real jobs.",
    )
    parser.add_argument(
        "--dry-run-validate",
        action="store_true",
        help="Probe candidate tokens from data/watchlist-100.json without modifying data/openings-watchlist.json.",
    )
    args = parser.parse_args()
    if args.validate_watchlist or args.dry_run_validate:
        validate_watchlist_tokens(write=not args.dry_run_validate)
        if args.dry_run_validate:
            return
    run()


if __name__ == "__main__":
    main()

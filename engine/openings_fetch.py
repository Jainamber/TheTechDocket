"""Fetch fresh global tech & AI openings (max 25 days old) for TheTechDocket /topics/jobs/openings/.

Ported from JobEngine's read-only ATS (Greenhouse, Ashby, Lever, SmartRecruiters, Workable),
Himalayas, and Jobicy fetchers — zero external pip dependencies (Python stdlib only).

Usage:
    python -m engine.openings_fetch
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCHLIST_PATH = ROOT / "data" / "openings-watchlist.json"
OUT_PATH = ROOT / "data" / "openings.json"

MAX_AGE_DAYS = 25
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
HIMALAYAS_API = "https://himalayas.app/jobs/api?limit=100"
JOBICY_API = "https://jobicy.com/api/v2/remote-jobs?count=50"

TAG_RE = re.compile(r"<[^>]+>")
EXP_RANGE_RE = re.compile(r"\b(\d{1,2})\s*(?:\+|to|-|–)\s*(\d{1,2})?\s*\+?\s*(?:years?|yrs?)\b", re.I)
EXP_MIN_RE = re.compile(r"\b(\d{1,2})\s*\+\s*(?:years?|yrs?)\b", re.I)
EXP_PLAIN_RE = re.compile(r"\b(?:minimum|at least|requires?)\s+(\d{1,2})\s*(?:years?|yrs?)\b", re.I)

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


def _fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:
        return None


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


def _make_record(source: str, company: str, title: str, url: str, posted_dt: datetime | None,
                 location: str, salary: str, tags: list[str], desc: str, workplace: str = "") -> dict | None:
    if not title or not url or not posted_dt:
        return None
    now = datetime.now(timezone.utc)
    age_days = max(0, int((now - posted_dt).total_seconds() // 86400))
    if age_days > MAX_AGE_DAYS:
        return None
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


def _fetch_ats_company(entry: dict) -> list[dict]:
    ats = entry.get("ats")
    token = entry.get("token")
    name = entry.get("name") or token
    if ats not in ATS_ENDPOINTS or not token:
        return []
    data = _fetch_json(ATS_ENDPOINTS[ats] % token)
    if not data:
        return []
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
                )
                if rec:
                    out.append(rec)
    except Exception:
        pass
    return out


def _fetch_himalayas() -> list[dict]:
    data = _fetch_json(HIMALAYAS_API)
    if not data or "jobs" not in data:
        return []
    out = []
    for it in data["jobs"]:
        locs = it.get("locationRestrictions")
        loc = "Worldwide" if (isinstance(locs, list) and not locs) else ", ".join(locs or [])
        lo, hi = it.get("minSalary"), it.get("maxSalary")
        cur = it.get("currency") or "USD"
        sal = ""
        if lo:
            hi = hi or lo
            sal = f"${int(lo):,}–${int(hi):,}" if cur == "USD" else f"{cur} {int(lo):,}–{int(hi):,}"
        rec = _make_record(
            "himalayas", it.get("companyName") or "", it.get("title") or "",
            it.get("applicationLink") or it.get("guid") or "",
            _parse_when(it.get("pubDate")), loc or "Worldwide", sal,
            list(it.get("categories") or []) + list(it.get("seniority") or []),
            _strip_html(it.get("description") or it.get("excerpt") or ""), "remote",
        )
        if rec:
            out.append(rec)
    return out


def _fetch_jobicy() -> list[dict]:
    data = _fetch_json(JOBICY_API)
    if not data or "jobs" not in data:
        return []
    out = []
    for it in data["jobs"]:
        sal = ""
        if it.get("annualSalaryMin"):
            lo = int(it["annualSalaryMin"])
            hi = int(it.get("annualSalaryMax") or lo)
            cur = it.get("salaryCurrency") or "USD"
            sal = f"${lo:,}–${hi:,}" if cur == "USD" else f"{cur} {lo:,}–{hi:,}"
        rec = _make_record(
            "jobicy", it.get("companyName") or "", it.get("jobTitle") or "",
            it.get("url") or "", _parse_when(it.get("pubDate")),
            it.get("jobGeo") or "Remote", sal,
            list(it.get("jobIndustry") or []) + list(it.get("jobType") or []),
            _strip_html(it.get("jobExcerpt") or ""), "remote",
        )
        if rec:
            out.append(rec)
    return out


def run() -> dict:
    watchlist = []
    if WATCHLIST_PATH.exists():
        watchlist = json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))

    all_jobs: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(_fetch_ats_company, entry) for entry in watchlist]
        futs.append(pool.submit(_fetch_himalayas))
        futs.append(pool.submit(_fetch_jobicy))
        for f in concurrent.futures.as_completed(futs):
            try:
                all_jobs.extend(f.result())
            except Exception:
                pass

    # Deduplicate by apply_url and (company, title, country)
    seen_urls, seen_keys, deduped = set(), set(), []
    for j in sorted(all_jobs, key=lambda x: (x["age_days"], not x["is_ai_role"], not bool(x["salary"]))):
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
    payload = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "max_age_days": MAX_AGE_DAYS,
        "update_cadence": "Refreshed weekly (roles older than 25 days auto-expire)",
        "sources_polled": len(watchlist) + 2,
        "total_openings": len(trimmed),
        "countries": countries,
        "ai_tools": ai_tools,
        "openings": trimmed,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(trimmed)} fresh openings (<= {MAX_AGE_DAYS}d) from {len(watchlist)+2} sources -> {OUT_PATH}")
    return payload


if __name__ == "__main__":
    run()

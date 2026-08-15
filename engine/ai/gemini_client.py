"""Vertex AI (Gemini) HTTP client for the daily editorial pipeline.

Adapted (not imported) from `C:/oProjectsHigh/GeminiBridge/bridge.py`, a
live-proven client for the SAME GCP project: endpoint construction, the ADC
access-token subprocess flow + on-disk cache, 401 force-refresh, 403
`x-goog-user-project` quota retry, thinkingLevel-vs-thinkingBudget handling,
and usageMetadata parsing (including thoughtsTokenCount) are all carried
over. New here: ledger-gated budget enforcement, googleSearch/urlContext
tool + groundingMetadata parsing, JSON-schema-forced output, model
fallback, and a fixture-replay mode for $0/no-network tests.

Contract: `generate()` ALWAYS calls `ledger.precheck(step)` before any HTTP
request (raises BudgetExceeded, no ledger row written) and ALWAYS calls
`ledger.record(...)` after an attempt — success, HTTP/parse failure, or
fixture replay — so data/costs/ledger.csv stays a complete spend record.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from zoneinfo import ZoneInfo

from .ledger import BudgetExceeded, Ledger  # noqa: F401  (re-exported: see below)
from .pricing import estimate

IST = ZoneInfo("Asia/Kolkata")
ROOT = Path(__file__).resolve().parent.parent.parent

# ~/.ttd/ holds runtime-only, never-committed local state (token cache,
# project id). Never written into the repo — see SPEC.md hard rule 2.
TOKEN_CACHE_PATH = Path.home() / ".ttd" / "token_cache.json"
VERTEX_CONFIG_PATH = Path.home() / ".ttd" / "vertex.json"
TOKEN_TTL_S = 40 * 60  # ~40 min; bridge.py uses 45 min (2700s), kept slightly tighter here

RETRY_STATUSES = {408, 429, 500, 502, 503, 504, 529}
MAX_ATTEMPTS = 3


class ModelUnavailable(RuntimeError):
    """Raised when Vertex returns 404 for a model (not served in this
    project/location) — see SPEC.md "NOT SERVED" list."""


# BudgetExceeded is defined in ledger.py (it's Ledger.precheck() that raises
# it) and re-exported here so `engine.ai.gemini_client.BudgetExceeded` is
# importable per SPEC.md's module contract, without a circular import.
__all__ = ["GeminiClient", "GenResult", "BudgetExceeded", "ModelUnavailable"]


@dataclass
class GenResult:
    text: str
    usage: dict                # {"in": int, "out": int, "thinking": int}
    grounded_queries: int
    url_fetches: int
    sources: list = field(default_factory=list)   # [{"url": str, "title": str}]
    finish_reason: str = "?"
    cost_usd: float = -1.0
    model: str = ""


def _resolve_project() -> str:
    proj = os.environ.get("TTD_GCP_PROJECT")
    if proj:
        return proj
    if VERTEX_CONFIG_PATH.exists():
        try:
            data = json.loads(VERTEX_CONFIG_PATH.read_text(encoding="utf-8"))
            if data.get("project"):
                return data["project"]
        except Exception:
            pass
    raise RuntimeError(
        "no GCP project configured: set env TTD_GCP_PROJECT, or write "
        f'{{"project": "..."}} to {VERTEX_CONFIG_PATH}')


def _endpoint(project: str, location: str, model: str) -> str:
    # Mirrors bridge.py's endpoint_for(): the `global` location uses the
    # plain aiplatform.googleapis.com host; other locations are region-prefixed.
    host = "aiplatform.googleapis.com" if location == "global" else f"{location}-aiplatform.googleapis.com"
    return (f"https://{host}/v1/projects/{project}/locations/{location}"
            f"/publishers/google/models/{model}:generateContent")


def _thinking_config(thinking) -> dict:
    """int -> thinkingBudget (2.5-series token budget, -1 = dynamic);
    str -> thinkingLevel (3.x-series: minimal|low|medium|high)."""
    if isinstance(thinking, int):
        return {"thinkingBudget": thinking}
    t = str(thinking).strip()
    if t.lstrip("-").isdigit():
        return {"thinkingBudget": int(t)}
    return {"thinkingLevel": t.lower()}


def _gcloud_token(force: bool = False) -> str:
    if not force and TOKEN_CACHE_PATH.exists():
        try:
            cache = json.loads(TOKEN_CACHE_PATH.read_text(encoding="utf-8"))
            if cache.get("token") and time.time() - cache.get("ts", 0) < TOKEN_TTL_S:
                return cache["token"]
        except Exception:
            pass
    exe = shutil.which("gcloud") or shutil.which("gcloud.cmd")
    if not exe:
        raise RuntimeError("gcloud CLI not found on PATH (needed for the ADC access token)")
    p = subprocess.run(
        [exe, "auth", "application-default", "print-access-token"],
        capture_output=True, text=True, timeout=45,
    )
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError(
            "could not obtain an ADC access token — run "
            "`gcloud auth application-default login`")
    token = p.stdout.strip().splitlines()[-1].strip()
    try:
        TOKEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_CACHE_PATH.write_text(json.dumps({"token": token, "ts": time.time()}), encoding="utf-8")
    except Exception:
        pass
    return token


def _sa_token() -> str:
    """CI path: GOOGLE_APPLICATION_CREDENTIALS points at a service-account
    key JSON file. Lazy-imported so local/gcloud-ADC usage never needs
    google-auth installed."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import service_account
    except ImportError as e:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS is set but google-auth is not "
            "installed — pip install -r requirements-ai.txt") from e
    creds = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    creds.refresh(Request())
    return creds.token


def _get_token(force: bool = False) -> str:
    env_tok = os.environ.get("GEMINI_BEARER_TOKEN")
    if env_tok:
        return env_tok
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        return _sa_token()
    return _gcloud_token(force=force)


def _http_post_json(url: str, headers: dict, body: dict, timeout: int):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            payload = {"error": {"message": "unreadable error body"}}
        return e.code, payload


def _parse_grounding(payload: dict) -> tuple:
    """(grounded_queries, url_fetches, sources) from groundingMetadata /
    urlContextMetadata on the first candidate. Missing metadata -> (0,0,[])."""
    cands = payload.get("candidates") or []
    if not cands:
        return 0, 0, []
    cand = cands[0]
    gm = cand.get("groundingMetadata") or {}
    grounded_queries = len(gm.get("webSearchQueries") or [])
    sources = []
    for chunk in gm.get("groundingChunks") or []:
        web = chunk.get("web") or {}
        if web.get("uri"):
            sources.append({"url": web.get("uri", ""), "title": web.get("title", "")})
    ucm = cand.get("urlContextMetadata") or {}
    url_fetches = len(ucm.get("urlMetadata") or [])
    return grounded_queries, url_fetches, sources


def _parse_response(payload: dict) -> dict:
    um = payload.get("usageMetadata") or {}
    tin = int(um.get("promptTokenCount", 0))
    tout = int(um.get("candidatesTokenCount", 0))
    thinking = int(um.get("thoughtsTokenCount", 0))
    cands = payload.get("candidates") or []
    if not cands:
        block = (payload.get("promptFeedback") or {}).get("blockReason")
        raise RuntimeError(f"no candidates (blockReason={block or 'none'}): {json.dumps(payload)[:300]}")
    cand = cands[0]
    parts = (cand.get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    finish = cand.get("finishReason", "?")
    grounded_queries, url_fetches, sources = _parse_grounding(payload)
    return {
        "text": text, "finish_reason": finish,
        "usage": {"in": tin, "out": tout, "thinking": thinking},
        "grounded_queries": grounded_queries, "url_fetches": url_fetches,
        "sources": sources,
    }


class GeminiClient:
    def __init__(self, config: dict, ledger: Ledger, fixture_dir: str | None = None,
                 root: str | Path | None = None):
        # NOTE: `root` is not in SPEC.md's literal signature. Added (optional,
        # defaults to repo root) per SPEC.md's own testing instructions
        # ("modules should take a root path arg ... make them testable").
        self.config = config or {}
        self.ledger = ledger
        self.root = Path(root) if root else ROOT
        self.fixture_mode = bool(fixture_dir) or os.environ.get("TTD_AI_FIXTURE") == "1"
        self.fixture_dir = Path(fixture_dir) if fixture_dir else (self.root / "tests" / "fixtures" / "ai")
        self.location = self.config.get("location", "global")
        self.project = None
        if not self.fixture_mode:
            self.project = _resolve_project()

    # ---------------------------------------------------------------- fixture

    def _fixture_result(self, step: str, model: str) -> GenResult:
        path = self.fixture_dir / f"{step}.json"
        if not path.exists():
            raise RuntimeError(f"fixture mode: no fixture at {path} for step '{step}'")
        data = json.loads(path.read_text(encoding="utf-8"))
        usage = data.get("usage") or {"in": 0, "out": 0, "thinking": 0}
        result = GenResult(
            text=data.get("text", ""),
            usage=usage,
            grounded_queries=int(data.get("grounded_queries", 0)),
            url_fetches=int(data.get("url_fetches", 0)),
            sources=data.get("sources", []),
            finish_reason=data.get("finish_reason", "STOP"),
            cost_usd=0.0,
            model=data.get("model", model),
        )
        self.ledger.record(
            step=step, model=result.model, usage=result.usage,
            grounded_queries=result.grounded_queries, url_fetches=result.url_fetches,
            cost_usd=0.0, note="fixture",
        )
        return result

    # ---------------------------------------------------------------- live

    def generate(self, step: str, model: str, contents, system: str | None = None,
                 tools: list | None = None, thinking=None, max_output: int = 8192,
                 temperature: float = 0.7, json_schema: dict | None = None,
                 note: str = "") -> GenResult:
        # note: extra ledger-note text (e.g. "fallback:<model>"), used by
        # generate_with_fallback(). Not in SPEC.md's literal parameter list;
        # added so a fallback attempt's own ledger row carries the marker
        # spec asks for without a second (double-counting) record() call.
        #
        # Scope the per-run grounded-query / url-fetch caps to calls that
        # actually request that tool, so a non-grounded step (write,
        # citation-check verdicts, select) is never blocked just because an
        # earlier research call legitimately used up the run's grounding
        # budget (ai_research.py is designed to spend the whole cap).
        uses_grounding = any("googleSearch" in t for t in (tools or []))
        uses_url_fetch = any("urlContext" in t for t in (tools or []))
        self.ledger.precheck(step, uses_grounding=uses_grounding, uses_url_fetch=uses_url_fetch)

        if self.fixture_mode:
            return self._fixture_result(step, model)

        if isinstance(contents, str):
            contents = [{"role": "user", "parts": [{"text": contents}]}]

        gen_config: dict = {"maxOutputTokens": int(max_output), "temperature": temperature}
        if thinking is not None:
            gen_config["thinkingConfig"] = _thinking_config(thinking)
        if json_schema is not None:
            gen_config["responseMimeType"] = "application/json"
            gen_config["responseSchema"] = json_schema

        body: dict = {"contents": contents, "generationConfig": gen_config}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        if tools:
            body["tools"] = tools

        url = _endpoint(self.project, self.location, model)
        headers = {"Authorization": "Bearer " + _get_token()}

        try:
            status, payload = self._call_with_retries(url, headers, body, model)
            parsed = _parse_response(payload)
            cost = estimate(
                model, parsed["usage"]["in"],
                parsed["usage"]["out"] + parsed["usage"]["thinking"],
                parsed["grounded_queries"],
            )
            result = GenResult(
                text=parsed["text"], usage=parsed["usage"],
                grounded_queries=parsed["grounded_queries"], url_fetches=parsed["url_fetches"],
                sources=parsed["sources"], finish_reason=parsed["finish_reason"],
                cost_usd=cost, model=model,
            )
            self.ledger.record(
                step=step, model=model, usage=result.usage,
                grounded_queries=result.grounded_queries, url_fetches=result.url_fetches,
                cost_usd=cost, note=note,
            )
            return result
        except ModelUnavailable as e:
            self.ledger.record(
                step=step, model=model, usage={"in": 0, "out": 0, "thinking": 0},
                grounded_queries=0, url_fetches=0, cost_usd=0.0,
                note=(note + " " if note else "") + "model_unavailable",
            )
            raise e
        except Exception as e:
            self.ledger.record(
                step=step, model=model, usage={"in": 0, "out": 0, "thinking": 0},
                grounded_queries=0, url_fetches=0, cost_usd=-1.0,
                note=(note + " " if note else "") + f"error:{type(e).__name__}:{str(e)[:150]}",
            )
            raise

    def _call_with_retries(self, url: str, headers: dict, body: dict, model: str):
        last_err = None
        status, payload = None, None
        token_retry_done = False
        quota_retry_done = False
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            attempt += 1
            try:
                status, payload = _http_post_json(url, headers, body, self.config.get("timeout_s", 120))
            except Exception as e:
                last_err = f"network error: {e}"
                time.sleep(min(1.5 * attempt, 6))
                continue

            if status == 200:
                return status, payload

            msg = json.dumps(payload.get("error", payload))[:400] if isinstance(payload, dict) else str(payload)

            if (status == 401 and not token_retry_done and attempt < MAX_ATTEMPTS
                    and not os.environ.get("GEMINI_BEARER_TOKEN")):
                headers["Authorization"] = "Bearer " + _get_token(force=True)
                token_retry_done = True
                continue
            if status == 403 and not quota_retry_done and self.project:
                headers["x-goog-user-project"] = self.project
                quota_retry_done = True
                continue
            if status == 404:
                raise ModelUnavailable(f"model '{model}' not available at {self.location}: {msg}")
            if status in RETRY_STATUSES and attempt < MAX_ATTEMPTS:
                last_err = f"HTTP {status}: {msg}"
                time.sleep(min(1.5 * attempt, 6))
                continue
            raise RuntimeError(f"HTTP {status} from {model}@{self.location}: {msg}")

        raise RuntimeError(f"gave up after {MAX_ATTEMPTS} attempts: {last_err}")

    def generate_with_fallback(self, step: str, models: list, **kw) -> GenResult:
        """Try each model in order; on ModelUnavailable, move to the next and
        tag its ledger row `fallback:<model>`. Raises ModelUnavailable if all
        fail."""
        last_err: Exception | None = None
        for i, model in enumerate(models):
            extra_note = f"fallback:{model}" if i > 0 else kw.get("note", "")
            call_kw = dict(kw)
            call_kw["note"] = extra_note
            try:
                return self.generate(step, model, **call_kw)
            except ModelUnavailable as e:
                last_err = e
                continue
        raise ModelUnavailable(f"all models unavailable for step '{step}': {models} ({last_err})")

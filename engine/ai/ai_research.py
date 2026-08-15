"""Research pass: DAILY_RUN.md Step 4 ("the quality moat"), run by
`llm.model_research` with Google Search grounding in place of a human
WebSearching. Reads today's brief (data/briefs/<date>.md, written by
engine.brief.build_brief()) and makes a bounded series of grounded calls —
one per targeted research angle from prompts/v1/research_queries.md —
aggregating everything found into organized notes plus a deduplicated
source pool for ai_write to build the article from.

Contract (SPEC.md, Agent B):
    run(date_ist, slug_hint, client, cfg) -> ResearchPack

Query count is enforced by engine.ai.ledger.Ledger's per-run caps (raised
as BudgetExceeded from inside client.generate()), not by trusting the
model to stop itself — this module simply stops looping and keeps whatever
it already gathered the first time a call raises.

Deviations from SPEC.md's literal text (kept minimal, called out per the
task brief):
  * `run()` takes an optional trailing `root: Path = ROOT` kwarg, same
    testability pattern as ai_select.py/gemini_client.py/ledger.py.
  * `cfg` is the FULL config.yaml dict; `cfg["llm"]` is read internally —
    matches how engine/ai/writer_cli.py (Agent D) actually calls this
    module.
  * `ResearchPack` is defined here (SPEC only names the return type, not
    where it lives) as a plain dataclass with no behavior beyond data —
    downstream code (ai_write.py) does not import it, it reads the
    written `-research.md` / `-sources.json` files directly, so this
    dataclass is purely the in-process return value / test seam.
  * `slug_hint` may be None (writer_cli.py calls this step before a slug
    exists) — the prompt renders an explicit "no slug yet" note instead.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from ..util import ROOT

_PROMPTS = Path(__file__).resolve().parent.parent.parent / "prompts" / "v1"
PROMPT_PATH = _PROMPTS / "research_queries.md"
STYLE_PATH = _PROMPTS / "_style.md"

# The 5-10 targeted angles DAILY_RUN.md Step 4 / research_queries.md ask
# for. Fixed (not model-chosen) so the module stays deterministic — the
# ledger's per-run cap, not this list's length, is what actually limits how
# many fire on a given day.
QUERY_ANGLES = [
    ("primary_source", "Find the primary/official source(s) for the story — "
     "the vendor announcement, filing, paper or docs page. Do not settle for "
     "blogs that merely report on it."),
    ("verify_numbers", "Verify every specific number, date, or price you can "
     "find in independent coverage; note the exact source URL for each one."),
    ("india_angle", "Find the India angle: local pricing (in rupees), "
     "availability, regulation, and any Indian companies or officials "
     "involved."),
    ("global_context", "Find the global context and how competitors or peer "
     "companies are reacting."),
    ("competing_coverage", "Find what the top-ranking pages already say about "
     "this topic, so the article can add real synthesis instead of "
     "repeating them."),
    ("faq_phrasings", "Find real user question phrasings (autocomplete- or "
     "forum-style) suitable for a short FAQ section."),
]


@dataclass
class ResearchPack:
    date: str
    slug_hint: str | None
    queries_run: list = field(default_factory=list)
    sources: list = field(default_factory=list)
    notes_path: Path | None = None
    sources_path: Path | None = None
    grounded_queries_used: int = 0
    url_fetches_used: int = 0
    note: str = ""


def _primary_guess(url: str, title: str) -> bool:
    """Heuristic only (hence the field name `primary_guess`, not
    `primary`) — real per-claim primary/secondary judgment is an editorial
    call the writer makes when it fills in front-matter `sources[].primary`.
    This just biases the writer's source pool towards official domains."""
    host = urlparse(url).netloc.lower()
    t = (title or "").lower()
    official_markers = ("official", "press release", "newsroom", "govt",
                        "government", " (gov)")
    official_hosts = ("blog.google", "openai.com", "cerebras.ai",
                      "deepmind.google", "pib.gov.in")
    return (host.endswith(".gov") or ".gov." in host
            or any(host.endswith(h) or h in host for h in official_hosts)
            or any(m in t for m in official_markers))


def _render_prompt(date_ist: str, slug_hint: str | None, brief_text: str,
                   angle_instruction: str) -> str:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    style = STYLE_PATH.read_text(encoding="utf-8") if STYLE_PATH.exists() else ""
    return (template.replace("{{style}}", style)
                    .replace("{{date}}", date_ist)
                    .replace("{{slug_hint}}", slug_hint or "(none yet — topic still being scoped)")
                    .replace("{{brief}}", brief_text)
                    .replace("{{angle}}", angle_instruction))


def run(date_ist: str, slug_hint: str | None, client, cfg: dict,
        root: Path | None = None) -> ResearchPack:
    root = root or ROOT
    briefs_dir = root / "data" / "briefs"
    brief_path = briefs_dir / f"{date_ist}.md"
    if not brief_path.exists():
        raise SystemExit(f"no brief at {brief_path} — run `engine.run brief` first")
    brief_text = brief_path.read_text(encoding="utf-8")

    llm_cfg = cfg.get("llm", cfg)
    max_calls = int(llm_cfg.get("max_grounded_queries_per_run") or len(QUERY_ANGLES))
    max_calls = max(1, min(max_calls, len(QUERY_ANGLES)))

    pack = ResearchPack(date=date_ist, slug_hint=slug_hint)
    notes_sections: list[str] = []
    seen_urls: set[str] = set()

    for angle_key, angle_instruction in QUERY_ANGLES[:max_calls]:
        user_msg = _render_prompt(date_ist, slug_hint, brief_text, angle_instruction)
        try:
            res = client.generate(
                step="research",
                model=llm_cfg["model_research"],
                contents=[{"role": "user", "parts": [{"text": user_msg}]}],
                tools=[{"googleSearch": {}}],
                temperature=0.3,
                max_output=4096,
            )
        except Exception as e:  # noqa: BLE001 — BudgetExceeded/ModelUnavailable/etc: stop, keep what we have
            pack.note = (pack.note + f" | stopped at '{angle_key}': "
                        f"{type(e).__name__}: {e}").strip(" |")
            break

        pack.queries_run.append(angle_key)
        pack.grounded_queries_used += int(getattr(res, "grounded_queries", 0) or 0)
        pack.url_fetches_used += int(getattr(res, "url_fetches", 0) or 0)
        notes_sections.append(f"## {angle_key}\n\n{(res.text or '').strip()}\n")

        for s in (getattr(res, "sources", None) or []):
            url = str(s.get("url") or "").strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            title = s.get("title") or url
            pack.sources.append({
                "url": url, "title": title,
                "supports": True,  # grounding returned it for this query — the
                                    # citation gate (Agent C) makes the real,
                                    # per-claim supported/unsupported call later
                "primary_guess": _primary_guess(url, title),
            })

    briefs_dir.mkdir(parents=True, exist_ok=True)
    notes_path = briefs_dir / f"{date_ist}-research.md"
    sources_path = briefs_dir / f"{date_ist}-sources.json"
    header = f"# Research notes — {date_ist} ({slug_hint or 'no slug yet'})\n\n"
    if not notes_sections:
        header += "(no research angles completed — see `note` for why)\n"
    notes_path.write_text(header + "\n".join(notes_sections), encoding="utf-8")
    sources_path.write_text(json.dumps(pack.sources, indent=2, ensure_ascii=False),
                            encoding="utf-8")
    pack.notes_path = notes_path
    pack.sources_path = sources_path
    return pack

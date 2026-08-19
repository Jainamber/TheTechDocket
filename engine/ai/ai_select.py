"""AI-assisted topic selection: the semantic filter DAILY_RUN.md Step 2
asks a human editor to apply, run here by `llm.model_fast` against today's
mechanically-scored candidates (data/briefs/<date>-candidates.json, written
by engine.scoring.select()).

Contract (SPEC.md, Agent B):
    run(date_ist, client, cfg) -> dict

Never blocks the daily run: any failure (missing candidates file, budget
exceeded, model unavailable, malformed JSON, out-of-range pick) falls back
to the mechanical top-scored pick (rank 0) with a `note` explaining why,
and `data/briefs/<date>-ai-select.json` is always written.

Deviations from SPEC.md's literal text (kept minimal, called out per the
task brief):
  * `run()` takes an optional trailing `root: Path = ROOT` kwarg (not in
    SPEC's literal 3-arg signature) so the module is testable against a
    tmp_path tree, per SPEC's own testing instructions ("modules should
    take a root path arg ... make them testable") — matches the same
    pattern Agent A used in gemini_client.py/ledger.py. writer_cli.py
    (Agent D) calls `ai_select.run(date_ist, client, cfg)` positionally,
    which still works since `root` defaults.
  * `cfg` is the FULL config.yaml dict (as `engine.util.load_config()`
    returns it), matching how engine/ai/writer_cli.py (Agent D) actually
    calls this module — `cfg["llm"]` is read internally for model_fast.
  * On an override, this module also rewrites the `pick` (and adds
    `selection_note`) in `data/briefs/<date>-candidates.json` in place, so
    the unmodified `engine.brief.build_brief()` — which only ever reads
    `selection["pick"]` — picks up the AI's override without engine/*.py
    needing to change. This is a runtime data-file edit, not a change to
    engine module source, so it stays inside the "don't touch engine/*.py"
    hard rule.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..util import ROOT

_PROMPTS = Path(__file__).resolve().parent.parent.parent / "prompts" / "v1"
PROMPT_PATH = _PROMPTS / "select_override.md"
STYLE_PATH = _PROMPTS / "_style.md"

SELECT_SCHEMA = {
    "type": "object",
    "properties": {
        "pick_rank": {"type": "integer"},
        "reason": {"type": "string"},
        "override": {"type": "boolean"},
    },
    "required": ["pick_rank", "reason", "override"],
}


def _mechanical_fallback(reason: str) -> dict:
    return {"pick_rank": 0, "reason": reason, "override": False, "note": reason}


def _write_result(out_path: Path, result: dict) -> dict:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def _render_prompt(candidates: list, date_ist: str) -> str:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    style = STYLE_PATH.read_text(encoding="utf-8") if STYLE_PATH.exists() else ""
    return (template.replace("{{style}}", style)
                    .replace("{{date}}", date_ist)
                    .replace("{{candidates_json}}",
                             json.dumps(candidates, indent=2, ensure_ascii=False)))


def run(date_ist: str, client, cfg: dict, root: Path | None = None) -> dict:
    root = root or ROOT
    briefs_dir = root / "data" / "briefs"
    cand_path = briefs_dir / f"{date_ist}-candidates.json"
    out_path = briefs_dir / f"{date_ist}-ai-select.json"

    if not cand_path.exists():
        return _write_result(out_path, _mechanical_fallback(
            f"no candidates file at {cand_path} — mechanical pick used"))

    try:
        selection = json.loads(cand_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return _write_result(out_path, _mechanical_fallback(
            f"candidates file unreadable ({e}) — mechanical pick used"))

    candidates = selection.get("candidates") or []
    if selection.get("use_evergreen") or not candidates:
        return _write_result(out_path, _mechanical_fallback(
            "use_evergreen or no candidates — ai_select skipped, mechanical pick used"))

    llm_cfg = cfg.get("llm", cfg)
    try:
        user_msg = _render_prompt(candidates, date_ist)
        res = client.generate(
            step="select",
            model=llm_cfg["model_fast"],
            contents=[{"role": "user", "parts": [{"text": user_msg}]}],
            json_schema=SELECT_SCHEMA,
            temperature=0.2,
            max_output=1024,
        )
        data = json.loads(res.text)
        rank = int(data["pick_rank"])
        if not (0 <= rank < len(candidates)):
            raise ValueError(f"pick_rank {rank} out of range for {len(candidates)} candidates")
        result = {
            "pick_rank": rank,
            "reason": str(data.get("reason", ""))[:600],
            "override": bool(data.get("override", rank != 0)),
        }
    except Exception as e:  # noqa: BLE001 — any failure here must never block the daily run
        return _write_result(out_path, _mechanical_fallback(
            f"ai_select failed ({type(e).__name__}: {e}) — mechanical pick used"))

    _write_result(out_path, result)

    if result["override"] and 0 <= result["pick_rank"] < len(candidates):
        selection["pick"] = candidates[result["pick_rank"]]
        selection["selection_note"] = result["reason"]
        cand_path.write_text(json.dumps(selection, indent=2, ensure_ascii=False), encoding="utf-8")

    return result

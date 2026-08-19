"""AI draft of Today's Docket (DAILY_RUN Step 7.5 — ported).

Contract (SPEC.md, Agent C):
    run(date_ist, client, cfg) -> dict

Hard invariants (mirroring engine/docket.py's own doc-comment):
  * Reads ONLY `data/briefs/<date>-candidates.json` — zero new data
    collection.
  * Article-first: this module NEVER touches `data/history.json` and a
    docket failure never blocks or reverts an article publish. It is safe
    to skip entirely — `run()` never raises; a failure is reported back as
    `{"ok": False, ...}` so callers (writer_cli's best-effort step 10) can
    log and move on without changing the run's exit code.

Reuses `engine.docket.write_draft()` for the candidate-harvesting +
editorial-scaffolding template (tag suggestions, lead-item shape, per-field
comments) rather than reimplementing that logic, per the task brief. The
model (model_fast + prompts/v1/docket_entry.md) is given that template plus
the raw candidates JSON and asked to return a filled `items[]` array
(json_schema-forced); this module then serializes that into the exact YAML
shape `engine.docket.parse_docket()` / `DocketGateRunner` expect at
`data/docket/<date>.md`, and self-validates by round-tripping it through
`parse_docket()` before declaring success.

Deviation from SPEC.md: `run()` gains an optional trailing `root: Path`
kwarg (default `engine.util.ROOT`) for testability; writer_cli.py calls it
positionally with 3 args, which still works. `engine.docket.write_draft()`
itself has no root parameter (it always resolves paths from its own
module-level `ROOT`/`DOCKET_DIR`), so tests that need isolation monkeypatch
`engine.docket.ROOT` / `engine.docket.DOCKET_DIR` alongside `root=` — see
tests/test_citation_gate.py's sibling ai_docket test for the pattern. In
real (default-root) use this is a no-op: `engine.docket.ROOT` already
equals `engine.util.ROOT`.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from ..docket import parse_docket, write_draft
from ..util import ROOT

DOCKET_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "hub": {"type": "string"},
        "lead": {"type": "boolean"},
        "rank": {"type": "integer"},
        "tag": {"type": "string"},
        "pick": {"type": "boolean"},
        "headline": {"type": "string"},
        "dek": {"type": "string"},
        "why": {"type": "string"},
        "counterpoint": {"type": "string"},
        "stat_line": {"type": "string"},
        "community_read": {"type": "string"},
        "community_attr": {"type": "string"},
        "save_worthy": {"type": "boolean"},
        "url": {"type": "string"},
        "source": {"type": "string"},
    },
    "required": ["hub", "rank", "headline", "dek", "url", "source"],
}
DOCKET_SCHEMA = {
    "type": "object",
    "properties": {"items": {"type": "array", "items": DOCKET_ITEM_SCHEMA}},
    "required": ["items"],
}


def _load_prompt(root: Path) -> str:
    path = root / "prompts" / "v1" / "docket_entry.md"
    if not path.exists():
        raise FileNotFoundError(f"missing prompt template: {path}")
    return path.read_text(encoding="utf-8")


def _load_style(root: Path) -> str:
    path = root / "prompts" / "v1" / "_style.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def run(date_ist: str, client, cfg: dict, root: Path = ROOT) -> dict:
    """Best-effort. Never raises. Returns
    {"ok": bool, "path": str|None, "note": str}."""
    root = Path(root)
    try:
        cand_path = root / "data" / "briefs" / f"{date_ist}-candidates.json"
        if not cand_path.exists():
            return {"ok": False, "path": None,
                    "note": f"no candidates file for {date_ist} — nothing to draft"}
        candidates = json.loads(cand_path.read_text(encoding="utf-8"))

        # Reuse engine.docket's own harvesting/tag-suggestion/template logic
        # instead of reimplementing it (task brief).
        draft_path = write_draft(date_ist)
        template = draft_path.read_text(encoding="utf-8")

        model = (cfg.get("llm") or {}).get("model_fast")
        if not model:
            return {"ok": False, "path": None, "note": "cfg['llm']['model_fast'] missing"}

        prompt_template = _load_prompt(root)
        style = _load_style(root)
        prompt = (prompt_template.replace("{{style}}", style)
                                  .replace("{{draft_template}}", template)
                                  .replace("{{candidates_json}}",
                                           json.dumps(candidates, ensure_ascii=False)))
        prompt += (f"\n\n---\nDRAFT TEMPLATE (editorial scaffolding, do not "
                   f"copy the comment lines verbatim):\n{template}\n\n"
                   f"CANDIDATES JSON:\n{json.dumps(candidates, ensure_ascii=False)}\n")

        result = client.generate(step="docket", model=model, contents=prompt,
                                 json_schema=DOCKET_SCHEMA, temperature=0.4)
        data = json.loads(result.text)
        items = data.get("items") or []
        if not items:
            return {"ok": False, "path": None, "note": "model returned zero items"}

        out_path = draft_path.parent / f"{date_ist}.md"
        fm = {"date": date_ist, "pool": len(candidates.get("candidates") or []),
              "items": items}
        out_path.write_text(
            "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                                     default_flow_style=None, width=100)
            + "---\n", encoding="utf-8")

        parse_docket(out_path)  # self-check: must round-trip as valid YAML
        return {"ok": True, "path": str(out_path), "note": f"{len(items)} items"}
    except Exception as e:  # noqa: BLE001 — article-first: never raise
        return {"ok": False, "path": None, "note": f"{type(e).__name__}: {e}"}

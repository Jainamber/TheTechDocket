"""AI social caption export (DAILY_RUN social step — ported).

Contract (SPEC.md, Agent C):
    run(date_ist, client, cfg) -> dict

Reads the day's already-published docket data file
(`data/docket/<date>.md`, via `engine.docket.parse_docket` — reused, not
reimplemented) and asks model_fast + prompts/v1/social_caption.md for an
Instagram-ready caption, writing it to `data/social/<date>.md` (the
directory is gitignored per .gitignore's `data/social/` rule — it's an
export/deliverable, not site state, same as `engine.run social`'s image
carousel output).

Safe-to-skip, article- and docket-first: this module never touches the
article, the docket data file, or `data/history.json`, and `run()` never
raises — a missing docket file, a disabled `social.enabled` config flag, or
any model/parse error all come back as `{"ok": False, ...}` so writer_cli's
best-effort step 10 can log and move on without changing the run's exit
code.

Deviation from SPEC.md: `run()` gains an optional trailing `root: Path`
kwarg (default `engine.util.ROOT`) for testability; writer_cli.py calls it
positionally with 3 args, which still works.
"""
from __future__ import annotations

from pathlib import Path

from ..docket import parse_docket
from ..util import ROOT


def _load_prompt(root: Path) -> str:
    path = root / "prompts" / "v1" / "social_caption.md"
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
        scfg = cfg.get("social") or {}
        if not scfg.get("enabled", True):
            return {"ok": False, "path": None, "note": "social export disabled in config"}

        docket_path = root / "data" / "docket" / f"{date_ist}.md"
        if not docket_path.exists():
            return {"ok": False, "path": None,
                    "note": f"no docket data file for {date_ist} — nothing to export"}
        docket = parse_docket(docket_path)

        model = (cfg.get("llm") or {}).get("model_fast")
        if not model:
            return {"ok": False, "path": None, "note": "cfg['llm']['model_fast'] missing"}

        import json
        prompt_template = _load_prompt(root)
        style = _load_style(root)
        docket_json = json.dumps(
            {k: v for k, v in docket.items() if not k.startswith("_")},
            ensure_ascii=False)
        prompt = (prompt_template.replace("{{style}}", style)
                                  .replace("{{docket_json}}", docket_json))
        prompt += f"\n\n---\nTODAY'S DOCKET JSON:\n{docket_json}\n"

        result = client.generate(step="social", model=model, contents=prompt,
                                 temperature=0.6)
        if not (result.text or "").strip():
            return {"ok": False, "path": None, "note": "model returned empty caption"}

        out_dir = root / "data" / "social"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{date_ist}.md"
        out_path.write_text(result.text, encoding="utf-8")
        return {"ok": True, "path": str(out_path), "note": ""}
    except Exception as e:  # noqa: BLE001 — safe-to-skip: never raise
        return {"ok": False, "path": None, "note": f"{type(e).__name__}: {e}"}

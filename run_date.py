import sys
import traceback
from pathlib import Path

root = Path(r"C:\NewStartsNov\TheTechDocket")
sys.path.insert(0, str(root))

from engine.ai.writer_cli import load_config, _build_client_and_ledger, Runner, _slug_from_article

date_ist = sys.argv[1] if len(sys.argv) > 1 else "2026-11-09"
print(f"Starting step-by-step run for {date_ist}...", flush=True)

try:
    cfg = load_config()
    client, ledger = _build_client_and_ledger(cfg, root, False)
    r = Runner(root)
    
    print("Step 1: inbox", flush=True)
    inbox_path = root / "data" / "inbox" / f"{date_ist}.json"
    print(f"Inbox exists: {inbox_path.exists()}", flush=True)
    
    print("Step 2: select", flush=True)
    rc = r.engine_run("select", "--date", date_ist)
    print(f"select returncode: {rc.returncode}", flush=True)
    
    print("Step 3: ai_select", flush=True)
    sel = r.ai_select(date_ist, client, cfg)
    print(f"ai_select: {sel.get('pick_rank')}, {sel.get('override')}", flush=True)
    
    print("Step 4: brief", flush=True)
    rc = r.engine_run("brief", "--date", date_ist)
    print(f"brief returncode: {rc.returncode}", flush=True)
    
    print("Step 5: ai_research", flush=True)
    pack = r.ai_research(date_ist, None, client, cfg)
    print(f"ai_research done: {len(pack.sources)} sources", flush=True)
    
    print("Step 6: ai_write", flush=True)
    art_path = r.ai_write(date_ist, client, cfg)
    slug = _slug_from_article(art_path)
    print(f"ai_write done: {slug}", flush=True)

    print("Step 7: citation_gate", flush=True)
    cit_ok, cit_feedback = r.citation_gate(date_ist, slug, client, cfg)
    print(f"citation_gate: {cit_ok}", flush=True)
    if not cit_ok:
        print(f"Retrying ai_write with citation feedback...", flush=True)
        art_path = r.ai_write(date_ist, client, cfg, retry_feedback=cit_feedback, reuse_slug=slug)
        slug = _slug_from_article(art_path)
        cit_ok, cit_feedback = r.citation_gate(date_ist, slug, client, cfg)
        print(f"citation_gate after retry: {cit_ok}", flush=True)

    print("Step 8: build", flush=True)
    r.engine_run("build")

    print("Step 9: gate", flush=True)
    gate_ok, gate_feedback = r.gate(slug, date_ist)
    print(f"gate: {gate_ok}", flush=True)

    if cit_ok and gate_ok:
        from engine.ai.writer_cli import _record_entry, _write_run_state
        _record_entry(date_ist, slug, root, cfg)
        print(f"RECORDED to history.json: {date_ist} -> {slug}", flush=True)
        _write_run_state(root, date_ist, slug, "ok", True)
        
        print("Step 10: docket", flush=True)
        try:
            r.ai_docket(date_ist, client, cfg)
            print("docket: ok", flush=True)
        except Exception as e:
            print(f"docket skipped: {e}", flush=True)

        print("Step 11: social", flush=True)
        try:
            r.ai_social(date_ist, client, cfg)
            print("social: ok", flush=True)
        except Exception as e:
            print(f"social skipped: {e}", flush=True)

        print("Step 12: share", flush=True)
        try:
            from engine.share import build_share_kit
            build_share_kit(slug=slug, date_str=date_ist, open_browser=False)
            print("share: ok", flush=True)
        except Exception as e:
            print(f"share skipped: {e}", flush=True)

        print(f"ALL STEPS COMPLETED FOR {date_ist}!", flush=True)
    else:
        print(f"GATES FAILED for {slug}: cit_ok={cit_ok}, gate_ok={gate_ok}", flush=True)

except BaseException as e:
    print(f"FAILED AT: {type(e).__name__}: {e}", flush=True)
    traceback.print_exc()





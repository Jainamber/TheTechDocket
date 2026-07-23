"""Content engine CLI.

  python -m engine.run fetch                # pull trend data -> data/inbox/
  python -m engine.run select               # score candidates -> pick
  python -m engine.run brief                # write today's article brief
  python -m engine.run build                # build the static site -> docs/
  python -m engine.run gate --slug SLUG     # run compliance/SEO gates
  python -m engine.run publish --slug SLUG  # gate + history + git commit/push
  python -m engine.run publish --slug SLUG --no-push
  python -m engine.run docket-draft         # pre-draft Today's Docket from candidates
  python -m engine.run docket [--date D]    # run D-gates on the built docket
  python -m engine.run docket-publish [--date D] [--no-push]
  python -m engine.run social [--date D]    # IG carousel slides + caption -> data/social/
  python -m engine.run status               # engine state overview
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .util import ROOT, all_articles, load_config, load_history, today_str


def main(argv=None):
    ap = argparse.ArgumentParser(prog="engine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch")
    sel = sub.add_parser("select")
    sel.add_argument("--inbox", type=Path, default=None)
    sub.add_parser("brief")
    sub.add_parser("build")
    g = sub.add_parser("gate")
    g.add_argument("--slug", required=True)
    p = sub.add_parser("publish")
    p.add_argument("--slug", required=True)
    p.add_argument("--no-push", action="store_true")
    sub.add_parser("feedback")
    dd = sub.add_parser("docket-draft")
    dd.add_argument("--date", default=None)
    dg = sub.add_parser("docket")
    dg.add_argument("--date", default=None)
    dp = sub.add_parser("docket-publish")
    dp.add_argument("--date", default=None)
    dp.add_argument("--no-push", action="store_true")
    so = sub.add_parser("social")
    so.add_argument("--date", default=None)
    sub.add_parser("status")
    args = ap.parse_args(argv)

    if args.cmd == "fetch":
        from . import fetchers
        box = fetchers.fetch_all()
        path = fetchers.write_inbox(box)
        ok = sum(1 for v in box["sources_status"].values() if v == "ok")
        print(f"inbox: {path} ({ok}/{len(box['sources_status'])} sources ok)")

    elif args.cmd == "select":
        from .scoring import select
        res = select(args.inbox)
        pick = res["pick"]
        print(json.dumps({"pick": pick["title"] if pick else None,
                          "score": pick["score"] if pick else None,
                          "use_evergreen": res["use_evergreen"],
                          "alternates": [c["title"] for c in
                                         res["candidates"][1:6]]},
                         indent=2, ensure_ascii=False))

    elif args.cmd == "brief":
        from .brief import build_brief
        day = today_str()
        sel_path = ROOT / "data" / "briefs" / f"{day}-candidates.json"
        inbox_path = ROOT / "data" / "inbox" / f"{day}.json"
        if not sel_path.exists():
            sys.exit("run `select` first")
        selection = json.loads(sel_path.read_text(encoding="utf-8"))
        inbox = json.loads(inbox_path.read_text(encoding="utf-8")) \
            if inbox_path.exists() else {}
        out = build_brief(selection, inbox)
        print(f"brief: {out}")

    elif args.cmd == "build":
        from .build import build_site
        build_site()

    elif args.cmd == "gate":
        from .gates import run_gates
        rep = run_gates(args.slug)
        sys.exit(0 if rep["passed"] else 1)

    elif args.cmd == "publish":
        from .publish import publish
        publish(args.slug, push=not args.no_push)

    elif args.cmd == "feedback":
        from .feedback import build_insights
        build_insights()

    elif args.cmd == "docket-draft":
        from .docket import write_draft
        print(f"docket draft: {write_draft(args.date)}")

    elif args.cmd == "docket":
        from .docket import run_docket_gates
        rep = run_docket_gates(args.date)
        sys.exit(0 if rep["passed"] else 1)

    elif args.cmd == "docket-publish":
        from .docket import docket_publish
        docket_publish(args.date, push=not args.no_push)

    elif args.cmd == "social":
        # Phase B (proposal 2026-07-23): render the day's docket as an
        # Instagram-ready carousel. Output is gitignored — the owner posts
        # manually; skipping this step forever is fine.
        from . import images
        from .build import docket_context
        from .docket import DOCKET_DIR, parse_docket
        cfg = load_config()
        scfg = cfg.get("social") or {}
        if not scfg.get("enabled", True):
            sys.exit("social export disabled in config.yaml")
        day = args.date or today_str()
        path = DOCKET_DIR / f"{day}.md"
        if not path.exists():
            sys.exit(f"no docket data file for {day} — nothing to export")
        ctx = docket_context(cfg, parse_docket(path))
        outdir = ROOT / "data" / "social" / day
        files = images.generate_carousel(
            day, ctx["date_human"], ctx["entries"], cfg["site"]["base_url"],
            outdir, int(scfg.get("slide_w", 1080)),
            int(scfg.get("slide_h", 1350)), int(scfg.get("max_slides", 20)))
        print(f"social: {len(files)} slides + caption.txt -> {outdir}")

    elif args.cmd == "status":
        cfg = load_config()
        arts = all_articles()
        hist = load_history()
        day = today_str()
        print(json.dumps({
            "site": cfg["site"]["name"],
            "topic": cfg["topic"]["name"],
            "articles_in_repo": len(arts),
            "published_total": len(hist["published"]),
            "last_published": hist["published"][-1] if hist["published"] else None,
            "today_inbox": (ROOT / "data" / "inbox" / f"{day}.json").exists(),
            "today_brief": (ROOT / "data" / "briefs" / f"{day}.md").exists(),
            "today_article": any(str(a.get("date")) == day for a in arts),
            "today_docket": (ROOT / "data" / "docket" / f"{day}.md").exists(),
        }, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()

# AI-PIPELINE — Operating Manual for the Gemini (Vertex) Writing Pipeline

Ported from `DAILY_RUN.md` (the claude.ai session manual) on 2026-08-15.
**During the parallel-run period, `DAILY_RUN.md` remains the manual for the
claude.ai scheduled session; this file documents the scripted replacement.**
Nothing here changes editorial policy or the gates — it is the same
seven-and-a-half-step process, executed by `engine/ai/*.py` calling Gemini
(Vertex) instead of a human-in-the-loop cloud session. At cutover (the
`TTD_PIPELINE_MODE: live` flag flips and stays flipped, see the workflow
section below), this document becomes the authoritative operating manual
and `DAILY_RUN.md` is kept only as historical/provenance reference.

## What runs, and in what order

`python -m engine.ai.writer_cli --all` runs, once per IST day:

0. **STOP guard** — if `data/history.json` already has an entry dated
   today (IST), print `STOP` and exit `3`. Prevents a second publish on the
   same day if the schedule fires twice. `--skip-stop-guard` bypasses this
   — staging/smoke runs only, never for a live cutover run.
1. Ensure `data/inbox/<date>.json` exists; else `engine.run fetch`.
2. `engine.run select` (mechanical scoring) → `engine.ai.ai_select` (an LLM
   sanity pass over the scorer's pick, `model_fast`, can override rank 0).
3. `engine.run brief` → `engine.ai.ai_research` (grounded Gemini calls,
   `googleSearch` tool, up to `llm.max_grounded_queries_per_run` queries).
4. `engine.ai.ai_write` — one `model_writer` call (high-thinking) producing
   the complete article file, parsed and validated.
5. `engine.run build` → `engine.run gate`. On a HARD gate failure, the
   report feeds back into one more `ai_write` call (`retry_feedback=...`),
   then rebuild + re-gate.
6. `engine.ai.citation_gate` — one `urlContext` check per cited source.
   Shares the SAME retry budget as step 5 (`llm.max_retry_rewrites` total,
   not per-gate-kind) — a citation failure can also trigger one more
   `ai_write` retry if the budget hasn't been spent yet on a compliance-gate
   retry.
7. `engine.ai.ai_docket` + `engine.ai.ai_social` — best-effort. A failure
   here is logged and never changes the run's exit code and never touches
   the already-written, already-gated article (article-first invariant).

`writer_cli` never runs a git command. Publishing stays `engine.run
publish` (local) or the CI PR rail (`.github/workflows/daily-pipeline.yml`,
Agent E) — the writer only produces a gated, citation-checked article on
disk plus a cost ledger row per LLM call.

## Running locally (ADC)

```bash
gcloud auth login
gcloud auth application-default login
export TTD_GCP_PROJECT=<your-gcp-project-id>       # never committed to the repo
pip install -r requirements.txt -r requirements-ai.txt
python -m engine.ai.writer_cli --all
```

`GeminiClient` resolves the project id at runtime only, in this order:
env `TTD_GCP_PROJECT` → `~/.ttd/vertex.json` (`{"project": "..."}`) → a
clear error. It never reads a project id or credential out of a repo file
— this repo is public.

Token resolution order (also runtime-only): env `GEMINI_BEARER_TOKEN` →
(if `GOOGLE_APPLICATION_CREDENTIALS` is set) a minted service-account
token → `gcloud auth application-default print-access-token`, cached at
`~/.ttd/token_cache.json` for ~40 minutes.

## Running in CI

The `VERTEX_SA_KEY` repo secret (a service-account JSON key, never a
project id or key committed to any file) is written to a temp file by the
workflow and exported as `GOOGLE_APPLICATION_CREDENTIALS` before
`writer_cli` runs. This is the only path that imports `google-auth`
(`requirements-ai.txt`); local ADC runs never need that package installed.
`TTD_GCP_PROJECT` is set the same way as local runs, as a repo/environment
variable — never hardcoded in `config.yaml` or any other tracked file.

## Fixture mode ($0, no network, no gcloud)

```bash
export TTD_AI_FIXTURE=1                 # or: writer_cli --fixture
python -m engine.ai.writer_cli --all --fixture --skip-stop-guard
```

`GeminiClient` auto-enables fixture mode when env `TTD_AI_FIXTURE=1` is
set or a `fixture_dir` is passed (`writer_cli --fixture` passes
`tests/fixtures/ai/`). In fixture mode every `generate()` call reads a
canned `GenResult` from `tests/fixtures/ai/{step}.json` instead of making
an HTTP request; the ledger still records the call, at `cost_usd: 0` with
a `fixture` note, so retry-budget and cost-reporting logic can be tested
end to end. `--skip-stop-guard` is typically combined with `--fixture` for
staging/smoke runs against a date that's already in `history.json`.

All tests under `tests/` run this way — zero live network calls to
Gemini, zero `gcloud` invocations, by hard rule.

## Budget caps

Everything in the `llm:` block of `config.yaml` is a CODE-enforced cap,
not a suggestion:

- `daily_budget_usd` (default `2.00`) — `Ledger.precheck()` raises
  `BudgetExceeded` before any HTTP call once today's (IST) recorded spend
  reaches this. Unpriced-model rows record cost `-1` (`UNKNOWN`, never
  silently `0`) and count as a pessimistic `$0.05` placeholder toward this
  total — see `engine/ai/pricing.py` / `engine/ai/ledger.py`.
- `max_grounded_queries_per_run` (default `12`) and
  `max_url_fetches_per_run` (default `25`) — per-run counters enforced by
  the ledger, independent of the daily dollar cap, so a single pathological
  run can't burn the whole day's grounding allowance.
- `max_retry_rewrites` (default `1`) — the single shared retry budget for
  steps 5 and 6 above (gate failures + citation failures combined).

A `BudgetExceeded` or `ModelUnavailable` (or any other unexpected
exception) anywhere in the pipeline is caught by `writer_cli` and reported
as exit code `2` ("infra error") — it is never allowed to leave a
half-written article or corrupt `history.json` (the writer never touches
`history.json`; only `engine.run publish` does).

## Model matrix + fallbacks

Verified live against the owner's GCP project, location `global`,
2026-08-15 (see `SPEC.md`):

| role            | model                  | fallback(s)        |
|-----------------|------------------------|---------------------|
| writer          | `gemini-3.5-flash`     | `gemini-2.5-pro`    |
| research        | `gemini-3.5-flash`     | `gemini-2.5-flash`  |
| fast (select/citations/docket/social) | `gemini-2.5-flash-lite` | — |

`gemini-3.5-pro` / `gemini-3.1-pro` are **not served** on this project
(404) — do not reference them outside a fallback-probe comment.
`GeminiClient.generate_with_fallback(step, models, **kw)` tries each model
in order on `ModelUnavailable`, records a `fallback:<model>` note in the
ledger, and only raises once every model in the list has failed.

## Staging → live cutover

Controlled entirely by the GitHub Actions repo variable
`TTD_PIPELINE_MODE` (Agent E's `daily-pipeline.yml`), not by anything in
this codebase:

- **`staging`** (default/absent) — `writer_cli --all --skip-stop-guard`
  runs against a `staging/daily-<date>` branch and opens a **draft** PR
  that is never auto-merged. Safe to run in parallel with the claude.ai
  `DAILY_RUN.md` session every day — nothing in staging mode touches
  `main` or `history.json` on `main`.
- **`live`** — `writer_cli --all` runs normally (STOP guard active),
  pushes to `agent/daily-<date>`, opens a PR with auto-merge enabled, and
  merge only happens once the separate non-LLM `gate-check` job passes on
  the PR ref. This is the point at which `DAILY_RUN.md` stops being the
  daily manual and this file takes over.

Flip the variable only after several staging-mode PRs have been reviewed
and look right — this document does not set the flag, a human does.

At the moment of cutover (flipping `TTD_PIPELINE_MODE` to `live`), also:

- **Disable `fetch-trends.yml`'s cron** — comment out its `schedule:`
  trigger (leave `workflow_dispatch` so it can still be run by hand).
  `daily-pipeline.yml`'s "Fetch trend data" step already folds in the same
  `engine.run fetch` call, so once live, two independent writers committing
  to `main` around the same time would race/conflict. `fetch-trends.yml`
  only needs to keep running unchanged during the staging/parallel-run
  period, to feed the claude.ai `DAILY_RUN.md` session.
- **Periodically prune stale staging branches/draft PRs** —
  `staging/daily-<date>` branches and their draft PRs accumulate one per
  day during parallel-run and are never auto-merged or auto-deleted; sweep
  them (close the draft PRs, delete the branches) on some regular cadence
  so they don't pile up indefinitely once live mode is the sole daily run.

## Provenance

Every prompt in `prompts/v1/*.md` is a direct port of the corresponding
step in `DAILY_RUN.md` (front-matter contract v1.2, primary-source rule,
India+US audience, gate-driven quality bar) — see each prompt file's
`<!-- v1 | ported from DAILY_RUN.md 2026-08-15 | ... -->` header for the
exact mapping. `writer_cli` itself is a line-for-line port of
`DAILY_RUN.md` Steps 0–7.6, minus the human editorial judgment calls
(topic override, source vetting) which are now Gemini calls with an
explicit override/no-fabrication contract instead of a person reading the
brief.

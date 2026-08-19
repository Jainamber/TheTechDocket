# Owner actions — off-Claude migration (2026-08-19)

Five items from the plan. Status + exact steps. Items 1, 3, 5 need YOUR browser
session or a credential only you should handle; item 2 is DONE; item 4 is
deliberately deferred to cutover (see why).

## 1. ⏰ Export the live claude.ai routine prompts (UNRECOVERABLE after sub ends)

Tab already open in Chrome: https://claude.ai/code/scheduled (the routines are
under the sidebar "Scheduled" section, NOT the routines list). For EACH of the
two routines (daily 06:30 IST publish, 15:00 IST retry):

1. Open the routine → copy its FULL prompt text (Ctrl+A in the prompt box,
   Ctrl+C) + note: schedule, attached repo, any project/instructions it uses.
2. Paste into `docs-src/routine-prompts-2026-08.md` in this repo (create the
   folder; one `## 06:30 IST publish` and one `## 15:00 IST retry` section,
   verbatim — do NOT tidy it). If either routine references a claude.ai
   Project with custom instructions, copy those too under `## Project
   instructions`.
3. Commit + push to main (tiny docs-only commit; the engine ignores it):
   ```bash
   cd C:/oProjectsHigh/TheTechDocket && git checkout main && git pull -q && git add docs-src/ && git commit -m "docs: export live claude.ai routine prompts (verbatim, 2026-08)" && git push
   ```
   Then `git checkout feat/gemini-pipeline` to return.

Why verbatim: recon could not verify DAILY_RUN.md matches the live prompts;
five weeks of owner tuning may exist only on claude.ai. The diff vs
DAILY_RUN.md is the first thing the next build session folds into prompts/v1/.

## 2. Merge PR #1 (covers v3) — ✅ DONE (merged 2026-08-17 02:06 UTC by you)

Live site rebuilt after; nothing left to do.

## 3. Vertex service-account key → repo secret `VERTEX_SA_KEY`

A credential — you create and paste it; Claude never handles the value.
PowerShell (gcloud is installed and ADC-authed on this machine; project id is
in `~/.ttd/vertex.json`):

```powershell
$P = (Get-Content "$HOME\.ttd\vertex.json" | ConvertFrom-Json).project
$SA = "ttd-pipeline-ci@$P.iam.gserviceaccount.com"
gcloud iam service-accounts create ttd-pipeline-ci --project $P --display-name "TheTechDocket CI writer"
gcloud projects add-iam-policy-binding $P --member "serviceAccount:$SA" --role roles/aiplatform.user
gcloud iam service-accounts keys create "$HOME\.ttd\ttd-pipeline-ci.json" --iam-account $SA --project $P
gh secret set VERTEX_SA_KEY --repo Jainamber/TheTechDocket < "$HOME\.ttd\ttd-pipeline-ci.json"
```

Least privilege: `roles/aiplatform.user` only (generateContent; nothing else).
Key file stays in `~/.ttd/` (outside every repo; `.ttd` is never committed).
Set a GCP budget alert on the project at ~$40/month (Billing → Budgets) —
the pipeline's own breaker is $2/day but belt-and-suspenders.

Verify: `gh secret list --repo Jainamber/TheTechDocket` shows VERTEX_SA_KEY +
GOATCOUNTER_TOKEN.

## 4. Branch protection + auto-merge — DEFERRED TO CUTOVER (on purpose)

NOT done today, and should not be: the claude.ai routine still pushes
DIRECTLY to `main` every morning. A protection rule requiring the
`gate-check` status would block tomorrow's publish. This flips ONLY when
PR #2 merges AND the routines are turned off, in this order:

```bash
# at cutover, after PR #2 merge + routines paused:
gh api -X PATCH repos/Jainamber/TheTechDocket -f allow_auto_merge=true -f delete_branch_on_merge=true
gh api -X PUT repos/Jainamber/TheTechDocket/branches/main/protection \
  --input - <<'EOF'
{"required_status_checks":{"strict":false,"contexts":["gate-check"]},
 "enforce_admins":false,"required_pull_request_reviews":null,"restrictions":null,
 "allow_force_pushes":false,"allow_deletions":false}
EOF
gh variable set TTD_PIPELINE_MODE --body live --repo Jainamber/TheTechDocket
```
(Until then the staging cron opens draft PRs only; `TTD_PIPELINE_MODE` unset
= staging. Those need no protection rule.)

## 5. Revoke the old PAT

Browser only (GitHub has no API to list/delete classic PATs):
https://github.com/settings/tokens → find the token the old routine used
(created ~July 2026, scope repo) → Delete. Nothing uses it anymore: the
routines were PAT-scrubbed 08-09 (injected-credential push), the pipeline
uses GITHUB_TOKEN, this machine uses gh OAuth.
After deleting, also delete the local copy:
`C:\oProjectsHigh\NewContent\_secrets\credentials.txt.txt` (contains that
PAT; confirm nothing else is in it first — it's 291 bytes).

---
*Written by the 2026-08-19 session after both browser surfaces (Chrome
extension + Browser pane) failed to inject scripts into any page — not a
site block, a session-level extension fault. Re-try Chrome takeover in a
fresh session if you'd rather Claude drive items 1 and 5.*

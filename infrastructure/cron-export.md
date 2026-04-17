# Cron Jobs Export

This file is manually maintained. Update it whenever cron jobs are added or changed.

**Last exported:** 2026-04-17

---

## Active Jobs

### nightly-git-push
- **ID:** c152c115-cd39-4ec1-a7ed-390f25788b1e
- **Schedule:** `0 3 * * *` (3:00 AM CT every night)
- **What it does:** `git add -A && git commit && git push` — backs up all workspace changes to GitHub
- **Delivery:** Silent (no notification unless error)
- **Added:** 2026-04-17

---

## Format (for re-adding after restore)

```
openclaw cron add \
  --name "nightly-git-push" \
  --schedule "0 3 * * *" \
  --tz "America/Chicago" \
  --message "Run a silent git backup of Mira's workspace: cd /Users/mira/Documents/Novian_Intelligence && git add -A && git diff --cached --quiet || (git commit -m 'chore: nightly auto-backup' && git push). Only report back if there's an error."
```

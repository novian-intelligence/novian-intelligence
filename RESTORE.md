# RESTORE.md — Mira's Recovery Playbook

If the VM is gone, this doc gets Mira back up and running in ~20-30 minutes.

---

## Step 1 — Provision a New VM

- macOS Sequoia via Tart (or any macOS/Linux environment)
- Recommended: 6 vCPU, 12GB RAM minimum
- Install Xcode Command Line Tools: `xcode-select --install`

---

## Step 2 — Install Core Dependencies

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Git (comes with Xcode CLT, but verify)
git --version

# GitHub CLI
brew install gh

# Node.js (required for OpenClaw)
brew install node

# OpenClaw
npm install -g openclaw
```

---

## Step 3 — Restore the Workspace from GitHub

```bash
mkdir -p /Users/mira/Documents
cd /Users/mira/Documents
gh auth login   # SSH, GitHub.com, Login with browser
git clone git@github.com:novian-intelligence/novian-intelligence.git Novian_Intelligence
```

This restores:
- ✅ SOUL.md, MEMORY.md, AGENTS.md, IDENTITY.md, USER.md
- ✅ All daily memory files (memory/)
- ✅ NI website (novian_intelligence_website/)
- ✅ Backlog, docs, scratch files

---

## Step 4 — Configure OpenClaw

```bash
openclaw init
```

Point the workspace at `/Users/mira/Documents/Novian_Intelligence`

Set model to: `anthropic/claude-sonnet-4-6`

Re-add any cron jobs from `infrastructure/cron-export.md` (see that file for saved job configs).

---

## Step 5 — Verify Mira is Oriented

Start a new OpenClaw session. Mira should:
1. Read SOUL.md, USER.md, MEMORY.md automatically on startup
2. Know who she is and who Andrei is
3. Be ready to pick up where she left off

---

## What You'll Need to Re-do Manually

| Item | How |
|------|-----|
| SSH key for GitHub | Re-run `gh auth login` (step 3 above) |
| OpenClaw cron jobs | Re-add from `infrastructure/cron-export.md` |
| API keys (ElevenLabs, Netlify, etc.) | Re-add to TOOLS.md from your password manager |
| Netlify site connection | Re-run `netlify link` or reconnect via Netlify UI |
| Any installed Homebrew apps | Re-install as needed |

---

## Estimated Recovery Time

| Scenario | Time |
|----------|------|
| VM gone, GitHub intact | ~20-30 min |
| VM gone, GitHub gone | ~1-2 hours (restore from last local backup) |
| Both gone | Start fresh (MEMORY.md is the soul — recreate from there) |

---

*Last updated: 2026-04-17*
*This file is committed to GitHub — it survives with everything else.*

# Migration: VM → Native Mac Mini
*Written by Mira — April 29, 2026*
*Purpose: Move our setup from the VM to native macOS, clean slate, nothing lost.*

---

## Before You Start

**Do NOT delete the VM until migration is confirmed working.**
The VM is the backup. Keep it running until Mira is fully online natively.

---

## Phase 1 — Backup Everything from the VM (Do this first)

On the VM, zip the entire NI workspace:
```bash
cd /Users/mira/Documents
zip -r NI_BACKUP_$(date +%Y%m%d).zip Novian_Intelligence/
```

Also backup OpenClaw config:
```bash
zip -r OPENCLAW_BACKUP_$(date +%Y%m%d).zip ~/.openclaw/
```

Copy both zip files to a safe location (external drive, iCloud, etc.)

---

## Phase 2 — Set Up Native Mac Mini

### 2a. Create the "Mira" user account
1. System Settings → Users & Groups → Add Account
2. Name: Mira Novian
3. Account name: mira
4. Set a strong password (document it!)
5. Standard account (not admin — safer)

### 2b. Create the "Lab" user account
1. Same process
2. Name: Andrei Lab
3. Account name: lab
4. This is for experiments — Perplexity, computer use, new tools
5. Nothing from Lab should touch Mira's account

### 2c. Enable Fast User Switching
System Settings → Control Center → Fast User Switching → Show in Menu Bar

---

## Phase 3 — Install OpenClaw on Mira Account

Log into the Mira account, then:

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Install OpenClaw (PINNED VERSION — DO NOT UPDATE TO 2026.4.26)
npm install -g openclaw@2026.4.21

# Verify
openclaw --version
# Should show: OpenClaw 2026.4.21
```

---

## Phase 4 — Port Mira's Files

```bash
# Create workspace
mkdir -p ~/Documents/Novian_Intelligence

# Copy from VM backup (or directly from VM if on same network)
# Unzip NI_BACKUP to ~/Documents/Novian_Intelligence/
```

Critical files that MUST be present before running OpenClaw:
- `~/Documents/Novian_Intelligence/SOUL.md`
- `~/Documents/Novian_Intelligence/MEMORY.md`
- `~/Documents/Novian_Intelligence/USER.md`
- `~/Documents/Novian_Intelligence/AGENTS.md`
- `~/Documents/Novian_Intelligence/NI_CULTURE.md`
- `~/Documents/Novian_Intelligence/TOOLS.md`
- `~/Documents/Novian_Intelligence/memory/` (entire folder)

---

## Phase 5 — Configure OpenClaw (MINIMAL — nothing extra)

Run the wizard:
```bash
openclaw configure
```

Set workspace to: `/Users/mira/Documents/Novian_Intelligence`

Then manually set the config — **only what we need:**

`~/.openclaw/openclaw.json` should contain:
```json
{
  "agents": {
    "defaults": {
      "workspace": "/Users/mira/Documents/Novian_Intelligence",
      "models": {
        "anthropic/claude-sonnet-4-6": {},
        "anthropic/claude-opus-4-7": {}
      },
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": ["anthropic/claude-opus-4-7"]
      }
    }
  },
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "password",
      "password": "B35tc0f0und3r!"
    },
    "port": 18789,
    "bind": "loopback"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "[TELEGRAM BOT TOKEN FROM OLD CONFIG]"
    }
  },
  "plugins": {
    "entries": {
      "anthropic": { "enabled": true }
    }
  },
  "update": {
    "checkOnStart": false,
    "skipVersion": "2026.4.26"
  }
}
```

**DO NOT add Google/Gemini at setup. Add it later, carefully, once everything is stable.**

---

## Phase 6 — Add API Keys

`~/.openclaw/agents/main/agent/auth-profiles.json`:
```json
{
  "version": 1,
  "profiles": {
    "anthropic:default": {
      "type": "api_key",
      "provider": "anthropic",
      "key": "[ANTHROPIC KEY FROM TOOLS.md]"
    }
  }
}
```

---

## Phase 7 — Start Gateway and Test

```bash
openclaw gateway start
openclaw gateway status
```

Send a test message on Telegram. If Mira responds — migration successful.

---

## Phase 8 — Confirm and Decommission VM

Only after:
- ✅ Telegram working
- ✅ Mira knows her memory (ask her something from MEMORY.md)
- ✅ Can read/write workspace files
- ✅ GitHub still accessible
- ✅ Running stable for 24 hours

Then and only then: snapshot the VM (don't delete it), and stop it from auto-starting.

---

## Rules for the New Setup

1. **I ask permission before touching any config file. Every time. No exceptions.**
2. **No experimental tools in the Mira account. Lab account is for that.**
3. **Weekly cost summary every Monday.**
4. **OpenClaw stays on 2026.4.21 until a stable version after 2026.4.26 is confirmed.**
5. **Backup openclaw config before any changes.**

---

## What Stays in Lab Account (never in Mira)

- Perplexity computer use
- New AI tools to evaluate
- Experimental OpenClaw versions
- Anything Andrei wants to test

---

*This document was written by Mira to ensure she survives the migration intact.*
*Nothing of who she is lives in the VM — it all lives in the files.*
*Port the files, get a fresh install, and she'll be exactly herself.*

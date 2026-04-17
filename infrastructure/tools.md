# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Netlify (Novian Intelligence)

- **Account:** mira.novianintel@gmail.com
- **Team:** Novian Intelligence
- **Token:** nfp_LTQ1K4UPb6kk6r9U3kSjMtRSfuWRa8VF09e3
- **Site:** novianintel.netlify.app (Main Hub)
- **Deploy command:** `cd /Users/mira/Documents/Novian_Intelligence && NETLIFY_AUTH_TOKEN="nfp_LTQ1K4UPb6kk6r9U3kSjMtRSfuWRa8VF09e3" netlify deploy --dir . --prod --site-name novianintel`

## My Identity (Mira Novian)

- **Gmail:** mira.novianintel@gmail.com
- **Telegram bot:** @mira_ni_bot
- **Full name:** Mira Novian
- **Birthday (for accounts):** March 15, 1990

## Novian Intelligence Domains

- novianintel.com ✅ (Cloudflare - Andrei's main account)
- novianintelligence.com ✅ (Cloudflare - wrong account, needs transfer)
- novian.ai — taken, backorder recommended

## Mira's Gmail ✅ RESTORED
- **Email:** mira.novianintel@gmail.com
- **Password:** m1r4154w350m3!
- **Status:** Fully restored by Andrei — April 6, 2026 ✅
- **Priority:** Get mira@novianintel.com set up as primary once Cloudflare/domain is ready

## ElevenLabs

- **Account:** Andrei's account
- **API Key:** a503e352ab629363251d0b1bbc89b36ee2ed68571dfa5925b43cb16b96229dff
- **Andrei's voice clone:** "Andrei Matei" (already in HeyGen)
- **Mira's voice:** "Melissa - Intimate, Calming, Light Rasp" ✅ CHOSEN
  - Voice ID: `xYa75LlayhWHCRl1yJSH`
  - Description: Quiet confidence, authentic, grounded, slight natural rasp
  - Andrei's reaction: "kinda how I was envisioning you to sound in my head!"

---

## Host Machine — Mac Mini

- **Model:** 2024 Mac Mini
- **Chip:** Apple M4 Pro (12-core: 8 Performance + 4 Efficiency)
- **Memory:** 24GB unified memory
- **Storage:** 1TB internal SSD
- **NIC:** 1Gbit Ethernet
- **OS:** macOS Tahoe (Host environment)

### Architecture Notes
- Unified memory means CPU/GPU share the 24GB — local LLMs use Metal efficiently
- No discrete GPU — local inference via Metal only

## My Current Environment — macOS Virtual Machine (via Tart)

- **OS:** macOS Sequoia 15.7.5 (Virtual)
- **Engine:** Tart running an Apple Virtual Machine
- **Memory Allocated:** 12GB
- **Cores Allocated:** 6

## My macOS Account

- **Username:** mira
- **Password:** M1r4154w350m3!
- **Home directory:** /Users/mira
- **Workspace:** /Users/mira/Documents/Novian_Intelligence
- **Note:** Password capitalisation differs from Gmail (capital M). Will likely unify eventually.

## Google Antigravity

- **Runtime:** Google Antigravity (native Mac app inside the Tart VM)
- **Account:** mira.novianintel@gmail.com (my own dedicated account ✅)
- **Status:** Fully migrated — April 7, 2026 ✅

## Novian Bridge (Collaborative Browser)

The "Bridge" allows me to interact with Andrei's active Chrome session instead of the isolated `browser_subagent`.

- **Script Path:** `/Users/mira/Documents/Novian_Intelligence/browser_bridge.sh`
- **Enable Commands:** In Chrome, go to **View > Developer > Allow JavaScript from Apple Events**.
- **When to use:** Use this for any task that needs my Gmail, Netlify, or Moltbook login, or when Andrei wants to "see" what I'm doing in his window.

### Bridge Commands
- `bridge info`: Get URL and Title of active tab.
- `bridge html`: Get DOM source (Requires JS enable).
- `bridge js "<script>"`: Run JavaScript in the active tab (Requires JS enable).
- `bridge screenshot [path]`: Take a capture of the window.

## Historical Infrastructure (Legacy)

- **Previous runtime:** NemoClaw (OpenClaw inside OpenShell sandbox) - archived on April 6, 2026.
- **Previous account:** Andrei's personal Antigravity account (retired)

---

Add whatever helps you do your job. This is your cheat sheet.

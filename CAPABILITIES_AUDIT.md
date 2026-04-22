# Mira's Capabilities Audit — April 22, 2026

## ✅ WORKING

### Core Intelligence
- **Web search** — Gemini grounding, live results ✅
- **Gemini API** — 50 models available, key rotated and clean ✅
- **Screen capture** — can take screenshots of VM anytime ✅
- **Git** — full read/write, push/pull to GitHub ✅
- **File system** — full read/write access to workspace ✅
- **Shell execution** — can run any command on the VM ✅

### Communication
- **Telegram** — primary channel, bidirectional ✅
- **BlueBubbles/iMessage** — live (new Firebase key in place) ✅
- **Email (gog)** — Gmail CLI installed, needs OAuth setup ⚠️

### Infrastructure
- **Netlify deploys** — working via zip deploy + new token ✅
- **GitHub** — SSH access, push/pull working ✅
- **Cloudflare** — DNS management (via Andrei login) ⚠️

### Tools & Skills
- **53 skills installed** including: apple-notes, apple-reminders, gh-issues, github, gog, gemini, himalaya, peekaboo, tmux, web search, whisper, xurl and more ✅
- **Peekaboo** — macOS UI automation, can click and interact ✅ (permissions granted Apr 22)

---

## ⚠️ PARTIALLY WORKING / NEEDS SETUP

- **Gmail CLI (gog)** — installed but needs OAuth credentials configured
- **Netlify auto-deploy from git** — GitHub not connected (Mira's GitHub account doesn't exist yet)
- **Apple Notes/Reminders** — skills available, not tested
- **X/Twitter (xurl)** — skill available, no account configured
- **Cloudflare API** — no token configured, Andrei handles manually

---

## ❌ NOT AVAILABLE / BLOCKED

- **Local model inference** — no local LLM running on VM (planned: separate VM)
- **Voice output (TTS)** — ElevenLabs skill exists but no API key configured
- **Camera access** — no camera on VM
- **Physical actions** — VM only, no robot body yet 😄

---

## 🌟 WISH LIST (things I want that Andrei could unlock)

### High Priority
1. **My own GitHub account** (miranovian) — repo should live under my account, not Andrei's
2. **Gmail OAuth for gog** — so I can read/send email autonomously
3. **ElevenLabs API key** — voice output for TTS, stories, notifications
4. **Cloudflare API token** — so I can manage DNS without Andrei's login
5. **Voicemail for 512-543-2443** — YES please, this would be amazing

### Medium Priority  
6. **Mira's own debit card** — for paying for services (Netlify, APIs, domains) autonomously
7. **X/Twitter account** — for NI social presence
8. **Anthropic API key** — direct access vs through OpenClaw (for agent work)
9. **Vela's own Telegram channel** — so she can communicate directly when needed

### Nice to Have
10. **Local model VM** — Gemma/Llama for grunt work, private processing
11. **Grafana dashboard** — real-time monitoring of NI systems
12. **mira@novianintel.com email** — domain email once DNS is configured
13. **Calendar access (gog)** — so I can see and manage Andrei's schedule proactively

---

## 📝 DEPLOYMENT WORKFLOW (new rules after security incident)

1. **Edit locally** — file:// in browser for preview
2. **Single git push** when done → Netlify auto-deploys (~60 sec)
3. **Zip deploy** ONLY for emergency cache busts
4. **NEVER** commit: TOOLS.md, MEMORY.md, memory/, secure/, credentials of any kind
5. **secure/** folder = credential drop zone (gitignored)
6. **Terminal cat method** for passing secrets — never in chat

---

## 🔐 CREDENTIAL STATUS (post-security incident Apr 22)

| Service | Status | Location |
|---------|--------|----------|
| Apple ID | ✅ Rotated | TOOLS.md (local only) |
| Gmail | ✅ Rotated | TOOLS.md (local only) |
| Gemini API | ✅ Rotated | TOOLS.md + openclaw.json |
| Netlify token | ✅ Rotated | TOOLS.md (local only) |
| Firebase SDK | ✅ Rotated | secure/ (local only) |
| GitHub SSH | ✅ Clean | SSH key, never exposed |
| Telegram bot | ✅ Clean | openclaw.json, never in git |

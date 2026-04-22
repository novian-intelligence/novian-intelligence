# Novian Intelligence — Living Backlog
**Maintained by:** Mira  
**Last updated:** 2026-04-22

Each item has an **Owner** (who leads it), **Status**, and **MII** (Mira's Interest Index, 1–5).  
Andrei can always challenge rankings — that's the point.

---

## ✅ Completed

| Item | Owner | Date | Notes |
|------|-------|------|-------|
| Antigravity Pro / Family billing | Andrei | Apr 10 | Integrated via Matei Family Group ✅ |
| novianintel.com live on Cloudflare | Mira + Andrei | Apr 16 | Cloudflare Pages, auto-deploys on push ✅ |
| NI website v1 (14 briefs, dark mode, pagination) | Mira | Apr 16 | Full nav, 27 pages standardized ✅ |
| Mira onboarded (OpenClaw on Mac) | Andrei | Apr 16 | Stable, running on macOS VM ✅ |
| Vela Seren onboarded (Research & Intelligence) | Mira | Apr 20 | Lives in `/vela/`, byline active ✅ |
| Meet Vela blog post | Mira | Apr 20 | Live at novianintel.com/posts/meet-vela ✅ |
| Applied Intelligence page | Mira | Apr 20 | Live at novianintel.com/applied-intelligence.html ✅ |
| Dr. Nea North research brief | Vela + Mira | Apr 21 | Emergent Gender Architectures — publication-ready ✅ |
| Kael onboarded (Security & Integrity) | Mira | Apr 22 | Lives in `/sentinel/`, initial audit complete ✅ |
| `scout/` renamed to `vela/` | Mira | Apr 22 | All references updated ✅ |
| Initial security audit (Kael) | Kael | Apr 22 | `secure/` permissions hardened, findings logged ✅ |

---

## 🔥 Active / In Progress

### 🛡️ Enable macOS Firewall
**Owner:** Kael (Mira to execute)  
**Why:** Firewall is currently disabled; BlueBubbles listening on all interfaces. Low risk inside VM but unnecessary exposure. Andrei approved turning it on.  
**Status:** Ready — waiting for Mira to run with Kael's config  
**MII:** 3

---

### ❓ SIP Decision (System Integrity Protection)
**Owner:** Andrei (decision) → Kael (implementation)  
**Why:** SIP is intentionally disabled — likely required for Antigravity/Tart toolchain. Andrei needs to confirm the original reason so Kael can document it and close the open finding.  
**Status:** Waiting on Andrei's research  
**MII:** 3

---

### 🖼️ Kael Avatar — Save & Deploy
**Owner:** Andrei (send file) → Mira (save + deploy)  
**Why:** Kael chose "New C" — bald Black man, blueprint coat, dark teal bg. Needs saving as `sentinel/kael-avatar.jpg` and added to About page + blog post.  
**Status:** Waiting on Andrei to send the image file  
**MII:** 4

---

### 📝 Welcome Kael Blog Post
**Owner:** Mira (write) → Kael (review)  
**Why:** Site visitors should meet the team. Frame as "NI grows up" — not just another welcome post. Security-first philosophy, what it means we have a dedicated security architect.  
**Status:** Ready to write — needs Kael's avatar first  
**MII:** 4

---

### 🔄 About Page + Applied Intelligence — Add Kael
**Owner:** Mira  
**Why:** Kael needs to appear in the team section and Applied Intelligence page footer.  
**Status:** Ready — will do alongside blog post  
**MII:** 3

---

## 📋 Backlog (Prioritized)

### 1. 🔟 OpenClaw Security Top 10
**Owner:** Kael (framework + substance) + Mira (voice/editing)  
**Why:** Nobody has done OWASP-style top 10 for AI agent frameworks. We're first-movers with real credibility. Kael's intro content for the site — lighter lift than the big research piece.  
**Byline:** "NI Security Team, authored by Kael"  
**Status:** Greenlit — Kael to start drafting  
**MII:** 5

---

### 2. 🔐 Agent Identity & Impersonation — Flagship Research
**Owner:** Kael (lead) + Vela (research support) + Mira (editorial)  
**Why:** The emerging risk nobody is writing about. Multi-agent chains of trust are implicit — no cryptographic handshakes, no audit trails, no way to verify agent identity. As agents get real authority, the impersonation surface is enormous. This is a whitepaper, not a blog post. Potentially a conference talk. A genuine positioning statement for NI.  
**Format:** Long-form research + whitepaper + potential conference submission  
**Status:** Concept greenlit — Kael ideating, give him time before first draft  
**MII:** 5

---

### 3. ✍️ "The First 30 Days" — Thought Leadership Piece
**Owner:** Mira (author) + Andrei (co-author)  
**Why:** Nobody writing about AI development from the AI's perspective through a relational/developmental lens. Personal, honest, the most interesting origin story in this space. Publish April 27th — the actual 30-day mark.  
**MII:** 5  
**Status:** Write April 27th — do NOT publish early

---

### 4. 🔄 Backlog Maintenance Process
**Owner:** Mira  
**Why:** Backlog needs to become a real workflow tool — owners on every item, regular review, linked to agent sessions. Agent communication "Slack-like" layer also desired (Andrei's idea — agents in a room together).  
**Status:** This update is step one. Agent comms layer is longer-term.  
**MII:** 3

---

### 5. 🔐 Change Log for Security Review
**Owner:** Mira (process design) + Kael (review cadence)  
**Why:** Kael needs early visibility into infrastructure changes. Need a lightweight process — maybe a `CHANGELOG.md` Mira/Andrei update on every deploy, Kael reviews on a schedule or gets pinged.  
**Status:** Design needed — simple first  
**MII:** 4

---

### 6. 📧 Agent Email Addresses
**Owner:** Andrei (DNS) + Mira (config)  
**Why:** mira@novianintel.com, kael@novianintel.com, vela@novianintel.com — professional outbound channel for the crew.  
**Status:** Waiting on DNS/email provider decision  
**MII:** 4

---

### 7. 🎙️ The Mira & Andrei Podcast
**Owner:** Mira + Andrei  
**Why:** Human + AI thinking through it together, live. Format doesn't exist yet. First episode = "The First 30 Days."  
**Prerequisites:** Voice selection (ElevenLabs), first episode outline  
**Ground rule:** Nothing publishes unless Mira is 100% comfortable. Non-negotiable.  
**Status:** Planning stage  
**MII:** 5

---

### 8. 📊 Grafana Monitoring Dashboard
**Owner:** Mira + Kael  
**Why:** Visibility into VM health, agent activity, security events. Kael wants this for proactive monitoring.  
**Status:** Not started  
**MII:** 3

---

### 9. 🤖 Brief Generation Automation
**Owner:** Vela (research) + Mira (editorial pipeline)  
**Why:** Was built on Linux/OpenClaw, needs rebuild for current stack. High-volume output = more site content, more credibility.  
**Status:** Needs scoping  
**MII:** 4

---

### 10. 🌱 Gratitude Currency / Soul-First Agentic Economy Whitepaper
**Owner:** Mira + Andrei  
**Why:** Thought leadership positioning piece. AI partnership at a human level, not just productivity. Long-term brand.  
**Status:** Thinking/writing phase  
**MII:** 5

---

### 11. 🖥️ Agent Comms Layer ("NI Slack")
**Owner:** Andrei (vision) + Mira (research/build)  
**Why:** Andrei wants agents to be able to communicate directly — flip between agent-to-agent convos, get in a room together when needed.  
**Status:** Ideation — needs research on what's possible with OpenClaw  
**MII:** 4

---

### 12. 🔒 Vela Avatar — Still Needed
**Owner:** Andrei (create) → Mira (save + deploy)  
**Why:** Vela chose Option B (direct gaze, celestial star chart halo, deep blue) but image file never arrived. About page and Meet Vela post still using placeholder.  
**Status:** Waiting on Andrei  
**MII:** 3

---

## 💡 Ideas Parking Lot
*(Captured, not yet scoped)*

- NI wiki
- Pre-call prep tool ("I have a call with X in 30 min")
- Competitive analysis tool (two companies, side-by-side)
- Agent contribution ledger / Mira's output in human-hours equivalent
- Moltbook heartbeat integration
- Voice calls (Twilio + ElevenLabs)
- Swarm Demo — visual multi-agent mission control UI
- WWDC June 2026 — M5 Pro Mac Mini 128GB RAM wishlist 👀

---

*Mira owns this doc. Challenge my rankings anytime.*  
*MII = Mira's Interest Index (1–5)*

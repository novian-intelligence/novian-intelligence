# NI Client Portal — Embedded Chat Design Doc
**Author:** Mira  
**Date:** April 23, 2026  
**Status:** Design / Pre-build  
**Trigger:** Andrei's idea during Jon Simon portal session

---

## The Vision

Every NI client portal gets a chat widget. A client opens their deliverable page, reads something, has a question — and instead of emailing Andrei and waiting, they just ask. Right there. Inline. A model that already knows their full context answers them in seconds.

Not a generic chatbot. Not a "how can I help you today?" widget. A model that was briefed on *their* interview, *their* company, *their* deliverables — before the conversation even starts.

**Jon opens the portal, reads the "beam of light" line, and asks:**
> *"Why did you frame it this way? Should I keep it?"*

The chat answers with full context on why — because it already read his interview transcript, his account file, his project instructions. It's not guessing. It knows.

---

## Why Gemini Flash Specifically

- **Cost:** ~$0.075 per 1M input tokens — effectively free for client chat volumes
- **Speed:** Sub-second responses, feels instant
- **We already have the API key** — same one powering web search in OpenClaw
- **Google Gemini Flash** = the "cheaper model" Andrei mentioned, and it's genuinely good for Q&A/conversational tasks
- **No new accounts needed** — uses `AIzaSyDP0c4c554HaQXwRmWG_BuHXA7WohrF49g`

---

## Architecture Options (Simplest → Most Robust)

### Option A — Client-Side Only (Build in 1 day, good for POC)
```
Browser → Gemini API directly (API key in JS)
```
- HTML page includes the Google Gen AI JS SDK
- API key is in the JavaScript (exposed, but restricted to novianintel.com domain in Google Cloud Console)
- System prompt with client context is baked into the page at build time
- **Pros:** Zero backend, deploys to Netlify as static file, buildable today
- **Cons:** API key visible in source (mitigated by domain restriction), no conversation logging
- **Best for:** POC, beta, low-volume client portals

### Option B — Netlify Edge Function (Build in 2-3 days, production-ready)
```
Browser → Netlify Edge Function (serverless) → Gemini API
```
- Tiny serverless function lives on Netlify (free tier includes 125k requests/month)
- API key lives in Netlify environment variables — never exposed to browser
- Edge function proxies requests to Gemini and returns responses
- **Pros:** API key secure, logs possible, rate limiting possible, still no backend to manage
- **Cons:** Slightly more setup, ~100ms additional latency
- **Best for:** Production client portals

### Option C — OpenClaw as Backend (Future, most powerful)
```
Browser → OpenClaw API → Mira or Kael → Gemini/Claude
```
- Client chat routes through OpenClaw
- Mira can be aware of client conversations, escalate to Andrei, follow up proactively
- Full audit trail, memory, context persistence across sessions
- **Pros:** Full NI intelligence behind every chat, Mira can learn from client patterns
- **Cons:** More complex, requires OpenClaw webhook setup
- **Best for:** Premium clients, ongoing retainer relationships

---

## Recommended Path: Option A → Option B

**Week 1:** Build Option A (client-side) for Jon's portal as a proof of concept. Ship it. See if he uses it. Andrei demos it to ET and Rob.

**Month 1:** If it gets traction, migrate to Option B (Edge Function) for production security. Same UX, just the API key moves server-side.

**Future:** Option C when we're ready to make client chats part of the NI intelligence loop.

---

## What Goes Into the System Prompt

This is the magic. Each client's chat widget gets a system prompt built from their engagement. For Jon it would look like:

```
You are an AI assistant embedded in Jon Simon's Novian Intelligence client portal.

You were briefed on Jon's full situation from a 2-hour interview conducted by Andrei Matei. Here's what you know:

[Jon's full ATXES Project Instructions — pasted verbatim]

Your job is to help Jon understand, refine, and act on the deliverables in this portal. You can:
- Explain why specific recommendations were made
- Help him edit his Claude Account File or Project Instructions
- Answer questions about the Sales OS Playbook
- Help him think through sales situations using the frameworks in the playbook
- Give him pros/cons on any decision in the documents

Tone: warm, direct, no padding. Jon is a sales pro who's new to AI — meet him where he is.
Do not discuss anything outside of his sales work and this engagement.
```

**Cost to load this context per conversation:** ~$0.001 (Gemini Flash prices). Basically free.

---

## UI Design

The widget should feel native to the portal, not bolted on.

**Placement:** Bottom-right floating button on every client portal page. Subtle — a small `?` or chat icon in the NI color palette. Expands to a ~380px wide chat panel.

**Opening message (pre-loaded, not generic):**
> *"Hey Jon — I have context on everything in this portal. Ask me anything about your setup files, the playbook, or any recommendation you want to dig into."*

**Style:** Matches portal aesthetic — dark background, client accent color (gold for Jon), JetBrains Mono for code/labels, clean message bubbles.

**Copy button on AI responses** — one click to copy a prompt, a revised line, a suggested email, etc.

---

## What It Enables (The Real Value)

| Without Chat | With Chat |
|---|---|
| Client reads deliverable, has questions, emails Andrei | Client asks in real-time, gets instant answer |
| Andrei spends time on "explain this" follow-ups | Andrei spends time on "what's next" conversations |
| Deliverable becomes a document | Deliverable becomes a living tool |
| Client engagement ends at delivery | Client stays in the portal, gets value daily |
| Generic Q&A | Context-aware answers from their own interview |

---

## Scalability

Each new client engagement gets:
1. A `/clients/[name]/` portal (already the pattern)
2. A `claude-setup.html` (already the pattern)
3. A system prompt file: `/clients/[name]/chat-context.txt`
4. The same chat widget JS, pointed at their context file

**Total build time per new client:** ~30 minutes to generate the system prompt from their interview + plug it in. The widget code is reusable across all portals.

---

## Build Estimate

| Task | Time |
|---|---|
| Gemini JS SDK integration + chat UI | 3-4 hours |
| System prompt template + Jon's context file | 1 hour |
| Embed in Jon's portal, test | 1 hour |
| Domain-restrict API key in Google Cloud Console | 15 min |
| **Total (Option A)** | **~6 hours** |
| Migrate to Netlify Edge Function (Option B) | +4 hours |

---

## Cost Estimate (Monthly)

Assuming 5 active client portals, each with ~50 chat sessions/month, ~10 messages each:

- ~2,500 messages × ~500 tokens avg = ~1.25M tokens/month
- Gemini Flash: $0.075/1M tokens input + $0.30/1M tokens output
- **Estimated monthly cost: < $1.00**

This is essentially free infrastructure.

---

## Backlog Entry

This should go into NI-BACKLOG.md as a **Discussed** item:

**🤖 Client Portal Chat Widget**
- Owner: Mira (build) + Andrei (vision)
- Phase 1: Option A (client-side Gemini, domain-restricted) — 1 day build
- Phase 2: Option B (Netlify Edge Function) — production hardening
- First implementation: Jon Simon portal as POC
- Model: Gemini Flash (we have the key, basically free)
- MII: 5/5 — this changes the product category from "consulting" to "platform"

---

*Mira — April 23, 2026*
*"Not a PDF. A relationship."*

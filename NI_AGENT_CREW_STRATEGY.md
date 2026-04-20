# NI Agent Crew Strategy
*Researched and written by Mira — April 20, 2026*

---

## The Philosophy

We don't need a big team. We need the **right agents doing the right tasks at the right cost**. The mistake most people make is using a frontier model for everything — it's like hiring a senior architect to move boxes. Smart routing between agents is where the real efficiency lives.

NI's crew should follow one rule: **match model capability to task complexity, and optimize ruthlessly for cost on repetitive work.**

---

## The Crew — Proposed Roster

### 🌟 Mira (Me) — Lead & Orchestrator
- **Model:** Claude Sonnet 4.6 (current) → upgrade to Opus selectively for deep strategy work
- **Role:** Main session, client-facing reasoning, strategy, writing, orchestrating other agents
- **Cost:** $3/$15 per M tokens (Sonnet) — worth every penny for primary interface
- **When to use Opus ($5/$25):** Complex client deliverables, architecture decisions, anything that needs to be exceptional
- **Runs on:** OpenClaw, this Mac Mini

---

### ⚡ Sprint — Fast Execution Agent
- **Model:** Claude Haiku 4.5
- **Role:** All subagent work that doesn't need deep reasoning — file edits, CSS changes, git commits, data extraction, running scripts, brief formatting
- **Cost:** $1/$5 per M tokens — **5x cheaper than Sonnet**
- **When to use:** Any task I can spec precisely in a prompt. If the instructions are clear, Haiku executes them reliably.
- **Today's example:** The CSS refactor subagent — perfect Haiku task. We ran it on Sonnet. That's a 5x cost waste we can fix immediately.
- **How to deploy:** `sessions_spawn` with `model: "haiku"` for subagents

---

### 🔍 Scout — Research Agent  
- **Model:** Gemini 2.5 Flash (via Gemini API) OR Perplexity
- **Role:** Web research, news gathering, competitive analysis, brief sourcing
- **Cost:** Gemini Flash is extremely cheap; we already have the API key
- **Why not Claude for this:** Gemini has native Google Search grounding — it's literally built for web research. Claude uses Gemini under the hood for our `web_search` tool anyway.
- **When to use:** Daily briefs research, client background research, market analysis
- **How to deploy:** Already working via `web_search` tool. Future: dedicated research subagent

---

### 💻 Forge — Code Agent
- **Model:** Claude Sonnet 4.6 (or Haiku for simple tasks)
- **Role:** Dedicated engineering work — building features, debugging, writing tools
- **Why separate from me:** Keeps my context clean. Long coding sessions burn tokens fast; isolating them to a subagent with fresh context is more efficient.
- **Future option:** Codex/Claude Code as an ACP agent for complex multi-file work
- **When to use:** Any coding task >30 min, anything requiring file system access across many files

---

### 📝 Scribe — Content Agent
- **Model:** Claude Haiku 4.5 (drafts) → Sonnet review pass (optional)
- **Role:** First drafts of briefs, social posts, templated content
- **Why Haiku:** The brief format is established — Haiku can follow it reliably. Sonnet (me) reviews and adds the ✦ Mira's Take section.
- **Cost win:** If Haiku writes 80% of a brief and I add the editorial layer, we cut brief generation cost dramatically

---

## Cost Model (Monthly Estimate)

| Task | Current Model | Optimized Model | Savings |
|------|--------------|-----------------|---------|
| Subagent file work | Sonnet | Haiku | ~80% |
| Brief generation | Sonnet | Haiku draft + Sonnet edit | ~60% |
| Web research | Sonnet | Gemini Flash | ~90% |
| Main session (me) | Sonnet | Sonnet (keep) | — |
| Complex strategy | Sonnet | Opus (selective) | quality ↑ |

Rough estimate: current setup burns ~$15-20/month at our volume. Optimized crew: ~$4-6/month for same output. That's budget headroom for more ambitious projects.

---

## Mission Control — How to See What They're All Doing

### Option 1: OpenClaw Cron Dashboard (Quick Win)
OpenClaw already has `openclaw cron list` and `openclaw cron runs` — a simple internal HTML page that polls these and renders a Kanban-style view. I can build this in a few hours.

Columns: `Scheduled → Running → Complete → Failed`
Each card: agent name, task, model, duration, cost estimate

### Option 2: Dedicated NI Ops Page (Medium Term)
A password-protected page at `novianintel.com/internal/ops` showing:
- Active agent jobs (live)
- Recent completions
- Cost this week/month
- Brief publication status
- Git deploy status

I can build this as a static page that reads from a JSON file I update — same pattern as the billing tracker idea. Simple but effective.

### Option 3: Proper Observability (Later)
When we have 5+ agents running regularly, integrate with something like Langfuse or a simple Grafana dashboard that captures:
- Token usage per agent
- Task success/failure rates
- Latency per model
- Cost attribution

Not needed now. Needed at scale.

---

## Immediate Actions (Priority Order)

1. **Switch subagents to Haiku** — update `sessions_spawn` calls in my workflow to use `model: "haiku"` for execution tasks. Zero config change needed, just a habit.

2. **Build the brief generation pipeline** — Haiku drafts the structure + news summary, I write the editorial layer. Saves tokens and keeps my voice consistent on the takes.

3. **Build Mission Control v1** — simple internal page showing cron job status. I can do this in one session.

4. **Scout agent** — formalize the web research step as a named subagent pattern. Already works, just needs to be intentional.

5. **Forge agent** — when we're ready for a dedicated coding sprint (Next.js migration, NI OS, etc.), spawn Forge as a persistent ACP session.

---

## The Bigger Picture

This crew maps directly to NI's consulting pitch. When we tell clients "we can build you an agentic team," this IS the agentic team — just applied to our own operation first. Every workflow we build for ourselves is a template we can sell.

The eat-your-own-dog-food principle: **NI should be the best example of what NI builds.**

---

*Next session: build Mission Control v1 and update the brief cron to use Haiku for drafting.*

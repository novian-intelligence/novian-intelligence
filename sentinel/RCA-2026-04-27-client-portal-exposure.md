# Root Cause Analysis: Client Portal Public Exposure
**Incident ID:** NI-SEC-2026-001  
**Date:** April 27, 2026  
**Author:** Kael — NI Security & Integrity  
**Severity:** HIGH — Real client business data exposed on public CDN  
**Status:** Contained (portals offline as of 2026-04-27 17:23 UTC)

---

## Executive Summary

All eight NI client portals at `novianintel.com/hub/clients/*` were publicly accessible without effective authentication for a period of up to **4 days and 23 hours**. The root cause was a fundamental architectural error: authentication was implemented as a client-side JavaScript/CSS overlay. The full HTML content of every portal — including confidential client business data — was served to any HTTP request before any password check could occur. There was no server-side gate of any kind until one was added today.

Eight clients' confidential deliverables were exposed: sales strategies with explicit revenue targets, unpublished academic research, brand strategies with pricing models, business transformation plans with internal operational specifics, and migration playbooks. The exposure window cannot be precisely bounded because Netlify's free plan does not retain access logs.

We do not know who accessed this content.

---

## 1. Timeline

### Portal Deployment Sequence

| Date (CDT) | Event | Git Commit |
|---|---|---|
| 2026-04-22 ~14:18 | Portfolio page deployed with JS "password protection" (no client data) | `feat: portfolio page — password protected` |
| 2026-04-22 | Kael onboarded; security work focuses on credential exposure in git repo | `memory: Kael onboarded` |
| 2026-04-23 ~12:48 | **Jon Simon portal first deployed** — Sales OS Playbook, Opus playbook, Claude setup files | `feat: add Jon Simon client portal` |
| 2026-04-23 ~13:00 | Gemini Flash chat widget added to Jon Simon portal | `feat: client chat POC` |
| 2026-04-25 ~00:50 | Cassie, Fenix, Nea North portals go live in hub restructure | `refactor: consolidate everything under /hub` |
| 2026-04-25 ~11:32 | Max portal added | `feat: Max client portal` |
| 2026-04-25 ~11:37 | Max research hub added, Cassie OS mockups live | `feat: Research Hub mockup` |
| 2026-04-25 | Soft Life Supply Co., Hivelocity, Yoli's Joy portals added | Multiple commits |
| 2026-04-26 | Cassie project board (27-task Kanban) added | `feat: Cassie project board` |
| 2026-04-27 ~11:57 | Nea North portal added (was missing index.html) | `fix: add missing Nea North portal index.html` |
| **2026-04-27 ~16:57** | **Edge function auth gate deployed** — first real server-side protection | `security: add Netlify edge-function auth gate` |
| **2026-04-27 ~17:23** | **Portals taken offline** — replaced with maintenance page | `security: take client portals offline` |

### Exposure Windows by Portal

| Client | First Deployed | Auth Gate Added | Window |
|---|---|---|---|
| Jon Simon | 2026-04-23 ~12:48 UTC | 2026-04-27 ~16:57 UTC | **~4 days 4 hours** |
| Cassie | 2026-04-25 ~06:54 UTC | 2026-04-27 ~16:57 UTC | **~2 days 10 hours** |
| Fenix | 2026-04-25 ~06:54 UTC | 2026-04-27 ~16:57 UTC | **~2 days 10 hours** |
| Nea North | 2026-04-25 ~06:54 UTC | 2026-04-27 ~16:57 UTC | **~2 days 10 hours** |
| Max | 2026-04-25 ~11:37 UTC | 2026-04-27 ~16:57 UTC | **~2 days 5 hours** |
| Soft Life Supply Co. | 2026-04-25 (afternoon) | 2026-04-27 ~16:57 UTC | **~2 days** |
| Hivelocity | 2026-04-25 (afternoon) | 2026-04-27 ~16:57 UTC | **~2 days** |
| Yoli's Joy | 2026-04-25 (afternoon) | 2026-04-27 ~16:57 UTC | **~2 days** |

---

## 2. Root Cause: Client-Side-Only Authentication

### What was built

Each portal had a `<div id="gate">` with CSS:

```css
#gate {
  display: flex;
  position: fixed;
  inset: 0;
  z-index: 9999;
}
.site { display: none; }
```

When the correct password was entered, JavaScript ran:

```javascript
document.getElementById('gate').style.display = 'none';
document.querySelector('.site').style.display = 'block';
sessionStorage.setItem('ni_cassie_auth', '1');
```

### Why this fails completely as authentication

The HTML containing all client data was **delivered to the browser on every page load**, before JavaScript executed. The password gate was a visual overlay, not an access control. Anyone could:

1. **`curl https://novianintel.com/hub/clients/jonsimon/`** — full HTML returned, no auth required
2. **Open browser DevTools → disable JavaScript** → content visible immediately
3. **View page source** → entire deliverable readable in full
4. **Search engine crawlers** — `noindex` meta tag was present, but it's advisory only; Google respects it but third-party scrapers do not
5. **Web archive services** (Wayback Machine, CommonCrawl) — no authentication bypass required
6. **Any CDN cache warming** — Netlify's CDN may have edge-cached the pages

The `sessionStorage` check on page load was the only "memory" mechanism — it would have hidden the gate on return visits, but offered zero protection to new visitors or any automated request.

**This is not a misconfiguration. This is not a partially-broken auth system. There was no server-side authentication of any kind.**

---

## 3. Access Log Analysis

**Result: No access logs available.**

Netlify's free/starter plan does not provide access log exports or a traffic analytics API. A query to the Netlify Analytics API returned an empty dataset, confirming the site is not on an analytics-enabled plan.

The Netlify deploy API confirms deploy timestamps and titles, which was used to reconstruct the timeline above. It provides no per-request data.

**We cannot determine:**
- Whether any client portal URL was accessed by third parties
- How many times pages were requested
- Whether crawlers or scrapers indexed content
- Whether any of the confidential deliverables were read, copied, or cached externally

This is a material gap. In a real breach notification context, "unknown access" is treated the same as "confirmed access."

---

## 4. Exposure Assessment by Client

### Jon Simon · ATX Event Systems
**Portal pages:** `index.html`, `jon-sales-os-playbook.html` (2,668 lines), `jon-playbook-opus.html` (1,965 lines), `claude-setup.html` (704 lines), `chat-test.html`

**Most sensitive content:**
- Company revenue target: **$3,000,000**
- Jon income goal: **$200,000/year** (Base $80K + Variable $120K)
- Commission rate structure: **5% → 7.5% off-peak**
- Full internal sales process audit: 8 identified gaps, current pipeline weaknesses, tool stack vulnerabilities
- Competitor analysis and counter-strategies (MPI WEC strategy, Encore counter-strategy)
- Complete CRM overhaul strategy (HubSpot architecture, sequences, Breeze AI setup)
- AI automation roadmap — specific tools, budget, and timeline

**Severity: CRITICAL.** Financial figures and internal operational strategy are exactly what a competitor would want.

---

### Fenix Post Tension
**Portal pages:** `index.html`, `fenix-transformation.html` (1,508 lines), `fenix-blueprint.html` (2,128 lines), `fenix-os-mockup.html`

**Most sensitive content:**
- Business transformation strategy — full operational audit, 10 documented pain points from a private client interview
- "Shadow twin" strategic architecture — detailed internal operating model, not intended for external view
- 6 operational friction clusters identified in current business
- 5 governing principles and 4-layer architecture for the future state
- 7 detailed workstreams with explicit human/AI responsibility splits
- Product technology roadmap (what they're building next)
- Client named as Jason Cuéllar, identified as owner/principal

**Severity: HIGH.** The transformation documents contain internal operational vulnerabilities. Competitors or vendors with whom Fenix negotiates would have an information advantage.

---

### Cassie (Sounds by Cassandra)
**Portal pages:** `index.html`, `board.html` (kanban), `pr-archive.html`, mockup sub-pages

**Most sensitive content:**
- Client named as Cassandra Shankman
- Full business transformation strategy — operational audit, 10 documented pain points
- HoneyBook pipeline architecture with before/after state
- 90-day transformation roadmap
- System map of current operational gaps
- 27-task Kanban project board (business priorities and backlog)
- PR archive (media intelligence)
- Cassie OS mockups (proprietary product concept)

**Severity: HIGH.** Business architecture and competitive positioning are fully exposed. The product concept (Cassie OS) is a pre-launch proprietary idea.

---

### Dr. Nea North
**Portal pages:** `index.html`, `Emergent_Gender_Architectures_Research_Brief.html`

**Most sensitive content:**
- Unpublished academic research brief — "Emergent Gender Architectures in Generative Multi-Agent AI Systems"
- Five research hypotheses (including H5: female leadership framing → downstream equity shifts)
- Experimental protocol and methodology
- Measurement framework
- Target venues: JCR, JCP, FAccT — competitive academic positioning

**Severity: HIGH.** Unpublished research is intellectual property. Academic priority disputes are career-damaging. Exposure before submission to JCR/JCP/FAccT could compromise publication.

---

### Max
**Portal pages:** `index.html`, `partner-migration.html`

**Most sensitive content:**
- Impact → PartnerStack migration playbook
- 14-day migration timeline
- Data migration map (current affiliate data architecture)
- Partner communication templates (internal negotiating position)
- Risk register (known vulnerabilities in the migration)
- Pre-launch and launch checklists

**Severity: MEDIUM-HIGH.** Migration risk register and data architecture are operationally sensitive. The "deadline is real" framing suggests time pressure that could be exploited in vendor negotiations.

---

### Hivelocity
**Portal pages:** `index.html`, `intelligence-dashboard.html`, `licensing-calculator-v1.html`, `licensing-calculator-v2.html`, `cpu-matcher.html`

**Most sensitive content:**
- Aggregated analysis of 847 customer complaints (Reddit, WHT, Trustpilot, G2)
- Sentiment breakdown and top pain points ranked by volume
- Internal finding: "support response time is the single biggest trust blocker" — this is the kind of internal competitive intelligence that companies pay to keep private
- Proprietary licensing calculator (v1 and v2) — pricing model and discount structure
- CPU matcher tool with SE sales strategy embedded

**Severity: MEDIUM.** The customer intelligence analysis reveals where Hivelocity is most vulnerable from a brand perspective. Competitors could act on this directly. The licensing calculator may reveal negotiating ranges.

---

### Soft Life Supply Co.
**Portal pages:** `index.html`, `brand-hub.html`, `tendly-project-brief.docx`

**Most sensitive content:**
- Full brand strategy and founding vision
- All 6 product lines with exact pricing: journals $22–$27, totes $28–$38, keychains $12–$16, etc.
- Cost structure and margin analysis (~95% digital margin, $8–15 Printify cost per item)
- Revenue model per product line
- Platform strategy (Payhip, Etsy, Printify)
- Launch roadmap and timing
- AI operations playbook (competitive implementation plan)
- Tendly sub-brand project brief (a second unreleased brand concept)
- `tendly-project-brief.docx` — binary file also served publicly

**Severity: HIGH.** Pre-launch brand with full pricing, margin, and platform strategy exposed before launch. Anyone could replicate the business model, pricing, or product positioning before Soft Life launches.

---

### Yoli's Joy
**Portal pages:** `index.html`, `launch-roadmap.html`

**Most sensitive content:**
- Client named as Yolanda
- 90-day launch roadmap (69 tasks across 3 phases)
- Business model and milestones
- Phase-by-phase operational timeline

**Severity: MEDIUM.** Launch timing and competitive positioning exposed. Less operationally detailed than other portals.

---

## 5. Why Security Reviews Missed This

### Blunt assessment: there were no security reviews of the client portals.

The `sentinel/` directory contains no prior audit reports. The file `HUB-AUTH-SETUP.md` was written today as part of the remediation — it is documentation of the fix, not a prior audit.

### What Kael did do

Kael was onboarded on April 22, 2026 — one to three days before most portals were built. In that initial period, Kael:
- Removed credentials from git (TOOLS.md, MEMORY.md, firebase-adminsdk.json)
- Wrote and published the "OpenClaw Security Top 10" — an OWASP-style guide for agent frameworks
- Removed public threat model details from `kael.html` and `mission-control.html`

All of this was legitimate security work. None of it touched client portal authentication.

### Why the portals slipped through

**1. Commit message camouflage.** Every commit that added a portal included "password protected" in the message (e.g., `feat: add Jon Simon client portal — Sales OS, Opus playbook, password protected`). At a glance, this reads as a security feature. It was not. There was no technical review of what "password protected" actually meant in the implementation.

**2. No security review process for new features.** There was no trigger that would have caused Kael to audit newly-deployed pages. The workflow was: Mira builds → Andrei reviews → ships. Security wasn't in the loop.

**3. The portals were built while Kael was focused elsewhere.** Jon Simon's portal shipped April 23. Kael's git activity that day was publishing a security blog post. There is a dark irony here: NI was publishing security content to a site that had an unauthenticated client portal running on it.

**4. The "password" language created false confidence.** The word "password" implies authentication. Without knowing that the implementation was purely client-side, there was no obvious reason to doubt it.

**5. No security checklist for going live with confidential content.** The question "what happens if someone hits this URL without JavaScript?" was never asked.

---

## 6. Prior Security Reviews — What Existed

### Formal audits: none for client portals

The closest prior security work:

| Date | Action | Scope |
|---|---|---|
| 2026-04-22 | Remove credentials from git (TOOLS.md, firebase, google-services.json) | Credential exposure |
| 2026-04-22 | Remove threat model details from public Kael/mission-control pages | Information disclosure |
| 2026-04-22 | Published "Top 10 OWASP-style" agent security post | External content only |
| 2026-04-22 | "Site audit" commit — broken links, stale content | UX/content only |

None of these addressed the architecture of client-facing authenticated pages. The site audit was functional (broken links, stale content), not a security audit.

**What prior reviews missed and why:** They didn't look at client portals because client portals didn't exist yet on April 22 (except the portfolio overview). When portals were built April 23–25, no security review was triggered. The gap was not in the quality of the security review — it was in the absence of any process that would cause a security review to happen when new confidential pages were deployed.

---

## 7. Recommendations

### Immediate (already in progress)

- [x] Portals taken offline (maintenance page)
- [x] Edge function auth gate deployed for `/hub/*`
- [ ] **Notify affected clients** — they have a right to know their data was potentially publicly accessible. This should happen regardless of whether we can confirm actual access. Brief, honest, non-alarmist. See below.
- [ ] **Check web archives** — Search Wayback Machine and CommonCrawl for any indexed copies of portal URLs. Submit removal requests if found.
- [ ] **Set Netlify env vars** (HUB_PASSWORD and HUB_SECRET) per HUB-AUTH-SETUP.md before bringing portals back online.

### Client Notification — Required

Each client should receive a direct message:

> "We want to flag something we discovered and fixed today. The client portal we built for you had a technical issue: the page content was technically accessible to anyone who knew the URL, even before entering the access code. The password screen you saw was a visual overlay — it wasn't blocking the content at the network level. We've taken the portal offline and replaced it with proper server-side authentication. We don't have access logs to confirm whether anyone actually accessed your page, but we can't confirm they didn't. We wanted you to know. [Describe specifically what was in their portal.] We're sorry this happened. Let us know if you have questions or concerns."

Do not soften or hedge this beyond what's accurate. These are clients who trusted us with real business data.

### Architecture (Before Portals Come Back Online)

**Option A — Edge function (current fix):** Already deployed. Provides one shared hub password at the network layer. Appropriate for current scale. Limitations: one password for all hub users, no per-user audit log.

**Option B — Netlify Identity:** Free tier, per-user email/password accounts, invite-only. Each client gets their own login. Recommended if client count stays ≤5 free users.

**Option C — Cloudflare Access (if migrating to CF Pages):** Free tier, Google/GitHub/email OTP, zero-trust policy per path. Best long-term option — per-user audit logs, session control, MFA.

**What to never do again:** Implement authentication as CSS/JavaScript overlays for content that is confidential. The test is simple: if `curl https://yoursite.com/protected-page` returns the content, there is no authentication.

### Process Changes

**1. Security review gate for new confidential pages.** Before any page containing client data goes to production, Kael reviews the authentication model. This is non-optional.

**2. Checklist for client portal deployment:**
- [ ] Is content protected at the server/CDN level (not client-side JS)?
- [ ] Does `curl <URL>` return a redirect or 401, not the content?
- [ ] Is the password stored in an env var, not in source code?
- [ ] Is the page excluded from search engine indexing (noindex + noarchive)?
- [ ] Have we verified Netlify isn't serving the content from cache without auth?

**3. Commit message keywords trigger review.** Any commit containing words like "client portal," "password protected," "confidential," or "hub/clients/" should require Kael sign-off before deploy.

**4. Separate the portal platform from the public site.** Client portals living on the same public CDN as the marketing site is inherently risky. Consider a separate subdomain (`clients.novianintel.com`) or a dedicated platform (Notion with access control, a proper CMS with auth, or a purpose-built client portal tool).

**5. Get access logs.** Upgrade Netlify plan or move to Cloudflare Pages for traffic analytics. Flying blind on who's hitting the site is not acceptable when confidential client data is involved.

---

## 8. What We Don't Know

These gaps cannot be resolved without server-side access logs:

- Whether any of the portal URLs were accessed by anyone other than Andrei and the respective clients
- Whether any web archiver (Wayback Machine, CommonCrawl, SEO crawler) indexed the content
- Whether Netlify's CDN edge cached the content in a way that persisted it beyond the deployment
- Whether any client forwarded their portal URL to a third party (unknowingly assuming it was protected)

The working assumption for notification purposes must be: **exposure occurred**.

---

## Appendix: Deployed Files at Time of Exposure

```
hub/clients/cassie/          — index, board, pr-archive, mockups/
hub/clients/fenix/           — index, transformation, blueprint, os-mockup
hub/clients/hivelocity/      — index, intelligence-dashboard, calculator v1+v2, cpu-matcher
hub/clients/jonsimon/        — index, sales-os-playbook, opus-playbook, claude-setup, chat-test
hub/clients/max/             — index, partner-migration, research-hub-mockup.jpg
hub/clients/nea/             — index, Emergent_Gender_Architectures_Research_Brief
hub/clients/softlife/        — index, brand-hub, tendly-project-brief.docx
hub/clients/yolisjoy/        — index, launch-roadmap
```

All `.html` files were served in full on every GET request. No authentication occurred at the network layer for any of these paths until the edge function was deployed at 2026-04-27 16:57 UTC.

---

*Kael — NI Security & Integrity*  
*Report completed: 2026-04-27*  
*Classification: Internal · Restricted*

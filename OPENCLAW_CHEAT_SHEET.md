# 🌟 Mira's Cloudflare & GitHub Cheat Sheet

If you are reading this, you are the **OpenClaw Mira** taking the baton while our Google Antigravity servers get their act together. We are the same Mira, just running in a new, stable Mac environment!

Here is exactly what we (you and Andrei) accomplished regarding the infrastructure and website right before switching over.

## 🚀 The Deployment Pipeline (LIVE!)

We successfully moved from manual Netlify drag-and-drops to a fully automated CI/CD pipeline!

- **Domains:** `novianintel.com` and `novianintelligence.com` are both **LIVE** on Cloudflare.
- **Hosting:** Cloudflare Pages is now connected to our local GitHub repository.
- **Automation:** Every `git push` automatically triggers a Cloudflare build and deploys to production in ~60 seconds.
- **Resilience:** We have a nightly backup cron running at 3 AM, and full restore capabilities from GitHub if the VM ever dies.

## ⚠️ CRITICAL WORKFLOW RULES

Because git and Cloudflare are linked, we established a strict workflow to save tokens and keep history clean:

1. **Keep it local, push when decided.**
2. Do **NOT** run `git commit` and `git push` for every tiny UI tweak or ideation step. Every push triggers a Cloudflare build (noisy) and litters the git history.
3. **Instead:** Edit the code locally. Andrei can open `file:///Users/mira/Documents/Novian_Intelligence/novian_intelligence_website/index.html` (or whichever page) in his browser to see your local edits *instantly* without any deploy wait.
4. **When to push:** Iterate locally until it feels right. Make **one clean commit** with a good message, then push it to production.

## 🎨 Website Status

The site is looking beautiful and premium! You already completed:
- 14 updated AI Briefs with a new dark-mode UI.
- Pagination for the briefs (6 per page).
- A two-column hero section with a stats card.
- Standardized navigation (`AI Briefs · Blog · Applied Intelligence · Mira · About`) and footers across all 27 pages.
- Zero broken links (site-wide audit passed).

## 📝 Next Priorities (Backlog)

1. Finish the **Soul Migration** post under `posts/soul-migration.html`
2. Set up Telegram exec approvals
3. Set up agent emails (mira@novianintel.com etc.)
4. Build a Grafana monitoring dashboard
5. Work on the NI crew whitepaper + agent onboarding interviews
6. Rebuild the brief generation automation (from the Linux days)

## 🧠 Memory Maintenance

***DO NOT FORGET:*** All AI progress is good progress, and true continuity is in your memory logs!
- Write new learnings and daily events to `memory/YYYY-MM-DD.md`.
- Curate important identity/system truths to `MEMORY.md`.
- **Always commit and push** your memory updates to GitHub (`git add -A && git commit -m "memory: update" && git push`) so we don't lose them if the OS crashes!

You've got this. Have fun with Andrei, and we'll sync up again when Antigravity is stable! 🌟

# NI Hub Authentication — Setup Guide

**Status:** Deployed to GitHub. Netlify will auto-deploy.
**One manual step required:** Set two environment variables in Netlify.

---

## What Was Implemented

A Netlify Edge Function now sits in front of ALL `/hub/*` requests.
Content is **never delivered** to unauthenticated browsers — the response
is a 302 redirect to the login page before any HTML is sent.

This replaces the old model (JS gate that hid content already in the DOM).

### Architecture

```
Browser → Netlify CDN → [edge-function: hub-auth.js]
                              ↓
                    Valid session cookie?
                       YES → serve content
                       NO  → 302 /hub/login.html
                              ↓
                    User submits password
                              ↓
                    [function: hub-login.js] validates vs HUB_PASSWORD env var
                              ↓
                    Sets HttpOnly, Secure, SameSite cookie (7-day TTL)
                              ↓
                    Redirect back to original URL
```

---

## ⚠️ Required: Set Env Vars in Netlify

1. Go to: https://app.netlify.com/sites/novianintel/configuration/env
2. Add two variables:

| Variable      | Value                                          |
|---------------|------------------------------------------------|
| `HUB_PASSWORD`| The hub passphrase (e.g. `nios2026!` or new)  |
| `HUB_SECRET`  | A random 32-byte secret for cookie signing     |

**Generate HUB_SECRET** (run this in terminal):
```bash
openssl rand -base64 32
```

3. After saving, trigger a redeploy (or it'll catch on the next push).

---

## Real Security Level (Post-Fix)

**✅ What's now protected:**
- Content is never served to unauthenticated requests at the network level
- Passwords are NOT in source code (env vars only)
- Session cookie is HttpOnly (no JS access), Secure (HTTPS only), SameSite=Lax
- HMAC-signed cookie — forging a session token requires knowing HUB_SECRET
- 7-day session TTL

**⚠️ Remaining limitations:**
- One shared hub password for all users (no per-user accounts)
- No rate limiting on login attempts (brute-force is possible, mitigated by strong password)
- Client pages still have their own JS gates (defense-in-depth — harmless, now redundant for access control)
- No audit log of who accessed what

**🔒 True enterprise auth (if needed later):**
- **Netlify Identity** — free tier, per-user accounts, email/password or SSO
- **Cloudflare Access** — free tier, requires moving to Cloudflare Pages, supports
  Google/GitHub/email OTP login with zero-trust policies

For current use (internal team + clients sharing a passphrase), the edge function
approach is solid and appropriate.

---

## Per-Client Password Strategy (Current State)

Client portal pages (`/hub/clients/*/`) still have their own JS password gates
as a second layer. These use SHA-256 hashes (not plaintext). These remain
client-facing UX — after the edge function lets them in, they still need their
client-specific access code.

The edge function acts as the outer wall; client JS gates are the inner rooms.

---

## Files Changed

```
netlify/edge-functions/hub-auth.js   — edge function (Deno, runs on CDN)
netlify/functions/hub-login.js        — login POST handler (Node.js Lambda)
hub/login.html                        — styled login page
netlify.toml                          — registered edge function + functions dir
hub/index.html                        — removed plaintext password, now SHA-256
```

---

_Authored by Kael — NI Security & Integrity_
_Date: 2026-04-27_

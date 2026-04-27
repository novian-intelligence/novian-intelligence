# CLIENT PORTAL PLATFORM PLAN
**Prepared by:** Kael — NI Security & Integrity  
**Date:** April 27, 2026  
**Status:** URGENT — Decision Required Today  
**Context:** 8 client portals were running on Netlify with client-side-only JS password gates. This means no real server-side authentication existed. Portals contained sensitive business data (playbooks, strategies, financials, research) for clients: Cassie, Fenix (Jason), Jon Simon, Dr. Nea North, Max, Hivelocity, Soft Life Supply Co., and Yoli's Joy.

---

## The Core Problem (Plain English)

The old Netlify setup had a "fake lock" — it looked like a password was protecting each portal, but the actual files were fully accessible to anyone who knew (or guessed) the URL. It's like putting a "no entry" sign on a door with no lock.

The replacement needs a **real lock** — meaning the server itself refuses to hand over any content unless the user has logged in with verified credentials.

---

## Option Evaluations

---

### 1. Notion — Shared Pages with Invite-Only Access

**What it is:** A workspace/docs app where you can share individual pages with specific email addresses. Clients get a Notion account and you invite them to their page only.

**How secure is it really?**  
Genuinely secure. Notion's sharing is server-side — if someone isn't invited, they get nothing. Invite-only means each client can only see what you've explicitly shared with them. This is real authentication backed by Notion's infrastructure.

**How hard to set up?**  
Very easy. Create a page per client, share it to their email. Done in an afternoon. No coding.

**Cost:**  
Free for basic use. Notion Plus is $10/month if you want more advanced features. For this use case, free probably works.

**Appropriate for this use case?**  
Mostly yes. The security is real. The look is clean and professional. The limitation: it looks like Notion, not like your branded portal. Clients will notice they're in a "Notion workspace." For some clients that's fine; for others who expect a polished branded experience, it may feel informal. Also, no custom domain.

**Verdict:** ✅ Secure | ⚠️ Limited branding | ✅ Free | ✅ Easy

---

### 2. Google Drive / Google Docs — Shared Folders Per Client

**What it is:** Google's file storage and docs suite. You create a folder per client, share it to their Gmail/Google account, and they access it via Google Drive.

**How secure is it really?**  
Secure, with caveats. Google's sharing is server-side — only people you explicitly share with can access files. However: if clients share links accidentally, or you use "anyone with link" instead of "specific people," security breaks. Done correctly (shared to specific email only), it's solid.

**How hard to set up?**  
Very easy. Create a folder per client, upload documents, share to their email. An hour of work max.

**Cost:**  
Free (personal Google account) or $6–$12/month for Google Workspace. For a small consultancy, personal accounts work fine.

**Appropriate for this use case?**  
Functionally yes, but aesthetically it feels like you're just giving them a Google Drive folder. For a consultant selling high-value strategy work, "here's your Google Drive link" can undercut the premium positioning. There's also no central portal feel — it's just file storage.

**Verdict:** ✅ Secure | ⚠️ Not professional-looking | ✅ Free/cheap | ✅ Easy

---

### 3. Webflow + Memberstack — Custom Site with Real Auth

**What it is:** Webflow is a no-code website builder. Memberstack adds real login/membership functionality on top. Together they can create a fully branded client portal.

**How secure is it really?**  
Secure. Memberstack provides real server-side authentication. Content is gated properly.

**How hard to set up?**  
Significant effort for a non-developer. Webflow has a learning curve. Memberstack requires configuration, setting up member plans, assigning content restrictions. Expect 2–5 days of focused work to do it right, and ongoing maintenance when things need updating.

**Cost:**  
Webflow Basic: ~$23/month. Memberstack Starter: ~$29/month. Total: **~$52/month minimum**, more as you scale.

**Appropriate for this use case?**  
Overkill right now. This is the right solution if you're building a polished product or have many clients. For 8 clients as a solo consultant, the setup complexity and ongoing maintenance burden isn't worth it when simpler options deliver equal security.

**Verdict:** ✅ Secure | ✅ Very professional | 🔴 Hard to set up | 💸 $52+/month

---

### 4. Softr — No-Code Client Portal Builder

**What it is:** A no-code tool that lets you build web apps and client portals connected to Airtable or Google Sheets as the data source. Has built-in user authentication.

**How secure is it really?**  
Secure. Authentication is server-side. You control who sees what by assigning users to groups.

**How hard to set up?**  
Medium. Easier than Webflow + Memberstack, but you'll need to understand how Airtable/Sheets works as a backend, and how Softr's user/group permissions work. Expect a full weekend to get it working properly.

**Cost:**  
Free tier is very limited. Paid starts at ~$49/month for the Basic plan. You'd likely need the Professional tier (~$135/month) for white-labeling and more clients.

**Appropriate for this use case?**  
Good if you want something custom-feeling without full development. But requires learning Softr AND Airtable/Sheets as a system. For 8 clients today, it's more infrastructure than you need.

**Verdict:** ✅ Secure | ✅ Professional | ⚠️ Medium setup | 💸 $49–$135/month

---

### 5. Copilot (usecop.io) — Purpose-Built Client Portal SaaS

**What it is:** A SaaS product built specifically for freelancers and consultants to give clients a dedicated portal. Includes file sharing, messaging, forms, invoices, and contracts — all per client, all behind real login.

**How secure is it really?**  
Secure. Built on real authentication — clients log in with email/password or magic link. Each client only sees their portal. No shared links, no guessable URLs.

**How hard to set up?**  
Very easy. It's designed for non-technical founders. Add a client, invite them by email, upload their files. You're done in hours. Has a custom domain option so it looks like your brand.

**Cost:**  
~$29/month (Starter, up to 3 clients) — but you have 8 clients, so you'd need the Basic plan at ~$69/month or Professional at ~$119/month. Pricing can shift, verify at usecop.io.

**Appropriate for this use case?**  
Yes. This is the closest thing to "exactly what Andrei needs." It's made for this exact scenario: solo consultant, multiple clients, needs to look professional, doesn't want to build anything.

**Verdict:** ✅ Secure | ✅ Professional | ✅ Easy | 💸 ~$69–$119/month

---

### 6. Clinked or Portal.io — Client Portal SaaS Tools

**What it is:** Both are client portal platforms similar to Copilot but more enterprise-oriented. Clinked offers team collaboration, file sharing, and client spaces. Portal.io is lighter-weight.

**How secure is it really?**  
Both use real server-side authentication. Secure.

**How hard to set up?**  
Moderate. Both have onboarding flows but are slightly more complex than Copilot.

**Cost:**  
Clinked: ~$83–$119/month. Portal.io: ~$49/month.

**Appropriate for this use case?**  
Portal.io is a reasonable alternative to Copilot at a lower price. Clinked leans enterprise and is likely more than needed. Neither has the polish or non-technical UX that Copilot has specifically built for freelancers/consultants.

**Verdict:** ✅ Secure | ✅ Professional | ⚠️ Medium ease | 💸 $49–$119/month

---

### 7. Password-Protected PDFs — Simplest Possible

**What it is:** Export your content as PDFs, encrypt them with a password, email them to clients. Adobe Acrobat and free tools like LibreOffice can do this.

**How secure is it really?**  
Depends. PDF password encryption is real — a properly encrypted PDF is genuinely protected if you use a strong password. But: it's not access-controlled in real time. Once you send it, you can't revoke access. If a client forwards the PDF and password, you have no visibility or control. Also, PDF security has had historical vulnerabilities with older encryption standards (RC4) — you must use AES-256 encryption.

**How hard to set up?**  
Very easy. Export → encrypt → email. Five minutes per client.

**Cost:**  
Free (LibreOffice) or ~$20/month (Adobe Acrobat).

**Appropriate for this use case?**  
Acceptable as an emergency bridge while you set up a real solution. Not appropriate as a permanent platform — you lose versioning, access control, and the ability to update content without resending. Also looks unprofessional for ongoing consulting relationships.

**Verdict:** ⚠️ Adequate security | 🔴 Not professional | ✅ Free | ✅ Easiest

---

### 8. Rebuild on Netlify with Netlify Identity

**What it is:** Stay on Netlify, but add Netlify Identity — their built-in authentication service that provides real server-side user management and role-based access.

**How secure is it really?**  
If done correctly, secure. Netlify Identity is real auth backed by GoTrue (Auth0-derived). The key word is "if done correctly" — this requires proper serverless function setup to protect routes, which involves real development work.

**How hard to set up?**  
For a non-developer: hard. You'd need to rebuild the site architecture to use protected serverless functions or Netlify's edge middleware. This is not a weekend project without developer help.

**Cost:**  
Netlify Identity is free up to 1,000 users. But you'd likely need a developer to implement it properly (one-time cost of a few hours of dev work).

**Appropriate for this use case?**  
Not recommended without hiring someone to implement it. The risk is rebuilding it wrong again. Given the options above, there's no good reason to add developer complexity when simpler solutions exist.

**Verdict:** ✅ Can be secure | ✅ Stays on familiar ground | 🔴 Requires developer | ⚠️ Risky if done wrong

---

## The Recommendation

### 🏆 Go with Copilot (usecop.io)

**Why Copilot, not the others:**

- It was literally built for your situation: solo consultant, multiple clients, needs to look premium, not a developer.
- Setup is measured in hours, not days or weeks.
- Real authentication — not a workaround or a hack.
- Each client gets their own branded space. You can use your custom domain. It looks like you built something intentional.
- Handles files, messaging, and eventually invoices/contracts — all in one place. That's an upgrade, not just a replacement.
- The cost (~$69–$119/month) is real money, but for a consultancy charging clients premium rates, this is a business expense that protects the business.

**For the next 24–48 hours while you get Copilot set up:**  
Send clients a brief note (template below) and either temporarily password-protect the PDFs of their most sensitive content or take the exposed Netlify pages offline entirely until the new portal is ready.

**Migration path:**
1. Sign up for Copilot today (usecop.io)
2. Add each of your 8 clients as users — they'll get an email invite
3. Upload their portal content to their individual spaces
4. Verify each client can log in and see only their content
5. Take down (or delete) the old Netlify pages
6. Done.

---

## What to Tell Clients

This is the part that matters most. Here's honest language Andrei can actually use:

---

**Email/message template:**

> Hi [Client Name],
>
> I want to be transparent with you about something regarding your client portal.
>
> I recently discovered that the portal platform I was using had a technical vulnerability — the password protection it used was implemented in a way that didn't provide the security I intended. In plain terms: the files could potentially have been accessed without the password if someone knew or guessed the URL directly.
>
> I have no evidence that your portal was accessed by anyone unauthorized. There are no logs indicating outside access, and the URLs were not publicly listed anywhere. But I can't tell you with certainty that it wasn't accessed, and I owe you honesty about that.
>
> I've taken the old portals offline and I'm moving everything to a new platform that uses proper, server-side security. You'll receive a new invite link shortly with secure access to your materials.
>
> I'm sorry this happened. I take the security of your business information seriously, and I'm committed to making sure this is handled properly going forward. If you have questions or concerns, please reach out directly — I'm happy to talk through it.
>
> — Andrei

---

**If they ask follow-up questions:**

- *"Was my data stolen?"* → "I have no evidence of that. There are no access logs showing unauthorized access. But I can't rule it out completely, and I didn't want to downplay the situation."
- *"What data was exposed?"* → Be specific about what each client's portal contained. Don't generalize. They deserve to know exactly what was at risk.
- *"Should I be worried?"* → "The information was consultant strategy and business materials — not passwords, credit cards, or personal financial data. The risk profile is lower than a banking breach, but I still take it seriously because it's your confidential business strategy."
- *"What are you doing to prevent this?"* → Explain Copilot and real auth. Show them you've thought it through.

---

## Summary Checklist — Today

- [ ] Take all exposed Netlify portals offline NOW (or delete the pages)
- [ ] Sign up for Copilot at usecop.io
- [ ] Create client spaces for all 8 clients
- [ ] Send honest notification to all 8 clients (use template above)
- [ ] Upload content per-client to Copilot
- [ ] Verify each client can log in
- [ ] Confirm old Netlify pages are fully removed
- [ ] Document this incident in internal records

---

*Prepared by Kael — NI Security & Integrity*  
*This document is internal. Do not share with clients.*

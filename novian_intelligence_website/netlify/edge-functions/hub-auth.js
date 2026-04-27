/**
 * hub-auth.js — Netlify Edge Function
 * Protects all /hub/* paths with server-side cookie auth.
 * Content is NEVER served to unauthenticated requests.
 *
 * Env vars required (Netlify UI → Site config → Environment variables):
 *   HUB_SECRET    — random secret for HMAC signing (openssl rand -base64 32)
 *   HUB_PASSWORD  — the hub passphrase
 */

const COOKIE_NAME = "ni_hub_session";
const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000;

const EXEMPT = ["/hub/login", "/hub/login.html"];

export default async function handler(request, context) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Allow login page through
  if (EXEMPT.some(p => path === p || path.startsWith(p + "?"))) {
    return context.next();
  }

  // Allow Netlify function calls through
  if (path.startsWith("/.netlify/")) {
    return context.next();
  }

  const secret = Netlify.env.get("HUB_SECRET");

  if (!secret) {
    return new Response(
      `<html><body style="font-family:monospace;padding:2rem;background:#0a0a0a;color:#ff4444">
        <h2>⚠️ Hub Not Configured</h2>
        <p>HUB_SECRET environment variable is not set.</p>
        <p>Contact the site administrator.</p>
      </body></html>`,
      { status: 503, headers: { "Content-Type": "text/html" } }
    );
  }

  // Check session cookie
  const cookieHeader = request.headers.get("cookie") || "";
  const token = getCookieValue(cookieHeader, COOKIE_NAME);

  if (token && await verifyToken(token, secret)) {
    return context.next();
  }

  // Not authenticated — redirect to login
  const next = encodeURIComponent(path + url.search);
  return Response.redirect(`${url.origin}/hub/login.html?next=${next}`, 302);
}

function getCookieValue(header, name) {
  for (const part of header.split(";")) {
    const [k, ...rest] = part.trim().split("=");
    if (k.trim() === name) return rest.join("=").trim();
  }
  return null;
}

async function verifyToken(token, secret) {
  try {
    const dotIdx = token.indexOf(".");
    if (dotIdx === -1) return false;
    const tsB64 = token.slice(0, dotIdx);
    const sigB64 = token.slice(dotIdx + 1);
    const ts = parseInt(atob(tsB64), 10);
    if (isNaN(ts) || Date.now() - ts > SESSION_TTL_MS) return false;
    const expected = await hmacSign(secret, tsB64);
    return timingSafeEqual(sigB64, expected);
  } catch {
    return false;
  }
}

async function hmacSign(secret, data) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  return btoa(String.fromCharCode(...new Uint8Array(sig)));
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export const config = { path: "/hub/*" };

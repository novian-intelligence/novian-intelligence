/**
 * hub-auth.js — Netlify Edge Function
 * Protects all /hub/* paths with server-side cookie auth.
 * Content is NEVER served to unauthenticated requests.
 *
 * Env vars required (set in Netlify UI → Site Settings → Environment):
 *   HUB_SECRET  — random secret for HMAC cookie signing (generate with: openssl rand -base64 32)
 *
 * Token format: base64(timestamp) + "." + base64(HMAC-SHA256(secret, base64(timestamp)))
 * Session valid for 7 days.
 */

const COOKIE_NAME = "ni_hub_session";
const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

// Paths exempt from auth (login page itself)
const EXEMPT_PATHS = ["/hub/login.html", "/hub/login"];

export default async function handler(request, context) {
  const url = new URL(request.url);

  // Allow the login page through
  if (EXEMPT_PATHS.some(p => url.pathname === p || url.pathname.startsWith(p + "?"))) {
    return context.next();
  }

  const secret = Deno.env.get("HUB_SECRET");
  if (!secret) {
    // Misconfigured — fail closed (block access, don't leak content)
    return new Response(
      "Hub authentication is not configured. Contact Andrei.",
      { status: 503, headers: { "Content-Type": "text/plain" } }
    );
  }

  // Check for valid session cookie
  const cookieHeader = request.headers.get("cookie") || "";
  const token = getCookieValue(cookieHeader, COOKIE_NAME);

  if (token && await verifyToken(token, secret)) {
    return context.next();
  }

  // No valid session — redirect to login
  const next = encodeURIComponent(url.pathname + url.search);
  const loginUrl = `${url.origin}/hub/login.html?next=${next}`;
  return Response.redirect(loginUrl, 302);
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

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

    // Check timestamp
    const ts = parseInt(atob(tsB64), 10);
    if (isNaN(ts) || Date.now() - ts > SESSION_TTL_MS) return false;

    // Verify HMAC
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
  const sig = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(data)
  );
  return btoa(String.fromCharCode(...new Uint8Array(sig)));
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}

export const config = { path: "/hub/*" };

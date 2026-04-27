/**
 * hub-login.js — Netlify Serverless Function
 * POST handler for /hub login. Validates password, issues a signed session cookie.
 *
 * Env vars required (set in Netlify UI → Site Settings → Environment):
 *   HUB_PASSWORD — the passphrase for /hub access
 *   HUB_SECRET   — random signing secret (same as used in edge function)
 *
 * Flow:
 *   POST /.netlify/functions/hub-login
 *   Body: application/x-www-form-urlencoded  { password, next }
 *   → On success: 302 to `next` (sanitised to /hub/*), Set-Cookie: ni_hub_session
 *   → On failure: 302 back to login page with ?error=1
 */

const crypto = require("crypto");

const COOKIE_NAME  = "ni_hub_session";
const COOKIE_MAX_AGE = 7 * 24 * 60 * 60; // seconds

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const body      = new URLSearchParams(event.body || "");
  const password  = body.get("password") || "";
  const nextRaw   = body.get("next")     || "/hub/";

  // Sanitise `next` — only allow redirecting within /hub/
  const next = nextRaw.startsWith("/hub") ? nextRaw : "/hub/";

  const hubPassword = process.env.HUB_PASSWORD;
  const hubSecret   = process.env.HUB_SECRET;

  if (!hubPassword || !hubSecret) {
    return {
      statusCode: 503,
      body: "Server configuration error — HUB_PASSWORD / HUB_SECRET not set.",
    };
  }

  if (password !== hubPassword) {
    return {
      statusCode: 302,
      headers: {
        Location: `/hub/login.html?next=${encodeURIComponent(next)}&error=1`,
      },
      body: "",
    };
  }

  // Issue signed session token
  const tsB64 = Buffer.from(Date.now().toString()).toString("base64");
  const sig   = crypto
    .createHmac("sha256", hubSecret)
    .update(tsB64)
    .digest("base64");
  const token = `${tsB64}.${sig}`;

  return {
    statusCode: 302,
    headers: {
      Location: next,
      "Set-Cookie": [
        `${COOKIE_NAME}=${token}`,
        "Path=/hub",
        "HttpOnly",
        "Secure",
        "SameSite=Lax",
        `Max-Age=${COOKIE_MAX_AGE}`,
      ].join("; "),
    },
    body: "",
  };
};

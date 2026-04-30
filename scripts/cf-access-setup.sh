#!/usr/bin/env bash
# ============================================================
# Cloudflare Access — Client Portal Setup Script
# NI Security | Author: Kael
# ============================================================
# USAGE:
#   export CF_API_TOKEN="your_token_here"
#   bash cf-access-setup.sh
#
# Required token permissions:
#   - Access: Apps and Policies (Edit)
#   - Zone: Zone (Read)  [optional but helpful]
#
# To create a token: https://dash.cloudflare.com/profile/api-tokens
# Use template "Edit Cloudflare Access" or create custom with above perms.
# ============================================================

set -euo pipefail

ACCOUNT_ID="1861cf75c09ee90b8d95fb81f5b907f1"
DOMAIN="novianintel.com"
SESSION_DURATION="24h"

if [[ -z "${CF_API_TOKEN:-}" ]]; then
  echo "❌ ERROR: CF_API_TOKEN not set."
  echo "   Export it: export CF_API_TOKEN='your_token_here'"
  exit 1
fi

API="https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/access/apps"
AUTH_HEADER="Authorization: Bearer ${CF_API_TOKEN}"

# ---- helpers ----
create_app() {
  local name="$1"
  local path="$2"
  echo "→ Creating app: ${name} (${path})"
  local response
  response=$(curl -s -X POST "${API}" \
    -H "${AUTH_HEADER}" \
    -H "Content-Type: application/json" \
    --data "{
      \"name\": \"${name}\",
      \"domain\": \"${DOMAIN}${path}\",
      \"type\": \"self_hosted\",
      \"session_duration\": \"${SESSION_DURATION}\",
      \"auto_redirect_to_identity\": false,
      \"allowed_idps\": [],
      \"app_launcher_visible\": false,
      \"enable_binding_cookie\": false,
      \"http_only_cookie_attribute\": true,
      \"same_site_cookie_attribute\": \"lax\"
    }")
  local success
  success=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('success','false'))")
  if [[ "$success" != "True" && "$success" != "true" ]]; then
    echo "  ❌ Failed to create app ${name}:"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    return 1
  fi
  local app_id
  app_id=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['id'])")
  echo "  ✅ App created: ${app_id}"
  echo "$app_id"
}

create_policy() {
  local app_id="$1"
  local name="$2"
  shift 2
  local emails=("$@")

  # Build include array: one email rule per allowed address
  local include_json=""
  for email in "${emails[@]}"; do
    if [[ -n "$include_json" ]]; then include_json+=","; fi
    include_json+="{\"email\":{\"email\":\"${email}\"}}"
  done

  echo "  → Creating policy for: ${emails[*]}"
  local response
  response=$(curl -s -X POST "${API}/${app_id}/policies" \
    -H "${AUTH_HEADER}" \
    -H "Content-Type: application/json" \
    --data "{
      \"name\": \"${name} - Allowed Users\",
      \"decision\": \"allow\",
      \"include\": [${include_json}],
      \"require\": [],
      \"exclude\": [],
      \"precedence\": 1
    }")
  local success
  success=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('success','false'))")
  if [[ "$success" != "True" && "$success" != "true" ]]; then
    echo "  ❌ Failed to create policy for ${name}:"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    return 1
  fi
  local policy_id
  policy_id=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['id'])")
  echo "  ✅ Policy created: ${policy_id}"
}

# ============================================================
# CLIENT DEFINITIONS
# ============================================================

echo ""
echo "======================================================"
echo " Novian Intelligence — Cloudflare Access Setup"
echo "======================================================"
echo ""

RESULTS=()

run_client() {
  local slug="$1"
  local display="$2"
  shift 2
  local emails=("$@")

  echo "📁 [${display}] /clients/${slug}/*"
  local app_id
  app_id=$(create_app "NI Portal — ${display}" "/clients/${slug}/*")
  if [[ -z "$app_id" ]]; then
    RESULTS+=("❌ ${display}: App creation FAILED")
    return
  fi
  if create_policy "$app_id" "${display}" "${emails[@]}"; then
    RESULTS+=("✅ ${display}: App + Policy created (app: ${app_id})")
  else
    RESULTS+=("⚠️  ${display}: App created (${app_id}) but Policy FAILED")
  fi
  echo ""
}

# 1. Cassie
run_client "cassie" "Cassie" \
  "hello@soundsbycassandra.com" \
  "hello@andreimatei.com"

# 2. Fenix
run_client "fenix" "Fenix" \
  "jason.a.cuellar@gmail.com" \
  "hello@andreimatei.com"

# 3. Jon Simon
run_client "jonsimon" "Jon Simon" \
  "djgatsby@gmail.com" \
  "hello@andreimatei.com"

# 4. NEA
run_client "nea" "NEA" \
  "neanorth@gmail.com" \
  "hello@andreimatei.com"

# 5. Soft Life
run_client "softlife" "Soft Life" \
  "hello@andreimatei.com"

# 6. Max
run_client "max" "Max" \
  "hello@andreimatei.com"

# 7. Hivelocity
run_client "hivelocity" "Hivelocity" \
  "amatei@hivelocity.net" \
  "hello@andreimatei.com"

# 8. Yolis Joy
run_client "yolisjoy" "Yolis Joy" \
  "hello@andreimatei.com"

# ============================================================
# SUMMARY
# ============================================================
echo "======================================================"
echo " RESULTS"
echo "======================================================"
for r in "${RESULTS[@]}"; do
  echo "  $r"
done
echo ""
echo "Done. Visit https://one.dash.cloudflare.com/novianintelligence/access/apps to verify."

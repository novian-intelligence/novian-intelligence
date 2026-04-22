#!/usr/bin/env bash
# =============================================================================
# publish-brief.sh — NI Morning Brief Publisher
# Usage: ./publish-brief.sh ai_briefs/YYYY-MM-DD.html [--dry-run]
# =============================================================================
set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
BRIEF_FILE="${1:-}"
DRY_RUN=false
[[ "${2:-}" == "--dry-run" ]] && DRY_RUN=true

# ── Colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

log()  { echo -e "${CYAN}▸${RESET} $*"; }
ok()   { echo -e "${GREEN}✓${RESET} $*"; }
warn() { echo -e "${YELLOW}⚠${RESET}  $*"; }
die()  { echo -e "${RED}✗${RESET}  $*" >&2; exit 1; }

# ── Validate input ────────────────────────────────────────────────────────────
[[ -z "$BRIEF_FILE" ]] && die "Usage: $0 ai_briefs/YYYY-MM-DD.html [--dry-run]"
[[ ! -f "$SITE_DIR/$BRIEF_FILE" ]] && die "File not found: $SITE_DIR/$BRIEF_FILE"

BRIEF_PATH="$SITE_DIR/$BRIEF_FILE"
BRIEF_BASENAME="$(basename "$BRIEF_FILE")"          # e.g. 2026-04-22.html
BRIEF_SLUG="${BRIEF_BASENAME%.html}"                # e.g. 2026-04-22

# ── Extract metadata via Python (handles quotes safely) ───────────────────────
log "Extracting metadata from $BRIEF_BASENAME..."

TMP_META=$(mktemp /tmp/brief-meta-XXXX.json)

python3 - "$BRIEF_PATH" "$SITE_DIR/ai_briefs/briefs.html" "$BRIEF_BASENAME" "$BRIEF_SLUG" > "$TMP_META" <<'PYEOF'
import sys, re, json

brief_path   = sys.argv[1]
briefs_index = sys.argv[2]
brief_basename = sys.argv[3]
brief_slug   = sys.argv[4]

with open(brief_path, 'r') as f:
    brief_html = f.read()

# Extract title from <h1 class="article-title">
m = re.search(r'<h1 class="article-title">(.*?)</h1>', brief_html, re.DOTALL)
full_title = m.group(1).strip() if m else ''
full_title = full_title.replace('&amp;', '&').replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&mdash;', '—')

# Extract description from meta
m = re.search(r'name="description" content="([^"]*)"', brief_html)
brief_desc = m.group(1) if m else ''

# Parse date from slug
parts = brief_slug.split('-')
year, month_num, day = parts[0], parts[1], parts[2]
month_names = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
               '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
month_name = month_names.get(month_num, month_num)
day_num = str(int(day))
full_date = f"{month_name} {day_num}, {year}"
short_date = f"{month_name} {day_num}"

# Extract tags
tag_matches = re.findall(r'class="story-cat cat-([a-z]+)">([^<]+)<', brief_html)
tag_html = ''
for cat_class, label in tag_matches[:3]:
    tag_html += f'            <span class="tag tag-{cat_class}">{label.strip()}</span>\n'

# Get current featured brief info from briefs.html
with open(briefs_index, 'r') as f:
    briefs_html = f.read()

current_count = len(re.findall(r'class="brief-row"', briefs_html))

m = re.search(r'href="([0-9][^"]*\.html)" class="featured-card"', briefs_html)
old_href = m.group(1) if m else ''

m = re.search(r'<h2 class="featured-title">([^<]*)</h2>', briefs_html)
old_title = m.group(1) if m else ''

m = re.search(r'class="featured-card".*?(<div class="brief-tags">.*?</div>)', briefs_html, re.DOTALL)
old_tags = m.group(1) if m else ''
# Flatten to single line of span tags
old_tag_spans = re.findall(r'<span class="tag[^"]*">[^<]*</span>', old_tags)
old_tags_html = '\n                '.join(old_tag_spans)

# Parse old slug for date
old_slug = old_href.replace('.html', '') if old_href else ''
if old_slug:
    op = old_slug.split('-')
    old_month_name = month_names.get(op[1], op[1]) if len(op) >= 3 else ''
    old_day_num = str(int(op[2])) if len(op) >= 3 else ''
else:
    old_month_name = ''
    old_day_num = ''

result = {
    'full_title': full_title,
    'brief_desc': brief_desc,
    'full_date': full_date,
    'short_date': short_date,
    'tag_html': tag_html,
    'current_count': current_count,
    'new_count': current_count + 1,
    'old_href': old_href,
    'old_title': old_title,
    'old_tags_html': old_tags_html,
    'old_month_name': old_month_name,
    'old_day_num': old_day_num,
    'brief_basename': brief_basename,
    'brief_slug': brief_slug,
    'short_date': short_date,
}
print(json.dumps(result))
PYEOF

# Read back metadata for shell display
FULL_TITLE=$(python3 -c "import json,sys; d=json.load(open('$TMP_META')); print(d['full_title'])")
BRIEF_DESC=$(python3 -c "import json,sys; d=json.load(open('$TMP_META')); print(d['brief_desc'])")
FULL_DATE=$(python3 -c "import json,sys; d=json.load(open('$TMP_META')); print(d['full_date'])")
SHORT_DATE=$(python3 -c "import json,sys; d=json.load(open('$TMP_META')); print(d['short_date'])")
NEW_COUNT=$(python3 -c "import json,sys; d=json.load(open('$TMP_META')); print(d['new_count'])")
OLD_HREF=$(python3 -c "import json,sys; d=json.load(open('$TMP_META')); print(d['old_href'])")

echo ""
echo -e "${BOLD}Brief metadata:${RESET}"
echo "  Slug:    $BRIEF_SLUG"
echo "  Date:    $FULL_DATE"
echo "  Title:   ${FULL_TITLE:0:80}..."
echo "  Desc:    ${BRIEF_DESC:0:80}..."
echo ""

log "Current featured: $OLD_HREF → will be demoted to archive"
log "New brief count: $NEW_COUNT"

# ── Dry run preview ───────────────────────────────────────────────────────────
if $DRY_RUN; then
  echo ""
  warn "DRY RUN — no files will be changed"
  echo ""
  echo -e "${BOLD}Would update:${RESET}"
  echo "  1. index.html — homepage featured card → $BRIEF_SLUG"
  echo "  2. ai_briefs/briefs.html — featured card → $BRIEF_SLUG"
  echo "  3. ai_briefs/briefs.html — stats: $(($NEW_COUNT - 1)) → $NEW_COUNT briefs, Last: $SHORT_DATE"
  echo "  4. ai_briefs/briefs.html — demote $OLD_HREF to archive row 0"
  echo "  5. ai_briefs/briefs.html — re-index all archive data-idx values"
  echo "  6. git add -A && git commit && git push"
  echo ""
  ok "Dry run complete. Run without --dry-run to publish."
  rm -f "$TMP_META"
  exit 0
fi

# ── 1. Update homepage (index.html) ──────────────────────────────────────────
log "Updating homepage featured card..."

HOMEPAGE="$SITE_DIR/index.html"

# Update the brief card link href
sed -i '' "s|href=\"ai_briefs/[^\"]*\" class=\"brief-card\"|href=\"ai_briefs/${BRIEF_BASENAME}\" class=\"brief-card\"|" "$HOMEPAGE"

python3 - "$HOMEPAGE" "$TMP_META" <<'PYEOF'
import re, json, sys

homepage = sys.argv[1]
meta = json.load(open(sys.argv[2]))

with open(homepage, 'r') as f:
    content = f.read()

# Update brief-label
content = re.sub(
    r'<div class="brief-label">Latest · [^<]*</div>',
    f'<div class="brief-label">Latest · {meta["full_date"]}</div>',
    content
)

# Update brief-title
content = re.sub(
    r'<div class="brief-title">NI Morning Brief[^<]*</div>',
    f'<div class="brief-title">NI Morning Brief — {meta["full_title"]}</div>',
    content
)

# Update brief-desc
content = re.sub(
    r'<div class="brief-desc">.*?</div>',
    f'<div class="brief-desc">{meta["brief_desc"]}</div>',
    content,
    flags=re.DOTALL,
    count=1
)

with open(homepage, 'w') as f:
    f.write(content)
print("homepage updated")
PYEOF

ok "Homepage updated"

# ── 2 & 3 & 4 & 5. Update briefs.html ────────────────────────────────────────
log "Updating briefs index..."

BRIEFS_INDEX="$SITE_DIR/ai_briefs/briefs.html"

python3 - "$BRIEFS_INDEX" "$TMP_META" <<'PYEOF'
import re, json, sys

briefs_index = sys.argv[1]
meta = json.load(open(sys.argv[2]))

with open(briefs_index, 'r') as f:
    content = f.read()

# ── Stats: brief count ──
content = re.sub(
    r'(<span class="hero-stat-lbl">Briefs published</span>\s*<span class="hero-stat-num">)\d+(</span>)',
    r'\g<1>' + str(meta['new_count']) + r'\2',
    content
)

# ── Stats: last brief date ──
content = re.sub(
    r'(<span class="hero-stat-lbl">Last brief</span>\s*<span class="hero-stat-num">)[^<]*(</span>)',
    r'\g<1>' + meta['short_date'] + r'\2',
    content
)

# ── Featured card: update href ──
content = re.sub(
    r'href="[^"]*\.html" class="featured-card"',
    f'href="{meta["brief_basename"]}" class="featured-card"',
    content
)

# ── Featured card: update date display ──
content = re.sub(
    r'(<div class="featured-date">\s*)([A-Za-z]+ \d+, \d+)(\s*<span class="latest-badge">)',
    r'\g<1>' + meta['full_date'] + r'\3',
    content
)

# ── Featured card: update title ──
content = re.sub(
    r'<h2 class="featured-title">[^<]*</h2>',
    f'<h2 class="featured-title">{meta["full_title"]}</h2>',
    content
)

# ── Featured card: update description ──
content = re.sub(
    r'(<p class="featured-desc">).*?(</p>)',
    r'\g<1>' + meta['brief_desc'] + r'\2',
    content,
    flags=re.DOTALL,
    count=1
)

# ── Featured card: update meta date ──
content = re.sub(
    r'(<div class="featured-meta">\s*<span>)[A-Za-z]+ \d+, \d+(</span>)',
    r'\g<1>' + meta['full_date'] + r'\2',
    content,
    count=1
)

# ── Featured card: update tags ──
tag_html = meta['tag_html']
content = re.sub(
    r'(<div class="brief-tags">).*?(</div>)',
    r'\g<1>\n' + tag_html.strip() + r'\n          \2',
    content,
    flags=re.DOTALL,
    count=1
)

# ── Bump all existing archive data-idx by 1 ──
def bump_idx(m):
    old = int(m.group(1))
    return f'data-idx="{old + 1}"'
content = re.sub(r'data-idx="(\d+)"', bump_idx, content)

# ── Build new archive row for old featured brief ──
new_row = f'''          <a data-idx="0" href="{meta['old_href']}" class="brief-row">
            <div class="date-badge">
              <div class="month">{meta['old_month_name']}</div>
              <div class="day">{meta['old_day_num']}</div>
            </div>
            <div class="brief-content">
              <div class="brief-row-title">{meta['old_title']}</div>
              <div class="brief-row-tags">
                {meta['old_tags_html']}
              </div>
            </div>
            <span class="brief-arrow">→</span>
          </a>

          '''

# Insert new archive row at the top of .brief-list
content = re.sub(
    r'(<div class="brief-list">\s*)',
    r'\g<1>' + new_row,
    content,
    count=1
)

with open(briefs_index, 'w') as f:
    f.write(content)
print("briefs index updated")
PYEOF

ok "Briefs index updated"

# ── Cleanup temp file ─────────────────────────────────────────────────────────
rm -f "$TMP_META"

# ── 6. Commit and push ────────────────────────────────────────────────────────
log "Committing and pushing..."

cd "$SITE_DIR"
git add -A
git commit -m "feat: publish NI Morning Brief — ${FULL_DATE}"
git push

echo ""
echo -e "${GREEN}${BOLD}✓ Brief published!${RESET}"
echo -e "  Live at: ${CYAN}https://novianintel.com/ai_briefs/${BRIEF_BASENAME}${RESET}"
echo -e "  Netlify will deploy in ~60 seconds."
echo ""

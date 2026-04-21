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

# ── Extract metadata from the brief ──────────────────────────────────────────
log "Extracting metadata from $BRIEF_BASENAME..."

# Full title from <h1 class="article-title"> (the real headline)
FULL_TITLE=$(grep -o '<h1 class="article-title">[^<]*</h1>' "$BRIEF_PATH" \
  | sed 's/<h1 class="article-title">//;s/<\/h1>//' \
  | sed 's/&amp;/\&/g;s/&ldquo;/"/g;s/&rdquo;/"/g;s/&mdash;/—/g')

# Short title for homepage card (first ~80 chars up to a natural break)
BRIEF_TITLE="$FULL_TITLE"

# Description from <meta name="description" content="...">
BRIEF_DESC=$(grep -o 'name="description" content="[^"]*"' "$BRIEF_PATH" \
  | sed 's/name="description" content="//;s/"//')

# Date from filename
YEAR=$(echo "$BRIEF_SLUG" | cut -d- -f1)
MONTH=$(echo "$BRIEF_SLUG" | cut -d- -f2)
DAY=$(echo "$BRIEF_SLUG" | cut -d- -f3)

# Human-readable month
case "$MONTH" in
  01) MONTH_NAME="Jan" ;; 02) MONTH_NAME="Feb" ;; 03) MONTH_NAME="Mar" ;;
  04) MONTH_NAME="Apr" ;; 05) MONTH_NAME="May" ;; 06) MONTH_NAME="Jun" ;;
  07) MONTH_NAME="Jul" ;; 08) MONTH_NAME="Aug" ;; 09) MONTH_NAME="Sep" ;;
  10) MONTH_NAME="Oct" ;; 11) MONTH_NAME="Nov" ;; 12) MONTH_NAME="Dec" ;;
  *) die "Invalid month in filename: $MONTH" ;;
esac
DAY_NUM="${DAY#0}"  # strip leading zero for display
FULL_DATE="${MONTH_NAME} ${DAY_NUM}, ${YEAR}"       # e.g. Apr 22, 2026
SHORT_DATE="${MONTH_NAME} ${DAY_NUM}"               # e.g. Apr 22

# Extract tags from the brief's story-cat classes
TAGS_RAW=$(grep -o 'class="story-cat cat-[a-z]*">[^<]*<' "$BRIEF_PATH" \
  | sed 's/class="story-cat cat-\([a-z]*\)">\([^<]*\)</cat=\1 label=\2/' \
  | head -3)

# Build tag HTML for featured card (briefs.html format)
TAG_HTML=""
while IFS= read -r tag_line; do
  cat_class=$(echo "$tag_line" | sed 's/cat=\([a-z]*\).*/\1/')
  tag_label=$(echo "$tag_line" | sed 's/.*label=\(.*\)/\1/')
  TAG_HTML+="            <span class=\"tag tag-${cat_class}\">${tag_label}</span>\n"
done <<< "$TAGS_RAW"

echo ""
echo -e "${BOLD}Brief metadata:${RESET}"
echo "  Slug:    $BRIEF_SLUG"
echo "  Date:    $FULL_DATE"
echo "  Title:   $BRIEF_TITLE"
echo "  Desc:    ${BRIEF_DESC:0:80}..."
echo ""

# ── Count current briefs ──────────────────────────────────────────────────────
CURRENT_COUNT=$(grep -c 'class="brief-row"' "$SITE_DIR/ai_briefs/briefs.html" || true)
NEW_COUNT=$((CURRENT_COUNT + 1))

# ── Get current featured brief info (to demote to archive) ───────────────────
OLD_FEATURED_HREF=$(grep -o 'href="[0-9][^"]*\.html" class="featured-card"' \
  "$SITE_DIR/ai_briefs/briefs.html" | grep -o '"[^"]*\.html"' | tr -d '"')
OLD_FEATURED_DATE_FULL=$(grep -A3 'class="featured-card"' "$SITE_DIR/ai_briefs/briefs.html" \
  | grep -o 'April\|February\|March\|January\|May\|June\|July\|August\|September\|October\|November\|December' \
  | head -1)
OLD_FEATURED_TITLE=$(grep -A5 'class="featured-card"' "$SITE_DIR/ai_briefs/briefs.html" \
  | grep -o '<h2 class="featured-title">[^<]*</h2>' \
  | sed 's/<h2 class="featured-title">//;s/<\/h2>//')
OLD_FEATURED_TAGS=$(grep -A20 'class="featured-card"' "$SITE_DIR/ai_briefs/briefs.html" \
  | grep -o '<span class="tag[^"]*">[^<]*</span>' \
  | head -3 | tr '\n' ' ')

# Parse old featured date for archive entry
OLD_SLUG="${OLD_FEATURED_HREF%.html}"
OLD_YEAR=$(echo "$OLD_SLUG" | cut -d- -f1)
OLD_MONTH_NUM=$(echo "$OLD_SLUG" | cut -d- -f2)
OLD_DAY=$(echo "$OLD_SLUG" | cut -d- -f3)
OLD_DAY_NUM="${OLD_DAY#0}"
case "$OLD_MONTH_NUM" in
  01) OLD_MONTH_NAME="Jan" ;; 02) OLD_MONTH_NAME="Feb" ;; 03) OLD_MONTH_NAME="Mar" ;;
  04) OLD_MONTH_NAME="Apr" ;; 05) OLD_MONTH_NAME="May" ;; 06) OLD_MONTH_NAME="Jun" ;;
  07) OLD_MONTH_NAME="Jul" ;; 08) OLD_MONTH_NAME="Aug" ;; 09) OLD_MONTH_NAME="Sep" ;;
  10) OLD_MONTH_NAME="Oct" ;; 11) OLD_MONTH_NAME="Nov" ;; 12) OLD_MONTH_NAME="Dec" ;;
esac

log "Current featured: $OLD_FEATURED_HREF → will be demoted to archive"
log "New brief count: $NEW_COUNT"

# ── Dry run preview ───────────────────────────────────────────────────────────
if $DRY_RUN; then
  echo ""
  warn "DRY RUN — no files will be changed"
  echo ""
  echo -e "${BOLD}Would update:${RESET}"
  echo "  1. index.html — homepage featured card → $BRIEF_SLUG"
  echo "  2. ai_briefs/briefs.html — featured card → $BRIEF_SLUG"
  echo "  3. ai_briefs/briefs.html — stats: $CURRENT_COUNT → $NEW_COUNT briefs, Last: $SHORT_DATE"
  echo "  4. ai_briefs/briefs.html — demote $OLD_FEATURED_HREF to archive row 0"
  echo "  5. ai_briefs/briefs.html — re-index all archive data-idx values"
  echo "  6. git add -A && git commit && git push"
  echo ""
  ok "Dry run complete. Run without --dry-run to publish."
  exit 0
fi

# ── 1. Update homepage (index.html) ──────────────────────────────────────────
log "Updating homepage featured card..."

HOMEPAGE="$SITE_DIR/index.html"

# Update the brief card link href
sed -i '' "s|href=\"ai_briefs/[^\"]*\" class=\"brief-card\"|href=\"ai_briefs/${BRIEF_BASENAME}\" class=\"brief-card\"|" "$HOMEPAGE"

# Update the brief-label date
python3 - <<PYEOF
import re

with open('$HOMEPAGE', 'r') as f:
    content = f.read()

# Update brief-label
content = re.sub(
    r'<div class="brief-label">Latest · [^<]*</div>',
    '<div class="brief-label">Latest · $FULL_DATE</div>',
    content
)

# Update brief-title
content = re.sub(
    r'<div class="brief-title">NI Morning Brief[^<]*</div>',
    '<div class="brief-title">NI Morning Brief — $BRIEF_TITLE</div>',
    content
)

# Update brief-desc
content = re.sub(
    r'<div class="brief-desc">.*?</div>',
    '<div class="brief-desc">$BRIEF_DESC</div>',
    content,
    flags=re.DOTALL,
    count=1
)

with open('$HOMEPAGE', 'w') as f:
    f.write(content)
print("homepage updated")
PYEOF

ok "Homepage updated"

# ── 2 & 3 & 4 & 5. Update briefs.html ────────────────────────────────────────
log "Updating briefs index..."

BRIEFS_INDEX="$SITE_DIR/ai_briefs/briefs.html"

python3 - <<PYEOF
import re

with open('$BRIEFS_INDEX', 'r') as f:
    content = f.read()

# ── Stats: brief count ──
content = re.sub(
    r'(<span class="hero-stat-lbl">Briefs published</span>\s*<span class="hero-stat-num">)\d+(</span>)',
    r'\g<1>$NEW_COUNT\2',
    content
)

# ── Stats: last brief date ──
content = re.sub(
    r'(<span class="hero-stat-lbl">Last brief</span>\s*<span class="hero-stat-num">)[^<]*(</span>)',
    r'\g<1>$SHORT_DATE\2',
    content
)

# ── Featured card: update href ──
content = re.sub(
    r'href="[^"]*\.html" class="featured-card"',
    'href="$BRIEF_BASENAME" class="featured-card"',
    content
)

# ── Featured card: update date display ──
content = re.sub(
    r'(<div class="featured-date">\s*)([A-Za-z]+ \d+, \d+)(\s*<span class="latest-badge">)',
    r'\g<1>$FULL_DATE\3',
    content
)

# ── Featured card: update title ──
content = re.sub(
    r'<h2 class="featured-title">[^<]*</h2>',
    '<h2 class="featured-title">$FULL_TITLE</h2>',
    content
)

# ── Featured card: update description ──
content = re.sub(
    r'(<p class="featured-desc">).*?(</p>)',
    r'\g<1>$BRIEF_DESC\2',
    content,
    flags=re.DOTALL,
    count=1
)

# ── Featured card: update meta date ──
content = re.sub(
    r'(<div class="featured-meta">\s*<span>)[A-Za-z]+ \d+, \d+(</span>)',
    r'\g<1>$FULL_DATE\2',
    content,
    count=1
)

# ── Featured card: update tags ──
tag_html = '$TAG_HTML'
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
new_row = '''          <a data-idx="0" href="$OLD_FEATURED_HREF" class="brief-row">
            <div class="date-badge">
              <div class="month">$OLD_MONTH_NAME</div>
              <div class="day">$OLD_DAY_NUM</div>
            </div>
            <div class="brief-content">
              <div class="brief-row-title">$OLD_FEATURED_TITLE</div>
              <div class="brief-row-tags">
                $OLD_FEATURED_TAGS
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

with open('$BRIEFS_INDEX', 'w') as f:
    f.write(content)
print("briefs index updated")
PYEOF

ok "Briefs index updated"

# ── 6. Commit and push ────────────────────────────────────────────────────────
log "Committing and pushing..."

cd "$SITE_DIR"
git add -A
git commit -m "feat: publish NI Morning Brief — ${FULL_DATE} (${BRIEF_TITLE})"
git push

echo ""
echo -e "${GREEN}${BOLD}✓ Brief published!${RESET}"
echo -e "  Live at: ${CYAN}https://novianintel.com/ai_briefs/${BRIEF_BASENAME}${RESET}"
echo -e "  Cloudflare will deploy in ~60 seconds."
echo ""

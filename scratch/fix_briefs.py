"""
Updates briefs.html:
1. Makes hero full-width with larger title
2. Adds JS client-side pagination (6 per page, hash-based)
"""
import re

path = '/Users/mira/Documents/Novian_Intelligence/novian_intelligence_website/ai_briefs/briefs.html'
with open(path) as f:
    c = f.read()

# ── 1. Enlarge hero title in CSS ─────────────────────────────
c = c.replace(
    '.page-title {\n      font-size: clamp(2.4rem, 5vw, 3.4rem);\n      font-weight: 900; line-height: 1.05;\n      letter-spacing: -0.04em; color: #fff;\n      margin-bottom: 20px;\n    }',
    '.page-title {\n      font-size: clamp(3rem, 6vw, 4.2rem);\n      font-weight: 900; line-height: 1.0;\n      letter-spacing: -0.05em; color: #fff;\n      margin-bottom: 20px;\n    }'
)

# ── 2. Widen the page-hero to feel full-width ─────────────────
c = c.replace(
    '.page-hero { padding: 56px 0 48px; }',
    '.page-hero { padding: 64px 0 56px; border-bottom: 1px solid var(--border); margin-bottom: 48px; }'
)

# Make subtitle slightly larger
c = c.replace(
    '.page-subtitle {\n      font-size: 1rem; line-height: 1.75;\n      color: var(--text-muted); max-width: 520px;\n      font-weight: 400;\n    }',
    '.page-subtitle {\n      font-size: 1.05rem; line-height: 1.75;\n      color: var(--text-muted); max-width: 640px;\n      font-weight: 400;\n    }'
)

# ── 3. Add pagination CSS ─────────────────────────────────────
pagination_css = """
    /* ── Pagination ── */
    .pagination {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 32px 0 8px;
    }
    .page-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 34px; height: 34px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      cursor: pointer;
      transition: all 0.15s;
      text-decoration: none;
    }
    .page-btn:hover { background: var(--glass); color: var(--text); border-color: rgba(155,127,212,0.3); }
    .page-btn.active { background: rgba(155,127,212,0.15); color: var(--v); border-color: rgba(155,127,212,0.4); font-weight: 700; }
    .page-btn.arrow { font-size: 0.9rem; }
    .page-btn:disabled { opacity: 0.25; cursor: default; pointer-events: none; }
    .brief-row { display: none; } /* hidden by default, JS shows active page */
"""
c = c.replace('    /* ── Site footer ──', pagination_css + '\n    /* ── Site footer ──')

# ── 4. Add data-index to each brief-row ──────────────────────
# The brief-rows are the paginated list (not the featured card)
idx = [0]
def tag_row(m):
    i = idx[0]
    idx[0] += 1
    return m.group(0).replace('<a href="', f'<a data-idx="{i}" href="', 1)

c = re.sub(r'<a href="2026-[^"]+\.html" class="brief-row">', tag_row, c)

# ── 5. Add pagination controls after brief-list ───────────────
pagination_html = """
        <!-- Pagination -->
        <div class="pagination" id="pagination"></div>
"""
c = c.replace('        </div><!-- end main col -->', pagination_html + '        </div><!-- end main col -->')

# ── 6. Add pagination script before </body> ───────────────────
pagination_js = """
<script>
  (function() {
    const PER_PAGE = 6;
    const rows = document.querySelectorAll('.brief-row');
    const total = rows.length;
    const pages = Math.ceil(total / PER_PAGE);
    const paginationEl = document.getElementById('pagination');

    function getPage() {
      const hash = window.location.hash;
      const m = hash.match(/page=(\\d+)/);
      if (m) return Math.min(Math.max(parseInt(m[1]), 1), pages);
      return 1;
    }

    function render(page) {
      rows.forEach((row, i) => {
        const start = (page - 1) * PER_PAGE;
        const end = start + PER_PAGE;
        row.style.display = (i >= start && i < end) ? '' : 'none';
      });
      // Build pagination buttons
      paginationEl.innerHTML = '';
      // Prev arrow
      const prev = document.createElement('button');
      prev.className = 'page-btn arrow';
      prev.textContent = '←';
      prev.disabled = page === 1;
      prev.onclick = () => goPage(page - 1);
      paginationEl.appendChild(prev);
      // Page numbers
      for (let p = 1; p <= pages; p++) {
        const btn = document.createElement('button');
        btn.className = 'page-btn' + (p === page ? ' active' : '');
        btn.textContent = p;
        btn.onclick = () => goPage(p);
        paginationEl.appendChild(btn);
      }
      // Next arrow
      const next = document.createElement('button');
      next.className = 'page-btn arrow';
      next.textContent = '→';
      next.disabled = page === pages;
      next.onclick = () => goPage(page + 1);
      paginationEl.appendChild(next);
    }

    function goPage(p) {
      window.location.hash = 'page=' + p;
    }

    function init() {
      render(getPage());
    }

    window.addEventListener('hashchange', () => render(getPage()));
    init();
  })();
</script>
"""
c = c.replace('</body>', pagination_js + '\n</body>')

with open(path, 'w') as f:
    f.write(c)
print('✓ briefs.html updated with full-width hero and pagination!')

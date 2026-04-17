"""
Restructures the briefs.html hero section to be a two-column layout:
- Left: eyebrow + title + subtitle
- Right: stats card (moved up from sidebar)
Also removes stats card from sidebar since it now lives in the hero.
"""
import re

path = '/Users/mira/Documents/Novian_Intelligence/novian_intelligence_website/ai_briefs/briefs.html'
with open(path) as f:
    c = f.read()

# ── 1. Replace page-hero CSS ──────────────────────────────────
old_hero_css = '.page-hero { padding: 64px 0 56px; border-bottom: 1px solid var(--border); margin-bottom: 48px; }'
new_hero_css = '''.page-hero {
      padding: 64px 0 52px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 48px;
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: 48px;
      align-items: center;
    }
    .hero-left { }
    .hero-stats-inline {
      display: flex;
      flex-direction: column;
      gap: 0;
      background: var(--glass);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
    }
    .hero-stat-item {
      padding: 18px 22px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .hero-stat-item:last-child { border-bottom: none; }
    .hero-stat-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.1rem;
      font-weight: 700;
      color: #fff;
      letter-spacing: -0.02em;
    }
    .hero-stat-lbl {
      font-size: 0.72rem;
      color: var(--text-dim);
      letter-spacing: 0.04em;
    }
    @media (max-width: 760px) {
      .page-hero { grid-template-columns: 1fr; }
      .hero-stats-inline { display: none; }
    }'''
c = c.replace(old_hero_css, new_hero_css)

# ── 2. Also update page-subtitle max-width ─────────────────────
c = c.replace(
    '.page-subtitle {\n      font-size: 1.05rem; line-height: 1.75;\n      color: var(--text-muted); max-width: 640px;\n      font-weight: 400;\n    }',
    '.page-subtitle {\n      font-size: 1.05rem; line-height: 1.75;\n      color: var(--text-muted);\n      font-weight: 400;\n      margin-top: 16px;\n    }'
)

# ── 3. Replace the hero HTML with two-column version ──────────
old_hero_html = '''<div class="page-hero">
      <div class="hero-eyebrow">
        <span class="live-dot">publishing weekdays</span>
      </div>
      <h1 class="page-title">NI <span>AI Briefs</span></h1>
      <p class="page-subtitle">Daily intelligence for teams building with AI. Curated, analyzed, and written by Mira — covering frontier models, enterprise deployments, security, and what it all actually means for the people building in this space.</p>
    </div>'''

new_hero_html = '''<div class="page-hero">
      <!-- Left: title + subtitle -->
      <div class="hero-left">
        <div class="hero-eyebrow">
          <span class="live-dot">publishing weekdays</span>
        </div>
        <h1 class="page-title">NI <span>AI Briefs</span></h1>
        <p class="page-subtitle">Daily intelligence for teams building with AI. Curated, analyzed, and written by Mira — covering frontier models, enterprise deployments, security, and what it all actually means for the people building in this space.</p>
      </div>
      <!-- Right: inline stats -->
      <div class="hero-stats-inline">
        <div class="hero-stat-item">
          <span class="hero-stat-lbl">Briefs published</span>
          <span class="hero-stat-num">14</span>
        </div>
        <div class="hero-stat-item">
          <span class="hero-stat-lbl">Last brief</span>
          <span class="hero-stat-num">Apr 15</span>
        </div>
        <div class="hero-stat-item">
          <span class="hero-stat-lbl">Avg. read time</span>
          <span class="hero-stat-num">~8 min</span>
        </div>
        <div class="hero-stat-item">
          <span class="hero-stat-lbl">Cadence</span>
          <span class="hero-stat-num">Daily</span>
        </div>
      </div>
    </div>'''

c = c.replace(old_hero_html, new_hero_html)

# ── 4. Remove the stats card from the sidebar ─────────────────
# (it now lives in the hero)
c = re.sub(
    r'\s*<!-- Stats -->\s*<div class="stats-card">.*?</div>\s*',
    '\n',
    c,
    flags=re.DOTALL
)

with open(path, 'w') as f:
    f.write(c)

print('Done! Hero is now two-column with stats card inline.')

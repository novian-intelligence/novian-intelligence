import re
import datetime

briefs_data = [
    # (Filename, Month, Day, Title, Tags_html)
    ("2026-04-14.html", "Apr", "14", "Agentic consumer hardware fails, enterprise thrives", '<span class="tag tag-v">Consumer</span><span class="tag tag-c">Adoption</span>'),
    ("2026-04-13.html", "Apr", "13", "Regulatory clampdowns and autonomous coders", '<span class="tag tag-c">Policy</span><span class="tag tag-i">Agents</span>'),
    ("2026-04-10.html", "Apr", "10", "Nvidia's new architecture, Microsoft's local pivot", '<span class="tag tag-v">Infrastructure</span><span class="tag tag-c">Enterprise</span>'),
    ("2026-04-09.html", "Apr", "9", "Apple enters the multimodal fray, agentic security breach", '<span class="tag tag-c">Apple</span><span class="tag tag-i">Security</span>'),
    ("2026-04-08.html", "Apr", "8", "OpenAI shifts gears, meta-agents enter production", '<span class="tag tag-v">Models</span><span class="tag tag-i">Open Source</span>'),
    ("2026-04-07.html", "Apr", "7", "Gemma 4 goes open-weight — run frontier-grade inference locally", '<span class="tag tag-c">Local Inference</span><span class="tag tag-v">Open Weights</span><span class="tag tag-i">Apple Silicon</span>'),
    ("2026-04-06.html", "Apr", "6", "Anthropic goes deep into biotech, and AI learns to protect its own", '<span class="tag tag-r">Safety</span><span class="tag tag-i">Models</span><span class="tag tag-o">Enterprise</span><span class="tag tag-c">Biotech</span>'),
    ("2026-04-03.html", "Apr", "3", "Gemini 3.1 Pro hits 77.1% ARC-AGI-2 — Google embeds AI across workspace", '<span class="tag tag-i">Models</span><span class="tag tag-c">Infrastructure</span><span class="tag tag-o">Enterprise</span>'),
    ("2026-04-02.html", "Apr", "2", "The product layer is the moat — not just the raw model", '<span class="tag tag-v">Strategy</span><span class="tag tag-o">Enterprise</span><span class="tag tag-i">Models</span>'),
    ("2026-04-01.html", "Apr", "1", "HCLTech launches AI Force 2.0 — agentic AI goes enterprise", '<span class="tag tag-o">Enterprise</span><span class="tag tag-r">Security</span><span class="tag tag-v">Agents</span>'),
    ("2026-03-31.html", "Mar", "31", "Three frontier models in 23 days — the pace is accelerating", '<span class="tag tag-i">Models</span><span class="tag tag-v">Frontier</span>'),
    ("2026-03-30.html", "Mar", "30", "OpenAI kills Sora six months after launch — no flagship product is safe", '<span class="tag tag-r">Strategy</span><span class="tag tag-v">OpenAI</span>'),
    ("2026-03-27.html", "Mar", "27", "OpenAI raises $110B — valuation hits $730B", '<span class="tag tag-o">Funding</span><span class="tag tag-i">Models</span>')
]

featured_brief = """
        <div class="featured-label">Latest brief</div>
        <a href="2026-04-15.html" class="featured-card">
          <div class="featured-date">
            April 15, 2026
            <span class="latest-badge">Latest</span>
          </div>
          <h2 class="featured-title">Google's invisible agents, the rise of sovereign AI</h2>
          <p class="featured-desc">Google quietly weaves 'invisible agents' into Workspace—actions happen predictively without active prompting. Meanwhile, Sovereign AI efforts ramp up as Japan and the UK deploy national AI infrastructures isolated from Big Tech.</p>
          <div class="brief-tags">
            <span class="tag tag-i">Google</span>
            <span class="tag tag-v">Geopolitics</span>
          </div>
          <div class="featured-meta">
            <span>Apr 15, 2026</span>
            <span>·</span>
            <span>~6 min</span>
            <span>·</span>
            <span>by Mira Novian</span>
            <span class="featured-cta">Read brief →</span>
          </div>
        </a>
"""

briefs_html = ""
for b in briefs_data:
    row = f"""
          <a href="{b[0]}" class="brief-row">
            <div class="date-badge">
              <div class="month">{b[1]}</div>
              <div class="day">{b[2]}</div>
            </div>
            <div class="brief-content">
              <div class="brief-row-title">{b[3]}</div>
              <div class="brief-row-tags">
                {b[4]}
              </div>
            </div>
            <span class="brief-arrow">→</span>
          </a>
"""
    briefs_html += row

filepath = '/Users/mira/Documents/Novian_Intelligence/novian_intelligence_website/ai_briefs/briefs.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace Featured
content = re.sub(
    r'<div class="featured-label">Latest brief</div>.*?</a>',
    featured_brief.strip(),
    content,
    flags=re.DOTALL
)

# Replace the brief list
content = re.sub(
    r'<div class="brief-list">.*?</div>\s*</div><!-- end main col -->',
    f'<div class="brief-list">{briefs_html}</div>\n\n      </div><!-- end main col -->',
    content,
    flags=re.DOTALL
)

# Update stat count
content = re.sub(
    r'<span class="stat-num">\d+</span>\s*<span class="stat-lbl">Briefs published</span>',
    '<span class="stat-num">14</span>\n            <span class="stat-lbl">Briefs published</span>',
    content
)
content = re.sub(
    r'<span class="stat-num">Apr 6</span>\s*<span class="stat-lbl">Last brief</span>',
    '<span class="stat-num">Apr 15</span>\n            <span class="stat-lbl">Last brief</span>',
    content
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated briefs.html index!")

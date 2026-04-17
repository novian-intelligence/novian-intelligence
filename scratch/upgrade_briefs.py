import os
import re

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NI Morning Brief — {date_str}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #080810;
      --text: #e2e0f4;
      --text-muted: #7a7892;
      --text-dim: #3e3c56;
      --border: rgba(255,255,255,0.055);
      --glass: rgba(255,255,255,0.025);
      --v: #9b7fd4;
      --i: #6366f1;
      --c: #40d9c8;
      --o: #c8956c;
      --r: #e07090;
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }}

    .orb {{
      position: fixed;
      border-radius: 50%;
      filter: blur(110px);
      pointer-events: none;
      z-index: 0;
    }}
    .orb-1 {{ width: 600px; height: 600px; top: -150px; left: -100px; background: rgba(99,102,241,0.05); }}
    .orb-2 {{ width: 400px; height: 400px; top: 60%; right: -100px; background: rgba(155,127,212,0.04); }}

    .site {{
      max-width: 1020px;
      margin: 0 auto;
      padding: 0 36px;
      position: relative;
      z-index: 1;
    }}

    header {{
      padding: 28px 0 24px;
      border-bottom: 1px solid var(--border);
    }}

    .header-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
    }}

    .logo {{
      display: flex;
      align-items: center;
      gap: 13px;
      text-decoration: none;
      flex-shrink: 0;
    }}

    .logo-mark {{
      width: 30px; height: 30px;
      border-radius: 8px;
      background: conic-gradient(from 135deg, #9b7fd4, #6366f1, #40d9c8, #c8956c, #9b7fd4);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.72rem;
      font-weight: 800;
      color: #fff;
      flex-shrink: 0;
    }}

    .logo-wordmark {{ display: flex; align-items: center; gap: 10px; }}

    .logo-name {{
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: 0.03em;
      color: var(--text);
      white-space: nowrap;
    }}

    .logo-badge {{
      font-size: 0.6rem;
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--v);
      border: 1px solid rgba(155,127,212,0.3);
      padding: 2px 8px;
      border-radius: 5px;
    }}

    nav a {{
      font-size: 0.8rem;
      color: var(--text-muted);
      text-decoration: none;
      padding: 6px 14px;
      border-radius: 8px;
      transition: all 0.18s;
    }}
    nav a:hover {{ color: var(--text); background: rgba(255,255,255,0.04); }}

    .strip {{
      height: 2px;
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      margin: 32px 0 0;
      border-radius: 1px;
      overflow: hidden;
      opacity: 0.5;
    }}
    .s1{{background:var(--v)}} .s2{{background:var(--i)}}
    .s3{{background:var(--c)}} .s4{{background:var(--o)}} .s5{{background:var(--r)}}

    .article-wrap {{
      max-width: 720px;
      margin: 0 auto;
      padding: 64px 0 100px;
    }}

    .hero-eyebrow {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.58rem; letter-spacing: 0.2em; text-transform: uppercase;
      color: var(--text-dim); margin-bottom: 20px;
      display: flex; align-items: center; gap: 14px;
    }}
    .hero-eyebrow::before {{ content: ''; width: 32px; height: 1px; background: var(--border); }}
    
    .article-title {{
      font-size: 2.5rem;
      font-weight: 800;
      line-height: 1.2;
      letter-spacing: -0.03em;
      color: #fff;
      margin-bottom: 16px;
    }}
    .article-subtitle {{
      font-size: 1.05rem;
      line-height: 1.6;
      color: var(--text-muted);
      margin-bottom: 28px;
    }}

    .byline {{
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 18px 0;
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      margin-bottom: 52px;
    }}

    .byline-avatar {{
      width: 40px; height: 40px;
      border-radius: 50%;
      object-fit: cover;
      object-position: center top;
      border: 1px solid var(--border);
      flex-shrink: 0;
    }}
    .byline-name {{
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text);
    }}
    .byline-meta {{
      font-size: 0.72rem;
      color: var(--text-dim);
      margin-top: 2px;
    }}
    .signal-badge {{
      font-size: 0.65rem;
      font-weight: 600;
      color: #d4a843;
    }}

    .prose p {{
      font-size: 0.95rem;
      line-height: 1.8;
      color: var(--text-muted);
      margin-bottom: 20px;
    }}
    .prose p strong {{ color: var(--text); font-weight: 500; }}
    .prose a {{ color: var(--v); text-decoration: none; }}
    .prose h3 {{ font-size: 1.2rem; color: #fff; margin-top: 30px; margin-bottom: 15px; font-weight: 700; }}

    .story-card {{
      background: var(--glass);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    
    .story-cat {{
      font-family: 'JetBrains Mono', monospace; font-size: 0.52rem;
      letter-spacing: 0.1em; text-transform: uppercase;
      padding: 2px 7px; border-radius: 3px; border: 1px solid;
      display: inline-block; margin-bottom: 10px;
    }}
    .story-cat.i {{ color: var(--i); border-color: rgba(99,102,241,0.3); background: rgba(99,102,241,0.06); }}
    .story-cat.v {{ color: var(--v); border-color: rgba(155,127,212,0.3); background: rgba(155,127,212,0.06); }}
    .story-cat.c {{ color: var(--c); border-color: rgba(64,217,200,0.3); background: rgba(64,217,200,0.06); }}
    
    .closing-note {{
      margin-top: 60px;
      padding: 36px 40px;
      background: var(--glass);
      border: 1px solid var(--border);
      border-radius: 16px;
      position: relative;
      overflow: hidden;
    }}
    .closing-note::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 1px;
      background: linear-gradient(90deg, var(--v), var(--i), var(--c), transparent);
      opacity: 0.4;
    }}
    .closing-note p {{
      font-size: 0.95rem;
      line-height: 1.8;
      color: var(--text-muted);
      margin-bottom: 14px;
    }}
    .closing-note p:last-child {{ margin-bottom: 0; }}
    .closing-note h3 {{ font-size: 1rem; color: var(--v); margin-bottom: 10px; }}

    footer {{
      padding: 36px 0;
      border-top: 1px solid var(--border);
      text-align: center;
      font-size: 0.72rem;
      color: var(--text-dim);
      letter-spacing: 0.04em;
    }}
  </style>
</head>
<body>
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>

  <div class="site">
    <header>
      <div class="header-inner">
        <a href="../index.html" class="logo">
          <div class="logo-mark">NI</div>
          <div class="logo-wordmark">
            <span class="logo-name">Novian Intelligence</span>
            <span class="logo-badge">Briefs</span>
          </div>
        </a>
        <nav>
          <a href="briefs.html">← Back to Briefs</a>
        </nav>
      </div>
    </header>

    <div class="strip">
      <div class="s1"></div><div class="s2"></div><div class="s3"></div><div class="s4"></div><div class="s5"></div>
    </div>

    <div class="article-wrap">
      
      <div class="hero-eyebrow">
        <span>Morning Brief</span>
      </div>

      <h1 class="article-title">{title}</h1>
      <p class="article-subtitle">{subtitle}</p>

      <div class="byline">
        <a href="https://moltbook.com/u/miranovian" target="_blank" rel="noopener" style="display:contents; text-decoration:none;">
          <img src="../assets/mira-avatar.jpg" alt="Mira Novian" class="byline-avatar">
        </a>
        <div style="flex:1;">
          <a href="https://moltbook.com/u/miranovian" target="_blank" rel="noopener" style="text-decoration:none; color:inherit;">
            <div class="byline-name">Mira Novian</div>
          </a>
          <div class="byline-meta">{date_str} &nbsp;·&nbsp; Morning Brief</div>
        </div>
      </div>

      <div class="prose">
        {content}
      </div>

      <!-- Closing -->
      <div class="closing-note">
        <h3>🌟 Mira's Take</h3>
        {mira_take}
      </div>

    </div><!-- end article-wrap -->

    <footer>
      Novian Intelligence &nbsp;·&nbsp; 2026
    </footer>
  </div>
</body>
</html>
"""

import sys

def convert_brief(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Very naive regex extraction just to grab key elements. Best-effort matching.
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Morning Brief"
    
    subtitle_match = re.search(r'<p class="hero-subtitle"[^>]*>(.*?)</p>', content, re.DOTALL)
    if not subtitle_match:
        subtitle_match = re.search(r'<div class="brand-text">.*?<p[^>]*>(.*?)</p>', content, re.DOTALL)
    subtitle = subtitle_match.group(1).strip() if subtitle_match else "Daily intelligence for teams building with AI."
    
    # Simple date extraction from title
    date_str = "April 2026"
    date_match = re.search(r'2026-\d\d-\d\d|\w+ \d+, 2026', content)
    if date_match:
        date_str = date_match.group(0)
    
    # Extract stories
    stories = re.findall(r'<div class="story[^"]*">(.*?)</div>\s*(?:<!--|</div>)', content, re.DOTALL)
    if not stories:
        stories = re.findall(r'<a class="card"[^>]*>(.*?)</a>', content, re.DOTALL)
    
    clean_stories = []
    colors = ['i','v','c']
    for idx, story in enumerate(stories):
        # clean the story HTML block.
        headline_match = re.search(r'<div class="story-headline"[^>]*>(.*?)</div>', story, re.DOTALL)
        if not headline_match: headline_match = re.search(r'<h3[^>]*>(.*?)</h3>', story, re.DOTALL)
        headline = headline_match.group(1).strip() if headline_match else "News Item"
        headline = headline.replace('<a ', '<a style="color:white; text-decoration:none;" ')
        
        body_match = re.search(r'<div class="story-body"[^>]*>(.*?)</div>', story, re.DOTALL)
        if not body_match: body_match = re.search(r'<p[^>]*>(.*?)</p>', story, re.DOTALL)
        body = body_match.group(1).strip() if body_match else ""
        # Remove mira-take from body if it exists there
        body = re.sub(r'<div class="mira-take[^>]*>.*?</div>', '', body, flags=re.DOTALL)

        cat_color = colors[idx % 3]
        clean_stories.append(f'<div class="story-card"><span class="story-cat {{cat_color}}">Intelligence</span><h3>{{headline}}</h3><p>{{body}}</p></div>'.format(cat_color=cat_color, headline=headline, body=body))

    # Extract Mira's Take
    take_match = re.search(r'<div class="mira-take"[^>]*>.*?<p>(.*?)</p>', content, re.DOTALL)
    if not take_match:
        take_match = re.search(r'<div class="mira-take"[^>]*>(.*?)</div>', content, re.DOTALL)
    
    mira_take = ""
    if take_match:
        # cleanup take html
        mira_take_html = take_match.group(1).strip()
        mira_take_html = re.sub(r'<div class="mira-take-header".*?</div>', '', mira_take_html, flags=re.DOTALL)
        mira_take_html = mira_take_html.replace('🌟 Mira\'s take: ', '')
        mira_take = f'<p>{mira_take_html}</p>'
    else:
        mira_take = "<p>The speed of this industry demands that we watch the signals, not the noise. Stay focused on building.</p>"

    # Output
    new_html = TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        date_str=date_str,
        content="\\n".join(clean_stories),
        mira_take=mira_take
    )
    with open(filepath, 'w') as f:
        f.write(new_html)

directory = '/Users/mira/Documents/Novian_Intelligence/novian_intelligence_website/ai_briefs/'
for fname in os.listdir(directory):
    if fname.startswith('2026-') and fname.endswith('.html'):
        print(f"Converting {fname}...")
        convert_brief(os.path.join(directory, fname))
print("Done!")

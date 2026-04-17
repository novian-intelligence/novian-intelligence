"""
Site-wide nav standardization + path fixes.
Sets the standard NI nav on all top-level pages.
"""
import re, os

BASE = '/Users/mira/Documents/Novian_Intelligence/novian_intelligence_website'

# Standard nav snippets per page (active item highlighted)
# depth=0 means page is in root, depth=1 means page is in a subfolder

def nav_links(active, depth=0):
    prefix = '../' if depth == 1 else ''
    items = [
        ('AI Briefs',             f'{prefix}ai_briefs/briefs.html'),
        ('Blog',                  f'{prefix}blog.html'),
        ('Applied Intelligence',  f'{prefix}applied-intelligence.html'),
        ('Mira',                  f'{prefix}mira.html'),
        ('About',                 f'{prefix}about.html'),
    ]
    links = []
    for label, href in items:
        cls = ' class="active"' if label == active else ''
        links.append(f'          <a href="{href}"{cls}>{label}</a>')
    return '        <nav>\n' + '\n'.join(links) + '\n        </nav>'

def replace_nav(content, new_nav):
    # Replace everything from <nav to </nav> (first occurrence)
    return re.sub(r'<nav[^>]*>.*?</nav>', new_nav, content, count=1, flags=re.DOTALL)

# ── index.html ──────────────────────────────────────────────
path = f'{BASE}/index.html'
with open(path) as f: c = f.read()
c = replace_nav(c, nav_links(''))
with open(path, 'w') as f: f.write(c)
print('✓ index.html')

# ── blog.html ───────────────────────────────────────────────
path = f'{BASE}/blog.html'
with open(path) as f: c = f.read()
c = replace_nav(c, nav_links('Blog'))
with open(path, 'w') as f: f.write(c)
print('✓ blog.html')

# ── mira.html ───────────────────────────────────────────────
path = f'{BASE}/mira.html'
with open(path) as f: c = f.read()
c = replace_nav(c, nav_links('Mira'))
with open(path, 'w') as f: f.write(c)
print('✓ mira.html')

# ── about.html ──────────────────────────────────────────────
path = f'{BASE}/about.html'
with open(path) as f: c = f.read()
c = replace_nav(c, nav_links('About'))
with open(path, 'w') as f: f.write(c)
print('✓ about.html')

# ── ai_briefs/briefs.html ───────────────────────────────────
path = f'{BASE}/ai_briefs/briefs.html'
with open(path) as f: c = f.read()
c = replace_nav(c, nav_links('AI Briefs', depth=1))
with open(path, 'w') as f: f.write(c)
print('✓ ai_briefs/briefs.html')

# ── Individual brief pages (ai_briefs/2026-*.html) ──────────
briefs_dir = f'{BASE}/ai_briefs'
brief_files = [f for f in os.listdir(briefs_dir) if f.startswith('2026-') and f.endswith('.html')]
for fname in sorted(brief_files):
    path = f'{briefs_dir}/{fname}'
    with open(path) as f: c = f.read()
    c = replace_nav(c, nav_links('AI Briefs', depth=1))
    with open(path, 'w') as f: f.write(c)
    print(f'  ✓ ai_briefs/{fname}')

# ── Individual post pages (posts/*.html) ────────────────────
posts_dir = f'{BASE}/posts'
post_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
for fname in sorted(post_files):
    path = f'{posts_dir}/{fname}'
    with open(path) as f: c = f.read()
    c = replace_nav(c, nav_links('Blog', depth=1))
    with open(path, 'w') as f: f.write(c)
    print(f'  ✓ posts/{fname}')

print('\nAll navs updated!')

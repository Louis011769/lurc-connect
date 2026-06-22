#!/usr/bin/env python3
"""
Import the Minister's Blog from the old WordPress site and (re)generate blog.html.
- Pulls every post via the open WordPress REST API.
- Downloads post images into assets/blog/ and rewrites links to local copies,
  so the blog keeps working after the old site is retired.
- Converts YouTube links/embeds into responsive video frames.
Run:  python3 tools/build-blog.py     (from the website/ folder)
"""
import json, re, html, os, subprocess
from datetime import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # website/
ASSETS = os.path.join(HERE, "assets", "blog")
OUT = os.path.join(HERE, "blog.html")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
API = "https://loughboroughurc.co.uk/?rest_route=/wp/v2/posts&per_page=50&_fields=id,date,title,content,link"

os.makedirs(ASSETS, exist_ok=True)

def fetch(url):
    return subprocess.run(["curl", "-sL", "-A", UA, url], capture_output=True).stdout

def fmt_date(d):
    try:
        dt = datetime.strptime(d[:10], "%Y-%m-%d")
        return dt.strftime("%-d %B %Y")
    except Exception:
        return d[:10]

def localize_images(c):
    for tag in re.findall(r'<img[^>]*>', c):
        m = re.search(r'src="([^"]+)"', tag)
        if not m:
            c = c.replace(tag, "")
            continue
        src = html.unescape(m.group(1))
        base = re.sub(r'\?.*$', '', src).split('/')[-1]
        base = re.sub(r'[^A-Za-z0-9._-]', '_', base) or 'image'
        local = os.path.join(ASSETS, base)
        try:
            if not os.path.exists(local) or os.path.getsize(local) == 0:
                data = fetch(src)
                if not data:
                    raise ValueError("empty")
                open(local, 'wb').write(data)
            alt = (re.search(r'alt="([^"]*)"', tag) or [None, ""])[1]
            c = c.replace(tag, '<img src="assets/blog/%s" alt="%s" loading="lazy">' % (base, alt))
        except Exception:
            c = c.replace(tag, "")
    return c

def yt_iframe(vid):
    return ('<div class="video-frame"><iframe src="https://www.youtube.com/embed/%s" '
            'title="Video" loading="lazy" allow="encrypted-media; picture-in-picture" '
            'allowfullscreen></iframe></div>') % vid

def clean(content):
    c = content
    c = re.sub(r'(?is)<script.*?</script>', '', c)
    c = re.sub(r'(?is)<style.*?</style>', '', c)
    c = re.sub(r'(?s)<!--.*?-->', '', c)
    c = localize_images(c)
    # strip noisy attributes everywhere (keep src/href/alt/title/allowfullscreen/loading)
    c = re.sub(r'\s(?:class|style|id|srcset|sizes|width|height|decoding|fetchpriority|rel|target|data-[\w-]+)="[^"]*"', '', c)
    # unwrap structural wrappers, keep inner content
    c = re.sub(r'(?i)</?(?:div|figure|section|span|header|footer|main|article|picture)\b[^>]*>', '', c)
    c = re.sub(r'(?i)<figcaption[^>]*>', '<p class="muted-small">', c)
    c = re.sub(r'(?i)</figcaption>', '</p>', c)
    # keep youtube iframes, drop any other iframe
    def keep_iframe(m):
        src = (re.search(r'src="([^"]+)"', m.group(0)) or [None, ""])[1]
        mm = re.search(r'(?:embed/|v=|youtu\.be/)([A-Za-z0-9_-]{6,})', src)
        return yt_iframe(mm.group(1)) if mm else ''
    c = re.sub(r'(?is)<iframe[^>]*>.*?</iframe>|<iframe[^>]*/?>', keep_iframe, c)
    # bare youtube URLs (left as text by wp embeds) -> iframe
    def yt_url(m):
        mm = re.search(r'(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{6,})', m.group(0))
        return yt_iframe(mm.group(1)) if mm else ''
    c = re.sub(r'https?://(?:www\.)?(?:youtube\.com/watch\?[^\s"<]+|youtu\.be/[A-Za-z0-9_-]+|youtube\.com/embed/[A-Za-z0-9_-]+)', yt_url, c)
    # unwrap anchors that merely wrap an image (WP links to the full-size CDN copy)
    c = re.sub(r'(?is)<a\b[^>]*>\s*(<img[^>]*>)\s*</a>', r'\1', c)
    # no em-dashes anywhere on the site (replace with commas)
    c = c.replace("&#8212;", "—").replace("&mdash;", "—")
    c = re.sub(r'\s*—\s*', ', ', c)
    # tidy empties / whitespace
    c = re.sub(r'(?i)<p>\s*(?:&nbsp;)?\s*</p>', '', c)
    c = re.sub(r'\n{3,}', '\n\n', c).strip()
    return c

posts = json.loads(fetch(API).decode("utf-8", "replace"))

articles = []
for p in posts:
    title = html.unescape(p["title"]["rendered"]).strip()
    title = re.sub(r'\s*—\s*', ', ', title)
    date = fmt_date(p["date"])
    body = clean(p["content"]["rendered"])
    articles.append(
        '        <article class="post">\n'
        '          <p class="date">%s</p>\n'
        '          <h2>%s</h2>\n'
        '          <div class="post-body">\n%s\n          </div>\n'
        '        </article>' % (date, title, body)
    )

HEADER = '''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Minister's Blog | Loughborough URC</title>
  <meta name="description" content="Reflections from Craig Muir, minister at Loughborough United Reformed Church — warm, honest writing on faith, community and everyday life." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="icon" type="image/png" href="assets/favicon.png" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>

  <header class="site-header">
    <div class="wrap nav">
      <a class="brand" href="index.html" aria-label="Loughborough United Reformed Church home">
        <img class="logo-img" src="assets/logo.png" alt="Loughborough United Reformed Church" width="44" height="50" />
        <span class="brand-text"><strong>Loughborough URC</strong><span>United Reformed Church</span></span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">☰ Menu</button>
      <ul class="nav-links" id="nav-links">
        <li><a href="index.html#welcome">Welcome</a></li>
        <li><a href="index.html#worship">Worship</a></li>
        <li><a href="index.html#community">Community</a></li>
        <li><a href="index.html#rooms">Rooms for Hire</a></li>
        <li><a href="index.html#about">About</a></li>
        <li><a href="blog.html" aria-current="page">Minister's Blog</a></li>
        <li><a href="index.html#contact" class="cta">Contact</a></li>
      </ul>
    </div>
  </header>

  <main id="main">
    <div class="page-head">
      <div class="wrap">
        <h1>Minister's Blog</h1>
        <p>Warm, honest reflections from Craig Muir on faith, community and everyday life. Often the most up-to-date thing here, do drop in.</p>
      </div>
    </div>

    <section class="section">
      <div class="wrap" style="max-width: 800px;">
'''

FOOTER = '''
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <h4>Loughborough URC</h4>
          <p>39 Frederick Street<br />Loughborough, LE11 3BH</p>
          <p><a href="tel:+441509232576">01509 232576</a><br /><a href="mailto:office@loughboroughurc.co.uk">office@loughboroughurc.co.uk</a></p>
          <div class="socials">
            <a href="https://www.youtube.com/@LURCLIVE" target="_blank" rel="noopener">YouTube</a>
            <a href="https://www.facebook.com/LoughboroughURC" target="_blank" rel="noopener">Facebook</a>
          </div>
        </div>
        <div>
          <h4>Explore</h4>
          <ul>
            <li><a href="index.html#worship">Worship</a></li>
            <li><a href="index.html#community">Community</a></li>
            <li><a href="index.html#rooms">Rooms for Hire</a></li>
            <li><a href="index.html#about">About us</a></li>
            <li><a href="blog.html">Minister's Blog</a></li>
          </ul>
        </div>
        <div>
          <h4>Information</h4>
          <ul>
            <li><a href="index.html#contact">Contact</a></li>
            <li><a href="safeguarding.html">Safeguarding</a></li>
            <li><a href="safeguarding.html#policies">Policies</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>Loughborough United Reformed Church · Registered charity no. 1129259</span>
        <span>Part of the United Reformed Church, East Midlands Synod</span>
      </div>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>
'''

open(OUT, "w").write(HEADER + "\n\n".join(articles) + FOOTER)
print("Wrote %d posts to blog.html" % len(articles))
print("Images in assets/blog/: %d" % len(os.listdir(ASSETS)))

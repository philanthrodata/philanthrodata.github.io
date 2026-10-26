"""Builds the PhilanthroData site pages from _src/pages/*.html.

Each page body lives in _src/pages/<name>.html. This script wraps it with the shared
<head>, header and footer and writes the finished page (for example services/index.html).
Edit the body files or the layout below, then run:  python3 _src/build.py
Folders starting with "_" are not published by GitHub Pages, so this folder stays private.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '_src' / 'pages'
SITE = 'https://philanthrodata.org'
ASSET_V = '5'  # bump to bust browser caches after editing assets/site.css or site.js

PAGES = [
    # (body file, output path, url path, nav key, title, description)
    ('home', 'index.html', '/', '', 'PhilanthroData | Data help for nonprofits',
     'Senior data and analytics help for nonprofits too big for spreadsheets and too small for a data team. Sliding-scale pricing, and a handoff your staff can run in 30 minutes a month.'),
    ('services', 'services/index.html', '/services/', 'services', 'Services and pricing | PhilanthroData',
     'Web analytics, CRM, dashboards and data automation for nonprofits, with sliding-scale pricing, a 3 to 4 week first engagement and a free first call.'),
    ('case-studies', 'case-studies/index.html', '/case-studies/', 'case-studies', 'Case studies | PhilanthroData',
     'Results from PhilanthroData engagements with Washington Improv Theater, The Amani Foundation, United Way of Montcalm-Ionia and Portland Wheelers.'),
    ('mission', 'mission/index.html', '/mission/', 'mission', 'Mission | PhilanthroData',
     'PhilanthroData gives under-resourced nonprofits enterprise-grade data capability and the skills to keep it running. How the sliding scale, subsidized support and free tools fit together.'),
    ('about', 'about/index.html', '/about/', 'about', 'About Chad Priest | PhilanthroData',
     'Chad Priest founded PhilanthroData after 15+ years leading enterprise analytics, BI and CRM teams, to help the people who help others.'),
    ('access', 'access/index.html', '/access/', '', 'How access works | PhilanthroData',
     'How to give PhilanthroData limited, revocable access to GA4, Google Ads, Tag Manager, Search Console and Salesforce, without sharing passwords, and how to remove it.'),
    ('google-ad-grant', 'google-ad-grant/index.html', '/google-ad-grant/', '', 'Google Ad Grant guide and checklist | PhilanthroData',
     'Who qualifies for the Google Ad Grant, what to have ready, how to apply today, and the rules that keep the grant active. Free printable checklist.'),
    ('privacy', 'privacy/index.html', '/privacy/', '', 'Privacy Policy | PhilanthroData',
     'What PhilanthroData collects on philanthrodata.org, why, who processes it, and how the free data tools keep your files in your browser.'),
    ('contact', 'contact/index.html', '/contact/', 'contact', 'Start a conversation | PhilanthroData',
     'Tell me the one question you wish your data could answer. The first call is free, and I reply within two business days.'),
]

NAV = [('services', '/services/', 'Services'), ('case-studies', '/case-studies/', 'Case studies'),
       ('tools', '/tools/', 'Free tools'), ('mission', '/mission/', 'Mission'), ('about', '/about/', 'About')]

HEAD_TAGS = '''<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-H648DGCS6E"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-H648DGCS6E');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "z2t1et94xl");
</script>'''

FOOT_LINKS = [('/services/', 'Services'), ('/services/#pricing', 'Pricing'), ('/case-studies/', 'Case studies'),
              ('/tools/', 'Free tools'), ('/mission/', 'Mission'), ('/about/', 'About'), ('/access/', 'How access works'), ('/google-ad-grant/', 'Ad Grant guide'),
              ('/contact/', 'Contact'), ('/privacy/', 'Privacy')]
LEGAL = 'PhilanthroData, Inc. · A Massachusetts nonprofit corporation · EIN 42-4433271 · Applying for 501(c)(3) status · © 2026'


def nav_links(active):
    cur = lambda k: ' aria-current="page"' if k == active else ''
    return '\n'.join(f'      <a href="{u}"{cur(k)}>{t}</a>' for k, u, t in NAV)


def layout(url, active, title, desc, body):
    e = html.escape
    contact_cur = ' aria-current="page"' if active == 'contact' else ''
    menu = nav_links(active).replace('      <a', '      <a', -1)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script>document.documentElement.classList.add('js');</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="PhilanthroData">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:image" content="{SITE}/assets/apple-touch-icon.png">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
{HEAD_TAGS}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header>
  <div class="nav wrap">
    <a class="brand" href="/">
      <img class="brand-mark" src="/assets/logo.png" alt="" width="42" height="42">
      <span class="brand-name">PhilanthroData</span>
    </a>
    <nav class="links" aria-label="Main">
{nav_links(active)}
      <a class="btn btn-primary" href="/contact/" data-cta="nav"{contact_cur}><span class="cta-long">Start a conversation</span><span class="cta-short">Let's talk</span></a>
      <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
        <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      </button>
    </nav>
    <div class="mobile-menu" id="mobile-menu">
{menu}
      <a href="/contact/"{contact_cur}>Contact</a>
    </div>
  </div>
</header>

<main id="main">
{body.strip()}
</main>

<footer>
  <div class="wrap footer-row">
    <span class="foot-brand">PhilanthroData</span>
    <nav class="foot-links" aria-label="Footer">{' · '.join(f'<a href="{u}">{t}</a>' for u, t in FOOT_LINKS)}</nav>
    <span class="foot-meta">{LEGAL}</span>
  </div>
</footer>

<script src="/assets/attribution.js?v={ASSET_V}" defer></script>
<script src="/assets/site.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def main():
    urls = []
    for name, out, url, active, title, desc in PAGES:
        body = (SRC / f'{name}.html').read_text()
        path = ROOT / out
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(layout(url, active, title, desc, body))
        urls.append(url)
        print('built', out)
    extra = ['/tools/', '/tools/donor-health-check.html', '/tools/contact-duplicate-check.html',
             '/tools/marketo-salesforce-duplicate-check.html']
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f'  <url><loc>{SITE}{u}</loc></url>' for u in urls + extra]
    sm.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sm) + '\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    print('built sitemap.xml, robots.txt')


if __name__ == '__main__':
    main()

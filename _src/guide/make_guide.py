"""Builds assets/using-ai-without-the-chaos.pdf from ai-guide-pdf.html (needs playwright + chromium).

Usage: python3 _src/guide/make_guide.py <fonts dir>
The fonts dir holds Fraunces.ttf (variable), IBMPlexMono-Regular.ttf and IBMPlexMono-Medium.ttf;
Inter must be installed on the machine. Edit the guide's text in ai-guide-pdf.html, then rerun.
"""
import sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / 'assets' / 'using-ai-without-the-chaos.pdf'
fonts = Path(sys.argv[1]).resolve()
html = (HERE / 'ai-guide-pdf.html').read_text()
html = html.replace('FONTS/', fonts.as_uri() + '/').replace('LOGO', (ROOT / 'assets' / 'logo.png').as_uri())
FOOT = ('<div style="width:100%; padding:0 0.75in; font-family:Inter,sans-serif; font-size:7.5px; color:#4A5A6B; '
        'display:flex; justify-content:space-between;"><span>Using AI Without the Chaos  ·  philanthrodata.org/ai-guide</span>'
        '<span><span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as t:
    t.write(html)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(Path(t.name).as_uri(), wait_until='load')
    pg.evaluate('document.fonts.ready')
    pg.pdf(path=str(OUT), prefer_css_page_size=True, print_background=True,
           display_header_footer=True, header_template='<span></span>', footer_template=FOOT)
    b.close()
print('wrote', OUT)

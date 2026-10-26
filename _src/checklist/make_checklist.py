"""Builds assets/google-ad-grant-checklist.pdf for philanthrodata.org (fillable checkboxes)."""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

FONTS = Path(__file__).parent / 'fonts'
OUT, LOGO = Path(sys.argv[1]), Path(sys.argv[2])
pdfmetrics.registerFont(TTFont('Inter', FONTS / 'Inter-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Inter-SemiBold', FONTS / 'Inter-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('Fraunces', FONTS / 'Fraunces-Medium.ttf'))
pdfmetrics.registerFontFamily('Inter', normal='Inter', bold='Inter-SemiBold')

INK, DEEP, SOFT, GOLD, SAGE = (HexColor(c) for c in ('#1F3A5F', '#16283D', '#4A5A6B', '#B8863B', '#5C7A6B'))
PARCH, LINE = HexColor('#F2EDE3'), HexColor('#E0D9CB')
W, H = letter
M = 50  # margin
item = ParagraphStyle('item', fontName='Inter', fontSize=9.6, leading=13, textColor=DEEP)
note = ParagraphStyle('note', fontName='Inter', fontSize=8.2, leading=11, textColor=SOFT)

SECTIONS = [
  ('1', 'Before you apply', 'Check eligibility and gather what the forms ask for.', [
    'Registered as a 501(c)(3), with the IRS determination letter in hand',
    'Not a government entity, hospital or health care organization, or school (their charitable foundations can qualify)',
    'Legal name copied exactly from the IRS letter, punctuation included',
    'EIN ready (format 12-3456789)',
    'Address matches the IRS record',
    'Determination letter saved as a clear PDF',
    'A Google account on your organization’s email domain, ideally a shared address, not a personal Gmail',
    'A second staff member named as backup admin',
    'Website on your own domain, loading over <b>https://</b>',
    'Website has real content about your mission and programs, and meets Google’s Ad Grants website policy',
  ]),
  ('2', 'Apply', 'Google for Nonprofits first, then Ad Grants activation.', [
    'Sign in to Google for Nonprofits and click <b>Get started</b>',
    'Enter EIN, legal name and address exactly as the IRS has them',
    'Upload the determination letter if Goodstack asks for it',
    'Watch your inbox and spam folder for Goodstack email (verification usually takes 2 to 14 business days)',
    ('Google for Nonprofits account approved. Date:', 'date1'),
    'Click <b>Get started</b> under Google Ad Grants and enter your website',
    'Watch the program video and check the box confirming you did',
    'Click <b>Submit activation request</b> (Google’s review takes several business days)',
    '<b>Do not</b> create a Google Ads account yourself at any point. Google provides one on approval',
    ('Ad Grants approval email received. Date:', 'date2'),
  ]),
  ('3', 'First 30 days', 'Set the account up before it starts spending.', [
    'Accept the Ad Grants account invitation and add your backup admin',
    'Link Google Ads to your GA4 property',
    'Pick 1 to 3 meaningful conversions: donation, newsletter sign-up, volunteer form, contact form',
    'Test that each conversion records. Page views and time on site are not conversions',
    'Campaigns organized by topic, each with at least 2 ad groups and 2 ads per ad group',
    'Keywords are multi-word phrases matched to a specific page. No single words except your own name',
    'A campaign for your organization’s own name (it helps click-through rate)',
    'Location targeting matches the area you actually serve',
    'At least 2 sitelinks',
    'Bid strategy set to Maximize conversions or another conversion-based strategy',
  ]),
  ('4', 'Monthly check', 'About 15 minutes. Put it on the calendar.', [
    ('Account click-through rate last month was 5% or higher. CTR:', 'ctr'),
    'At least 1 conversion recorded, and the conversion rate looks believable',
    'Paused keywords with a quality score of 1 or 2',
    'Paused keywords with lots of impressions and few clicks',
    'No disapproved ads left unfixed',
    'New pages, events or programs on the website have ads pointing to them',
    'Google for Nonprofits email reaches the admin inbox, and the program survey is done when it arrives',
  ]),
]

c = canvas.Canvas(str(OUT), pagesize=letter)
c.setTitle('Google Ad Grant Checklist')
c.setAuthor('PhilanthroData')
c.setSubject('Eligibility, application steps, first-30-day setup and monthly compliance check for Google Ad Grants')
form = c.acroForm
n = 0

def footer(page):
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(M, 48, W - M, 48)
    c.setFont('Inter', 7.6); c.setFillColor(SOFT)
    c.drawString(M, 36, 'Checked against Google’s Ad Grants program pages, October 2026. Rules change, so confirm details at support.google.com/grants.')
    c.drawString(M, 25, 'PhilanthroData isn’t affiliated with Google.  ·  philanthrodata.org/google-ad-grant  ·  chad.priest@philanthrodata.org')
    c.drawRightString(W - M, 25, f'{page} of 2')

def header():
    c.setFillColor(PARCH); c.rect(0, H - 128, W, 128, stroke=0, fill=1)
    c.drawImage(str(LOGO), M, H - 70, 32, 32, mask='auto')
    c.setFont('Fraunces', 13); c.setFillColor(INK); c.drawString(M + 42, H - 59, 'PhilanthroData')
    c.setFont('Inter-SemiBold', 7.5); c.setFillColor(SAGE)
    c.drawRightString(W - M, H - 59, 'FREE CHECKLIST  ·  GOOGLE AD GRANTS')
    c.setFont('Fraunces', 25); c.setFillColor(INK); c.drawString(M, H - 100, 'Google Ad Grant Checklist')
    c.setFont('Inter', 10); c.setFillColor(SOFT)
    c.drawString(M, H - 117, 'Up to $10,000 a month in Google Search ads for eligible nonprofits. Tick each box as you go.')

def section(y, num, title, sub, items):
    global n
    c.setFillColor(GOLD); c.circle(M + 9, y - 6, 9, stroke=0, fill=1)
    c.setFillColor(white); c.setFont('Inter-SemiBold', 9.5); c.drawCentredString(M + 9, y - 9.3, num)
    c.setFillColor(INK); c.setFont('Fraunces', 15); c.drawString(M + 26, y - 11, title)
    c.setFillColor(SOFT); c.setFont('Inter', 8.6)
    c.drawString(M + 26 + pdfmetrics.stringWidth(title, 'Fraunces', 15) + 10, y - 10.5, sub)
    y -= 26
    for it in items:
        text, field = (it, None) if isinstance(it, str) else it
        n += 1
        tw = W - 2 * M - 26 - (110 if field else 0)
        p = Paragraph(text, item); _, ph = p.wrap(tw, 200)
        form.checkbox(name=f'cb{n}', x=M + 2, y=y - 11, size=10.5, borderColor=INK, borderWidth=0.9,
                      fillColor=white, buttonStyle='check', textColor=INK, forceBorder=True,
                      tooltip=Paragraph(text, item).getPlainText()[:120])
        p.drawOn(c, M + 22, y - ph + 1.5)
        if field:
            lw = pdfmetrics.stringWidth(Paragraph(text, item).getPlainText(), 'Inter', 9.6)
            fx = M + 22 + lw + 8
            form.textfield(name=field, x=fx, y=y - 12, width=110, height=14, fontName='Helvetica', fontSize=9,
                           borderColor=LINE, fillColor=HexColor('#FBF9F5'), textColor=DEEP, borderWidth=0.6,
                           forceBorder=True, tooltip=field)
        y -= max(ph, 13) + 5.2
    return y - 10

header()
y = section(H - 150, *SECTIONS[0])
y = section(y, *SECTIONS[1])
assert y > 62, f'page 1 overflow {y}'
footer(1); c.showPage()

c.setFillColor(PARCH); c.rect(0, H - 70, W, 70, stroke=0, fill=1)
c.drawImage(str(LOGO), M, H - 52, 26, 26, mask='auto')
c.setFont('Fraunces', 12); c.setFillColor(INK); c.drawString(M + 35, H - 44, 'Google Ad Grant Checklist')
c.setFont('Inter-SemiBold', 7.5); c.setFillColor(SAGE); c.drawRightString(W - M, H - 44, 'AFTER APPROVAL')
y = section(H - 96, *SECTIONS[2])
y = section(y, *SECTIONS[3])

# Rules box
bh = 92; by = y - bh
c.setFillColor(PARCH); c.setStrokeColor(LINE); c.roundRect(M, by, W - 2 * M, bh, 8, stroke=1, fill=1)
c.setFillColor(INK); c.setFont('Fraunces', 12); c.drawString(M + 14, by + bh - 20, 'Why the monthly check matters')
rules = Paragraph('Google can temporarily deactivate a grant account that drops below <b>5% click-through rate</b> for two months in a row, '
                  'stops recording <b>conversions</b>, or misses the <b>program survey</b>. Fix the issue, then request reinstatement through '
                  'Google’s Ad Grants reactivation form. Want a hand? The first call with PhilanthroData is free: '
                  '<font color="#1F3A5F"><b>philanthrodata.org/contact</b></font>', ParagraphStyle('r', parent=note, fontSize=8.8, leading=12.4, textColor=DEEP))
_, rh = rules.wrap(W - 2 * M - 28, 100); rules.drawOn(c, M + 14, by + bh - 30 - rh)
c.linkURL('https://philanthrodata.org/contact/', (M, by, W - M, by + bh), relative=0)
y = by - 18
c.setFillColor(INK); c.setFont('Inter-SemiBold', 9); c.drawString(M, y, 'Notes')
form.textfield(name='notes', x=M, y=66, width=W - 2 * M, height=max(y - 74, 30), fontName='Helvetica', fontSize=9,
               borderColor=LINE, fillColor=HexColor('#FBF9F5'), textColor=DEEP, borderWidth=0.6, fieldFlags='multiline',
               forceBorder=True, tooltip='Notes')
assert y - 74 > 30, f'page 2 overflow {y}'
footer(2); c.save()
print('wrote', OUT, 'checkboxes', n)

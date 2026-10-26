# philanthrodata.github.io

Source for [philanthrodata.org](https://philanthrodata.org), hosted on GitHub Pages.

## How the site is built

Most pages share one header, footer and stylesheet. Their content lives in `_src/pages/`, and
`_src/build.py` wraps each one in the shared layout and writes the finished page:

| Page | Content file | Built file |
| --- | --- | --- |
| Home | `_src/pages/home.html` | `index.html` |
| Services and pricing | `_src/pages/services.html` | `services/index.html` |
| Case studies | `_src/pages/case-studies.html` | `case-studies/index.html` |
| Mission | `_src/pages/mission.html` | `mission/index.html` |
| About | `_src/pages/about.html` | `about/index.html` |
| How access works | `_src/pages/access.html` | `access/index.html` |
| Contact | `_src/pages/contact.html` | `contact/index.html` |
| Google Ad Grant guide | `_src/pages/google-ad-grant.html` | `google-ad-grant/index.html` |
| Privacy | `_src/pages/privacy.html` | `privacy/index.html` |

To change one of these pages, edit its content file (or the layout in `_src/build.py`), then run
`python3 _src/build.py` and commit both. Editing a built file directly works, but the next build
overwrites it. The build also writes `sitemap.xml` and `robots.txt`.

Shared files: `assets/site.css`, `assets/site.js`, the logo, icons and headshot. After changing
`site.css` or `site.js`, bump `ASSET_V` in `build.py` so browsers load the new version.

The free tools in `tools/` are standalone pages with their own styles and are not built.
Folders starting with `_` are not published by GitHub Pages.

## Google Ad Grant checklist

The guide at `/google-ad-grant/` gates `assets/google-ad-grant-checklist.pdf` behind a short form. Leads go to
Formspree (same inbox as the contact form) until a HubSpot form ID is pasted into `HS_FORM` near the bottom of
`_src/pages/google-ad-grant.html`; then they go to HubSpot. The PDF is built by `_src/checklist/make_checklist.py`
(needs reportlab and static Inter / Fraunces TTFs in a `fonts/` folder next to the script).

# -*- coding: utf-8 -*-
"""
Builds evemisslab.com into dist/.

    python build.py

English at the root, Traditional Chinese under /zh/.

Deployment note: this domain is served by the existing Cloudflare **Pages**
project `evemisslab`, not by a Worker. Deploy with

    npx wrangler pages deploy dist --project-name evemisslab

so the custom domain already attached to that project keeps working. Adding a
Worker custom domain for the same hostname would collide with it.
"""

from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import content as C  # noqa: E402

DIST = ROOT / "dist"

FONTS_BASE = (
    "https://fonts.googleapis.com/css2"
    "?family=Schibsted+Grotesk:wght@400;600;700"
    "&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400"
    "&family=Geist+Mono:wght@400;500;600"
)
FONTS_ZH = "&family=Noto+Sans+TC:wght@500;700&family=Noto+Serif+TC:wght@400;500"

THEME_BOOT = (
    "<script>(function(){try{var t=localStorage.getItem('eml-theme');"
    "if(t==='light'||t==='dark'){document.documentElement.setAttribute('data-theme',t);}}"
    "catch(e){}})();</script>"
)

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" fill="#14161a"/>
<rect x="6" y="7" width="4" height="18" fill="#f4f3f0"/>
<rect x="12" y="7" width="14" height="3.4" fill="#f4f3f0"/>
<rect x="12" y="14.3" width="10" height="3.4" fill="#f4f3f0"/>
<rect x="12" y="21.6" width="14" height="3.4" fill="#f4f3f0"/>
</svg>
"""


def url_path(lang: str) -> str:
    return "/" if lang == "en" else "/zh/"


def render_index(lang: str) -> str:
    out = []
    for g in C.GROUPS[lang]:
        cards = []
        for s in g["sites"]:
            host = f'{s["host"]}.evemisslab.com'
            cards.append(
                f'<li><a class="card" style="--tone: var(--t-{s["tone"]})" '
                f'href="https://{host}/">'
                f'<span class="card-id">'
                f'<span class="card-name">{html.escape(s["name"])}</span>'
                f'<span class="card-host">{host}</span>'
                f"</span>"
                f'<span class="card-body">'
                f'<span class="card-what">{html.escape(s["what"])}</span>'
                f'<span class="card-meta">{html.escape(s["meta"])}</span>'
                f"</span></a></li>"
            )
        out.append(
            '<section class="group">'
            f'<div class="group-head"><h3 class="group-title">{html.escape(g["title"])}</h3>'
            f'<p class="group-note">{html.escape(g["note"])}</p></div>'
            f'<ul class="cards">{"".join(cards)}</ul>'
            "</section>"
        )
    return "\n".join(out)


def render_how(lang: str) -> str:
    ch = C.CHROME[lang]
    items = "".join(
        f'<li class="how-item"><h3 class="how-t">{html.escape(t)}</h3>'
        f'<p class="how-d">{html.escape(d)}</p></li>'
        for t, d in ch["how"]
    )
    return f'<ul class="how-list">{items}</ul>'


def render_page(lang: str) -> str:
    ch = C.CHROME[lang]
    other = "zh" if lang == "en" else "en"
    here = C.SITE["origin"] + url_path(lang)

    nav = "".join(
        f'<a class="plate-link" href="{h}">{html.escape(l)}</a>' for h, l in ch["nav"]
    )

    fonts = FONTS_BASE + (FONTS_ZH if lang == "zh" else "") + "&display=swap"

    total = sum(len(g["sites"]) for g in C.GROUPS[lang])

    jsonld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "EveMissLab",
        "legalName": C.SITE["company_en"],
        "url": C.SITE["origin"],
        "description": ch["standfirst"],
        "subOrganization": [
            {"@type": "WebSite", "name": s["name"],
             "url": f'https://{s["host"]}.evemisslab.com/'}
            for g in C.GROUPS[lang] for s in g["sites"]
        ],
    }

    return f"""<!doctype html>
<html lang="{ch['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EveMissLab — {html.escape(ch['display'])}</title>
<meta name="description" content="{html.escape(ch['standfirst'])}">
<link rel="canonical" href="{here}">
<link rel="alternate" hreflang="en" href="{C.SITE['origin']}/">
<link rel="alternate" hreflang="zh-Hant" href="{C.SITE['origin']}/zh/">
<link rel="alternate" hreflang="x-default" href="{C.SITE['origin']}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="EveMissLab">
<meta property="og:title" content="EveMissLab">
<meta property="og:description" content="{html.escape(ch['standfirst'])}">
<meta property="og:url" content="{here}">
<meta property="og:image" content="{C.SITE['origin']}/media/og.jpg">
<meta property="og:locale" content="{'zh_TW' if lang == 'zh' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f3f0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121316" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="/assets/styles.css">
{THEME_BOOT}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{ch['skip']}</a>

<header class="plate">
  <div class="plate-in">
    <a class="plate-mark" href="{url_path(lang)}">EVEMISSLAB</a>
    <nav class="plate-nav" aria-label="EveMissLab">{nav}</nav>
    <div class="plate-tools">
      <a class="plate-btn" href="{url_path(other)}" hreflang="{'zh-Hant' if other == 'zh' else 'en'}" title="{ch['lang_switch_title']}">{ch['lang_switch']}</a>
      <button class="plate-btn" type="button" data-theme-toggle aria-label="{ch['theme']}">&#9681;</button>
    </div>
  </div>
</header>

<main id="main">
  <div class="shell hero">
    <div class="hero-grid">
      <div>
        <p class="hero-eyebrow">{html.escape(ch['eyebrow'])}</p>
        <h1 class="hero-display">{html.escape(ch['display'])}</h1>
        <p class="hero-stand">{html.escape(ch['standfirst'])}</p>
      </div>
      <figure class="hero-fig">
        <div class="hero-frame">
        <picture>
          <source srcset="/media/miss-eve-3-600.webp 600w, /media/miss-eve-3-1200.webp 1200w"
                  sizes="(min-width: 58rem) 22rem, 100vw" type="image/webp">
          <img src="/media/miss-eve-3-600.jpg"
               srcset="/media/miss-eve-3-600.jpg 600w, /media/miss-eve-3-1200.jpg 1200w"
               sizes="(min-width: 58rem) 22rem, 100vw"
               width="600" height="600" alt="{html.escape(ch['image_caption'])}"
               fetchpriority="high" decoding="async">
        </picture>
        </div>
        <figcaption class="hero-cap"><span>{html.escape(ch['image_caption'])}</span><span>evemisslab.com</span></figcaption>
      </figure>
    </div>
  </div>

  <div class="shell index" id="index">
    <div class="sec-head">
      <h2 class="sec-title">{html.escape(ch['index_title'])}</h2>
      <p class="sec-note">{html.escape(ch['index_note'])}</p>
    </div>
    {render_index(lang)}
  </div>

  <div class="shell how" id="how">
    <div class="sec-head"><h2 class="sec-title">{html.escape(ch['how_title'])}</h2></div>
    {render_how(lang)}
  </div>

  <div class="shell contact" id="contact">
    <div class="sec-head"><h2 class="sec-title">{html.escape(ch['contact_title'])}</h2></div>
    <p class="contact-p">{html.escape(ch['contact'])}</p>
  </div>
</main>

<footer class="foot">
  <div class="shell foot-in">
    <div>
      <p class="foot-co">{C.SITE['company_en']} &nbsp;|&nbsp; {C.SITE['company_zh']}</p>
      <p class="foot-line">&copy; {C.SITE['year']} EVEMISSLAB &middot; {html.escape(ch['footer_rights'])}</p>
    </div>
    <span class="foot-right">{total} sites</span>
  </div>
</footer>

<script src="/assets/app.js" defer></script>
</body>
</html>
"""


def render_sitemap() -> str:
    urls = []
    for lang in ("en", "zh"):
        loc = C.SITE["origin"] + url_path(lang)
        alts = "".join(
            f'<xhtml:link rel="alternate" hreflang="{h}" href="{C.SITE["origin"]}{url_path(l)}"/>'
            for h, l in (("en", "en"), ("zh-Hant", "zh"), ("x-default", "en"))
        )
        urls.append(f"<url><loc>{loc}</loc>{alts}</url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(urls) + "</urlset>\n"
    )


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    (DIST / "index.html").write_text(render_page("en"), encoding="utf-8")
    (DIST / "zh").mkdir()
    (DIST / "zh" / "index.html").write_text(render_page("zh"), encoding="utf-8")

    assets = DIST / "assets"
    assets.mkdir()
    for name in ("styles.css", "app.js"):
        shutil.copyfile(ROOT / "src" / "assets" / name, assets / name)

    media_src = ROOT / "src" / "media"
    media = DIST / "media"
    media.mkdir()
    for f in sorted(media_src.iterdir()):
        if f.is_file():
            shutil.copyfile(f, media / f.name)

    (DIST / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (DIST / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {C.SITE['origin']}/sitemap.xml\n",
        encoding="utf-8",
    )

    total = sum(len(g["sites"]) for g in C.GROUPS["en"])
    assert total == sum(len(g["sites"]) for g in C.GROUPS["zh"]), "index differs by language"
    print(f"built 2 pages, {total} indexed sites, into {DIST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""
Builds evemisslab.com into dist/.

    python build.py

English at the root, Traditional Chinese under /zh/. The AI Research
Laboratory lives under /ai/ (and /zh/ai/); see src/ai_research.py.

Deployment note: this domain is served by the existing Cloudflare **Pages**
project `evemisslab`, not by a Worker. Deploy with

    npx wrangler pages deploy dist --project-name evemisslab

so the custom domain already attached to that project keeps working. Adding a
Worker custom domain for the same hostname would collide with it.
"""

from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import ai_research as A  # noqa: E402
import content as C  # noqa: E402
import shell as S  # noqa: E402

DIST = ROOT / "dist"
CONTENT = ROOT / "content"

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" fill="#14161a"/>
<rect x="6" y="7" width="4" height="18" fill="#f4f3f0"/>
<rect x="12" y="7" width="14" height="3.4" fill="#f4f3f0"/>
<rect x="12" y="14.3" width="10" height="3.4" fill="#f4f3f0"/>
<rect x="12" y="21.6" width="14" height="3.4" fill="#f4f3f0"/>
</svg>
"""

# The parent spec names the archive cell "Archives" and routes it to
# /ai/archives/; the site spec's route map says /ai/archive/. The site spec
# wins, and the other spelling redirects so neither document's link breaks.
REDIRECTS = """/ai/archives/ /ai/archive/ 301
/ai/archives/* /ai/archive/:splat 301
/zh/ai/archives/ /zh/ai/archive/ 301
/zh/ai/archives/* /zh/ai/archive/:splat 301
"""


def url_path(lang: str) -> str:
    return S.url_path(lang)


def render_index(lang: str) -> str:
    out = []
    for g in C.GROUPS[lang]:
        cards = []
        for s in g["sites"]:
            # a host containing a dot is already fully qualified: Logic Matrix moved to
            # unboundedaxiom.org on 2026-08-07 and is no longer under this apex, so the
            # entry names its own host.
            host = s["host"] if "." in s["host"] else f'{s["host"]}.evemisslab.com'
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


def render_matrix(lang: str) -> str:
    """The AI Research Matrix: twelve text links into /ai/, in the hero's left
    column where the statement used to be."""
    ai = C.AI[lang]
    base = url_path(lang) + "ai/"
    cells = "".join(
        f'<li><a class="matrix-cell" href="{base}{slug}/"><span>{html.escape(label)}</span>'
        f'<span class="matrix-arrow" aria-hidden="true">&#8599;</span></a></li>'
        for slug, label in ai["matrix"]
    )
    return (
        f'<div class="matrix-wrap"><p class="hero-eyebrow">{html.escape(ai["matrix_eyebrow"])}</p>'
        f'<nav aria-label="{html.escape(ai["name"])}"><ul class="matrix">{cells}</ul></nav>'
        f'<p class="matrix-foot"><a href="{base}">{html.escape(ai["matrix_home"])} &rarr;</a></p></div>'
    )


def render_page(lang: str) -> str:
    ch = C.CHROME[lang]
    path = url_path(lang)
    total = sum(len(g["sites"]) for g in C.GROUPS[lang])

    jsonld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "EveMissLab",
        "legalName": C.SITE["company_en"],
        "url": C.SITE["origin"],
        "description": ch["standfirst"],
        "subOrganization": [
            {"@type": "ResearchOrganization", "name": C.AI["en"]["full_name"],
             "url": C.SITE["origin"] + "/ai/"},
        ] + [
            {"@type": "WebSite", "name": s["name"],
             "url": f'https://{s["host"] if "." in s["host"] else s["host"] + ".evemisslab.com"}/'}
            for g in C.GROUPS[lang] for s in g["sites"]
        ],
    }

    body = f"""<main id="main">
  <div class="shell hero">
    <div class="hero-grid">
      {render_matrix(lang)}
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

  <div class="shell statement">
    <p class="hero-eyebrow">{html.escape(ch['eyebrow'])}</p>
    <h1 class="hero-display">{html.escape(ch['display'])}</h1>
    <p class="hero-stand">{html.escape(ch['standfirst'])}</p>
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

"""
    return (
        S.head(lang, path, f"EveMissLab — {ch['display']}", ch["standfirst"], jsonld=jsonld)
        + S.header(lang, path)
        + body
        + S.footer(lang, f"{total} sites")
    )


def render_404() -> str:
    """The page Cloudflare Pages serves, with a 404 status, for any path that
    is not a file in dist/.

    Without this file in the output, Pages answers every unknown path with the
    homepage and a 200. That is how /index.php became the single most-crawled
    path on this domain: a static site with no PHP anywhere was returning a
    successful page for it, so the crawlers kept asking. /wp-login.php,
    /admin.php and every other probe answered the same way.

    English only. The 404 should not appear in the sitemap or in the language
    switcher.
    """
    ch = C.CHROME["en"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Not found &middot; EveMissLab</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{S.fonts('en')}">
<link rel="stylesheet" href="/assets/styles.css">
{S.THEME_BOOT}
</head>
<body>
<header class="plate">
  <div class="plate-in">
    <a class="plate-mark" href="/">EVEMISSLAB</a>
  </div>
</header>

<main id="main">
  <div class="shell hero">
    <div>
      <p class="hero-eyebrow">404</p>
      <h1 class="hero-display">No page exists at this address.</h1>
      <p class="hero-stand">This is a static site &mdash; there is no application
        here to log into and no path that takes a query. Start from the
        <a href="/">index</a>, which lists every site the lab runs, or from the
        <a href="/ai/">AI Research Laboratory</a>.</p>
    </div>
  </div>
</main>

<footer class="foot">
  <div class="shell foot-in">
    <div>
      <p class="foot-co">{C.SITE['company_en']} &nbsp;|&nbsp; {C.SITE['company_zh']}</p>
      <p class="foot-line">&copy; {C.SITE['year']} EVEMISSLAB &middot; {html.escape(ch['footer_rights'])}</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def render_sitemap(en_paths: list[str]) -> str:
    origin = C.SITE["origin"]
    urls = []
    for en in en_paths:
        zh = S.path_in(en, "zh")
        alts = (
            f'<xhtml:link rel="alternate" hreflang="en" href="{origin}{en}"/>'
            f'<xhtml:link rel="alternate" hreflang="zh-Hant" href="{origin}{zh}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{origin}{en}"/>'
        )
        for loc in (origin + en, origin + zh):
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

    ai = A.build(CONTENT / "ai", DIST)
    pages = ["/"] + ai["pages"]

    (DIST / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (DIST / "404.html").write_text(render_404(), encoding="utf-8")
    (DIST / "sitemap.xml").write_text(render_sitemap(pages), encoding="utf-8")
    (DIST / "_redirects").write_text(REDIRECTS, encoding="utf-8", newline="\n")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {C.SITE['origin']}/sitemap.xml\n",
        encoding="utf-8",
    )

    total = sum(len(g["sites"]) for g in C.GROUPS["en"])
    assert total == sum(len(g["sites"]) for g in C.GROUPS["zh"]), "index differs by language"
    snap = ai["snapshot"]
    print(
        f"built {2 * len(pages)} pages, {total} indexed sites, "
        f"{snap['object_count']} public research objects and {snap['relation_count']} relations "
        f"({snap['snapshot_id']}), into {DIST}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

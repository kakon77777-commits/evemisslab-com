# -*- coding: utf-8 -*-
"""
Page chrome shared by the front page and the /ai/ projection: <head>, the
nameplate header and the footer.

Every page passes its own path so that the language switch, the canonical
link and the hreflang alternates all point at *this* page in the other
language, not at the homepage.
"""

from __future__ import annotations

import html
import json

import content as C

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


def url_path(lang: str) -> str:
    return "/" if lang == "en" else "/zh/"


def other_lang(lang: str) -> str:
    return "zh" if lang == "en" else "en"


def en_path_of(path: str, lang: str) -> str:
    """The English path of a page given its path in `lang`."""
    if lang == "en":
        return path
    return path[3:] if path.startswith("/zh/") else path


def path_in(en_path: str, lang: str) -> str:
    return en_path if lang == "en" else "/zh" + en_path


def fonts(lang: str) -> str:
    return FONTS_BASE + (FONTS_ZH if lang == "zh" else "") + "&display=swap"


def head(lang: str, path: str, title: str, description: str, *,
         jsonld: dict | None = None, og_type: str = "website", extra: str = "") -> str:
    ch = C.CHROME[lang]
    origin = C.SITE["origin"]
    en = en_path_of(path, lang)
    zh = path_in(en, "zh")
    ld = (
        f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n'
        if jsonld else ""
    )
    return f"""<!doctype html>
<html lang="{ch['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{origin}{path}">
<link rel="alternate" hreflang="en" href="{origin}{en}">
<link rel="alternate" hreflang="zh-Hant" href="{origin}{zh}">
<link rel="alternate" hreflang="x-default" href="{origin}{en}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="EveMissLab">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{origin}{path}">
<meta property="og:image" content="{origin}/media/og.jpg">
<meta property="og:locale" content="{'zh_TW' if lang == 'zh' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f3f0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121316" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts(lang)}">
<link rel="stylesheet" href="/assets/styles.css">
{THEME_BOOT}
{ld}{extra}</head>
<body>
<a class="skip" href="#main">{html.escape(ch['skip'])}</a>
"""


def header(lang: str, path: str, *, current: str | None = None) -> str:
    ch = C.CHROME[lang]
    other = other_lang(lang)
    links = []
    for href, label in ch["nav"]:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a class="plate-link" href="{href}"{cur}>{html.escape(label)}</a>')
    return f"""<header class="plate">
  <div class="plate-in">
    <a class="plate-mark" href="{url_path(lang)}">EVEMISSLAB</a>
    <nav class="plate-nav" aria-label="EveMissLab">{"".join(links)}</nav>
    <div class="plate-tools">
      <a class="plate-btn" href="{path_in(en_path_of(path, lang), other)}" hreflang="{'zh-Hant' if other == 'zh' else 'en'}" title="{ch['lang_switch_title']}">{ch['lang_switch']}</a>
      <button class="plate-btn" type="button" data-theme-toggle aria-label="{ch['theme']}">&#9681;</button>
    </div>
  </div>
</header>
"""


def footer(lang: str, right: str) -> str:
    ch = C.CHROME[lang]
    return f"""<footer class="foot">
  <div class="shell foot-in">
    <div>
      <p class="foot-co">{C.SITE['company_en']} &nbsp;|&nbsp; {C.SITE['company_zh']}</p>
      <p class="foot-line">&copy; {C.SITE['year']} EVEMISSLAB &middot; {html.escape(ch['footer_rights'])}</p>
    </div>
    <span class="foot-right">{html.escape(right)}</span>
  </div>
</footer>

<script src="/assets/app.js" defer></script>
</body>
</html>
"""

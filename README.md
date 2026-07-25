# evemisslab.com

The EveMissLab front page. Its job is to be an index: the lab publishes one
site per thing it builds, and the set keeps growing, so this page is designed
to take twenty entries as gracefully as it takes eight.

## Build

```bash
python build.py
```

Writes two pages (English at the root, Traditional Chinese under `/zh/`) plus
`sitemap.xml`, `robots.txt`, the favicon and the media derivatives into
`dist/`. Standard library only.

## Deploy

```bash
npx wrangler pages deploy dist --project-name evemisslab
```

**Pages, not a Worker.** This domain is served by the existing Cloudflare Pages
project `evemisslab`, which already owns the `evemisslab.com` custom domain.
The three 3M sub-sites use assets-only Workers, but attaching a Worker custom
domain to this hostname would collide with the Pages one. Deploying into the
existing project keeps the DNS untouched.

## Local preview

```bash
python -m http.server 8790 --directory dist
```

## Shape

```
build.py             page shell, index renderer, sitemap
src/content.py       every string, EN and zh-Hant, plus the index itself
src/assets/          styles.css, app.js
src/media/           optimized cover derivatives (committed)
dist/                build output, not committed
```

## Adding a sub-site to the index

Add one entry to both language lists in `src/content.py`, and one tone token in
`styles.css`:

```python
{"host": "newthing", "name": "New Thing", "tone": "newthing",
 "what": "One line, taken from that site's own meta description.",
 "meta": "Apache-2.0 · v1.0"},
```

```css
--t-newthing: #......;   /* light  */
--t-newthing: #......;   /* dark, in both dark blocks */
```

`build.py` asserts that both languages carry the same number of entries, so a
half-finished addition fails the build rather than shipping a page where the
Chinese index is shorter than the English one.

Check the new tone against the page background before shipping — three of the
eight sampled colours had to be darkened to clear 4.5:1 as text on this
lighter paper.

## Design notes

**The index is the site.** The previous version was a manifesto with six
Google Drive links and exactly one link to a sub-site, while seven sub-sites
were live. The page described a research programme and never mentioned that
the programme had shipped anything.

**Parent register.** Every sub-site in the family uses a `--paper` / `--ink`
pair on a warm, muted ground — logic, felra, storyforge, amral, mmr, mmlc and
mlf all do. The old front page was the only neon-on-black page in the set,
which is why it never looked like it belonged to its own children. This one
sits in a neutral register: lighter and less committed than any child, so each
child keeps its own voice.

**Every entry wears its own colour.** The tone on each index row is sampled
from that sub-site's own stylesheet. This is the only page in the family where
the whole palette appears at once, which is the one thing a front page can do
that none of its children can.

**The cover is framed, not bled.** The artwork is saturated and dark; the page
is paper and ink. Putting it inside a bordered dark panel lets it read as
something the lab is showing rather than as a background that failed. The
caption sits outside that panel — page ink on near-black measured 3.15:1.

**Type.** Schibsted Grotesk, Newsreader and Geist Mono, none of them used by
any sibling site. The family shares a build system and a set of conventions,
not a template.

## Licence

Apache-2.0 over the code. The cover artwork is the owner's and is not covered
by that grant — see `NOTICE`.

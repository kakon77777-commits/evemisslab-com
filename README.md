# evemisslab.com

The EveMissLab front page, in two halves. The top is the **AI Research
Matrix**: twelve text links into `/ai/`, the AI Research Laboratory, which is
where research is happening. Below it, **The Index**: the lab publishes one
site per thing it finishes, and the set keeps growing, so that list is
designed to take twenty entries as gracefully as it takes eight.

```text
AI Research Matrix   ->  /ai/   (research in)
Statement
The Index            ->  one site per finished thing (artifacts out)
```

The index includes `Axioglyph｜理符` at `https://axioglyph.evemisslab.com/`.
The child is an assets-only Worker; this apex remains on the existing Pages
project.

## Build

```bash
python build.py
```

Writes the front page (English at the root, Traditional Chinese under `/zh/`),
the whole `/ai/` and `/zh/ai/` tree with its JSON twins, `sitemap.xml`,
`robots.txt`, `_redirects`, the favicon and the media derivatives into
`dist/`. Standard library only. The build fails, rather than shipping, if any
research record fails the publication gate (see below).

## Deploy

```bash
bash deploy.sh
```

Runs `python build.py`, `npx wrangler pages deploy dist --project-name evemisslab`, a smoke test against the live domain (`/`, `/zh/`, `/ai/`, `/zh/ai/`, `/ai/index.json`), then notifies the Continuous Discovery Beacon (beacon.evemiss.com) — only after that smoke test confirms the deploy is actually live. Set `BEACON_SUBMIT_TOKEN_EVEMISSLAB` locally to enable that last step; it's silently skipped otherwise.

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
build.py             front page, 404, sitemap, redirects
src/shell.py         <head>, header and footer shared by every page
src/content.py       every string, EN and zh-Hant: the index, and the /ai/ chrome
src/ai_research.py   the /ai/ projection: gate, HTML, JSON, graph, manifest
content/ai/          research records (one JSON file per object / relation / artifact)
src/assets/          styles.css, app.js
src/media/           optimized cover derivatives (committed)
tests/               regression tests; `python -m pytest tests`
dist/                build output, not committed
```

## AI Research Laboratory — `/ai/`

`/ai/` is the canonical home of EveMissLab's AI research: research lines,
theory, experiments, data, benchmarks, results, programs, papers, systems,
models, an archive, and a research graph. It is built from records, not
prose, so the same source produces the human pages and the machine-readable
layer:

```text
/ai/                          /ai/index.json        map of every endpoint + counts
/ai/experiments/              /ai/experiments/index.json
/ai/experiments/EXP-2026-0001/  …/EXP-2026-0001/index.json
/ai/graph/                    /ai/graph/research-graph.json, relations.json
                              /ai/snapshot.json, /ai/MANIFEST.sha256
```

`/ai/memory/` and `/ai/computation/` are domain views (filters over the same
records), and `/ai/archive/` lists everything `ARCHIVED`, `SUPERSEDED` or
`PAUSED` with its relations intact.

### Records

One file per record under `content/ai/objects/`, `relations/` and
`artifacts/`, named by its stable ID. The shape is the SEDB research-ledger
contract from the implementation pack, so a validated SEDB publication
snapshot can replace these files later without touching the generator:

```json
{
  "id": "EXP-2026-0001",
  "kind": "experiment",
  "label": "4096-D to Layered Carrier Projection",
  "created_at": "2026-08-27",
  "updated_at": "2026-08-27",
  "values": {
    "eml_status": "EXPERIMENTAL",
    "eml_evidence_level": "E2",
    "eml_visibility": "PUBLIC",
    "eml_summary": "…",
    "eml_model_ids": ["MOD-2026-0001"]
  }
}
```

IDs are `RES|THY|EXP|RST|DAT|BEN|MOD|PRG|PAP|SYS|CLM|OBS|EVA|ART|REL-YYYY-NNNN`
and never reused. **Research status and evidence level are separate fields
on purpose** — `ACTIVE` is not a truth claim, and an `ARCHIVED` line can still
carry `E4` evidence. Result records carry `eml_result_type`, and `NEGATIVE`,
`MIXED` and `INCONCLUSIVE` are listed like any other.

Relations are records too (`kind: research_relation`, with
`eml_relation_source / predicate / target / status`), which is what the
object pages' relation tables and `research-graph.json` are built from.

### The gate

`ai_research.project()` runs before anything is written, and one bad record
fails the whole build:

- only `eml_visibility: PUBLIC` objects ship; `INTERNAL`, `EMBARGOED`,
  `RESTRICTED`, `NEVER_PUBLISH` are omitted, and an unknown or missing
  visibility fails closed;
- only fields listed in `content/ai/publication_policy.json` →
  `public_field_keys` are projected, so a new internal field cannot leak just
  because its object is public;
- status, evidence level, result type and relation status must be in the
  policy's vocabularies;
- IDs must be well-formed, unique, and prefixed for their kind;
- a relation's endpoints must exist, and it ships only if both are public;
- `eml_canonical_url`, when present, must equal the route map's URL.

### Adding a research object

Drop a JSON file in the right folder, named by its ID, with
`eml_visibility: PUBLIC`, a status and an evidence level. Add relations as
their own `REL-…` files. Run `python build.py`; if the gate rejects it, the
message says which record and why. Chinese titles and summaries are optional
(`eml_label_zh`, `eml_summary_zh`); until they exist, `/zh/ai/` pages show the
English record marked `lang="en"` rather than silently mixing languages.

The records come from Neo's private research collection (真本體論13), one
research line per extractor package under `tools/`, all written together by

```bash
python tools/extract_all.py "<path to 真本體論13>"
```

Each line owns an ID block (`tools/extract_lib/ledger.py`): the **Adaptive
Epistemic Systems** line uses `…-0001` to `…-0099`, the **Intelligence Physical
Metrology** line `…-0101` to `…-0199`, so adding a record to one line never
renumbers another line's published IDs. Relations are edges, numbered globally
in line order. A third line is a new `tools/extract_<line>/` package plus one
entry in `extract_all.py`.

- **Adaptive Epistemic Systems** (`tools/extract_aes/`): one program, four
  research lines, seven theories, thirteen papers (the eleven-paper series, the
  PACC conjecture, the runtime whitepaper), the AER-0 runtime and the PACC labs
  as systems, three benchmarks, two datasets, the architectures under test as
  models, the AER-0 rounds, PACC-Lab v0.1–v0.13 and PACC-Hybrid v0.1–v0.2 as
  experiments — including three real-model runs of the v0.2 protocol on a local
  9B model — their key results, and one artifact per canonical file with its
  SHA-256. Every series paper's digest is asserted against the series manifest;
  the real-run numbers are read from inside the sealed result bundles.
- **Intelligence Physical Metrology** (`tools/extract_ipm/`): one program, three
  research lines (execution/physical, quality, capability), ten theories (one
  per paper), the five falsifiable propositions F1–F5 as claim records, the ten
  papers plus the canonical index, the XA-02 task pack as a benchmark, the
  XA-03/04/06/06L instrument packages as systems, the Experiment A protocol,
  the XA-05 synthetic smoke gate, the first real-model pilot (36 trials on a
  local 9B model, sealed `REAL_MODEL_PILOT_INCOMPLETE`) with its two results,
  and experiments B–E as declared-not-run. The extractor asserts the whole
  chain of custody the packages declare — paper digests against the canonical
  manifest, XA-04 → XA-02/03, XA-05 → XA-02/03/04, XA-06 → XA-02/03/04/05, the
  diagnostic against the result bundle, the bundle manifest against its members.

Status, evidence level, result type and data basis follow each artifact's own
stated claim boundary — `MIXED` and `NEGATIVE` results are listed like any
other, synthetic runs carry the `SYNTHETIC` badge, and experiments that were
never executed say `NOT RUN`. The records can be regenerated and re-verified
against the private source folders at any time.

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

**Research in, artifacts out.** The hero's left column is the AI Research
Matrix — twelve plain text links, hairlines, no cards, no colour — and the
statement (`One lab. One site per thing it builds.`) moved below it, above
the index, so it reads as the bridge between the two: what the lab is
researching now, and what it has already built and published. The index
itself was not redesigned.

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

# -*- coding: utf-8 -*-
"""
The /ai/ projection — EveMissLab AI Research Laboratory.

    content/ai/{objects,relations,artifacts}/<ID>.json
        -> publication gate (fails closed)
        -> dist/ai/**     HTML in English, plus JSON
        -> dist/zh/ai/**  HTML in Traditional Chinese

Records follow the SEDB research-ledger contract from the implementation
pack — {id, kind, label, created_at, updated_at, values: {eml_*}} — so a
validated SEDB publication snapshot can replace the hand-maintained files
without touching this module. The gate applies the same rules as the pack's
reference exporter: PUBLIC objects only, allow-listed fields only, unknown
visibility fails closed, and a relation survives only if both ends are public.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import content as C
import shell as S

ID_RE = re.compile(r"^(RES|THY|EXP|RST|DAT|BEN|MOD|PRG|PAP|SYS|CLM|OBS|EVA|ART|REL)-\d{4}-\d{4}$")

KIND_PREFIX = {
    "research": "RES", "theory": "THY", "experiment": "EXP", "result": "RST",
    "dataset": "DAT", "benchmark": "BEN", "model": "MOD", "program": "PRG",
    "paper": "PAP", "system": "SYS", "claim": "CLM", "observation": "OBS",
    "evaluation": "EVA", "artifact": "ART", "research_relation": "REL",
}
RESEARCH_KINDS = tuple(k for k in KIND_PREFIX if k not in ("artifact", "research_relation"))

# The site spec's canonical route map (section 4). Claims, observations and
# evaluations have no route in the spec; they get one here so that a record
# of those kinds can never end up unreachable.
SECTION_OF_KIND = {
    "research": "research", "theory": "theory", "experiment": "experiments",
    "dataset": "data", "benchmark": "benchmarks", "result": "results",
    "program": "programs", "paper": "papers", "system": "systems",
    "model": "models", "claim": "claims", "observation": "observations",
    "evaluation": "evaluations",
}
KIND_OF_SECTION = {v: k for k, v in SECTION_OF_KIND.items()}
# Rendered even when empty (Phase A of the spec allows an empty index).
NAV_SECTIONS = ("research", "theory", "experiments", "data", "benchmarks",
                "results", "programs", "models", "papers", "systems")
DOMAIN_VIEWS = {"memory": ("Context & Memory",), "computation": ("Computation",)}
ARCHIVE_STATUSES = ("ARCHIVED", "SUPERSEDED", "PAUSED")
ACTIVE_STATUSES = ("ACTIVE", "EXPERIMENTAL", "VALIDATING", "REPLICATING")
KNOWN_VISIBILITY = ("PUBLIC", "EMBARGOED", "INTERNAL", "RESTRICTED", "NEVER_PUBLISH")

# Rendered by a named part of the page, so not repeated under "recorded fields".
CORE_FIELDS = {
    "eml_status", "eml_evidence_level", "eml_object_version", "eml_canonical_url",
    "eml_provenance", "eml_summary", "eml_summary_zh", "eml_label_zh",
    "eml_primary_domain", "eml_domains", "eml_program_id", "eml_result_type",
    "eml_data_basis", "eml_authors", "eml_ai_collaborators",
}

# Page templates per kind (site spec sections 12-21): (section key, fields).
TEMPLATES = {
    "research": [
        ("questions", ["eml_research_questions"]),
        ("claims", ["eml_claims"]),
        ("limitations", ["eml_limitations"]),
        ("links", ["eml_repository", "eml_repositories", "eml_external_sites"]),
    ],
    "theory": [
        ("definitions", ["eml_definitions"]),
        ("assumptions", ["eml_assumptions"]),
        ("claims", ["eml_claims"]),
        ("formalization", ["eml_formalization"]),
        ("predictions", ["eml_predictions"]),
        ("falsification", ["eml_falsification_conditions"]),
        ("known_limitations", ["eml_known_limitations"]),
    ],
    "experiment": [
        ("hypothesis", ["eml_hypothesis"]),
        ("setup", ["eml_model_ids", "eml_dataset_ids", "eml_benchmark_ids",
                   "eml_hardware", "eml_software_environment", "eml_configuration"]),
        ("procedure", ["eml_procedure"]),
        ("runs", ["eml_run_count", "eml_random_seeds", "eml_controls", "eml_metrics"]),
        ("interpretation", ["eml_interpretation"]),
        ("limitations", ["eml_limitations"]),
        ("reproduction", ["eml_reproduction_instructions", "eml_repository"]),
    ],
    "result": [
        ("observed", ["eml_metrics", "eml_statistical_notes"]),
        ("interpretation", ["eml_interpretation"]),
        ("alternatives", ["eml_alternative_interpretations"]),
        ("limitations", ["eml_limitations"]),
    ],
    "dataset": [
        ("contains", ["eml_description"]),
        ("why", ["eml_purpose"]),
        ("created_how", ["eml_generation_method"]),
        ("transformed", ["eml_cleaning_method"]),
        ("bias", ["eml_known_bias"]),
        ("license", ["eml_license"]),
        ("checksum", ["eml_checksums"]),
        ("format", ["eml_format", "eml_schema", "eml_size", "eml_splits"]),
        ("download", ["eml_download", "eml_repository"]),
    ],
    "benchmark": [
        ("purpose", ["eml_purpose"]),
        ("tasks", ["eml_tasks"]),
        ("metrics", ["eml_metrics"]),
        ("protocol", ["eml_evaluation_protocol"]),
        ("baselines", ["eml_baseline_models", "eml_baseline_results"]),
        ("not_measured", ["eml_limitations"]),
        ("repository", ["eml_repository"]),
    ],
    "model": [
        ("record", ["eml_provider", "eml_model_version", "eml_release", "eml_access_type",
                    "eml_context_window", "eml_modalities", "eml_configuration_notes",
                    "eml_known_behavior_notes", "eml_canonical_external_reference",
                    "eml_repository", "eml_architecture", "eml_training_or_adaptation",
                    "eml_license"]),
    ],
    "program": [
        ("goals", ["eml_goals"]),
        ("open_questions", ["eml_open_questions"]),
        ("milestones", ["eml_milestones"]),
    ],
    "paper": [
        ("record", ["eml_publication_type", "eml_authors", "eml_date",
                    "eml_canonical_publication_url", "eml_doi_or_external_id",
                    "eml_source_artifact", "eml_repository"]),
    ],
    "system": [
        ("purpose", ["eml_purpose"]),
        ("architecture", ["eml_architecture"]),
        ("links", ["eml_repository", "eml_release", "eml_documentation", "eml_demo"]),
    ],
}

# Sections driven by relations rather than fields: (section key, direction, predicates).
REL_SECTIONS = {
    "experiment": [("results", "out", ("produces",))],
    "result": [("claims", "out", ("supports", "contradicts", "qualifies"))],
    "theory": [("evidence", "in", ("tests", "supports", "contradicts"))],
    "program": [("timeline", "in", ("belongs_to", "supports"))],
}

FACETS_OF_SECTION = {
    "research": ("status", "domain", "year", "evidence", "model", "program"),
    "experiments": ("status", "model", "dataset", "benchmark", "year", "research", "result"),
}
DEFAULT_FACETS = ("status", "evidence", "domain", "year")
FACET_OF_KIND = {"model": "model", "dataset": "dataset", "benchmark": "benchmark",
                 "research": "research", "program": "program"}
LD_TYPE = {"paper": "ScholarlyArticle", "dataset": "Dataset"}


class GateError(ValueError):
    """A record failed the publication gate. The build must not ship."""


# --------------------------------------------------------------------------
# source + gate
# --------------------------------------------------------------------------

def load(src: Path):
    policy = json.loads((src / "publication_policy.json").read_bytes().decode("utf-8"))
    records = []
    for sub in ("objects", "relations", "artifacts"):
        folder = src / sub
        if not folder.is_dir():
            continue
        for f in sorted(folder.glob("*.json")):
            rec = json.loads(f.read_bytes().decode("utf-8"))
            if rec.get("id") != f.stem:
                raise GateError(f"{f.name}: file name must equal the record id {rec.get('id')!r}")
            records.append(rec)
    return policy, records


def object_path(kind: str, oid: str, lang: str = "en") -> str:
    return f"{S.url_path(lang)}ai/{SECTION_OF_KIND[kind]}/{oid}/"


def canonical_url(kind: str, oid: str) -> str:
    return C.SITE["origin"] + object_path(kind, oid, "en")


def project(policy: dict, records: list[dict]) -> dict:
    """The publication gate. Any invalid record aborts the whole build."""
    allowed_vis = set(policy["allowed_object_visibility"])
    allowed_status = set(policy["allowed_status"])
    allowed_evidence = set(policy["allowed_evidence_levels"])
    allowed_rel = set(policy["allowed_relation_status"])
    allowed_result = set(policy["allowed_result_types"])
    public_fields = set(policy["public_field_keys"])
    for control in ("eml_visibility", "eml_publication_policy"):
        if control in public_fields:
            raise GateError(f"{control} is projector-control metadata and cannot be public")

    ids = [r.get("id") for r in records]
    dups = sorted({i for i in ids if ids.count(i) > 1}, key=str)
    if dups:
        raise GateError(f"duplicate stable IDs: {dups}")
    by_id = {r["id"]: r for r in records}

    def values(r):
        return r.get("values") or {}

    def vis(r):
        v = values(r).get("eml_visibility")
        if v not in KNOWN_VISIBILITY:
            raise GateError(f"{r.get('id')}: unknown visibility {v!r} — failing closed")
        return v

    for r in records:
        oid, kind, v = r.get("id"), r.get("kind"), values(r)
        if not isinstance(oid, str) or not ID_RE.match(oid):
            raise GateError(f"malformed ID: {oid!r}")
        if kind not in KIND_PREFIX:
            raise GateError(f"{oid}: unknown kind {kind!r}")
        if not oid.startswith(KIND_PREFIX[kind] + "-"):
            raise GateError(f"{oid}: ID prefix does not match kind {kind!r}")
        if not str(r.get("label") or "").strip():
            raise GateError(f"{oid}: empty label")
        vis(r)
        if kind in RESEARCH_KINDS:
            if v.get("eml_status") not in allowed_status:
                raise GateError(f"{oid}: invalid research status {v.get('eml_status')!r}")
            if v.get("eml_evidence_level") not in allowed_evidence:
                raise GateError(f"{oid}: invalid evidence level {v.get('eml_evidence_level')!r}")
            rt = v.get("eml_result_type")
            if rt is not None and rt not in allowed_result:
                raise GateError(f"{oid}: invalid result type {rt!r}")
            cu = v.get("eml_canonical_url")
            if cu is not None and cu != canonical_url(kind, oid):
                raise GateError(f"{oid}: eml_canonical_url {cu!r} does not match the route map "
                                f"({canonical_url(kind, oid)})")
        elif kind == "research_relation":
            for end in ("eml_relation_source", "eml_relation_target"):
                if v.get(end) not in by_id:
                    raise GateError(f"{oid}: {end} {v.get(end)!r} does not exist")
            if not v.get("eml_relation_predicate"):
                raise GateError(f"{oid}: relation has no predicate")
            if v.get("eml_relation_status") not in allowed_rel:
                raise GateError(f"{oid}: invalid relation status {v.get('eml_relation_status')!r}")
        elif kind == "artifact" and not v.get("eml_artifact_uri"):
            raise GateError(f"{oid}: artifact has no URI")

    def public(r):
        return {
            "id": r["id"], "kind": r["kind"], "label": r["label"],
            "created_at": r.get("created_at"), "updated_at": r.get("updated_at"),
            "values": {k: x for k, x in values(r).items() if k in public_fields},
        }

    objects = [public(r) for r in records if r["kind"] in RESEARCH_KINDS and vis(r) in allowed_vis]
    artifacts = [public(r) for r in records if r["kind"] == "artifact" and vis(r) in allowed_vis]
    public_ids = {o["id"] for o in objects} | {a["id"] for a in artifacts}
    relations = [
        public(r) for r in records
        if r["kind"] == "research_relation" and vis(r) in allowed_vis
        and values(r)["eml_relation_source"] in public_ids
        and values(r)["eml_relation_target"] in public_ids
    ]
    by_id_key = lambda x: x["id"]  # noqa: E731
    return {
        "objects": sorted(objects, key=by_id_key),
        "relations": sorted(relations, key=by_id_key),
        "artifacts": sorted(artifacts, key=by_id_key),
    }


def canonical_json(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def make_snapshot(projected: dict) -> dict:
    digest = hashlib.sha256(canonical_json(projected)).hexdigest()[:12]
    return {
        "snapshot_id": f"AI-SNAPSHOT-v0.1-{digest}",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "format_version": "0.1",
        "sedb_baseline": "v0.4B contract; static source content/ai/",
        "generator_version": "evemisslab-com ai_research 0.1",
        "object_count": len(projected["objects"]),
        "relation_count": len(projected["relations"]),
        "artifact_count": len(projected["artifacts"]),
    }


# --------------------------------------------------------------------------
# rendering helpers
# --------------------------------------------------------------------------

def esc(x) -> str:
    return html.escape("" if x is None else str(x), quote=True)


def d10(s) -> str:
    return (s or "")[:10]


def T(lang: str) -> dict:
    return C.AI[lang]


def badge(text) -> str:
    return f'<span class="badge">{esc(text)}</span>'


def localized(lang: str, o: dict, key: str) -> tuple[str, str]:
    """(escaped text, lang attribute). A Chinese page that has to fall back to
    the English record says so in markup instead of pretending."""
    v = o["values"]
    if key == "label":
        en, zh = o["label"], v.get("eml_label_zh")
    else:
        en, zh = v.get("eml_summary") or "", v.get("eml_summary_zh")
    if lang == "zh" and zh:
        return esc(zh), ""
    return esc(en), (' lang="en"' if lang == "zh" and en else "")


def latest(items, cap=None):
    items = sorted(items, key=lambda o: o["id"])
    items.sort(key=lambda o: o.get("updated_at") or "", reverse=True)
    return items[:cap] if cap else items


class Model:
    def __init__(self, projected: dict, snapshot: dict):
        self.objects = projected["objects"]
        self.relations = projected["relations"]
        self.artifacts = projected["artifacts"]
        self.snapshot = snapshot
        self.by_id = {o["id"]: o for o in self.objects}
        self.by_id.update({a["id"]: a for a in self.artifacts})
        self.by_kind: dict[str, list] = {}
        for o in self.objects:
            self.by_kind.setdefault(o["kind"], []).append(o)
        self.out: dict[str, list] = {}
        self.inc: dict[str, list] = {}
        for r in self.relations:
            v = r["values"]
            self.out.setdefault(v["eml_relation_source"], []).append(r)
            self.inc.setdefault(v["eml_relation_target"], []).append(r)

    def kind(self, k):
        return self.by_kind.get(k, [])

    def neighbours(self, oid):
        seen = []
        for r in self.out.get(oid, []):
            seen.append(r["values"]["eml_relation_target"])
        for r in self.inc.get(oid, []):
            seen.append(r["values"]["eml_relation_source"])
        return seen

    def domains_of(self, o):
        v = o["values"]
        out = []
        if v.get("eml_primary_domain"):
            out.append(v["eml_primary_domain"])
        for d in v.get("eml_domains") or []:
            if d not in out:
                out.append(d)
        return out

    def section_items(self, section):
        if section in KIND_OF_SECTION:
            return list(self.kind(KIND_OF_SECTION[section]))
        if section in DOMAIN_VIEWS:
            wanted = DOMAIN_VIEWS[section]
            return [o for o in self.objects if any(d in wanted for d in self.domains_of(o))]
        if section == "archive":
            return [o for o in self.objects if o["values"]["eml_status"] in ARCHIVE_STATUSES]
        raise KeyError(section)

    def facets(self, o):
        v = o["values"]
        f = {k: [] for k in ("status", "evidence", "domain", "year", "program",
                             "model", "dataset", "benchmark", "research", "result")}
        f["status"].append(v["eml_status"])
        f["evidence"].append(v["eml_evidence_level"])
        if o.get("updated_at"):
            f["year"].append(d10(o["updated_at"])[:4])
        f["domain"].extend(self.domains_of(o))
        if v.get("eml_program_id"):
            f["program"].append(v["eml_program_id"])
        for key, facet in (("eml_model_ids", "model"), ("eml_dataset_ids", "dataset"),
                           ("eml_benchmark_ids", "benchmark")):
            for i in v.get(key) or []:
                if i not in f[facet]:
                    f[facet].append(i)
        if v.get("eml_result_type"):
            f["result"].append(v["eml_result_type"])
        for other in self.neighbours(o["id"]):
            rec = self.by_id.get(other)
            facet = FACET_OF_KIND.get(rec["kind"]) if rec else None
            if facet and other not in f[facet]:
                f[facet].append(other)
        return f

    def facet_label(self, lang, facet, value):
        if facet == "evidence":
            return f'{value} — {T(lang)["evidence"].get(value, "")}'
        if facet in FACET_OF_KIND.values() and value in self.by_id:
            return f'{value} — {self.by_id[value]["label"]}'
        return value

    def stats(self):
        def active(kind):
            return sum(1 for o in self.kind(kind) if o["values"]["eml_status"] in ACTIVE_STATUSES)
        return {
            "active_research": active("research"),
            "active_experiments": active("experiment"),
            "datasets": len(self.kind("dataset")),
            "benchmarks": len(self.kind("benchmark")),
            "programs": len(self.kind("program")),
        }

    # ---- fragments -------------------------------------------------------

    def obj_link(self, lang, oid, self_id=None):
        rec = self.by_id.get(oid)
        if rec is None:
            return f"<code>{esc(oid)}</code>"
        label, la = localized(lang, rec, "label")
        if oid == self_id:
            return f'<strong><code>{esc(oid)}</code> <span{la}>{label}</span></strong>'
        if rec["kind"] == "artifact":
            uri = rec["values"].get("eml_artifact_uri", "")
            return f'<code>{esc(oid)}</code> <span{la}>{label}</span> <code>{esc(uri)}</code>'
        return (f'<a href="{object_path(rec["kind"], oid, lang)}">'
                f'<code>{esc(oid)}</code> <span{la}>{label}</span></a>')

    def domain_link(self, lang, domain):
        for slug, wanted in DOMAIN_VIEWS.items():
            if domain in wanted:
                return f'<a href="{S.url_path(lang)}ai/{slug}/">{esc(domain)}</a>'
        return esc(domain)

    def render_value(self, lang, x):
        if isinstance(x, bool):
            return "true" if x else "false"
        if isinstance(x, (int, float)):
            return esc(x)
        if isinstance(x, str):
            if ID_RE.match(x):
                return self.obj_link(lang, x)
            if x.startswith(("http://", "https://")):
                return f'<a href="{esc(x)}">{esc(x)}</a>'
            paras = [p.strip() for p in x.split("\n\n") if p.strip()]
            if len(paras) <= 1:
                return esc(x).replace("\n", "<br>")
            return "".join(f"<p>{esc(p).replace(chr(10), '<br>')}</p>" for p in paras)
        if isinstance(x, list):
            return "<ul>" + "".join(f"<li>{self.render_value(lang, i)}</li>" for i in x) + "</ul>"
        if isinstance(x, dict):
            rows = "".join(
                f"<div><dt><code>{esc(k)}</code></dt><dd>{self.render_value(lang, i)}</dd></div>"
                for k, i in x.items()
            )
            return f'<dl class="kv kv-nested">{rows}</dl>'
        return esc(x)

    def card(self, lang, o):
        t = T(lang)
        v, kind = o["values"], o["kind"]
        title, la = localized(lang, o, "label")
        summ, sa = localized(lang, o, "summary")
        meta = [badge(v["eml_status"]), badge(v["eml_evidence_level"])]
        if v.get("eml_result_type"):
            meta.append(badge(v["eml_result_type"]))
        if v.get("eml_data_basis"):
            meta.append(badge(v["eml_data_basis"]))
        if v.get("eml_primary_domain"):
            meta.append(f'<span>{esc(v["eml_primary_domain"])}</span>')
        if o.get("updated_at"):
            meta.append(f'<span>{esc(t["labels"]["updated"])} {esc(d10(o["updated_at"]))}</span>')
        data = "".join(
            f' data-{k}="{esc("|".join(vals))}"' for k, vals in self.facets(o).items() if vals
        )
        summary = f'<span class="rc-sum"{sa}>{summ}</span>' if summ else ""
        return (
            f'<li class="rc" data-item{data}><a class="rc-link" href="{object_path(kind, o["id"], lang)}">'
            f'<span class="rc-id"><span class="rc-kind">{esc(t["kinds"][kind])}</span>'
            f'<span class="rc-code">{esc(o["id"])}</span></span>'
            f'<span class="rc-body"><span class="rc-title"{la}>{title}</span>{summary}'
            f'<span class="rc-meta">{" ".join(meta)}</span></span></a></li>'
        )

    def cards(self, lang, items):
        t = T(lang)
        if not items:
            return f'<p class="empty">{esc(t["labels"]["empty"])}</p>'
        return f'<ul class="rlist">{"".join(self.card(lang, o) for o in items)}</ul>'

    def subnav(self, lang, current):
        t = T(lang)
        base = S.url_path(lang) + "ai/"
        links = []
        for slug, label in t["subnav"]:
            href = base + (f"{slug}/" if slug else "")
            cur = ' aria-current="page"' if slug == current else ""
            links.append(f'<a class="subnav-link" href="{href}"{cur}>{esc(label)}</a>')
        return (f'<nav class="subnav" aria-label="{esc(t["name"])}">'
                f'<div class="subnav-in">{"".join(links)}</div></nav>\n')

    def relations_table(self, lang, rels, self_id=None, *, caption=None):
        t = T(lang)
        head = "".join(f'<th scope="col">{esc(c)}</th>' for c in t["rel_cols"])
        rows = []
        for r in rels:
            v = r["values"]
            rows.append(
                f'<tr><td>{self.obj_link(lang, v["eml_relation_source"], self_id)}</td>'
                f'<td><code>{esc(v["eml_relation_predicate"])}</code></td>'
                f'<td>{self.obj_link(lang, v["eml_relation_target"], self_id)}</td>'
                f'<td><code>{esc(v["eml_relation_status"])}</code></td>'
                f'<td><code>{esc(r["id"])}</code></td></tr>'
            )
        cap = f"<caption>{esc(caption)}</caption>" if caption else ""
        return (f'<div class="tbl-wrap"><table class="tbl">{cap}<thead><tr>{head}</tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table></div>')

    def page(self, lang, path, *, title, description, body, current, jsonld=None, extra=""):
        t = T(lang)
        right = f'{len(self.objects)} {t["labels"]["objects"]}'
        return (
            S.head(lang, path, title, description, jsonld=jsonld, extra=extra)
            + S.header(lang, path, current=S.url_path(lang) + "ai/")
            + self.subnav(lang, current)
            + f'<main id="main" class="ai-main">\n{body}</main>\n'
            + S.footer(lang, right)
        )

    def json_link(self, en_json):
        return f'<link rel="alternate" type="application/json" href="{en_json}">\n'

    # ---- pages -----------------------------------------------------------

    def render_home(self, lang):
        t = T(lang)
        base = S.url_path(lang) + "ai/"
        st = self.stats()
        stats = "".join(
            f'<div><dt>{esc(label)}</dt><dd>{st[key]}</dd></div>' for key, label in t["stats"]
        )
        snap = self.snapshot
        snapline = (
            f'<p class="ai-snap">{esc(t["labels"]["snapshot"])} <code>{esc(snap["snapshot_id"])}</code>'
            f' · {snap["object_count"]} {esc(t["labels"]["objects"])}'
            f' · {snap["relation_count"]} {esc(t["labels"]["relations"])}'
            f' · {esc(t["labels"]["generated"])} {esc(d10(snap["created_at"]))}'
            f' · <a href="/ai/index.json"><code>index.json</code></a></p>'
        )
        hero = f"""  <div class="shell ai-hero">
    <p class="hero-eyebrow">EveMissLab</p>
    <h1 class="ai-title">{esc(t["name"])}</h1>
    <p class="ai-tag">{esc(t["tagline"])}</p>
    <p class="ai-lede">{esc(t["lede"])}</p>
    <dl class="stats">{stats}</dl>
    {snapline}
  </div>
"""
        not_archived = [o for o in self.objects if o["values"]["eml_status"] not in ARCHIVE_STATUSES]
        by = lambda k: [o for o in not_archived if o["kind"] == k]  # noqa: E731
        active_exp = [o for o in self.kind("experiment") if o["values"]["eml_status"] in ACTIVE_STATUSES]

        def section(section, home_key, items, cap=6, extra=""):
            head = (f'<div class="sec-head sec-head-row"><h2 class="sec-title" id="{section}">'
                    f'{esc(t["home"].get(home_key) or t["sections"][section][0])}</h2>'
                    f'<a class="sec-more" href="{base}{section}/">{esc(t["labels"]["view_all"])} ({len(items)}) →</a></div>')
            return f'  <section class="shell ai-sec">{head}{self.cards(lang, latest(items, cap))}{extra}</section>\n'

        def subsection(section, items, cap=4):
            title, _ = t["sections"][section]
            return (f'<h3 class="sec-sub"><a href="{base}{section}/">{esc(title)}</a> · {len(items)}</h3>'
                    f'{self.cards(lang, latest(items, cap))}')

        parts = [hero]
        parts.append(section("research", "research", by("research")))
        parts.append(section("theory", "theory", by("theory")))
        # sections the spec leaves optional: shown only once a record of that kind exists
        for kind, sec in (("claim", "claims"), ("observation", "observations"), ("evaluation", "evaluations")):
            if by(kind):
                parts.append(section(sec, sec, by(kind)))
        parts.append(section("experiments", "experiments", active_exp))
        parts.append(section("results", "results", by("result")))
        parts.append(
            f'  <section class="shell ai-sec"><div class="sec-head"><h2 class="sec-title" id="evidence">'
            f'{esc(t["home"]["evidence"])}</h2></div>'
            f'{subsection("data", by("dataset"))}{subsection("benchmarks", by("benchmark"))}</section>\n'
        )
        parts.append(section("programs", "programs", by("program")))
        parts.append(section("models", "models", by("model")))
        parts.append(section("papers", "papers", by("paper")))
        parts.append(section("systems", "systems", by("system")))

        graph_links = (
            f'<p class="ai-links"><a href="{base}graph/">{esc(t["sections"]["graph"][0])} →</a>'
            f' · <a href="/ai/graph/research-graph.json"><code>research-graph.json</code></a>'
            f' · <a href="/ai/graph/relations.json"><code>relations.json</code></a></p>'
        )
        graph_body = (self.relations_table(lang, self.relations[:20]) if self.relations
                      else f'<p class="empty">{esc(t["labels"]["no_relations"])}</p>')
        parts.append(
            f'  <section class="shell ai-sec"><div class="sec-head sec-head-row"><h2 class="sec-title" id="graph">'
            f'{esc(t["home"]["graph"])}</h2><a class="sec-more" href="{base}graph/">{esc(t["labels"]["view_all"])} ({len(self.relations)}) →</a></div>'
            f'{graph_body}{graph_links}</section>\n'
        )
        parts.append(section("archive", "archive", self.section_items("archive")))

        statuses = "".join(
            f'<div><dt>{badge(k)}</dt><dd>{esc(d)}</dd></div>' for k, d in t["statuses"].items()
        )
        evidence = "".join(
            f'<div><dt>{badge(k)}</dt><dd>{esc(d)}</dd></div>' for k, d in t["evidence"].items()
        )
        basis = "".join(
            f'<div><dt>{badge(k)}</dt><dd>{esc(d)}</dd></div>' for k, d in t["data_basis"].items()
        )
        parts.append(
            f'  <section class="shell ai-sec"><div class="sec-head"><h2 class="sec-title" id="vocab">'
            f'{esc(t["home"]["vocab"])}</h2></div><div class="vocab">'
            f'<dl class="kv"><div><dt>{esc(t["labels"]["status"])}</dt><dd></dd></div>{statuses}</dl>'
            f'<dl class="kv"><div><dt>{esc(t["labels"]["evidence"])}</dt><dd></dd></div>{evidence}</dl>'
            f'<dl class="kv"><div><dt>{esc(t["labels"]["data_basis"])}</dt><dd></dd></div>{basis}</dl>'
            f'</div><p class="vocab-note">{esc(t["vocab_note"])}</p>'
            f'<p class="vocab-note">{esc(t["basis_note"])}</p></section>\n'
        )
        jsonld = {
            "@context": "https://schema.org",
            "@type": "ResearchOrganization",
            "name": t["full_name"],
            "url": C.SITE["origin"] + "/ai/",
            "description": t["tagline"],
            "parentOrganization": {"@type": "Organization", "name": "EveMissLab", "url": C.SITE["origin"]},
        }
        return self.page(lang, base, title=f'{t["name"]} · EveMissLab', description=t["tagline"],
                         body="".join(parts), current="", jsonld=jsonld, extra=self.json_link("/ai/index.json"))

    def render_index(self, lang, section, items):
        t = T(lang)
        title, note = t["sections"][section]
        path = S.url_path(lang) + f"ai/{section}/"
        wanted = FACETS_OF_SECTION.get(section, DEFAULT_FACETS)
        filters = []
        for facet in wanted:
            counts: dict[str, int] = {}
            for o in items:
                for x in self.facets(o).get(facet, []):
                    counts[x] = counts.get(x, 0) + 1
            if len(counts) < 2:
                continue
            opts = "".join(
                f'<option value="{esc(x)}">{esc(self.facet_label(lang, facet, x))} ({n})</option>'
                for x, n in sorted(counts.items())
            )
            filters.append(
                f'<label class="flt"><span>{esc(t["facets"][facet])}</span>'
                f'<select data-facet="{facet}"><option value="">{esc(t["labels"]["all"])}</option>{opts}</select></label>'
            )
        form = ""
        if filters:
            form = (f'<form class="filters" data-filters aria-label="{esc(t["labels"]["filter"])}">'
                    f'{"".join(filters)}<span class="flt-count"><span data-count>{len(items)}</span> / {len(items)}</span></form>')
        body = f"""  <div class="shell pg-head">
    <p class="pg-eyebrow"><span>{esc(t["name"])}</span><span>{len(items)} {esc(t["labels"]["records"])}</span></p>
    <h1 class="pg-title">{esc(title)}</h1>
    <p class="pg-lede">{esc(note)}</p>
  </div>
  <div class="shell ai-sec" data-filter-root>{form}{self.cards(lang, latest(items))}</div>
"""
        jsonld = {
            "@context": "https://schema.org", "@type": "CollectionPage", "name": title,
            "url": C.SITE["origin"] + path,
            "isPartOf": {"@type": "WebSite", "name": t["full_name"], "url": C.SITE["origin"] + "/ai/"},
        }
        return self.page(lang, path, title=f'{title} · {t["name"]} · EveMissLab', description=note,
                         body=body, current=section, jsonld=jsonld,
                         extra=self.json_link(f"/ai/{section}/index.json"))

    def render_graph(self, lang):
        t = T(lang)
        title, note = t["sections"]["graph"]
        path = S.url_path(lang) + "ai/graph/"
        table = (self.relations_table(lang, self.relations) if self.relations
                 else f'<p class="empty">{esc(t["labels"]["no_relations"])}</p>')
        body = f"""  <div class="shell pg-head">
    <p class="pg-eyebrow"><span>{esc(t["name"])}</span><span>{len(self.relations)} {esc(t["labels"]["relations"])}</span></p>
    <h1 class="pg-title">{esc(title)}</h1>
    <p class="pg-lede">{esc(note)}</p>
    <p class="ai-links"><a href="/ai/graph/research-graph.json"><code>research-graph.json</code></a> · <a href="/ai/graph/relations.json"><code>relations.json</code></a></p>
  </div>
  <div class="shell ai-sec">{table}</div>
"""
        return self.page(lang, path, title=f'{title} · {t["name"]} · EveMissLab', description=note,
                         body=body, current=None, extra=self.json_link("/ai/graph/research-graph.json"))

    def kv_section(self, lang, key, pairs):
        t = T(lang)
        rows = "".join(
            f'<div><dt><code>{esc(f[4:] if f.startswith("eml_") else f)}</code></dt>'
            f'<dd>{self.render_value(lang, x)}</dd></div>' for f, x in pairs
        )
        return f'<section class="obj-sec"><h2 class="obj-h">{esc(t["tpl"][key])}</h2><dl class="kv">{rows}</dl></section>'

    def render_object(self, lang, o):
        t = T(lang)
        v, kind, oid = o["values"], o["kind"], o["id"]
        path = object_path(kind, oid, lang)
        json_path = object_path(kind, oid, "en") + "index.json"
        title, la = localized(lang, o, "label")
        summ, sa = localized(lang, o, "summary")

        rows = [
            (t["labels"]["status"], f'{badge(v["eml_status"])} <span class="meta-help">{esc(t["statuses"].get(v["eml_status"], ""))}</span>'),
            (t["labels"]["evidence"], f'{badge(v["eml_evidence_level"])} <span class="meta-help">{esc(t["evidence"].get(v["eml_evidence_level"], ""))}</span>'),
        ]
        if v.get("eml_result_type"):
            rows.append((t["labels"]["result"], badge(v["eml_result_type"])))
        if v.get("eml_data_basis"):
            rows.append((t["labels"]["data_basis"], f'{badge(v["eml_data_basis"])} <span class="meta-help">{esc(t["data_basis"].get(v["eml_data_basis"], ""))}</span>'))
        if v.get("eml_object_version"):
            rows.append((t["labels"]["version"], esc(v["eml_object_version"])))
        if o.get("updated_at"):
            rows.append((t["labels"]["updated"], esc(d10(o["updated_at"]))))
        if o.get("created_at"):
            rows.append((t["labels"]["created"], esc(d10(o["created_at"]))))
        domains = self.domains_of(o)
        if domains:
            rows.append((t["labels"]["domain"], ", ".join(self.domain_link(lang, d) for d in domains)))
        if v.get("eml_program_id"):
            rows.append((t["labels"]["program"], self.obj_link(lang, v["eml_program_id"])))
        if v.get("eml_authors"):
            rows.append((t["labels"]["authors"], esc(", ".join(v["eml_authors"]))))
        if v.get("eml_ai_collaborators"):
            rows.append((t["labels"]["ai_collaborators"], esc(", ".join(v["eml_ai_collaborators"]))))
        meta = '<dl class="meta">' + "".join(
            f'<div><dt>{esc(k)}</dt><dd>{val}</dd></div>' for k, val in rows) + "</dl>"

        consumed = set(CORE_FIELDS)
        parts = []
        for key, fields in TEMPLATES.get(kind, []):
            present = [f for f in fields if v.get(f) not in (None, "", [], {})]
            if not present:
                continue
            consumed.update(present)
            parts.append(self.kv_section(lang, key, [(f, v[f]) for f in present]))
        for key, direction, preds in REL_SECTIONS.get(kind, []):
            pool = self.out if direction == "out" else self.inc
            rels = [r for r in pool.get(oid, []) if r["values"]["eml_relation_predicate"] in preds]
            if rels:
                parts.append(f'<section class="obj-sec"><h2 class="obj-h">{esc(t["tpl"][key])}</h2>'
                             f'{self.relations_table(lang, rels, oid)}</section>')
        rest = [(f, v[f]) for f in v if f not in consumed]
        if rest:
            parts.append(self.kv_section(lang, "fields", rest))

        rels = self.out.get(oid, []) + self.inc.get(oid, [])
        rel_body = (self.relations_table(lang, rels, oid) if rels
                    else f'<p class="empty">{esc(t["labels"]["no_relations"])}</p>')
        parts.append(f'<section class="obj-sec"><h2 class="obj-h">{esc(t["tpl"]["relations"])}</h2>{rel_body}</section>')

        hist = [
            (t["labels"]["canonical"], f'<a href="{esc(canonical_url(kind, oid))}">{esc(canonical_url(kind, oid))}</a>'),
            (t["labels"]["json"], f'<a href="{esc(json_path)}"><code>{esc(json_path)}</code></a>'),
            (t["labels"]["snapshot"], f'<code>{esc(self.snapshot["snapshot_id"])}</code>'),
        ]
        if v.get("eml_provenance"):
            hist.append((t["labels"]["provenance"], self.render_value(lang, v["eml_provenance"])))
        parts.append(
            f'<section class="obj-sec"><h2 class="obj-h">{esc(t["tpl"]["history"])}</h2><dl class="kv">'
            + "".join(f'<div><dt>{esc(k)}</dt><dd>{val}</dd></div>' for k, val in hist) + "</dl></section>"
        )

        body = f"""  <div class="shell pg-head">
    <p class="pg-eyebrow"><span>{esc(t["kinds"][kind])}</span><span>{esc(oid)}</span>{f'<span>v{esc(v["eml_object_version"])}</span>' if v.get("eml_object_version") else ""}</p>
    <h1 class="pg-title"{la}>{title}</h1>
    {f'<p class="pg-lede"{sa}>{summ}</p>' if summ else ""}
    {meta}
  </div>
  <div class="shell obj-body">{"".join(parts)}</div>
"""
        ld_type = LD_TYPE.get(kind, "CreativeWork")
        if kind == "system" and v.get("eml_repository"):
            ld_type = "SoftwareSourceCode"
        jsonld = {k: x for k, x in {
            "@context": "https://schema.org", "@type": ld_type, "name": o["label"],
            "identifier": oid, "url": canonical_url(kind, oid),
            "description": v.get("eml_summary"), "dateModified": o.get("updated_at"),
            "version": v.get("eml_object_version"),
            "isPartOf": {"@type": "WebSite", "name": t["full_name"], "url": C.SITE["origin"] + "/ai/"},
        }.items() if x is not None}
        page_title = f'{o["label"]} · {oid} · {t["name"]} · EveMissLab'
        return self.page(lang, path, title=page_title, description=v.get("eml_summary") or o["label"],
                         body=body, current=SECTION_OF_KIND[kind], jsonld=jsonld,
                         extra=self.json_link(json_path))

    # ---- machine-readable -----------------------------------------------

    def public_record(self, o):
        rec = dict(o)
        rec["canonical_url"] = canonical_url(o["kind"], o["id"])
        rec["json"] = object_path(o["kind"], o["id"]) + "index.json"
        return rec

    def object_json(self, o):
        rec = self.public_record(o)
        rec["relations"] = [
            {"id": r["id"], "predicate": r["values"]["eml_relation_predicate"],
             "source": r["values"]["eml_relation_source"], "target": r["values"]["eml_relation_target"],
             "status": r["values"]["eml_relation_status"]}
            for r in self.out.get(o["id"], []) + self.inc.get(o["id"], [])
        ]
        rec["snapshot"] = self.snapshot
        return rec

    def section_json(self, section, items):
        return {
            "section": section,
            "kind": KIND_OF_SECTION.get(section),
            "canonical": C.SITE["origin"] + f"/ai/{section}/",
            "count": len(items),
            "records": [self.public_record(o) for o in latest(items)],
            "snapshot": self.snapshot,
        }

    def graph_json(self):
        nodes = [{
            "id": o["id"], "type": o["kind"], "title": o["label"],
            "status": o["values"].get("eml_status"), "evidence_level": o["values"].get("eml_evidence_level"),
            "url": canonical_url(o["kind"], o["id"]),
        } for o in self.objects]
        nodes += [{"id": a["id"], "type": "artifact", "title": a["label"],
                   "uri": a["values"].get("eml_artifact_uri")} for a in self.artifacts]
        edges = [{
            "id": r["id"], "relation_type": r["values"]["eml_relation_predicate"],
            "source": r["values"]["eml_relation_source"], "target": r["values"]["eml_relation_target"],
            "status": r["values"]["eml_relation_status"],
            "provenance": r["values"].get("eml_relation_provenance"),
        } for r in self.relations]
        return {"snapshot": self.snapshot, "nodes": nodes, "edges": edges}

    def index_json(self, sections):
        origin = C.SITE["origin"]
        out = {
            "site": T("en")["full_name"], "version": "0.1",
            "canonical": origin + "/ai/", "snapshot": self.snapshot,
            "counts": {k: len(self.kind(k)) for k in RESEARCH_KINDS},
        }
        out["counts"]["relations"] = len(self.relations)
        out["counts"]["artifacts"] = len(self.artifacts)
        for section in sections:
            key = {"data": "datasets"}.get(section, section)
            out[key] = f"/ai/{section}/index.json"
        out["graph"] = "/ai/graph/research-graph.json"
        out["relations"] = "/ai/graph/relations.json"
        out["snapshot_file"] = "/ai/snapshot.json"
        out["manifest"] = "/ai/MANIFEST.sha256"
        return out


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------

def pretty_json(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def build(src: Path, dist: Path) -> dict:
    policy, records = load(src)
    projected = project(policy, records)
    snapshot = make_snapshot(projected)
    m = Model(projected, snapshot)
    pages: list[str] = []

    def write_html(en_path: str, render):
        for lang in ("en", "zh"):
            f = dist / S.path_in(en_path, lang).strip("/") / "index.html"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(render(lang), encoding="utf-8")
        pages.append(en_path)

    def write_json(en_path: str, value):
        f = dist / en_path.lstrip("/")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(pretty_json(value), encoding="utf-8", newline="\n")

    write_html("/ai/", m.render_home)

    sections = list(NAV_SECTIONS)
    for section in ("claims", "observations", "evaluations"):
        if m.section_items(section):
            sections.append(section)
    sections += ["memory", "computation", "archive"]
    for section in sections:
        items = m.section_items(section)
        write_html(f"/ai/{section}/", lambda lang, s=section, i=items: m.render_index(lang, s, i))
        write_json(f"/ai/{section}/index.json", m.section_json(section, items))

    for o in m.objects:
        write_html(object_path(o["kind"], o["id"]), lambda lang, o=o: m.render_object(lang, o))
        write_json(object_path(o["kind"], o["id"]) + "index.json", m.object_json(o))

    write_html("/ai/graph/", m.render_graph)
    write_json("/ai/graph/research-graph.json", m.graph_json())
    write_json("/ai/graph/relations.json", m.relations)
    write_json("/ai/snapshot.json", {"snapshot": snapshot, **projected})
    write_json("/ai/index.json", m.index_json(sections))

    lines = []
    for p in sorted((dist / "ai").rglob("*.json")):
        lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(dist).as_posix()}")
    (dist / "ai" / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    return {"pages": pages, "snapshot": snapshot, "model": m}

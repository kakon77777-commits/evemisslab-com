# Shared ledger for the research-line extractors.
#
# Every research line gets its own Ledger with an ID block: the objects and
# artifacts of line k are numbered from base_k + 1 (Adaptive Epistemic Systems:
# 0001–0099, Intelligence Physical Metrology: 0101–0199, …), so adding a record
# to one line never renumbers another line's published IDs. Relations are edges,
# not published objects: they are numbered globally, in line order, when all
# lines are written together by tools/extract_all.py — adding a relation to an
# earlier line shifts later relation IDs, which is documented and harmless
# (relations have no canonical URL; the snapshot id changes on every content
# change anyway).
#
# The source folders are private (Neo's research collection); they are passed on
# the command line and never recorded in the output beyond file names and hashes.
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ORIGIN = "https://evemisslab.com"
SECTION = {
    "research": "research", "theory": "theory", "experiment": "experiments",
    "dataset": "data", "benchmark": "benchmarks", "result": "results",
    "program": "programs", "paper": "papers", "system": "systems", "model": "models",
    "claim": "claims", "observation": "observations", "evaluation": "evaluations",
}
ID_RE = re.compile(r"^[A-Z]{3}-\d{4}-(\d{4})$")
BLOCK = 100
MEDIA = {"md": "text/markdown; charset=utf-8", "zip": "application/zip", "json": "application/json",
         "csv": "text/csv; charset=utf-8", "png": "image/png", "yaml": "application/yaml", "py": "text/x-python"}


class Ledger:
    def __init__(self, *, base: int, slug: str, collection: str, generator: str, program: str | None,
                 authors: list[str], ai_collaborators: list[str], extracted_at: str = "2026-09-11",
                 extracted_by: str = "Splice (Claude Code), reading the canonical UTF-8 sources and each package's own reports"):
        assert base % BLOCK == 0, base
        self.base, self.slug, self.collection, self.program = base, slug, collection, program
        self.authors, self.ai_collaborators, self.extracted_at = authors, ai_collaborators, extracted_at
        self.PROV = {
            "source": f"EveMissLab research collection: {collection}",
            "extracted_by": extracted_by,
            "extracted_at": extracted_at,
            "generator": generator,
            "claim_boundary": "status, evidence level and result type follow the source artifact's own stated claim boundary; nothing is upgraded beyond what the report supports",
        }
        self.SRC: Path | None = None
        self.OBJECTS: list[dict] = []
        self.RELATIONS: list[tuple[str, str, str]] = []
        self.ARTIFACTS: list[dict] = []
        self._art_by_name: dict[str, str] = {}

    # -- source access -------------------------------------------------------
    def configure(self, src: Path) -> None:
        self.SRC = Path(src)
        if not self.SRC.is_dir():
            raise SystemExit(f"source folder not found: {self.SRC}")

    def mtime(self, name: str) -> str:
        return datetime.fromtimestamp((self.SRC / name).stat().st_mtime, tz=timezone.utc).date().isoformat()

    def read_text(self, name: str) -> str:
        return (self.SRC / name).read_bytes().decode("utf-8")

    def zip_member(self, name: str, member: str) -> bytes:
        with zipfile.ZipFile(self.SRC / name) as z:
            return z.read(member)

    def zip_json(self, name: str, member: str):
        return json.loads(self.zip_member(name, member).decode("utf-8"))

    def sha256(self, name: str) -> str:
        return hashlib.sha256((self.SRC / name).read_bytes()).hexdigest()

    # -- records ---------------------------------------------------------------
    def _check_block(self, oid: str) -> None:
        m = ID_RE.match(oid)
        assert m, oid
        n = int(m.group(1))
        assert self.base < n <= self.base + BLOCK - 1, f"{oid} is outside this line's ID block {self.base + 1}–{self.base + BLOCK - 1}"

    def obj(self, oid, kind, label, label_zh, summary, summary_zh, status, evidence, *,
            created, updated=None, domain=None, domains=None, program="default", version="0.1", **fields):
        self._check_block(oid)
        assert oid.startswith(_PREFIX[kind] + "-"), (oid, kind)
        values = {
            "eml_status": status,
            "eml_evidence_level": evidence,
            "eml_object_version": version,
            "eml_canonical_url": f"{ORIGIN}/ai/{SECTION[kind]}/{oid}/",
            "eml_provenance": self.PROV,
            "eml_visibility": "PUBLIC",
            "eml_publication_policy": "REVIEW_REQUIRED",
            "eml_summary": summary,
            "eml_summary_zh": summary_zh,
            "eml_label_zh": label_zh,
        }
        if domain:
            values["eml_primary_domain"] = domain
        if domains:
            values["eml_domains"] = domains
        prog = self.program if program == "default" else program
        if prog and kind != "program":
            values["eml_program_id"] = prog
        fields.setdefault("eml_authors", list(self.authors))
        fields.setdefault("eml_ai_collaborators", list(self.ai_collaborators))
        for k, v in fields.items():
            if v is not None:
                assert k.startswith("eml_"), k
                values[k] = v
        self.OBJECTS.append({"id": oid, "kind": kind, "label": label, "created_at": created,
                             "updated_at": updated or created, "values": values})
        return oid

    def get(self, oid: str) -> dict:
        return next(o for o in self.OBJECTS if o["id"] == oid)

    def rel(self, src: str, pred: str, tgt: str) -> None:
        self.RELATIONS.append((src, pred, tgt))

    def artifact(self, name: str, *, kind: str, label: str, member: str | None = None,
                 visibility: str = "PUBLIC", policy: str = "REVIEW_REQUIRED", note: str | None = None) -> str:
        key = name if member is None else f"{name}!/{member}"
        if key in self._art_by_name:
            return self._art_by_name[key]
        data = self.zip_member(name, member) if member else (self.SRC / name).read_bytes()
        oid = f"ART-2026-{self.base + len(self.ARTIFACTS) + 1:04d}"
        self._check_block(oid)
        suffix = (member or name).rsplit(".", 1)[-1].lower()
        values = {
            "eml_artifact_type": kind,
            "eml_artifact_uri": f"artifact://evemisslab/{self.slug}/{key}",
            "eml_artifact_sha256": hashlib.sha256(data).hexdigest(),
            "eml_artifact_size": len(data),
            "eml_artifact_media_type": MEDIA.get(suffix, "application/octet-stream"),
            "eml_artifact_provenance": {
                "source": f"EveMissLab research collection: {self.collection}",
                "verification": f"sha256 computed over the file bytes on {self.extracted_at}",
                "note": note or "canonical file; not yet published at a public URL",
            },
            "eml_visibility": visibility,
            "eml_publication_policy": policy,
        }
        self.ARTIFACTS.append({"id": oid, "kind": "artifact", "label": label, "created_at": self.mtime(name),
                               "updated_at": self.mtime(name), "values": values})
        self._art_by_name[key] = oid
        return oid

    def artifact_sha(self, aid: str) -> str:
        return next(a for a in self.ARTIFACTS if a["id"] == aid)["values"]["eml_artifact_sha256"]


_PREFIX = {"research": "RES", "theory": "THY", "experiment": "EXP", "result": "RST", "dataset": "DAT",
           "benchmark": "BEN", "model": "MOD", "program": "PRG", "paper": "PAP", "system": "SYS",
           "claim": "CLM", "observation": "OBS", "evaluation": "EVA"}


# -- writing ---------------------------------------------------------------------
def dump(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_all(parts, out: Path, *, date: str = "2026-09-11") -> None:
    """parts: iterable of (objects, artifacts, relations) in line order. Clears
    content/ai/{objects,relations,artifacts} and writes every line; relation IDs
    are assigned globally in that order."""
    parts = list(parts)
    for sub in ("objects", "relations", "artifacts"):
        folder = out / sub
        if folder.exists():
            for f in folder.glob("*.json"):
                f.unlink()
    ids: set[str] = set()
    n_obj = n_art = 0
    for objects, artifacts, _ in parts:
        for o in objects:
            assert o["id"] not in ids, f"duplicate id across lines: {o['id']}"
            ids.add(o["id"])
            dump(out / "objects" / f'{o["id"]}.json', o)
            n_obj += 1
        for a in artifacts:
            assert a["id"] not in ids, f"duplicate id across lines: {a['id']}"
            ids.add(a["id"])
            dump(out / "artifacts" / f'{a["id"]}.json', a)
            n_art += 1
    seen: set[tuple] = set()
    n = 0
    for _, _, relations in parts:
        for src, pred, tgt in relations:
            assert src in ids, f"relation source missing: {src}"
            assert tgt in ids, f"relation target missing: {tgt}"
            key = (src, pred, tgt)
            if key in seen:
                continue
            seen.add(key)
            n += 1
            rid = f"REL-2026-{n:04d}"
            dump(out / "relations" / f"{rid}.json", {
                "id": rid, "kind": "research_relation", "label": f"{src} {pred} {tgt}",
                "created_at": date, "updated_at": date,
                "values": {
                    "eml_relation_source": src, "eml_relation_predicate": pred, "eml_relation_target": tgt,
                    "eml_relation_status": "ACTIVE",
                    "eml_relation_provenance": {"source": "extracted from the artifacts' own cross-references", "date": date},
                    "eml_visibility": "PUBLIC", "eml_publication_policy": "REVIEW_REQUIRED",
                },
            })
    print(f"objects {n_obj}  artifacts {n_art}  relations {n}  -> {out}")

# Shared helpers for extracting the Adaptive Epistemic Systems research folder
# into content/ai/ records. Data lives in aes_data_*.py; extract.py drives it.
#
# The source folder is private (Neo's research collection); it is passed on the
# command line and never recorded in the output beyond file names and hashes.
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SRC: Path | None = None
OUT = Path(__file__).resolve().parents[2] / "content" / "ai"
ORIGIN = "https://evemisslab.com"
SECTION = {
    "research": "research", "theory": "theory", "experiment": "experiments",
    "dataset": "data", "benchmark": "benchmarks", "result": "results",
    "program": "programs", "paper": "papers", "system": "systems", "model": "models",
}
PROV = {
    "source": "EveMissLab research collection: Adaptive Epistemic Systems (真本體論13)",
    "extracted_by": "Splice (Claude Code), reading the canonical UTF-8 sources and each lab's own result reports",
    "extracted_at": "2026-09-11",
    "generator": "tools/extract_aes/extract.py",
    "claim_boundary": "status, evidence level and result type follow the source artifact's own stated claim boundary; nothing is upgraded beyond what the report supports",
}

OBJECTS: list[dict] = []
RELATIONS: list[tuple[str, str, str]] = []
ARTIFACTS: list[dict] = []
_ART_BY_NAME: dict[str, str] = {}


def configure(src: Path) -> None:
    global SRC
    SRC = Path(src)
    if not SRC.is_dir():
        raise SystemExit(f"source folder not found: {SRC}")


def mtime(name: str) -> str:
    return datetime.fromtimestamp((SRC / name).stat().st_mtime, tz=timezone.utc).date().isoformat()


def read_text(name: str) -> str:
    return (SRC / name).read_bytes().decode("utf-8")


def zip_member(name: str, member: str) -> bytes:
    with zipfile.ZipFile(SRC / name) as z:
        return z.read(member)


def obj(oid, kind, label, label_zh, summary, summary_zh, status, evidence, *,
        created, updated=None, domain=None, domains=None, program="PRG-2026-0001",
        version="0.1", **fields):
    values = {
        "eml_status": status,
        "eml_evidence_level": evidence,
        "eml_object_version": version,
        "eml_canonical_url": f"{ORIGIN}/ai/{SECTION[kind]}/{oid}/",
        "eml_provenance": PROV,
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
    if program and kind != "program":
        values["eml_program_id"] = program
    # Authorship for this line, stated once: Neo.K is the author; the AI
    # collaborator across the series, the labs and AER-0 is Sol (GPT-5.6).
    fields.setdefault("eml_authors", ["Neo.K (EveMissLab)"])
    fields.setdefault("eml_ai_collaborators", ["Sol (GPT-5.6, OpenAI ChatGPT)"])
    for k, v in fields.items():
        if v is not None:
            assert k.startswith("eml_"), k
            values[k] = v
    OBJECTS.append({"id": oid, "kind": kind, "label": label, "created_at": created,
                    "updated_at": updated or created, "values": values})
    return oid


def rel(src: str, pred: str, tgt: str):
    RELATIONS.append((src, pred, tgt))


def artifact(name: str, *, kind: str, label: str, visibility: str = "PUBLIC",
             policy: str = "REVIEW_REQUIRED", note: str | None = None) -> str:
    if name in _ART_BY_NAME:
        return _ART_BY_NAME[name]
    path = SRC / name
    data = path.read_bytes()
    oid = f"ART-2026-{len(ARTIFACTS) + 1:04d}"
    media = {"md": "text/markdown; charset=utf-8", "zip": "application/zip", "json": "application/json"}[path.suffix[1:]]
    values = {
        "eml_artifact_type": kind,
        "eml_artifact_uri": f"artifact://evemisslab/adaptive-epistemic-systems/{name}",
        "eml_artifact_sha256": hashlib.sha256(data).hexdigest(),
        "eml_artifact_size": len(data),
        "eml_artifact_media_type": media,
        "eml_artifact_provenance": {
            "source": "EveMissLab research collection: Adaptive Epistemic Systems",
            "verification": "sha256 computed over the file bytes on 2026-09-11",
            "note": note or "canonical file; not yet published at a public URL",
        },
        "eml_visibility": visibility,
        "eml_publication_policy": policy,
    }
    ARTIFACTS.append({"id": oid, "kind": "artifact", "label": label, "created_at": mtime(name),
                      "updated_at": mtime(name), "values": values})
    _ART_BY_NAME[name] = oid
    return oid


def dump(path: Path, record: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_all():
    for sub in ("objects", "relations", "artifacts"):
        folder = OUT / sub
        if folder.exists():
            for f in folder.glob("*.json"):
                f.unlink()
    ids = {o["id"] for o in OBJECTS} | {a["id"] for a in ARTIFACTS}
    for o in OBJECTS:
        dump(OUT / "objects" / f'{o["id"]}.json', o)
    for a in ARTIFACTS:
        dump(OUT / "artifacts" / f'{a["id"]}.json', a)
    seen = set()
    n = 0
    for src, pred, tgt in RELATIONS:
        assert src in ids, f"relation source missing: {src}"
        assert tgt in ids, f"relation target missing: {tgt}"
        key = (src, pred, tgt)
        if key in seen:
            continue
        seen.add(key)
        n += 1
        rid = f"REL-2026-{n:04d}"
        dump(OUT / "relations" / f"{rid}.json", {
            "id": rid, "kind": "research_relation", "label": f"{src} {pred} {tgt}",
            "created_at": "2026-09-11", "updated_at": "2026-09-11",
            "values": {
                "eml_relation_source": src, "eml_relation_predicate": pred, "eml_relation_target": tgt,
                "eml_relation_status": "ACTIVE",
                "eml_relation_provenance": {"source": "extracted from the artifacts' own cross-references", "date": "2026-09-11"},
                "eml_visibility": "PUBLIC", "eml_publication_policy": "REVIEW_REQUIRED",
            },
        })
    print(f"objects {len(OBJECTS)}  artifacts {len(ARTIFACTS)}  relations {n}  -> {OUT}")

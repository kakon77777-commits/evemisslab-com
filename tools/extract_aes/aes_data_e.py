# The v0.2 bundle's mock smoke file is explicitly MOCK_ONLY_NOT_REAL_MODEL and
# must never be cited as evidence: recorded, but INTERNAL / NEVER_PUBLISH, so the
# gate's private-record path is exercised by real data. It is registered last so
# that it never sits between two public artifacts.
import hashlib

from aes_common import ARTIFACTS, mtime, rel, zip_member

HZ2 = "PACC-Hybrid-Lab_v0.2_REAL_LLM_HARNESS_FINAL.zip"
MEMBER = "PACC-Hybrid-Lab-v0.2/results/pacc_hybrid_v0.2_mock_smoke.json"
data = zip_member(HZ2, MEMBER)
mock_id = f"ART-2026-{len(ARTIFACTS) + 1:04d}"
ARTIFACTS.append({
    "id": mock_id, "kind": "artifact", "label": "PACC-Hybrid v0.2 mock smoke run (MOCK_ONLY_NOT_REAL_MODEL)",
    "created_at": mtime(HZ2), "updated_at": mtime(HZ2),
    "values": {
        "eml_artifact_type": "mock-run-output",
        "eml_artifact_uri": f"artifact://evemisslab/adaptive-epistemic-systems/{HZ2}!/{MEMBER}",
        "eml_artifact_sha256": hashlib.sha256(data).hexdigest(), "eml_artifact_size": len(data),
        "eml_artifact_media_type": "application/json",
        "eml_artifact_provenance": {"source": "PACC-Hybrid-Lab v0.2 bundle", "note": "deterministic fake provider output; the bundle itself forbids using it to claim PACC improvement or degradation on real language models"},
        "eml_visibility": "INTERNAL", "eml_publication_policy": "NEVER_PUBLISH",
    },
})
rel("EXP-2026-0022", "produced", mock_id)

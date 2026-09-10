# Regenerates content/ai/ from the Adaptive Epistemic Systems research folder.
#
#     python tools/extract_aes/extract.py "<path to 自適應世界狀態系統的第一原理框架>"
#
# Every series paper's SHA-256 is asserted against the series' own manifest, and
# every artifact record carries the digest of the file bytes, so the published
# records can be checked against the canonical sources later.
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aes_common as C  # noqa: E402

if len(sys.argv) != 2:
    raise SystemExit(__doc__ or "usage: extract.py <source folder>")
C.configure(Path(sys.argv[1]))

import aes_data_a  # noqa: E402,F401
import aes_data_b  # noqa: E402,F401
import aes_data_c  # noqa: E402,F401
import aes_data_d  # noqa: E402,F401

# The v0.2 bundle's mock smoke file is explicitly MOCK_ONLY_NOT_REAL_MODEL and
# must never be cited as evidence: recorded, but INTERNAL / NEVER_PUBLISH.
HZ2 = "PACC-Hybrid-Lab_v0.2_REAL_LLM_HARNESS_FINAL.zip"
MEMBER = "PACC-Hybrid-Lab-v0.2/results/pacc_hybrid_v0.2_mock_smoke.json"
data = C.zip_member(HZ2, MEMBER)
mock_id = f"ART-2026-{len(C.ARTIFACTS) + 1:04d}"
C.ARTIFACTS.append({
    "id": mock_id, "kind": "artifact", "label": "PACC-Hybrid v0.2 mock smoke run (MOCK_ONLY_NOT_REAL_MODEL)",
    "created_at": C.mtime(HZ2), "updated_at": C.mtime(HZ2),
    "values": {
        "eml_artifact_type": "mock-run-output",
        "eml_artifact_uri": f"artifact://evemisslab/adaptive-epistemic-systems/{HZ2}!/{MEMBER}",
        "eml_artifact_sha256": hashlib.sha256(data).hexdigest(), "eml_artifact_size": len(data),
        "eml_artifact_media_type": "application/json",
        "eml_artifact_provenance": {"source": "PACC-Hybrid-Lab v0.2 bundle", "note": "deterministic fake provider output; the bundle itself forbids using it to claim PACC improvement or degradation on real language models"},
        "eml_visibility": "INTERNAL", "eml_publication_policy": "NEVER_PUBLISH",
    },
})
C.rel("EXP-2026-0022", "produced", mock_id)

C.write_all()

# Regenerates content/ai/ from every research line under Neo's 真本體論13 folder.
#
#     python tools/extract_all.py "<path to 真本體論13>"
#
# Each line's extractor reads its own subfolder, asserts every digest it can
# find against the manifests inside the packages, and appends to its own ID
# block (see tools/extract_lib/ledger.py). Relations are numbered globally in
# the order below. A new line = a new tools/extract_<line>/ package + one entry.
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from extract_lib.ledger import write_all  # noqa: E402

LINES = [
    ("extract_aes", "自適應世界狀態系統的第一原理框架"),
    ("extract_ipm", "智能的物理計量：從最小語意執行到成果品質與計算時空"),
]
if len(sys.argv) != 2:
    raise SystemExit(__doc__ or "usage: extract_all.py <path to 真本體論13>")
root = Path(sys.argv[1])
for pkg, sub in LINES:
    if not (root / sub).is_dir():
        raise SystemExit(f"missing research-line folder: {root / sub}")
    sys.path.insert(0, str(TOOLS / pkg))

# line 1 — Adaptive Epistemic Systems (ID block 0001–0099)
import aes_common as AES  # noqa: E402
AES.configure(root / LINES[0][1])
import aes_data_a, aes_data_b, aes_data_c, aes_data_d, aes_data_e  # noqa: E402,F401

# line 2 — Intelligence Physical Metrology (ID block 0101–0199)
from ipm_common import L as IPM  # noqa: E402
IPM.configure(root / LINES[1][1])
import ipm_data_a, ipm_data_b, ipm_data_c  # noqa: E402,F401

write_all([(AES.OBJECTS, AES.ARTIFACTS, AES.RELATIONS), (IPM.OBJECTS, IPM.ARTIFACTS, IPM.RELATIONS)], AES.OUT)

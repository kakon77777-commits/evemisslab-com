# Regenerates content/ai/ from the Adaptive Epistemic Systems research folder
# ALONE — superseded by tools/extract_all.py, which writes every research line
# together. Running this script drops the other lines' records from content/ai/;
# it is kept for debugging one line in isolation.
#
#     python tools/extract_aes/extract.py "<path to 自適應世界狀態系統的第一原理框架>"
#
# Every series paper's SHA-256 is asserted against the series' own manifest, and
# every artifact record carries the digest of the file bytes, so the published
# records can be checked against the canonical sources later.
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
import aes_data_e  # noqa: E402,F401

print("WARNING: single-line extraction; use tools/extract_all.py to regenerate the whole ledger", file=sys.stderr)
C.write_all()

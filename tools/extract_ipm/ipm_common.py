# The Intelligence Physical Metrology (IPM) line: one Ledger in the 0101–0199 ID
# block. Data lives in ipm_data_*.py; tools/extract_all.py drives it together
# with the other lines. The series is authored "Neo.K with Aletheia（GPT-5.6
# Sol）" on every paper, so that is the default collaborator credit here.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from extract_lib.ledger import Ledger  # noqa: E402

L = Ledger(
    base=100,
    slug="intelligence-physical-metrology",
    collection="Intelligence Physical Metrology (真本體論13)",
    generator="tools/extract_all.py",
    program="PRG-2026-0101",
    authors=["Neo.K (EveMissLab)"],
    ai_collaborators=["Aletheia (GPT-5.6 Sol, OpenAI ChatGPT)"],
)
obj, rel, artifact = L.obj, L.rel, L.artifact

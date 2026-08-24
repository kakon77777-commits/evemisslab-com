import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import content  # noqa: E402

APPROVED_ENTRIES = {
    "en": {
        "host": "apr",
        "name": "APR",
        "tone": "apr",
        "what": "A runtime for deciding when an agent should observe, what it should read, how deeply it should read, when it must reobserve, and when fresh evidence means it should stop reading.",
        "meta": "Research MVP · v0.10",
    },
    "zh": {
        "host": "apr",
        "name": "APR",
        "tone": "apr",
        "what": "一套決定代理何時應觀察、該讀什麼、讀多深、何時必須重看，以及何時因證據仍新鮮而停止閱讀的 Runtime。",
        "meta": "研究型 MVP · v0.10",
    },
}
LIGHT_APR_TONE = "#006b80"
DARK_APR_TONE = "#67d7e7"


def entries(language):
    return [
        site
        for group in content.GROUPS[language]
        for site in group["sites"]
        if site["host"] == "apr"
    ]


def systems_entries(language):
    return [
        site
        for group in content.GROUPS[language]
        if group["key"] == "systems"
        for site in group["sites"]
        if site["host"] == "apr"
    ]


class AprIndexTests(unittest.TestCase):
    def test_both_languages_have_the_exact_apr_entry_in_the_systems_group(self):
        for language in ("en", "zh"):
            with self.subTest(language=language):
                self.assertEqual([APPROVED_ENTRIES[language]], systems_entries(language))
                self.assertEqual([APPROVED_ENTRIES[language]], entries(language))

    def test_rendered_pages_link_to_apr(self):
        subprocess.run([sys.executable, "-B", "build.py"], cwd=ROOT, check=True)
        for relative in ("dist/index.html", "dist/zh/index.html"):
            rendered = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("https://apr.evemisslab.com/", rendered)

    def test_apr_tone_has_one_exact_light_and_two_identical_exact_dark_values(self):
        css = (ROOT / "src/assets/styles.css").read_text(encoding="utf-8")
        values = re.findall(r"--t-apr:\s*(#[0-9a-f]{6});", css)
        self.assertEqual([LIGHT_APR_TONE, DARK_APR_TONE, DARK_APR_TONE], values)
        self.assertEqual(1, values.count(LIGHT_APR_TONE))
        self.assertEqual(2, values.count(DARK_APR_TONE))

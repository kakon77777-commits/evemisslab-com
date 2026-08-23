import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import content  # noqa: E402


def entries(language):
    return [site for group in content.GROUPS[language]
            for site in group["sites"] if site["host"] == "apr"]


class AprIndexTests(unittest.TestCase):
    def test_both_languages_have_one_apr_entry(self):
        self.assertEqual(1, len(entries("en")))
        self.assertEqual(1, len(entries("zh")))
        self.assertEqual("apr", entries("en")[0]["tone"])
        self.assertEqual("apr", entries("zh")[0]["tone"])

    def test_rendered_pages_link_to_apr(self):
        subprocess.run([sys.executable, "-B", "build.py"], cwd=ROOT, check=True)
        for relative in ("dist/index.html", "dist/zh/index.html"):
            rendered = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("https://apr.evemisslab.com/", rendered)

    def test_apr_tone_exists_in_light_and_dark_palettes(self):
        css = (ROOT / "src/assets/styles.css").read_text(encoding="utf-8")
        self.assertEqual(3, css.count("--t-apr:"))
        self.assertRegex(css, r"--t-apr:\s+#[0-9a-f]{6}")

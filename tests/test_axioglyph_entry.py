import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import content  # noqa: E402


def find_entries(language: str):
    return [
        site
        for group in content.GROUPS[language]
        for site in group["sites"]
        if site["host"] == "axioglyph"
    ]


class AxioglyphIndexTests(unittest.TestCase):
    def test_both_languages_have_one_matching_entry(self):
        english = find_entries("en")
        chinese = find_entries("zh")
        self.assertEqual(1, len(english))
        self.assertEqual(1, len(chinese))
        self.assertEqual("axioglyph", english[0]["tone"])
        self.assertEqual("axioglyph", chinese[0]["tone"])
        self.assertIn("passes or fails", english[0]["what"])
        self.assertIn("故意弄錯", chinese[0]["what"])

    def test_rendered_pages_link_to_the_live_child(self):
        subprocess.run([sys.executable, "-B", "build.py"], cwd=ROOT, check=True)
        for relative in ("dist/index.html", "dist/zh/index.html"):
            html = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("https://axioglyph.evemisslab.com/", html)
            self.assertIn("19 sites", html)

    def test_parent_styles_define_the_child_tone(self):
        css = (ROOT / "src/assets/styles.css").read_text(encoding="utf-8")
        self.assertEqual(3, css.count("--t-axioglyph:"))
        self.assertRegex(css, r"--t-axioglyph:\s+#8e4d23")
        self.assertEqual(2, len(re.findall(r"--t-axioglyph:\s+#e8aa6d", css)))


if __name__ == "__main__":
    unittest.main()

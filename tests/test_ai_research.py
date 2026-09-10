import copy
import hashlib
import html
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import ai_research as A  # noqa: E402
import content as C  # noqa: E402

DIST = ROOT / "dist"
CONTENT = ROOT / "content" / "ai"


def build():
    subprocess.run([sys.executable, "-B", "build.py"], cwd=ROOT, check=True)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class HomepageIntegrationTests(unittest.TestCase):
    """Parent spec section 19: the homepage acceptance criteria."""

    @classmethod
    def setUpClass(cls):
        build()
        cls.en = read("dist/index.html")
        cls.zh = read("dist/zh/index.html")

    def test_header_has_the_ai_research_entry(self):
        self.assertIn('class="plate-link" href="/ai/">AI Research</a>', self.en)
        self.assertIn('class="plate-link" href="/zh/ai/">AI 研究</a>', self.zh)

    def test_matrix_has_twelve_cells_to_the_route_map(self):
        for page, base, lang in ((self.en, "/ai/", "en"), (self.zh, "/zh/ai/", "zh")):
            with self.subTest(lang=lang):
                self.assertEqual(12, page.count('class="matrix-cell"'))
                for slug, label in C.AI[lang]["matrix"]:
                    self.assertIn(f'class="matrix-cell" href="{base}{slug}/"><span>{label}</span>', page)

    def test_statement_is_preserved_and_sits_between_the_hero_and_the_index(self):
        for page, lang in ((self.en, "en"), (self.zh, "zh")):
            with self.subTest(lang=lang):
                ch = C.CHROME[lang]
                self.assertIn(ch["display"], page)
                self.assertIn(ch["standfirst"], page)
                matrix = page.index('class="matrix"')
                figure = page.index('class="hero-fig"')
                statement = page.index('class="shell statement"')
                index = page.index('id="index"')
                self.assertLess(matrix, figure)
                self.assertLess(figure, statement)
                self.assertLess(statement, index)
                # the statement heading is no longer inside the hero grid
                self.assertLess(page.index("</figure>"), page.index('class="hero-display"'))

    def test_the_index_is_untouched(self):
        for page in (self.en, self.zh):
            self.assertIn("19 sites", page)
            self.assertEqual(19, page.count('class="card"'))

    def test_archive_spelling_redirects(self):
        redirects = read("dist/_redirects")
        self.assertIn("/ai/archives/* /ai/archive/:splat 301", redirects)
        self.assertIn("/zh/ai/archives/* /zh/ai/archive/:splat 301", redirects)


class PublicationGateTests(unittest.TestCase):
    """The gate fails closed: one bad record and nothing ships."""

    def setUp(self):
        self.policy, self.records = A.load(CONTENT)

    def with_record(self, rec):
        return self.records + [rec]

    @staticmethod
    def record(**over):
        base = {
            "id": "RES-2099-0001", "kind": "research", "label": "Gate fixture",
            "created_at": "2099-01-01", "updated_at": "2099-01-01",
            "values": {"eml_status": "ACTIVE", "eml_evidence_level": "E1", "eml_visibility": "PUBLIC"},
        }
        base.update({k: v for k, v in over.items() if k != "values"})
        if "values" in over:
            base["values"] = {**base["values"], **over["values"]}
        return base

    def test_current_content_passes_the_gate(self):
        projected = A.project(self.policy, self.records)
        self.assertGreater(len(projected["objects"]), 0)

    def test_non_public_records_are_excluded(self):
        projected = A.project(self.policy, self.records)
        shipped = {x["id"] for group in projected.values() for x in group}
        private = [r["id"] for r in self.records if r["values"]["eml_visibility"] != "PUBLIC"]
        self.assertTrue(private, "the fixture needs at least one non-public record")
        for oid in private:
            self.assertNotIn(oid, shipped)

    def test_control_fields_never_reach_the_projection(self):
        projected = A.project(self.policy, self.records)
        for group in projected.values():
            for rec in group:
                self.assertNotIn("eml_visibility", rec["values"])
                self.assertNotIn("eml_publication_policy", rec["values"])

    def test_unknown_visibility_fails_closed(self):
        for vis in ("WHATEVER", "", None):
            with self.subTest(visibility=vis):
                bad = self.record(values={"eml_visibility": vis})
                if vis is None:
                    del bad["values"]["eml_visibility"]
                with self.assertRaises(A.GateError):
                    A.project(self.policy, self.with_record(bad))

    def test_invalid_status_evidence_or_result_type_fails(self):
        for values in ({"eml_status": "DONE"}, {"eml_evidence_level": "E9"}, {"eml_result_type": "GREAT"}):
            with self.subTest(values=values):
                with self.assertRaises(A.GateError):
                    A.project(self.policy, self.with_record(self.record(values=values)))

    def test_id_prefix_must_match_kind(self):
        with self.assertRaises(A.GateError):
            A.project(self.policy, self.with_record(self.record(id="EXP-2099-0001")))

    def test_duplicate_id_fails(self):
        with self.assertRaises(A.GateError):
            A.project(self.policy, self.with_record(copy.deepcopy(self.records[0])))

    def test_canonical_url_must_match_the_route_map(self):
        wrong = self.record(values={"eml_canonical_url": "https://evemisslab.com/ai/research-line/RES-2099-0001/"})
        with self.assertRaises(A.GateError):
            A.project(self.policy, self.with_record(wrong))
        right = self.record(values={"eml_canonical_url": "https://evemisslab.com/ai/research/RES-2099-0001/"})
        A.project(self.policy, self.with_record(right))

    def test_relation_to_a_missing_target_fails(self):
        rel = {
            "id": "REL-2099-0001", "kind": "research_relation", "label": "x",
            "values": {"eml_relation_source": "RES-2026-0001", "eml_relation_predicate": "extends",
                       "eml_relation_target": "RES-2099-9999", "eml_relation_status": "ACTIVE",
                       "eml_visibility": "PUBLIC"},
        }
        with self.assertRaises(A.GateError):
            A.project(self.policy, self.with_record(rel))

    def test_relation_to_a_private_object_is_dropped_not_shipped(self):
        private = self.record(values={"eml_visibility": "INTERNAL"})
        rel = {
            "id": "REL-2099-0001", "kind": "research_relation", "label": "x",
            "values": {"eml_relation_source": "RES-2026-0001", "eml_relation_predicate": "extends",
                       "eml_relation_target": "RES-2099-0001", "eml_relation_status": "ACTIVE",
                       "eml_visibility": "PUBLIC"},
        }
        projected = A.project(self.policy, self.records + [private, rel])
        self.assertNotIn("REL-2099-0001", {r["id"] for r in projected["relations"]})
        self.assertNotIn("RES-2099-0001", {o["id"] for o in projected["objects"]})

    def test_only_allow_listed_fields_are_projected(self):
        rec = self.record(values={"eml_secret_note": "do not publish"})
        projected = A.project(self.policy, self.with_record(rec))
        shipped = next(o for o in projected["objects"] if o["id"] == "RES-2099-0001")
        self.assertNotIn("eml_secret_note", shipped["values"])
        self.assertEqual("ACTIVE", shipped["values"]["eml_status"])


class OutputTests(unittest.TestCase):
    """Site spec sections 33, 46 and 47."""

    @classmethod
    def setUpClass(cls):
        build()
        cls.policy, cls.records = A.load(CONTENT)
        cls.projected = A.project(cls.policy, cls.records)
        cls.objects = cls.projected["objects"]

    def test_ai_home_exists_in_both_languages_with_the_identity(self):
        en = read("dist/ai/index.html")
        zh = read("dist/zh/ai/index.html")
        self.assertIn("AI Research Laboratory", en)
        self.assertIn("AI 研究實驗室", zh)
        self.assertIn('hreflang="zh-Hant" href="https://evemisslab.com/zh/ai/"', en)
        self.assertIn('hreflang="en" href="https://evemisslab.com/ai/"', zh)
        self.assertIn('href="/zh/ai/" hreflang="zh-Hant"', en)  # language switch stays on this page

    def test_hero_stats_come_from_the_data(self):
        en = read("dist/ai/index.html")
        active = {"ACTIVE", "EXPERIMENTAL", "VALIDATING", "REPLICATING"}
        expected = {
            "Active research": sum(1 for o in self.objects if o["kind"] == "research" and o["values"]["eml_status"] in active),
            "Active experiments": sum(1 for o in self.objects if o["kind"] == "experiment" and o["values"]["eml_status"] in active),
            "Datasets": sum(1 for o in self.objects if o["kind"] == "dataset"),
            "Benchmarks": sum(1 for o in self.objects if o["kind"] == "benchmark"),
            "Programs": sum(1 for o in self.objects if o["kind"] == "program"),
        }
        for label, n in expected.items():
            self.assertIn(f"<dt>{label}</dt><dd>{n}</dd>", en)

    def test_every_public_object_has_html_in_both_languages_and_a_json_twin(self):
        for o in self.objects:
            path = A.object_path(o["kind"], o["id"]).strip("/")
            with self.subTest(id=o["id"]):
                self.assertTrue((DIST / path / "index.html").is_file())
                self.assertTrue((DIST / "zh" / path / "index.html").is_file())
                twin = json.loads((DIST / path / "index.json").read_text(encoding="utf-8"))
                self.assertEqual(o["id"], twin["id"])
                self.assertEqual(A.canonical_url(o["kind"], o["id"]), twin["canonical_url"])
                self.assertNotIn("eml_visibility", twin["values"])

    def test_status_and_evidence_are_shown_as_separate_labels(self):
        exp = next(o for o in self.objects if o["kind"] == "experiment")
        page = read(f'dist/ai/experiments/{exp["id"]}/index.html')
        self.assertIn("<dt>Research status</dt>", page)
        self.assertIn("<dt>Evidence level</dt>", page)
        self.assertIn(f'<span class="badge">{exp["values"]["eml_status"]}</span>', page)
        self.assertIn(f'<span class="badge">{exp["values"]["eml_evidence_level"]}</span>', page)

    def test_every_measurement_object_states_its_data_basis(self):
        allowed = set(C.AI["en"]["data_basis"])
        for o in self.objects:
            if o["kind"] in ("experiment", "result", "dataset", "model", "theory", "paper"):
                with self.subTest(id=o["id"]):
                    self.assertIn(o["values"].get("eml_data_basis"), allowed)
        page = read("dist/ai/experiments/index.html")
        self.assertIn('<span class="badge">SYNTHETIC</span>', page)

    def test_result_type_is_visible_including_non_positive_ones(self):
        results = read("dist/ai/results/index.html")
        types = {o["values"].get("eml_result_type") for o in self.objects if o["kind"] == "result"}
        self.assertTrue(types & {"NEGATIVE", "MIXED", "INCONCLUSIVE"}, "the batch must carry non-positive results")
        for rtype in types:
            self.assertIn(f'<span class="badge">{rtype}</span>', results)

    def test_no_non_public_record_leaks_into_the_output(self):
        private = [r["id"] for r in self.records if r["values"]["eml_visibility"] != "PUBLIC"]
        self.assertTrue(private)
        for path in DIST.rglob("*"):
            if path.suffix in (".html", ".json", ".xml", ".txt", ".sha256"):
                text = path.read_text(encoding="utf-8")
                for oid in private:
                    self.assertNotIn(oid, text, f"{oid} leaked into {path}")

    def test_every_json_file_is_valid_utf8_json(self):
        files = list((DIST / "ai").rglob("*.json"))
        self.assertGreater(len(files), 20)
        for path in files:
            with self.subTest(path=str(path.relative_to(DIST))):
                json.loads(path.read_bytes().decode("utf-8"))

    def test_index_json_map_points_at_files_that_exist(self):
        index = json.loads(read("dist/ai/index.json"))
        self.assertEqual("EveMissLab AI Research Laboratory", index["site"])
        for key in ("research", "experiments", "datasets", "benchmarks", "results",
                    "programs", "papers", "systems", "models", "archive", "graph", "relations"):
            with self.subTest(key=key):
                self.assertTrue((DIST / index[key].lstrip("/")).is_file(), index[key])
        self.assertEqual(len(self.objects), sum(index["counts"][k] for k in A.RESEARCH_KINDS))

    def test_graph_edges_reference_graph_nodes(self):
        graph = json.loads(read("dist/ai/graph/research-graph.json"))
        nodes = {n["id"] for n in graph["nodes"]}
        self.assertEqual(len(self.projected["relations"]), len(graph["edges"]))
        for edge in graph["edges"]:
            self.assertIn(edge["source"], nodes)
            self.assertIn(edge["target"], nodes)

    def test_manifest_matches_the_json_files(self):
        lines = read("dist/ai/MANIFEST.sha256").splitlines()
        listed = {}
        for line in lines:
            digest, name = line.split("  ", 1)
            listed[name] = digest
        on_disk = {p.relative_to(DIST).as_posix() for p in (DIST / "ai").rglob("*.json")}
        self.assertEqual(on_disk, set(listed))
        for name, digest in listed.items():
            self.assertEqual(digest, hashlib.sha256((DIST / name).read_bytes()).hexdigest())

    def test_internal_links_resolve(self):
        href = re.compile(r'href="(/[^"#?]*)')
        missing = set()
        for page in DIST.rglob("*.html"):
            for target in href.findall(page.read_text(encoding="utf-8")):
                if target.startswith("//"):
                    continue
                candidate = DIST / target.lstrip("/")
                if target.endswith("/"):
                    candidate = candidate / "index.html"
                if not candidate.is_file():
                    missing.add(target)
        self.assertEqual(set(), missing)

    def test_sitemap_lists_ai_pages_with_alternates(self):
        sitemap = read("dist/sitemap.xml")
        self.assertIn("<loc>https://evemisslab.com/ai/</loc>", sitemap)
        self.assertIn("<loc>https://evemisslab.com/zh/ai/</loc>", sitemap)
        self.assertIn("<loc>https://evemisslab.com/ai/experiments/EXP-2026-0001/</loc>", sitemap)
        self.assertIn('hreflang="zh-Hant" href="https://evemisslab.com/zh/ai/experiments/EXP-2026-0001/"', sitemap)
        self.assertNotIn("404", sitemap)

    def test_chinese_pages_use_zh_titles_and_mark_english_fallback(self):
        for o in self.objects:
            path = A.object_path(o["kind"], o["id"], "zh").strip("/")
            page = (DIST / path / "index.html").read_text(encoding="utf-8")
            with self.subTest(id=o["id"]):
                self.assertIn('<html lang="zh-Hant">', page)
                if o["values"].get("eml_label_zh"):
                    self.assertIn(f'<h1 class="pg-title">{html.escape(o["values"]["eml_label_zh"])}</h1>', page)
                else:
                    self.assertIn('class="pg-title" lang="en">', page)

    def test_archive_and_domain_views_exist_even_when_empty(self):
        for section in ("archive", "memory", "computation", "theory", "claims"):
            with self.subTest(section=section):
                if section == "claims":
                    # no claim records yet: no page, and no dangling nav link either
                    self.assertFalse((DIST / "ai" / "claims").exists())
                    continue
                self.assertTrue((DIST / "ai" / section / "index.html").is_file())
                self.assertTrue((DIST / "ai" / section / "index.json").is_file())


if __name__ == "__main__":
    unittest.main()

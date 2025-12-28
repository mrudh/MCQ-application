import io
import os
import json
import types
import shutil
import tempfile
import unittest
import importlib.util
from contextlib import redirect_stdout


def find_project_root(start_dir: str) -> str:
    cur = os.path.abspath(start_dir)
    while True:
        candidate = os.path.join(cur, "answer_links.py")
        if os.path.exists(candidate):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError("Could not find answer_links.py by walking up from tests folder.")
        cur = parent


def import_module_under_test(project_root: str):
    dummy_quiz_data = types.ModuleType("quiz_data")
    dummy_quiz_data.ALL_QUIZ_DATA = [
        {
            "question": "Dummy MCQ?",
            "options": ["A. Option A", "B. Option B", "C. Option C", "D. Option D"],
            "answer": "A",
        }
    ]
    dummy_quiz_data.FILL_IN_QUIZ_DATA = [
        {"question": "Dummy Fill?", "answer": "alpha|beta"}
    ]

    import sys
    sys.modules["quiz_data"] = dummy_quiz_data
    module_path = os.path.join(project_root, "answer_links.py")
    spec = importlib.util.spec_from_file_location("answer_links_under_test", module_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


class TestAnswerReferenceLinks(unittest.TestCase):
    def setUp(self):
        self.project_root = find_project_root(os.path.dirname(__file__))
        self.m = import_module_under_test(self.project_root)
        self.tmpdir = tempfile.mkdtemp()
        self.links_path = os.path.join(self.tmpdir, "answer_links.json")
        self.m.LINKS_FILE = self.links_path
        self.m.DEFAULT_MCQ_LINKS = {}
        self.m.DEFAULT_FILL_LINKS = {}

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def write_links_dict(self, d: dict):
        with open(self.links_path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

    def write_invalid_json(self):
        with open(self.links_path, "w", encoding="utf-8") as f:
            f.write("{")  # invalid JSON

    def menu_like_add_mcq(self, idx: int, link: str):
        if link.strip():
            self.m.add_link_for_mcq(idx, link.strip())

    def menu_like_add_fill(self, idx: int, link: str):
        if link.strip():
            self.m.add_link_for_fill(idx, link.strip())

    def test_01_load_file_missing_returns_empty_dict(self):
        if os.path.exists(self.links_path):
            os.remove(self.links_path)
        self.assertEqual({}, self.m._load_links())

    def test_02_load_invalid_json_returns_empty_dict(self):
        self.write_invalid_json()
        self.assertEqual({}, self.m._load_links())

    def test_03_load_valid_json_returns_dict(self):
        self.write_links_dict({"MCQ-1": ["u1"]})
        self.assertEqual({"MCQ-1": ["u1"]}, self.m._load_links())

    def test_04_save_writes_json_file(self):
        data = {"MCQ-1": ["u1", "u2"]}
        self.m._save_links(data)
        self.assertTrue(os.path.exists(self.links_path))
        with open(self.links_path, "r", encoding="utf-8") as f:
            self.assertEqual(data, json.load(f))

    def test_05_get_mcq_defaults_only(self):
        self.m.DEFAULT_MCQ_LINKS = {1: ["d1"]}
        self.assertEqual(["d1"], self.m.get_links_for_mcq(1))

    def test_06_get_mcq_no_links(self):
        self.m.DEFAULT_MCQ_LINKS = {1: []}
        self.assertEqual([], self.m.get_links_for_mcq(1))

    def test_07_get_mcq_merged_defaults_and_user(self):
        self.m.DEFAULT_MCQ_LINKS = {1: ["d1"]}
        self.write_links_dict({"MCQ-1": ["u1", "d1"]})  
        self.assertEqual(["d1", "u1"], self.m.get_links_for_mcq(1))

    def test_08_get_fill_defaults_only(self):
        self.m.DEFAULT_FILL_LINKS = {1: ["fd1"]}
        self.assertEqual(["fd1"], self.m.get_links_for_fill(1))

    def test_09_get_fill_no_links(self):
        self.m.DEFAULT_FILL_LINKS = {1: []}
        self.assertEqual([], self.m.get_links_for_fill(1))

    def test_10_get_fill_merged_defaults_and_user(self):
        self.m.DEFAULT_FILL_LINKS = {1: ["fd1"]}
        self.write_links_dict({"FILL-1": ["fu1", "fd1"]})
        self.assertEqual(["fd1", "fu1"], self.m.get_links_for_fill(1))

    def test_11_add_mcq_empty_link_no_change_via_menu(self):
        self.menu_like_add_mcq(1, "") 
        self.assertEqual({}, self.m._load_links())

    def test_12_add_mcq_duplicate_no_change(self):
        self.m.add_link_for_mcq(1, "u1")
        self.m.add_link_for_mcq(1, "u1")  
        self.assertEqual(["u1"], self.m._load_links().get("MCQ-1"))

    def test_13_add_mcq_new_link_appends_and_saves(self):
        self.m.add_link_for_mcq(1, "u1")
        self.m.add_link_for_mcq(1, "u2")
        self.assertEqual(["u1", "u2"], self.m._load_links().get("MCQ-1"))

    def test_14_add_fill_empty_link_no_change_via_menu(self):
        self.menu_like_add_fill(1, "")
        self.assertEqual({}, self.m._load_links())

    def test_15_add_fill_duplicate_no_change(self):
        self.m.add_link_for_fill(1, "fu1")
        self.m.add_link_for_fill(1, "fu1")
        self.assertEqual(["fu1"], self.m._load_links().get("FILL-1"))

    def test_16_add_fill_new_link_appends_and_saves(self):
        self.m.add_link_for_fill(1, "fu1")
        self.m.add_link_for_fill(1, "fu2")
        self.assertEqual(["fu1", "fu2"], self.m._load_links().get("FILL-1"))

    def test_17_show_mcq_invalid_index_message(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.m.show_mcq_with_links(999)
        out = f.getvalue()
        self.assertIn("Invalid MCQ number.", out)

    def test_18_show_mcq_prints_answer_and_links(self):
        self.m.DEFAULT_MCQ_LINKS = {1: ["d1"]}
        self.write_links_dict({"MCQ-1": ["u1"]})

        f = io.StringIO()
        with redirect_stdout(f):
            self.m.show_mcq_with_links(1)
        out = f.getvalue()

        self.assertIn("===== MCQ ANSWER & LINKS =====", out)
        self.assertIn("Q1. Dummy MCQ?", out)
        self.assertIn("Correct answer:", out)
        self.assertIn("d1", out)
        self.assertIn("u1", out)

    def test_19_show_fill_invalid_index_message(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.m.show_fill_with_links(999)
        out = f.getvalue()
        self.assertIn("Invalid fill-in question number.", out)

    def test_20_show_fill_prints_answer_and_links(self):
        self.m.DEFAULT_FILL_LINKS = {1: ["fd1"]}
        self.write_links_dict({"FILL-1": ["fu1"]})

        f = io.StringIO()
        with redirect_stdout(f):
            self.m.show_fill_with_links(1)
        out = f.getvalue()

        self.assertIn("===== FILL-IN ANSWER & LINKS =====", out)
        self.assertIn("Q1. Dummy Fill?", out)
        self.assertIn("Accepted answer(s): alpha / beta", out)
        self.assertIn("fd1", out)
        self.assertIn("fu1", out)


if __name__ == "__main__":
    unittest.main()

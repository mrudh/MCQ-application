

import os
import sys
import io
import unittest
import importlib
from contextlib import redirect_stdout
from unittest.mock import patch




POSSIBLE_MODULES = [

    "mcq",
    "main",
    "answer_links",
    "answers_viewer",
    "storage",
    "assessment_storage",
    "assessment",
]

POSSIBLE_FUNC_NAMES = [
    "_show_user_links_for_mcq",  
    "show_user_links_for_mcq",   
]


def _import_project_module():
    here = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    last_err = None
    for mod_name in POSSIBLE_MODULES:
        try:
            mod = importlib.import_module(mod_name)
            for fn_name in POSSIBLE_FUNC_NAMES:
                if hasattr(mod, fn_name):
                    return mod, fn_name
        except Exception as e:
            last_err = e

    raise ImportError(
        "Could not find _show_user_links_for_mcq in any expected module.\n"
        f"Tried modules: {POSSIBLE_MODULES}\n"
        f"Tried names: {POSSIBLE_FUNC_NAMES}\n"
        f"Last error: {last_err}"
    )




class TestShowUserLinksForMCQ_FromTSLFrames(unittest.TestCase):
   

    def setUp(self):
        self.mod, self.fn_name = _import_project_module()
        self.fn = getattr(self.mod, self.fn_name)

    def _run_case(self, *, index_value, links_list):
        fake_key = "mcq_key"
        fake_links_data = {fake_key: links_list}
        with patch.object(self.mod, "_load_links", return_value=fake_links_data), \
             patch.object(self.mod, "_key_for_mcq", return_value=fake_key):
            buf = io.StringIO()
            with redirect_stdout(buf):
                result = self.fn(index_value)
            output = buf.getvalue()
        return result, output
    
    def _links_zero(self): return []
    def _links_one(self):  return ["http://x1.com"]
    def _links_two(self):  return ["http://x1.com", "http://x2.com"]
    def _links_many(self): return [f"http://x{i}.com" for i in range(1, 6)]
    def _links_special(self): return ["http://example.com?q=@#", "weird text link @@##", "spaced link  "]

    def test_case_1_key_1_1_1(self):
        result, out = self._run_case(index_value=1, links_list=self._links_zero())
        self.assertEqual([], result)
        self.assertIn("No user-added links stored for this MCQ yet.", out)

    def test_case_2_key_1_1_2(self):
        result, out = self._run_case(index_value=1, links_list=self._links_one())
        self.assertEqual(self._links_one(), result)
        self.assertIn("User-added link(s) for this MCQ:", out)
        self.assertIn("1. http://x1.com", out)

    def test_case_3_key_1_1_3(self):
        result, out = self._run_case(index_value=1, links_list=self._links_two())
        self.assertEqual(self._links_two(), result)
        self.assertIn("User-added link(s) for this MCQ:", out)
        self.assertIn("2. http://x2.com", out)

    def test_case_4_key_1_1_4(self):
        links = self._links_many()
        result, out = self._run_case(index_value=1, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("5. http://x5.com", out)

    def test_case_5_key_1_1_5(self):
        links = self._links_special()
        result, out = self._run_case(index_value=1, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("weird text link @@##", out)

    def test_case_6_key_1_2_1(self):
        result, out = self._run_case(index_value=1, links_list=self._links_zero())
        self.assertEqual([], result)
        self.assertIn("No user-added links stored for this MCQ yet.", out)

    def test_case_7_key_1_2_2(self):
        links = self._links_one()
        result, out = self._run_case(index_value=1, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("1. http://x1.com", out)

    def test_case_8_key_1_2_3(self):
        links = self._links_two()
        result, out = self._run_case(index_value=1, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("2. http://x2.com", out)

    def test_case_9_key_1_2_4(self):
        links = self._links_many()
        result, out = self._run_case(index_value=1, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("5. http://x5.com", out)

    def test_case_10_key_1_2_5(self):
        links = self._links_special()
        result, out = self._run_case(index_value=1, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("spaced link", out)

    def test_case_11_key_2_1_1(self):
        result, out = self._run_case(index_value=-999, links_list=self._links_zero())
        self.assertEqual([], result)
        self.assertIn("No user-added links stored for this MCQ yet.", out)

    def test_case_12_key_2_1_2(self):
        links = self._links_one()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("1. http://x1.com", out)

    def test_case_13_key_2_1_3(self):
        links = self._links_two()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("2. http://x2.com", out)

    def test_case_14_key_2_1_4(self):
        links = self._links_many()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("5. http://x5.com", out)

    def test_case_15_key_2_1_5(self):
        links = self._links_special()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("weird text link @@##", out)

    def test_case_16_key_2_2_1(self):
        result, out = self._run_case(index_value=-999, links_list=self._links_zero())
        self.assertEqual([], result)
        self.assertIn("No user-added links stored for this MCQ yet.", out)

    def test_case_17_key_2_2_2(self):
        links = self._links_one()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("1. http://x1.com", out)

    def test_case_18_key_2_2_3(self):
        links = self._links_two()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("2. http://x2.com", out)

    def test_case_19_key_2_2_4(self):
        links = self._links_many()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("5. http://x5.com", out)

    def test_case_20_key_2_2_5(self):
        links = self._links_special()
        result, out = self._run_case(index_value=-999, links_list=links)
        self.assertEqual(links, result)
        self.assertIn("spaced link", out)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest
import importlib
from unittest.mock import patch


CANDIDATE_MODULES = [
    "answer_links",
    "mcq",
    "main",
]


def _ensure_project_root_on_path():
    here = os.path.abspath(os.path.dirname(__file__))

    cur = here
    for _ in range(15):
        if os.path.exists(os.path.join(cur, "answer_links.py")) or os.path.exists(os.path.join(cur, "mcq.py")):
            if cur not in sys.path:
                sys.path.insert(0, cur)
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent

    
    fallback = os.path.abspath(os.path.join(here, "../../../../../.."))
    if fallback not in sys.path:
        sys.path.insert(0, fallback)
    return fallback


def _find_module_with_function(func_name: str):
    _ensure_project_root_on_path()

    for mod_name in CANDIDATE_MODULES:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        if hasattr(mod, func_name):
            return mod_name, mod

    raise ImportError(
        f"Could not find function '{func_name}' in any of: {CANDIDATE_MODULES}. "
        "Check where delete_link_for_mcq is defined and add that module name to CANDIDATE_MODULES."
    )


class TestDeleteLinkForMCQ_FromTSLFrames(unittest.TestCase):
   

    def setUp(self):
        self.module_name, mod = _find_module_with_function("delete_link_for_mcq")
        self.fn = getattr(mod, "delete_link_for_mcq")

        self.p_load = patch(f"{self.module_name}._load_links")
        self.p_save = patch(f"{self.module_name}._save_links")
        self.p_key = patch(f"{self.module_name}._key_for_mcq")

        self.mock_load = self.p_load.start()
        self.mock_save = self.p_save.start()
        self.mock_key = self.p_key.start()

        self.addCleanup(self.p_load.stop)
        self.addCleanup(self.p_save.stop)
        self.addCleanup(self.p_key.stop)
        self.mock_key.return_value = "mcq_1"

   
    def _set_no_links(self):
        self.mock_load.return_value = {}

    def _set_has_links(self, links=None):
        if links is None:
            links = ["http://a.com", "http://b.com"]
        self.mock_load.return_value = {"mcq_1": list(links)}


    def _assert_fail_no_links(self, result):
        ok, msg = result
        self.assertFalse(ok)
        self.assertIn("No user-added links", msg)
        self.mock_save.assert_not_called()

    def _assert_fail_bad_pos(self, result, expected_len):
        ok, msg = result
        self.assertFalse(ok)
        self.assertIn("Invalid number", msg)
        self.assertIn(str(expected_len), msg)
        self.mock_save.assert_not_called()

    def _assert_success_deleted(self, result):
        ok, msg = result
        self.assertTrue(ok)
        self.assertIn("Deleted:", msg)
        self.mock_save.assert_called_once()

    def _assert_fail_not_found(self, result):
        ok, msg = result
        self.assertFalse(ok)
        self.assertIn("not found", msg.lower())
        self.mock_save.assert_not_called()


    def test_case_1_key_1_1_1(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, 1))

    def test_case_2_key_1_1_2(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, 99))

    def test_case_3_key_1_1_3(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, 1))

    def test_case_4_key_1_1_4(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, 1))

    def test_case_5_key_1_1_5(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, 1))

    def test_case_6_key_1_2_1(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, "http://a.com"))

    def test_case_7_key_1_2_2(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, "anything"))

    def test_case_8_key_1_2_3(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, "anything"))

    def test_case_9_key_1_2_4(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, "http://a.com"))

    def test_case_10_key_1_2_5(self):
        self._set_no_links()
        self._assert_fail_no_links(self.fn(1, "http://missing.com"))

    def test_case_11_key_2_1_1(self):
        self._set_has_links()
        self._assert_fail_bad_pos(self.fn(1, 99), expected_len=2)

    def test_case_12_key_2_1_2(self):
        self._set_has_links()
        self._assert_fail_bad_pos(self.fn(1, 99), expected_len=2)

    def test_case_13_key_2_1_3(self):
        self._set_has_links()
        self._assert_success_deleted(self.fn(1, 1))

    def test_case_14_key_2_1_4(self):
        self._set_has_links()
        self._assert_success_deleted(self.fn(1, 1))

    def test_case_15_key_2_1_5(self):
        self._set_has_links()
        self._assert_fail_bad_pos(self.fn(1, 99), expected_len=2)

    def test_case_16_key_2_2_1(self):
        self._set_has_links()
        self._assert_fail_not_found(self.fn(1, "http://missing.com"))

    def test_case_17_key_2_2_2(self):
        self._set_has_links()
        self._assert_fail_not_found(self.fn(1, "http://missing.com"))

    def test_case_18_key_2_2_3(self):
        self._set_has_links()
        self._assert_success_deleted(self.fn(1, "http://a.com"))

    def test_case_19_key_2_2_4(self):
        self._set_has_links()
        self._assert_success_deleted(self.fn(1, "http://a.com"))

    def test_case_20_key_2_2_5(self):
        self._set_has_links()
        self._assert_fail_not_found(self.fn(1, "http://missing.com"))


if __name__ == "__main__":
    unittest.main()

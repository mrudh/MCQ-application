import os
import sys
import unittest
import importlib
from unittest.mock import patch, MagicMock



MODULE_CANDIDATES = [
    "attempt_comparison",   
    "comparison",           
    "main",
    "mcq",
]


def _ensure_project_root_on_syspath():
    here = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "..", "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def _import_target_module():
    _ensure_project_root_on_syspath()

    last_err = None
    for name in MODULE_CANDIDATES:
        try:
            mod = importlib.import_module(name)
        except Exception as e:
            last_err = e
            continue

        if hasattr(mod, "get_all_users") and hasattr(mod, "choose_user_from_list_and_compare"):
            return mod

    raise ImportError(
        "Could not find a module that defines BOTH get_all_users() and choose_user_from_list_and_compare().\n"
        f"Tried: {MODULE_CANDIDATES}\n"
        "Fix: add your real python filename (without .py) into MODULE_CANDIDATES."
        + (f"\nLast import error seen: {last_err}" if last_err else "")
    )


class TestChooseUserFromListAndCompare_FromTSLFrames(unittest.TestCase):


    def setUp(self):
        self.mod = _import_target_module()
        self.get_all_users = getattr(self.mod, "get_all_users")
        self.choose = getattr(self.mod, "choose_user_from_list_and_compare")

    def _scores_from_names(self, names):
        return [{"name": n} for n in names]

    def _run_choose(self, scores_names, normalize_map=None, user_input="1"):
        
        scores = self._scores_from_names(scores_names)

        def default_norm(x):
            return (x or "").strip().lower()

        def norm_side_effect(x):
            if normalize_map is None:
                return default_norm(x)
           
            sx = (x or "").strip()
            return normalize_map.get(x, normalize_map.get(sx, default_norm(x)))

        with patch.object(self.mod, "load_scores", return_value=scores), \
             patch.object(self.mod, "_normalize_name", side_effect=norm_side_effect), \
             patch.object(self.mod, "show_first_and_latest_attempt") as show_mock, \
             patch("builtins.input", return_value=user_input), \
             patch("builtins.print") as print_mock:

            self.choose()

        printed = "\n".join(" ".join(map(str, c.args)) for c in print_mock.call_args_list)
        return printed, show_mock.call_args_list

    def test_case_01_key_1_no_attempts_users_empty_prints_no_attempts(self):
        out, calls = self._run_choose(scores_names=[], user_input="1")
        self.assertIn("No quiz attempts stored yet.", out)
        self.assertEqual([], calls)

    def test_case_02_key_2_no_attempts_returns(self):
        out, calls = self._run_choose(scores_names=[], user_input="0")
        self.assertIn("No quiz attempts stored yet.", out)
        self.assertEqual([], calls)

    def test_case_03_key_3_non_numeric_input_prints_invalid_input(self):
        out, calls = self._run_choose(scores_names=["Alex"], user_input="abc")
        self.assertIn("Invalid input. Please enter a number.", out)
        self.assertEqual([], calls)

    def test_case_04_key_4_non_numeric_includes_please_enter_number(self):
        out, _ = self._run_choose(scores_names=["Alex"], user_input="xyz")
        self.assertIn("Please enter a number", out)

    def test_case_05_key_5_non_numeric_returns(self):
        out, calls = self._run_choose(scores_names=["Alex"], user_input="nope")
        self.assertIn("Invalid input. Please enter a number.", out)
        self.assertEqual([], calls)

    def test_case_06_key_6_input_zero_prints_cancelled(self):
        out, calls = self._run_choose(scores_names=["Alex"], user_input="0")
        self.assertIn("Cancelled.", out)
        self.assertEqual([], calls)

    def test_case_07_key_7_input_zero_returns(self):
        out, calls = self._run_choose(scores_names=["Alex"], user_input="0")
        self.assertIn("Cancelled.", out)
        self.assertEqual([], calls)

    def test_case_08_key_8_one_user_choose_1_calls_show(self):
        out, calls = self._run_choose(scores_names=["Alex"], user_input="1")
        self.assertIn("USERS WITH QUIZ ATTEMPTS", out)
        self.assertEqual(1, len(calls))
        self.assertEqual(("Alex",), calls[0].args)

    def test_case_09_key_9_two_users_choose_1_calls_first(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob"], user_input="1")
        self.assertIn("1. Alex", out)
        self.assertIn("2. Bob", out)
        self.assertEqual(("Alex",), calls[0].args)

    def test_case_10_key_10_two_users_choose_2_calls_second(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob"], user_input="2")
        self.assertEqual(("Bob",), calls[0].args)

    def test_case_11_key_11_three_users_choose_1_calls_first(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob", "Cara"], user_input="1")
        self.assertEqual(("Alex",), calls[0].args)

    def test_case_12_key_12_three_users_choose_2_calls_middle(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob", "Cara"], user_input="2")
        self.assertEqual(("Bob",), calls[0].args)

    def test_case_13_key_13_three_users_choose_3_calls_last(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob", "Cara"], user_input="3")
        self.assertEqual(("Cara",), calls[0].args)

    
    def test_case_14_key_14_three_users_input_minus_one_invalid_selection(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob", "Cara"], user_input="-1")
        self.assertIn("Invalid selection.", out)
        self.assertEqual([], calls)

    def test_case_15_key_15_three_users_input_minus_one_returns(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob", "Cara"], user_input="-1")
        self.assertIn("Invalid selection.", out)
        self.assertEqual([], calls)

    def test_case_16_key_16_three_users_input_four_invalid_selection(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob", "Cara"], user_input="4")
        self.assertIn("Invalid selection.", out)
        self.assertEqual([], calls)

    def test_case_17_key_17_three_users_input_four_returns(self):
        out, calls = self._run_choose(scores_names=["Alex", "Bob", "Cara"], user_input="4")
        self.assertIn("Invalid selection.", out)
        self.assertEqual([], calls)


    def test_case_18_key_18_blank_names_only_prints_no_attempts(self):
        out, calls = self._run_choose(scores_names=["", "   ", None, "\n\t"], user_input="1")
        self.assertIn("No quiz attempts stored yet.", out)
        self.assertEqual([], calls)

    
    def test_case_19_key_19_duplicate_names_different_casing_collapses_to_one(self):
        out, calls = self._run_choose(scores_names=["Alex", " alex ", "ALEX"], user_input="1")
        self.assertIn("1. Alex", out)
        self.assertNotIn("2.", out)
        self.assertEqual(("Alex",), calls[0].args)

    def test_case_20_key_20_duplicate_names_fragment_continuation(self):
        out, calls = self._run_choose(scores_names=["Alex", " alex ", "ALEX"], user_input="1")
        self.assertEqual(1, len(calls))

    def test_case_21_key_21_duplicates_normalized_to_one_user(self):
        norm = {"Alex": "alex", " alex ": "alex", "ALEX": "alex"}
        out, calls = self._run_choose(scores_names=["Alex", " alex ", "ALEX"], normalize_map=norm, user_input="1")
        self.assertNotIn("2.", out)
        self.assertEqual(("Alex",), calls[0].args)

    def test_case_22_key_22_duplicates_mixed_with_blanks_results_one_user(self):
        out, calls = self._run_choose(scores_names=["", "Alex", "   ", " alex ", None], user_input="1")
        self.assertIn("1. Alex", out)
        self.assertNotIn("2.", out)
        self.assertEqual(("Alex",), calls[0].args)


    def test_case_23_key_23_many_users_choose_1_calls_first(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="1")
        self.assertEqual(("U1",), calls[0].args)

    def test_case_24_key_24_many_users_fragment_continuation(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="1")
        self.assertIn("5. U5", out)

    def test_case_25_key_25_many_users_choose_1_calls_show(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="1")
        self.assertEqual(1, len(calls))

    def test_case_26_key_26_many_users_choose_5_calls_last(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="5")
        self.assertEqual(("U5",), calls[0].args)

    def test_case_27_key_27_many_users_fragment_continuation(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, _ = self._run_choose(scores_names=names, user_input="5")
        self.assertIn("0. Cancel", out)

    def test_case_28_key_28_many_users_choose_5_calls_show(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="5")
        self.assertEqual(1, len(calls))

    def test_case_29_key_29_many_users_choose_6_invalid_selection(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="6")
        self.assertIn("Invalid selection.", out)
        self.assertEqual([], calls)

    def test_case_30_key_30_many_users_fragment_continuation(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="6")
        self.assertEqual([], calls)

    def test_case_31_key_31_many_users_choose_6_returns(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="6")
        self.assertIn("Invalid selection.", out)
        self.assertEqual([], calls)

    def test_case_32_key_32_many_users_choose_6_returns_cont(self):
        names = ["U1", "U2", "U3", "U4", "U5"]
        out, calls = self._run_choose(scores_names=names, user_input="6")
        self.assertEqual([], calls)

   
    def test_case_33_key_33_special_char_names_treated_valid(self):
        out, calls = self._run_choose(scores_names=["@#", "weird  name"], user_input="1")
        self.assertIn("1. @#", out)
        self.assertEqual(("@#",), calls[0].args)

    def test_case_34_key_34_special_names_fragment_continuation(self):
        out, _ = self._run_choose(scores_names=["@#", "weird  name"], user_input="2")
        self.assertIn("2. weird  name", out)

    def test_case_35_key_35_weird_name_non_empty_after_strip_valid(self):
        out, calls = self._run_choose(scores_names=["   weird  name   "], user_input="1")
        self.assertIn("1. weird  name", out)
        self.assertEqual(("weird  name",), calls[0].args)

    def test_case_36_key_36_leading_trailing_whitespace_valid_name(self):
        out, calls = self._run_choose(scores_names=["   Alex   "], user_input="1")
        self.assertIn("1. Alex", out)
        self.assertEqual(("Alex",), calls[0].args)

    
    def test_case_37_key_37_all_names_normalize_same_key_length_one(self):
        norm = {"A1": "same", "A2": "same", "A3": "same"}
        out, calls = self._run_choose(scores_names=["A1", "A2", "A3"], normalize_map=norm, user_input="1")
        self.assertIn("1. A1", out)
        self.assertNotIn("2.", out)
        self.assertEqual(("A1",), calls[0].args)


if __name__ == "__main__":
    unittest.main(verbosity=2)

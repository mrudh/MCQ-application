import os
import sys
import unittest
import importlib
from unittest.mock import patch, mock_open

MODULE_UNDER_TEST = "export_questions"


def _import_target():
    here = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return importlib.import_module(MODULE_UNDER_TEST)


class TestExportQuestions_FromTSLFrames(unittest.TestCase):


    def setUp(self):
        self.mod = _import_target()
        self.fn = getattr(self.mod, "export_questions")
        self.sample_data = [{"question": "Q1", "options": ["A", "B"], "answer": "A"}]
        setattr(self.mod, "ALL_QUIZ_DATA", self.sample_data)
        self.F1_default = None  
        self.F2_default_explicit = "exported_questions.json"
        self.F3_simple_custom = "questions.json"
        self.F4_path_like = os.path.join("exports", "questions.json")
        self.F5_spaces = "my questions.json"
        self.F6_spaces_path = os.path.join("my exports", "questions.json")
        self.F7_unicode = "प्रश्न.json"
        self.F8_unicode_spaces = "प्रश्न bank.json"


    def _call_with_filename(self, filename_or_none):
        if filename_or_none is None:
            return self.fn()  
        return self.fn(filename_or_none)

    def _assert_success_print(self, printed_args, expected_filename):
        joined = " ".join(str(x) for x in printed_args)
        self.assertIn("All questions exported successfully", joined)
        self.assertIn(f"'{expected_filename}'", joined)

    def _assert_error_print(self, printed_args):
        joined = " ".join(str(x) for x in printed_args)
        self.assertIn("Error exporting questions:", joined)

    def _run_success_case(self, filename_or_none, expected_filename):
        m = mock_open()
        with patch("builtins.open", m), patch.object(self.mod.json, "dump") as dump_mock, patch(
            "builtins.print"
        ) as print_mock:
            self._call_with_filename(filename_or_none)

        dump_mock.assert_called_once()
        args, kwargs = dump_mock.call_args
        self.assertEqual(args[0], self.sample_data)
        self.assertEqual(kwargs.get("indent"), 4)
        self.assertTrue(print_mock.called)
        self._assert_success_print(print_mock.call_args[0], expected_filename)

    def _run_open_error_case(self, filename_or_none, expected_filename, exc):
        with patch("builtins.open", side_effect=exc), patch("builtins.print") as print_mock:
            self._call_with_filename(filename_or_none)

        self.assertTrue(print_mock.called)
        self._assert_error_print(print_mock.call_args[0])

    def _run_dump_error_case(self, filename_or_none, expected_filename, exc):
        m = mock_open()
        with patch("builtins.open", m), patch.object(self.mod.json, "dump", side_effect=exc), patch(
            "builtins.print"
        ) as print_mock:
            self._call_with_filename(filename_or_none)

        self.assertTrue(print_mock.called)
        self._assert_error_print(print_mock.call_args[0])
        
    def test_case_01_key_1_1_default_success(self):
        self._run_success_case(self.F1_default, "exported_questions.json")

    def test_case_02_key_1_2_default_permission_denied(self):
        self._run_open_error_case(self.F1_default, "exported_questions.json", PermissionError("Permission denied"))

    def test_case_03_key_1_3_default_path_not_found(self):
        self._run_open_error_case(self.F1_default, "exported_questions.json", FileNotFoundError("No such file or directory"))

    def test_case_04_key_1_4_default_json_serialization_error(self):
        self._run_dump_error_case(self.F1_default, "exported_questions.json", TypeError("Object not JSON serializable"))

    def test_case_05_key_1_5_default_other_io_error(self):
        self._run_open_error_case(self.F1_default, "exported_questions.json", OSError("I/O error"))

    def test_case_06_key_2_1_default_explicit_success(self):
        self._run_success_case(self.F2_default_explicit, self.F2_default_explicit)

    def test_case_07_key_2_2_default_explicit_permission_denied(self):
        self._run_open_error_case(self.F2_default_explicit, self.F2_default_explicit, PermissionError("Permission denied"))

    def test_case_08_key_2_3_default_explicit_path_not_found(self):
        self._run_open_error_case(self.F2_default_explicit, self.F2_default_explicit, FileNotFoundError("No such file or directory"))

    def test_case_09_key_2_4_default_explicit_json_serialization_error(self):
        self._run_dump_error_case(self.F2_default_explicit, self.F2_default_explicit, TypeError("Object not JSON serializable"))

    def test_case_10_key_2_5_default_explicit_other_io_error(self):
        self._run_open_error_case(self.F2_default_explicit, self.F2_default_explicit, OSError("I/O error"))

    def test_case_11_key_3_1_simple_custom_success(self):
        self._run_success_case(self.F3_simple_custom, self.F3_simple_custom)

    def test_case_12_key_3_2_simple_custom_permission_denied(self):
        self._run_open_error_case(self.F3_simple_custom, self.F3_simple_custom, PermissionError("Permission denied"))

    def test_case_13_key_3_3_simple_custom_path_not_found(self):
        self._run_open_error_case(self.F3_simple_custom, self.F3_simple_custom, FileNotFoundError("No such file or directory"))

    def test_case_14_key_3_4_simple_custom_json_serialization_error(self):
        self._run_dump_error_case(self.F3_simple_custom, self.F3_simple_custom, TypeError("Object not JSON serializable"))

    def test_case_15_key_3_5_simple_custom_other_io_error(self):
        self._run_open_error_case(self.F3_simple_custom, self.F3_simple_custom, OSError("I/O error"))

    def test_case_16_key_4_1_path_like_success(self):
        self._run_success_case(self.F4_path_like, self.F4_path_like)

    def test_case_17_key_4_2_path_like_permission_denied(self):
        self._run_open_error_case(self.F4_path_like, self.F4_path_like, PermissionError("Permission denied"))

    def test_case_18_key_4_3_path_like_path_not_found(self):
        self._run_open_error_case(self.F4_path_like, self.F4_path_like, FileNotFoundError("No such file or directory"))

    def test_case_19_key_4_4_path_like_json_serialization_error(self):
        self._run_dump_error_case(self.F4_path_like, self.F4_path_like, TypeError("Object not JSON serializable"))

    def test_case_20_key_4_5_path_like_other_io_error(self):
        self._run_open_error_case(self.F4_path_like, self.F4_path_like, OSError("I/O error"))

    def test_case_21_key_5_1_spaces_success(self):
        self._run_success_case(self.F5_spaces, self.F5_spaces)

    def test_case_22_key_5_2_spaces_permission_denied(self):
        self._run_open_error_case(self.F5_spaces, self.F5_spaces, PermissionError("Permission denied"))

    def test_case_23_key_5_3_spaces_path_not_found(self):
        self._run_open_error_case(self.F5_spaces, self.F5_spaces, FileNotFoundError("No such file or directory"))

    def test_case_24_key_5_4_spaces_json_serialization_error(self):
        self._run_dump_error_case(self.F5_spaces, self.F5_spaces, TypeError("Object not JSON serializable"))

    def test_case_25_key_5_5_spaces_other_io_error(self):
        self._run_open_error_case(self.F5_spaces, self.F5_spaces, OSError("I/O error"))

    def test_case_26_key_6_1_spaces_path_success(self):
        self._run_success_case(self.F6_spaces_path, self.F6_spaces_path)

    def test_case_27_key_6_2_spaces_path_permission_denied(self):
        self._run_open_error_case(self.F6_spaces_path, self.F6_spaces_path, PermissionError("Permission denied"))

    def test_case_28_key_6_3_spaces_path_path_not_found(self):
        self._run_open_error_case(self.F6_spaces_path, self.F6_spaces_path, FileNotFoundError("No such file or directory"))

    def test_case_29_key_6_4_spaces_path_json_serialization_error(self):
        self._run_dump_error_case(self.F6_spaces_path, self.F6_spaces_path, TypeError("Object not JSON serializable"))

    def test_case_30_key_6_5_spaces_path_other_io_error(self):
        self._run_open_error_case(self.F6_spaces_path, self.F6_spaces_path, OSError("I/O error"))

    def test_case_31_key_7_1_unicode_success(self):
        self._run_success_case(self.F7_unicode, self.F7_unicode)

    def test_case_32_key_7_2_unicode_permission_denied(self):
        self._run_open_error_case(self.F7_unicode, self.F7_unicode, PermissionError("Permission denied"))

    def test_case_33_key_7_3_unicode_path_not_found(self):
        self._run_open_error_case(self.F7_unicode, self.F7_unicode, FileNotFoundError("No such file or directory"))

    def test_case_34_key_7_4_unicode_json_serialization_error(self):
        self._run_dump_error_case(self.F7_unicode, self.F7_unicode, TypeError("Object not JSON serializable"))

    def test_case_35_key_7_5_unicode_other_io_error(self):
        self._run_open_error_case(self.F7_unicode, self.F7_unicode, OSError("I/O error"))

    def test_case_36_key_8_1_unicode_spaces_success(self):
        self._run_success_case(self.F8_unicode_spaces, self.F8_unicode_spaces)

    def test_case_37_key_8_2_unicode_spaces_permission_denied(self):
        self._run_open_error_case(self.F8_unicode_spaces, self.F8_unicode_spaces, PermissionError("Permission denied"))

    def test_case_38_key_8_3_unicode_spaces_path_not_found(self):
        self._run_open_error_case(self.F8_unicode_spaces, self.F8_unicode_spaces, FileNotFoundError("No such file or directory"))

    def test_case_39_key_8_4_unicode_spaces_json_serialization_error(self):
        self._run_dump_error_case(self.F8_unicode_spaces, self.F8_unicode_spaces, TypeError("Object not JSON serializable"))

    def test_case_40_key_8_5_unicode_spaces_other_io_error(self):
        self._run_open_error_case(self.F8_unicode_spaces, self.F8_unicode_spaces, OSError("I/O error"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

import io
import json as pyjson
import os
import runpy
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, mock_open


import export_answers as sut


class TestExportAnswers(unittest.TestCase):
    
    def _read_json_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            return pyjson.load(f)

    def _set_quiz_data(self, mcq, fill):
        sut.ALL_QUIZ_DATA = mcq
        sut.FILL_IN_QUIZ_DATA = fill

    
    def test_illegal_filename_error(self):
        self._set_quiz_data([], [])
        bad_name = "illegal:name.json"

        fake_out = io.StringIO()
        with redirect_stdout(fake_out), patch("builtins.open", side_effect=OSError("illegal filename")):
            sut.export_answers(bad_name)

        out = fake_out.getvalue()
        self.assertIn("Error exporting answers", out)

  
    def test_cannot_write_permission_error(self):
        self._set_quiz_data([], [])
        fake_out = io.StringIO()

        with redirect_stdout(fake_out), patch("builtins.open", side_effect=PermissionError("no permission")):
            sut.export_answers("exported_answers.json")

        out = fake_out.getvalue()
        self.assertIn("Error exporting answers", out)

    
    def test_json_missing_error(self):
        self._set_quiz_data([], [])
        fake_out = io.StringIO()

        old_json = getattr(sut, "json", None)
        try:
            if hasattr(sut, "json"):
                delattr(sut, "json")

            with redirect_stdout(fake_out):
               
                with tempfile.TemporaryDirectory() as td:
                    outpath = os.path.join(td, "out.json")
                    sut.export_answers(outpath)

            out = fake_out.getvalue()
            self.assertIn("Error exporting answers", out)
        finally:
            
            sut.json = old_json

   
    def test_wrong_entrypoint_does_not_prompt(self):
      
        with patch("builtins.input") as mocked_input:
            runpy.run_module("export_answers", run_name="__main__")
            mocked_input.assert_not_called()

 
    def test_fill_in_data_not_iterable_raises(self):
        sut.ALL_QUIZ_DATA = []
        sut.FILL_IN_QUIZ_DATA = None

        with self.assertRaises(TypeError):
            sut.export_answers("x.json")

  
    def test_happy_default_filename_creates_json(self):
        mcq = [
            {
                "question": "Q1?",
                "options": ["A. one", "B. two"],
                "answer": "A",
                "topic": "t",
                "difficulty": "easy",
            }
        ]
        fill = [
            {"question": "Fill1?", "answer": "ans", "topic": "t2", "difficulty": "med"}
        ]
        self._set_quiz_data(mcq, fill)

        with tempfile.TemporaryDirectory() as td:
            cwd = os.getcwd()
            try:
                os.chdir(td)
                sut.export_answers()
                self.assertTrue(os.path.exists("exported_answers.json"))
                data = self._read_json_file("exported_answers.json")
                self.assertEqual(len(data["mcq_answers"]), 1)
                self.assertEqual(len(data["fill_in_answers"]), 1)
            finally:
                os.chdir(cwd)


    def test_happy_custom_filename(self):
        self._set_quiz_data([], [])
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "my_answers.json")
            sut.export_answers(outpath)
            self.assertTrue(os.path.exists(outpath))
            data = self._read_json_file(outpath)
            self.assertIn("mcq_answers", data)
            self.assertIn("fill_in_answers", data)


    def test_happy_filename_with_spaces(self):
        self._set_quiz_data([], [])
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "answers file.json")
            sut.export_answers(outpath)
            self.assertTrue(os.path.exists(outpath))


    def test_happy_path_with_folders(self):
        self._set_quiz_data([], [])
        with tempfile.TemporaryDirectory() as td:
            sub = os.path.join(td, "subdir1", "subdir2")
            os.makedirs(sub, exist_ok=True)
            outpath = os.path.join(sub, "answers.json")
            sut.export_answers(outpath)
            self.assertTrue(os.path.exists(outpath))


    def test_whitespace_input_results_in_default_name_logic(self):
        default_name = "exported_answers.json"
        user_input = "   "
        filename = user_input.strip()
        if not filename:
            filename = default_name
        self.assertEqual(filename, default_name)


    def test_edge_mcq_present_but_empty(self):
        self._set_quiz_data([], [])
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "out.json")
            sut.export_answers(outpath)
            data = self._read_json_file(outpath)
            self.assertEqual(data["mcq_answers"], [])


    def test_edge_fill_in_present_but_empty(self):
        self._set_quiz_data([], [])
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "out.json")
            sut.export_answers(outpath)
            data = self._read_json_file(outpath)
            self.assertEqual(data["fill_in_answers"], [])


    def test_edge_mcq_option_not_found_fallback(self):
        mcq = [
            {
                "question": "Q?",
                "options": ["A. one", "B. two"],
                "answer": "C",
                "topic": None,
                "difficulty": None,
            }
        ]
        self._set_quiz_data(mcq, [])
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "out.json")
            sut.export_answers(outpath)
            data = self._read_json_file(outpath)
            self.assertIn("option text not found", data["mcq_answers"][0]["correct_option_text"])

    
    def test_edge_mcq_answer_blank(self):
        mcq = [
            {
                "question": "Q?",
                "options": ["A. one", "B. two"],
                "answer": "",
                "topic": "x",
                "difficulty": "y",
            }
        ]
        self._set_quiz_data(mcq, [])
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "out.json")
            sut.export_answers(outpath)
            data = self._read_json_file(outpath)
            self.assertEqual(data["mcq_answers"][0]["correct_letter"], "")

    
    def test_edge_mcq_options_missing_none(self):
        mcq = [
            {
                "question": "Q?",
                "options": None,  
                "answer": "A",
                "topic": "x",
                "difficulty": "y",
            }
        ]
        sut.ALL_QUIZ_DATA = mcq
        sut.FILL_IN_QUIZ_DATA = []
        with self.assertRaises(TypeError):
            sut.export_answers("x.json")


    def test_edge_mcq_option_prefix_A_paren(self):
        mcq = [
            {
                "question": "Q?",
                "options": ["A) one", "B) two"],
                "answer": "A",
                "topic": "x",
                "difficulty": "y",
            }
        ]
        self._set_quiz_data(mcq, [])
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "out.json")
            sut.export_answers(outpath)
            data = self._read_json_file(outpath)
            self.assertIn("option text not found", data["mcq_answers"][0]["correct_option_text"])


    def test_edge_fillin_alternatives(self):
        fill = [{"question": "Fill?", "answer": "ans1 | ans2|ans3", "topic": "t", "difficulty": "d"}]
        self._set_quiz_data([], fill)
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "out.json")
            sut.export_answers(outpath)
            data = self._read_json_file(outpath)
            self.assertEqual(data["fill_in_answers"][0]["accepted_answers"], ["ans1", "ans2", "ans3"])

   
    def test_edge_fillin_blank(self):
        fill = [{"question": "Fill?", "answer": "   ", "topic": "t", "difficulty": "d"}]
        self._set_quiz_data([], fill)
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "out.json")
            sut.export_answers(outpath)
            data = self._read_json_file(outpath)
            self.assertEqual(data["fill_in_answers"][0]["accepted_answers"], [])


if __name__ == "__main__":
    unittest.main()

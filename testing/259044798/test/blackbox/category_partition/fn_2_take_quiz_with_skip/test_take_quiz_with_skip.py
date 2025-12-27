import sys
import unittest
import importlib
from pathlib import Path
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout


def add_project_root_to_syspath():
    here = Path(__file__).resolve()
    for parent in [here] + list(here.parents):
        if (parent / "mcq.py").exists():
            sys.path.insert(0, str(parent))
            return parent
    raise RuntimeError("Could not locate project root (mcq.py not found in parents).")


def run_quiz_capture_output(mod, questions, options, answers, name=None, inputs=None):
    if inputs is None:
        inputs = []

    buf = StringIO()

    has_scores = hasattr(mod, "load_scores") and hasattr(mod, "save_scores")

    patches = [
        patch("builtins.input", side_effect=inputs),
    ]
    if has_scores:
        patches += [
            patch.object(mod, "load_scores", return_value=[]),
            patch.object(mod, "save_scores", return_value=None),
        ]

    with patches[0]:
        if has_scores:
            with patches[1], patches[2]:
                with redirect_stdout(buf):
                    mod.take_quiz_with_skip(questions, options, answers, name=name)
        else:
            with redirect_stdout(buf):
                mod.take_quiz_with_skip(questions, options, answers, name=name)

    return buf.getvalue()


class TestTakeQuizWithSkip_FromTSL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_root = add_project_root_to_syspath()
        cls.mod = importlib.import_module("mcq")

        if not hasattr(cls.mod, "take_quiz_with_skip"):
            raise ImportError("mcq.py does not define take_quiz_with_skip")

    
    def sample_quiz_0(self):
        return [], [], []

    def sample_quiz_1(self):
        q = ["2 + 2 = ?"]
        o = [["A. 3", "B. 4", "C. 5", "D. 6"]]
        a = ["B"]
        return q, o, a

    def sample_quiz_2(self):
        q = ["2 + 2 = ?", "Capital of France?"]
        o = [
            ["A. 3", "B. 4", "C. 5", "D. 6"],
            ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
        ]
        a = ["B", "C"]
        return q, o, a

    
    def test_tc01_empty_questions_name_none(self):
        q, o, a = self.sample_quiz_0()
        out = run_quiz_capture_output(self.mod, q, o, a, name=None, inputs=[])
        self.assertIn("Total questions : 0", out)
        self.assertIn("Answered        : 0", out)
        self.assertIn("Skipped         : 0", out)
        self.assertIn("Your score is   : 0%", out)

    
    def test_tc02_empty_questions_name_provided(self):
        q, o, a = self.sample_quiz_0()
        out = run_quiz_capture_output(self.mod, q, o, a, name="Devyani", inputs=[])
        self.assertIn("Total questions : 0", out)
        self.assertIn("Your score is   : 0%", out)

    
    def test_tc03_options_length_mismatch(self):
        q, o, a = self.sample_quiz_2()
        o_bad = o[:1]  

        with self.assertRaises(Exception):
            run_quiz_capture_output(self.mod, q, o_bad, a, inputs=["A"])

    
    def test_tc04_answers_length_mismatch(self):
        q, o, a = self.sample_quiz_2()
        a_bad = a[:1]  

        with self.assertRaises(Exception):
            run_quiz_capture_output(self.mod, q, o, a_bad, inputs=["A"])

   
    def test_tc05_answers_contain_non_ad(self):
        q, o, a = self.sample_quiz_1()
        a_bad = ["E"]

        try:
            out = run_quiz_capture_output(self.mod, q, o, a_bad, inputs=["A"])
            self.assertIn("INCORRECT!", out)
            self.assertIn("E is the correct answer", out)
        except Exception:
            
            pass

    
    def test_tc06_valid_immediate_correct_no_skip(self):
        q, o, a = self.sample_quiz_1()
        out = run_quiz_capture_output(self.mod, q, o, a, inputs=["B"])
        self.assertIn("CORRECT!", out)
        self.assertIn("Skipped         : 0", out)
        self.assertIn("Correct         : 1", out)
        self.assertIn("Your score is   : 100%", out)

    
    def test_tc07_valid_immediate_incorrect(self):
        q, o, a = self.sample_quiz_1()
        out = run_quiz_capture_output(self.mod, q, o, a, inputs=["A"])
        self.assertIn("INCORRECT!", out)
        self.assertIn("B is the correct answer", out)
        self.assertIn("Your score is   : 0%", out)

    
    def test_tc08_skip_using_s_some_skipped(self):
        q, o, a = self.sample_quiz_2()
        out = run_quiz_capture_output(self.mod, q, o, a, inputs=["S", "C"])
        self.assertIn("Question skipped.", out)
        self.assertIn("Skipped         : 1", out)
        self.assertIn("Answered        : 1", out)

    
    def test_tc09_skip_using_enter_some_skipped(self):
        q, o, a = self.sample_quiz_2()
        out = run_quiz_capture_output(self.mod, q, o, a, inputs=["", "C"])
        self.assertIn("Question skipped.", out)
        self.assertIn("Skipped         : 1", out)
        self.assertIn("Answered        : 1", out)

    
    def test_tc10_invalid_then_valid(self):
        q, o, a = self.sample_quiz_1()
        out = run_quiz_capture_output(self.mod, q, o, a, inputs=["X", "B"])
        self.assertIn("Invalid input. Please enter A, B, C, D, or S to skip.", out)
        self.assertIn("CORRECT!", out)
        self.assertIn("Your score is   : 100%", out)

    
    def test_tc11_invalid_then_skip(self):
        q, o, a = self.sample_quiz_1()
        out = run_quiz_capture_output(self.mod, q, o, a, inputs=["X", "S"])
        self.assertIn("Invalid input. Please enter A, B, C, D, or S to skip.", out)
        self.assertIn("Question skipped.", out)
        self.assertIn("Answered        : 0", out)
        self.assertIn("Skipped         : 1", out)
        self.assertIn("Your score is   : 0%", out)

    
    def test_tc12_all_skipped_answered_zero_percent_zero(self):
        q, o, a = self.sample_quiz_2()
        out = run_quiz_capture_output(self.mod, q, o, a, inputs=["S", ""])
        self.assertIn("Skipped         : 2", out)
        self.assertIn("Answered        : 0", out)
        self.assertIn("Your score is   : 0%", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)

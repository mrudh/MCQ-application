import os
import sys
import io
import unittest
import importlib
from contextlib import redirect_stdout
from unittest.mock import patch


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

MODULE_UNDER_TEST = "mcq"


def _get_func():
    mod = importlib.import_module(MODULE_UNDER_TEST)
    return mod.take_quiz_with_summary


class TestTakeQuizWithSummary_FromTSLFrames(unittest.TestCase):
    

    def setUp(self):
        self.take_quiz_with_summary = _get_func()

      
        self.questions = ["Q1?"]
        self.options = [["A. Option A", "B. Option B", "C. Option C", "D. Option D"]]
        self.answers = ["A"]

    def _run_case(self, *, timed: bool, input_mode: str, name_value):
        
        buf = io.StringIO()

        if timed:
            tq_return = "A" if input_mode == "valid" else None

            with patch("mcq.timed_quiz", return_value=tq_return):
                with redirect_stdout(buf):
                    self.take_quiz_with_summary(
                        self.questions,
                        self.options,
                        self.answers,
                        name=name_value,
                        timed=True
                    )
        else:
            input_return = "A" if input_mode == "valid" else ""

            with patch("builtins.input", return_value=input_return):
                with redirect_stdout(buf):
                    self.take_quiz_with_summary(
                        self.questions,
                        self.options,
                        self.answers,
                        name=name_value,
                        timed=False
                    )

        return buf.getvalue()


    def test_20_frames(self):
        

        name_states = [
            ("Name is provided (non-empty)", "Sarthak"),
            ("Name is not provided (None)", None),
            ('Name is empty string ("")', ""),
            ('Name is whitespace ("   ")', "   "),
            ('Name contains special chars ("@#")', "@#"),
        ]

        frames = []

        for _, name in name_states:
            frames.append((True, "valid", name))

        for _, name in name_states:
            frames.append((True, "timeout", name))

        for _, name in name_states:
            frames.append((False, "valid", name))

        for _, name in name_states:
            frames.append((False, "timeout", name))

        for i, (timed, input_mode, name_val) in enumerate(frames, start=1):
           
            with self.subTest(
                TSL_Test_Case=f"Test Case {i}",
                QuizMode=("Timed enabled" if timed else "Timed disabled"),
                InputResult=("Valid choice" if input_mode == "valid" else "Timeout/Blank"),
                NameProvided=repr(name_val),
            ):
                output = self._run_case(
                    timed=timed,
                    input_mode=input_mode,
                    name_value=name_val
                )

                self.assertIn("RESULTS", output)

                if timed:
                    self.assertIn("You have 5 seconds for each question!", output)

                if input_mode == "valid":
                 
                    self.assertIn("CORRECT!", output)
                    self.assertIn("Score: 1 / 1", output)
                    self.assertIn("Percentage: 100%", output)
                else:
                    
                    if timed:
                        self.assertIn("Time's up!", output)

                    self.assertIn("INCORRECT!", output)
                    self.assertIn("The correct answer is: A", output)
                    self.assertIn("Score: 0 / 1", output)
                    self.assertIn("Percentage: 0%", output)


if __name__ == "__main__":
    unittest.main()

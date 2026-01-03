import unittest
from unittest.mock import patch
import importlib
import io
import contextlib


CANDIDATE_MODULES = ["mcq", "main", "mcq_types"]


def _import_target():
    last_err = None
    for m in CANDIDATE_MODULES:
        try:
            mod = importlib.import_module(m)
            if hasattr(mod, "take_quiz_with_summary"):
                return mod
        except Exception as e:
            last_err = e
    raise ImportError(
        "Could not import a module containing take_quiz_with_summary. "
        f"Tried: {CANDIDATE_MODULES}. Last error: {last_err}"
    )


class TestLoopTakeQuizWithSummary(unittest.TestCase):

    def test_zero_iteration(self):
        target = _import_target()

        questions = []
        options = []
        answers = []
        with self.assertRaises(ZeroDivisionError):
            target.take_quiz_with_summary(questions, options, answers, name="Sarthak", timed=False)

    @patch("builtins.input", side_effect=["A"])
    def test_one_iteration(self, _mock_input):
        target = _import_target()

        questions = ["Q1?"]
        options = [["A. a", "B. b", "C. c", "D. d"]]
        answers = ["A"]

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            target.take_quiz_with_summary(questions, options, answers, name="Sarthak", timed=False)

        out = buf.getvalue()
        self.assertIn("CORRECT!", out)

    @patch("builtins.input", side_effect=["A", "B", "C"])
    def test_multiple_iterations(self, _mock_input):
        target = _import_target()

        questions = ["Q1?", "Q2?", "Q3?"]
        options = [
            ["A. a", "B. b", "C. c", "D. d"],
            ["A. a", "B. b", "C. c", "D. d"],
            ["A. a", "B. b", "C. c", "D. d"],
        ]
        answers = ["A", "B", "D"]  

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            target.take_quiz_with_summary(questions, options, answers, name="Sarthak", timed=False)

        out = buf.getvalue()
        self.assertIn("CORRECT!", out)
        self.assertIn("INCORRECT!", out)


    def test_timed_mode_timeout_path(self):
        target = _import_target()

        with patch(f"{target.__name__}.timed_quiz", return_value=None):
            questions = ["Q1?"]
            options = [["A. a", "B. b", "C. c", "D. d"]]
            answers = ["A"]

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                target.take_quiz_with_summary(questions, options, answers, name="Sarthak", timed=True)

            out = buf.getvalue()
            self.assertIn("Time's up!", out)


if __name__ == "__main__":
    unittest.main()

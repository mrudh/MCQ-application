import unittest
from unittest.mock import patch
import importlib
import io
import contextlib
import os
import sys



def _find_project_root(start_dir: str) -> str | None:
    cur = os.path.abspath(start_dir)
    while True:
        if (os.path.exists(os.path.join(cur, "mcq.py")) or
                os.path.exists(os.path.join(cur, "main.py")) or
                os.path.exists(os.path.join(cur, "mcq_types.py"))):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


PROJECT_ROOT = _find_project_root(os.path.dirname(__file__))
if PROJECT_ROOT and PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


CANDIDATE_MODULES = ["mcq", "main", "mcq_types"]


def _import_target():
    for m in CANDIDATE_MODULES:
        try:
            mod = importlib.import_module(m)
            if hasattr(mod, "take_quiz_with_summary"):
                return mod
        except Exception:
            pass
    raise ImportError(
        f"Could not import take_quiz_with_summary from {CANDIDATE_MODULES}. "
        f"Detected PROJECT_ROOT={PROJECT_ROOT}"
    )


def _capture(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()


class TestTakeQuizWithSummary_StatementTesting(unittest.TestCase):


    @patch("builtins.input", side_effect=["A"])
    def test_statement_non_timed_correct(self, _):
        target = _import_target()
        out = _capture(
            target.take_quiz_with_summary,
            ["Q1?"],
            [["A. a", "B. b", "C. c", "D. d"]],
            ["A"],
            name="Sarthak",
            timed=False
        )
        self.assertIn("CORRECT!", out)
        self.assertIn("RESULTS", out)

    @patch("builtins.input", side_effect=["B"])
    def test_statement_non_timed_incorrect(self, _):
        target = _import_target()
        out = _capture(
            target.take_quiz_with_summary,
            ["Q1?"],
            [["A. a", "B. b", "C. c", "D. d"]],
            ["A"],
            name="Sarthak",
            timed=False
        )
        self.assertIn("INCORRECT!", out)
        self.assertIn("The correct answer is:", out)


    def test_statement_timed_timeout(self):
        target = _import_target()
        with patch(f"{target.__name__}.timed_quiz", return_value=None):
            out = _capture(
                target.take_quiz_with_summary,
                ["Q1?"],
                [["A. a", "B. b", "C. c", "D. d"]],
                ["A"],
                name="Sarthak",
                timed=True
            )
        self.assertIn("You have 5 seconds", out)
        self.assertIn("Time's up!", out)

    @patch("builtins.input", side_effect=["A", "B", "C"])
    def test_statement_multiple_questions(self, _):
        target = _import_target()
        out = _capture(
            target.take_quiz_with_summary,
            ["Q1?", "Q2?", "Q3?"],
            [["A. a", "B. b", "C. c", "D. d"]] * 3,
            ["A", "B", "D"],  
            name="Sarthak",
            timed=False
        )
        self.assertIn("CORRECT!", out)
        self.assertIn("INCORRECT!", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)

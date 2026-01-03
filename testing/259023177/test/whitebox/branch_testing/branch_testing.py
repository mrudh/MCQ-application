import unittest
from unittest.mock import patch
import importlib
import io
import contextlib
import os
import sys



def _find_project_root(start_dir: str):
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
    errors = {}
    for m in CANDIDATE_MODULES:
        try:
            mod = importlib.import_module(m)
            if hasattr(mod, "take_quiz_with_summary"):
                return mod
            errors[m] = "imported but take_quiz_with_summary not found"
        except Exception as e:
            errors[m] = repr(e)

    raise ImportError(
        "Could not locate take_quiz_with_summary.\n"
        f"Detected PROJECT_ROOT={PROJECT_ROOT}\n" +
        "\n".join([f"{k}: {v}" for k, v in errors.items()])
    )


def _capture_output(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()



class TestTakeQuizWithSummary_BranchTesting(unittest.TestCase):


    def test_timed_true_timeout_branch(self):
        target = _import_target()
        with patch(f"{target.__name__}.timed_quiz", return_value=None):
            out = _capture_output(
                target.take_quiz_with_summary,
                ["Q1?"],
                [["A. a", "B. b", "C. c", "D. d"]],
                ["A"],
                name="Sarthak",
                timed=True
            )
        self.assertIn("Time's up!", out)  
        
        
    def test_timed_true_non_timeout_branch_correct(self):
        target = _import_target()
        with patch(f"{target.__name__}.timed_quiz", return_value="A"):
            out = _capture_output(
                target.take_quiz_with_summary,
                ["Q1?"],
                [["A. a", "B. b", "C. c", "D. d"]],
                ["A"],
                name="Sarthak",
                timed=True
            )
        self.assertIn("CORRECT!", out)

    
    @patch("builtins.input", side_effect=["B", "B", "B", "B"])  
    def test_summary_branch_0_to_25(self, _):
        target = _import_target()
        out = _capture_output(
            target.take_quiz_with_summary,
            ["Q1?", "Q2?", "Q3?", "Q4?"],
            [["A. a", "B. b", "C. c", "D. d"]] * 4,
            ["A", "A", "A", "A"],
            timed=False
        )
        self.assertIn("A challenging start", out)

    @patch("builtins.input", side_effect=["A", "A", "B", "B"])  
    def test_summary_branch_26_to_50(self, _):
        target = _import_target()
        out = _capture_output(
            target.take_quiz_with_summary,
            ["Q1?", "Q2?", "Q3?", "Q4?"],
            [["A. a", "B. b", "C. c", "D. d"]] * 4,
            ["A", "A", "A", "A"],
            timed=False
        )
        self.assertIn("Good effort", out)

    @patch("builtins.input", side_effect=["A", "A", "A", "B"])  
    def test_summary_branch_51_to_75(self, _):
        target = _import_target()
        out = _capture_output(
            target.take_quiz_with_summary,
            ["Q1?", "Q2?", "Q3?", "Q4?"],
            [["A. a", "B. b", "C. c", "D. d"]] * 4,
            ["A", "A", "A", "A"],
            timed=False
        )
        self.assertIn("Nice work", out)


    @patch("builtins.input", side_effect=["A", "A", "A", "A"])  
    def test_summary_branch_76_to_100(self, _):
        target = _import_target()
        out = _capture_output(
            target.take_quiz_with_summary,
            ["Q1?", "Q2?", "Q3?", "Q4?"],
            [["A. a", "B. b", "C. c", "D. d"]] * 4,
            ["A", "A", "A", "A"],
            timed=False
        )
        self.assertIn("Excellent performance", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)

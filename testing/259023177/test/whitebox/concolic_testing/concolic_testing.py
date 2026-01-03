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
                os.path.exists(os.path.join(cur, "main.py"))):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


PROJECT_ROOT = _find_project_root(os.path.dirname(__file__))
if PROJECT_ROOT and PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

CANDIDATE_MODULES = ["mcq", "main"]


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
    raise ImportError("Could not import take_quiz_with_summary: " + str(errors))


def _run_case(target, *, timed: bool, timeout: bool, answers, guesses):
    n = len(answers)
    questions = [f"Q{i+1}?" for i in range(n)]
    options = [["A. a", "B. b", "C. c", "D. d"] for _ in range(n)]

    buf = io.StringIO()
    hit = set()

    hit.add("TIMED_TRUE" if timed else "TIMED_FALSE")

    if timed:
        if timeout:
            timed_side_effect = [None] * n
        else:
            timed_side_effect = guesses[:]  

        with patch(f"{target.__name__}.timed_quiz", side_effect=timed_side_effect):
            with contextlib.redirect_stdout(buf):
                target.take_quiz_with_summary(
                    questions, options, answers, name="Sarthak", timed=True
                )
    else:
        with patch("builtins.input", side_effect=guesses):
            with contextlib.redirect_stdout(buf):
                target.take_quiz_with_summary(
                    questions, options, answers, name="Sarthak", timed=False
                )

    out = buf.getvalue()

    if "Time's up!" in out:
        hit.add("TIMEOUT_PATH")
    else:
        hit.add("NO_TIMEOUT_PATH")

    if "CORRECT!" in out:
        hit.add("HAS_CORRECT")
    if "INCORRECT!" in out:
        hit.add("HAS_INCORRECT")
    if "A challenging start" in out:
        hit.add("SUMMARY_0_25")
    if "Good effort" in out:
        hit.add("SUMMARY_26_50")
    if "Nice work" in out:
        hit.add("SUMMARY_51_75")
    if "Excellent performance" in out:
        hit.add("SUMMARY_76_100")

    return out, hit


class TestTakeQuizWithSummary_Concolic(unittest.TestCase):


    def test_concolic_path_generation(self):
        target = _import_target()
        goals = {
            "TIMED_TRUE",
            "TIMED_FALSE",
            "TIMEOUT_PATH",
            "NO_TIMEOUT_PATH",
            "HAS_CORRECT",
            "HAS_INCORRECT",
            "SUMMARY_0_25",
            "SUMMARY_26_50",
            "SUMMARY_51_75",
            "SUMMARY_76_100",
        }

        cases = [
            dict(timed=True, timeout=True, answers=["A"], guesses=["A"]),
            dict(timed=True, timeout=False, answers=["A"], guesses=["A"]),
            dict(timed=False, timeout=False, answers=["A"], guesses=["B"]),
        ]


        cases += [
            dict(timed=False, timeout=False, answers=["A", "A", "A", "A"], guesses=["B", "B", "B", "B"]),  # 0%
            dict(timed=False, timeout=False, answers=["A", "A", "A", "A"], guesses=["A", "A", "B", "B"]),  # 50%
            dict(timed=False, timeout=False, answers=["A", "A", "A", "A"], guesses=["A", "A", "A", "B"]),  # 75%
            dict(timed=False, timeout=False, answers=["A", "A", "A", "A"], guesses=["A", "A", "A", "A"]),  # 100%
        ]

        covered = set()
        outputs = []

        for c in cases:
            out, hit = _run_case(target, **c)
            outputs.append(out)
            covered |= hit

        missing = goals - covered

        self.assertFalse(
            missing,
            msg="Concolic goals not covered: " + ", ".join(sorted(missing))
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

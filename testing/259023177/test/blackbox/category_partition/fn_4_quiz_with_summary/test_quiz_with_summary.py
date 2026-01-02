import os
import sys
import io
import unittest
import importlib
from contextlib import redirect_stdout
from unittest.mock import patch

# ------------------------------------------------------------------
# Ensure project root (MCQ-application) is on Python path
# ------------------------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Module where take_quiz_with_summary is defined
MODULE_UNDER_TEST = "mcq"


def _get_func():
    mod = importlib.import_module(MODULE_UNDER_TEST)
    return mod.take_quiz_with_summary


class TestTakeQuizWithSummary_FromTSLFrames(unittest.TestCase):
    """
    Unit tests derived from the 20 TSL test frames
    (Category Partition → TSL → Test Frames → Python unittest)

    Run with verbose output to see each frame:
      python -m unittest testing.259023177.test.blackbox.category_partition.fn_4_quiz_with_summary.test_quiz_with_summary -v
    """

    def setUp(self):
        self.take_quiz_with_summary = _get_func()

        # Minimal deterministic quiz (1 question)
        self.questions = ["Q1?"]
        self.options = [["A. Option A", "B. Option B", "C. Option C", "D. Option D"]]
        self.answers = ["A"]

    def _run_case(self, *, timed: bool, input_mode: str, name_value):
        """
        input_mode:
          - "valid"   -> correct answer "A"
          - "timeout" -> None for timed=True, "" for timed=False
        """
        buf = io.StringIO()

        if timed:
            # timed=True → uses timed_quiz()
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
            # timed=False → uses input()
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
        """
        Covers all 20 TSL frames:
        (Timed/Untimed) × (Valid/Timeout) × (5 name states)

        Each subTest is labeled so you can see the specific frame in verbose output.
        """

        name_states = [
            ("Name is provided (non-empty)", "Sarthak"),
            ("Name is not provided (None)", None),
            ('Name is empty string ("")', ""),
            ('Name is whitespace ("   ")', "   "),
            ('Name contains special chars ("@#")', "@#"),
        ]

        frames = []

        # Test cases 1–5: timed + valid
        for _, name in name_states:
            frames.append((True, "valid", name))

        # Test cases 6–10: timed + timeout
        for _, name in name_states:
            frames.append((True, "timeout", name))

        # Test cases 11–15: untimed + valid
        for _, name in name_states:
            frames.append((False, "valid", name))

        # Test cases 16–20: untimed + blank (timeout-like)
        for _, name in name_states:
            frames.append((False, "timeout", name))

        for i, (timed, input_mode, name_val) in enumerate(frames, start=1):
            # ✅ SubTest label shows the specific test frame in output when run with -v
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

                # Results section must always print
                self.assertIn("RESULTS", output)

                if timed:
                    self.assertIn("You have 5 seconds for each question!", output)

                if input_mode == "valid":
                    # Correct case
                    self.assertIn("CORRECT!", output)
                    self.assertIn("Score: 1 / 1", output)
                    self.assertIn("Percentage: 100%", output)
                else:
                    # Timeout / blank → incorrect
                    if timed:
                        self.assertIn("Time's up!", output)

                    self.assertIn("INCORRECT!", output)
                    self.assertIn("The correct answer is: A", output)
                    self.assertIn("Score: 0 / 1", output)
                    self.assertIn("Percentage: 0%", output)


if __name__ == "__main__":
    unittest.main()

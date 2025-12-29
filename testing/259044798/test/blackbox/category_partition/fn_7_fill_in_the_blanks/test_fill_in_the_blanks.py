import io
import unittest
from unittest.mock import patch, Mock
import sys
import os


ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../..")
)
sys.path.insert(0, ROOT_DIR)

import mcq as m


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def run_quiz_capture(questions, answers, user_inputs, name):
    fake_out = io.StringIO()
    save_called = False
    saved_payload = None

    def fake_save_scores(payload):
        nonlocal save_called, saved_payload
        save_called = True
        saved_payload = payload

    
    fake_load_scores = Mock(return_value=[])

    exc = None
    with patch.object(m, "_normalize_text", side_effect=_norm), \
         patch.object(m, "load_scores", fake_load_scores), \
         patch.object(m, "save_scores", side_effect=fake_save_scores), \
         patch("builtins.input", side_effect=user_inputs), \
         patch("sys.stdout", fake_out):
        try:
            m.take_fill_in_the_blanks_quiz(questions, answers, name=name)
        except Exception as e:
            exc = e

    return fake_out.getvalue(), save_called, saved_payload, exc


class TestFillInTheBlanksQuiz_Frames(unittest.TestCase):
    def test_all_frames(self):

        NONEMPTY_Q = ["2+2=__"]  
        SINGLE_CORRECT_A = ["4"]
        MULTI_CORRECT_A = ["4|four"]

        frames = []
        frames.append(dict(
            key="TC1",
            questions=["Q1", "Q2"],
            answers=["A1"],  # shorter
            user_inputs=["a", "b"],
            name=None,
            expect_exc=IndexError,
            expect_percent=None,
            expect_save=False
        ))

        
        def add_frame(tc, key, questions, answers, user_inputs, name, expect_percent, expect_save):
            frames.append(dict(
                key=f"{tc} (Key = {key})",
                questions=questions,
                answers=answers,
                user_inputs=user_inputs,
                name=name,
                expect_exc=None,
                expect_percent=expect_percent,
                expect_save=expect_save
            ))

        
        empty_q = []
        longer_answers_single = ["4", "extra"]
        longer_answers_multi = ["4|four", "extra|spare"]

        
        for tc, key, name in [
            (2, "1.1.1.1.1.0.", None),
            (3, "1.1.1.1.2.1.", "Devyani"),
            (4, "1.1.1.2.1.0.", None),
            (5, "1.1.1.2.2.1.", "Devyani"),
            (6, "1.1.2.1.1.0.", None),
            (7, "1.1.2.1.2.1.", "Devyani"),
            (8, "1.1.2.2.1.0.", None),
            (9, "1.1.2.2.2.1.", "Devyani"),
        ]:
            add_frame(tc, key, empty_q, [], [], name, expect_percent=0, expect_save=(name is not None))

        
        for tc, key, name, ans in [
            (10, "1.3.1.1.1.0.", None, longer_answers_single),
            (11, "1.3.1.1.2.1.", "Devyani", longer_answers_single),
            (12, "1.3.1.2.1.0.", None, longer_answers_single),
            (13, "1.3.1.2.2.1.", "Devyani", longer_answers_single),
            (14, "1.3.2.1.1.0.", None, longer_answers_multi),
            (15, "1.3.2.1.2.1.", "Devyani", longer_answers_multi),
            (16, "1.3.2.2.1.0.", None, longer_answers_multi),
            (17, "1.3.2.2.2.1.", "Devyani", longer_answers_multi),
        ]:
            add_frame(tc, key, empty_q, ans, [], name, expect_percent=0, expect_save=(name is not None))

        

        add_frame(18, "2.1.1.1.1.0.", NONEMPTY_Q, SINGLE_CORRECT_A, ["4"], None, 100, False)
        add_frame(19, "2.1.1.1.2.1.", NONEMPTY_Q, SINGLE_CORRECT_A, ["4"], "Devyani", 100, True)
        add_frame(20, "2.1.1.2.1.0.", NONEMPTY_Q, SINGLE_CORRECT_A, ["5"], None, 0, False)
        add_frame(21, "2.1.1.2.2.1.", NONEMPTY_Q, SINGLE_CORRECT_A, ["5"], "Devyani", 0, True)

        add_frame(22, "2.1.2.1.1.0.", NONEMPTY_Q, MULTI_CORRECT_A, ["four"], None, 100, False)
        add_frame(23, "2.1.2.1.2.1.", NONEMPTY_Q, MULTI_CORRECT_A, ["four"], "Devyani", 100, True)
        add_frame(24, "2.1.2.2.1.0.", NONEMPTY_Q, MULTI_CORRECT_A, ["5"], None, 0, False)
        add_frame(25, "2.1.2.2.2.1.", NONEMPTY_Q, MULTI_CORRECT_A, ["5"], "Devyani", 0, True)

        
        add_frame(26, "2.3.1.1.1.0.", NONEMPTY_Q, ["4", "x"], ["4"], None, 100, False)
        add_frame(27, "2.3.1.1.2.1.", NONEMPTY_Q, ["4", "x"], ["4"], "Devyani", 100, True)
        add_frame(28, "2.3.1.2.1.0.", NONEMPTY_Q, ["4", "x"], ["5"], None, 0, False)
        add_frame(29, "2.3.1.2.2.1.", NONEMPTY_Q, ["4", "x"], ["5"], "Devyani", 0, True)

        add_frame(30, "2.3.2.1.1.0.", NONEMPTY_Q, ["4|four", "x|y"], ["four"], None, 100, False)
        add_frame(31, "2.3.2.1.2.1.", NONEMPTY_Q, ["4|four", "x|y"], ["four"], "Devyani", 100, True)
        add_frame(32, "2.3.2.2.1.0.", NONEMPTY_Q, ["4|four", "x|y"], ["5"], None, 0, False)
        add_frame(33, "2.3.2.2.2.1.", NONEMPTY_Q, ["4|four", "x|y"], ["5"], "Devyani", 0, True)

        for fr in frames:
            with self.subTest(frame=fr["key"]):
                out, save_called, saved_payload, exc = run_quiz_capture(
                    fr["questions"], fr["answers"], fr["user_inputs"], fr["name"]
                )

                if fr["expect_exc"] is not None:
                    self.assertIsNotNone(exc)
                    self.assertIsInstance(exc, fr["expect_exc"])
                    continue

                self.assertIsNone(exc)

                if fr["expect_percent"] is not None:
                    self.assertIn(f"Your score is   : {fr['expect_percent']}%", out)

                self.assertEqual(fr["expect_save"], save_called)
                if fr["expect_save"]:
                    self.assertIsInstance(saved_payload, list)
                    self.assertTrue(any(x.get("name") == fr["name"] for x in saved_payload))


if __name__ == "__main__":
    unittest.main()

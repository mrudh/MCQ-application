import unittest
from unittest.mock import patch, mock_open
import io
import mcq as mcq_mod
import attempts as att_mod


class TestConditionQuizFunctions(unittest.TestCase):

    def test_fill_in_correct(self):
        with patch("builtins.input", return_value="4"), \
             patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_fill_in_the_blanks_quiz(["2+2=____"], ["4"], name=None)
            self.assertIn("CORRECT", out.getvalue())


    def test_fill_in_incorrect(self):
        with patch("builtins.input", return_value="5"), \
             patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_fill_in_the_blanks_quiz(["2+2=____"], ["4"], name=None)
            self.assertIn("INCORRECT", out.getvalue())

   
    def test_get_option_text_match(self):
        if not hasattr(mcq_mod, "_get_option_text"):
            self.skipTest("_get_option_text not implemented")
        result = mcq_mod._get_option_text(["A. Apple"], "A")
        self.assertEqual(result, "A. Apple")


    def test_get_option_text_no_match(self):
        if not hasattr(mcq_mod, "_get_option_text"):
            self.skipTest("_get_option_text not implemented")
        result = mcq_mod._get_option_text(["A. Apple"], "B")
        self.assertIn("not found", result)

    
    def test_quiz_skip(self):
        with patch("builtins.input", return_value=""), \
             patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_quiz_with_skip(
                ["Q?"],
                [["A. X", "B. Y", "C. Z", "D. W"]],
                ["A"],
                name=None
            )
            self.assertIn("skipped", out.getvalue().lower())


    def test_quiz_answer(self):
        with patch("builtins.input", return_value="A"), \
             patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_quiz_with_skip(
                ["Q?"],
                [["A. X", "B. Y", "C. Z", "D. W"]],
                ["A"],
                name=None
            )
            self.assertIn("score", out.getvalue().lower())

    
    def test_age_based_no_questions(self):
        data = [{
            "question": "Hard Q",
            "options": ["A","B","C","D"],
            "answer": "A",
            "difficulty": "Hard"
        }]
        with patch("builtins.input", side_effect=["Dev", "9"]), \
             patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.age_based_quiz(data)
            self.assertIn("No questions", out.getvalue())


    def test_age_based_questions_exist(self):
        data = [{
            "question": "Easy Q",
            "options": ["A","B","C","D"],
            "answer": "A",
            "difficulty": "Easy"
        }]
        with patch("builtins.input", side_effect=["Dev", "9", "1"]), \
             patch.object(mcq_mod, "take_quiz"), \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.age_based_quiz(data)

    
    def test_can_attempt_true(self):
        with patch.object(att_mod, "get_attempts_left", return_value=1):
            self.assertTrue(att_mod.can_attempt_quiz("Dev"))

    def test_can_attempt_false(self):
        with patch.object(att_mod, "get_attempts_left", return_value=0):
         can_attempt, left = att_mod.can_attempt_quiz("Dev")
         self.assertFalse(can_attempt)
         self.assertEqual(left, 0)



if __name__ == "__main__":
    unittest.main()

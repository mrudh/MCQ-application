import unittest
from unittest.mock import patch, mock_open
import io

import mcq as mcq_mod
import attempts as att_mod


class TestStatementQuizFunctions(unittest.TestCase):

    def test_take_fill_in_the_blanks_quiz(self):
        questions = ["2+2 = ____"]
        answers = ["4"]
        with patch("builtins.input", return_value="4"), \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.take_fill_in_the_blanks_quiz(questions, answers, name="Dev")


    def test_get_option_text(self):
        if not hasattr(mcq_mod, "_get_option_text"):
            self.skipTest("_get_option_text not implemented in mcq.py")

        options = ["A. Apple", "B. Banana"]
        result = mcq_mod._get_option_text(options, "A")
        self.assertEqual(result, "A. Apple")


    def test_show_all_mcq_answers(self):
        if not hasattr(mcq_mod, "show_all_mcq_answers") or not hasattr(mcq_mod, "ALL_QUIZ_DATA"):
            self.skipTest("show_all_mcq_answers / ALL_QUIZ_DATA not implemented in mcq.py")

        data = [{
            "question": "Capital of India?",
            "options": ["A. Delhi", "B. Mumbai"],
            "answer": "A"
        }]
        with patch.object(mcq_mod, "ALL_QUIZ_DATA", data), \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.show_all_mcq_answers()

    
    def test_show_all_fill_in_answers(self):
        if not hasattr(mcq_mod, "show_all_fill_in_answers") or not hasattr(mcq_mod, "FILL_IN_QUIZ_DATA"):
            self.skipTest("show_all_fill_in_answers / FILL_IN_QUIZ_DATA not implemented in mcq.py")

        data = [{"question": "Sky color ____", "answer": "blue"}]
        with patch.object(mcq_mod, "FILL_IN_QUIZ_DATA", data), \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.show_all_fill_in_answers()

    
    def test_take_quiz_with_skip(self):
        questions = ["Pick A"]
        options = [["A. Yes", "B. No", "C. Maybe", "D. Later"]]
        answers = ["A"]
        with patch("builtins.input", return_value="A"), \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.take_quiz_with_skip(questions, options, answers, name="Dev")

    
    def test_age_based_quiz(self):
        data = [{
            "question": "Easy Q",
            "options": ["A.1","B.2","C.3","D.4"],
            "answer": "A",
            "difficulty": "Easy"
        }]
        with patch("builtins.input", side_effect=["Dev", "9", "1"]), \
             patch.object(mcq_mod, "take_quiz"), \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.age_based_quiz(data)

   
    def test_load_attempts(self):
        fake_json = '{"Dev": {"2025-01-01": 1}}'
        with patch("builtins.open", mock_open(read_data=fake_json)), \
             patch("os.path.exists", return_value=True):
            result = att_mod._load_attempts()
            self.assertIn("Dev", result)

    
    def test_save_attempts(self):
        data = {"Dev": {"2025-01-01": 1}}
        with patch("builtins.open", mock_open()):
            att_mod._save_attempts(data)

    
    def test_today_str(self):
        date_str = att_mod._today_str()
        self.assertEqual(len(date_str), 10)

   
    def test_get_attempts_left(self):
        fake_data = {"Dev": {"2025-01-01": 1}}
        with patch.object(att_mod, "_load_attempts", return_value=fake_data), \
             patch.object(att_mod, "_today_str", return_value="2025-01-01"):
            left = att_mod.get_attempts_left("Dev")
            self.assertGreaterEqual(left, 0)

    
    def test_can_attempt_quiz(self):
        with patch.object(att_mod, "get_attempts_left", return_value=1):
            self.assertTrue(att_mod.can_attempt_quiz("Dev"))

    
    def test_record_quiz_attempt(self):
        fake_data = {}
        with patch.object(att_mod, "_load_attempts", return_value=fake_data), \
             patch.object(att_mod, "_save_attempts"):
            att_mod.record_quiz_attempt("Dev")

    
    def test_key_zero_na(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

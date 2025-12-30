import unittest
from unittest.mock import patch
import io
import mcq as mcq_mod          
import attempts as att_mod     


class TestLoopQuizFunctions(unittest.TestCase):

    def test_fillin_zero_iteration(self):
        with patch("builtins.input", side_effect=[]), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_fill_in_the_blanks_quiz([], [], name=None)
            text = out.getvalue()
            self.assertIn("Total questions : 0", text)
            self.assertIn("Your score is   : 0%", text)

    def test_fillin_one_iteration(self):
        questions = ["2+2 = ____"]
        answers = ["4"]
        with patch("builtins.input", side_effect=["4"]), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_fill_in_the_blanks_quiz(questions, answers, name=None)
            text = out.getvalue()
            self.assertIn("CORRECT!", text)
            self.assertIn("Total questions : 1", text)

    def test_fillin_multiple_iterations(self):
        questions = ["A = ____", "B = ____", "C = ____"]
        answers = ["x", "y", "z"]
        with patch("builtins.input", side_effect=["x", "wrong", "z"]), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_fill_in_the_blanks_quiz(questions, answers, name=None)
            text = out.getvalue()
            self.assertIn("Total questions : 3", text)
            self.assertIn("INCORRECT!", text)


    def test_get_option_text_one_iteration_match(self):
        if not hasattr(mcq_mod, "_get_option_text"):
            self.skipTest("_get_option_text not found in mcq.py")
        options = ["A. Apple", "B. Banana", "C. Cat"]
        self.assertEqual(mcq_mod._get_option_text(options, "B"), "B. Banana")

    def test_get_option_text_multiple_iterations_no_match(self):
        if not hasattr(mcq_mod, "_get_option_text"):
            self.skipTest("_get_option_text not found in mcq.py")
        options = ["A. Apple", "B. Banana", "C. Cat"]
        self.assertIn("D (option text not found)", mcq_mod._get_option_text(options, "D"))


    def test_show_all_mcq_answers_zero_iteration(self):
        if not hasattr(mcq_mod, "show_all_mcq_answers") or not hasattr(mcq_mod, "ALL_QUIZ_DATA"):
            self.skipTest("show_all_mcq_answers / ALL_QUIZ_DATA not found in mcq.py")
        with patch.object(mcq_mod, "ALL_QUIZ_DATA", []), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.show_all_mcq_answers()
            self.assertIn("ANSWER KEY", out.getvalue())

    def test_show_all_mcq_answers_one_iteration(self):
        if not hasattr(mcq_mod, "show_all_mcq_answers") or not hasattr(mcq_mod, "ALL_QUIZ_DATA"):
            self.skipTest("show_all_mcq_answers / ALL_QUIZ_DATA not found in mcq.py")
        data = [{"question": "Q?", "options": ["A. X", "B. Y"], "answer": "A"}]
        with patch.object(mcq_mod, "ALL_QUIZ_DATA", data), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.show_all_mcq_answers()
            text = out.getvalue()
            self.assertIn("Q1. Q?", text)
            self.assertIn("Correct answer: A", text)


    def test_show_all_mcq_answers_multiple_iterations(self):
        if not hasattr(mcq_mod, "show_all_mcq_answers") or not hasattr(mcq_mod, "ALL_QUIZ_DATA"):
            self.skipTest("show_all_mcq_answers / ALL_QUIZ_DATA not found in mcq.py")
        data = [
            {"question": "Q1?", "options": ["A. X", "B. Y"], "answer": "A"},
            {"question": "Q2?", "options": ["A. M", "B. N"], "answer": "B"},
        ]
        with patch.object(mcq_mod, "ALL_QUIZ_DATA", data), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.show_all_mcq_answers()
            self.assertIn("Q2. Q2?", out.getvalue())

    
    def test_show_all_fill_in_answers_zero_iteration(self):
        if not hasattr(mcq_mod, "show_all_fill_in_answers") or not hasattr(mcq_mod, "FILL_IN_QUIZ_DATA"):
            self.skipTest("show_all_fill_in_answers / FILL_IN_QUIZ_DATA not found in mcq.py")
        with patch.object(mcq_mod, "FILL_IN_QUIZ_DATA", []), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.show_all_fill_in_answers()
            self.assertIn("ANSWER KEY", out.getvalue())


    def test_show_all_fill_in_answers_one_iteration(self):
        if not hasattr(mcq_mod, "show_all_fill_in_answers") or not hasattr(mcq_mod, "FILL_IN_QUIZ_DATA"):
            self.skipTest("show_all_fill_in_answers / FILL_IN_QUIZ_DATA not found in mcq.py")
        data = [{"question": "Capital of France: ____", "answer": "Paris|paris"}]
        with patch.object(mcq_mod, "FILL_IN_QUIZ_DATA", data), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.show_all_fill_in_answers()
            self.assertIn("Accepted answer(s): Paris / paris", out.getvalue())


    def test_show_all_fill_in_answers_multiple_iterations(self):
        if not hasattr(mcq_mod, "show_all_fill_in_answers") or not hasattr(mcq_mod, "FILL_IN_QUIZ_DATA"):
            self.skipTest("show_all_fill_in_answers / FILL_IN_QUIZ_DATA not found in mcq.py")
        data = [
            {"question": "1+1=____", "answer": "2"},
            {"question": "2+2=____", "answer": "4"},
            {"question": "3+3=____", "answer": "6"},
        ]
        with patch.object(mcq_mod, "FILL_IN_QUIZ_DATA", data), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.show_all_fill_in_answers()
            self.assertIn("Q3.", out.getvalue())


    def test_skipquiz_zero_iteration(self):
        with patch("builtins.input", side_effect=[]), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_quiz_with_skip([], [], [], name=None)
            text = out.getvalue()
            self.assertIn("Total questions : 0", text)
            self.assertIn("Skipped         : 0", text)


    def test_skipquiz_one_iteration_skip(self):
        questions = ["Pick A?"]
        options = [["A. Yes", "B. No", "C. Maybe", "D. Later"]]
        answers = ["A"]
        with patch("builtins.input", side_effect=[""]), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_quiz_with_skip(questions, options, answers, name=None)
            text = out.getvalue()
            self.assertIn("Question skipped.", text)
            self.assertIn("Answered        : 0", text)
            self.assertIn("Your score is   : 0%", text)


    def test_skipquiz_multiple_iterations_mixed(self):
        questions = ["Q1?", "Q2?", "Q3?"]
        options = [
            ["A. X", "B. Y", "C. Z", "D. W"],
            ["A. X", "B. Y", "C. Z", "D. W"],
            ["A. X", "B. Y", "C. Z", "D. W"],
        ]
        answers = ["A", "B", "C"]
        user_inputs = ["K", "A", "S", "D"]

        with patch("builtins.input", side_effect=user_inputs), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.take_quiz_with_skip(questions, options, answers, name=None)
            text = out.getvalue()
            self.assertIn("Invalid input", text)
            self.assertIn("Skipped         : 1", text)
            self.assertIn("Total questions : 3", text)

    
    def test_age_based_quiz_filtered_empty(self):
        data = [{"question": "Hard Q", "options": ["A.1","B.2","C.3","D.4"], "answer":"A", "difficulty":"Hard"}]
        with patch("builtins.input", side_effect=["Dev", "9"]), patch("sys.stdout", new_callable=io.StringIO) as out:
            mcq_mod.age_based_quiz(data)
            self.assertIn("No questions available for this age group.", out.getvalue())


    def test_age_based_quiz_one_question(self):
        data = [{"question": "Easy Q", "options": ["A.1","B.2","C.3","D.4"], "answer":"A", "difficulty":"Easy"}]
        with patch("builtins.input", side_effect=["Dev", "9", "1"]), \
             patch("mcq.take_quiz") as fake_take_quiz, \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.age_based_quiz(data)
            self.assertTrue(fake_take_quiz.called)


    def test_age_based_quiz_multiple_questions(self):
        data = [
            {"question": "Easy1", "options": ["A.1","B.2","C.3","D.4"], "answer":"A", "difficulty":"Easy"},
            {"question": "Easy2", "options": ["A.1","B.2","C.3","D.4"], "answer":"B", "difficulty":"Easy"},
            {"question": "Easy3", "options": ["A.1","B.2","C.3","D.4"], "answer":"C", "difficulty":"Easy"},
        ]
        with patch("builtins.input", side_effect=["Dev", "9", "2"]), \
             patch("mcq.take_quiz") as fake_take_quiz, \
             patch("sys.stdout", new_callable=io.StringIO):
            mcq_mod.age_based_quiz(data)
            self.assertTrue(fake_take_quiz.called)

    
    def test_today_str_format(self):
        s = att_mod._today_str()
        self.assertEqual(10, len(s))
        self.assertEqual("-", s[4])
        self.assertEqual("-", s[7])


    def test_load_attempts_file_missing(self):
        with patch("os.path.exists", return_value=False):
            self.assertEqual({}, att_mod._load_attempts())


    def test_record_quiz_attempt_creates_entry(self):
        fake_data = {}
        with patch.object(att_mod, "_load_attempts", return_value=fake_data), \
             patch.object(att_mod, "_save_attempts") as save_mock:
            att_mod.record_quiz_attempt("Dev")
            self.assertTrue(save_mock.called)


if __name__ == "__main__":
    unittest.main()

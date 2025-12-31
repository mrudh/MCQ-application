import unittest
import io
from contextlib import ExitStack
from unittest.mock import patch
import mcq  
import questions_viewer 
import wrong_answer_quiz  


topic_quiz = mcq


class TestQuizConditionTesting(unittest.TestCase):
    
    def _run_with_io(self, func, inputs, patch_take_quiz=False):
        
        fake_out = io.StringIO()

        with ExitStack() as stack:
            stack.enter_context(patch("builtins.input", side_effect=inputs))
            stack.enter_context(patch("sys.stdout", new=fake_out))

            mock_take_quiz = None
            if patch_take_quiz:
                mock_take_quiz = stack.enter_context(
                    patch.object(topic_quiz, "take_quiz", create=True)
                )

            func()
            return fake_out.getvalue(), mock_take_quiz

    
    def test_01_quiz_by_topic_no_topics(self):
        data = []
        out, _ = self._run_with_io(lambda: topic_quiz.quiz_by_topic(data), inputs=[])
        self.assertIn("No topics found", out)


    def test_02_quiz_by_topic_topics_exist_valid_topic(self):
        data = [
            {"topic": "Math", "question": "Q1", "options": ["A)1", "B)2", "C)3", "D)4"], "answer": "A"},
            {"topic": "Sci",  "question": "Q2", "options": ["A)a", "B)b", "C)c", "D)d"], "answer": "B"},
        ]
        out, mock_take_quiz = self._run_with_io(
            lambda: topic_quiz.quiz_by_topic(data),
            inputs=["1"],
            patch_take_quiz=True,
        )
        self.assertIn("Select a topic:", out)
        self.assertTrue(mock_take_quiz.called)


    def test_03_quiz_by_topic_topics_exist_invalid_topic_number(self):
        data = [{"topic": "Math", "question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        out, mock_take_quiz = self._run_with_io(
            lambda: topic_quiz.quiz_by_topic(data),
            inputs=["99"],
            patch_take_quiz=True,
        )
        self.assertIn("Invalid topic selection", out)
        self.assertFalse(mock_take_quiz.called)


    def test_04_quiz_by_topic_topics_exist_non_int_input(self):
        data = [{"topic": "Math", "question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        out, mock_take_quiz = self._run_with_io(
            lambda: topic_quiz.quiz_by_topic(data),
            inputs=["abc"],
            patch_take_quiz=True,
        )
        self.assertIn("Invalid input", out)
        self.assertFalse(mock_take_quiz.called)

    
    def test_05_viewer_choose_mcq_only_mcq_nonempty(self):
        with patch.object(questions_viewer, "show_all_mcq_questions_only") as mcq, \
             patch.object(questions_viewer, "show_all_fill_in_questions_only") as fill, \
             patch("builtins.input", side_effect=["1", "0"]):
            questions_viewer.questions_viewer_menu()
            self.assertTrue(mcq.called)
            self.assertFalse(fill.called)


    def test_06_viewer_choose_mcq_only_mcq_empty(self):
        with patch.object(questions_viewer, "show_all_mcq_questions_only") as mcq, \
             patch("builtins.input", side_effect=["1", "0"]):
            questions_viewer.questions_viewer_menu()
            self.assertTrue(mcq.called)


    def test_07_viewer_choose_fill_only_fill_nonempty(self):
        with patch.object(questions_viewer, "show_all_fill_in_questions_only") as fill, \
             patch("builtins.input", side_effect=["2", "0"]):
            questions_viewer.questions_viewer_menu()
            self.assertTrue(fill.called)


    def test_08_viewer_choose_fill_only_fill_empty(self):
        with patch.object(questions_viewer, "show_all_fill_in_questions_only") as fill, \
             patch("builtins.input", side_effect=["2", "0"]):
            questions_viewer.questions_viewer_menu()
            self.assertTrue(fill.called)


    def test_09_viewer_choose_all_both_nonempty(self):
        with patch.object(questions_viewer, "show_all_questions_only") as allq, \
             patch("builtins.input", side_effect=["3", "0"]):
            questions_viewer.questions_viewer_menu()
            self.assertTrue(allq.called)


    def test_10_viewer_choose_all_mcq_only_available(self):
        with patch.object(questions_viewer, "show_all_questions_only") as allq, \
             patch("builtins.input", side_effect=["3", "0"]):
            questions_viewer.questions_viewer_menu()
            self.assertTrue(allq.called)


    def test_11_viewer_choose_all_fill_only_available(self):
        with patch.object(questions_viewer, "show_all_questions_only") as allq, \
             patch("builtins.input", side_effect=["3", "0"]):
            questions_viewer.questions_viewer_menu()
            self.assertTrue(allq.called)


    def test_12_viewer_invalid_menu_choice(self):
        fake_out = io.StringIO()
        with patch("sys.stdout", new=fake_out), patch("builtins.input", side_effect=["9", "0"]):
            questions_viewer.questions_viewer_menu()
        self.assertIn("Invalid choice", fake_out.getvalue())


    def test_13_viewer_back(self):
        with patch("builtins.input", side_effect=["0"]):
            questions_viewer.questions_viewer_menu()

    
    def test_14_wrong_mode_no_mcq_questions_available(self):
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", [], create=True), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("No questions available", fake_out.getvalue())


    def test_15_wrong_mode_available_name_provided(self):
        one_q = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", one_q, create=True), \
             patch("builtins.input", side_effect=["1", "B"]), \
             patch("sys.stdout", new=fake_out), \
             patch.object(wrong_answer_quiz, "load_scores", return_value=[], create=True), \
             patch.object(wrong_answer_quiz, "save_scores", create=True) as save_scores:
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
            self.assertTrue(save_scores.called)


    def test_16_wrong_mode_available_name_skipped(self):
        one_q = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", one_q, create=True), \
             patch("builtins.input", side_effect=["", "1", "B"]), \
             patch.object(wrong_answer_quiz, "save_scores", create=True) as save_scores:
            wrong_answer_quiz.take_wrong_answer_quiz(name=None)
            self.assertFalse(save_scores.called)


    def test_17_wrong_mode_count_valid(self):
        qs = [
            {"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"},
            {"question": "Q2", "options": ["A)1","B)2","C)3","D)4"], "answer": "B"},
        ]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["2", "C", "D"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("WRONG-ANSWER TRAINING MODE", fake_out.getvalue())


    def test_18_wrong_mode_count_out_of_range_then_fixed(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["99", "1", "B"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("Please enter a number between 1 and 1", fake_out.getvalue())


    def test_19_wrong_mode_count_non_integer_then_fixed(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["abc", "1", "B"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("Please enter a valid number", fake_out.getvalue())


    def test_20_wrong_mode_guess_valid_avoids_real_answer(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["1", "B"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("successfully avoided", fake_out.getvalue())


    def test_21_wrong_mode_guess_valid_picks_real_answer(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["1", "A"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("You chose the REAL correct answer", fake_out.getvalue())


    def test_22_wrong_mode_invalid_guess_then_fixed(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["1", "Z", "B"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("Please enter one of", fake_out.getvalue())


    def test_23_wrong_mode_save_score_name_provided(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["1", "B"]), \
             patch.object(wrong_answer_quiz, "load_scores", return_value=[], create=True), \
             patch.object(wrong_answer_quiz, "save_scores", create=True) as save_scores:
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
            self.assertTrue(save_scores.called)


    def test_24_wrong_mode_no_save_name_skipped(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["", "1", "B"]), \
             patch.object(wrong_answer_quiz, "save_scores", create=True) as save_scores:
            wrong_answer_quiz.take_wrong_answer_quiz(name=None)
            self.assertFalse(save_scores.called)

    
    def test_25_viewer_mcq_unknown_topic_difficulty(self):
        mcq_data = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(questions_viewer, "ALL_QUIZ_DATA", mcq_data, create=True), \
             patch("sys.stdout", new=fake_out):
            questions_viewer.show_all_mcq_questions_only()
        self.assertIn("Unknown topic", fake_out.getvalue())
        self.assertIn("Unknown difficulty", fake_out.getvalue())


    def test_26_viewer_fill_unknown_topic_difficulty(self):
        fill_data = [{"question": "Fill ___", "answer": "X"}]
        fake_out = io.StringIO()
        with patch.object(questions_viewer, "FILL_IN_QUIZ_DATA", fill_data, create=True), \
             patch("sys.stdout", new=fake_out):
            questions_viewer.show_all_fill_in_questions_only()
        self.assertIn("Unknown topic", fake_out.getvalue())
        self.assertIn("Unknown difficulty", fake_out.getvalue())

   
    def test_27_quiz_by_topic_valid_with_hard_questions(self):
        data = [{"topic": "Math", "difficulty": "hard", "question": "Q1",
                 "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        out, mock_take_quiz = self._run_with_io(
            lambda: topic_quiz.quiz_by_topic(data),
            inputs=["1"],
            patch_take_quiz=True,
        )
        self.assertTrue(mock_take_quiz.called)


    def test_28_quiz_by_topic_valid_with_easy_questions(self):
        data = [{"topic": "Math", "difficulty": "easy", "question": "Q1",
                 "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        out, mock_take_quiz = self._run_with_io(
            lambda: topic_quiz.quiz_by_topic(data),
            inputs=["1"],
            patch_take_quiz=True,
        )
        self.assertTrue(mock_take_quiz.called)

    
    def test_29_wrong_mode_multiple_questions_run(self):
        qs = [
            {"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"},
            {"question": "Q2", "options": ["A)1","B)2","C)3","D)4"], "answer": "B"},
            {"question": "Q3", "options": ["A)1","B)2","C)3","D)4"], "answer": "C"},
        ]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["3", "D", "D", "D"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("Total questions", fake_out.getvalue())


    def test_30_wrong_mode_single_question_run(self):
        qs = [{"question": "Q1", "options": ["A)1","B)2","C)3","D)4"], "answer": "A"}]
        fake_out = io.StringIO()
        with patch.object(wrong_answer_quiz, "ALL_QUIZ_DATA", qs, create=True), \
             patch("builtins.input", side_effect=["1", "B"]), \
             patch("sys.stdout", new=fake_out):
            wrong_answer_quiz.take_wrong_answer_quiz(name="X")
        self.assertIn("Total questions", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()

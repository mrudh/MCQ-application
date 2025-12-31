import unittest
from unittest.mock import patch, call
import wrong_answer_quiz as mod


class TestWrongAnswerQuiz(unittest.TestCase):
    def setUp(self):
        
        self.quiz_data = [
            {
                "question": "Q1?",
                "options": ["A. a", "B. b", "C. c", "D. d"],
                "answer": "A",  
            },
            {
                "question": "Q2?",
                "options": ["A. a2", "B. b2", "C. c2", "D. d2"],
                "answer": "B",  
            },
        ]

    

    @patch.object(mod, "ALL_QUIZ_DATA", [])
    @patch("builtins.print")
    def test_no_questions_available(self, p_print):
        mod.take_wrong_answer_quiz()
        self.assertTrue(any("No questions available" in str(c) for c in p_print.call_args_list))


    def _no_shuffle(self, xs):
        return None

    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_name_none_does_not_save(self, _):
        mod.ALL_QUIZ_DATA[:] = self.quiz_data
        inputs = ["", "1", "B"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch.object(mod, "load_scores") as p_load, \
             patch.object(mod, "save_scores") as p_save:
            mod.take_wrong_answer_quiz(name=None)

            p_load.assert_not_called()
            p_save.assert_not_called()

    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_name_provided_saves_score(self, _):
        mod.ALL_QUIZ_DATA[:] = self.quiz_data
        inputs = ["1", "B"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch.object(mod, "load_scores", return_value=[]) as p_load, \
             patch.object(mod, "save_scores") as p_save:
            mod.take_wrong_answer_quiz(name="Alice")

            p_load.assert_called_once()
            p_save.assert_called_once()
            saved_arg = p_save.call_args[0][0]  
            self.assertEqual(saved_arg[-1]["name"], "Alice")
            self.assertEqual(saved_arg[-1]["score"], 100)

    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_name_prompted_nonblank_saves_score(self, _):
        mod.ALL_QUIZ_DATA[:] = self.quiz_data
        inputs = ["Bob", "1", "A"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch.object(mod, "load_scores", return_value=[]) as p_load, \
             patch.object(mod, "save_scores") as p_save:
            mod.take_wrong_answer_quiz(name=None)

            p_load.assert_called_once()
            p_save.assert_called_once()
            saved_arg = p_save.call_args[0][0]
            self.assertEqual(saved_arg[-1]["name"], "Bob")
            self.assertEqual(saved_arg[-1]["score"], 0)


    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_count_value_error_then_valid(self, _):
        mod.ALL_QUIZ_DATA[:] = self.quiz_data
        inputs = ["1", "x", "1", "B"]  
        inputs = ["x", "1", "B"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch("builtins.print") as p_print:
            mod.take_wrong_answer_quiz(name="Alice")
            self.assertTrue(any("Please enter a valid number." in str(c) for c in p_print.call_args_list))

    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_count_range_error_then_valid(self, _):
        mod.ALL_QUIZ_DATA[:] = self.quiz_data
        inputs = ["999", "1", "B"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch("builtins.print") as p_print:
            mod.take_wrong_answer_quiz(name="Alice")

            self.assertTrue(any("Please enter a number between" in str(c) for c in p_print.call_args_list))


    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_answer_needs_strip_upper(self, _):
        mod.ALL_QUIZ_DATA[:] = [
            {
                "question": "Q?",
                "options": ["A. a", "B. b", "C. c", "D. d"],
                "answer": "  a  ",  
            }
        ]

        
        inputs = ["1", "B"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch("builtins.print") as p_print:
            mod.take_wrong_answer_quiz(name="Alice")
            self.assertTrue(any("Real correct answer was: A" in str(c) for c in p_print.call_args_list))


    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_guess_invalid_then_valid(self, _):
        mod.ALL_QUIZ_DATA[:] = self.quiz_data
        inputs = ["1", "Z", "B"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch("builtins.print") as p_print:
            mod.take_wrong_answer_quiz(name="Alice")

            self.assertTrue(any("Please enter one of: A, B, C, or D." in str(c) for c in p_print.call_args_list))


    @patch.object(mod, "ALL_QUIZ_DATA", new_callable=lambda: [])
    def test_count_equals_total(self, _):
        mod.ALL_QUIZ_DATA[:] = self.quiz_data  
        inputs = ["2", "B", "B"]

        with patch("builtins.input", side_effect=inputs), \
             patch("random.shuffle", side_effect=self._no_shuffle), \
             patch("builtins.print") as p_print:
            mod.take_wrong_answer_quiz(name="Alice")
            self.assertTrue(any("Mode score" in str(c) and "1 / 2" in str(c) for c in p_print.call_args_list))


if __name__ == "__main__":
    unittest.main()

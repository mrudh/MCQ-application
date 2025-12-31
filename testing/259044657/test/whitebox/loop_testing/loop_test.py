import unittest
from unittest.mock import patch
import random
import wrong_answer_quiz as app


class TestLoopWrongAnswerQuiz(unittest.TestCase):
    
    def test_wrong_mode_zero_iteration(self):
        with patch.object(app, "ALL_QUIZ_DATA", []), \
             patch("builtins.print") as mock_print:
            app.take_wrong_answer_quiz(name="Ali")
            printed = " ".join(str(args[0]) for args, _ in mock_print.call_args_list if args)
            self.assertIn("No questions available.", printed)

    
    def test_wrong_mode_one_iteration(self):
        one_q = [
            {
                "question": "Q1?",
                "options": ["A. a", "B. b", "C. c", "D. d"],
                "answer": "A",
                "topic": "T1",
                "difficulty": "Easy",
            }
        ]

       
        user_inputs = iter(["1", "B"]) 

        with patch.object(app, "ALL_QUIZ_DATA", one_q), \
             patch.object(app, "load_scores", return_value=[]), \
             patch.object(app, "save_scores") as mock_save, \
             patch("builtins.input", side_effect=lambda _: next(user_inputs)), \
             patch("builtins.print") as mock_print, \
             patch.object(random, "shuffle", side_effect=lambda x: None):
            app.take_wrong_answer_quiz(name="Ali")

            
            mock_save.assert_called_once()

            printed = "\n".join(str(args[0]) for args, _ in mock_print.call_args_list if args)
            self.assertIn("WRONG-ANSWER TRAINING MODE", printed)
            self.assertIn("Total questions : 1", printed)

    
    def test_wrong_mode_multiple_iterations(self):
        three_q = [
            {
                "question": "Q1?",
                "options": ["A. a", "B. b", "C. c", "D. d"],
                "answer": "A",
                "topic": "T1",
                "difficulty": "Easy",
            },
            {
                "question": "Q2?",
                "options": ["A. a2", "B. b2", "C. c2", "D. d2"],
                "answer": "B",
                "topic": "T1",
                "difficulty": "Medium",
            },
            {
                "question": "Q3?",
                "options": ["A. a3", "B. b3", "C. c3", "D. d3"],
                "answer": "C",
                "topic": "T2",
                "difficulty": "Hard",
            },
        ]

        
        user_inputs = iter(["3", "B", "C", "D"])

        with patch.object(app, "ALL_QUIZ_DATA", three_q), \
             patch.object(app, "load_scores", return_value=[]), \
             patch.object(app, "save_scores") as mock_save, \
             patch("builtins.input", side_effect=lambda _: next(user_inputs)), \
             patch("builtins.print") as mock_print, \
             patch.object(random, "shuffle", side_effect=lambda x: None):
            app.take_wrong_answer_quiz(name="Ali")

            
            mock_save.assert_called_once()
            printed = "\n".join(str(args[0]) for args, _ in mock_print.call_args_list if args)
            self.assertIn("Total questions : 3", printed)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

import certification_quiz


class TestCertificationExam(unittest.TestCase):
    
    def setUp(self):
        self.sample_quiz = [
            {
                "question": "2+2=?",
                "options": ["A. 3", "B. 4", "C. 5", "D. 6"],
                "answer": "B"
            }
        ]

    @patch("builtins.print")
    def test_quiz_data_missing_single(self, mock_print):
        with patch.object(certification_quiz, "ALL_QUIZ_DATA", []):
            result = certification_quiz.run_certification_exam("Alice")

        self.assertIsNone(result)
        mock_print.assert_any_call("No questions available for certification.")

    @patch("builtins.print")
    def test_candidate_name_empty_single(self, mock_print):
        with patch.object(certification_quiz, "ALL_QUIZ_DATA", self.sample_quiz):
            result = certification_quiz.run_certification_exam("   ")

        self.assertIsNone(result)
        mock_print.assert_any_call("Name cannot be empty for certification.")

    @patch("builtins.print")
    def test_attempts_exhausted_single(self, mock_print):
        with patch.object(certification_quiz, "ALL_QUIZ_DATA", self.sample_quiz), \
             patch.object(certification_quiz, "can_attempt_cert_quiz", return_value=(False, 0)):

            result = certification_quiz.run_certification_exam("Bob")

        self.assertIsNone(result)
        mock_print.assert_any_call("\nYou have used all certification attempts for today.")
        mock_print.assert_any_call("Please try again tomorrow.")

    
    @patch("builtins.input", return_value="")
    @patch("builtins.print")
    def test_run_exam_timed(self, mock_print, _):
        with patch.object(certification_quiz, "ALL_QUIZ_DATA", self.sample_quiz), \
             patch.object(certification_quiz, "can_attempt_cert_quiz", return_value=(True, 1)), \
             patch.object(certification_quiz, "record_cert_attempt"), \
             patch.object(certification_quiz, "load_scores", return_value=[]), \
             patch.object(certification_quiz, "save_scores"), \
             patch.object(certification_quiz, "_add_cert_result"), \
             patch("certification_quiz.timed_quiz", return_value="B", create=True):

            result = certification_quiz.run_certification_exam(
                "Alice",
                pass_mark=70,
                timed=True,
                time_per_question=5
            )

        self.assertIsNone(result)

    
    @patch("builtins.input", side_effect=["", "B"])
    @patch("builtins.print")
    def test_run_exam_not_timed(self, mock_print, _):
        with patch.object(certification_quiz, "ALL_QUIZ_DATA", self.sample_quiz), \
             patch.object(certification_quiz, "can_attempt_cert_quiz", return_value=(True, 1)), \
             patch.object(certification_quiz, "record_cert_attempt"), \
             patch.object(certification_quiz, "load_scores", return_value=[]), \
             patch.object(certification_quiz, "save_scores"), \
             patch.object(certification_quiz, "_add_cert_result"):

            result = certification_quiz.run_certification_exam(
                "Alice",
                pass_mark=70,
                timed=False
            )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

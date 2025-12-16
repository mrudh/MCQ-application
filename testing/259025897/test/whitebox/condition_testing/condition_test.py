import io
import sys
import unittest
from unittest.mock import patch
import mcq
import assessment


class TestTakeQuizConditions(unittest.TestCase):

# Condition testing for take_quiz
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("builtins.input", side_effect=["A"])
    def test_take_quiz_untimed_correct_named(
        self, mock_input, mock_print_results, mock_load, mock_save
    ):
# timed = False, guess == answer, name not None
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq.take_quiz(questions, options, answers, name="Alice", timed=False)

        mock_print_results.assert_called_once()
        mock_load.assert_called_once()
        mock_save.assert_called_once()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores")
    @patch("mcq.print_results")
    @patch("builtins.input", side_effect=["B"])
    def test_take_quiz_untimed_incorrect_anonymous(
        self, mock_input, mock_print_results, mock_load, mock_save
    ):
# timed = False, guess != answer, name is None
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq.take_quiz(questions, options, answers, name=None, timed=False)

        mock_print_results.assert_called_once()
        mock_load.assert_not_called()
        mock_save.assert_not_called()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("mcq.timed_quiz", return_value="C")
    def test_take_quiz_timed_no_timeout(
        self, mock_timed, mock_print_results, mock_load, mock_save
    ):
# timed = True, timed_quiz returns a letter (no timeout)
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["C"]

        mcq.take_quiz(questions, options, answers, name="Bob", timed=True)

        mock_timed.assert_called_once()
        mock_print_results.assert_called_once()
        mock_load.assert_called_once()
        mock_save.assert_called_once()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("mcq.timed_quiz", return_value=None)
    def test_take_quiz_timed_timeout(
        self, mock_timed, mock_print_results, mock_load, mock_save
    ):
# timed = True, timed_quiz returns None
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq.take_quiz(questions, options, answers, name="Eve", timed=True)

        mock_timed.assert_called_once()
        mock_print_results.assert_called_once()
        mock_load.assert_called_once()
        mock_save.assert_called_once()


class TestTimedQuizConditions(unittest.TestCase):
#Condition testing for non-Windows branch of timed_quiz

    @patch("select.select", return_value=([], [], []))
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_timed_quiz_timeout_non_windows(self, mock_stdout, mock_select):
        with patch.object(sys, "platform", "darwin"):
            result = mcq.timed_quiz("Enter:", timeout=0.01)
        self.assertIsNone(result)


    @patch("select.select", return_value=([sys.stdin], [], []))
    @patch("sys.stdin.readline", return_value="b\n")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_timed_quiz_input_non_windows(self, mock_stdout, mock_read, mock_select):
        with patch.object(sys, "platform", "darwin"):
            result = mcq.timed_quiz("Enter:", timeout=5)
        self.assertEqual("B", result)


class TestNegativeMarkConditions(unittest.TestCase):
#Condition testing for take_negative_mark_quiz
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", ""])
    def test_negative_mark_all_branches(self, mock_input, mock_load, mock_save):
        questions = ["Q1", "Q2", "Q3"]
        options = [
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
        ]
        answers = ["A", "A", "A"]

        mcq.take_negative_mark_quiz(
            questions, options, answers, name="Nina", neg_mark=0.25
        )

        mock_save.assert_called_once()


class TestChallengeModeConditions(unittest.TestCase):

    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq.timed_quiz", return_value=None)   # user never finishes second question
    @patch("builtins.input", side_effect=["3"])   # valid minutes between 2 and 5
    def test_challenge_valid_time_then_timeout(
        self, mock_input, mock_timed, mock_load, mock_save
    ):
        questions = ["Q1", "Q2"]
        options = [
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
        ]
        answers = ["A", "B"]

        mcq.take_quiz_challenge(questions, options, answers, name="TestUser")
        mock_load.assert_called_once()
        mock_save.assert_called_once()


    @patch("builtins.input", side_effect=["10", "abc", "3"])
    def test_challenge_rejects_invalid_minutes(self, mock_input):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        with patch("mcq.timed_quiz", return_value=None), \
             patch("mcq.load_scores", return_value=[]), \
             patch("mcq.save_scores"), \
             patch("time.time", side_effect=[0, 1000]):
            mcq.take_quiz_challenge(questions, options, answers, name="Dan")


class TestStreakModeConditions(unittest.TestCase):

#Condition testing for take_quiz_until_wrong

    @patch("mcq.random.shuffle", side_effect=lambda x: x)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B"])
    def test_streak_first_correct_second_wrong(
        self, mock_input, mock_load, mock_save, mock_shuffle
    ):
        questions = ["Q1", "Q2"]
        options = [
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
        ]
        answers = ["A", "A"]

        mcq.take_quiz_until_wrong(questions, options, answers, name="Sara")

        mock_save.assert_called_once()


    @patch("mcq.random.shuffle", side_effect=lambda x: x)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["", ""])
    def test_streak_empty_answer_branch(
        self, mock_input, mock_load, mock_save, mock_shuffle
    ):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq.take_quiz_until_wrong(questions, options, answers, name="Leo")
        mock_save.assert_called_once()


class TestLearningModeConditions(unittest.TestCase):
#Condition testing for learning_mode
    @patch(
        "builtins.input",
        side_effect=[
            "",
            "x",
            "q",
        ],
    )
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_learning_mode_quit_branch(self, mock_stdout, mock_input):
        questions = ["Q1"]
        answers = ["A"]

        mcq.learning_mode(questions, answers)

        out = mock_stdout.getvalue()
        self.assertIn("Cards reviewed", out)
        # because we quit immediately, total_seen should be 0
        self.assertIn("Cards reviewed : 0", out)



class TestAssessmentConditions(unittest.TestCase):

#Condition testing for assessment related functions

    @patch("assessment.save_custom_assessments")
    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("mcq.take_quiz")
    @patch(
        "builtins.input",
        side_effect=[
            "MyTest",
            "1",
            "Q1",
            "optA", "optB", "optC", "optD",
            "A",
            "n"
        ],
    )
    def test_create_assessment_not_taken_now(
        self, mock_input, mock_take_quiz, mock_load, mock_save
    ):
        assessment.create_assessment()
        mock_save.assert_called_once()
        mock_take_quiz.assert_not_called()


    @patch("assessment.load_custom_assessments", return_value=[])
    def test_list_assessments_none(self, mock_load):
# condition - print and return None if not assessments
        result = assessment.list_assessments()
        self.assertIsNone(result)


    @patch(
        "assessment.list_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    @patch("assessment.save_custom_assessments")
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "New Q",
            "oA", "oB", "oC", "oD",
            "A"
        ],
    )
    def test_add_question_valid(self, mock_input, mock_save, mock_list):
        assessment.add_question_to_assessment()
        mock_save.assert_called_once()


    @patch(
        "assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("assessment.save_custom_assessments")
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "1",
            "",
            "", "", "", "",
            ""
        ],
    )
    def test_edit_question_keep_existing(
        self, mock_input, mock_save, mock_list
    ):
        assessment.edit_question_in_assessment()
        mock_save.assert_called_once()


    @patch(
        "assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("assessment.save_custom_assessments")
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "1"
        ],
    )
    def test_delete_question_valid(self, mock_input, mock_save, mock_list):
        assessment.delete_question_from_assessment()
        mock_save.assert_called_once()


    @patch(
        "assessment.load_custom_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["1"])
    def test_view_questions_valid(self, mock_input, mock_stdout, mock_load):
        assessment.view_questions_in_assessment()
        out = mock_stdout.getvalue()
        self.assertIn("Assessment: A", out)
        self.assertIn("Q1", out)


if __name__ == "__main__":
    unittest.main()
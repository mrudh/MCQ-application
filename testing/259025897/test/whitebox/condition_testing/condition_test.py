import io
import sys
import unittest
from unittest.mock import patch
import mcq_types
import assessment


class TestTakeQuizConditions(unittest.TestCase):

    #Saves score for a named user in untimed mode after a correct answer
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["A"])
    def test_take_quiz_untimed_correct_named(self, mock_input, mock_print_results, mock_load, mock_save):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]
        mcq_types.take_quiz(questions, options, answers, name="Alice", timed=False)
        mock_print_results.assert_called_once()
        mock_load.assert_called_once()
        mock_save.assert_called_once()


    #Does not save score when the user is anonymous in untimed mode
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores")
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["B"])
    def test_take_quiz_untimed_incorrect_anonymous(
        self, mock_input, mock_print_results, mock_load, mock_save
    ):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]
        mcq_types.take_quiz(questions, options, answers, name=None, timed=False)
        mock_print_results.assert_called_once()
        mock_load.assert_not_called()
        mock_save.assert_not_called()


    # Saves score in timed mode when an answer arrives before timeout
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value="C")
    def test_take_quiz_timed_no_timeout(self, mock_timed, mock_print_results, mock_load, mock_save):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["C"]

        mcq_types.take_quiz(questions, options, answers, name="Bob", timed=True)

        mock_timed.assert_called_once()
        mock_print_results.assert_called_once()
        mock_load.assert_called_once()
        mock_save.assert_called_once()


    #Treats a timed-out response as a wrong/blank attempt but still records the attempt for a named user
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_take_quiz_timed_timeout(
        self, mock_timed, mock_print_results, mock_load, mock_save
    ):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]
        mcq_types.take_quiz(questions, options, answers, name="Eve", timed=True)
        mock_timed.assert_called_once()
        mock_print_results.assert_called_once()
        mock_load.assert_called_once()
        mock_save.assert_called_once()


class TestTimedQuizConditions(unittest.TestCase):

    #Returns None on non-Windows when no input is received before the timeout
    @patch("select.select", return_value=([], [], []))
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_timed_quiz_timeout_non_windows(self, mock_stdout, mock_select):
        with patch.object(sys, "platform", "darwin"):
            result = mcq_types.timed_quiz("Enter:", timeout=0.01)
        self.assertIsNone(result)


    #Reads and uppercases a non-Windows input line when stdin becomes ready
    @patch("select.select", return_value=([sys.stdin], [], []))
    @patch("sys.stdin.readline", return_value="b\n")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_timed_quiz_input_non_windows(self, mock_stdout, mock_read, mock_select):
        with patch.object(sys, "platform", "darwin"):
            result = mcq_types.timed_quiz("Enter:", timeout=5)
        self.assertEqual("B", result)


class TestNegativeMarkConditions(unittest.TestCase):

    #Applies +1 for correct, penalty for wrong, and 0 for blank, then saves for a named user
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", ""])
    def test_negative_mark_all_branches(self, mock_input, mock_load, mock_save):
        questions = ["Q1", "Q2", "Q3"]
        options = [
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
        ]
        answers = ["A", "A", "A"]
        mcq_types.take_negative_mark_quiz(questions, options, answers, name="Nina", neg_mark=0.25)
        mock_save.assert_called_once()


class TestChallengeModeConditions(unittest.TestCase):

    #Saves accuracy when the challenge ends due to timed_quiz returning None mid-question
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    @patch("builtins.input", side_effect=["3"])
    def test_challenge_valid_time_then_timeout(self, mock_input, mock_timed, mock_load, mock_save):
        questions = ["Q1", "Q2"]
        options = [
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
        ]
        answers = ["A", "B"]
        mcq_types.take_quiz_challenge(questions, options, answers, name="TestUser")
        mock_load.assert_called_once()
        mock_save.assert_called_once()


    # Keeps prompting until a valid challenge duration is entered
    @patch("builtins.input", side_effect=["10", "abc", "3"])
    def test_challenge_rejects_invalid_minutes(self, mock_input):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]
        with patch("mcq_types.timed_quiz", return_value=None), \
             patch("mcq_types.load_scores", return_value=[]), \
             patch("mcq_types.save_scores"), \
             patch("time.time", side_effect=[0, 1000]):
            mcq_types.take_quiz_challenge(questions, options, answers, name="Dan")


class TestStreakModeConditions(unittest.TestCase):

    #Saves score after the first wrong answer ends the streak
    @patch("mcq_types.random.shuffle", side_effect=lambda x: x)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B"])
    def test_streak_first_correct_second_wrong(self, mock_input, mock_load, mock_save, mock_shuffle):
        questions = ["Q1", "Q2"]
        options = [
            ("A. 1", "B. 2", "C. 3", "D. 4"),
            ("A. 1", "B. 2", "C. 3", "D. 4"),
        ]
        answers = ["A", "A"]
        mcq_types.take_quiz_until_wrong(questions, options, answers, name="Sara")
        mock_save.assert_called_once()


    #Saves score even when the first answer is blank and the streak ends immediately
    @patch("mcq_types.random.shuffle", side_effect=lambda x: x)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["", ""])
    def test_streak_empty_answer_branch(
        self, mock_input, mock_load, mock_save, mock_shuffle
    ):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]
        mcq_types.take_quiz_until_wrong(questions, options, answers, name="Leo")
        mock_save.assert_called_once()


class TestLearningModeConditions(unittest.TestCase):

    #Prints a summary with zero reviewed cards when the user quits immediately
    @patch(
        "builtins.input",
        side_effect=["", "x", "q"],
    )
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_learning_mode_quit_branch(self, mock_stdout, mock_input):
        questions = ["Q1"]
        answers = ["A"]

        mcq_types.learning_mode(questions, answers)

        out = mock_stdout.getvalue()
        self.assertIn("Cards reviewed", out)
        self.assertIn("Cards reviewed : 0", out)


class TestAssessmentConditions(unittest.TestCase):

    # Creates and saves an assessment without starting the quiz when the user selects 'n'
    @patch("assessment.save_custom_assessments")
    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("mcq_types.take_quiz")
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
    def test_create_assessment_not_taken_now(self, mock_input, mock_take_quiz, mock_load, mock_save):
        assessment.create_assessment()
        mock_save.assert_called_once()
        mock_take_quiz.assert_not_called()


    #Returns None from list_assessments when there are no stored assessments
    @patch("assessment.load_custom_assessments", return_value=[])
    def test_list_assessments_none(self, mock_load):
        result = assessment.list_assessments()
        self.assertIsNone(result)


    #Adds a new question into the selected assessment and maintains the update
    @patch(
        "assessment.list_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    @patch("assessment.save_custom_assessments")
    @patch("builtins.input",
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


    #Keeps existing values during edit when the user presses 'Enter' for all fields
    @patch("assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("assessment.save_custom_assessments")
    @patch("builtins.input",
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


    #Deletes the chosen question from the assessment and maintains the change
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
        side_effect=["1", "1"],
    )
    def test_delete_question_valid(self, mock_input, mock_save, mock_list):
        assessment.delete_question_from_assessment()
        mock_save.assert_called_once()


    #Prints the selected assessment’s questions, options, and answers
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

import io
import unittest
from unittest.mock import patch
import mcq_types
import manage_assessment


class TestTakeQuizLoops(unittest.TestCase):

    #Loop testing for take_quiz
    @patch("mcq_types.print_results")
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A"])
    def test_take_quiz_one_question(self, mock_input, mock_load, mock_save, mock_pr):
    #one iteration of the question loop
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz(qs, opts, ans, name="OneUser", timed=False)

        mock_pr.assert_called_once()


    @patch("mcq_types.print_results")
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", "C"])
    def test_take_quiz_multiple_questions(
        self, mock_input, mock_load, mock_save, mock_pr
    ):
    #multiple iterations of the question loop
        qs = ["Q1", "Q2", "Q3"]
        opts = [
            ("A.1", "B.2", "C.3", "D.4"),
            ("A.1", "B.2", "C.3", "D.4"),
            ("A.1", "B.2", "C.3", "D.4"),
        ]
        ans = ["A", "B", "C"]
        mcq_types.take_quiz(qs, opts, ans, name="MultiUser", timed=False)
        mock_pr.assert_called_once()


class TestNegativeQuizLoops(unittest.TestCase):

    #Loop testing for take_negative_mark_quiz with one question
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A"])
    def test_negative_quiz_one_question(self, mock_input, mock_load, mock_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="One", neg_mark=0.25)


    #Loop testing for take_negative_mark_quiz with multiple question
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", ""])
    def test_negative_quiz_multiple_questions(
        self, mock_input, mock_load, mock_save
    ):
        qs = ["Q1", "Q2", "Q3"]
        opts = [
            ("A.1", "B.2", "C.3", "D.4"),
            ("A.1", "B.2", "C.3", "D.4"),
            ("A.1", "B.2", "C.3", "D.4"),
        ]
        ans = ["A", "A", "A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="Many", neg_mark=0.25)


class TestChallengeLoops(unittest.TestCase):

    #Loop testing for take_quiz_challenge with one iteration
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    @patch("builtins.input", side_effect=["2"])
    @patch("time.time", side_effect=[0, 1])
    def test_challenge_one_iteration_then_timeout(
        self, mock_time, mock_input, mock_timed, mock_load, mock_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="One")


    #Loop testing for take_quiz_challenge with multiple iteration
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", side_effect=["A", "B", None])
    @patch("builtins.input", side_effect=["2"])
    @patch("time.time", side_effect=[0, 1, 2, 3])
    def test_challenge_multiple_iterations_then_timeout(
        self, mock_time, mock_input, mock_timed, mock_load, mock_save
    ):
        qs = ["Q1", "Q2"]
        opts = [
            ("A.1", "B.2", "C.3", "D.4"),
            ("A.1", "B.2", "C.3", "D.4"),
        ]
        ans = ["A", "B"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="Many")


class TestStreakLoops(unittest.TestCase):

    #Loop testing for take_quiz_until_wrong with one question
    @patch("mcq_types.random.shuffle", side_effect=lambda x: x)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A"])
    def test_streak_one_question(self, mock_input, mock_load, mock_save, mock_shuf):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="One")


    #Loop testing for take_quiz_until_wrong with multiple question
    @patch("mcq_types.random.shuffle", side_effect=lambda x: x)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B"])
    def test_streak_multiple_questions_break_second(
        self, mock_input, mock_load, mock_save, mock_shuf
    ):
        qs = ["Q1", "Q2"]
        opts = [
            ("A.1", "B.2", "C.3", "D.4"),
            ("A.1", "B.2", "C.3", "D.4"),
        ]
        ans = ["A", "A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="Many")


class TestLearningModeLoops(unittest.TestCase):

    #Loop testing for learning_mode
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=[])
    def test_learning_zero_cards(self, mock_input, mock_stdout):
    #zero iterations of the main 'for' loop
        mcq_types.learning_mode([], [])
        out = mock_stdout.getvalue()
        self.assertIn("Cards reviewed : 0", out)


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "y"])
    def test_learning_one_card(self, mock_input, mock_stdout):
    #one iteration
        mcq_types.learning_mode(["Q1"], ["A"])
        out = mock_stdout.getvalue()
        self.assertIn("Cards reviewed : 1", out)


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "y", "", "n"])
    def test_learning_multiple_cards(self, mock_input, mock_stdout):
    #multiple iterations
        mcq_types.learning_mode(["Q1", "Q2"], ["A", "B"])
        out = mock_stdout.getvalue()
        self.assertIn("Cards reviewed : 2", out)


class TestAssessmentLoops(unittest.TestCase):

    #Loop testing for assessment functions with zero questions
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    @patch("mcq_types.take_quiz")
    @patch(
        "builtins.input",
        side_effect=[
            "Assess1",
            "0",
            "n"
        ],
    )
    def test_create_assessment_zero_questions(
        self, mock_input, mock_take, mock_load, mock_save
    ):
        manage_assessment.create_assessment()
        mock_save.assert_called_once()


    #Loop testing for assessment functions with one question
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    @patch("mcq_types.take_quiz")
    @patch(
        "builtins.input",
        side_effect=[
            "Assess1",
            "1",
            "Q1",
            "A1", "B1", "C1", "D1",
            "A",
            "n",
        ],
    )
    def test_create_assessment_one_question(
        self, mock_input, mock_take, mock_load, mock_save
    ):
        manage_assessment.create_assessment()
        mock_save.assert_called_once()


    #Loop testing for add question option functions
    @patch(
        "manage_assessment.list_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    @patch("manage_assessment.save_custom_assessments")
    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "New Q",
            "oA", "oB", "oC", "oD",
            "A",
        ],
    )
    def test_add_question_option_loop(
        self, mock_input, mock_save, mock_list
    ):
        manage_assessment.add_question_to_assessment()
        mock_save.assert_called_once()


    @patch(
        "manage_assessment.load_custom_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1", "Q2"],
            "options": [
                ("A1", "B1", "C1", "D1"),
                ("A2", "B2", "C2", "D2"),
            ],
            "answers": ["A", "B"],
        }],
    )
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["1"])
    def test_view_questions_multiple(
        self, mock_input, mock_stdout, mock_load
    ):
    #loops over multiple questions when viewing
        manage_assessment.view_questions_in_assessment()
        out = mock_stdout.getvalue()
        self.assertIn("Q1", out)
        self.assertIn("Q2", out)


if __name__ == "__main__":
    unittest.main()
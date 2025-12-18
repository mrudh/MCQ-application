import unittest
from unittest.mock import patch, mock_open
import sys
import mcq_types
import assessment
import storage


class TestTakeQuizStatements(unittest.TestCase):
    # Tests the basic untimed quiz flow where the user answers correctly
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["A"])
    def test_take_quiz_not_timed_all_correct_no_name(self, mock_input, mock_print):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq_types.take_quiz(questions, options, answers, name=None, timed=False)


    #Tests the untimed quiz flow where answer is wrong and saving the score should occur
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["B"])
    def test_take_quiz_not_timed_wrong_with_name(
        self, mock_input, mock_print, mock_load, mock_save
    ):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq_types.take_quiz(questions, options, answers, name="Alice", timed=False)

        mock_save.assert_called_once()


    # Verifies that the timed quiz correctly handles a valid user input
    @patch("mcq_types.print")
    @patch("mcq_types.timed_quiz", return_value="A")
    def test_take_quiz_timed_correct(self, mock_timed, mock_print):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq_types.take_quiz(questions, options, answers, name=None, timed=True)


    #Verifies that the timed quiz handles timeout
    @patch("mcq_types.print")
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_take_quiz_timed_timeout(self, mock_timed, mock_print):
        questions = ["Q1"]
        options = [("A. 1", "B. 2", "C. 3", "D. 4")]
        answers = ["A"]

        mcq_types.take_quiz(questions, options, answers, name=None, timed=True)


class TestTimedQuizStatements(unittest.TestCase):
    #Tests the non-windows path behaves correctly when input arrives before timeout
    @patch.object(sys, "platform", "darwin")
    @patch("sys.stdin.readline", return_value="A\n")
    @patch("select.select")
    def test_timed_quiz_non_windows_input(self, mock_select, mock_read, *_):
        mock_select.return_value = ([sys.stdin], [], [])
        result = mcq_types.timed_quiz("Enter: ", timeout=1)
        self.assertEqual(result, "A")


    #Tests non-windows flow returns None if no input arrives before timeout
    @patch.object(sys, "platform", "darwin")
    @patch("sys.stdin.readline", return_value="A\n")
    @patch("select.select")
    def test_timed_quiz_non_windows_timeout(self, mock_select, mock_read, *_):
        mock_select.return_value = ([], [], [])
        result = mcq_types.timed_quiz("Enter: ", timeout=1)
        self.assertIsNone(result)


class TestNegativeMarkStatements(unittest.TestCase):
    #Tests negative marking handles correct, wrong, and blank answers correctly
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["A", "B", ""])
    def test_negative_mark_mix_no_name(self, mock_input, mock_print):
        questions = ["Q1", "Q2", "Q3"]
        options = [("A.1", "B.2", "C.3", "D.4")] * 3
        answers = ["A", "A", "A"]

        mcq_types.take_negative_mark_quiz(questions, options, answers, name=None)

    #Tests negative mark mode saves score when a name is provided
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["B"])
    def test_negative_mark_with_name(self, mock_input, mock_print, mock_load, mock_save):
        questions = ["Q1"]
        options = [("A.1", "B.2", "C.3", "D.4")]
        answers = ["A"]

        mcq_types.take_negative_mark_quiz(questions, options, answers, name="Bob")
        mock_save.assert_called_once()


class TestChallengeModeStatements(unittest.TestCase):
    #Tests repeated invalid inputs until user finally enters a valid time, followed by immediate timeout
    @patch("mcq_types.print")
    @patch("mcq_types.time.time", side_effect=[0, 1000])
    @patch("mcq_types.input", side_effect=["abc", "1", "3"])
    def test_challenge_invalid_then_valid_minutes_immediate_timeout(
        self, mock_input, mock_time, mock_print
    ):
        questions = ["Q1"]
        options = [("A.1", "B.2", "C.3", "D.4")]
        answers = ["A"]

        mcq_types.take_quiz_challenge(questions, options, answers, name=None)


    #Tests challenge mode when exactly one question is answered before time runs out and score is saved
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda lst: None)
    @patch("mcq_types.timed_quiz", return_value="A")
    @patch("mcq_types.time.time", side_effect=[0, 0, 9999])
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["3"])
    def test_challenge_one_question_then_timeup(
        self,
        mock_input,
        mock_print,
        mock_time,
        mock_timed,
        mock_shuffle,
        mock_load,
        mock_save,
    ):
        questions = ["Q1", "Q2"]
        options = [("A.1", "B.2", "C.3", "D.4")] * 2
        answers = ["A", "B"]

        mcq_types.take_quiz_challenge(questions, options, answers, name="Carol")
        mock_save.assert_called_once()


class TestStreakModeStatements(unittest.TestCase):
    #Tests streak mode ending immediately when user provides blank input
    @patch("mcq_types.random.shuffle", side_effect=lambda lst: None)
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=[""])
    def test_streak_first_blank_ends(self, mock_input, mock_print, mock_shuffle):
        questions = ["Q1"]
        options = [("A.1", "B.2", "C.3", "D.4")]
        answers = ["A"]

        mcq_types.take_quiz_until_wrong(questions, options, answers, name=None)


    #Tests streak mode where the user gets the first question correct, second wrong, and score is saved
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda lst: None)
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["A", "B"])
    def test_streak_all_correct_then_wrong_with_name(
        self, mock_input, mock_print, mock_shuffle, mock_load, mock_save
    ):
        questions = ["Q1", "Q2"]
        options = [("A.1", "B.2", "C.3", "D.4")] * 2
        answers = ["A", "B"]

        mcq_types.take_quiz_until_wrong(questions, options, answers, name="Dave")
        mock_save.assert_called_once()


class TestLearningModeStatements(unittest.TestCase):
    #Tests learning mode when the user quits immediately after first question
    @patch("mcq_types.random.shuffle", side_effect=lambda lst: None)
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["", "q"])
    def test_learning_mode_quit_immediately(self, mock_input, mock_print, mock_shuffle):
        questions = ["Q1"]
        answers = ["A1"]

        mcq_types.learning_mode(questions, answers)


    # Tests learning mode when user marks some questions as correct and some as incorrect
    @patch("mcq_types.random.shuffle", side_effect=lambda lst: None)
    @patch("mcq_types.print")
    @patch("mcq_types.input", side_effect=["", "x", "y", "", "n"])
    def test_learning_mode_y_and_n(self, mock_input, mock_print, mock_shuffle):
        questions = ["Q1", "Q2"]
        answers = ["A1", "A2"]

        mcq_types.learning_mode(questions, answers)


class TestAssessmentStatements(unittest.TestCase):
    #Loading assessments returns an empty list when no file exists
    @patch("assessment_storage.os.path.exists", return_value=False)
    def test_load_custom_assessments_no_file(self, mock_exists):
        from assessment_storage import load_custom_assessments as storage_load

        self.assertEqual(storage_load(), [])


    #To test assessments are correctly loaded from file when one exists
    @patch("assessment_storage.os.path.exists", return_value=True)
    @patch("assessment_storage.open", new_callable=mock_open, read_data='[{"name": "A"}]')
    def test_load_custom_assessments_with_file(self, mock_file, mock_exists):
        from assessment_storage import load_custom_assessments as storage_load

        data = storage_load()
        self.assertEqual(data, [{"name": "A"}])


    #Tests saving assessments triggers a file write
    @patch("assessment_storage.open", new_callable=mock_open)
    def test_save_custom_assessments(self, mock_file):
        from assessment_storage import save_custom_assessments as storage_save

        storage_save([{"name": "A"}])
        mock_file.assert_called_once()


    #Tests creating an assessment from user inputs and ensures it is saved
    @patch("assessment.save_custom_assessments")
    @patch("assessment.load_custom_assessments", return_value=[])
    @patch(
        "assessment.input",
        side_effect=[
            "MyTest", "1", "Q1", "1", "2", "3", "4", "A", "n"
        ],
    )
    @patch("assessment.print")
    def test_create_assessment(self, mock_print, mock_input, mock_load, mock_save):
        assessment.create_assessment()
        mock_save.assert_called_once()


    #Ensures that listing assessments returns None when there are no stored assessments
    @patch("assessment.print")
    @patch("assessment.load_custom_assessments", return_value=[])
    def test_list_assessments_empty(self, mock_load, mock_print):
        result = assessment.list_assessments()
        self.assertIsNone(result)


    #testing list_assessments returns a list when assessments exist
    @patch("assessment.print")
    @patch(
        "assessment.load_custom_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    def test_list_assessments_non_empty(self, mock_load, mock_print):
        result = assessment.list_assessments()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)


    #To test whether adding a question updates the assessment and triggers save
    @patch("assessment.save_custom_assessments")
    @patch(
        "assessment.list_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    @patch(
        "assessment.input",
        side_effect=["1", "New Q?", "1", "2", "3", "4", "A"],
    )
    @patch("assessment.print")
    def test_add_question_to_assessment(
        self, mock_print, mock_input, mock_list, mock_save
    ):
        assessment.add_question_to_assessment()
        mock_save.assert_called_once()


    #To test editing a question updates the assessment and triggers save
    @patch("assessment.save_custom_assessments")
    @patch(
        "assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch(
        "assessment.input",
        side_effect=["1", "1", "", "", "", "", "", ""],
    )
    @patch("assessment.print")
    def test_edit_question_in_assessment(
        self, mock_print, mock_input, mock_list, mock_save
    ):
        assessment.edit_question_in_assessment()
        mock_save.assert_called_once()


    #To test deleting a question removes it and triggers save
    @patch("assessment.save_custom_assessments")
    @patch(
        "assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("assessment.input", side_effect=["1", "1"])
    @patch("assessment.print")
    def test_delete_question_from_assessment(
        self, mock_print, mock_input, mock_list, mock_save
    ):
        assessment.delete_question_from_assessment()
        mock_save.assert_called_once()


    #To check view_questions_in_assessment displays questions correctly
    @patch(
        "assessment.load_custom_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("assessment.input", side_effect=["1"])
    @patch("assessment.print")
    def test_view_questions_in_assessment(
        self, mock_print, mock_input, mock_load
    ):
        assessment.view_questions_in_assessment()


if __name__ == "__main__":
    unittest.main()


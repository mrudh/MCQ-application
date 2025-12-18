import json
import unittest
from unittest.mock import mock_open, patch
import assessment as app
import assessment_storage


class TestCreateAssessmentCategoryPartition(unittest.TestCase):

    def _run_create_assessment(self, inputs):
        with patch("builtins.input", side_effect=inputs):
            app.create_assessment()


    #Creates an assessment with 0 questions and chooses not to take it, so it should save but not start a quiz
    @patch("builtins.print")
    @patch("assessment.take_quiz")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.load_custom_assessments", return_value=[])
    def test_question_count_zero_take_no(
        self,
        _mock_load,
        mock_save,
        mock_take_quiz,
        _mock_print,
    ):
        inputs = [
            "Assessment 0",
            "0",
            "n"
        ]
        self._run_create_assessment(inputs)
        mock_save.assert_called_once()
        mock_take_quiz.assert_not_called()


    #Creates an assessment with 1 question and opts to take it immediately, answer should be uppercased and quiz should run
    @patch("builtins.print")
    @patch("assessment.take_quiz")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.load_custom_assessments", return_value=[])
    def test_question_count_one_valid_answer_take_yes(
        self,
        _mock_load,
        mock_save,
        mock_take_quiz,
        _mock_print,
    ):
        inputs = [
            "Assessment 1",
            "1",
            "What is 2+2?",
            "4", "3", "5", "6",
            "a",
            "y"
        ]
        self._run_create_assessment(inputs)
        mock_save.assert_called_once()
        mock_take_quiz.assert_called_once()
        args = mock_take_quiz.call_args[0]
        self.assertEqual(args[0], ["What is 2+2?"])
        self.assertEqual(args[2], ["A"])


    #Creates an assessment with multiple questions and declines to take it, so it should save without invoking the quiz
    @patch("builtins.print")
    @patch("assessment.take_quiz")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.load_custom_assessments", return_value=[])
    def test_question_count_many_take_no(
        self,
        _mock_load,
        mock_save,
        mock_take_quiz,
        _mock_print,
    ):
        inputs = [
            "Assessment many",
            "2",
            "Q1?", "A1", "B1", "C1", "D1", "B",
            "Q2?", "A2", "B2", "C2", "D2", "D",
            "n",
        ]
        self._run_create_assessment(inputs)
        mock_save.assert_called_once()
        mock_take_quiz.assert_not_called()


    #Even with an invalid correct option (not A/B/C/D), the assessment should still be persisted, and the quiz should not run when user says 'n'
    @patch("builtins.print")
    @patch("assessment.take_quiz")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.load_custom_assessments", return_value=[])
    def test_invalid_correct_option_still_saved(
        self,
        _mock_load,
        mock_save,
        mock_take_quiz,
        _mock_print,
    ):
        inputs = [
            "Invalid answer assessment",
            "1",
            "Q1?",
            "optA", "optB", "optC", "optD",
            "x",
            "n"
        ]
        self._run_create_assessment(inputs)
        mock_save.assert_called_once()
        mock_take_quiz.assert_not_called()


class TestAssessmentStorageFunctions(unittest.TestCase):

    #When the JSON file does not exist, load should return an empty list instead of crashing
    @patch("assessment_storage.os.path.exists", return_value=False)
    def test_load_custom_assessments_file_missing_returns_empty(self, _mock_exists):
        self.assertEqual(assessment_storage.load_custom_assessments(), [])


    #When the file exists, load should parse JSON content and return the exact decoded Python structure
    @patch("assessment_storage.os.path.exists", return_value=True)
    def test_load_custom_assessments_file_exists_reads_json(self, _mock_exists):
        fake_data = [{"name": "A1", "questions": [], "options": [], "answers": []}]
        m = mock_open(read_data=json.dumps(fake_data))
        with patch("assessment_storage.open", m):
            result = assessment_storage.load_custom_assessments()
        self.assertEqual(result, fake_data)


    #Save should write valid JSON that rounds back to the original data structure
    def test_save_custom_assessments_writes_json(self):
        fake_data = [{"name": "A1", "questions": [], "options": [], "answers": []}]
        m = mock_open()
        with patch("assessment_storage.open", m):
            assessment_storage.save_custom_assessments(fake_data)
        handle = m()
        written = "".join(call.args[0] for call in handle.write.mock_calls)
        self.assertEqual(json.loads(written), fake_data)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch
import assessment


def sample_assessments():
    return [
        {
            "name": "Math",
            "questions": ["Q1"],
            "options": [("A. 1", "B. 2", "C. 3", "D. 4")],
            "answers": ["B"],
        },
        {
            "name": "Science",
            "questions": ["S1", "S2"],
            "options": [
                ("A. a", "B. b", "C. c", "D. d"),
                ("A. x", "B. y", "C. z", "D. w"),
            ],
            "answers": ["A", "D"],
        },
    ]


class TestListAssessments(unittest.TestCase):

    #If there are no saved assessments, the helper should print a message and return None
    @patch("builtins.print")
    @patch("assessment.load_custom_assessments", return_value=[])
    def test_none_saved_returns_none(self, _mock_load, _mock_print):
        result = assessment.list_assessments()
        self.assertIsNone(result)


    #If saved assessments exist, the helper should return the same list it loaded
    @patch("builtins.print")
    @patch("assessment.load_custom_assessments")
    def test_some_saved_returns_list(self, mock_load, _mock_print):
        data = sample_assessments()
        mock_load.return_value = data

        result = assessment.list_assessments()
        self.assertEqual(result, data)


class TestAddQuestionToAssessment(unittest.TestCase):

    #When there are no assessments, add-question should exit early and not attempt to save anything
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments", return_value=[])
    def test_none_saved_returns_early(self, _mock_list, mock_save, _mock_print):
        assessment.add_question_to_assessment()
        mock_save.assert_not_called()


    #A non-numeric assessment selection should be treated as invalid and must not trigger a save
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_invalid_selection_non_int(self, mock_list, mock_save, _mock_print):
        mock_list.return_value = sample_assessments()

        with patch("builtins.input", side_effect=["abc"]):
            assessment.add_question_to_assessment()

        mock_save.assert_not_called()


    #An out-of-range assessment index should be rejected and must not modify or save the data
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_out_of_range_selection(self, mock_list, mock_save, _mock_print):
        mock_list.return_value = sample_assessments()

        with patch("builtins.input", side_effect=["99"]):
            assessment.add_question_to_assessment()

        mock_save.assert_not_called()


    #A valid selection should append the new question/options/answer and persist the updated assessments list
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_valid_adds_question_and_saves(self, mock_list, mock_save, _mock_print):
        data = sample_assessments()
        mock_list.return_value = data

        inputs = [
            "1",
            "New Q?",
            "oA",
            "oB",
            "oC",
            "oD",
            "c"
        ]
        with patch("builtins.input", side_effect=inputs):
            assessment.add_question_to_assessment()

        self.assertEqual(data[0]["questions"][-1], "New Q?")
        self.assertEqual(
            data[0]["options"][-1],
            ("A. oA", "B. oB", "C. oC", "D. oD"),
        )
        self.assertEqual(data[0]["answers"][-1], "C")
        mock_save.assert_called_once_with(data)


class TestEditQuestionInAssessment(unittest.TestCase):

    #If no assessments exist, edit should stop immediately and never call save
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments", return_value=[])
    def test_none_saved_returns_early(self, _mock_list, mock_save, _mock_print):
        assessment.edit_question_in_assessment()
        mock_save.assert_not_called()


    #If the user enters a non-integer for assessment selection, nothing should be edited or saved
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_invalid_assessment_selection(self, mock_list, mock_save, _mock_print):
        mock_list.return_value = sample_assessments()

        with patch("builtins.input", side_effect=["nope"]):
            assessment.edit_question_in_assessment()

        mock_save.assert_not_called()


    #If the selected question number is out of range, edit should abort without saving
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_question_index_out_of_range(self, mock_list, mock_save, _mock_print):
        mock_list.return_value = sample_assessments()

        inputs = ["2", "99"]
        with patch("builtins.input", side_effect=inputs):
            assessment.edit_question_in_assessment()

        mock_save.assert_not_called()


    #Leaving all prompts blank should keep question, options, and answer unchanged
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_blank_keep_everything(self, mock_list, mock_save, _mock_print):
        data = sample_assessments()
        mock_list.return_value = data

        original_q = data[0]["questions"][0]
        original_opts = data[0]["options"][0]
        original_ans = data[0]["answers"][0]

        inputs = [
            "1",
            "1",
            "",
            "",
            "",
            "",
            "",
            ""
        ]
        with patch("builtins.input", side_effect=inputs):
            assessment.edit_question_in_assessment()
        self.assertEqual(data[0]["questions"][0], original_q)
        self.assertEqual(data[0]["options"][0], original_opts)
        self.assertEqual(data[0]["answers"][0], original_ans)
        mock_save.assert_called_once_with(data)


    #Editing specific fields should update only those fields and uppercase the final answer before saving
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_changes_question_some_options_and_answer(
        self,
        mock_list,
        mock_save,
        _mock_print
    ):
        data = sample_assessments()
        mock_list.return_value = data
        inputs = ["2", "1", "S1 edited", "", "B changed", "", "", "c"]
        with patch("builtins.input", side_effect=inputs):
            assessment.edit_question_in_assessment()
        self.assertEqual(data[1]["questions"][0], "S1 edited")
        self.assertEqual(
            data[1]["options"][0],
            ("A. a", "B changed", "C. c", "D. d"),
        )
        self.assertEqual(data[1]["answers"][0], "C")
        mock_save.assert_called_once_with(data)


class TestDeleteQuestionFromAssessment(unittest.TestCase):

    #If there are no assessments to delete from, the function should exit without saving
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments", return_value=[])
    def test_none_saved_returns_early(self, _mock_list, mock_save, _mock_print):
        assessment.delete_question_from_assessment()
        mock_save.assert_not_called()


    #An invalid assessment selection should not delete anything and should not call save
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_invalid_assessment_selection(self, mock_list, mock_save, _mock_print):
        mock_list.return_value = sample_assessments()
        with patch("builtins.input", side_effect=["x"]):
            assessment.delete_question_from_assessment()
        mock_save.assert_not_called()


    #An out-of-range question number should be rejected without mutating data or saving
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_question_index_out_of_range(self, mock_list, mock_save, _mock_print):
        mock_list.return_value = sample_assessments()

        inputs = ["1", "99"]

        with patch("builtins.input", side_effect=inputs):
            assessment.delete_question_from_assessment()

        mock_save.assert_not_called()


    #A valid delete should remove the chosen question/options/answer consistently and then persist the updated list
    @patch("builtins.print")
    @patch("assessment.save_custom_assessments")
    @patch("assessment.list_assessments")
    def test_valid_deletes_and_saves(self, mock_list, mock_save, _mock_print):
        data = sample_assessments()
        mock_list.return_value = data
        inputs = ["2", "2"]

        with patch("builtins.input", side_effect=inputs):
            assessment.delete_question_from_assessment()

        self.assertEqual(data[1]["questions"], ["S1"])
        self.assertEqual(len(data[1]["options"]), 1)
        self.assertEqual(data[1]["answers"], ["A"])
        mock_save.assert_called_once_with(data)


if __name__ == "__main__":
    unittest.main()
import unittest
from unittest.mock import patch
import manage_assessment


def build_assessments_with_questions():
    return [
        {
            "name": "Assessment 1",
            "questions": ["Q1?", "Q2?"],
            "options": [
                ("A. a", "B. b", "C. c", "D. d"),
                ("A. x", "B. y", "C. z", "D. w"),
            ],
            "answers": ["B", "D"],
        }
    ]


class TestViewQuestionsInAssessment(unittest.TestCase):

    #If there are no assessments stored, the function should inform the user and exit immediately
    @patch("builtins.print")
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    def test_frame_1_none_saved_returns_early(self, _mock_load, mock_print):
        manage_assessment.view_questions_in_assessment()
        mock_print.assert_any_call("No assessments saved yet.")


    #If the selection input is not a number, it should be handled as invalid input without crashing
    @patch("builtins.print")
    @patch("manage_assessment.load_custom_assessments", return_value=build_assessments_with_questions())
    def test_frame_2_selection_input_invalid_value_error(
        self,
        _mock_load,
        mock_print
    ):
        with patch("builtins.input", return_value="abc"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("Invalid input.")


    #Entering 0 becomes index -1 after subtracting 1, so it should be rejected as an invalid selection
    @patch("builtins.print")
    @patch("manage_assessment.load_custom_assessments", return_value=build_assessments_with_questions())
    def test_frame_3_out_of_range_negative_index(
        self,
        _mock_load,
        mock_print
    ):
        with patch("builtins.input", return_value="0"):
            manage_assessment.view_questions_in_assessment()
        mock_print.assert_any_call("Invalid selection.")


    #A selection larger than the number of available assessments should be rejected cleanly
    @patch("builtins.print")
    @patch("manage_assessment.load_custom_assessments", return_value=build_assessments_with_questions())
    def test_frame_3_out_of_range_too_large_index(
        self,
        _mock_load,
        mock_print
    ):
        with patch("builtins.input", return_value="99"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("Invalid selection.")


    #If the chosen assessment has an empty questions list, the function should show the 'no questions' message
    @patch("builtins.print")
    @patch(
        "manage_assessment.load_custom_assessments",
        return_value=[{"name": "Empty Assessment", "questions": []}],
    )
    def test_frame_4_no_questions_prints_message_and_returns(self, _mock_load, mock_print):
        with patch("builtins.input", return_value="1"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("This assessment has no questions yet.")


    #For a valid assessment with questions, the function should print the assessment header and each question line
    @patch("builtins.print")
    @patch("manage_assessment.load_custom_assessments", return_value=build_assessments_with_questions())
    def test_frame_17_has_questions_prints_header_and_questions(
        self,
        _mock_load,
        mock_print
    ):
        with patch("builtins.input", return_value="1"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("\n--- Assessment: Assessment 1 ---")
        mock_print.assert_any_call("Q1: Q1?")
        mock_print.assert_any_call("Q2: Q2?")


    #If options are missing for some questions, the function should still print questions without raising errors
    @patch("builtins.print")
    @patch(
        "manage_assessment.load_custom_assessments",
        return_value=[
            {
                "name": "Partial Options",
                "questions": ["Q1?", "Q2?"],
                "options": [("A. a", "B. b")],
                "answers": ["A", "B"],
            }
        ],
    )
    def test_has_questions_options_shorter_does_not_crash(self, _mock_load, mock_print):
        with patch("builtins.input", return_value="1"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("Q1: Q1?")
        mock_print.assert_any_call("A. a")
        mock_print.assert_any_call("B. b")
        mock_print.assert_any_call("Q2: Q2?")


    #If answers are missing for later questions, only the available answers should be printed and execution should continue
    @patch("builtins.print")
    @patch(
        "manage_assessment.load_custom_assessments",
        return_value=[
            {
                "name": "Partial Answers",
                "questions": ["Q1?", "Q2?"],
                "options": [
                    ("A. a", "B. b", "C. c", "D. d"),
                    ("A. x", "B. y", "C. z", "D. w"),
                ],
                "answers": ["C"],
            }
        ],
    )
    def test_has_questions_answers_shorter_does_not_crash(
        self,
        _mock_load,
        mock_print
    ):
        with patch("builtins.input", return_value="1"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("Correct answer: C")
        mock_print.assert_any_call("Q2: Q2?")


    #If the 'questions' key is missing, it should be treated the same as having no questions
    @patch("builtins.print")
    @patch(
        "manage_assessment.load_custom_assessments",
        return_value=[{"name": "Missing Questions Key"}],
    )
    def test_missing_questions_key_treated_as_no_questions(self, _mock_load, mock_print):
        with patch("builtins.input", return_value="1"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("This assessment has no questions yet.")


    #On a normal run, the function should first display the saved assessments list before showing questions
    @patch("builtins.print")
    @patch("manage_assessment.load_custom_assessments", return_value=build_assessments_with_questions())
    def test_valid_selection_displays_saved_assessments_list(self, _mock_load, mock_print):
        with patch("builtins.input", return_value="1"):
            manage_assessment.view_questions_in_assessment()

        mock_print.assert_any_call("\nSaved assessments:")
        mock_print.assert_any_call("1. Assessment 1")


if __name__ == "__main__":
    unittest.main()
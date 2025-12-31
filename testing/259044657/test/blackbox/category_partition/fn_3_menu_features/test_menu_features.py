import unittest
from unittest.mock import patch

import attempt_comparison as ac
import mcq as mcqmod
import questions_viewer as qv


class TestMenusAndViewer_CategoryPartition(unittest.TestCase):
    
    @patch("builtins.input", side_effect=["0"])
    @patch("builtins.print")
    def test_comparison_menu_back_single(self, mock_print, _):
        ac.comparison_menu()
        mock_print.assert_any_call("Returning to main menu.")

    @patch("builtins.input", side_effect=["9", "0"])
    @patch("builtins.print")
    def test_comparison_menu_invalid_option_single(self, mock_print, _):
        ac.comparison_menu()
        mock_print.assert_any_call("Invalid choice. Please try again.")

    @patch("builtins.input", side_effect=["1", "   ", "0"])
    @patch("builtins.print")
    def test_comparison_menu_name_empty_single(self, mock_print, _):
        ac.comparison_menu()
        mock_print.assert_any_call("Name cannot be empty.")

    @patch("attempt_comparison.show_first_and_latest_attempt")
    @patch("builtins.input", side_effect=["1", "Alice", "0"])
    def test_comparison_menu_option1_name_nonempty_calls_compare(self, _, mock_compare):
        ac.comparison_menu()
        mock_compare.assert_called_once_with("Alice")

    @patch("attempt_comparison.choose_user_from_list_and_compare")
    @patch("builtins.input", side_effect=["2", "0"])
    def test_comparison_menu_option2_calls_choose_user(self, _, mock_choose_user):
        ac.comparison_menu()
        mock_choose_user.assert_called_once()

    @patch("builtins.print")
    def test_quiz_by_topic_no_topics_found_single(self, mock_print):
        mcqmod.quiz_by_topic([])
        mock_print.assert_any_call("No topics found in the quiz data.")

    @patch("builtins.input", return_value="abc")
    @patch("builtins.print")
    def test_quiz_by_topic_input_not_integer_single(self, mock_print, _):
        data = [{"topic": "Math", "question": "Q1", "options": ["A", "B"], "answer": "A"}]
        mcqmod.quiz_by_topic(data)
        mock_print.assert_any_call("Invalid input.")

    @patch("builtins.input", return_value="99")
    @patch("builtins.print")
    def test_quiz_by_topic_selection_out_of_range_single(self, mock_print, _):
        data = [{"topic": "Math", "question": "Q1", "options": ["A", "B"], "answer": "A"}]
        mcqmod.quiz_by_topic(data)
        mock_print.assert_any_call("Invalid topic selection.")

    @patch("mcq.take_quiz")
    @patch("builtins.input", return_value="2")
    def test_quiz_by_topic_valid_topic_calls_take_quiz(self, _, mock_take_quiz):
        data = [
            {"topic": "Math", "question": "Q1", "options": ["A", "B"], "answer": "A"},
            {"topic": "Math", "question": "Q2", "options": ["A", "B"], "answer": "B"},
            {"topic": "Geo",  "question": "Q3", "options": ["A", "B"], "answer": "A"},
        ]
        mcqmod.quiz_by_topic(data)

        args, _kwargs = mock_take_quiz.call_args
        questions, options, answers = args

        self.assertEqual(questions, ["Q1", "Q2"])
        self.assertEqual(options, [["A", "B"], ["A", "B"]])
        self.assertEqual(answers, ["A", "B"])

    @patch("builtins.print")
    def test_show_all_mcq_questions_only_prints(self, mock_print):
        qv.ALL_QUIZ_DATA = [
            {"question": "2+2=?", "options": ["A.3", "B.4"], "answer": "B", "topic": "Math", "difficulty": "Easy"}
        ]
        qv.show_all_mcq_questions_only()
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    def test_show_all_fill_in_questions_only_prints(self, mock_print):
        qv.FILL_IN_QUIZ_DATA = [
            {"question": "Capital of France: ____", "topic": "Geo", "difficulty": "Easy"}
        ]
        qv.show_all_fill_in_questions_only()
        self.assertTrue(mock_print.called)

    @patch("builtins.input", side_effect=["0"])
    @patch("builtins.print")
    def test_questions_viewer_menu_back_single(self, mock_print, _):
        qv.questions_viewer_menu()
        self.assertTrue(mock_print.called)

    @patch("builtins.input", side_effect=["9", "0"])
    @patch("builtins.print")
    def test_questions_viewer_menu_invalid_option_single(self, mock_print, _):
        qv.questions_viewer_menu()
        mock_print.assert_any_call("Invalid choice. Please try again.")

    @patch("questions_viewer.show_all_mcq_questions_only")
    @patch("builtins.input", side_effect=["1", "0"])
    def test_questions_viewer_menu_view_mcq_only_calls_fn(self, _, mock_fn):
        qv.questions_viewer_menu()
        mock_fn.assert_called_once()

    @patch("questions_viewer.show_all_fill_in_questions_only")
    @patch("builtins.input", side_effect=["2", "0"])
    def test_questions_viewer_menu_view_fill_only_calls_fn(self, _, mock_fn):
        qv.questions_viewer_menu()
        mock_fn.assert_called_once()

    @patch("questions_viewer.show_all_questions_only")
    @patch("builtins.input", side_effect=["3", "0"])
    def test_questions_viewer_menu_view_all_calls_fn(self, _, mock_fn):
        qv.questions_viewer_menu()
        mock_fn.assert_called_once()


if __name__ == "__main__":
    unittest.main()

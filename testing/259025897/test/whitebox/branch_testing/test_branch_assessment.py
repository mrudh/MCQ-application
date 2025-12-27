import io
import unittest
from unittest.mock import patch
import manage_assessment


class TestAssessment_Branches(unittest.TestCase):

    # Verifies create_assessment does not start the quiz when the user chooses not to take it now
    @patch("manage_assessment.take_quiz")
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    @patch("builtins.input",
        side_effect=["Assess1", "1", "Q1", "o1", "o2", "o3", "o4", "A", "n"],
    )
    def test_create_assessment_not_taken_now(self, m_input, m_load, m_save, m_take):
        manage_assessment.create_assessment()
        m_save.assert_called_once()
        m_take.assert_not_called()


    #Checks create_assessment starts the quiz when the user chooses to take it immediately
    @patch("manage_assessment.take_quiz")
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    @patch("builtins.input",
        side_effect=["Assess2", "1", "Q1", "o1", "o2", "o3", "o4", "A", "y"],
    )
    def test_create_assessment_taken_now_calls_quiz(self, m_input, m_load, m_save, m_take):
        manage_assessment.create_assessment()
        m_save.assert_called_once()
        m_take.assert_called_once()


    #Tests list_assessments returns None when there are no saved assessments
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    def test_list_assessments_empty_returns_none(self, m_load):
        self.assertIsNone(manage_assessment.list_assessments())


    #Tests list_assessments returns a list when saved assessments exist
    @patch("manage_assessment.load_custom_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    def test_list_assessments_non_empty_returns_list(self, m_load):
        out = manage_assessment.list_assessments()
        self.assertIsInstance(out, list)
        self.assertEqual(len(out), 1)


    #Verifies add_question_to_assessment exits when the assessment selection is not a number
    @patch("manage_assessment.list_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    @patch("builtins.input", side_effect=["abc"])
    def test_add_question_invalid_selection(self, m_input, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.add_question_to_assessment()


    #Checks add_question_to_assessment appends question/options/answer and keeps the updated assessment
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.list_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    @patch("builtins.input", side_effect=["1", "New Q", "oA", "oB", "oC", "oD", "A"])
    def test_add_question_valid_saves(self, m_input, m_list, m_save):
        manage_assessment.add_question_to_assessment()
        m_save.assert_called_once()


    #Verifies edit_question_in_assessment returns early when the selected question index is out of range
    @patch("manage_assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("builtins.input", side_effect=["1", "99"])
    def test_edit_question_invalid_q_index(self, m_input, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.edit_question_in_assessment()


    #Verifies edit_question_in_assessment keeps existing values when blanks are provided and still saves
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("builtins.input", side_effect=["1", "1", "", "", "", "", "", ""])
    def test_edit_question_keep_existing_saves(self, m_input, m_list, m_save):
        manage_assessment.edit_question_in_assessment()
        m_save.assert_called_once()


    #Tests delete_question_from_assessment removes the chosen question and maintains the change
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("builtins.input", side_effect=["1", "1"])
    def test_delete_question_valid_saves(self, m_input, m_list, m_save):
        manage_assessment.delete_question_from_assessment()
        m_save.assert_called_once()


    #Verifies delete_question_from_assessment exits early when the selected question index is out of range
    @patch("manage_assessment.list_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("builtins.input", side_effect=["1", "99"])
    def test_delete_question_invalid_index(self, m_input, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.delete_question_from_assessment()


    #Checks view_questions_in_assessment returns immediately when no assessments are saved
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    def test_view_questions_no_assessments(self, m_load):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.view_questions_in_assessment()


    #Verifies view_questions_in_assessment returns early when the user selects an invalid assessment number
    @patch("manage_assessment.load_custom_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("builtins.input", side_effect=["99"])
    def test_view_questions_invalid_selection(self, m_input, m_load):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.view_questions_in_assessment()


    #Tests view_questions_in_assessment shows the 'no questions yet' path when the assessment has no questions
    @patch("manage_assessment.load_custom_assessments",
        return_value=[{"name": "A", "questions": [], "options": [], "answers": []}],
    )
    @patch("builtins.input", side_effect=["1"])
    def test_view_questions_empty_questions_branch(self, m_input, m_load):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.view_questions_in_assessment()

    #Tests view_questions_in_assessment prints question text and the correct answer for a normal assessment
    @patch("manage_assessment.load_custom_assessments",
        return_value=[{
            "name": "A",
            "questions": ["Q1"],
            "options": [("A.1", "B.2", "C.3", "D.4")],
            "answers": ["A"],
        }],
    )
    @patch("builtins.input", side_effect=["1"])
    def test_view_questions_normal_branch(self, m_input, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            out = buf.getvalue()
            self.assertIn("Q1", out)
            self.assertIn("Correct answer: A", out)


if __name__ == "__main__":
    unittest.main()
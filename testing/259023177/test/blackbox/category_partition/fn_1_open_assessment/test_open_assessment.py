import unittest
from unittest.mock import patch, MagicMock


from assessment import open_assessment


class TestOpenAssessment_FromTSLFrames(unittest.TestCase):
   
   
    def _assessment_list(self):
        return [{
            "name": "A1",
            "questions": ["Q1"],
            "options": [["A", "B", "C", "D"]],
            "answers": ["A"]
        }]

 

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_1_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

   
    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_2_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_3_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_4_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_5_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_6_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_7_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_8_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_9_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_10_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_11_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

    @patch("assessment.load_custom_assessments", return_value=[])
    @patch("builtins.print")
    def test_case_12_no_assessments(self, mprint, _):
        open_assessment()
        mprint.assert_any_call("No assessments saved yet.")

   
    @patch("assessment.load_custom_assessments")
    @patch("builtins.input", side_effect=["abc"]) 
    @patch("builtins.print")
    def test_case_13_non_integer_selection(self, mprint, _minput, mload):
        mload.return_value = self._assessment_list()
        open_assessment()
        mprint.assert_any_call("Invalid input.")

   
    @patch("assessment.load_custom_assessments")
    @patch("builtins.input", side_effect=["99"])  
    @patch("builtins.print")
    def test_case_17_out_of_range_selection(self, mprint, _minput, mload):
        mload.return_value = self._assessment_list()
        open_assessment()
        mprint.assert_any_call("Invalid selection.")

   
    @patch("assessment.load_custom_assessments")
    @patch("builtins.input", side_effect=["1", "   "])  
    @patch("builtins.print")
    def test_case_21_valid_selection_empty_name(self, mprint, _minput, mload):
        mload.return_value = self._assessment_list()
        open_assessment()
        mprint.assert_any_call("Name cannot be empty.")

    
    @patch("assessment.take_quiz")
    @patch("assessment.record_quiz_attempt")
    @patch("assessment.can_attempt_quiz", return_value=(False, 0))
    @patch("assessment.load_custom_assessments")
    @patch("builtins.input", side_effect=["1", "Sarthak"]) 
    @patch("builtins.print")
    def test_case_23_no_attempts_left(
        self, mprint, _minput, mload, _mcan, mrecord, mtake
    ):
        mload.return_value = self._assessment_list()
        open_assessment()

        
        self.assertFalse(mrecord.called)
        self.assertFalse(mtake.called)
        
        found = any("used all your attempts" in str(call.args[0]) for call in mprint.call_args_list)
        self.assertTrue(found)

    
    @patch("assessment.take_quiz")
    @patch("assessment.record_quiz_attempt")
    @patch("assessment.can_attempt_quiz", return_value=(True, 1))
    @patch("assessment.load_custom_assessments")
    @patch("builtins.input", side_effect=["1", "Sarthak"]) 
    @patch("builtins.print")
    def test_case_24_attempts_ok_proceed(
        self, mprint, _minput, mload, _mcan, mrecord, mtake
    ):
        assessments = self._assessment_list()
        mload.return_value = assessments

        open_assessment()

        
        self.assertTrue(mrecord.called)

      
        chosen = assessments[0]
        mtake.assert_called_once_with(
            chosen["questions"], chosen["options"], chosen["answers"], name="Sarthak"
        )

        
        found = any("Opening assessment" in str(call.args[0]) for call in mprint.call_args_list)
        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch
import io
import contextlib
from attempt_comparison import show_first_and_latest_attempt

def run_and_capture(func, *args, **kwargs) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()


class TestShowFirstAndLatestAttempt(unittest.TestCase):
    @patch("attempt_comparison.get_user_attempts")
    def test_case_01_empty_attempts(self, mock_get_user_attempts):
        mock_get_user_attempts.return_value = []
        out = run_and_capture(show_first_and_latest_attempt, "any_user")

        self.assertIn("No quiz attempts found", out)
        self.assertIn("any_user", out)

    
    def assert_comparison_output(self, out: str, user: str, first_score: int, latest_score: int):
        self.assertIn("===== QUIZ ATTEMPT COMPARISON =====", out)
        self.assertIn(f"User: {user}", out)
        self.assertIn(f"First attempt score : {first_score}%", out)
        self.assertIn(f"Latest attempt score: {latest_score}%", out)

        diff = latest_score - first_score
        if diff > 0:
            self.assertIn(f"Progress          : +{diff}% (improvement)", out)
        elif diff < 0:
            self.assertIn(f"Progress          : {diff}% (drop)", out)
        else:
            self.assertIn("Progress          : 0% (no change)", out)

    
    def make_attempts(self, first_present: bool, latest_present: bool, first_val: int, latest_val: int):
        first = {"score": first_val} if first_present else {}
        latest = {"score": latest_val} if latest_present else {}
        return [first, latest]
    @patch("attempt_comparison.get_user_attempts")


    def test_case_02_existing_has_first_present_latest_present_diff_positive(self, mock_get):
        mock_get.return_value = self.make_attempts(True, True, 50, 80)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 50, 80)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_03_existing_has_first_present_latest_present_diff_negative(self, mock_get):
        mock_get.return_value = self.make_attempts(True, True, 80, 50)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 80, 50)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_04_existing_has_first_present_latest_present_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(True, True, 70, 70)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 70, 70)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_05_existing_has_first_present_latest_missing_diff_positive(self, mock_get):
        mock_get.return_value = self.make_attempts(True, False, -10, 0)  
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", -10, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_06_existing_has_first_present_latest_missing_diff_negative(self, mock_get):
        mock_get.return_value = self.make_attempts(True, False, 10, 0)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 10, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_07_existing_has_first_present_latest_missing_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(True, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_08_existing_has_first_missing_latest_present_diff_positive(self, mock_get):
        mock_get.return_value = self.make_attempts(False, True, 0, 10)  
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 0, 10)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_09_existing_has_first_missing_latest_present_diff_negative(self, mock_get):
        mock_get.return_value = self.make_attempts(False, True, 0, -10)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 0, -10)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_10_existing_has_first_missing_latest_present_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, True, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_11_existing_has_first_missing_latest_missing_diff_positive_frame_but_actual_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_12_existing_has_first_missing_latest_missing_diff_negative_frame_but_actual_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_13_existing_has_first_missing_latest_missing_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "existing_user")
        self.assert_comparison_output(out, "existing_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_14_unknown_has_first_present_latest_present_diff_positive(self, mock_get):
        mock_get.return_value = self.make_attempts(True, True, 40, 60)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 40, 60)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_15_unknown_has_first_present_latest_present_diff_negative(self, mock_get):
        mock_get.return_value = self.make_attempts(True, True, 60, 40)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 60, 40)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_16_unknown_has_first_present_latest_present_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(True, True, 55, 55)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 55, 55)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_17_unknown_has_first_present_latest_missing_diff_positive(self, mock_get):
        mock_get.return_value = self.make_attempts(True, False, -5, 0)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", -5, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_18_unknown_has_first_present_latest_missing_diff_negative(self, mock_get):
        mock_get.return_value = self.make_attempts(True, False, 5, 0)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 5, 0)
    @patch("attempt_comparison.get_user_attempts")

    def test_case_19_unknown_has_first_present_latest_missing_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(True, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_20_unknown_has_first_missing_latest_present_diff_positive(self, mock_get):
        mock_get.return_value = self.make_attempts(False, True, 0, 5)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 0, 5)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_21_unknown_has_first_missing_latest_present_diff_negative(self, mock_get):
        mock_get.return_value = self.make_attempts(False, True, 0, -5)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 0, -5)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_22_unknown_has_first_missing_latest_present_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, True, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_23_unknown_has_first_missing_latest_missing_diff_positive_frame_but_actual_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_24_unknown_has_first_missing_latest_missing_diff_negative_frame_but_actual_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 0, 0)
    @patch("attempt_comparison.get_user_attempts")


    def test_case_25_unknown_has_first_missing_latest_missing_diff_zero(self, mock_get):
        mock_get.return_value = self.make_attempts(False, False, 0, 0)
        out = run_and_capture(show_first_and_latest_attempt, "unknown_user")
        self.assert_comparison_output(out, "unknown_user", 0, 0)


if __name__ == "__main__":
    unittest.main()

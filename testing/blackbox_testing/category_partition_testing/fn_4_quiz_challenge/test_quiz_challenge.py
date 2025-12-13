import unittest
from unittest.mock import patch
import mcq


class TestTakeQuizChallengeFromFrames(unittest.TestCase):
    NAME = "Mru"

    def setUp(self):
        self.questions = ["Q1?"]
        self.options = [["A", "B", "C", "D"]]
        self.answers = ["A"]


    @patch("builtins.print")
    def test_frame_1_zero_questions_raises_error(self, _mock_print):
        with patch("builtins.input", side_effect=["2"]):
            with self.assertRaises(Exception):
                mcq.take_quiz_challenge([], [], [], name=self.NAME)


    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq.timed_quiz", return_value=None)
    def test_frame_2_below_then_valid_minutes(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["1", "2"]):
            with patch("mcq.time.time", side_effect=[0.0, 120.1]):
                with patch("mcq.random.shuffle", side_effect=lambda x: x):
                    mcq.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq.timed_quiz", return_value=None)
    def test_frame_3_above_then_valid_minutes(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["6", "5"]):
            with patch("mcq.time.time", side_effect=[0.0, 300.1]):
                with patch("mcq.random.shuffle", side_effect=lambda x: x):
                    mcq.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq.timed_quiz", return_value=None)
    def test_frame_4_non_zero_valid_2(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["2"]):
            with patch("mcq.time.time", side_effect=[0.0, 120.1]):
                with patch("mcq.random.shuffle", side_effect=lambda x: x):
                    mcq.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq.timed_quiz", return_value=None)
    def test_frame_5_non_zero_valid_5(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["5"]):
            with patch("mcq.time.time", side_effect=[0.0, 300.1]):
                with patch("mcq.random.shuffle", side_effect=lambda x: x):
                    mcq.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()

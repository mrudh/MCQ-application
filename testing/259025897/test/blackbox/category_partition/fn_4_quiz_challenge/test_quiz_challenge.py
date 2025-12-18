import unittest
from unittest.mock import patch
import mcq_types as module_0


class TestTakeQuizChallengeFromFrames(unittest.TestCase):
    NAME = "Mru"

    def setUp(self):
        self.questions = ["Q1?"]
        self.options = [["A", "B", "C", "D"]]
        self.answers = ["A"]


    #Starting challenge mode with no questions should fail instead of looping forever
    @patch("builtins.print")
    def test_frame_1_zero_questions_raises_error(self, _mock_print):
        with patch("builtins.input", side_effect=["2"]):
            with self.assertRaises(Exception):
                module_0.take_quiz_challenge([], [], [], name=self.NAME)


    #If the user enters minutes below the allowed range, the function should reprompt and accept a valid value
    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_frame_2_below_then_valid_minutes(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["1", "2"]):
            with patch("mcq_types.time.time", side_effect=[0.0, 120.1]):
                with patch("mcq_types.random.shuffle", side_effect=lambda x: x):
                    module_0.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


    #If the user enters minutes above the allowed range, the function should reprompt and accept a valid value
    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_frame_3_above_then_valid_minutes(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["6", "5"]):
            with patch("mcq_types.time.time", side_effect=[0.0, 300.1]):
                with patch("mcq_types.random.shuffle", side_effect=lambda x: x):
                    module_0.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


    #A valid minimum duration of 2 minutes should run and save a result for a named user
    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_frame_4_non_zero_valid_2(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["2"]):
            with patch("mcq_types.time.time", side_effect=[0.0, 120.1]):
                with patch("mcq_types.random.shuffle", side_effect=lambda x: x):
                    module_0.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


    #A valid maximum duration of 5 minutes should run and save a result for a named user.
    @patch("builtins.print")
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_frame_5_non_zero_valid_5(
            self,
            _mock_timed_quiz,
            _mock_load,
            mock_save,
            _mock_print,
    ):
        with patch("builtins.input", side_effect=["5"]):
            with patch("mcq_types.time.time", side_effect=[0.0, 300.1]):
                with patch("mcq_types.random.shuffle", side_effect=lambda x: x):
                    module_0.take_quiz_challenge(
                        self.questions,
                        self.options,
                        self.answers,
                        name=self.NAME,
                    )
                    mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()

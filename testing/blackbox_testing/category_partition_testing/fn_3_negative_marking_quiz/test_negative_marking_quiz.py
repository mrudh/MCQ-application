import unittest
from unittest.mock import patch
import mcq


class TestTakeNegativeMarkQuizFromTSLFrames(unittest.TestCase):
    NAME = "Mru"

    def setUp(self):
        self.questions_one = ["Q1?"]
        self.options_one = [["A", "B", "C", "D"]]
        self.answers_one = ["A"]

        self.questions_many = ["Q1?", "Q2?"]
        self.options_many = [
            ["A", "B", "C", "D"],
            ["A", "B", "C", "D"],
        ]
        self.answers_many = ["A", "B"]


    @patch("builtins.print")
    def test_frame_1_zero_questions_raises_zero_division_error(self, _mock_print):
        with self.assertRaises(ZeroDivisionError):
            mcq.take_negative_mark_quiz(
                [],
                [],
                [],
                name=self.NAME,
                neg_mark=0.25,
                timed=False,
            )


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="A")
    def test_frame_2_one_default_correct_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_one,
            self.options_one,
            self.answers_one,
            name=self.NAME,
            neg_mark=0.25,
            timed=False,
        )
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="A")
    def test_frame_3_one_default_correct_name_no(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_one,
            self.options_one,
            self.answers_one,
            name=None,
            neg_mark=0.25,
            timed=False,
        )
        mock_save.assert_not_called()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="B")
    def test_frame_4_one_default_wrong_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_one,
            self.options_one,
            self.answers_one,
            name=self.NAME,
            neg_mark=0.25,
            timed=False,
        )
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="")
    def test_frame_6_one_default_empty_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_one,
            self.options_one,
            self.answers_one,
            name=self.NAME,
            neg_mark=0.25,
            timed=False,
        )
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="X")
    def test_frame_8_one_default_invalid_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_one,
            self.options_one,
            self.answers_one,
            name=self.NAME,
            neg_mark=0.25,
            timed=False,
        )
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="A")
    def test_frame_10_one_zero_penalty_correct_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_one,
            self.options_one,
            self.answers_one,
            name=self.NAME,
            neg_mark=0.0,
            timed=False,
        )
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="B")
    def test_frame_20_one_high_penalty_wrong_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_one,
            self.options_one,
            self.answers_one,
            name=self.NAME,
            neg_mark=1.0,
            timed=False,
        )
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B"])
    def test_frame_26_many_default_correct_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_many,
            self.options_many,
            self.answers_many,
            name=self.NAME,
            neg_mark=0.25,
            timed=False,
        )
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["C", "D"])
    def test_frame_28_many_default_wrong_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_negative_mark_quiz(
            self.questions_many,
            self.options_many,
            self.answers_many,
            name=self.NAME,
            neg_mark=0.25,
            timed=False,
        )
        mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()

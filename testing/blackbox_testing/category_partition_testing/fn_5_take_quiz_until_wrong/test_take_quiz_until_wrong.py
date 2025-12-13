import unittest
from unittest.mock import patch
import mcq


def shuffle_identity(indices):
    return None


class TestTakeQuizUntilWrongFromFrames(unittest.TestCase):
    NAME = "Mru"

    def setUp(self):
        self.qs1 = ["Q1?"]
        self.opts1 = [["A", "B", "C", "D"]]
        self.ans1 = ["A"]

        self.qs2 = ["Q1?", "Q2?", "Q3?"]
        self.opts2 = [
            ["A", "B", "C", "D"],
            ["A", "B", "C", "D"],
            ["A", "B", "C", "D"],
        ]
        self.ans2 = ["A", "B", "C"]

    @patch("builtins.print")
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    def test_tc1_zero_questions_saves_zero_percent(
        self,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong([], [], [], name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="A")
    def test_tc11_one_all_correct_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="A")
    def test_tc12_one_all_correct_name_no(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=None)
        mock_save.assert_not_called()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="")
    def test_tc17_one_empty_input_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="B")
    def test_tc23_one_wrong_input_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="X")
    def test_tc29_one_invalid_input_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", "C"])
    def test_tc37_many_all_correct_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", return_value="")
    def test_tc41_many_empty_first_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "D"])
    def test_tc49_many_wrong_middle_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


    @patch("builtins.print")
    @patch("mcq.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", "X"])
    def test_tc57_many_invalid_last_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        mcq.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()

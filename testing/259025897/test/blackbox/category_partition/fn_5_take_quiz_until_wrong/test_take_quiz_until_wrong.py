import unittest
from unittest.mock import patch
import mcq_types as module_0


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


    #If there are no questions, the function should still record a 0% score for a named user
    @patch("builtins.print")
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    def test_tc1_zero_questions_saves_zero_percent(
        self,
        _mock_load,
        mock_save,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong([], [], [], name=self.NAME)
        mock_save.assert_called_once()


    #A single-question streak where the user answers correctly should be saved when a name is provided
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", return_value="A")
    def test_tc11_one_all_correct_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    #Even if the answer is correct, no score should be persisted when the name is None
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", return_value="A")
    def test_tc12_one_all_correct_name_no(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=None)
        mock_save.assert_not_called()


    #An empty input should end the streak immediately, but the attempt should still be saved for a named user
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", return_value="")
    def test_tc17_one_empty_input_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    #A wrong answer on the first question should stop the quiz and still store the score for a named user
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", return_value="B")
    def test_tc23_one_wrong_input_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    #An invalid option should be treated as a wrong answer and still be saved for a named user
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", return_value="X")
    def test_tc29_one_invalid_input_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs1, self.opts1, self.ans1, name=self.NAME)
        mock_save.assert_called_once()


    #If the user answers every question correctly, it should save a 100% streak result for a named user
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", "C"])
    def test_tc37_many_all_correct_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


    #Empty input on the first question should end immediately and still save a 0% result for a named user
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", return_value="")
    def test_tc41_many_empty_first_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


    #A wrong answer part way through should stop the streak and save the partial score for a named user
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "D"])
    def test_tc49_many_wrong_middle_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


    #An invalid answer later in the quiz should count as wrong and the final streak score should be saved
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", "X"])
    def test_tc57_many_invalid_last_name_yes(
        self,
        _mock_input,
        _mock_load,
        mock_save,
        _mock_shuffle,
        _mock_print,
    ):
        module_0.take_quiz_until_wrong(self.qs2, self.opts2, self.ans2, name=self.NAME)
        mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()

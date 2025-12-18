import unittest
from unittest.mock import patch
import mcq_types as module_0


def shuffle_identity(indices):
    return None


class TestLearningModeFromFrames(unittest.TestCase):
    def setUp(self):
        self.qs0 = []
        self.ans0 = []
        self.qs1 = ["Q1?"]
        self.ans1 = ["A1"]
        self.qs2 = ["Q1?", "Q2?", "Q3?"]
        self.ans2 = ["A1", "A2", "A3"]


    #With no flashcards, learning mode should finish without prompting the user at all
    @patch("builtins.print")
    def test_tc1_zero_questions_no_input_needed(self, _mock_print):
        with patch("builtins.input") as mock_input:
            module_0.learning_mode(self.qs0, self.ans0)
            mock_input.assert_not_called()


    #For a single card, user presses 'Enter' to reveal, then marks it correct with 'y'
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc10_one_y_correct(self, _mock_shuffle, _mock_print):
        with patch("builtins.input", side_effect=["", "y"]) as mock_input:
            module_0.learning_mode(self.qs1, self.ans1)
            self.assertEqual(mock_input.call_count, 2)


    #For a single card, user presses 'Enter' to reveal, then marks it incorrect with 'n'
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc11_one_n_incorrect(self, _mock_shuffle, _mock_print):
        with patch("builtins.input", side_effect=["", "n"]) as mock_input:
            module_0.learning_mode(self.qs1, self.ans1)
            self.assertEqual(mock_input.call_count, 2)


    #User quits right after seeing the first answer by entering 'q' at the self-check prompt
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc12_one_quit_immediately_first(self, _mock_shuffle, _mock_print):
        with patch("builtins.input", side_effect=["", "q"]) as mock_input:
            module_0.learning_mode(self.qs1, self.ans1)
            self.assertEqual(mock_input.call_count, 2)


    #Across multiple cards, user reveals each answer and marks all of them correct
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc15_many_y_correct(self, _mock_shuffle, _mock_print):
        inputs = ["", "y", "", "y", "", "y"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            module_0.learning_mode(self.qs2, self.ans2)
            self.assertEqual(mock_input.call_count, 6)


    #Across multiple cards, user reveals each answer and marks all of them incorrect
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc16_many_n_incorrect(self, _mock_shuffle, _mock_print):
        inputs = ["", "n", "", "n", "", "n"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            module_0.learning_mode(self.qs2, self.ans2)
            self.assertEqual(mock_input.call_count, 6)


    #User quits immediately on the first card after revealing the answer
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc17_many_quit_first(self, _mock_shuffle, _mock_print):
        with patch("builtins.input", side_effect=["", "q"]) as mock_input:
            module_0.learning_mode(self.qs2, self.ans2)
            self.assertEqual(mock_input.call_count, 2)


    #User completes the first card, then quits during the self-check prompt of the second card
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc18_many_quit_middle(self, _mock_shuffle, _mock_print):
        with patch("builtins.input", side_effect=["", "y", "", "q"]) as mock_input:
            module_0.learning_mode(self.qs2, self.ans2)
            self.assertEqual(mock_input.call_count, 4)


    #User goes through cards in order and quits only on the final self-check prompt
    @patch("builtins.print")
    @patch("mcq_types.random.shuffle", side_effect=shuffle_identity)
    def test_tc19_many_quit_last(self, _mock_shuffle, _mock_print):
        inputs = ["", "y", "", "y", "", "q"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            module_0.learning_mode(self.qs2, self.ans2)
            self.assertEqual(mock_input.call_count, 6)


if __name__ == "__main__":
    unittest.main()

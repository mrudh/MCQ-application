import unittest
from unittest.mock import patch
import mcq


class TestTakeQuiz_CategoryPartition(unittest.TestCase):
    def setUp(self):
#one question scenario
        self.qs1 = ["Q1?"]
        self.opts1 = [["A", "B", "C", "D"]]
        self.ans1 = ["A"]

#multiple questions scenario
        self.qs2 = ["Q1?", "Q2?"]
        self.opts2 = [["A", "B", "C", "D"], ["A", "B", "C", "D"]]
        self.ans2 = ["A", "B"]


    def test_zero_questions_raises_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            mcq.take_quiz([], [], [], name="Mru", timed=True)


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("mcq.timed_quiz", return_value="A")
    def test_timed_correct_name_yes(self, _tq, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=True)
        save_scores.assert_called_once()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("mcq.timed_quiz", return_value="B")
    def test_timed_incorrect_name_no(self, _tq, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=True)
        save_scores.assert_not_called()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("mcq.timed_quiz", return_value="X")
    def test_timed_invalid_name_yes(self, _tq, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=True)
        save_scores.assert_called_once()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("mcq.timed_quiz", return_value="")
    def test_timed_empty_name_no(self, _tq, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=True)
        save_scores.assert_not_called()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("mcq.timed_quiz", return_value=None)
    def test_timed_timeout_name_yes(self, _tq, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=True)
        save_scores.assert_called_once()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("builtins.input", return_value="A")
    def test_not_timed_correct_name_yes(self, _inp, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=False)
        save_scores.assert_called_once()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("builtins.input", return_value="B")
    def test_not_timed_incorrect_name_no(self, _inp, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=False)
        save_scores.assert_not_called()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("builtins.input", return_value="X")
    def test_not_timed_invalid_name_yes(self, _inp, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=False)
        save_scores.assert_called_once()


    @patch("mcq.save_scores")
    @patch("mcq.load_scores", return_value=[])
    @patch("mcq.print_results")
    @patch("builtins.input", return_value="")
    def test_not_timed_empty_name_no(self, _inp, _pr, _ls, save_scores):
        mcq.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=False)
        save_scores.assert_not_called()


    @patch("mcq.print_results")
    @patch("builtins.input", side_effect=["A", "B"])
    def test_many_questions_not_timed(self, _inp, _pr):
        mcq.take_quiz(self.qs2, self.opts2, self.ans2, name=None, timed=False)


if __name__ == "__main__":
    unittest.main()

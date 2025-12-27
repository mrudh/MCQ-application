import unittest
from unittest.mock import patch
import mcq_types as module_0


class TestTakeQuiz_CategoryPartition(unittest.TestCase):
    def setUp(self):
        #Single question quiz data
        self.qs1 = ["Q1?"]
        self.opts1 = [["A", "B", "C", "D"]]
        self.ans1 = ["A"]

        #Multiple question quiz data
        self.qs2 = ["Q1?", "Q2?"]
        self.opts2 = [["A", "B", "C", "D"], ["A", "B", "C", "D"]]
        self.ans2 = ["A", "B"]


    #Verifies that calling take_quiz with zero questions results in a ZeroDivisionError when score percentage is calculated
    def test_zero_questions_raises_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            module_0.take_quiz([], [], [], name="Mru", timed=True)


    #Tests timed quiz with a correct answer and a valid user name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value="A")
    def test_timed_correct_name_yes(self, _tq, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=True)
        save_scores.assert_called_once()


    #Tests timed quiz with an incorrect answer and no user name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value="B")
    def test_timed_incorrect_name_no(self, _tq, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=True)
        save_scores.assert_not_called()


    #Tests timed quiz with an invalid answer input but a valid name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value="X")
    def test_timed_invalid_name_yes(self, _tq, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=True)
        save_scores.assert_called_once()


    #Tests timed quiz with empty input and no name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value="")
    def test_timed_empty_name_no(self, _tq, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=True)
        save_scores.assert_not_called()


    #Tests timed quiz where the user times out but the score is still saved when a valid name is given
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_timed_timeout_name_yes(self, _tq, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=True)
        save_scores.assert_called_once()


    #Tests non-timed quiz with correct input and a valid name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", return_value="A")
    def test_not_timed_correct_name_yes(self, _inp, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=False)
        save_scores.assert_called_once()


    #Tests non-timed quiz with incorrect input and no name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", return_value="B")
    def test_not_timed_incorrect_name_no(self, _inp, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=False)
        save_scores.assert_not_called()


    #Tests non-timed quiz with invalid input but a valid name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", return_value="X")
    def test_not_timed_invalid_name_yes(self, _inp, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name="Mru", timed=False)
        save_scores.assert_called_once()


    #Tests non-timed quiz with empty input and no name
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", return_value="")
    def test_not_timed_empty_name_no(self, _inp, _pr, _ls, save_scores):
        module_0.take_quiz(self.qs1, self.opts1, self.ans1, name=None, timed=False)
        save_scores.assert_not_called()


    #Tests non-timed quiz with multiple questions
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["A", "B"])
    def test_many_questions_not_timed(self, _inp, _pr):
        module_0.take_quiz(self.qs2, self.opts2, self.ans2, name=None, timed=False)


if __name__ == "__main__":
    unittest.main()

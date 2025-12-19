import io
import sys
import types
import unittest
from unittest.mock import patch
import mcq_types


class TestTakeQuiz_Branches(unittest.TestCase):

    #Checks untimed quiz path where the user answers correctly and no score is saved without a name
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["A"])
    def test_take_quiz_untimed_correct_no_name(self, m_input, m_print_results):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz(qs, opts, ans, name=None, timed=False)
        m_print_results.assert_called_once()


    #Tests untimed quiz path where a wrong answer is given and the score is saved when a name is provided
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["B"])
    def test_take_quiz_untimed_incorrect_with_name_saves(
        self, m_input, m_print_results, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz(qs, opts, ans, name="Alice", timed=False)
        m_print_results.assert_called_once()
        m_load.assert_called_once()
        m_save.assert_called_once()


    #Checks timed quiz path where timed_quiz returns a valid answer and the score is saved
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value="A")
    def test_take_quiz_timed_input_with_name_saves(
        self, m_timed, m_print_results, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz(qs, opts, ans, name="Bob", timed=True)
        m_timed.assert_called_once()
        m_print_results.assert_called_once()
        m_save.assert_called_once()


    #Checks timed quiz timeout path where timed_quiz returns None and the blank guess branch runs
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_take_quiz_timed_timeout_sets_blank_guess(
        self, m_timed, m_print_results, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz(qs, opts, ans, name="Eve", timed=True)
        m_timed.assert_called_once()
        m_print_results.assert_called_once()
        m_save.assert_called_once()


class TestTimedQuiz_Branches(unittest.TestCase):

    #Tests non-Windows timed_quiz branch where input arrives before the timeout
    @patch("select.select", return_value=([sys.stdin], [], []))
    @patch("sys.stdin.readline", return_value="b\n")
    def test_timed_quiz_non_windows_input(self, m_read, m_select):
        with patch.object(sys, "platform", "darwin"):
            self.assertEqual(mcq_types.timed_quiz("Enter:", timeout=1), "B")


    #Checks non-Windows timed_quiz branch where no input arrives and the function times out
    @patch("select.select", return_value=([], [], []))
    def test_timed_quiz_non_windows_timeout(self, m_select):
        with patch.object(sys, "platform", "darwin"):
            self.assertIsNone(mcq_types.timed_quiz("Enter:", timeout=0.01))


    #Tests Windows timed_quiz branch where a user types a character followed by Enter
    def test_timed_quiz_windows_input_enter(self):
        fake_msvcrt = types.SimpleNamespace(
            kbhit=lambda: True,
            getwch=lambda: "\r",
        )
        buf = {"typed": ""}

        def getwch():
            if buf["typed"] == "":
                buf["typed"] = "A"
                return "A"
            return "\r"

        fake_msvcrt.getwch = getwch

        with patch.dict(sys.modules, {"msvcrt": fake_msvcrt}):
            with patch.object(sys, "platform", "win32"):
                with patch("sys.stdout", new_callable=io.StringIO):
                    with patch("mcq_types.time.sleep", return_value=None):
                        self.assertEqual(mcq_types.timed_quiz("Enter:", timeout=1), "A")


    #Tests Windows timed_quiz timeout branch when no key is pressed before the timeout expires
    def test_timed_quiz_windows_timeout(self):
        fake_msvcrt = types.SimpleNamespace(
            kbhit=lambda: False,
            getwch=lambda: "",
        )

        t = {"now": 0.0}

        def fake_time():
            t["now"] += 0.02
            return t["now"]

        with patch.dict(sys.modules, {"msvcrt": fake_msvcrt}):
            with patch.object(sys, "platform", "win32"):
                with patch("mcq_types.time.time", side_effect=fake_time):
                    with patch("mcq_types.time.sleep", return_value=None):
                        with patch("sys.stdout", new_callable=io.StringIO):
                            self.assertIsNone(mcq_types.timed_quiz("Enter:", timeout=0.01))


class TestNegativeMark_Branches(unittest.TestCase):

    #Tests negative marking quiz branches for correct, wrong with penalty, and blank answer cases
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", ""])
    def test_negative_mark_branches(self, m_input, m_load, m_save):
        qs = ["Q1", "Q2", "Q3"]
        opts = [("A.1", "B.2", "C.3", "D.4")] * 3
        ans = ["A", "A", "A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="Nina", neg_mark=0.25)
        m_save.assert_called_once()


class TestChallenge_Branches(unittest.TestCase):

    #Checks challenge mode branch where time runs out immediately and the score is still saved for a named user
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=["3"])
    @patch("mcq_types.time.time", side_effect=[0, 9999])
    def test_challenge_immediate_timeup_saves(
        self, m_time, m_input, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User1")
        m_save.assert_called_once()


    #Checks challenge mode branch where timed_quiz returns None mid-question and the score is still saved
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("mcq_types.timed_quiz", return_value=None)
    @patch("builtins.input", side_effect=["3"])
    @patch("mcq_types.time.time", side_effect=[0, 0, 1])
    def test_challenge_guess_none_branch_saves(
        self, m_time, m_input, m_timed, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User2")
        m_save.assert_called_once()


    #Checks challenge mode validation loop where invalid minutes are rejected until a valid value is entered
    @patch("storage.save_scores")
    @patch("storage.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    @patch("builtins.input", side_effect=["10", "abc", "3"])
    @patch("mcq_types.time.time", side_effect=[0, 0, 1])
    def test_challenge_minutes_validation_loop_saves(
        self, m_time, m_input, m_timed, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User3")
        m_save.assert_called_once()


class TestStreak_Branches(unittest.TestCase):

    #Checks streak mode branch where all questions are answered correctly and the completion message path is reached
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=["A"])
    def test_streak_all_correct_amazing_branch(
        self, m_input, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="Sam")
        m_save.assert_called_once()


    #Checks streak mode branch where a wrong answer ends the quiz early and the score is saved
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=["B"])
    def test_streak_wrong_answer_branch_saves(
        self, m_input, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="Tina")
        m_save.assert_called_once()


    #Checks streak mode branch where the user submits a blank answer and the 'No answer selected' path is taken
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=[""])
    def test_streak_blank_answer_branch_saves(
        self, m_input, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="Leo")
        m_save.assert_called_once()


class TestLearningMode_Branches(unittest.TestCase):

    #Checks learning mode loop that rejects invalid marks and exits immediately when the user chooses to quit
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "x", "q"])
    def test_learning_mode_invalid_then_quit(self, m_input, m_out, m_shuffle):
        mcq_types.learning_mode(["Q1"], ["A1"])
        out = m_out.getvalue()
        self.assertIn("Cards reviewed : 0", out)


    #Tests learning mode path where the user marks the card as correct and accuracy is computed accordingly
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "y"])
    def test_learning_mode_yes_branch_counts(self, m_input, m_out, m_shuffle):
        mcq_types.learning_mode(["Q1"], ["A1"])
        out = m_out.getvalue()
        self.assertIn("Cards reviewed : 1", out)
        self.assertIn("Marked correct : 1", out)


if __name__ == "__main__":
    unittest.main()
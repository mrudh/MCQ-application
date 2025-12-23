import io
import sys
import types
import unittest
from unittest.mock import patch
import mcq_types
import manage_assessment

# test cases for take quiz function
class TestConcolicTakeQuiz(unittest.TestCase):

    # Concolic Case 1: untimed + correct answer + name=None should not save scores
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["A"])
    def test_concolic_case_1_untimed_correct_name_none_no_save(
        self, m_input, m_print_results, m_load_scores, m_save_scores
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]

        mcq_types.take_quiz(qs, opts, ans, name=None, timed=False)
        m_print_results.assert_called_once()
        m_load_scores.assert_not_called()
        m_save_scores.assert_not_called()


    #Concolic Case 2: untimed + correct answer + name provided should save scores once
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["A"])
    def test_concolic_case_2_untimed_correct_name_saves(
        self, m_input, m_print_results, m_load_scores, m_save_scores
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]

        mcq_types.take_quiz(qs, opts, ans, name="Mru", timed=False)
        m_print_results.assert_called_once()
        m_load_scores.assert_called_once()
        m_save_scores.assert_called_once()


    #Concolic Case 3: untimed + incorrect answer + name provided should still save percent once
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("builtins.input", side_effect=["B"])
    def test_concolic_case_3_untimed_incorrect_name_saves(
        self, m_input, m_print_results, m_load_scores, m_save_scores
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]

        mcq_types.take_quiz(qs, opts, ans, name="Dhu", timed=False)
        m_print_results.assert_called_once()
        m_load_scores.assert_called_once()
        m_save_scores.assert_called_once()


    #Concolic Case 4: timed + timed_quiz returns a letter + correct answer + name=None should not save
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value="A")
    def test_concolic_case_4_timed_input_correct_name_none_no_save(
        self, m_timed_quiz, m_print_results, m_load_scores, m_save_scores
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]

        mcq_types.take_quiz(qs, opts, ans, name=None, timed=True)
        m_timed_quiz.assert_called_once()
        m_print_results.assert_called_once()
        m_load_scores.assert_not_called()
        m_save_scores.assert_not_called()


    #Concolic Case 5: timed + timed_quiz returns None (timeout) + name provided should save once
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.print_results")
    @patch("mcq_types.timed_quiz", return_value=None)
    def test_concolic_case_5_timed_timeout_name_saves(
        self, m_timed_quiz, m_print_results, m_load_scores, m_save_scores
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]

        mcq_types.take_quiz(qs, opts, ans, name="Laa", timed=True)
        m_timed_quiz.assert_called_once()
        m_print_results.assert_called_once()
        m_load_scores.assert_called_once()
        m_save_scores.assert_called_once()


class TestTimedQuiz_Concolic(unittest.TestCase):

    # Concolic test case 1: Non-Windows path where select reports input and the function returns uppercase line.
    @patch("select.select", return_value=([sys.stdin], [], []))
    @patch("sys.stdin.readline", return_value="b\n")
    def test_concolic_1_non_windows_input_available(self, m_read, m_select):
        with patch.object(sys, "platform", "darwin"):
            self.assertEqual(mcq_types.timed_quiz("Enter:", timeout=1), "B")


    # Concolic test case 2: Non-Windows path where select times out with no input and the function returns None
    @patch("select.select", return_value=([], [], []))
    def test_concolic_2_non_windows_no_input_timeout(self, m_select):
        with patch.object(sys, "platform", "darwin"):
            self.assertIsNone(mcq_types.timed_quiz("Enter:", timeout=0.01))


    # Concolic test case 3: Windows path where a character is typed and then Enter returns the built buffer
    def test_concolic_3_windows_type_then_enter(self):
        state = {"step": 0}

        def fake_kbhit():
            return True

        def fake_getwch():
            state["step"] += 1
            if state["step"] == 1:
                return "a"
            return "\r"

        fake_msvcrt = types.SimpleNamespace(kbhit=fake_kbhit, getwch=fake_getwch)
        with patch.dict(sys.modules, {"msvcrt": fake_msvcrt}):
            with patch.object(sys, "platform", "win32"):
                with patch("sys.stdout", new_callable=io.StringIO):
                    with patch("mcq_types.time.sleep", return_value=None):
                        self.assertEqual(mcq_types.timed_quiz("Enter:", timeout=1), "A")


    # Concolic test case 4: Windows path where backspace removes a typed character and Enter returns an empty buffer
    def test_concolic_4_windows_backspace_then_enter(self):
        state = {"step": 0}

        def fake_kbhit():
            return True

        def fake_getwch():
            state["step"] += 1
            if state["step"] == 1:
                return "A"
            if state["step"] == 2:
                return "\b"
            return "\r"

        fake_msvcrt = types.SimpleNamespace(kbhit=fake_kbhit, getwch=fake_getwch)
        with patch.dict(sys.modules, {"msvcrt": fake_msvcrt}):
            with patch.object(sys, "platform", "win32"):
                with patch("sys.stdout", new_callable=io.StringIO):
                    with patch("mcq_types.time.sleep", return_value=None):
                        self.assertEqual(mcq_types.timed_quiz("Enter:", timeout=1), "")


    # Concolic test case 5: Windows path where backspace is pressed on an empty buffer and Enter still returns empty.
    def test_concolic_5_windows_backspace_on_empty_then_enter(self):
        state = {"step": 0}

        def fake_kbhit():
            return True

        def fake_getwch():
            state["step"] += 1
            if state["step"] == 1:
                return "\b"
            return "\r"

        fake_msvcrt = types.SimpleNamespace(kbhit=fake_kbhit, getwch=fake_getwch)
        with patch.dict(sys.modules, {"msvcrt": fake_msvcrt}):
            with patch.object(sys, "platform", "win32"):
                with patch("sys.stdout", new_callable=io.StringIO):
                    with patch("mcq_types.time.sleep", return_value=None):
                        self.assertEqual(mcq_types.timed_quiz("Enter:", timeout=1), "")


    # Concolic test case 6: Windows path where no keypress occurs until timeout and the function returns None.
    def test_concolic_6_windows_no_keypress_timeout(self):
        fake_msvcrt = types.SimpleNamespace(kbhit=lambda: False, getwch=lambda: "")
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




class TestNegativeMarkQuiz_Concolic(unittest.TestCase):

    # Concolic test case 1: Correct answer path with name=None avoids saving scores
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A"])
    def test_concolic_1_correct_no_save(self, m_input, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name=None, neg_mark=0.25)
        m_save.assert_not_called()


    # Concolic test case 2: Correct answer path with name set triggers to save score
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A"])
    def test_concolic_2_correct_with_save(self, m_input, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="Sam", neg_mark=0.25)
        m_load.assert_called_once()
        m_save.assert_called_once()


    # Concolic test case 3: Blank answer path keeps score unchanged and still saves when name is provided
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=[""])
    def test_concolic_3_blank_answer_branch_saves(self, m_input, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="Nina", neg_mark=0.25)
        m_save.assert_called_once()


    # Concolic test case 4: Wrong non-blank answer applies a negative penalty and saves when name is provided.
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["B"])
    def test_concolic_4_wrong_non_blank_penalty_saves(self, m_input, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="Lee", neg_mark=0.25)
        m_save.assert_called_once()


    # Concolic test case 5: Wrong non-blank with n=1 clamps percentage to 0 via max
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["B"])
    def test_concolic_5_negative_score_percent_clamped_to_zero(self, m_input, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="Zoe", neg_mark=1.0)
        m_save.assert_called_once()


    # Concolic test case 6: Mixed path across multiple questions hits correct, wrong penalty, and blank branches in one run.
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("builtins.input", side_effect=["A", "B", ""])
    def test_concolic_6_mixed_branches_in_one_execution(self, m_input, m_load, m_save):
        qs = ["Q1", "Q2", "Q3"]
        opts = [("A.1", "B.2", "C.3", "D.4")] * 3
        ans = ["A", "A", "A"]
        mcq_types.take_negative_mark_quiz(qs, opts, ans, name="MixUser", neg_mark=0.25)
        m_save.assert_called_once()


class TestChallengeMode_Concolic(unittest.TestCase):

    # Concolic test case 1: Remaining time becomes <= 0 immediately so the challenge exits and saves score
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=["3"])
    @patch("mcq_types.time.time", side_effect=[0, 9999])
    def test_concolic_1_immediate_timeup_saves(self, m_time, m_input, m_shuffle, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User1")
        m_save.assert_called_once()


    # Concolic test case 2: timed quiz returns None, so it exits via 'Time's up while answering' and saves
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("mcq_types.timed_quiz", return_value=None)
    @patch("builtins.input", side_effect=["3"])
    @patch("mcq_types.time.time", side_effect=[0, 0, 1])
    def test_concolic_2_guess_none_branch_saves(
        self, m_time, m_input, m_timed, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User2")
        m_save.assert_called_once()


    # Concolic test case 3: Minutes loop rejects out-of-range and non-numeric inputs before accepting a valid one
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.timed_quiz", return_value=None)
    @patch("builtins.input", side_effect=["10", "abc", "3"])
    @patch("mcq_types.time.time", side_effect=[0, 0, 1])
    def test_concolic_3_minutes_validation_loop_then_run(
        self, m_time, m_input, m_timed, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User3")
        m_save.assert_called_once()


    # Concolic test case 4: One correct answer path is taken before timed_quiz becomes None and exits
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("mcq_types.timed_quiz", side_effect=["A", None])
    @patch("builtins.input", side_effect=["3"])
    @patch("mcq_types.time.time", side_effect=[0, 0, 0, 1])
    def test_concolic_4_one_correct_then_guess_none(
        self, m_time, m_input, m_timed, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User4")
        m_save.assert_called_once()


    # Concolic test case 5: One incorrect answer path is taken before timed_quiz becomes None and exits
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("mcq_types.timed_quiz", side_effect=["B", None])
    @patch("builtins.input", side_effect=["3"])
    @patch("mcq_types.time.time", side_effect=[0, 0, 0, 1])
    def test_concolic_5_one_wrong_then_guess_none(
        self, m_time, m_input, m_timed, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User5")
        m_save.assert_called_once()


    # Concolic test case 6: i hits len(indices), triggering the reshuffle branch before exiting.
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("mcq_types.timed_quiz", side_effect=["A", "A", None])
    @patch("builtins.input", side_effect=["3"])
    @patch("mcq_types.time.time", side_effect=[0, 0, 0, 0, 1])
    def test_concolic_6_wraparound_shuffle_branch(
        self, m_time, m_input, m_timed, m_shuffle, m_load, m_save
    ):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_challenge(qs, opts, ans, name="User6")
        m_save.assert_called_once()


class TestStreakMode_Concolic(unittest.TestCase):

    # Concolic test case 1: All answers correct triggers the 'Amazing!' branch and saves when name is set
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=["A"])
    def test_concolic_1_all_correct_amazing_saves(self, m_input, m_shuffle, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="User1")
        m_save.assert_called_once()


    # Concolic test case 2: First answer wrong and non-blank hits the incorrect branch, breaks early and saves
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=["B"])
    def test_concolic_2_wrong_non_blank_breaks_and_saves(self, m_input, m_shuffle, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="User2")
        m_save.assert_called_once()


    # Concolic test case 3: Blank input hits the 'No answer selected' branch, breaks early and saves
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=[""])
    def test_concolic_3_blank_input_breaks_and_saves(self, m_input, m_shuffle, m_load, m_save):
        qs = ["Q1"]
        opts = [("A.1", "B.2", "C.3", "D.4")]
        ans = ["A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="User3")
        m_save.assert_called_once()


    # Concolic test case 4: One correct then one wrong proves the loop continues before breaking on the first wrong answer
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("builtins.input", side_effect=["A", "B"])
    def test_concolic_4_correct_then_wrong_breaks_and_saves(self, m_input, m_shuffle, m_load, m_save):
        qs = ["Q1", "Q2"]
        opts = [("A.1", "B.2", "C.3", "D.4")] * 2
        ans = ["A", "A"]
        mcq_types.take_quiz_until_wrong(qs, opts, ans, name="User4")
        m_save.assert_called_once()


    # Concolic test case 5: Empty question list forces asked==0 and percent==0 without saving when name is None
    @patch("mcq_types.save_scores")
    @patch("mcq_types.load_scores", return_value=[])
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    def test_concolic_5_zero_questions_no_save(self, m_shuffle, m_load, m_save):
        mcq_types.take_quiz_until_wrong([], [], [], name=None)
        m_save.assert_not_called()


class TestLearningMode_Concolic(unittest.TestCase):

    # Concolic test case 1: User quits immediately so totals stay zero and accuracy is 0%
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "q"])
    def test_concolic_1_quit_immediately(self, m_in, m_out, m_shuffle):
        mcq_types.learning_mode(["Q1"], ["A1"])
        out = m_out.getvalue()
        self.assertIn("Cards reviewed : 0", out)
        self.assertIn("Marked correct : 0", out)
        self.assertIn("Self-rated accuracy: 0%", out)


    # Concolic test case 2: User marks 'y' once so totals increment and accuracy becomes 100%
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "y"])
    def test_concolic_2_yes_once_accuracy_100(self, m_in, m_out, m_shuffle):
        mcq_types.learning_mode(["Q1"], ["A1"])
        out = m_out.getvalue()
        self.assertIn("Cards reviewed : 1", out)
        self.assertIn("Marked correct : 1", out)
        self.assertIn("Self-rated accuracy: 100%", out)


    # Concolic test case 3: User marks 'n' once so totals increment but correct remains 0
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "n"])
    def test_concolic_3_no_once_accuracy_0(self, m_in, m_out, m_shuffle):
        mcq_types.learning_mode(["Q1"], ["A1"])
        out = m_out.getvalue()
        self.assertIn("Cards reviewed : 1", out)
        self.assertIn("Marked correct : 0", out)
        self.assertIn("Self-rated accuracy: 0%", out)


    # Concolic test case 4: Invalid mark forces validation loop, then quitting exits with zero reviewed
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "x", "q"])
    def test_concolic_4_invalid_then_quit(self, m_in, m_out, m_shuffle):
        mcq_types.learning_mode(["Q1"], ["A1"])
        out = m_out.getvalue()
        self.assertIn("Please enter 'y', 'n', or 'q'.", out)
        self.assertIn("Cards reviewed : 0", out)
        self.assertIn("Self-rated accuracy: 0%", out)


    # Concolic test case 5: Two cards where first is 'y' and second is 'q' stops early with one reviewed
    @patch("mcq_types.random.shuffle", side_effect=lambda x: None)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["", "y", "", "q"])
    def test_concolic_5_two_cards_then_quit(self, m_in, m_out, m_shuffle):
        mcq_types.learning_mode(["Q1", "Q2"], ["A1", "A2"])
        out = m_out.getvalue()
        self.assertIn("Cards reviewed : 1", out)
        self.assertIn("Marked correct : 1", out)
        self.assertIn("Self-rated accuracy: 100%", out)



class TestCreateAssessment_Concolic(unittest.TestCase):

    # Concolic test case 1: Take-now is 'n' so assessment saves but quiz is not started
    @patch("manage_assessment.take_quiz")
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    @patch("builtins.input", side_effect=["Assess1", "1", "Q1", "o1", "o2", "o3", "o4","A", "n" ])
    def test_concolic_1_take_now_no(self, m_in, m_load, m_save, m_take):
        manage_assessment.create_assessment()
        m_save.assert_called_once()
        m_take.assert_not_called()


    # Concolic test case 2: Take-now is 'y' so assessment saves and quiz starts immediately
    @patch("manage_assessment.take_quiz")
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    @patch("builtins.input", side_effect=["Assess2","1","Q1", "o1", "o2", "o3", "o4","A", "y"])
    def test_concolic_2_take_now_yes(self, m_in, m_load, m_save, m_take):
        manage_assessment.create_assessment()
        m_save.assert_called_once()
        m_take.assert_called_once()


class TestListAssessments_Concolic(unittest.TestCase):

    # Concolic test case 1: Empty assessments list returns None after printing the 'no assessments' message
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    def test_concolic_1_list_empty_returns_none(self, m_load):
        with patch("sys.stdout", new_callable=io.StringIO):
            self.assertIsNone(manage_assessment.list_assessments())


    # Concolic test case 2: Non-empty assessments list is printed and returned as is
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A", "questions": [], "options": [], "answers": []}])
    def test_concolic_2_list_non_empty_returns_list(self, m_load):
        with patch("sys.stdout", new_callable=io.StringIO):
            out = manage_assessment.list_assessments()
        self.assertIsInstance(out, list)
        self.assertEqual(len(out), 1)


class TestAddQuestion_Concolic(unittest.TestCase):

    # Concolic test case 1: list_assessments returns nothing so the function exits immediately
    @patch("manage_assessment.list_assessments", return_value=None)
    def test_concolic_1_add_question_no_assessments_returns(self, m_list):
        manage_assessment.add_question_to_assessment()


    # Concolic test case 2: Non-numeric selection triggers the exception path and prints 'Invalid input'
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": [], "options": [], "answers": []}])
    @patch("builtins.input", side_effect=["abc"])
    def test_concolic_2_add_question_invalid_selection_string(self, m_in, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.add_question_to_assessment()


    # Concolic test case 3: Valid selection adds a question and calls save_custom_assessments once
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": [], "options": [], "answers": []}])
    @patch("builtins.input", side_effect=["1", "New Q", "oA", "oB", "oC", "oD", "A"])
    def test_concolic_3_add_question_valid_path_saves(self, m_in, m_list, m_save):
        manage_assessment.add_question_to_assessment()
        m_save.assert_called_once()


class TestEditQuestion_Concolic(unittest.TestCase):

    # Concolic test case 1: list_assessments returns nothing so edit exits immediately
    @patch("manage_assessment.list_assessments", return_value=None)
    def test_concolic_1_edit_no_assessments_returns(self, m_list):
        manage_assessment.edit_question_in_assessment()


    # Concolic test case 2: Non-numeric assessment selection triggers the invalid selection branch
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["abc"])
    def test_concolic_2_edit_invalid_assessment_selection(self, m_in, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.edit_question_in_assessment()


    # Concolic test case 3: Non-numeric question number triggers the invalid input branch
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1", "abc"])
    def test_concolic_3_edit_invalid_question_number_input(self, m_in, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.edit_question_in_assessment()


    # Concolic test case 4: Out-of-range question index triggers the invalid selection branch
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1", "99"])
    def test_concolic_4_edit_question_index_out_of_range(self, m_in, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.edit_question_in_assessment()


    # Concolic test case 5: Valid edit where user keeps question and answer unchanged but still saves
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1", "1", "", "", "", "", "", ""])
    def test_concolic_5_edit_keep_existing_fields_saves(self, m_in, m_list, m_save):
        manage_assessment.edit_question_in_assessment()
        m_save.assert_called_once()


    # Concolic test case 6: Valid edit where question and answer are both updated and saved
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1", "1", "New Q1", "", "", "", "", "B"])
    def test_concolic_6_edit_updates_question_and_answer(self, m_in, m_list, m_save):
        manage_assessment.edit_question_in_assessment()
        m_save.assert_called_once()


class TestDeleteQuestion_Concolic(unittest.TestCase):

    # Concolic test case 1: list_assessments returns nothing so delete exits immediately
    @patch("manage_assessment.list_assessments", return_value=None)
    def test_concolic_1_delete_no_assessments_returns(self, m_list):
        manage_assessment.delete_question_from_assessment()


    # Concolic test case 2: Non-numeric assessment selection triggers the invalid input branch
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["abc"])
    def test_concolic_2_delete_invalid_assessment_selection(self, m_in, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.delete_question_from_assessment()


    # Concolic test case 3: Non-numeric question selection triggers the invalid input branch
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1", "abc"])
    def test_concolic_3_delete_invalid_question_number_input(self, m_in, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.delete_question_from_assessment()


    # Concolic test case 4: Out-of-range question index triggers the invalid selection branch
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1", "99"])
    def test_concolic_4_delete_question_index_out_of_range(self, m_in, m_list):
        with patch("sys.stdout", new_callable=io.StringIO):
            manage_assessment.delete_question_from_assessment()


    # Concolic test case 5: Valid delete removes the question and saves the updated assessment list
    @patch("manage_assessment.save_custom_assessments")
    @patch("manage_assessment.list_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1", "1"])
    def test_concolic_5_delete_valid_path_saves(self, m_in, m_list, m_save):
        manage_assessment.delete_question_from_assessment()
        m_save.assert_called_once()


class TestViewQuestions_Concolic(unittest.TestCase):

    # Concolic test case 1: No saved assessments triggers the early 'No assessments saved yet' return.
    @patch("manage_assessment.load_custom_assessments", return_value=[])
    def test_concolic_1_no_assessments_returns_early(self, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            self.assertIn("No assessments saved yet.", buf.getvalue())


    # Concolic test case 2: Non-numeric selection causes ValueError and prints 'Invalid input'
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A"}])
    @patch("builtins.input", side_effect=["abc"])
    def test_concolic_2_invalid_input_value_error(self, m_in, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            self.assertIn("Invalid input.", buf.getvalue())


    # Concolic test case 3: Out-of-range positive selection prints 'Invalid selection'
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A"}])
    @patch("builtins.input", side_effect=["99"])
    def test_concolic_3_out_of_range_selection_high(self, m_in, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            self.assertIn("Invalid selection.", buf.getvalue())


    # Concolic test case 4: Selection “0” produces k=-1 and prints 'Invalid selection'
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A"}])
    @patch("builtins.input", side_effect=["0"])
    def test_concolic_4_out_of_range_selection_negative(self, m_in, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            self.assertIn("Invalid selection.", buf.getvalue())


    # Concolic test case 5: Valid assessment but empty questions prints 'This assessment has no questions yet'
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A", "questions": [], "options": [], "answers": []}])
    @patch("builtins.input", side_effect=["1"])
    def test_concolic_5_valid_selection_but_no_questions(self, m_in, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            self.assertIn("This assessment has no questions yet.", buf.getvalue())


    # Concolic test case 6: Normal path prints question text and correct answer when lists exist
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A", "questions": ["Q1"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1"])
    def test_concolic_6_prints_questions_and_answers(self, m_in, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            out = buf.getvalue()
            self.assertIn("Q1", out)
            self.assertIn("Correct answer: A", out)


    # Concolic test case 7: Options list shorter than questions skips option printing for later questions safely
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A", "questions": ["Q1", "Q2"], "options": [("A.1","B.2","C.3","D.4")], "answers": ["A", "B"]}])
    @patch("builtins.input", side_effect=["1"])
    def test_concolic_7_options_shorter_than_questions(self, m_in, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            out = buf.getvalue()
            self.assertIn("Q1: Q1", out)
            self.assertIn("Q2: Q2", out)
            self.assertIn("Correct answer: A", out)
            self.assertIn("Correct answer: B", out)


    # Concolic test case 8: Answers list shorter than questions skips answer printing for later questions safely
    @patch("manage_assessment.load_custom_assessments", return_value=[{"name": "A", "questions": ["Q1", "Q2"], "options": [("A.1","B.2","C.3","D.4"), ("A.x","B.y","C.z","D.w")], "answers": ["A"]}])
    @patch("builtins.input", side_effect=["1"])
    def test_concolic_8_answers_shorter_than_questions(self, m_in, m_load):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            manage_assessment.view_questions_in_assessment()
            out = buf.getvalue()
            self.assertIn("Q1: Q1", out)
            self.assertIn("Q2: Q2", out)
            self.assertIn("Correct answer: A", out)


if __name__ == "__main__":
    unittest.main()
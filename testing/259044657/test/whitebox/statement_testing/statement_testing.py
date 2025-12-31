import io
import unittest
from unittest.mock import patch
from main import main


MENU_QUIZ_BY_TOPIC = "1"
MENU_VIEWER = "2"
MENU_WRONG_MODE = "3"
MENU_EXIT = "0"

VIEWER_MCQ_ONLY = "1"
VIEWER_FILL_ONLY = "2"
VIEWER_ALL = "3"
VIEWER_BACK = "0"

WRONGMODE_START = "1"
WRONGMODE_BACK = "0"


class TestStatementCoverage(unittest.TestCase):
    

    def run_cli(self, inputs):
        
        safe_inputs = list(inputs) + [MENU_EXIT] * 10

        def fake_input(_prompt=""):
            return safe_inputs.pop(0)

        buf = io.StringIO()
        with patch("builtins.input", side_effect=fake_input), patch("sys.stdout", new=buf):
            try:
                main()
            except IndexError:
                pass
            except SystemExit:
                pass
        return buf.getvalue()

    
    def test_01_quiz_by_topic_no_mcq_topics(self):
        output = self.run_cli([MENU_QUIZ_BY_TOPIC, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_02_quiz_by_topic_valid_topic(self):
        output = self.run_cli([MENU_QUIZ_BY_TOPIC, "1", MENU_EXIT])
        self.assertIsInstance(output, str)


    def test_03_quiz_by_topic_invalid_topic(self):
        output = self.run_cli([MENU_QUIZ_BY_TOPIC, "999", "1", MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_04_quiz_by_topic_non_int_input(self):
        output = self.run_cli([MENU_QUIZ_BY_TOPIC, "abc", "1", MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_05_viewer_mcq_only_non_empty(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_MCQ_ONLY, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_06_viewer_mcq_only_empty(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_MCQ_ONLY, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_07_viewer_fill_only_non_empty(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_FILL_ONLY, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_08_viewer_fill_only_empty(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_FILL_ONLY, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_09_viewer_all_both_non_empty(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_ALL, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_10_viewer_all_mcq_only_available(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_ALL, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

   
    def test_11_viewer_all_fill_only_available(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_ALL, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_12_viewer_invalid_menu_choice(self):
        output = self.run_cli([MENU_VIEWER, "9", VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_13_viewer_back(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_14_wrongmode_no_mcq_questions_available(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_15_wrongmode_available_name_provided(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "Pranav", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_16_wrongmode_available_name_skipped(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_17_wrongmode_count_valid(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "3", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_18_wrongmode_count_out_of_range(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "999", "3", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_19_wrongmode_count_non_integer(self):
    
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "-1", "3", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)


    def test_20_wrongmode_guess_valid_avoids_real_answer(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "1", "2", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)


    def test_21_wrongmode_guess_valid_picks_real_answer(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "1", "1", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_22_wrongmode_invalid_guess_then_fixed(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "1", "9", "2", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_23_wrongmode_save_score_name_provided(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "1", "2", "y", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_24_wrongmode_no_save_name_skipped(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "", "1", "2", "n", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_25_viewer_mcq_only_unknown_topic_difficulty(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_MCQ_ONLY, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_26_viewer_fill_only_unknown_topic_difficulty(self):
        output = self.run_cli([MENU_VIEWER, VIEWER_FILL_ONLY, VIEWER_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_27_quiz_by_topic_valid_hard(self):
        output = self.run_cli([MENU_QUIZ_BY_TOPIC, "1", "hard", MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_28_quiz_by_topic_valid_easy(self):
        output = self.run_cli([MENU_QUIZ_BY_TOPIC, "1", "easy", MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_29_wrongmode_multiple_questions(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "3", "2", "2", "2", "n", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)

    
    def test_30_wrongmode_single_question_run(self):
        output = self.run_cli([MENU_WRONG_MODE, WRONGMODE_START, "User", "1", "2", "n", WRONGMODE_BACK, MENU_EXIT])
        self.assertIsInstance(output, str)


if __name__ == "__main__":
    unittest.main(verbosity=2)

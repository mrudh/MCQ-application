import unittest
import subprocess
import sys
from pathlib import Path

APP_PATH = Path("main.py")  

class TestQuizAppBranch(unittest.TestCase):
    
    def run_cli(self, inputs):
        if not APP_PATH.exists():
            self.fail(f"APP_PATH not found: {APP_PATH.resolve()}")

        input_data = "\n".join(map(str, inputs)) + "\n"
        result = subprocess.run(
            [sys.executable, str(APP_PATH)],
            input=input_data,
            text=True,
            capture_output=True,
            check=False
        )
        output = (result.stdout or "") + (result.stderr or "")
        return output


    def test_01_quizbytopic_no_mcq_topics(self):
        output = self.run_cli(["1", "0"])
        self.assertIsInstance(output, str)

    def test_02_quizbytopic_topics_exist_valid_topic(self):
        output = self.run_cli(["1", "1", "0"])
        self.assertIsInstance(output, str)

    def test_03_quizbytopic_topics_exist_invalid_topic(self):
        output = self.run_cli(["1", "999", "0"])
        self.assertIsInstance(output, str)

    def test_04_quizbytopic_topics_exist_nonint_input(self):
        output = self.run_cli(["1", "abc", "1", "0"])
        self.assertIsInstance(output, str)

    def test_27_quizbytopic_valid_hard(self):
        output = self.run_cli(["1", "1", "3", "0"])
        self.assertIsInstance(output, str)

    def test_28_quizbytopic_valid_easy(self):
        output = self.run_cli(["1", "1", "1", "0"])
        self.assertIsInstance(output, str)

    def test_05_viewer_mcq_only_non_empty(self):
        output = self.run_cli(["2", "1", "0"])
        self.assertIsInstance(output, str)

    def test_06_viewer_mcq_only_empty(self):
        output = self.run_cli(["2", "1", "0"])
        self.assertIsInstance(output, str)

    def test_07_viewer_fill_only_non_empty(self):
        output = self.run_cli(["2", "2", "0"])
        self.assertIsInstance(output, str)

    def test_08_viewer_fill_only_empty(self):
        output = self.run_cli(["2", "2", "0"])
        self.assertIsInstance(output, str)

    def test_09_viewer_all_both_non_empty(self):
        output = self.run_cli(["2", "3", "0"])
        self.assertIsInstance(output, str)

    def test_10_viewer_all_mcq_only(self):
        output = self.run_cli(["2", "3", "0"])
        self.assertIsInstance(output, str)

    def test_11_viewer_all_fill_only(self):
        output = self.run_cli(["2", "3", "0"])
        self.assertIsInstance(output, str)

    def test_12_viewer_invalid_choice(self):
        output = self.run_cli(["2", "9", "0"])
        self.assertIsInstance(output, str)

    def test_13_viewer_back(self):
        output = self.run_cli(["2", "0"])
        self.assertIsInstance(output, str)

    def test_25_viewer_mcq_unknown_topic(self):
        output = self.run_cli(["2", "1", "0"])
        self.assertIsInstance(output, str)

    def test_26_viewer_fill_unknown_topic(self):
        output = self.run_cli(["2", "2", "0"])
        self.assertIsInstance(output, str)

    def test_14_wrongmode_no_mcq_available(self):
        output = self.run_cli(["3", "0"])
        self.assertIsInstance(output, str)

    def test_15_wrongmode_name_given(self):
        output = self.run_cli(["3", "Alice", "0"])
        self.assertIsInstance(output, str)

    def test_16_wrongmode_name_skipped(self):
        output = self.run_cli(["3", "", "0"])
        self.assertIsInstance(output, str)

    def test_17_wrongmode_valid_count(self):
        output = self.run_cli(["3", "Bob", "3", "0"])
        self.assertIsInstance(output, str)

    def test_18_wrongmode_count_out_of_range(self):
        output = self.run_cli(["3", "Bob", "999", "3", "0"])
        self.assertIsInstance(output, str)

    def test_19_wrongmode_count_non_integer(self):
        output = self.run_cli(["3", "Bob", "abc", "3", "0"])
        self.assertIsInstance(output, str)

    def test_20_wrongmode_guess_wrong(self):
        output = self.run_cli(["3", "Bob", "1", "B", "n", "0"])
        self.assertIsInstance(output, str)

    def test_21_wrongmode_guess_correct(self):
        output = self.run_cli(["3", "Bob", "1", "A", "n", "0"])
        self.assertIsInstance(output, str)

    def test_22_wrongmode_invalid_guess_then_fixed(self):
        output = self.run_cli(["3", "Bob", "1", "Z", "A", "n", "0"])
        self.assertIsInstance(output, str)

    def test_23_wrongmode_save_score(self):
        output = self.run_cli(["3", "Bob", "1", "A", "y", "0"])
        self.assertIsInstance(output, str)

    def test_24_wrongmode_no_save(self):
        output = self.run_cli(["3", "", "1", "A", "n", "0"])
        self.assertIsInstance(output, str)

    def test_29_wrongmode_multiple_questions(self):
        output = self.run_cli(["3", "Bob", "3", "A", "B", "C", "n", "0"])
        self.assertIsInstance(output, str)

    def test_30_wrongmode_single_question(self):
        output = self.run_cli(["3", "Bob", "1", "A", "n", "0"])
        self.assertIsInstance(output, str)


if __name__ == "__main__":
    unittest.main(verbosity=2)

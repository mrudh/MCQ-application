import unittest
from unittest.mock import patch
from mcq import fifty_fifty_quiz
MODULE = "mcq"


class TestFiftyFiftyQuiz_FromTSLFrames(unittest.TestCase):
   

    def make_options(self, four_options: bool, correct_found: bool):
        
        if four_options:
            opts = ["A. OptA", "B. OptB", "C. OptC", "D. OptD"]
        else:
            opts = ["A. OptA", "B. OptB", "C. OptC"]

        if correct_found:
            answer = "A"
        else:
            answer = "D"

        return opts, answer

    def expected_percent(self, guess_correct: bool) -> int:
        return 100 if guess_correct else 0

    def test_all_32_tsl_frames(self):
        question = ["Q1?"]

        lifeline_choices = ["not_used", "used"]
        options_configs = ["four", "lt_four"]
        correct_detection = ["found", "missing"]
        user_guess_cases = ["correct", "incorrect"]
        name_cases = ["no_name", "has_name"]

        for lifeline in lifeline_choices:
            for opt_cfg in options_configs:
                for correct_case in correct_detection:
                    for guess_case in user_guess_cases:
                        for name_case in name_cases:
                            with self.subTest(
                                lifeline=lifeline,
                                opt_cfg=opt_cfg,
                                correct_case=correct_case,
                                guess_case=guess_case,
                                name_case=name_case
                            ):
                               
                                four_options = (opt_cfg == "four")
                                correct_found = (correct_case == "found")

                                opts, answer = self.make_options(four_options, correct_found)
                                options = [opts]
                                answers = [answer]

                      
                                lifeline_input = "" if lifeline == "not_used" else "F"

                              
                                if guess_case == "correct":
                                    guess_input = answer
                                    guess_correct = True
                                else:
                                    guess_input = "B" if answer != "B" else "A"
                                    guess_correct = False

              
                                name = None if name_case == "no_name" else "Sarthak"

                                
                                input_sequence = [lifeline_input, guess_input]

                                
                                patches = [
                                    patch(f"{MODULE}.random.choice", side_effect=lambda seq: seq[0]),
                                    patch("builtins.input", side_effect=input_sequence),
                                    patch("builtins.print") 
                                ]

                        
                                if name is not None:
                                    patches.append(patch(f"{MODULE}.load_scores", return_value=[]))
                                    save_scores_mock = patch(f"{MODULE}.save_scores").start()
                                else:
                                    save_scores_mock = None

  
                                started = []
                                try:
                                    for p in patches:
                                        started.append(p.start())


                                    fifty_fifty_quiz(question, options, answers, name=name)

                                    expected = self.expected_percent(guess_correct)

                                    if name is None:
                   
                                        pass
                                    else:
                                       
                                        self.assertTrue(save_scores_mock.called, "save_scores should be called when name is provided")
                                        saved_arg = save_scores_mock.call_args[0][0]
                                        self.assertIsInstance(saved_arg, list)
                                        self.assertGreaterEqual(len(saved_arg), 1)
                                        self.assertEqual(saved_arg[-1]["name"], "Sarthak")
                                        self.assertEqual(saved_arg[-1]["score"], expected)

                                finally:
                                    if save_scores_mock is not None:
                                        patch(f"{MODULE}.save_scores").stop()

                                    for p in reversed(patches):
                                        try:
                                            p.stop()
                                        except Exception:
                                            pass


if __name__ == "__main__":
    unittest.main()

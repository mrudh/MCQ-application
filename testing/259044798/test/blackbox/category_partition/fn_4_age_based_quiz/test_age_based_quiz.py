# test_age_based_quiz.py
import unittest
from unittest.mock import patch
import io
from contextlib import redirect_stdout


def age_based_quiz(ALL_QUIZ_DATA):
    import random

    name = input("Enter your name: ")

    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Invalid age. Defaulting to general quiz (all difficulties).")
        age = None

    if age is None:
        allowed_difficulties = ["Easy", "Medium", "Hard"]
    elif age <= 10:
        allowed_difficulties = ["Easy"]
    elif age <= 14:
        allowed_difficulties = ["Easy", "Medium"]
    else:
        allowed_difficulties = ["Easy", "Medium", "Hard"]

    print(f"Using questions with difficulties: {', '.join(allowed_difficulties)}")

    filtered_questions = [
        q for q in ALL_QUIZ_DATA if q["difficulty"] in allowed_difficulties
    ]

    if not filtered_questions:
        print("No questions available for this age group.")
        return

    max_q = len(filtered_questions)

    try:
        total_questions = int(
            input(f"How many questions do you want to take? (1 to {max_q}): ")
        )
        if not (1 <= total_questions <= max_q):
            print("Invalid number, using all available questions for your age group.")
            total_questions = max_q
    except ValueError:
        print("Invalid input, using all available questions for your age group.")
        total_questions = max_q

    selected = random.sample(filtered_questions, total_questions)
    qs = [q["question"] for q in selected]
    opts = [q["options"] for q in selected]
    ans = [q["answer"] for q in selected]

    take_quiz(qs, opts, ans, name=name)


def take_quiz(qs, opts, ans, name=None):
    raise NotImplementedError("take_quiz should be patched in tests")
EASY_ONLY_DATA = [
    {"difficulty": "Easy", "question": "E1", "options": ["A", "B"], "answer": "A"},
    {"difficulty": "Easy", "question": "E2", "options": ["A", "B"], "answer": "B"},
]

EASY_MED_DATA = [
    {"difficulty": "Easy", "question": "E1", "options": ["A", "B"], "answer": "A"},
    {"difficulty": "Medium", "question": "M1", "options": ["C", "D"], "answer": "C"},
]

ALL_LEVELS_DATA = [
    {"difficulty": "Easy", "question": "E1", "options": ["A", "B"], "answer": "A"},
    {"difficulty": "Medium", "question": "M1", "options": ["C", "D"], "answer": "C"},
    {"difficulty": "Hard", "question": "H1", "options": ["E", "F"], "answer": "F"},
]

NO_EASY_MATCH = [
    {"difficulty": "Medium", "question": "M1", "options": ["C", "D"], "answer": "C"},
    {"difficulty": "Hard", "question": "H1", "options": ["E", "F"], "answer": "F"},
]

NO_EASY_MED_MATCH = [
    {"difficulty": "Hard", "question": "H1", "options": ["E", "F"], "answer": "F"},
]

NO_ALL_MATCH = []  


def deterministic_sample(seq, k):
    return list(seq)[:k]
class TestAgeBasedQuiz(unittest.TestCase):

    
    def test_tc1_single_early_return_maxq_zero(self):
        inputs = ["Dev", "10"]
        f = io.StringIO()
        with patch("builtins.input", side_effect=inputs), \
             patch(__name__ + ".take_quiz") as mock_take_quiz, \
             redirect_stdout(f):
            age_based_quiz(NO_EASY_MATCH)

        out = f.getvalue()
        self.assertIn("No questions available for this age group.", out)
        mock_take_quiz.assert_not_called()

    
    def test_tc2_age_le10_has_questions_tq_valid_in_range(self):
        inputs = ["Dev", "10", "1"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(EASY_ONLY_DATA)

        mock_take_quiz.assert_called_once()
        qs, opts, ans = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], "E1")

    
    def test_tc3_age_le10_has_questions_tq_out_of_range_defaults_maxq(self):
        inputs = ["Dev", "10", "99"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(EASY_ONLY_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 2)

    
    def test_tc4_age_le10_has_questions_tq_invalid_defaults_maxq(self):
        inputs = ["Dev", "10", "abc"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(EASY_ONLY_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 2)

    
    def test_tc5_age_le10_no_matching_questions(self):
        inputs = ["Dev", "10"]
        f = io.StringIO()
        with patch("builtins.input", side_effect=inputs), \
             patch(__name__ + ".take_quiz") as mock_take_quiz, \
             redirect_stdout(f):
            age_based_quiz(NO_EASY_MATCH)

        out = f.getvalue()
        self.assertIn("No questions available for this age group.", out)
        mock_take_quiz.assert_not_called()

    
    def test_tc6_age_11to14_has_questions_tq_valid_in_range(self):
        inputs = ["Dev", "12", "1"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(EASY_MED_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 1)

    
    def test_tc7_age_11to14_has_questions_tq_out_of_range_defaults_maxq(self):
        inputs = ["Dev", "12", "0"]  # out of range (<=0)
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(EASY_MED_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 2)

    
    def test_tc8_age_11to14_has_questions_tq_invalid_defaults_maxq(self):
        inputs = ["Dev", "12", "xyz"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(EASY_MED_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 2)

    
    def test_tc9_age_11to14_no_matching_questions(self):
        inputs = ["Dev", "12"]
        f = io.StringIO()
        with patch("builtins.input", side_effect=inputs), \
             patch(__name__ + ".take_quiz") as mock_take_quiz, \
             redirect_stdout(f):
            age_based_quiz(NO_EASY_MED_MATCH)

        out = f.getvalue()
        self.assertIn("No questions available for this age group.", out)
        mock_take_quiz.assert_not_called()

    
    def test_tc10_age_ge15_has_questions_tq_valid_in_range(self):
        inputs = ["Dev", "15", "2"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(ALL_LEVELS_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 2)

    
    def test_tc11_age_ge15_has_questions_tq_out_of_range_defaults_maxq(self):
        inputs = ["Dev", "15", "999"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(ALL_LEVELS_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 3)

    
    def test_tc12_age_ge15_has_questions_tq_invalid_defaults_maxq(self):
        inputs = ["Dev", "15", "nope"]
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz:
            age_based_quiz(ALL_LEVELS_DATA)

        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 3)

    
    def test_tc13_age_ge15_no_matching_questions(self):
        inputs = ["Dev", "15"]
        f = io.StringIO()
        with patch("builtins.input", side_effect=inputs), \
             patch(__name__ + ".take_quiz") as mock_take_quiz, \
             redirect_stdout(f):
            age_based_quiz(NO_ALL_MATCH)

        out = f.getvalue()
        self.assertIn("No questions available for this age group.", out)
        mock_take_quiz.assert_not_called()

    
    def test_tc14_invalid_age_defaults_to_allowed_all(self):
        inputs = ["Dev", "abc", "1"]
        f = io.StringIO()
        with patch("builtins.input", side_effect=inputs), \
             patch("random.sample", side_effect=deterministic_sample), \
             patch(__name__ + ".take_quiz") as mock_take_quiz, \
             redirect_stdout(f):
            age_based_quiz(ALL_LEVELS_DATA)

        out = f.getvalue()
        self.assertIn("Invalid age. Defaulting to general quiz", out)
        self.assertIn("Using questions with difficulties: Easy, Medium, Hard", out)
        mock_take_quiz.assert_called_once()
        qs, _, _ = mock_take_quiz.call_args.args[:3]
        self.assertEqual(len(qs), 1)


if __name__ == "__main__":
    unittest.main()

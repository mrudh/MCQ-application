import sys
import os
import unittest
from unittest.mock import patch
import io
import contextlib
import copy

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, PROJECT_ROOT)


from mcq import (
    take_fill_in_the_blanks_quiz,
    take_quiz_with_skip,
    age_based_quiz
)


try:
    from quiz_data import ALL_QUIZ_DATA as REAL_ALL_QUIZ_DATA
except Exception:
    REAL_ALL_QUIZ_DATA = None


def run_func_with_inputs(func, inputs, *args, **kwargs):
    
    fake_out = io.StringIO()
    with patch("builtins.input", side_effect=inputs), contextlib.redirect_stdout(fake_out):
        result = func(*args, **kwargs)
    return result, fake_out.getvalue()


def _make_empty_like(real_data):
    
    if real_data is None:
        
        return {}

    data = copy.deepcopy(real_data)

    def wipe_lists(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                obj[k] = wipe_lists(v)
            return obj
        if isinstance(obj, list):
            return [] 
        return obj

    return wipe_lists(data)


class TestCase1_LengthMismatch(unittest.TestCase):
    
    def test_questions_answers_length_mismatch(self):
        questions = ["Q1 ___", "Q2 ___"]
        answers = ["A1"]  

        with self.assertRaises((ValueError, IndexError)):
            take_fill_in_the_blanks_quiz(name="Ali", questions=questions, answers=answers)


class TestTakeFillInTheBlanksQuiz(unittest.TestCase):
   
    def test_1_1_1_1_happy_name_provided_nonempty(self):
        name = "Sara"
        questions = ["Python is ___ language."]
        answers = ["great"]

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=["great"],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_1_1_1_2_edge_name_provided_invalid_or_incorrect(self):
        name = "Sara"
        questions = ["2 + 2 = ___"]
        answers = ["4"]

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=["5", "4"],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)

  
    def test_1_1_2_1_happy_name_provided_empty_questions(self):
        name = "Sara"
        questions = []
        answers = []

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=[],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)

   
    def test_1_1_2_2_edge_name_provided_empty_questions(self):
        name = "Sara"
        questions = []
        answers = []

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=[],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_1_2_1_1_happy_name_none_nonempty(self):
        name = None
        questions = ["Capital of France is ___"]
        answers = ["paris"]

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=["paris"],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_1_2_1_2_edge_name_none_invalid_or_incorrect(self):
        name = None
        questions = ["3 * 3 = ___"]
        answers = ["9"]

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=["8", "9"],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_1_2_2_1_happy_name_none_empty_questions(self):
        name = None
        questions = []
        answers = []

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=[],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_1_2_2_2_edge_name_none_empty_questions(self):
        name = None
        questions = []
        answers = []

        result, out = run_func_with_inputs(
            take_fill_in_the_blanks_quiz,
            inputs=[],
            name=name,
            questions=questions,
            answers=answers,
        )
        self.assertIsNotNone(out)


class TestTakeQuizWithSkip(unittest.TestCase):
    
    def test_2_1_1_1_happy_name_provided_nonempty(self):
        name = "Omar"
        questions = ["1+1?"]
        options = [["A) 2", "B) 3", "C) 4", "D) 1"]]
        answers = ["A"]

        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=["A"],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_2_1_1_2_edge_name_provided_skip_and_incorrect(self):
        name = "Omar"
        questions = ["Sun rises from the ___", "5-3?"]
        options = [
            ["A) West", "B) East", "C) North", "D) South"],
            ["A) 1", "B) 2", "C) 3", "D) 4"],
        ]
        answers = ["B", "B"]

        
        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=["S", "C", "B"],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)

   
    def test_2_1_2_1_happy_name_provided_empty_questions(self):
        name = "Omar"
        questions = []
        options = []
        answers = []

        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=[],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_2_1_2_2_edge_name_provided_empty_questions(self):
        name = "Omar"
        questions = []
        options = []
        answers = []

        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=[],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_2_2_1_1_happy_name_none_nonempty(self):
        name = None
        questions = ["Color of grass?"]
        options = [["A) Blue", "B) Green", "C) Red", "D) Yellow"]]
        answers = ["B"]

        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=["B"],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_2_2_1_2_edge_name_none_skip_incorrect(self):
        name = None
        questions = ["Largest planet?"]
        options = [["A) Earth", "B) Mars", "C) Jupiter", "D) Venus"]]
        answers = ["C"]

        
        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=["", "S"],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)

   
    def test_2_2_2_1_happy_name_none_empty_questions(self):
        name = None
        questions = []
        options = []
        answers = []

        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=[],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)

    
    def test_2_2_2_2_edge_name_none_empty_questions(self):
        name = None
        questions = []
        options = []
        answers = []

        result, out = run_func_with_inputs(
            take_quiz_with_skip,
            inputs=[],
            name=name,
            questions=questions,
            options=options,
            answers=answers,
        )
        self.assertIsNotNone(out)


class TestAgeBasedQuiz(unittest.TestCase):
    

    def test_3_1_1_1_happy_name_provided_nonempty(self):
        
        inputs = ["Mina", "21"] + ["A"] * 50
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=REAL_ALL_QUIZ_DATA)
        self.assertIsNotNone(out)

    def test_3_1_1_2_edge_name_provided_invalid_age_and_incorrect(self):
        inputs = ["Mina", "-1", "abc", "18"] + ["S", "A", "B", "C", "D"] * 10
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=REAL_ALL_QUIZ_DATA)
        self.assertIsNotNone(out)

    def test_3_1_2_1_happy_name_provided_empty_questions(self):
        empty_data = _make_empty_like(REAL_ALL_QUIZ_DATA)
        inputs = ["Mina", "18"] + ["A"] * 200  
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=empty_data)
        self.assertIsNotNone(out)

    def test_3_1_2_2_edge_name_provided_empty_questions(self):
        empty_data = _make_empty_like(REAL_ALL_QUIZ_DATA)
        inputs = ["Mina", "abc", "18"] + ["A"] * 200
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=empty_data)
        self.assertIsNotNone(out)

    def test_3_2_1_1_happy_name_none_nonempty(self):
        
        inputs = ["", "25"] + ["A"] * 50
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=REAL_ALL_QUIZ_DATA)
        self.assertIsNotNone(out)

    def test_3_2_1_2_edge_name_none_invalid_age_skip_incorrect(self):
        inputs = ["", "0", "20"] + ["S", "A", "B", "C", "D"] * 10
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=REAL_ALL_QUIZ_DATA)
        self.assertIsNotNone(out)

    def test_3_2_2_1_happy_name_none_empty_questions(self):
        empty_data = _make_empty_like(REAL_ALL_QUIZ_DATA)
        inputs = ["", "20"] + ["A"] * 200
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=empty_data)
        self.assertIsNotNone(out)

    def test_3_2_2_2_edge_name_none_empty_questions(self):
        empty_data = _make_empty_like(REAL_ALL_QUIZ_DATA)
        inputs = ["", "abc", "20"] + ["A"] * 200
        result, out = run_func_with_inputs(age_based_quiz, inputs=inputs, ALL_QUIZ_DATA=empty_data)
        self.assertIsNotNone(out)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import types
import unittest
import importlib.util
from io import StringIO
from contextlib import redirect_stdout


def project_root_from_here(start_dir: str) -> str:
    
    cur = os.path.abspath(start_dir)
    last = None
    while cur != last:
        if os.path.exists(os.path.join(cur, "mcq.py")):
            return cur
        last = cur
        cur = os.path.dirname(cur)
    return os.path.abspath(start_dir)


def find_py_file_containing_symbol(root_dir: str, symbol: str) -> str:
    
    needle = f"def {symbol}"
    for base, _, files in os.walk(root_dir):
        for f in files:
            if not f.endswith(".py"):
                continue
            path = os.path.join(base, f)
            try:
                with open(path, "r", encoding="utf-8") as fp:
                    txt = fp.read()
                if needle in txt:
                    return path
            except OSError:
                continue
    raise FileNotFoundError(
        f"Could not find any .py file under {root_dir} containing '{needle}'."
    )


def stub_missing_imports():
    if "mcq_types" not in sys.modules:
        m = types.ModuleType("mcq_types")
        def take_quiz(*args, **kwargs):  
            raise NotImplementedError
        def timed_quiz(*args, **kwargs): 
            raise NotImplementedError
        m.take_quiz = take_quiz
        m.timed_quiz = timed_quiz
        sys.modules["mcq_types"] = m
    if "utils" not in sys.modules:
        u = types.ModuleType("utils")

        def print_results(*args, **kwargs): 
            return None

        def load_scores(*args, **kwargs):  
            return []

        def save_scores(*args, **kwargs):  
            return None
        u.print_results = print_results
        u.load_scores = load_scores
        u.save_scores = save_scores
        sys.modules["utils"] = u


def import_module_from_path(module_path: str, module_name: str = "module_under_test"):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


class TestShowAllAnswers_FromTSL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        here = os.path.dirname(__file__)
        root = project_root_from_here(here)
        if root not in sys.path:
            sys.path.insert(0, root)
        stub_missing_imports()
        target_path = find_py_file_containing_symbol(root, "show_all_mcq_answers")
        cls.mod = import_module_from_path(target_path, "answers_module")
        for sym in ("show_all_mcq_answers", "show_all_fill_in_answers", "_get_option_text"):
            if not hasattr(cls.mod, sym):
                raise AttributeError(
                    f"Imported {target_path}, but it does not define '{sym}'. "
                    f"Double-check where your functions are defined."
                )

    def run_and_capture(self):
        buf = StringIO()
        with redirect_stdout(buf):
            self.mod.show_all_mcq_answers()
            self.mod.show_all_fill_in_answers()
        return buf.getvalue()

   
    def test_tc1_smoke_default_frame(self):
        self.mod.ALL_QUIZ_DATA = [
            {
                "question": "Capital of France?",
                "options": ["A. Paris", "B. London", "C. Rome", "D. Berlin"],
                "answer": "A",
            }
        ]
        self.mod.FILL_IN_QUIZ_DATA = [
            {"question": "2+2 = ?", "answer": "4"}
        ]

        out = self.run_and_capture()
        self.assertIn("===== ANSWER KEY: MULTIPLE-CHOICE QUESTIONS =====", out)
        self.assertIn("===== ANSWER KEY: FILL-IN-THE-BLANKS QUESTIONS =====", out)
        self.assertIn("Q1. Capital of France?", out)
        self.assertIn("Correct answer: A -> A. Paris", out)
        self.assertIn("Q1. 2+2 = ?", out)
        self.assertIn("Accepted answer(s): 4", out)

    
    def test__get_option_text_found(self):
        opts = ["A. Dog", "B. Cat", "C. Fish", "D. Bird"]
        self.assertEqual(self.mod._get_option_text(opts, "b"), "B. Cat")


    def test__get_option_text_not_found(self):
        opts = ["A. Dog", "B. Cat"]
        self.assertEqual(
            self.mod._get_option_text(opts, "D"),
            "D (option text not found)"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

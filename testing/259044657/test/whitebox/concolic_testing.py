import os
import sys
import unittest
import subprocess
from pathlib import Path

from z3 import Int, Solver, sat

APP_PATH = Path("main.py")

MAIN_MENU_QUIZ_MODES = "2"
MAIN_MENU_REVIEW_TOOLS = "4"

QUIZ_MODES_WRONG_ANSWER = "10"
REVIEW_TOOLS_SEE_ALL_QUESTIONS = "4"


def run_app_with_inputs(inputs):
    
    joined = "\n".join(inputs) + "\n"

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    proc = subprocess.run(
        [sys.executable, str(APP_PATH)],
        input=joined,
        text=True,
        capture_output=True,
        env=env,
        timeout=25,
    )
    return (proc.stdout or "") + (proc.stderr or "")


def z3_pick_valid_count(min_v=1, max_v=30):
    x = Int("x")
    s = Solver()
    s.add(x >= min_v, x <= max_v)
    assert s.check() == sat
    m = s.model()
    return str(m[x].as_long())


def z3_pick_invalid_count(min_v=1, max_v=30):
    
    x = Int("x")
    s = Solver()
    s.add((x < min_v) | (x > max_v))
    assert s.check() == sat
    m = s.model()
    return str(m[x].as_long())


class TestConcolicQuizApp(unittest.TestCase):
    
    def test_viewer_fill_questions_exist(self):
        
        inputs = [
            MAIN_MENU_REVIEW_TOOLS,          # 4
            REVIEW_TOOLS_SEE_ALL_QUESTIONS,  # 4
            "0",  
            "0", 
        ]
        out = run_app_with_inputs(inputs)

        self.assertIn("REVIEW & TOOLS", out.upper())
        self.assertIn("ALL FILL-IN-THE-BLANKS", out.upper())


    def test_wrong_mode_valid_flow(self):
        
        valid_count = z3_pick_valid_count(1, 30)

        inputs = [
            MAIN_MENU_QUIZ_MODES,      
            QUIZ_MODES_WRONG_ANSWER,   
            "",                        
            "",                        
            valid_count,               
            "A",                       
            "",                        
            "0",                       
            "0",                       
        ]
        out = run_app_with_inputs(inputs)

        self.assertIn("WRONG-ANSWER TRAINING MODE", out.upper())
        self.assertIn("INSTRUCTIONS", out.upper())

    def test_wrong_mode_invalid_count(self):
        
        invalid_count = z3_pick_invalid_count(1, 30)
        valid_count = z3_pick_valid_count(1, 30)

        inputs = [
            MAIN_MENU_QUIZ_MODES,      
            QUIZ_MODES_WRONG_ANSWER,   
            "",                        
            "",                        
            invalid_count,             
            valid_count,               
            "A",                       
            "",                        
            "0",                       
            "0",                       
        ]
        out = run_app_with_inputs(inputs)
        up = out.upper()

        self.assertIn("WRONG-ANSWER TRAINING MODE", up)

        self.assertTrue(
            ("PLEASE ENTER A VALID" in up) or ("PLEASE ENTER A NUMBER BETWEEN" in up),
            msg="Did not observe invalid-count validation message in output."
        )

       
        self.assertNotIn("EOFERROR", up)


if __name__ == "__main__":
    unittest.main(verbosity=2)

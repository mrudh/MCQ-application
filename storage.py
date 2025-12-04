import os
import json

SCORE_FILE = "high_scores.json"
ASSESSMENT_FILE = "custom_assessment.json"

def load_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    return []

def save_scores(scores):
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

def check_high_score(): 
    scores = load_scores()
    if scores:
        highest = max(scores, key=lambda x: x["score"])
        print("\n--- HIGHEST SCORE ---")
        print(f"{highest['name']}: {highest['score']}%")
    else:
        print("No scores yet.")

def load_custom_assessments():
    if os.path.exists(ASSESSMENT_FILE):
        with open(ASSESSMENT_FILE, "r") as f:
            return json.load(f)
    return []

def save_custom_assessments(assessments):
    with open(ASSESSMENT_FILE, "w") as f:
        json.dump(assessments, f)

        
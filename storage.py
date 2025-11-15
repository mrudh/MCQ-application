import os
import json

SCORE_FILE = "high_scores.json"

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

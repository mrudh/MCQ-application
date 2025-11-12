#import os
#import json

SCORE_FILE = "high_scores.json"

#def load_scores():
    

#def save_scores(scores):
    

def check_high_score():
    scores = load_scores()
    if scores:
    highest = max(scores, key=lambda x: x["score"])
    print("\n--- HIGHEST SCORE ---")
    print(f"{highest['name']}: {highest['score']}%")
    else:
    print("No scores yet.")
from utils import load_scores

def check_high_score(): 
    scores = load_scores()
    if scores:
        highest = max(scores, key=lambda x: x["score"])
        print("\n--- HIGHEST SCORE ---")
        print(f"{highest['name']}: {highest['score']}%")
    else:
        print("No scores yet.")

        
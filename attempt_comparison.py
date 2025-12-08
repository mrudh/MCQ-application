

from storage import load_scores


def _normalize_name(name: str) -> str:

    return " ".join(name.strip().lower().split())


def get_user_attempts(name: str):
  
    scores = load_scores()
    target = _normalize_name(name)
    user_attempts = [s for s in scores if _normalize_name(s.get("name", "")) == target]
    return user_attempts


def show_first_and_latest_attempt(name: str):
    
    attempts = get_user_attempts(name)

    if not attempts:
        print(f"\nNo quiz attempts found for '{name}'.")
        return

    first = attempts[0]
    latest = attempts[-1]

    first_score = first.get("score", 0)
    latest_score = latest.get("score", 0)
    diff = latest_score - first_score

    print("\n===== QUIZ ATTEMPT COMPARISON =====")
    print(f"User: {name}")
    print("-----------------------------------")
    print(f"First attempt score : {first_score}%")
    print(f"Latest attempt score: {latest_score}%")

    if diff > 0:
        print(f"Progress          : +{diff}% (improvement)")
    elif diff < 0:
        print(f"Progress          : {diff}% (drop)")
    else:
        print("Progress          : 0% (no change)")
    print("===================================\n")




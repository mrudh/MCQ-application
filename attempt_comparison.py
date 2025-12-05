

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


def get_all_users():
    
    scores = load_scores()
    seen = set()
    users = []
    for s in scores:
        raw_name = (s.get("name") or "").strip()
        if not raw_name:
            continue
        key = _normalize_name(raw_name)
        if key not in seen:
            seen.add(key)
            users.append(raw_name)
    return users


def choose_user_from_list_and_compare():
   
    users = get_all_users()
    if not users:
        print("\nNo quiz attempts stored yet.")
        return

    print("\n=== USERS WITH QUIZ ATTEMPTS ===")
    for idx, u in enumerate(users, start=1):
        print(f"{idx}. {u}")
    print("0. Cancel")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if choice == 0:
        print("Cancelled.")
        return

    if 1 <= choice <= len(users):
        selected_name = users[choice - 1]
        show_first_and_latest_attempt(selected_name)
    else:
        print("Invalid selection.")


def comparison_menu():
    
    while True:
        print("\n====== ATTEMPT COMPARISON MENU ======")
        print("1. Compare attempts by typing a name")
        print("2. Compare attempts by choosing from user list")
        print("0. Back to main menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Enter your name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            show_first_and_latest_attempt(name)
        elif choice == "2":
            choose_user_from_list_and_compare()
        elif choice == "0":
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice. Please try again.")

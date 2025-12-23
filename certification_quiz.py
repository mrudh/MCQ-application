import os
import json
import random
from datetime import date, datetime

from quiz_data import ALL_QUIZ_DATA
from utils import load_scores, save_scores

CERT_ATTEMPT_FILE = "cert_attempts.json"
MAX_CERT_ATTEMPTS_PER_DAY = 1   

CERT_RESULT_FILE = "certification_results.json"


def _load_cert_attempts():
    if os.path.exists(CERT_ATTEMPT_FILE):
        with open(CERT_ATTEMPT_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def _save_cert_attempts(data):
    with open(CERT_ATTEMPT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _today_str():
    return date.today().isoformat()


def get_cert_attempts_left(name, max_attempts=MAX_CERT_ATTEMPTS_PER_DAY):
    name = name.strip()
    attempts = _load_cert_attempts()
    today = _today_str()

    user_attempts = attempts.get(name, {})
    used_today = user_attempts.get(today, 0)
    remaining = max(0, max_attempts - used_today)
    return remaining


def can_attempt_cert_quiz(name, max_attempts=MAX_CERT_ATTEMPTS_PER_DAY):
    remaining = get_cert_attempts_left(name, max_attempts=max_attempts)
    return remaining > 0, remaining


def record_cert_attempt(name):
    name = name.strip()
    attempts = _load_cert_attempts()
    today = _today_str()

    user_attempts = attempts.setdefault(name, {})
    user_attempts[today] = user_attempts.get(today, 0) + 1

    _save_cert_attempts(attempts)


def _load_cert_results():
    if os.path.exists(CERT_RESULT_FILE):
        with open(CERT_RESULT_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def _save_cert_results(results):
    with open(CERT_RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def _add_cert_result(record):
    results = _load_cert_results()
    results.append(record)
    _save_cert_results(results)


def _normalize_text(s: str) -> str:
    return " ".join(s.strip().lower().split())


def run_certification_exam(
    name: str,
    pass_mark: int = 70,
    timed: bool = False,
    time_per_question: int = 5,
):
    


    if not ALL_QUIZ_DATA:
        print("No questions available for certification.")
        return

    name = name.strip()
    if not name:
        print("Name cannot be empty for certification.")
        return

    allowed, remaining = can_attempt_cert_quiz(name)
    if not allowed:
        print("\nYou have used all certification attempts for today.")
        print("Please try again tomorrow.")
        return

    print("\n===== CERTIFICATION EXAM MODE =====")
    print(f"Candidate : {name}")
    print(f"Pass mark : {pass_mark}%")
    print(f"Questions : {len(ALL_QUIZ_DATA)}")
    if timed:
        print(f"Timing    : {time_per_question} seconds per question")
    print("===================================")
    input("Press Enter to begin the certification exam...")

    
    record_cert_attempt(name)

    
    indices = list(range(len(ALL_QUIZ_DATA)))
    random.shuffle(indices)

    questions = [ALL_QUIZ_DATA[i]["question"] for i in indices]
    options = [ALL_QUIZ_DATA[i]["options"] for i in indices]
    answers = [ALL_QUIZ_DATA[i]["answer"].strip().upper() for i in indices]

    guesses = []
    score = 0
    total = len(questions)

    if timed:
        
        from mcq import timed_quiz

    for i, question in enumerate(questions):
        print("\n--------------------------------------------------")
        print(f"Q{i+1}. {question}")
        for opt in options[i]:
            print("   " + opt)

        if timed:
            guess = timed_quiz("Enter (A, B, C, D): ", timeout=time_per_question)
            if guess is None:
                print("Time's up for this question! No answer recorded.")
                guess = ""
        else:
            guess = input("Enter (A, B, C, D): ").strip().upper()

        guess = guess.upper()
        guesses.append(guess)

        if guess == answers[i]:
            score += 1
            print("✔ CORRECT")
        else:
            if guess == "":
                print("✖ No valid option chosen.")
            else:
                print("✖ INCORRECT")
            print(f"   Correct answer was: {answers[i]}")

    percent = int((score / total) * 100) if total > 0 else 0
    passed = percent >= pass_mark

    print("\n============== CERTIFICATION SUMMARY ==============")
    print(f"Candidate       : {name}")
    print(f"Score           : {score} / {total}")
    print(f"Percentage      : {percent}%")
    print(f"Pass mark       : {pass_mark}%")
    print(f"Result          : {'PASSED ✅' if passed else 'FAILED ❌'}")
    print("===================================================\n")

    scores = load_scores()
    scores.append({"name": name, "score": percent})
    save_scores(scores)

    record = {
        "name": name,
        "score": percent,
        "passed": passed,
        "pass_mark": pass_mark,
        "total_questions": total,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    _add_cert_result(record)

    if passed:
        print(
            f"🎉 Congratulations, {name}! You have PASSED the certification exam.\n"
            "   Your result has been recorded."
        )
    else:
        print(
            f"Keep going, {name}! You did not reach the pass mark this time.\n"
            "Review the topics and try again on another day."
        )


def show_cert_history_for_user(name: str):
    name = name.strip()
    if not name:
        print("Name cannot be empty.")
        return

    results = _load_cert_results()
    user_results = [r for r in results if _normalize_text(r.get("name", "")) == _normalize_text(name)]

    if not user_results:
        print(f"\nNo certification attempts found for '{name}'.")
        return

    print(f"\n===== CERTIFICATION HISTORY FOR: {name} =====")
    for idx, r in enumerate(user_results, start=1):
        status = "PASSED" if r.get("passed") else "FAILED"
        print(f"{idx}. {r.get('timestamp', 'N/A')}")
        print(f"   Score      : {r.get('score', 0)}%")
        print(f"   Pass mark  : {r.get('pass_mark', 0)}%")
        print(f"   Result     : {status}")
        print()
    print("=============================================\n")


def show_all_cert_attempts():
    results = _load_cert_results()
    if not results:
        print("\nNo certification attempts recorded yet.")
        return

    print("\n=========== ALL CERTIFICATION ATTEMPTS ===========")
    for idx, r in enumerate(results, start=1):
        status = "PASSED" if r.get("passed") else "FAILED"
        print(f"{idx}. {r.get('timestamp', 'N/A')}")
        print(f"   Candidate  : {r.get('name', 'Unknown')}")
        print(f"   Score      : {r.get('score', 0)}%")
        print(f"   Pass mark  : {r.get('pass_mark', 0)}%")
        print(f"   Result     : {status}")
        print()
    print("==================================================\n")


def certification_menu():
    while True:
        print("\n====== CERTIFICATION QUIZ MENU ======")
        print("1. Attempt certification exam")
        print("2. View my certification history")
        print("3. View ALL certification attempts")
        print("0. Back to main menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Enter your name: ").strip()
            if not name:
                print("Name is required for certification.")
                continue

            try:
                pass_mark = int(
                    input("Enter pass mark percentage (default 70): ").strip() or "70"
                )
            except ValueError:
                print("Invalid input. Using default pass mark of 70%.")
                pass_mark = 70

            timed_choice = input(
                "Timed exam? (y/n, default n): "
            ).strip().lower() or "n"
            timed = timed_choice == "y"

            if timed:
                try:
                    t = int(
                        input(
                            "Time per question in seconds (default 5): "
                        ).strip() or "5"
                    )
                except ValueError:
                    print("Invalid input. Using 5 seconds per question.")
                    t = 5
            else:
                t = 0

            run_certification_exam(
                name=name,
                pass_mark=pass_mark,
                timed=timed,
                time_per_question=t if timed else 0,
            )

        elif choice == "2":
            name = input("Enter your name: ").strip()
            show_cert_history_for_user(name)

        elif choice == "3":
            show_all_cert_attempts()

        elif choice == "0":
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "_main_":
    certification_menu()
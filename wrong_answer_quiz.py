
import random

from quiz_data import ALL_QUIZ_DATA
from storage import load_scores, save_scores


def _ask_int(prompt, minimum, maximum):
    
    while True:
        try:
            value = int(prompt())
            if minimum <= value <= maximum:
                return value
            print(f"Please enter a number between {minimum} and {maximum}.")
        except ValueError:
            print("Please enter a valid number.")


def _print_summary(questions_used, correct_letters, user_guesses, mode_score):
    
    print("\n================ WRONG-ANSWER MODE RESULTS ================")
    print("Real answers vs. what you chose:\n")

    for i, (q, real, guess) in enumerate(
        zip(questions_used, correct_letters, user_guesses), start=1
    ):
        print(f"Q{i}. {q}")
        print(f"   Real correct answer : {real}")
        print(f"   You chose           : {guess or 'No valid option'}")
        if guess == "":
            print("   → This did NOT count as a valid wrong answer.")
        elif guess == real:
            print("   → In this mode, that is considered a MISTAKE (you picked the real answer).")
        else:
            print("   → Good! You avoided the real answer.")
        print()

    total = len(questions_used)
    print("===========================================================")
    print(f"Total questions : {total}")
    print(f"Mode score      : {mode_score} / {total}")
    print("  (Score counts how many times you successfully avoided")
    print("   choosing the actual correct option.)")
    print("===========================================================\n")


def take_wrong_answer_quiz(name=None):
    
    if not ALL_QUIZ_DATA:
        print("No questions available.")
        return

    print("\n===== WRONG-ANSWER TRAINING MODE =====")
    if name is None:
        name = input("Enter your name (optional, press Enter to skip): ").strip() or None

    total_available = len(ALL_QUIZ_DATA)
    print(f"\nThere are {total_available} MCQ questions available.")

    def _prompt():
        return input(
            f"How many questions do you want to attempt in WRONG-ANSWER mode? (1 to {total_available}): "
        )

    total_questions = _ask_int(_prompt, 1, total_available)

    indices = list(range(total_available))
    random.shuffle(indices)
    indices = indices[:total_questions]

    questions = [ALL_QUIZ_DATA[i]["question"] for i in indices]
    options = [ALL_QUIZ_DATA[i]["options"] for i in indices]
    real_answers = [ALL_QUIZ_DATA[i]["answer"].strip().upper() for i in indices]

    print("\nINSTRUCTIONS:")
    print("  • This is NOT a normal quiz.")
    print("  • Your goal is to AVOID the real correct answer.")
    print("  • Pick ANY option (A, B, C, or D) that is WRONG.")
    print("  • If you accidentally pick the real correct answer,")
    print("    the game treats it as a mistake.\n")

    user_guesses = []
    mode_score = 0  

    for i, question in enumerate(questions):
        print("--------------------------------------------------")
        print(f"Q{i+1}. {question}")
        for opt in options[i]:
            print("   " + opt)

        correct_letter = real_answers[i]

        while True:
            guess = input("Pick a WRONG option (A/B/C/D): ").strip().upper()
            if guess in ("A", "B", "C", "D"):
                break
            print("Please enter one of: A, B, C, or D.")

        user_guesses.append(guess)

        if guess == correct_letter:
            print("You chose the REAL correct answer! ❌")
            print("In this mode, that counts as a mistake.")
        else:
            print("Nice! You successfully avoided the correct answer ✅")
            mode_score += 1

        print(f"(Real correct answer was: {correct_letter})")

    _print_summary(questions, real_answers, user_guesses, mode_score)

    if name is not None:
        percent = int((mode_score / len(questions)) * 100)
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)
        print(f"Your performance has been saved as: {percent}% for {name}.")


if __name__== "_main_":
    take_wrong_answer_quiz()
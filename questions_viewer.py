

from quiz_data import ALL_QUIZ_DATA, FILL_IN_QUIZ_DATA


def show_all_mcq_questions_only():
    
    print("\n===== ALL MULTIPLE-CHOICE QUESTIONS (NO ANSWERS) =====\n")
    for idx, q in enumerate(ALL_QUIZ_DATA, start=1):
        question = q["question"]
        options = q["options"]
        topic = q.get("topic", "Unknown topic")
        difficulty = q.get("difficulty", "Unknown difficulty")

        print(f"Q{idx}. {question}")
        for opt in options:
            print(f"   {opt}")
        print(f"   Topic     : {topic}")
        print(f"   Difficulty: {difficulty}")
        print()
    print("======================================================\n")


def show_all_fill_in_questions_only():
    
    print("\n===== ALL FILL-IN-THE-BLANKS QUESTIONS (NO ANSWERS) =====\n")
    for idx, q in enumerate(FILL_IN_QUIZ_DATA, start=1):
        question = q["question"]
        topic = q.get("topic", "Unknown topic")
        difficulty = q.get("difficulty", "Unknown difficulty")

        print(f"F{idx}. {question}")
        print(f"   Topic     : {topic}")
        print(f"   Difficulty: {difficulty}")
        print()
    print("=========================================================\n")


def show_all_questions_only():
    
    show_all_mcq_questions_only()
    show_all_fill_in_questions_only()


def questions_viewer_menu():
    
    while True:
        print("\n====== QUESTIONS VIEWER ======")
        print("1. See all MCQ questions (no answers)")
        print("2. See all fill-in-the-blanks questions (no answers)")
        print("3. See ALL questions (no answers)")
        print("0. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_all_mcq_questions_only()
        elif choice == "2":
            show_all_fill_in_questions_only()
        elif choice == "3":
            show_all_questions_only()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "_main_":
    questions_viewer_menu()
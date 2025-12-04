from mcq import menu, take_quiz, print_results, quiz_by_difficulty, timed_quiz, take_negative_mark_quiz, age_based_quiz, fifty_fifty_quiz
from storage import load_scores, save_scores, check_high_score, load_custom_assessments, save_custom_assessments
from assessment import create_assessment, open_assessment
from quiz_data import ALL_QUIZ_DATA

def main():
    while True:
        menu()
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        questions = [q['question'] for q in ALL_QUIZ_DATA]
        options = [q['options'] for q in ALL_QUIZ_DATA]
        answers = [q['answer'] for q in ALL_QUIZ_DATA]

        if choice == 1:
            name = input("Enter your name: ")
            try:
                total_questions = int(input(f"How many questions do you want to take? (1 to {len(ALL_QUIZ_DATA)}): "))
                if not (1 <= total_questions <= len(ALL_QUIZ_DATA)):
                    print("Invalid number, displaying all questions.")
                    total_questions = len(ALL_QUIZ_DATA)
            except ValueError:
                print("Invalid input, displaying all questions.")
                total_questions = len(ALL_QUIZ_DATA)
            import random
            selected = random.sample(ALL_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            opts = [q['options'] for q in selected]
            ans = [q['answer'] for q in selected]
            take_quiz(qs, opts, ans, name)
        elif choice == 2:
            check_high_score()
        elif choice == 4:
            create_assessment()
        elif choice ==5:
            open_assessment()
        elif choice == 6:
            name = input("Enter your name: ")
            try:
                total_questions = int(input(f"How many questions do you want to take? (1 to {len(ALL_QUIZ_DATA)}): "))
                if not (1 <= total_questions <= len(ALL_QUIZ_DATA)):
                    print("Invalid number, displaying all questions.")
                    total_questions = len(ALL_QUIZ_DATA)
            except ValueError:
                print("Invalid input, displaying all questions.")
                total_questions = len(ALL_QUIZ_DATA)

            import random
            selected = random.sample(ALL_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            opts = [q['options'] for q in selected]
            ans = [q['answer'] for q in selected]
            take_quiz(qs, opts, ans, name, timed=True)
        elif choice == 7:  
            quiz_by_difficulty(ALL_QUIZ_DATA)
        elif choice == 8:
            name = input("Enter your name: ")
            try:
                total_questions = int(input(f"How many questions do you want to take? (1 to {len(ALL_QUIZ_DATA)}): "))
                if not (1 <= total_questions <= len(ALL_QUIZ_DATA)):
                    print("Invalid number, displaying all questions.")
                    total_questions = len(ALL_QUIZ_DATA)
            except ValueError:
                print("Invalid input, displaying all questions.")
                total_questions = len(ALL_QUIZ_DATA)
            try:
                negative_mark = float(input("Enter negative mark per wrong answer (e.g., 0.25): "))
                if negative_mark < 0:
                    print("Negative mark cannot be negative. Using 0.25 instead.")
                    negative_mark = 0.25
            except ValueError:
                print("Invalid input. Using 0.25 as negative marking.")
                negative_mark = 0.25
            import random
            selected = random.sample(ALL_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            opts = [q['options'] for q in selected]
            ans = [q['answer'] for q in selected]
            take_negative_mark_quiz(qs, opts, ans, name=name, neg_mark=negative_mark)
        elif choice == 9:  # <-- NEW AGE-BASED QUIZ OPTION
            age_based_quiz(ALL_QUIZ_DATA)
        elif choice == 10:
            name = input("Enter your name: ")
            try:
                total_questions = int(input(f"How many questions do you want to take? (1 to {len(ALL_QUIZ_DATA)}): "))
                if not (1 <= total_questions <= len(ALL_QUIZ_DATA)):
                    print("Invalid number, using all questions.")
                    total_questions = len(ALL_QUIZ_DATA)
            except ValueError:
                print("Invalid input, using all questions.")
                total_questions = len(ALL_QUIZ_DATA)

            import random
            selected = random.sample(ALL_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            opts = [tuple(q['options']) for q in selected]
            ans = [q['answer'] for q in selected]
            fifty_fifty_quiz(qs, opts, ans, name)
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

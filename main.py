from mcq import menu, quiz_by_difficulty, age_based_quiz, fifty_fifty_quiz, take_quiz_with_skip, take_fill_in_the_blanks_quiz, take_quiz_with_summary, quiz_by_topic
from mcq_types import take_quiz, timed_quiz, take_negative_mark_quiz, take_quiz_until_wrong, take_quiz_challenge, learning_mode
from storage import check_high_score
from assessment_storage import load_custom_assessments, save_custom_assessments
from assessment import open_assessment
from manage_assessment import create_assessment, add_question_to_assessment, edit_question_in_assessment, delete_question_from_assessment, view_questions_in_assessment
from quiz_data import ALL_QUIZ_DATA, FILL_IN_QUIZ_DATA
from attempts import can_attempt_quiz, record_quiz_attempt
from answers_viewer import show_all_answers
from attempt_comparison import comparison_menu
from answer_links import links_menu
from questions_viewer import show_all_questions_only
from wrong_answer_quiz import take_wrong_answer_quiz
from export_questions import export_questions
from export_answers import export_answers
from certification_quiz import certification_menu
from utils import load_scores, save_scores, print_results



def quiz_modes_menu():
    while True:
        print("\n====== QUIZ MODES ======")
        print("1. Timed quiz")
        print("2. Quiz by difficulty")
        print("3. Negative marking quiz")
        print("4. Age-based quiz")
        print("5. 50-50 lifeline quiz")
        print("6. Challenge mode (time-based)")
        print("7. Streak mode (ends on first wrong)")
        print("8. Skip-mode quiz")
        print("9. Fill-in-the-blanks quiz")
        print("10. Wrong-answer training mode")
        print("11. Summary-based quiz")
        print("12. Learning mode (flashcard style)")
        print("0. Back")
        choice = input("Enter choice: ").strip()

        questions = [q['question'] for q in ALL_QUIZ_DATA]
        options = [q['options'] for q in ALL_QUIZ_DATA]
        answers = [q['answer'] for q in ALL_QUIZ_DATA]

        if choice == "1":
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

        elif choice == "2":
            quiz_by_difficulty(ALL_QUIZ_DATA)

        elif choice == "3":
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

        elif choice == "4":
            age_based_quiz(ALL_QUIZ_DATA)

        elif choice == "5":
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

        elif choice == "6":
            name = input("Enter your name: ")
            take_quiz_challenge(questions, options, answers, name=name)

        elif choice == "7":
            name = input("Enter your name: ")
            take_quiz_until_wrong(questions, options, answers, name=name)

        elif choice == "8":
            name = input("Enter your name: ")
            import random
            total_questions = len(ALL_QUIZ_DATA)
            selected = random.sample(ALL_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            opts = [q['options'] for q in selected]
            ans = [q['answer'] for q in selected]
            take_quiz_with_skip(qs, opts, ans, name=name)

        elif choice == "9":
            name = input("Enter your name: ").strip()
            import random

            available = len(FILL_IN_QUIZ_DATA)
            if available == 0:
                print("No fill-in-the-blanks questions available yet.")
                continue
            try:
                total_questions = int(input(f"How many questions do you want to take? (1 to {available}): "))
                if not (1 <= total_questions <= available):
                    print("Invalid number, using all fill-in-the-blanks questions.")
                    total_questions = available
            except ValueError:
                print("Invalid input, using all fill-in-the-blanks questions.")
                total_questions = available

            selected = random.sample(FILL_IN_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            ans = [q['answer'] for q in selected]
            take_fill_in_the_blanks_quiz(qs, ans, name=name)

        elif choice == "10":
            name = input("Enter your name: ").strip() or None
            take_wrong_answer_quiz(name=name)

        elif choice == "11":
            name = input("Enter your name: ")
            import random
            total_questions = len(ALL_QUIZ_DATA)
            selected = random.sample(ALL_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            opts = [q['options'] for q in selected]
            ans = [q['answer'] for q in selected]
            take_quiz_with_summary(qs, opts, ans, name=name)

        elif choice == "12":
            questions = [q['question'] for q in ALL_QUIZ_DATA]
            answers = [q['answer'] for q in ALL_QUIZ_DATA]
            learning_mode(questions, answers)

        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def assessments_menu():
    while True:
        print("\n--- Create & Manage Assessments ---")
        print("1. Create new assessment")
        print("2. Add question to assessment")
        print("3. Edit question in assessment")
        print("4. Delete question from assessment")
        print("5. View questions in assessment")
        print("6. Open an assessment to take it")
        print("0. Back")

        try:
            manage_choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input.")
            continue

        if manage_choice == 1:
            create_assessment()
        elif manage_choice == 2:
            add_question_to_assessment()
        elif manage_choice == 3:
            edit_question_in_assessment()
        elif manage_choice == 4:
            delete_question_from_assessment()
        elif manage_choice == 5:
            view_questions_in_assessment()
        elif manage_choice == 6:
            open_assessment()
        elif manage_choice == 0:
            break
        else:
            print("Invalid selection. Try again.")


def review_tools_menu():
    while True:
        print("\n====== REVIEW & TOOLS ======")
        print("1. See all answers")
        print("2. Compare first and latest attempts")
        print("3. Answer reference links")
        print("4. See all questions")
        print("5. Export all questions")
        print("6. Export all answers")
        print("0. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_all_answers()
        elif choice == "2":
            comparison_menu()
        elif choice == "3":
            links_menu()
        elif choice == "4":
            show_all_questions_only()
        elif choice == "5":
            filename = input("Enter filename (default: exported_questions.json): ").strip() or "exported_questions.json"
            export_questions(filename)
        elif choice == "6":
            filename = input("Enter filename (default: exported_answers.json): ").strip() or "exported_answers.json"
            export_answers(filename)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")



def main():
    while True:
        menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Enter your name: ")
            import random
            try:
                total_questions = int(input(f"How many questions do you want to take? (1 to {len(ALL_QUIZ_DATA)}): "))
                if not (1 <= total_questions <= len(ALL_QUIZ_DATA)):
                    print("Invalid number, displaying all questions.")
                    total_questions = len(ALL_QUIZ_DATA)
            except ValueError:
                print("Invalid input, displaying all questions.")
                total_questions = len(ALL_QUIZ_DATA)

            selected = random.sample(ALL_QUIZ_DATA, total_questions)
            qs = [q['question'] for q in selected]
            opts = [q['options'] for q in selected]
            ans = [q['answer'] for q in selected]
            take_quiz(qs, opts, ans, name)

        elif choice == "2":
            quiz_modes_menu()

        elif choice == "3":
            assessments_menu()

        elif choice == "4":
            review_tools_menu()

        elif choice == "5":
            certification_menu()

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

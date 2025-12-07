from mcq import menu, take_quiz, print_results, quiz_by_difficulty, timed_quiz, take_negative_mark_quiz, age_based_quiz, fifty_fifty_quiz, take_quiz_challenge, take_quiz_until_wrong, take_quiz_with_skip, take_fill_in_the_blanks_quiz, take_quiz_with_summary
from storage import load_scores, save_scores, check_high_score, load_custom_assessments, save_custom_assessments
from assessment import create_assessment
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
        elif choice == 5:
            name = input("Enter your name: ").strip()
            allowed, remaining = can_attempt_quiz(name)
            if not allowed:
                print(f"Sorry {name}, you have used all your assessment attempts for today.")
                print("Please try again tomorrow.")
                continue  
                print(f"You have {remaining} assessment attempt(s) left for today.\n")
 
            record_quiz_attempt(name)
            # open_assessment()
            create_assessment()
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

        elif choice == 9:  
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

        elif choice == 11:
            name = input("Enter your name: ")
            qs = [q['question'] for q in ALL_QUIZ_DATA]
            opts = [q['options'] for q in ALL_QUIZ_DATA]
            ans = [q['answer'] for q in ALL_QUIZ_DATA]
            take_quiz_challenge(qs, opts, ans, name=name)

        elif choice == 12:
            name = input("Enter your name: ")
            qs = [q['question'] for q in ALL_QUIZ_DATA]
            opts = [q['options'] for q in ALL_QUIZ_DATA]
            ans = [q['answer'] for q in ALL_QUIZ_DATA]
            take_quiz_until_wrong(qs, opts, ans, name=name)

        elif choice == 13:   
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
            take_quiz_with_skip(qs, opts, ans, name=name)

        elif choice == 14:
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

        elif choice == 15: 
            show_all_answers()

        elif choice == 16:
            comparison_menu()

        elif choice == 17:
            links_menu()

        elif choice == 18:
            show_all_questions_only()

        elif choice == 19:  
            name = input("Enter your name: ").strip()
            if not name:
                name = None
            take_wrong_answer_quiz(name=name)
            
        elif choice == 20:
            filename = input("Enter filename to export to (default: exported_questions.json): ").strip()
            if filename == "":
                filename = "exported_questions.json"
            export_questions(filename)
            
        elif choice == 21:
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
            opts = [q['options'] for q in selected]
            ans = [q['answer'] for q in selected]

            take_quiz_with_summary(qs, opts, ans, name=name)

        elif choice == 22:  
            filename = input(
                "Enter filename to export answers to (default: exported_answers.json): "
            ).strip()
            if filename == "":
                filename = "exported_answers.json"
            export_answers(filename)

        elif choice == 23:   
            certification_menu()

        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

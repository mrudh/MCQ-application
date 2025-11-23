from mcq import menu, take_quiz, print_results, quiz_by_difficulty, timed_quiz
from storage import load_scores, save_scores, check_high_score, load_custom_assessments, save_custom_assessments
from assessment import create_assessment
from quiz_data import ALL_QUIZ_DATA

def main():
    while True:
        menu()
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        if choice == 1:
            name = input("Enter your name: ")
            take_quiz(ALL_QUIZ_DATA, name=name)
        elif choice == 2:
            check_high_score()
        elif choice == 4:
            create_assessment()
        elif choice == 6:
            name = input("Enter your name: ")
            take_quiz(ALL_QUIZ_DATA, name=name, timed=True)
        elif choice == 7:  
            quiz_by_difficulty(ALL_QUIZ_DATA)
        elif choice == 8:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

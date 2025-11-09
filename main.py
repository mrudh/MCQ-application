from mcq import menu, take_quiz

#Data
QUESTIONS = (
    "Which planet in the solar system is the hottest?: ",
    "What is the most abundant gas in Earth's atmosphere?: ",
)
OPTIONS = (
    ("A. Mercury", "B. Venus", "C. Earth", "D. Mars"),
    ("A. Nitrogen", "B. Oxygen", "C. Carbon-Dioxide", "D. Hydrogen"),
)
ANSWERS = ("B","A")
#TOPICS = ()
DIFFICULTY_QUESTIONS = {
    "Easy": [
        ("Which animal lays the largest eggs?: ",
         ("A. Whale", "B. Crocodile", "C. Elephant", "D. Ostrich"), "D"),
    ],
    "Medium": [
        ("What is the most abundant gas in Earth's atmosphere?: ",
         ("A. Nitrogen", "B. Oxygen", "C. Carbon-Dioxide", "D. Hydrogen"), "A"),
    ],
    "Hard": [
        ("Which planet in the solar system is the hottest?: ",
         ("A. Mercury", "B. Venus", "C. Earth", "D. Mars"), "B"),
    ]
}

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
            take_quiz(QUESTIONS, OPTIONS, ANSWERS, name)
        """elif choice == 2:
            check_high_score()
        elif choice == 3:
            quiz_by_topic(QUESTIONS, OPTIONS, ANSWERS, TOPICS)"""
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

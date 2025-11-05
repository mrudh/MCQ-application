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
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

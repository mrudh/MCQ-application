from mcq import menu

#Data
QUESTIONS = (
    "Which planet in the solar system is the hottest?: ",
)
OPTIONS = (
    ("A. Mercury", "B. Venus", "C. Earth", "D. Mars"),
)
ANSWERS = ("B")
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
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

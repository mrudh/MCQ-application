
def menu():
    """Display the menu options."""
    print("\n====== QUIZ MENU ======")
    print("1. Take quiz")
    print("2. Check highest score")
    print("3. Take quiz by topics")
    print("4. Create assessment")
    print("5. Open assessment")
    print("6. Timed quiz")
    print("7. Exit")

def take_quiz(questions, options, answers, name=None):
    guesses = []
    score = 0
    total = len(questions)
    for i, question in enumerate(questions):
        print("----------------------")
        print(question)
        for option in options[i]:
            print(option)
        guess = input("Enter (A, B, C, D): ").strip().upper()
        guesses.append(guess)
        if guess == answers[i]:
            score += 1
            print("CORRECT!")
        else:
            print("INCORRECT!")
            print(f"{answers[i]} is the correct answer")

#def print_results():
    

#def quiz_by_topic():
    

#def timed_quiz():
    

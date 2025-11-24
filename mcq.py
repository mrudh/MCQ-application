
def menu():
    """Display the menu options."""
    print("\n====== QUIZ MENU ======")
    print("1. Take quiz")
    print("2. Check highest score")
    print("3. Take quiz by topics")
    print("4. Create assessment")
    print("5. Open assessment")
    print("6. Timed quiz")
    print("7. Take quiz by difficulty")
    print("8. Exit")

def take_quiz(questions, options, answers, name=None):
    from storage import load_scores, save_scores
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
    print_results(guesses, score, answers)
    percent = int(score / total * 100)
    if name is not None:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)

def print_results(guesses, score, answers):
    print("----------------------")
    print("       RESULTS        ")
    print("----------------------")
    print("Answers: ", end="")
    for answer in answers:
        print(answer, end=" ")
    print()
    print("Guesses: ", end="")
    for guess in guesses:
        print(guess, end=" ")
    print()
    percent = int(score / len(answers) * 100)
    print(f"\nYour score is: {percent}%")
    

#def quiz_by_topic(QUESTIONS, OPTIONS, ANSWERS, TOPICS):
    

#def timed_quiz():
    

def quiz_by_difficulty(ALL_QUIZ_DATA):
    levels = sorted(list(set(q['difficulty'] for q in ALL_QUIZ_DATA)))
    print("Select a difficulty level:")
    for idx, level in enumerate(levels):
        count = sum(1 for q in ALL_QUIZ_DATA if q['difficulty'] == level)
        print(f"{idx + 1}. {level} ({count} questions)")
    try:
        idx = int(input("Enter choice: ")) - 1
        
        if 0 <= idx < len(levels):
            selected_level = levels[idx]
            selected_data = [q for q in ALL_QUIZ_DATA if q['difficulty'] == selected_level]
            if not selected_data:
                print("No questions for this level.")
                return

            questions = [q['question'] for q in selected_data]
            options = [q['options'] for q in selected_data]
            answers = [q['answer'] for q in selected_data]
            
            take_quiz(questions, options, answers)
        else:
            print("Invalid difficulty selection.")
    except ValueError:
        print("Invalid input.")


import sys
import time

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

def take_quiz(questions, options, answers, name=None, timed=False):
    from storage import load_scores, save_scores
    guesses = []
    score = 0
    total = len(questions)
    for i, question in enumerate(questions):
        print("----------------------")
        print(question)
        for option in options[i]:
            print(option)
        if timed:
            guess = timed_quiz("Enter (A, B, C, D): ", timeout=5)
            if guess is None:
                print("Time's up!")
                guess = ''
        else:
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
    

def timed_quiz(prompt, timeout=5):
    if sys.platform.startswith("win"):
        import msvcrt
        print(prompt, end='', flush=True)
        start = time.time()
        buf = ""
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ("\r", "\n"):
                    print()
                    return buf.strip().upper()
                if ch == "\b":
                    if buf:
                        buf = buf[:-1]
                        print("\b \b", end='', flush=True)
                    continue
                buf += ch
                print(ch, end='', flush=True)

            if time.time() - start >= timeout:
                print()
                return None
            time.sleep(0.01)
    else:
        import select
        print(prompt, end='', flush=True)
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            return sys.stdin.readline().strip().upper()
        else:
            print()
            return None

def quiz_by_difficulty(DIFFICULTY_QUESTIONS):
    levels = list(DIFFICULTY_QUESTIONS.keys())
    print("Select a difficulty level:")
    for idx, level in enumerate(levels):
        print(f"{idx + 1}. {level}")
    try:
        idx = int(input("Enter choice: ")) - 1
        if 0 <= idx < len(levels):
            selected = DIFFICULTY_QUESTIONS[levels[idx]]
        if not selected:
            print("No questions for this level.")
        else:
            print("Invalid difficulty selection.")
        return
        questions = [q[0] for q in selected]
        options = [q[1] for q in selected]
        answers = [q[2] for q in selected]
        take_quiz(questions, options, answers)
    except ValueError:
        print("Invalid input.")



import sys
import time
import random

def menu():
    print("\n====== QUIZ MENU ======")
    print("1. Take quiz")
    print("2. Check highest score")
    print("3. Take quiz by topics")
    print("4. Create assessment")
    print("5. Open assessment")
    print("6. Timed quiz")
    print("7. Take quiz by difficulty")
    print("8. Take quiz with negative marking")
    print("9. Age-based quiz")
    print("10. 50 - 50 Lifeline Quiz")
    print("0. Exit")

def take_quiz(questions, options, answers, name=None, timed=False):
    from storage import load_scores, save_scores
    guesses = []
    score = 0
    total = len(questions)
    if timed:
        print("You have 5 seconds for each question!")
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

def take_negative_mark_quiz(questions, options, answers, name=None, neg_mark=0.25, timed=False):
    from storage import load_scores, save_scores
    guesses = []
    score = 0.0
    total = len(questions)

    print(f"\nNegative marking is ON: -{neg_mark} for each wrong answer")

    for i, question in enumerate(questions):
        print("----------------------")
        print(question)
        for option in options[i]:
            print(option)
        guess = input("Enter (A, B, C, D): ").strip().upper()
        guesses.append(guess)
        if guess == answers[i]:
            score += 1
            print("CORRECT! (+1)")
        else:
            if guess == '':
                print("No answer selected.")
                print(f"{answers[i]} is the correct answer (0 marks)")
            else:
                score -= neg_mark
                print("INCORRECT!")
                print(f"{answers[i]} is the correct answer (-{neg_mark})")
    percent = max(0, int((score / total) * 100))
    print("----------------------")
    print("NEGATIVE QUIZ RESULTS")
    print("----------------------")
    print("Answers: ", end="")
    for answer in answers:
        print(answer, end=" ")
    print()
    print("Guesses: ", end="")
    for guess in guesses:
        print(guess, end=" ")
    print()
    correct = sum(1 for g, a in zip(guesses, answers) if g == a)
    wrong = sum(1 for g, a in zip(guesses, answers) if g not in ("",) and g != a)
    penalty = wrong * neg_mark
    print(f"\nTotal questions : {total}")
    print(f"Correct answers : {correct}")
    print(f"Wrong answers   : {wrong}")
    print(f"Negative mark   : -{neg_mark} per wrong answer")
    print(f"Total penalty   : -{penalty} marks")
    print(f"\nFinal score : {round(score, 2)} / {total}")
    print(f"Your score is   : {percent}%")
    if name is not None:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)



def age_based_quiz(ALL_QUIZ_DATA):
    import random
    from .mcq import take_quiz  # if mcq.py is a module in a package
    # If this causes an ImportError in your setup, just remove this line;
    # main.py already imports age_based_quiz from mcq and can call take_quiz
    # directly if both are in same file.

    name = input("Enter your name: ")

    # Get age
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Invalid age. Defaulting to general quiz (all difficulties).")
        age = None

    # Map age to difficulty levels
    if age is None:
        allowed_difficulties = ["Easy", "Medium", "Hard"]
    elif age <= 10:
        allowed_difficulties = ["Easy"]
    elif age <= 14:
        allowed_difficulties = ["Easy", "Medium"]
    else:
        allowed_difficulties = ["Easy", "Medium", "Hard"]

    print(f"Using questions with difficulties: {', '.join(allowed_difficulties)}")

    # Filter questions by allowed difficulties
    filtered_questions = [
        q for q in ALL_QUIZ_DATA if q["difficulty"] in allowed_difficulties
    ]

    if not filtered_questions:
        print("No questions available for this age group.")
        return

    max_q = len(filtered_questions)

    # Ask how many questions
    try:
        total_questions = int(
            input(f"How many questions do you want to take? (1 to {max_q}): ")
        )
        if not (1 <= total_questions <= max_q):
            print("Invalid number, using all available questions for your age group.")
            total_questions = max_q
    except ValueError:
        print("Invalid input, using all available questions for your age group.")
        total_questions = max_q

    # Randomly select questions
    selected = random.sample(filtered_questions, total_questions)
    qs = [q["question"] for q in selected]
    opts = [q["options"] for q in selected]
    ans = [q["answer"] for q in selected]

    # Run the existing quiz function
    take_quiz(qs, opts, ans, name=name)


def age_based_quiz(ALL_QUIZ_DATA):
    import random

    name = input("Enter your name: ")

    # Get age
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Invalid age. Defaulting to general quiz (all difficulties).")
        age = None

    # Map age to difficulty levels
    if age is None:
        allowed_difficulties = ["Easy", "Medium", "Hard"]
    elif age <= 10:
        allowed_difficulties = ["Easy"]
    elif age <= 14:
        allowed_difficulties = ["Easy", "Medium"]
    else:
        allowed_difficulties = ["Easy", "Medium", "Hard"]

    print(f"Using questions with difficulties: {', '.join(allowed_difficulties)}")

    # Filter questions by allowed difficulties
    filtered_questions = [
        q for q in ALL_QUIZ_DATA if q["difficulty"] in allowed_difficulties
    ]

    if not filtered_questions:
        print("No questions available for this age group.")
        return

    max_q = len(filtered_questions)

    # Ask how many questions
    try:
        total_questions = int(
            input(f"How many questions do you want to take? (1 to {max_q}): ")
        )
        if not (1 <= total_questions <= max_q):
            print("Invalid number, using all available questions for your age group.")
            total_questions = max_q
    except ValueError:
        print("Invalid input, using all available questions for your age group.")
        total_questions = max_q

    # Randomly select questions
    selected = random.sample(filtered_questions, total_questions)
    qs = [q["question"] for q in selected]
    opts = [q["options"] for q in selected]
    ans = [q["answer"] for q in selected]

    
    take_quiz(qs, opts, ans, name=name)




def fifty_fifty(options, correct_letter):
    correct_idx = None
    for i, opt in enumerate(options):
        if opt.strip().upper().startswith(correct_letter.upper() + "."):
            correct_idx = i
            break
    wrong_indices = [i for i in range(len(options)) if i != correct_idx]
    keep_wrong = random.choice(wrong_indices)
    keep_indices = {correct_idx, keep_wrong}
    return tuple(opt for i, opt in enumerate(options) if i in keep_indices)


def fifty_fifty_quiz(questions, options, answers, name=None):
    from storage import load_scores, save_scores
    
    print("\n===== 50 - 50 LIFELINE QUIZ =====")
    guesses = []
    score = 0
    total = len(questions)
    for i, question in enumerate(questions):
        print("\n--------------------------")
        print(question)
        for opt in options[i]:
            print(opt)
        use = input("Press 'F' to use 50-50 or press Enter to continue: ").strip().upper()
        current_options = options[i]
        if use == "F":
            current_options = fifty_fifty(options[i], answers[i])
            print("\n50-50 Applied! Remaining options:")
            for opt in current_options:
                print(opt)
        guess = input("Enter (A, B, C, D): ").strip().upper()
        guesses.append(guess)
        
        if guess == answers[i]:
            score += 1
            print("CORRECT!")
        else:
            print("INCORRECT!")
            print(f"The correct answer was: {answers[i]}")
    percent = int((score / total) * 100)

    print("\n===== RESULTS =====")
    print(f"Your score: {score} / {total}")
    print(f"Percentage: {percent}%")

    if name:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)



  
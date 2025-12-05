import sys
import time
import random
from storage import load_scores, save_scores

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
    print("11. Quiz Challenge")
    print("12. Streak Mode")
    print("13. Take quiz (with skip)")
    print("0. Exit")

def take_quiz(questions, options, answers, name=None, timed=False):
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
    from .mcq import take_quiz  
    name = input("Enter your name: ")


    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Invalid age. Defaulting to general quiz (all difficulties).")
        age = None

    
    if age is None:
        allowed_difficulties = ["Easy", "Medium", "Hard"]
    elif age <= 10:
        allowed_difficulties = ["Easy"]
    elif age <= 14:
        allowed_difficulties = ["Easy", "Medium"]
    else:
        allowed_difficulties = ["Easy", "Medium", "Hard"]

    print(f"Using questions with difficulties: {', '.join(allowed_difficulties)}")

    
    filtered_questions = [
        q for q in ALL_QUIZ_DATA if q["difficulty"] in allowed_difficulties
    ]

    if not filtered_questions:
        print("No questions available for this age group.")
        return

    max_q = len(filtered_questions)

    
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


def take_quiz_challenge(questions, options, answers, name=None):
    from storage import load_scores, save_scores

    while True:
        try:
            minutes = int(input("Enter challenge duration in minutes (2 to 5): "))
            if 2 <= minutes <= 5:
                break
            else:
                print("Please enter a value between 2 and 5 minutes.")
        except ValueError:
            print("Please enter a valid number.")

    total_seconds = minutes * 60
    print(f"\nChallenge started for {minutes} minutes! Answer as many as you can.\n")

    indices = list(range(len(questions)))
    random.shuffle(indices)

    guesses = []
    used_answers = []
    asked = 0
    correct = 0
    i = 0

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        remaining = total_seconds - elapsed

        if remaining <= 0:
            print("\nTime is up for the challenge!")
            break

        if i >= len(indices):
            random.shuffle(indices)
            i = 0

        idx = indices[i]
        i += 1

        print("----------------------")
        print(f"Time remaining: {int(remaining)} seconds")
        print(questions[idx])
        for opt in options[idx]:
            print(opt)

        guess = timed_quiz("Enter (A, B, C, D): ", timeout=remaining)
        if guess is None:
            print("\nTime's up while answering!")
            break

        guess = guess.strip().upper()
        guesses.append(guess)
        used_answers.append(answers[idx])
        asked += 1

        if guess == answers[idx]:
            correct += 1
            print("CORRECT!")
        else:
            print("INCORRECT!")
            print(f"{answers[idx]} is the correct answer.")
    print("----------------------")
    print("CHALLENGE RESULTS")
    print("----------------------")
    print("Answers: ", end="")
    for a in used_answers:
        print(a, end=" ")
    print()
    print("Guesses: ", end="")
    for g in guesses:
        print(g, end=" ")
    print()

    print(f"\nTotal time        : {minutes} minutes")
    print(f"Questions answered: {asked}")
    print(f"Correct answers   : {correct}")

    if asked > 0:
        percent = int((correct / asked) * 100)
    else:
        percent = 0
    print(f"Accuracy          : {percent}%")

    if name is not None:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)


def take_quiz_until_wrong(questions, options, answers, name=None):
    indices = list(range(len(questions)))
    random.shuffle(indices)

    guesses = []
    answers_used = []
    score = 0
    asked = 0

    for idx in indices:
        question = questions[idx]
        opts = options[idx]
        correct_answer = answers[idx]

        print("--------------------------")
        print(question)
        for opt in opts:
            print(opt)

        guess = input("Enter (A, B, C, D): ").strip().upper()
        guesses.append(guess)
        answers_used.append(correct_answer)
        asked += 1

        if guess == correct_answer:
            score += 1
            print("CORRECT!")
        else:
            if guess == '':
                print("No answer selected.")
            else:
                print("INCORRECT!")
            print(f"{correct_answer} is the correct answer.")
            print("Quiz over!! First wrong answer reached.")
            break
    print("-------------------------")
    print("STREAK MODE QUIZ RESULTS")
    print("-------------------------")
    print("Answers: ", end="")
    for a in answers_used:
        print(a, end=" ")
    print()
    print("Guesses: ", end="")
    for g in guesses:
        print(g, end=" ")
    print()

    if asked > 0:
        percent = int((score / asked) * 100)
    else:
        percent = 0

    print(f"\nQuestions answered : {asked}")
    print(f"Correct in a row   : {score}")
    print(f"Your score is      : {percent}%")

    if score == asked and asked == len(questions):
        print("\nAmazing! You answered ALL questions correctly!")

    if name is not None:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)


def take_quiz_with_skip(questions, options, answers, name=None):
    
    guesses = []
    score = 0
    skipped = 0
    total = len(questions)

    print("\n===== QUIZ (WITH SKIP) =====")
    print("You can:")
    print("  - Enter A, B, C, or D to answer")
    print("  - Enter S or just press Enter to SKIP a question\n")

    for i, question in enumerate(questions):
        print("----------------------")
        print(f"Q{i+1}. {question}")
        for option in options[i]:
            print(option)

        while True:
            user_input = input("Enter (A, B, C, D) or S to skip: ").strip().upper()

            
            if user_input == "" or user_input == "S":
                guess = "S"       
                skipped += 1
                print("Question skipped.")
                break
            elif user_input in ("A", "B", "C", "D"):
                guess = user_input
                break
            else:
                print("Invalid input. Please enter A, B, C, D, or S to skip.")

        guesses.append(guess)

        if guess == answers[i]:
            score += 1
            print("CORRECT!")
        elif guess != "S":
            print("INCORRECT!")
            print(f"{answers[i]} is the correct answer")

    
    print("----------------------")
    print("     SKIP QUIZ RESULTS")
    print("----------------------")
    print("Answers: ", end="")
    for answer in answers:
        print(answer, end=" ")
    print()

    print("Guesses: ", end="")
    for guess in guesses:
        print(guess, end=" ")
    print()

    answered = total - skipped
    if answered > 0:
        percent = int((score / answered) * 100)
    else:
        percent = 0

    print(f"\nTotal questions : {total}")
    print(f"Answered        : {answered}")
    print(f"Skipped         : {skipped}")
    print(f"Correct         : {score}")
    print(f"Your score is   : {percent}% (based only on answered questions)")

    if name is not None:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)

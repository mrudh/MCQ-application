import sys
import time
import random
from utils import print_results, load_scores, save_scores


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


def take_quiz_challenge(questions, options, answers, name=None):
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


def learning_mode(questions, answers):
    indices = list(range(len(questions)))
    random.shuffle(indices)

    total_seen = 0
    correct_self = 0

    print("\n--- LEARNING MODE ---")
    print("Press Enter to see the answer for each question.")
    print("After seeing the answer, type 'y' if you got it right, 'n' if not.")
    print("Type 'q' at any time to quit learning mode.\n")

    for idx in indices:
        question = questions[idx]
        answer = answers[idx]

        print("----------------------")
        print(f"Q: {question}")
        input("Press Enter to reveal the answer...")

        print(f"A: {answer}")

        while True:
            mark = input("Did you get it right? (y/n, or q to quit): ").strip().lower()
            if mark in ("y", "n", "q"):
                break
            print("Please enter 'y', 'n', or 'q'.")

        if mark == "q":
            break

        total_seen += 1
        if mark == "y":
            correct_self += 1

    print("\n--- LEARNING MODE QUIZ SUMMARY ---")
    print(f"Cards reviewed : {total_seen}")
    print(f"Marked correct : {correct_self}")

    if total_seen > 0:
        accuracy = int((correct_self / total_seen) * 100)
    else:
        accuracy = 0

    print(f"Self-rated accuracy: {accuracy}%")
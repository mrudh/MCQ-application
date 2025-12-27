import sys
import time
import random
from mcq_types import take_quiz, timed_quiz
from utils import print_results, load_scores, save_scores

def _normalize_text(s: str) -> str:
    return " ".join(s.strip().lower().split())


def menu():
    print("\n====== QUIZ MENU ======")
    print("1. Quick quiz")                 
    print("2. Quiz modes")                
    print("3. Assessments")              
    print("4. Review & tools")           
    print("5. Certification exam")       
    print("0. Exit")
    

def quiz_by_topic(ALL_QUIZ_DATA):
    topics = sorted(list(set(q['topic'] for q in ALL_QUIZ_DATA)))
    if not topics:
        print("No topics found in the quiz data.")
        return
    print("Select a topic:")
    for idx, topic in enumerate(topics):
        count = sum(1 for q in ALL_QUIZ_DATA if q['topic'] == topic)
        print(f"{idx + 1}. {topic} ({count} questions)")
    try:
        topic_index = int(input("Enter topic number: ")) - 1
        if 0 <= topic_index < len(topics):
            selected_topic = topics[topic_index]
            selected_data = [q for q in ALL_QUIZ_DATA if q['topic'] == selected_topic]

            questions = [q['question'] for q in selected_data]
            options = [q['options'] for q in selected_data]
            answers = [q['answer'] for q in selected_data]
            
            take_quiz(questions, options, answers)
        else:
            print("Invalid topic selection.")
    except ValueError:
        print("Invalid input.")


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


def age_based_quiz(ALL_QUIZ_DATA):
    import random
     
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



def take_fill_in_the_blanks_quiz(questions, answers, name=None):
   
    guesses = []
    score = 0
    total = len(questions)

    print("\n===== FILL-IN-THE-BLANKS QUIZ =====")
    print("Type your answer in the blank. Answers are not case sensitive.\n")

    for i, question in enumerate(questions):
        print("----------------------")
        print(f"Q{i+1}. {question}")
        user_answer = input("Your answer: ").strip()
        guesses.append(user_answer)
        normalized_user = _normalize_text(user_answer)
        raw_correct = answers[i]
        correct_variants = [a.strip() for a in raw_correct.split("|")]
        normalized_correct_variants = [_normalize_text(a) for a in correct_variants]

        if normalized_user in normalized_correct_variants:
            score += 1
            print("CORRECT!")
        else:
            print("INCORRECT!")
            print("Accepted answer(s): " + " / ".join(correct_variants))

    print("----------------------")
    print("  FILL-IN QUIZ RESULTS")
    print("----------------------")

    print("Correct answers: ", end="")
    for a in answers:
        print(a, end=" | ")
    print()

    print("Your answers : ", end="")
    for g in guesses:
        print(g, end=" | ")
    print()

    percent = int((score / total) * 100) if total > 0 else 0
    print(f"\nTotal questions : {total}")
    print(f"Correct         : {score}")
    print(f"Your score is   : {percent}%")

    if name is not None:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)


def take_quiz_with_summary(questions, options, answers, name=None, timed=False):
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
            print(f"The correct answer is: {answers[i]}")

    
    percent = int((score / total) * 100)

    
    if percent <= 25:
        summary = "A challenging start, but every expert begins here. Review the basics and try again—you’ll improve quickly!"
    elif percent <= 50:
        summary = "Good effort! You’re starting to grasp the concepts. A little more practice will take you a long way."
    elif percent <= 75:
        summary = "Nice work! You’ve shown solid understanding. Keep practicing to reach full mastery."
    else:
        summary = "Excellent performance! You have a strong command of the material. Outstanding job!"

    print("----------------------")
    print("         RESULTS       ")
    print("----------------------")
    print("Answers: ", " ".join(answers))
    print("Guesses: ", " ".join(guesses))
    print(f"\nScore: {score} / {total}")
    print(f"Percentage: {percent}%")
    print("\n Summary:")
    print(summary)

    
    if name:
        scores = load_scores()
        scores.append({"name": name, "score": percent})
        save_scores(scores)


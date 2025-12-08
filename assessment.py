from storage import load_custom_assessments, save_custom_assessments
from mcq import take_quiz
from attempts import can_attempt_quiz, record_quiz_attempt 

def create_assessment():
    custom_questions = []
    custom_options = []
    custom_answers = []
    name = input("Enter a name for this assessment: ").strip()
    n = int(input("How many questions in your assessment? "))
    for i in range(n):
        q = input(f"Enter question {i+1}: ")
        opts = []
        for j in "ABCD":
            opt = input(f"Enter option {j}: ")
            opts.append(f"{j}. {opt}")
        ans = input("Enter correct option (A/B/C/D): ").strip().upper()
        custom_questions.append(q)
        custom_options.append(tuple(opts))
        custom_answers.append(ans)
    assessments = load_custom_assessments()
    assessments.append({"name": name, "questions": custom_questions, "options": custom_options, "answers": custom_answers})
    save_custom_assessments(assessments)
    print(f"Assessment '{name}' created and saved!")
    take_now = input("Take this assessment now? (y/n): ").strip().lower()
    if take_now == 'y':
        take_quiz(custom_questions, custom_options, custom_answers)

def open_assessment():
    assessments = load_custom_assessments()
    if not assessments:
        print("No assessments saved yet.")
        return
    print("\nSaved assessments:")
    for idx, a in enumerate(assessments):
        print(f"{idx + 1}. {a['name']}")
    try:
         sel = int(input("Enter assessment number to open: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    if not (0 <= sel < len(assessments)):
        print("Invalid selection.")
        return

    assessment = assessments[sel]
    assessment_name = assessment["name"]

    user_name = input("Enter your name: ").strip()
    if not user_name:
        print("Name cannot be empty.")
        return

    attempt_key = f"{user_name}::{assessment_name}"

    can_attempt, remaining = can_attempt_quiz(attempt_key)
    if not can_attempt:
        print(
            f"Sorry {user_name}, you have used all your attempts for "
            f"'{assessment_name}' today."
        )
        return

    print(
        f"You have {remaining} attempt(s) left today for the assessment "
        f"'{assessment_name}'."
    )

    record_quiz_attempt(attempt_key)

    print(f"\nOpening assessment: {assessment_name}")
    take_quiz(assessment["questions"], assessment["options"], assessment["answers"], name=user_name)



def list_assessments():
    assessments = load_custom_assessments()
    if not assessments:
        print("No assessments saved yet.")
        return None
    print("\nSaved assessments:")
    for i, a in enumerate(assessments):
        print(f"{i+1}. {a['name']}")
    return assessments


def add_question_to_assessment():
    assessments = list_assessments()
    if not assessments: return

    try:
        sel = int(input("Select assessment to add a question: ")) - 1
        assessment = assessments[sel]
    except:
        print("Invalid input.")
        return

    q = input("Enter new question: ")
    opts = []
    for j in "ABCD":
        opt = input(f"Enter option {j}: ")
        opts.append(f"{j}. {opt}")
    ans = input("Enter correct answer (A/B/C/D): ").strip().upper()

    assessment["questions"].append(q)
    assessment["options"].append(tuple(opts))
    assessment["answers"].append(ans)
    save_custom_assessments(assessments)
    print("Question added successfully!")


def edit_question_in_assessment():
    assessments = list_assessments()
    if not assessments: return

    try:
        sel = int(input("Select assessment to edit: ")) - 1
        assessment = assessments[sel]
    except:
        print("Invalid selection.")
        return

    for i, q in enumerate(assessment["questions"]):
        print(f"{i+1}. {q}")

    try:
        q_idx = int(input("Select a question number to edit: ")) - 1
    except:
        print("Invalid input.")
        return

    if q_idx < 0 or q_idx >= len(assessment["questions"]):
        print("Invalid selection.")
        return

    print(f"Editing question: {assessment['questions'][q_idx]}")
    new_q = input("Enter new question (leave blank to keep same): ")
    if new_q:
        assessment["questions"][q_idx] = new_q
    new_opts = []
    for j in "ABCD":
        current_opt = assessment["options"][q_idx][ord(j)-65]
        new_opt = input(f"{j} ({current_opt}): ")
        new_opts.append(new_opt if new_opt else current_opt)
    assessment["options"][q_idx] = tuple(new_opts)

    new_ans = input(f"Enter new answer (leave blank to keep {assessment['answers'][q_idx]}): ").upper()
    if new_ans:
        assessment["answers"][q_idx] = new_ans

    save_custom_assessments(assessments)
    print("Question updated!")


def delete_question_from_assessment():
    assessments = list_assessments()
    if not assessments: return

    try:
        sel = int(input("Select assessment: ")) - 1
        assessment = assessments[sel]
    except:
        print("Invalid input.")
        return

    for i, q in enumerate(assessment["questions"]):
        print(f"{i+1}. {q}")

    try:
        q_idx = int(input("Select a question number to delete: ")) - 1
    except:
        print("Invalid input.")
        return

    if q_idx < 0 or q_idx >= len(assessment["questions"]):
        print("Invalid selection.")
        return

    removed = assessment["questions"].pop(q_idx)
    assessment["options"].pop(q_idx)
    assessment["answers"].pop(q_idx)
    save_custom_assessments(assessments)
    print(f"Deleted: {removed}")


def view_questions_in_assessment():
    assessments = load_custom_assessments()
    if not assessments:
        print("No assessments saved yet.")
        return

    print("\nSaved assessments:")
    for idx, a in enumerate(assessments):
        print(f"{idx + 1}. {a['name']}")

    try:
        sel = int(input("Select an assessment to view: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    if sel < 0 or sel >= len(assessments):
        print("Invalid selection.")
        return

    assessment = assessments[sel]
    print(f"\n--- Assessment: {assessment['name']} ---")

    questions = assessment.get("questions", [])
    options_list = assessment.get("options", [])
    answers = assessment.get("answers", [])

    if not questions:
        print("This assessment has no questions yet.")
        return

    for i, question in enumerate(questions):
        print("\n----------------------")
        print(f"Q{i + 1}: {question}")
        if i < len(options_list):
            for opt in options_list[i]:
                print(opt)
        if i < len(answers):
            print(f"Correct answer: {answers[i]}")
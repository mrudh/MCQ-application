from storage import load_custom_assessments, save_custom_assessments
from mcq import take_quiz

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
        if 0 <= sel < len(assessments):
            a = assessments[sel]
            print(f"Opening assessment: {a['name']}")
            take_quiz(a["questions"], a["options"], a["answers"])
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


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
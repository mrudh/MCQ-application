from storage import load_custom_assessments, save_custom_assessments


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
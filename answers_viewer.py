from quiz_data import ALL_QUIZ_DATA, FILL_IN_QUIZ_DATA


def _get_option_text(options, correct_letter):
    correct_letter = correct_letter.strip().upper()
    for opt in options:
        if opt.strip().upper().startswith(correct_letter + "."):
            return opt
    return f"{correct_letter} (option text not found)"


def show_all_mcq_answers():
    print("\n===== ANSWER KEY: MULTIPLE-CHOICE QUESTIONS =====\n")
    for idx, q in enumerate(ALL_QUIZ_DATA, start=1):
        question = q["question"]
        options = q["options"]
        answer_letter = q["answer"]

        print(f"Q{idx}. {question}")
        for opt in options:
            print(f"   {opt}")

        correct_option_text = _get_option_text(options, answer_letter)
        print(f"   Correct answer: {answer_letter} -> {correct_option_text}")
        print()


def show_all_fill_in_answers():
    print("\n===== ANSWER KEY: FILL-IN-THE-BLANKS QUESTIONS =====\n")
    for idx, q in enumerate(FILL_IN_QUIZ_DATA, start=1):
        question = q["question"]
        raw_answer = q["answer"]

        print(f"Q{idx}. {question}")
        accepted = [a.strip() for a in raw_answer.split("|")]
        print("   Accepted answer(s): " + " / ".join(accepted))
        print()


def show_all_answers():
    show_all_mcq_answers()
    show_all_fill_in_answers()

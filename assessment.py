from assessment_storage import load_custom_assessments, save_custom_assessments
from mcq import take_quiz
from attempts import can_attempt_quiz, record_quiz_attempt


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
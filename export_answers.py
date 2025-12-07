import json
from quiz_data import ALL_QUIZ_DATA, FILL_IN_QUIZ_DATA


def _get_option_text(options, correct_letter):
   
    correct_letter = correct_letter.strip().upper()
    for opt in options:
        if opt.strip().upper().startswith(correct_letter + "."):
            return opt
    return f"{correct_letter} (option text not found)"


def export_answers(filename="exported_answers.json"):
    
    data = {
        "mcq_answers": [],
        "fill_in_answers": [],
    }


    for idx, q in enumerate(ALL_QUIZ_DATA, start=1):
        question_text = q.get("question")
        options = list(q.get("options", ()))
        correct_letter = q.get("answer", "").strip().upper()
        topic = q.get("topic")
        difficulty = q.get("difficulty")

        correct_option_text = _get_option_text(options, correct_letter)

        data["mcq_answers"].append({
            "number": idx,
            "question": question_text,
            "options": options,
            "correct_letter": correct_letter,
            "correct_option_text": correct_option_text,
            "topic": topic,
            "difficulty": difficulty,
        })


    for idx, q in enumerate(FILL_IN_QUIZ_DATA, start=1):
        question_text = q.get("question")
        raw_answer = q.get("answer", "")
        topic = q.get("topic")
        difficulty = q.get("difficulty")

        accepted_answers = [a.strip() for a in raw_answer.split("|") if a.strip()]

        data["fill_in_answers"].append({
            "number": idx,
            "question": question_text,
            "accepted_answers": accepted_answers,
            "raw_answer": raw_answer,
            "topic": topic,
            "difficulty": difficulty,
        })

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nAll answers exported successfully to '{filename}'")
    except Exception as e:
        print(f"Error exporting answers: {e}")


if __name__ == "_main_":
    print("=== Export Answers Utility ===")
    default_name = "exported_answers.json"
    filename = input(f"Enter filename to export to (default: {default_name}): ").strip()
    if not filename:
        filename = default_name
    export_answers(filename)
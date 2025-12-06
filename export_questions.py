import json
from quiz_data import ALL_QUIZ_DATA


def export_questions(filename="exported_questions.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(ALL_QUIZ_DATA, f, indent=4)
        print(f"\nAll questions exported successfully to '{filename}'")
    except Exception as e:
        print(f"Error exporting questions: {e}")

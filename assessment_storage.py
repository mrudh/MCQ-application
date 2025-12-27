import os
import json

ASSESSMENT_FILE = "custom_assessment.json"

def load_custom_assessments():
    if not os.path.exists(ASSESSMENT_FILE):
        return []
    try:
        with open(ASSESSMENT_FILE, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

def save_custom_assessments(assessments):
    with open(ASSESSMENT_FILE, "w") as f:
        json.dump(assessments, f)
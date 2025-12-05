import os
import json
from datetime import date

MAX_ATTEMPTS_PER_DAY = 3   

ATTEMPT_FILE = "attempts.json"


def _load_attempts():
    if os.path.exists(ATTEMPT_FILE):
        with open(ATTEMPT_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_attempts(data):
    with open(ATTEMPT_FILE, "w") as f:
        json.dump(data, f)


def _today_str():
    return date.today().isoformat()


def get_attempts_left(name, max_attempts=MAX_ATTEMPTS_PER_DAY):
    name = name.strip()
    attempts = _load_attempts()
    today = _today_str()

    user_attempts = attempts.get(name, {})
    used_today = user_attempts.get(today, 0)

    remaining = max(0, max_attempts - used_today)
    return remaining


def can_attempt_quiz(name, max_attempts=MAX_ATTEMPTS_PER_DAY):
    remaining = get_attempts_left(name, max_attempts=max_attempts)
    return remaining > 0, remaining


def record_quiz_attempt(name):
    name = name.strip()
    attempts = _load_attempts()
    today = _today_str()

    user_attempts = attempts.setdefault(name, {})
    user_attempts[today] = user_attempts.get(today, 0) + 1

    _save_attempts(attempts)

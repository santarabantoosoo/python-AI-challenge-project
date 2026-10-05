"""Server-side AI battle rate limit: max 5 AI battles per cooldown window.
Stored in a JSON file next to the app (works for Streamlit Community Cloud
single instance / school demo). Browser-side limits are NOT trusted.
"""
import json
import os
import time

MAX_BATTLES = 5
COOLDOWN_SECONDS = 60 * 60  # 1 hour rest after 5 battles
STATE_FILE = os.path.join(os.path.dirname(__file__), ".ai_battle_count.json")


def _load():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"count": 0, "window_start": time.time()}


def _save(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def battles_left():
    state = _load()
    if time.time() - state["window_start"] > COOLDOWN_SECONDS:
        return MAX_BATTLES
    return max(0, MAX_BATTLES - state["count"])


def can_start_ai_battle():
    return battles_left() > 0


def record_ai_battle():
    state = _load()
    if time.time() - state["window_start"] > COOLDOWN_SECONDS:
        state = {"count": 0, "window_start": time.time()}
    state["count"] += 1
    _save(state)
    return MAX_BATTLES - state["count"]

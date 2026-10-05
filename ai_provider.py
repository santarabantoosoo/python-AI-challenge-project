"""AI question wrapper for students.

Students call ONE function:
    question = generate_ai_question(subject, round_no)

- If OPENAI_API_KEY is set, it tries a real AI API (OpenAI chat format),
  constrained to APPROVED_DOCS (controlled knowledge).
- Otherwise it uses the offline fallback bank (no internet needed),
  so the app always works in class.

Returns dict: q, options[4], correct (A-D), explanation, concept, source.
Python (not the AI) evaluates the student's answer.
"""
import os
import json
import random
import urllib.request

from ai_docs import APPROVED_DOCS

# Offline fallback: extra questions NOT in the teacher bank (so AI feels new).
FALLBACK_AI_BANK = {
"Science": [
{"q": "Which gas do plants release during photosynthesis?", "options": ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"], "correct": "B", "explanation": "Plants release oxygen as they make food.", "concept": "photosynthesis"},
{"q": "What is water vapor?", "options": ["Solid water", "Liquid water", "Water as a gas", "Frozen water"], "correct": "C", "explanation": "Vapor is water in gas form after heating.", "concept": "states of matter"},
{"q": "Why does a parachute fall slowly?", "options": ["No gravity", "Air resistance pushes up", "It is heavy", "Wind pushes down"], "correct": "B", "explanation": "Air resistance pushes up against gravity.", "concept": "forces and motion"},
],
"Geography": [
{"q": "Which continent has the Sahara desert?", "options": ["Asia", "Africa", "Europe", "Australia"], "correct": "B", "explanation": "The Sahara is in Africa.", "concept": "deserts"},
{"q": "What is the Equator?", "options": ["Top of Earth", "Middle line of Earth", "A country", "An ocean"], "correct": "B", "explanation": "The Equator circles Earth's middle.", "concept": "globe"},
{"q": "Where does the sun set?", "options": ["East", "West", "North", "South"], "correct": "B", "explanation": "Sun rises east, sets west.", "concept": "compass"},
],
"Mathematics": [
{"q": "What is 6 x 7?", "options": ["42", "36", "48", "40"], "correct": "A", "explanation": "6 times 7 is 42.", "concept": "multiplication"},
{"q": "Which is equal to 1/2?", "options": ["1/4", "2/4", "3/4", "1/3"], "correct": "B", "explanation": "2/4 simplifies to 1/2.", "concept": "fractions"},
{"q": "What is the perimeter of a 3cm square?", "options": ["6cm", "9cm", "12cm", "7cm"], "correct": "C", "explanation": "4 sides x 3 = 12cm.", "concept": "area"},
],
"History": [
{"q": "What were Egyptian pyramids used for?", "options": ["Schools", "Tombs", "Shops", "Bridges"], "correct": "B", "explanation": "Pyramids were tombs for pharaohs.", "concept": "ancient egypt"},
{"q": "Where did the Olympics begin?", "options": ["Rome", "Greece", "Egypt", "China"], "correct": "B", "explanation": "The Olympics began in ancient Greece.", "concept": "ancient greece"},
{"q": "How many years in a century?", "options": ["10", "50", "100", "1000"], "correct": "C", "explanation": "A century is 100 years.", "concept": "history skills"},
],
"Python": [
{"q": "What does print('Hi') do?", "options": ["Reads input", "Shows Hi on screen", "Saves a file", "Deletes text"], "correct": "B", "explanation": "print() displays output.", "concept": "output"},
{"q": "Which line stores 10 in x?", "options": ["x == 10", "x = 10", "x -> 10", "10 = x"], "correct": "B", "explanation": "= assigns the value.", "concept": "variables"},
{"q": "What keyword repeats while a condition is True?", "options": ["if", "for", "while", "else"], "correct": "C", "explanation": "while loops while True.", "concept": "loops"},
],
}

def _try_real_api(subject, round_no):
    """Optional: use OpenAI-compatible API if key exists. Returns dict or None."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return None
    docs = "\n".join("- " + d for d in APPROVED_DOCS.get(subject, []))
    prompt = (
        f"Generate ONE multiple-choice question for children (age 11-12) about {subject}. "
        f"Use ONLY these approved facts:\n{docs}\n"
        'Reply with JSON only: {"q": "...", "options": ["...", "...", "...", "..."], '
        '"correct": "A", "explanation": "one short sentence", "concept": "short concept name"}'
    )
    try:
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps({
                "model": os.getenv("AI_MODEL", "gpt-4o-mini"),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            }).encode(),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
        text = data["choices"][0]["message"]["content"]
        # strip code fences if present
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        q = json.loads(text)
        assert q["correct"] in "ABCD" and len(q["options"]) == 4
        q["source"] = "ai-api"
        return q
    except Exception:
        return None


def generate_ai_question(subject, round_no=1, used_questions=None):
    """Student-facing helper. Always returns a valid MCQ dict."""
    used_questions = used_questions or []
    real = _try_real_api(subject, round_no)
    if real:
        return real
    pool = [q for q in FALLBACK_AI_BANK.get(subject, []) if q["q"] not in used_questions]
    if not pool:  # reuse with shuffle if exhausted
        pool = FALLBACK_AI_BANK.get(subject, [])
    q = random.choice(pool).copy()
    q["source"] = "ai-fallback (offline)"
    return q

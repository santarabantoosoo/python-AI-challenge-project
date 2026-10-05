"""AI Challenge Battle — Streamlit app (student-built final project).

Run:  streamlit run app.py
Needs: pip install streamlit

How it maps to the project spec:
  Stage 1: 15 teacher questions, need 4 correct IN A ROW (streak).
  Unlock:  "HORRAAY! AI HAS JOINED THE BATTLE!"
  Stage 2: while answer_is_correct: AI generates Q, PYTHON evaluates it.
  End: first mistake -> explanation + concept illustration.
  Limit: 5 AI battles per hour (server-side, see rate_limit.py).
"""
import random
import streamlit as st

from questions_bank import QUESTIONS, SUBJECTS, SUBJECT_EMOJI
from ai_provider import generate_ai_question
from illustrations import get_illustration
from rate_limit import battles_left, can_start_ai_battle, record_ai_battle

st.set_page_config(page_title="AI Challenge Battle", page_icon="🧠")

# ---------- tiny student-readable helpers ----------
def check_answer(student_answer, correct_answer):
    """Python (not AI) decides. Returns True/False."""
    return student_answer == correct_answer


def letter_options(options):
    return ["A", "B", "C", "D"]


# ---------- session state (the program's memory) ----------
def init_state():
    defaults = {
        "subject": "Science",
        "stage": "challenge",   # challenge | unlocked | ai_battle | gameover
        "order": [],            # shuffled teacher-question indexes
        "q_index": 0,
        "streak": 0,
        "score": 0,
        "current": None,        # current question dict
        "ai_score": 0,
        "ai_used": [],
        "ai_explain": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    # First load: order is [] until new_challenge() runs -> populate it now
    # so get_teacher_question() never indexes into an empty list.
    if not st.session_state.order:
        n = len(QUESTIONS.get(st.session_state.subject, [])) or 15
        st.session_state.order = random.sample(range(n), n)


def new_challenge(subject):
    st.session_state.subject = subject
    st.session_state.stage = "challenge"
    n = len(QUESTIONS.get(subject, [])) or 15
    st.session_state.order = random.sample(range(n), n)
    st.session_state.q_index = 0
    st.session_state.streak = 0
    st.session_state.score = 0
    st.session_state.current = None
    st.session_state.ai_score = 0
    st.session_state.ai_used = []
    st.session_state.ai_explain = None


def get_teacher_question():
    """Pick next prepared question (loops if bank exhausted)."""
    bank = QUESTIONS[st.session_state.subject]
    if not st.session_state.order:
        st.session_state.order = random.sample(range(len(bank)), len(bank))
        st.session_state.q_index = 0
    idx = st.session_state.order[st.session_state.q_index % len(st.session_state.order)]
    st.session_state.q_index += 1
    q = bank[idx].copy()
    q["source"] = "teacher"
    return q


def show_question(q, key_prefix):
    st.subheader(q["q"])
    labels = [f"{L}. {opt}" for L, opt in zip(letter_options(q["options"]), q["options"])]
    choice = st.radio("Choose your answer:", labels, key=f"{key_prefix}_{st.session_state.q_index}_{st.session_state.ai_score}")
    return choice[0]  # the letter A-D


# ---------- UI ----------
init_state()

st.title("🧠 AI CHALLENGE")
st.caption("Python controls the game. The AI provides the challenge. You control the outcome.")

with st.sidebar:
    st.header("Choose your subject")
    for s in SUBJECTS:
        if st.button(f"{SUBJECT_EMOJI[s]} {s}", use_container_width=True):
            new_challenge(s)
            st.rerun()
    st.divider()
    st.write(f"🤖 AI battles left: **{battles_left()} / 5**")
    if st.button("🔄 Restart"):
        new_challenge(st.session_state.subject)
        st.rerun()
    show_logic = st.checkbox("👀 Show student Python logic")

subject = st.session_state.subject
st.header(f"{SUBJECT_EMOJI[subject]} {subject}")

# ================= STAGE 1 =================
if st.session_state.stage == "challenge":
    st.info(f"Goal: get **4 correct in a row** to unlock the AI. Streak: **{st.session_state.streak}/4**  |  Score: {st.session_state.score}")
    st.progress(st.session_state.streak / 4)
    if st.session_state.current is None:
        st.session_state.current = get_teacher_question()
    q = st.session_state.current
    ans = show_question(q, "t")
    if st.button("Submit answer", type="primary"):
        if check_answer(ans, q["correct"]):
            st.session_state.streak += 1
            st.session_state.score += 1
            st.success(f"✅ Correct! Streak: {st.session_state.streak}")
            st.session_state.current = None
            if st.session_state.streak >= 4:
                st.session_state.stage = "unlocked"
            st.rerun()
        else:
            st.session_state.streak = 0  # mistake resets streak
            st.error(f"❌ Not quite. Correct was **{q['correct']}**. Streak reset to 0 — keep going!")
            st.info(f"💡 {q['explanation']}")
            st.session_state.current = None

# ================= UNLOCKED =================
elif st.session_state.stage == "unlocked":
    st.balloons()
    st.success("🎉 HORRAAAAAAY! You got 4 correct answers in a row!")
    st.header("🤖 THE AI HAS JOINED THE BATTLE!")
    if not can_start_ai_battle():
        st.warning("🤖 WHOA! Five champions have already challenged me! My AI brain needs a rest. Come back later!")
    else:
        if st.button("⚔️ Start AI Battle", type="primary"):
            record_ai_battle()
            st.session_state.stage = "ai_battle"
            st.session_state.ai_score = 0
            st.session_state.ai_used = []
            st.session_state.current = generate_ai_question(subject, round_no=1, used_questions=[])
            st.session_state.ai_used.append(st.session_state.current["q"])
            st.rerun()

# ================= STAGE 2: AI BATTLE =================
elif st.session_state.stage == "ai_battle":
    # while answer_is_correct: keep asking (one question per rerun)
    st.warning(f"🤖 AI BATTLE — score: **{st.session_state.ai_score}** (wrong answer ends the battle)")
    if st.session_state.current is None:
        st.session_state.current = generate_ai_question(
            subject, round_no=st.session_state.ai_score + 1, used_questions=st.session_state.ai_used)
        st.session_state.ai_used.append(st.session_state.current["q"])
    q = st.session_state.current
    st.caption(f"AI question #{st.session_state.ai_score + 1} ({q.get('source', 'ai')})")
    ans = show_question(q, "ai")
    if st.button("Submit AI battle answer", type="primary"):
        if check_answer(ans, q["correct"]):
            st.session_state.ai_score += 1
            st.success("✅ Correct! Next AI question...")
            st.session_state.current = None
            st.rerun()
        else:
            # first mistake ends the battle
            st.session_state.stage = "gameover"
            st.session_state.ai_explain = q
            st.rerun()

# ================= GAME OVER =================
elif st.session_state.stage == "gameover":
    q = st.session_state.ai_explain
    st.header(f"🏆 AI Battle Score: {st.session_state.ai_score} correct!")
    st.error("❌ Not quite!")
    if q:
        st.write(f"The correct answer was **{q['correct']}: {q['options']['ABCD'.index(q['correct'])]}**.")
        st.info(f"**Remember:** {q['explanation']}")
        st.code(get_illustration(q.get("concept", "")), language="text")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Play again (same subject)"):
            new_challenge(subject)
            st.rerun()
    with col2:
        if st.button("🏠 Choose subject"):
            st.session_state.stage = "challenge"
            new_challenge(subject)
            st.rerun()

if show_logic:
    st.divider()
    st.subheader("👀 Student Python logic (from the project spec)")
    st.code('''streak = 0
while streak < 4:
    question = get_prepared_question()
    answer = get_student_answer()
    if answer == question["correct_answer"]:
        streak = streak + 1
    else:
        streak = 0   # reset!

print("AI HAS JOINED THE BATTLE!")
answer_is_correct = True
while answer_is_correct:
    question = generate_ai_question()  # AI makes Q, Python checks it
    answer = get_student_answer()
    if answer == question["correct_answer"]:
        print("Correct!")
    else:
        answer_is_correct = False
        show_explanation(question)
        show_illustration(question)''', language="python")

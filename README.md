# 🧠 AI Challenge Battle

A simple educational web app built by students at the end of an introductory Python course.

> **Python controls the game. The AI provides the challenge. You control the outcome.**

Live demo: deploy with Streamlit Community Cloud (see below).

## How it works

- **Stage 1 — The Challenge:** choose a subject (Science, Geography, Mathematics, History, Python) and answer teacher-prepared MCQs. Get **4 correct in a row** to unlock the AI.
- **🎉 HORRAAAAAY! THE AI HAS JOINED THE BATTLE!**
- **Stage 2 — AI Battle:** the AI generates new MCQs. Python (not the AI) evaluates every answer with a `while` loop — the battle continues while you answer correctly.
- **First mistake** ends the battle and shows a short explanation + concept illustration.
- **Limit:** max 5 AI battles per hour (server-side, `rate_limit.py`) to avoid hitting API rate limits.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

No API key needed — without `OPENAI_API_KEY` the app uses an offline fallback question bank, so it always works in class.

Optional (real AI questions, constrained to approved docs in `ai_docs.py`):

```bash
export OPENAI_API_KEY=sk-...
export AI_MODEL=gpt-4o-mini   # optional
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (already done).
2. Go to https://share.streamlit.io → **New app** → select repo `python-AI-challenge-project`, branch `main`, main file `app.py`.
3. (Optional) Add `OPENAI_API_KEY` under **Advanced settings → Secrets**. Without it, offline fallback is used.
4. Click **Deploy**.

## Files

- `app.py` — Streamlit UI + game flow (streak logic, AI battle loop)
- `questions_bank.py` — 15 teacher MCQs per subject
- `ai_provider.py` — `generate_ai_question()` wrapper (real API + offline fallback)
- `ai_docs.py` — approved educational material constraining AI questions
- `illustrations.py` — teacher-approved concept diagrams
- `rate_limit.py` — server-side 5-battles-per-hour limit
- `AI_challenge_project.md` — full project spec

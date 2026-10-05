# Project ideas 

# 🧠 AI Challenge Battle

A simple educational web app built by students at the end of an introductory Python course.


* Students choose a subject and answer **15 teacher-prepared MCQs**.
* They must get **4 answers correct in a row** to unlock the AI.
* 🎉 **“Hooray! AI has joined the battle!”**
* The AI then generates new **MCQs based on approved educational documents**, including the correct answer.
* **Python evaluates every answer** and uses a `while` loop to continue the AI battle as long as the student answers correctly.
* The first mistake ends the battle and displays a **short explanation and simple concept illustration**.
* The app is deployed as a web app for students across the school to try.
* AI usage is limited to **5 AI battles** before a temporary cooldown to avoid hitting rate limits. 
* Students are responsible for all python programming. AI programming via APIs is optional to those who want to learn more. 

## Details

### An Interactive Educational Web App Built by Students

## 1. Project Overview

**AI Challenge Battle** is a small educational web application developed as the final project of an introductory Python course for children.

The project combines the Python concepts learned throughout the course with a simple AI API integration.

Students first demonstrate their knowledge using a set of **teacher-prepared multiple-choice questions**. After achieving a perfect streak of four correct answers, they unlock an **AI Battle**, where the AI generates new multiple-choice questions based on the selected subject and approved educational materials.

The project is designed to be deployed as a web app so that **other students and staff at the school can try it**.

The experience should be simple, fast, educational, and fun.

---

# 2. The Core Experience

The application has two stages.

### Stage 1 — The Challenge

The student chooses a subject, for example:

* 🔬 Science
* 🌍 Geography
* 📐 Mathematics
* 🏛️ History
* 💻 Python

Each subject contains approximately **15 carefully prepared multiple-choice questions**.

The student must achieve:

> **4 correct answers in a row without making a mistake.**

For example:

```text
Question 1
✅ Correct
Streak: 1

Question 2
✅ Correct
Streak: 2

Question 3
✅ Correct
Streak: 3

Question 4
✅ Correct
Streak: 4
```

The application then displays:

> 🎉 HORRAAAAAAY!
>
> You got 4 correct answers in a row!
>
> 🤖 **THE AI HAS JOINED THE BATTLE!**

---

# 3. What Happens After an Incorrect Answer?

An incorrect answer resets the streak.

For example:

```text
Question 1 → ✅
Question 2 → ✅
Question 3 → ❌

Streak: 0
```

The student continues answering questions from the prepared question bank.

This gives the student a simple goal:

> **Can I get four in a row?**

---

# 4. Stage 2 — AI Battle

Once the student achieves four consecutive correct answers, the AI becomes responsible for generating new questions.

However, the AI does **not** evaluate the student's answer.

The AI generates only the question and its correct answer.

For example, the AI might return:

```text
Question:
Which gas do plants take in during photosynthesis?

A. Oxygen
B. Nitrogen
C. Carbon dioxide
D. Hydrogen

Correct answer:
C
```

Python receives this information and presents the question to the student.

The student's answer is then evaluated **entirely by the Python application**.

```text
Student chooses: C

Python:
student_answer == correct_answer

True
```

The student gets another AI-generated question.

---

# 5. The AI-Controlled Loop

The main purpose of the AI stage is to give students a meaningful example of a `while` loop.

Conceptually:

```python
while answer_is_correct:

    question = generate_ai_question()

    answer = get_student_answer()

    if answer == correct_answer:
        print("Correct!")
    else:
        print("Incorrect!")
        break
```

The loop continues for as long as the student answers correctly.

For example:

```text
🤖 AI Question 1
✅ Correct!

🤖 AI Question 2
✅ Correct!

🤖 AI Question 3
✅ Correct!

🤖 AI Question 4
❌ Incorrect!
```

The AI Battle ends when the student makes their first mistake.

The student's final result might be:

> 🏆 AI Battle Score: 4 correct answers!

---

# 6. Why the Evaluation Remains in Python

This is an important part of the project design.

The AI is **not** responsible for deciding whether the student is correct.

Instead:

### AI

* Generates an MCQ.
* Provides the four answer choices.
* Identifies the correct answer.
* Provides information needed for an explanation after a mistake.

### Python

* Displays the question.
* Collects the student's answer.
* Compares the student's answer with the correct answer.
* Maintains the score.
* Maintains the streak.
* Controls the `while` loop.
* Decides when the AI Battle ends.
* Controls the application flow.

This keeps the project fundamentally a **Python programming project with an AI component**, rather than an AI project where Python is merely making API calls.

---

# 7. Controlled AI Knowledge

The AI should not generate arbitrary questions about any subject.

Each subject will have a small collection of approved educational documents.

For example:

```text
Science
├── States of Matter
├── Plants
├── Solar System
├── Forces and Motion
└── Water Cycle
```

The AI is instructed to generate questions **only from the supplied educational material**.

This provides greater control over:

* Age appropriateness
* Educational relevance
* Factual content
* Difficulty
* Curriculum alignment

The AI can therefore generate new questions while remaining within a defined knowledge boundary.

---

# 8. AI Question Requirements

Every AI-generated question must be a multiple-choice question.

The AI should return a structured result containing:

```text
Question
Option A
Option B
Option C
Option D
Correct Answer
Concept
```

For example:

```text
Question:
What happens when water reaches its boiling point?

A. It becomes ice.
B. It becomes water vapor.
C. It disappears.
D. It becomes soil.

Correct Answer:
B

Concept:
Change of state
```

The application then handles the rest.

The AI should **not** return an open-ended question.

It should also not evaluate the student's answer.

---

# 9. Learning From Mistakes

When the student eventually answers an AI question incorrectly, the application ends the AI Battle.

Instead of simply displaying:

> ❌ Wrong

the application provides a short learning moment.

For example:

> ❌ Not quite!
>
> The correct answer was **B: Water vapor**.
>
> **Remember:** When liquid water is heated to its boiling point, it changes into a gas called water vapor.

The application can then display a simple educational illustration or diagram related to the concept.

---

# 10. Concept Illustration

The AI can identify the relevant concept associated with the question.

For example:

```text
concept = "states of matter"
```

The application can then display a simple predefined diagram:

```text
       HEAT
         ↓
  💧 LIQUID WATER
         ↓
    💨 WATER VAPOR
```

The first implementation can use a small library of teacher-approved illustrations.

Possible concepts include:

* Water cycle
* States of matter
* Solar system
* Plant structure
* Food chain
* Fractions
* Electricity
* Gravity
* Photosynthesis

This keeps the visual educational content reliable and consistent.

---

# 11. The Role of the Students

The students do not need to implement the AI infrastructure themselves.

The course instructor can provide a simple function/API wrapper such as:

```python
generate_ai_question()
```

The students use the function as part of their Python program.

Their responsibility is to build the program logic around it.

They will need to apply:

* Variables
* Input
* Output
* Conditional statements
* Comparison operators
* Counters
* `while` loops
* Lists or simple data structures
* Basic program flow

Depending on the course scope, they may also use:

* `for` loops
* Functions
* Random selection

---

# 12. Example Student Logic

A simplified version of the final logic could look like:

```python
streak = 0

while streak < 4:

    question = get_prepared_question()

    display_question(question)

    answer = get_student_answer()

    if answer == question["correct_answer"]:
        streak = streak + 1
        print("Correct!")
    else:
        streak = 0
        print("Try again!")

print("HORRAAY!")
print("AI HAS JOINED THE BATTLE!")

answer_is_correct = True

while answer_is_correct:

    question = generate_ai_question()

    display_question(question)

    answer = get_student_answer()

    if answer == question["correct_answer"]:
        print("Correct!")
    else:
        answer_is_correct = False
        show_explanation(question)
        show_illustration(question)
```

The actual AI/API implementation can be hidden inside the provided helper function.

---

# 13. School-Wide Deployment

The finished project will be deployed as a web application.

Any student or staff member at the school can open the application and play.

The interface should be intentionally minimal:

```text
┌─────────────────────────────┐
│      🧠 AI CHALLENGE        │
│                             │
│   Choose your subject       │
│                             │
│   🔬 Science                │
│   🌍 Geography              │
│   📐 Mathematics            │
│   🏛️ History                │
│   💻 Python                 │
│                             │
└─────────────────────────────┘
```

The application should require no programming knowledge from the person playing it.

---

# 14. AI Usage Limitation

Because the application may be available to the whole school, AI usage should be controlled.

The application can allow a limited number of AI Battle sessions within a defined period.

For example:

> **Maximum: 5 AI Battle sessions**

Once the limit is reached:

> 🤖 WHOA!
>
> Five champions have already challenged me!
>
> My AI brain needs a little rest.
>
> **Come back later!**

Importantly, the limit applies to the **AI Battle**, not the initial question bank.

This means many students can use the normal educational challenge without consuming AI resources.

The rate limit should be implemented on the server side rather than relying on browser-side code.

---

# 15. Educational Value

The project provides students with a practical reason to use the programming concepts they have learned.

### Variables

Students maintain:

```text
score
streak
correct_answer
```

### Conditions

Python determines:

```text
Is the answer correct?
Has the student reached four consecutive correct answers?
```

### Loops

The first stage repeatedly presents questions until the student achieves the required streak.

The second stage introduces the more natural use of a `while` loop:

> **Keep asking questions while the student continues answering correctly.**

### API Integration

Students see how a Python program can communicate with an external service.

### Real-World Deployment

Their program becomes a functioning web application that can be used by other people.

---

# 16. Why the Project Is Exciting

The project has a clear progression:

```text
PLAY
  ↓
ANSWER
  ↓
BUILD A STREAK
  ↓
4 PERFECT ANSWERS
  ↓
🎉 AI UNLOCKED!
  ↓
🤖 AI BATTLE
  ↓
KEEP ANSWERING CORRECTLY
  ↓
MAKE A MISTAKE
  ↓
💡 LEARN FROM THE MISTAKE
```

The AI therefore feels like something the student **earns**, rather than something that is present from the beginning.

This also gives the final project a memorable moment:

> **“HORRAAAAAY — AI HAS JOINED THE BATTLE!”**

---

# 17. Final Project Goal

The goal is not to build a sophisticated AI system.

The goal is to give children a first experience of building a **real interactive software application** that:

1. Solves a simple problem.
2. Uses the Python concepts they have learned.
3. Uses a `while` loop for a meaningful purpose.
4. Connects to an external AI service.
5. Uses controlled educational content.
6. Provides immediate feedback.
7. Turns mistakes into learning opportunities.
8. Can be deployed and used by real people at the school.

The final result is a small but complete educational application:

> **Python controls the game.
> The AI provides the challenge.
> The student controls the outcome.**

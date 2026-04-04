# modules/take_test.py

import streamlit as st
import uuid
from datetime import datetime

from config.settings import DOCS_DIR, MAX_QUESTIONS
from database.db_manager import insert_row
from config.settings import TEST_SESSIONS_FILE, QUESTION_LOGS_FILE

from rag.rag_pipeline import load_rag_pipeline
from agents.question_agent import generate_questions
from agents.hint_agent import generate_hint
from agents.explain_agent import generate_explanation
from agents.example_agent import generate_example


# ==============================
# 🚀 INITIALIZE TEST SESSION
# ==============================

def init_test_session(user, test_id):
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.start_time = datetime.now()
        st.session_state.q_index = 0
        st.session_state.answers = {}
        st.session_state.hints = {}
        st.session_state.explains = {}
        st.session_state.examples = {}


# ==============================
# 🧠 LOAD QUESTIONS (RAG)
# ==============================

def load_questions(test_id):
    if "questions" not in st.session_state:
        doc_path = f"{DOCS_DIR}/{test_id}.pdf"

        qa_chain = load_rag_pipeline(doc_path)

        context = qa_chain.run("Extract key concepts from document")

        questions = generate_questions(context)

        st.session_state.questions = [
            q.strip() for q in questions.split("\n") if q.strip()
        ][:MAX_QUESTIONS]


# ==============================
# 💾 SAVE QUESTION LOG
# ==============================

def log_question(session_id, qid, question, answer):
    insert_row(QUESTION_LOGS_FILE, {
        "Session_ID": session_id,
        "Question_ID": qid,
        "Question_Text": question,
        "Answer": answer,
        "Time_Spent": 0,
        "Hint_Clicks": st.session_state.hints.get(qid, 0),
        "Explain_Clicks": st.session_state.explains.get(qid, 0),
        "Example_Clicks": st.session_state.examples.get(qid, 0),
        "Revisits": 0,
    })


# ==============================
# 🏁 COMPLETE TEST
# ==============================

def complete_test(user, test_id):
    end_time = datetime.now()
    start_time = st.session_state.start_time

    total_time = (end_time - start_time).total_seconds()

    insert_row(TEST_SESSIONS_FILE, {
        "Session_ID": st.session_state.session_id,
        "USN": user["USN"],
        "Assignment_ID": test_id,
        "Start_Time": start_time,
        "End_Time": end_time,
        "Total_Time": total_time,
        "Completed": True,
    })

    # Save all answers
    for i, q in enumerate(st.session_state.questions):
        log_question(
            st.session_state.session_id,
            f"Q{i+1}",
            q,
            st.session_state.answers.get(i, "")
        )

    st.success("✅ Test Completed Successfully!")

    # Clear session
    for key in ["questions", "q_index", "answers"]:
        st.session_state.pop(key, None)


# ==============================
# 🎯 MAIN TEST PAGE
# ==============================

def take_test_page(user, test_id):
    st.title(f"🧠 Take Test: {test_id}")

    init_test_session(user, test_id)
    load_questions(test_id)

    questions = st.session_state.questions
    idx = st.session_state.q_index

    if not questions:
        st.error("No questions generated")
        return

    question = questions[idx]

    # ==============================
    # ❓ DISPLAY QUESTION
    # ==============================
    st.subheader(f"Q{idx+1}: {question}")

    # Answer input
    answer = st.text_area(
        "Your Answer",
        value=st.session_state.answers.get(idx, ""),
        key=f"ans_{idx}"
    )
    st.session_state.answers[idx] = answer

    # ==============================
    # 🤖 AI ASSIST BUTTONS
    # ==============================
    col1, col2, col3 = st.columns(3)

    if col1.button("💡 Hint"):
        context = qa_chain.retrieve_context(question)
        hint = generate_hint(question, context)
        #hint = generate_hint(question)
        st.info(hint)
        st.session_state.hints[idx] = st.session_state.hints.get(idx, 0) + 1

    if col2.button("🧠 Explain"):
        explanation = generate_explanation(question)
        st.info(explanation)
        st.session_state.explains[idx] = st.session_state.explains.get(idx, 0) + 1

    if col3.button("📘 Example"):
        example = generate_example(question)
        st.info(example)
        st.session_state.examples[idx] = st.session_state.examples.get(idx, 0) + 1

    st.divider()

    # ==============================
    # 🔁 NAVIGATION
    # ==============================
    col_prev, col_next, col_submit = st.columns(3)

    if col_prev.button("⬅ Previous") and idx > 0:
        st.session_state.q_index -= 1

    if col_next.button("Next ➡") and idx < len(questions) - 1:
        st.session_state.q_index += 1

    if col_submit.button("✅ Submit Test"):
        complete_test(user, test_id)

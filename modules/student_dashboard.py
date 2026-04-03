# modules/student_dashboard.py

import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import ASSIGNMENTS_FILE, SUBMISSIONS_FILE
from modules.take_test import take_test_page
from modules.submission import submission_page
from utils.analytics import completion_rate


# ==============================
# 📊 GET TEST STATUS
# ==============================

def get_test_status(df_tests, df_submissions, usn):
    completed_tests = df_submissions[df_submissions["USN"] == usn]["Assignment_ID"].values

    status_list = []
    for _, row in df_tests.iterrows():
        test_id = row["Assignment_ID"]
        due_date = pd.to_datetime(row["Due_Date"])

        if test_id in completed_tests:
            status = "🟢 Completed"
        elif due_date < pd.Timestamp.now():
            status = "🔴 Overdue"
        else:
            status = "🟡 Pending"

        status_list.append(status)

    df_tests["Status"] = status_list
    return df_tests


# ==============================
# 📊 STUDENT ANALYTICS
# ==============================

def show_student_analytics(usn):
    df_tests = pd.read_excel(ASSIGNMENTS_FILE)
    df_sub = pd.read_excel(SUBMISSIONS_FILE)

    total_tests = len(df_tests)
    completed = len(df_sub[df_sub["USN"] == usn])
    pending = total_tests - completed

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tests", total_tests)
    col2.metric("Completed", completed)
    col3.metric("Pending", pending)

    if total_tests > 0:
        st.progress(completed / total_tests)


# ==============================
# 🎯 MAIN DASHBOARD
# ==============================

def student_dashboard(user):
    st.title("👨‍🎓 Student Dashboard")

    usn = user["USN"]

    # Load data
    df_tests = pd.read_excel(ASSIGNMENTS_FILE)
    df_sub = pd.read_excel(SUBMISSIONS_FILE)

    if df_tests.empty:
        st.info("No tests available yet")
        return

    # Add Status
    df_tests = get_test_status(df_tests, df_sub, usn)

    # ==============================
    # 📋 TEST LIST
    # ==============================
    st.subheader("📋 Available Tests")

    st.dataframe(
        df_tests[["Assignment_ID", "Subject", "Topic", "Due_Date", "Status"]],
        use_container_width=True
    )

    # ==============================
    # ⚠️ DUE ALERTS
    # ==============================
    overdue = df_tests[df_tests["Status"] == "🔴 Overdue"]

    if not overdue.empty:
        st.warning(f"⚠ {len(overdue)} tests are overdue!")

    # ==============================
    # ▶ SELECT TEST
    # ==============================
    selected_test = st.selectbox(
        "Select Test",
        df_tests["Assignment_ID"]
    )

    # ==============================
    # 🔀 MODE SELECTION
    # ==============================
    mode = st.radio(
        "Choose Mode",
        ["🧠 Take Test", "📤 Direct Upload"]
    )

    st.divider()

    # ==============================
    # 🚀 LOAD MODULE
    # ==============================
    if mode == "🧠 Take Test":
        take_test_page(user, selected_test)

    elif mode == "📤 Direct Upload":
        submission_page(user, selected_test)

    # ==============================
    # 📊 ANALYTICS
    # ==============================
    st.divider()
    st.subheader("📊 Your Analytics")

    show_student_analytics(usn)

# modules/admin_dashboard.py

import streamlit as st
import pandas as pd

from config.settings import USERS_FILE, ASSIGNMENTS_FILE, SUBMISSIONS_FILE
from database.db_manager import load_data, save_data
from modules.test_manager import add_test
from modules.student_manager import approve_students


# ==============================
# 📊 ANALYTICS FUNCTIONS
# ==============================

def student_wise_analytics(df_sub):
    st.subheader("👨‍🎓 Student-wise Submissions")

    if df_sub.empty:
        st.info("No submissions yet")
        return

    result = df_sub.groupby("USN").size().reset_index(name="Submission_Count")
    st.dataframe(result, use_container_width=True)


def test_wise_analytics(df_sub):
    st.subheader("📚 Test-wise Submissions")

    if df_sub.empty:
        st.info("No submissions yet")
        return

    result = df_sub.groupby("Assignment_ID").size().reset_index(name="Submission_Count")
    st.dataframe(result, use_container_width=True)


def topic_wise_analytics(df_sub, df_tests):
    st.subheader("🧠 Topic-wise Submissions")

    if df_sub.empty or df_tests.empty:
        st.info("No data available")
        return

    merged = df_sub.merge(df_tests, on="Assignment_ID", how="left")

    result = merged.groupby("Topic").size().reset_index(name="Submission_Count")
    st.dataframe(result, use_container_width=True)


# ==============================
# 🎯 MAIN ADMIN DASHBOARD
# ==============================

def admin_dashboard(user):
    st.title("🧑‍🏫 Admin Dashboard")

    # Load data
    df_users = load_data(USERS_FILE)
    df_tests = load_data(ASSIGNMENTS_FILE)
    df_sub = load_data(SUBMISSIONS_FILE)

    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "👥 Students",
        "📚 Tests",
        "📊 Analytics"
    ])

    # ==============================
    # 👥 STUDENT MANAGEMENT
    # ==============================
    with tab1:
        st.subheader("👥 Student Management")

        if df_users.empty:
            st.info("No users found")
        else:
            pending = df_users[df_users["Approved"] == False]

            if pending.empty:
                st.success("No pending approvals")
            else:
                st.write("Pending Approvals:")

                for idx, row in pending.iterrows():
                    col1, col2, col3 = st.columns([3, 1, 1])

                    col1.write(f"{row['Name']} ({row['USN']})")

                    if col2.button("✅ Approve", key=f"approve_{idx}"):
                        df_users.loc[idx, "Approved"] = True
                        save_data(df_users, USERS_FILE)
                        st.success(f"{row['Name']} approved")
                        st.rerun()

                    if col3.button("❌ Reject", key=f"reject_{idx}"):
                        df_users = df_users.drop(idx)
                        save_data(df_users, USERS_FILE)
                        st.warning(f"{row['Name']} rejected")
                        st.rerun()

        st.divider()
        st.subheader("📋 All Students")
        st.dataframe(df_users, use_container_width=True)

    # ==============================
    # 📚 TEST MANAGEMENT
    # ==============================
    with tab2:
        st.subheader("📚 Test Management")

        add_test()  # from test_manager.py

        st.divider()

        if df_tests.empty:
            st.info("No tests available")
        else:
            st.subheader("📋 All Tests")
            st.dataframe(df_tests, use_container_width=True)

    # ==============================
    # 📊 ANALYTICS
    # ==============================
    with tab3:
        st.subheader("📊 Analytics Dashboard")

        student_wise_analytics(df_sub)
        st.divider()

        test_wise_analytics(df_sub)
        st.divider()

        topic_wise_analytics(df_sub, df_tests)

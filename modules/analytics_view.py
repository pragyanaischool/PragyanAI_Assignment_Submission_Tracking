# modules/analytics_view.py

import streamlit as st
import pandas as pd
import plotly.express as px

from config.settings import SUBMISSIONS_FILE, ASSIGNMENTS_FILE


# ==============================
# 📊 LOAD DATA
# ==============================

def load_analytics_data():
    df_sub = pd.read_excel(SUBMISSIONS_FILE)
    df_tests = pd.read_excel(ASSIGNMENTS_FILE)
    return df_sub, df_tests


# ==============================
# 👨‍🎓 STUDENT-WISE ANALYTICS
# ==============================

def student_wise_chart(df_sub):
    st.subheader("👨‍🎓 Student-wise Submissions")

    if df_sub.empty:
        st.info("No submissions yet")
        return

    data = df_sub.groupby("USN").size().reset_index(name="Submissions")

    fig = px.bar(
        data,
        x="USN",
        y="Submissions",
        title="Submissions per Student"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# 📚 TEST-WISE ANALYTICS
# ==============================

def test_wise_chart(df_sub):
    st.subheader("📚 Test-wise Submissions")

    if df_sub.empty:
        st.info("No submissions yet")
        return

    data = df_sub.groupby("Assignment_ID").size().reset_index(name="Submissions")

    fig = px.bar(
        data,
        x="Assignment_ID",
        y="Submissions",
        title="Submissions per Test"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# 🧠 TOPIC-WISE ANALYTICS
# ==============================

def topic_wise_chart(df_sub, df_tests):
    st.subheader("🧠 Topic-wise Submissions")

    if df_sub.empty or df_tests.empty:
        st.info("No data available")
        return

    merged = df_sub.merge(df_tests, on="Assignment_ID", how="left")

    data = merged.groupby("Topic").size().reset_index(name="Submissions")

    fig = px.pie(
        data,
        names="Topic",
        values="Submissions",
        title="Topic-wise Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# 📈 KPI METRICS
# ==============================

def show_kpis(df_sub, df_tests):
    st.subheader("📊 Key Metrics")

    total_tests = len(df_tests)
    total_submissions = len(df_sub)

    unique_students = df_sub["USN"].nunique() if not df_sub.empty else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tests", total_tests)
    col2.metric("Total Submissions", total_submissions)
    col3.metric("Active Students", unique_students)


# ==============================
# 🎯 MAIN ANALYTICS VIEW
# ==============================

def analytics_dashboard():
    st.title("📊 Analytics Dashboard")

    df_sub, df_tests = load_analytics_data()

    # KPIs
    show_kpis(df_sub, df_tests)

    st.divider()

    # Charts
    student_wise_chart(df_sub)
    st.divider()

    test_wise_chart(df_sub)
    st.divider()

    topic_wise_chart(df_sub, df_tests)

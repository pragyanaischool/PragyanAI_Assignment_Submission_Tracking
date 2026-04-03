# modules/notifications.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from config.settings import ASSIGNMENTS_FILE, SUBMISSIONS_FILE


# ==============================
# 📅 DUE DATE ALERTS (STUDENT)
# ==============================

def show_due_alerts(usn):
    st.subheader("🔔 Notifications")

    df_tests = pd.read_excel(ASSIGNMENTS_FILE)
    df_sub = pd.read_excel(SUBMISSIONS_FILE)

    if df_tests.empty:
        return

    submitted_tests = df_sub[df_sub["USN"] == usn]["Assignment_ID"].values

    upcoming = []
    overdue = []

    for _, row in df_tests.iterrows():
        test_id = row["Assignment_ID"]
        due_date = pd.to_datetime(row["Due_Date"])

        if test_id in submitted_tests:
            continue

        days_left = (due_date - datetime.now()).days

        if days_left < 0:
            overdue.append(test_id)
        elif days_left <= 2:
            upcoming.append((test_id, days_left))

    # Overdue
    if overdue:
        st.error(f"⚠ Overdue Tests: {', '.join(overdue)}")

    # Upcoming
    if upcoming:
        for test_id, days in upcoming:
            st.warning(f"⏳ {test_id} due in {days} day(s)")


# ==============================
# 📊 ADMIN ALERTS
# ==============================

def admin_notifications():
    st.subheader("🔔 Admin Alerts")

    df_tests = pd.read_excel(ASSIGNMENTS_FILE)
    df_sub = pd.read_excel(SUBMISSIONS_FILE)

    if df_tests.empty:
        st.info("No tests available")
        return

    alerts = []

    for _, row in df_tests.iterrows():
        test_id = row["Assignment_ID"]
        due_date = pd.to_datetime(row["Due_Date"])

        total_students = df_sub["USN"].nunique() if not df_sub.empty else 0
        submitted = len(df_sub[df_sub["Assignment_ID"] == test_id])

        if total_students > 0:
            participation = (submitted / total_students) * 100
        else:
            participation = 0

        # Low participation alert
        if participation < 30:
            alerts.append(f"⚠ Low participation in {test_id} ({participation:.1f}%)")

        # Near due date alert
        days_left = (due_date - datetime.now()).days
        if days_left <= 1:
            alerts.append(f"⏳ {test_id} deadline approaching!")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("✅ No alerts")


# ==============================
# 📩 SIMPLE REMINDER FUNCTION
# ==============================

def get_pending_tests(usn):
    """Return list of pending tests (for future use: email/WhatsApp)"""
    df_tests = pd.read_excel(ASSIGNMENTS_FILE)
    df_sub = pd.read_excel(SUBMISSIONS_FILE)

    submitted = df_sub[df_sub["USN"] == usn]["Assignment_ID"].values

    pending = df_tests[~df_tests["Assignment_ID"].isin(submitted)]

    return pending["Assignment_ID"].tolist()

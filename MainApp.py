# app.py

import streamlit as st
import sys
# ==============================
# ⚙️ INIT SYSTEM
# ==============================
import os
from database.migrations import run_migrations
from utils.session_manager import init_session, get_user, clear_session
from ui.styles import apply_styles
from config.settings import USERS_FILE
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if not os.path.exists(USERS_FILE):
    run_migrations()
#run_migrations()
init_session()
apply_styles()

# ==============================
# 🔐 AUTH
# ==============================

from modules.auth import auth_page, logout

# ==============================
# DASHBOARDS
# ==============================

from modules.student_dashboard import student_dashboard
from modules.admin_dashboard import admin_dashboard

# ==============================
# 🔔 NOTIFICATIONS
# ==============================

from modules.notifications import show_due_alerts, admin_notifications


# ==============================
# 🎯 MAIN APP
# ==============================

def main():
    st.set_page_config(
        page_title="PragyanAI Assignment Tracker",
        layout="wide"
    )

    user = get_user()

    # ==============================
    # 🔐 LOGIN FLOW
    # ==============================
    if not user:
        user = auth_page()
        return

    # ==============================
    # 🧑‍💻 SIDEBAR
    # ==============================
    st.sidebar.title("🚀 PragyanAI")

    st.sidebar.write(f"👤 {user['Name']}")
    st.sidebar.write(f"🎭 Role: {user['Role']}")

    if st.sidebar.button("🚪 Logout"):
        clear_session()
        st.rerun()

    st.sidebar.divider()

    # ==============================
    # 🔔 NOTIFICATIONS
    # ==============================
    if user["Role"] == "student":
        show_due_alerts(user["USN"])
    else:
        admin_notifications()

    st.sidebar.divider()

    # ==============================
    # 🧭 NAVIGATION
    # ==============================
    if user["Role"] == "admin":
        menu = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Analytics"]
        )

        if menu == "Dashboard":
            admin_dashboard(user)

        elif menu == "Analytics":
            from modules.analytics_view import analytics_dashboard
            analytics_dashboard()

    # ==============================
    # 👨‍🎓 STUDENT FLOW
    # ==============================
    elif user["Role"] == "student":
        student_dashboard(user)

    else:
        st.error("Unknown role")


# ==============================
# 🚀 RUN APP
# ==============================

if __name__ == "__main__":
    main()

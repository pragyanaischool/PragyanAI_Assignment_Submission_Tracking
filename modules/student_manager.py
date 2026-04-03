# modules/student_manager.py

import streamlit as st
import pandas as pd

from config.settings import USERS_FILE
from database.db_manager import load_data, save_data


# ==============================
# 👥 APPROVE / REJECT STUDENTS
# ==============================

def approve_students():
    st.subheader("🟡 Pending Student Approvals")

    df = load_data(USERS_FILE)

    if df.empty:
        st.info("No users found")
        return

    pending = df[df["Approved"] == False]

    if pending.empty:
        st.success("No pending approvals")
        return

    for idx, row in pending.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])

        col1.write(f"{row['Name']} ({row['USN']})")

        # Approve
        if col2.button("✅ Approve", key=f"approve_{idx}"):
            df.loc[idx, "Approved"] = True
            save_data(df, USERS_FILE)
            st.success(f"{row['Name']} approved")
            st.rerun()

        # Reject
        if col3.button("❌ Reject", key=f"reject_{idx}"):
            df = df.drop(idx)
            save_data(df, USERS_FILE)
            st.warning(f"{row['Name']} rejected")
            st.rerun()


# ==============================
# 📋 VIEW ALL STUDENTS
# ==============================

def view_students():
    st.subheader("📋 All Students")

    df = load_data(USERS_FILE)

    if df.empty:
        st.info("No users available")
        return

    st.dataframe(df, use_container_width=True)


# ==============================
# 🔍 SEARCH STUDENT
# ==============================

def search_student():
    st.subheader("🔍 Search Student")

    df = load_data(USERS_FILE)

    if df.empty:
        st.info("No users available")
        return

    query = st.text_input("Search by Name / USN / Email")

    if query:
        filtered = df[
            df["Name"].str.contains(query, case=False, na=False) |
            df["USN"].str.contains(query, case=False, na=False) |
            df["Email"].str.contains(query, case=False, na=False)
        ]

        if filtered.empty:
            st.warning("No matching student found")
        else:
            st.dataframe(filtered, use_container_width=True)


# ==============================
# ❌ DELETE STUDENT
# ==============================

def delete_student():
    st.subheader("❌ Delete Student")

    df = load_data(USERS_FILE)

    if df.empty:
        st.info("No users available")
        return

    student_list = df["USN"].tolist()

    selected = st.selectbox("Select Student", student_list)

    if st.button("⚠️ Confirm Delete"):
        df = df[df["USN"] != selected]
        save_data(df, USERS_FILE)

        st.success(f"Student {selected} deleted")
        st.rerun()


# ==============================
# 🎯 MAIN STUDENT MANAGER
# ==============================

def student_manager():
    st.title("👥 Student Management")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🟡 Approvals",
        "📋 View Students",
        "🔍 Search",
        "❌ Delete"
    ])

    with tab1:
        approve_students()

    with tab2:
        view_students()

    with tab3:
        search_student()

    with tab4:
        delete_student()

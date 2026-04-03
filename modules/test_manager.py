# modules/test_manager.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

from config.settings import ASSIGNMENTS_FILE, DOCS_DIR
from database.db_manager import load_data, save_data, insert_row
from database.validators import validate_assignment


# ==============================
# 📁 SAVE TEST DOCUMENT
# ==============================

def save_test_file(file, test_id):
    if file is None:
        return None

    os.makedirs(DOCS_DIR, exist_ok=True)

    file_path = f"{DOCS_DIR}/{test_id}.pdf"

    with open(file_path, "wb") as f:
        f.write(file.read())

    return file_path


# ==============================
# ➕ ADD TEST
# ==============================

def add_test():
    st.subheader("➕ Add New Test")

    test_id = st.text_input("Test ID (Unique)")
    test_name = st.text_input("Test Name")
    subject = st.text_input("Subject")
    topic = st.text_input("Topic")
    description = st.text_area("Description")

    due_date = st.date_input("Due Date")

    uploaded_file = st.file_uploader("Upload Test Document (PDF)", type=["pdf"])

    if st.button("🚀 Create Test"):
        try:
            if not test_id:
                raise ValueError("Test ID is required")

            df = load_data(ASSIGNMENTS_FILE)

            # Check duplicate
            if not df.empty and test_id in df["Assignment_ID"].values:
                raise ValueError("Test ID already exists")

            # Save file
            file_path = save_test_file(uploaded_file, test_id)

            assignment_data = {
                "Assignment_ID": test_id,
                "Test_Name": test_name,
                "Subject": subject,
                "Topic": topic,
                "Description": description,
                "Document_Path": file_path,
                "Due_Date": str(due_date),
                "Created_By": "admin",
                "Created_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            validate_assignment(assignment_data)

            insert_row(ASSIGNMENTS_FILE, assignment_data)

            st.success("✅ Test created successfully!")

        except Exception as e:
            st.error(f"❌ {str(e)}")


# ==============================
# ✏️ EDIT TEST
# ==============================

def edit_test():
    st.subheader("✏️ Edit Test")

    df = load_data(ASSIGNMENTS_FILE)

    if df.empty:
        st.info("No tests available")
        return

    test_id = st.selectbox("Select Test", df["Assignment_ID"])

    test_data = df[df["Assignment_ID"] == test_id].iloc[0]

    test_name = st.text_input("Test Name", test_data["Test_Name"])
    subject = st.text_input("Subject", test_data["Subject"])
    topic = st.text_input("Topic", test_data["Topic"])
    description = st.text_area("Description", test_data["Description"])

    due_date = st.date_input("Due Date", pd.to_datetime(test_data["Due_Date"]))

    if st.button("💾 Update Test"):
        try:
            df.loc[df["Assignment_ID"] == test_id, [
                "Test_Name", "Subject", "Topic", "Description", "Due_Date"
            ]] = [
                test_name, subject, topic, description, str(due_date)
            ]

            save_data(df, ASSIGNMENTS_FILE)

            st.success("✅ Test updated successfully!")

        except Exception as e:
            st.error(f"❌ {str(e)}")


# ==============================
# ❌ DELETE TEST
# ==============================

def delete_test():
    st.subheader("❌ Delete Test")

    df = load_data(ASSIGNMENTS_FILE)

    if df.empty:
        st.info("No tests available")
        return

    test_id = st.selectbox("Select Test to Delete", df["Assignment_ID"])

    if st.button("⚠️ Confirm Delete"):
        try:
            df = df[df["Assignment_ID"] != test_id]
            save_data(df, ASSIGNMENTS_FILE)

            # Remove file if exists
            file_path = f"{DOCS_DIR}/{test_id}.pdf"
            if os.path.exists(file_path):
                os.remove(file_path)

            st.success("✅ Test deleted successfully!")

        except Exception as e:
            st.error(f"❌ {str(e)}")


# ==============================
# 🎯 MAIN TEST MANAGER
# ==============================

def test_manager():
    st.title("📚 Test Management")

    tab1, tab2, tab3 = st.tabs([
        "➕ Add Test",
        "✏️ Edit Test",
        "❌ Delete Test"
    ])

    with tab1:
        add_test()

    with tab2:
        edit_test()

    with tab3:
        delete_test()

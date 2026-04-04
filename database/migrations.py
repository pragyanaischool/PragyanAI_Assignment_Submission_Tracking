# database/migrations.py

import os
import pandas as pd
from datetime import datetime

from config.settings import (
    USERS_FILE,
    ASSIGNMENTS_FILE,
    SUBMISSIONS_FILE,
    TEST_SESSIONS_FILE,
    QUESTION_LOGS_FILE,
)

from database.schema import (
    USERS_SCHEMA,
    ASSIGNMENTS_SCHEMA,
    SUBMISSIONS_SCHEMA,
    TEST_SESSIONS_SCHEMA,
    QUESTION_LOGS_SCHEMA,
    empty_dataframe,
)


# ==============================
# 📁 CREATE FILE
# ==============================

def create_file(file_path, schema):
    if not os.path.exists(file_path):
        df = empty_dataframe(schema)
        df.to_excel(file_path, index=False)


# ==============================
# 👤 SAMPLE USERS
# ==============================

def seed_users():
    df = pd.read_excel(USERS_FILE)

    if not df.empty:
        return

    sample_users = [
        {
            "User_ID": "ADMIN01",
            "Name": "Admin",
            "USN": "ADMIN01",
            "Email": "admin@ai.com",
            "Password": "admin123",
            "Role": "admin",
            "Approved": True,
            "Created_At": datetime.now()
        },
        {
            "User_ID": "STU001",
            "Name": "Sateesh",
            "USN": "STU001",
            "Email": "sateesh@mail.com",
            "Password": "123456",
            "Role": "student",
            "Approved": True,
            "Created_At": datetime.now()
        },
        {
            "User_ID": "STU002",
            "Name": "Rahul",
            "USN": "STU002",
            "Email": "rahul@mail.com",
            "Password": "123456",
            "Role": "student",
            "Approved": False,
            "Created_At": datetime.now()
        }
    ]

    pd.DataFrame(sample_users).to_excel(USERS_FILE, index=False)


# ==============================
# 📚 SAMPLE ASSIGNMENTS
# ==============================

def seed_assignments():
    df = pd.read_excel(ASSIGNMENTS_FILE)

    if not df.empty:
        return

    sample_tests = [
        {
            "Assignment_ID": "ML_01",
            "Test_Name": "Machine Learning Basics",
            "Subject": "AI",
            "Topic": "Linear Regression",
            "Description": "Basic ML concepts",
            "Document_Path": "data/docs/ML_01.pdf",
            "Due_Date": "2026-04-10",
            "Created_By": "admin",
            "Created_At": datetime.now()
        },
        {
            "Assignment_ID": "DL_01",
            "Test_Name": "Deep Learning Intro",
            "Subject": "AI",
            "Topic": "Neural Networks",
            "Description": "DL basics",
            "Document_Path": "data/docs/DL_01.pdf",
            "Due_Date": "2026-04-12",
            "Created_By": "admin",
            "Created_At": datetime.now()
        }
    ]

    pd.DataFrame(sample_tests).to_excel(ASSIGNMENTS_FILE, index=False)


# ==============================
# 📤 SAMPLE SUBMISSIONS
# ==============================

def seed_submissions():
    df = pd.read_excel(SUBMISSIONS_FILE)

    if not df.empty:
        return

    sample = [
        {
            "Submission_ID": "SUB001",
            "USN": "STU001",
            "Assignment_ID": "ML_01",
            "Mode": "upload",
            "File_Path": "uploads/STU001/ML_01/file.pdf",
            "Text_Response": "",
            "Submitted_At": datetime.now(),
            "Status": "submitted"
        }
    ]

    pd.DataFrame(sample).to_excel(SUBMISSIONS_FILE, index=False)


# ==============================
# 🧠 SAMPLE TEST SESSIONS
# ==============================

def seed_sessions():
    df = pd.read_excel(TEST_SESSIONS_FILE)

    if not df.empty:
        return

    sample = [
        {
            "Session_ID": "S001",
            "USN": "STU001",
            "Assignment_ID": "ML_01",
            "Start_Time": datetime.now(),
            "End_Time": datetime.now(),
            "Total_Time": 120,
            "Completed": True
        }
    ]

    pd.DataFrame(sample).to_excel(TEST_SESSIONS_FILE, index=False)


# ==============================
# ❓ SAMPLE QUESTION LOGS
# ==============================

def seed_question_logs():
    df = pd.read_excel(QUESTION_LOGS_FILE)

    if not df.empty:
        return

    sample = [
        {
            "Session_ID": "S001",
            "Question_ID": "Q1",
            "Question_Text": "What is gradient descent?",
            "Answer": "Optimization method",
            "Time_Spent": 30,
            "Hint_Clicks": 1,
            "Explain_Clicks": 1,
            "Example_Clicks": 0,
            "Revisits": 0
        }
    ]

    pd.DataFrame(sample).to_excel(QUESTION_LOGS_FILE, index=False)


# ==============================
# 🚀 RUN ALL
# ==============================

def run_migrations():
    create_file(USERS_FILE, USERS_SCHEMA)
    create_file(ASSIGNMENTS_FILE, ASSIGNMENTS_SCHEMA)
    create_file(SUBMISSIONS_FILE, SUBMISSIONS_SCHEMA)
    create_file(TEST_SESSIONS_FILE, TEST_SESSIONS_SCHEMA)
    create_file(QUESTION_LOGS_FILE, QUESTION_LOGS_SCHEMA)

    seed_users()
    seed_assignments()
    seed_submissions()
    seed_sessions()
    seed_question_logs()

    print("✅ Database + Sample Data Ready!")


if __name__ == "__main__":
    run_migrations()

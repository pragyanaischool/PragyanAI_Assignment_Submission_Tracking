# database/schema.py

# ==============================
# 👤 USERS TABLE
# ==============================
USERS_SCHEMA = {
    "User_ID": str,
    "Name": str,
    "USN": str,
    "Email": str,
    "Password": str,
    "Role": str,
    "Approved": bool,
    "Created_At": str,
}


# ==============================
# 📚 ASSIGNMENTS TABLE
# ==============================
ASSIGNMENTS_SCHEMA = {
    "Assignment_ID": str,
    "Test_Name": str,
    "Subject": str,
    "Topic": str,
    "Description": str,
    "Document_Path": str,
    "Due_Date": str,
    "Created_By": str,
    "Created_At": str,
}


# ==============================
# 📤 SUBMISSIONS TABLE
# ==============================
SUBMISSIONS_SCHEMA = {
    "Submission_ID": str,
    "USN": str,
    "Assignment_ID": str,
    "Mode": str,                 # test / upload
    "File_Path": str,
    "Text_Response": str,
    "Submitted_At": str,
    "Status": str,               # submitted / late
}


# ==============================
# 🧠 TEST SESSIONS TABLE
# ==============================
TEST_SESSIONS_SCHEMA = {
    "Session_ID": str,
    "USN": str,
    "Assignment_ID": str,
    "Start_Time": str,
    "End_Time": str,
    "Total_Time": float,
    "Completed": bool,
}


# ==============================
# ❓ QUESTION LOGS TABLE
# ==============================
QUESTION_LOGS_SCHEMA = {
    "Session_ID": str,
    "Question_ID": str,
    "Question_Text": str,
    "Answer": str,
    "Time_Spent": float,
    "Hint_Clicks": int,
    "Explain_Clicks": int,
    "Example_Clicks": int,
    "Revisits": int,
}


# ==============================
# 📊 HELPER FUNCTIONS
# ==============================

def get_columns(schema: dict):
    """Return column names"""
    return list(schema.keys())


def empty_dataframe(schema: dict):
    """Create empty DataFrame with schema"""
    import pandas as pd
    return pd.DataFrame(columns=get_columns(schema))

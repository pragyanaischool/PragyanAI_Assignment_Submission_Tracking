# database/validators.py

import re


# ==============================
# 👤 USER VALIDATIONS
# ==============================

def validate_user_data(data: dict):
    required_fields = ["User_ID", "Name", "USN", "Email", "Password", "Role"]

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"{field} is required")

    if not is_valid_email(data["Email"]):
        raise ValueError("Invalid email format")

    if not is_strong_password(data["Password"]):
        raise ValueError("Password must be at least 6 characters")

    if not is_valid_usn(data["USN"]):
        raise ValueError("Invalid USN format")


# ==============================
# 📧 EMAIL VALIDATION
# ==============================

def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# ==============================
# 🔐 PASSWORD VALIDATION
# ==============================

def is_strong_password(password: str) -> bool:
    return len(password) >= 6


# ==============================
# 🆔 USN VALIDATION
# ==============================

def is_valid_usn(usn: str) -> bool:
    """
    Example: 1RV21CS001
    Adjust regex as needed
    """
    pattern = r"^[A-Za-z0-9]{5,15}$"
    return re.match(pattern, usn) is not None


# ==============================
# 📚 ASSIGNMENT VALIDATION
# ==============================

def validate_assignment(data: dict):
    required_fields = ["Assignment_ID", "Test_Name", "Subject", "Topic", "Due_Date"]

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"{field} is required")


# ==============================
# 📤 SUBMISSION VALIDATION
# ==============================

def validate_submission(data: dict):
    required_fields = ["USN", "Assignment_ID", "Mode"]

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"{field} is required")

    if data.get("Mode") not in ["test", "upload"]:
        raise ValueError("Invalid submission mode")


# ==============================
# 📁 FILE VALIDATION
# ==============================

def validate_file(file_name: str, allowed_types: list):
    if "." not in file_name:
        raise ValueError("Invalid file name")

    ext = file_name.split(".")[-1].lower()

    if ext not in allowed_types:
        raise ValueError(f"File type .{ext} not allowed")


# ==============================
# 🚫 DUPLICATE CHECKS
# ==============================

def check_duplicate(df, column, value):
    if value in df[column].values:
        raise ValueError(f"{column} '{value}' already exists")

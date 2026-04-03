# modules/auth.py

import streamlit as st
import hashlib
from datetime import datetime

from database.db_manager import load_data, insert_row
from database.validators import validate_user_data
from config.settings import USERS_FILE
from config.roles import Roles


# ==============================
# 🔐 PASSWORD HASHING
# ==============================

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ==============================
# 👤 REGISTER USER
# ==============================

def register_user():
    st.subheader("📝 Register")

    name = st.text_input("Full Name")
    usn = st.text_input("USN")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        user_data = {
            "User_ID": usn,
            "Name": name,
            "USN": usn,
            "Email": email,
            "Password": hash_password(password),
            "Role": Roles.STUDENT,
            "Approved": False,
            "Created_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        try:
            validate_user_data(user_data)
            insert_row(USERS_FILE, user_data)
            st.success("Registered successfully! Wait for admin approval.")
        except Exception as e:
            st.error(str(e))


# ==============================
# 🔑 LOGIN USER
# ==============================

def login_user():
    st.subheader("🔐 Login")

    usn = st.text_input("User ID / USN")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        df = load_data(USERS_FILE)

        if df.empty:
            st.error("No users found")
            return None

        user = df[df["User_ID"] == usn]

        if user.empty:
            st.error("User not found")
            return None

        user = user.iloc[0]

        if user["Password"] != hash_password(password):
            st.error("Invalid password")
            return None

        if not user["Approved"]:
            st.warning("Waiting for admin approval")
            return None

        st.session_state["user"] = user.to_dict()
        st.success(f"Welcome {user['Name']}")

        return user.to_dict()

    return None


# ==============================
# 🔄 AUTH FLOW CONTROLLER
# ==============================

def auth_page():
    st.title("🔐 PragyanAI Login System")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        user = login_user()
        if user:
            return user

    with tab2:
        register_user()

    return None


# ==============================
# 🔓 LOGOUT
# ==============================

def logout():
    if st.button("Logout"):
        st.session_state.pop("user", None)
        st.rerun()

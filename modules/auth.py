# modules/auth.py

import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

from config.settings import USERS_FILE
from database.db_manager import load_data, insert_row


# ==============================
# 🔐 PASSWORD HASHING
# ==============================

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ==============================
# 🔑 LOGIN USER
# ==============================

def login_user():
    st.subheader("🔐 Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn"):

        # 🔥 HARDCODED ADMIN (GUARANTEED LOGIN)
        if email == "admin@ai.com" and password == "admin123":
            user_data = {
                "User_ID": "ADMIN01",
                "Name": "Admin",
                "USN": "ADMIN01",
                "Email": "admin@ai.com",
                "Role": "admin",
                "Approved": True
            }

            st.session_state.user = user_data
            st.success("✅ Admin login successful!")
            st.rerun()
            return

        # ==============================
        # NORMAL DB LOGIN
        # ==============================
        df = load_data(USERS_FILE)

        if df.empty:
            st.error("No users found")
            return

        # 🔥 DEBUG (temporary)
        st.write("DEBUG USERS:", df)

        user = df[
            (df["Email"] == email) &
            (
                (df["Password"] == password)  # plain
            )
        ]

        if not user.empty:
            user_data = user.iloc[0].to_dict()

            if not user_data.get("Approved", False):
                st.warning("⏳ Not approved")
                return

            st.session_state.user = user_data
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid email or password")
            
# ==============================
# 📝 REGISTER USER
# ==============================

def register_user():
    st.subheader("📝 Register")

    name = st.text_input("Name", key="register_name")
    usn = st.text_input("USN", key="register_usn")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register", key="register_btn"):
        if not name or not usn or not email or not password:
            st.warning("⚠️ Please fill all fields")
            return

        df = load_data(USERS_FILE)

        # Check duplicate email or USN
        if not df.empty:
            if email in df["Email"].values:
                st.error("Email already exists")
                return
            if usn in df["USN"].values:
                st.error("USN already exists")
                return

        user_data = {
            "User_ID": usn,
            "Name": name,
            "USN": usn,
            "Email": email,
            "Password": hash_password(password),
            "Role": "student",
            "Approved": False,
            "Created_At": datetime.now()
        }

        insert_row(USERS_FILE, user_data)

        st.success("✅ Registration successful! Await admin approval.")


# ==============================
# 🔄 AUTH PAGE
# ==============================

def auth_page():
    st.title("🎓 PragyanAI Login System")

    menu = st.radio(
        "Choose Option",
        ["Login", "Register"],
        key="auth_menu"
    )

    if menu == "Login":
        login_user()
    else:
        register_user()

    return st.session_state.get("user")


# ==============================
# 🚪 LOGOUT
# ==============================

def logout():
    if st.button("Logout", key="logout_btn"):
        st.session_state.clear()
        st.rerun()
        

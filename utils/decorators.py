# utils/decorators.py

import streamlit as st
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in st.session_state or st.session_state.user is None:
            st.warning("Please login first")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = st.session_state.get("user")

            if not user or user.get("role") != role:
                st.error("Access denied")
                st.stop()

            return func(*args, **kwargs)
        return wrapper
    return decorator

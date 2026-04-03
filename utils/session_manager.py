# utils/session_manager.py

import streamlit as st


def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None


def set_user(user):
    st.session_state.user = user


def get_user():
    return st.session_state.get("user")


def clear_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

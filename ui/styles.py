# ui/styles.py

import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
        /* Main background */
        body {
            background-color: #f9fafb;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 8px;
            background-color: #4CAF50;
            color: white;
            padding: 8px 16px;
        }

        /* Input fields */
        .stTextInput>div>div>input {
            border-radius: 8px;
        }

        /* Cards */
        .card {
            padding: 15px;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

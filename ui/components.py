# ui/components.py

import streamlit as st


# ==============================
# 📊 METRIC CARD
# ==============================

def metric_card(title, value):
    st.metric(label=title, value=value)


# ==============================
# 📦 INFO CARD
# ==============================

def info_card(title, content):
    st.markdown(f"""
    <div style="
        padding:15px;
        border-radius:10px;
        background-color:#f5f5f5;
        margin-bottom:10px;">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# ⚠️ ALERT BOX
# ==============================

def alert_box(message, type="info"):
    if type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)
    else:
        st.info(message)


# ==============================
# 🔘 SECTION HEADER
# ==============================

def section_header(title):
    st.markdown(f"### {title}")
    st.divider()

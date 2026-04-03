# ui/charts.py

import plotly.express as px
import streamlit as st


# ==============================
# 📊 BAR CHART
# ==============================

def bar_chart(data, x, y, title):
    fig = px.bar(data, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)


# ==============================
# 🥧 PIE CHART
# ==============================

def pie_chart(data, names, values, title):
    fig = px.pie(data, names=names, values=values, title=title)
    st.plotly_chart(fig, use_container_width=True)


# ==============================
# 📈 LINE CHART
# ==============================

def line_chart(data, x, y, title):
    fig = px.line(data, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)

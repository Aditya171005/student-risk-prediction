import streamlit as st
import pandas as pd
from utils import load_history

st.set_page_config(layout="wide", page_title="Dashboard", initial_sidebar_state="collapsed")

# ================= CSS =================
st.markdown("""
<style>

/* REMOVE SIDEBAR */
section[data-testid="stSidebar"] {display: none !important;}
button[kind="header"] {display: none !important;}
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
    color: white;
}

/* NAVBAR */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.title {
    font-size: 2rem;
    font-weight: 700;
    color: #e2e8f0;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    transition: 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(99,102,241,0.4);
}

/* CARD */
.card {
    background: rgba(15, 23, 42, 0.7);
    padding: 1.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ================= NAVBAR =================
col1, col2 = st.columns([6,1])

with col1:
    st.markdown('<div class="title">📊 Dashboard</div>', unsafe_allow_html=True)

with col2:
    if st.button("🏠 Home"):
        st.switch_page("app.py")

# ================= LOAD DATA =================
df = load_history()

if df is None or df.empty:
    st.warning("No data yet. Go back and run predictions.")
else:
    st.markdown("### 📋 Prediction History")
    st.dataframe(df, use_container_width=True)

    # ================= CHARTS =================
    st.markdown("### 📈 Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Risk Distribution")
        st.bar_chart(df["risk"].value_counts())

    with col2:
        st.markdown("#### Failures vs Probability")
        st.line_chart(df[["failures", "prob"]])

    # ================= SUMMARY =================
    st.markdown("### 📊 Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Records", len(df))

    with c2:
        st.metric("High Risk Count", (df["risk"] == "High").sum())

    with c3:
        st.metric("Avg Probability", f"{int(df['prob'].mean())}%")
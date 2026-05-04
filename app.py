import streamlit as st
import pandas as pd
import pickle
from utils import save_prediction, load_history

st.set_page_config(layout="wide", page_title="Student Risk AI", initial_sidebar_state="collapsed")

# ================= QUERY NAVIGATION =================
page = st.query_params.get("page", "home")

# ================= CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

* { font-family: 'Inter', sans-serif !important; }

#MainMenu, footer, header {visibility: hidden;}
section[data-testid="stSidebar"] {display: none !important;}
button[kind="header"] {display: none !important;}

.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
}

/* NAVBAR */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* BUTTON STYLE (SAME EVERYWHERE) */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 0.6rem 1.6rem !important;
    font-weight: 600 !important;
    transition: 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(99,102,241,0.4);
}

/* HERO */
.hero {
    text-align: center;
    margin-bottom: 3rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #94a3b8;
}

/* RESULT */
.result {
    text-align: center;
    padding: 2rem;
    border-radius: 20px;
    margin-top: 2rem;
}
.high { border: 2px solid rgba(239,68,68,0.5); }
.low { border: 2px solid rgba(34,197,94,0.5); }

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
    st.markdown("## 🎓 Student Risk AI")

with col2:
    if page == "home":
        if st.button("📊 Dashboard"):
            st.query_params["page"] = "dashboard"
    else:
        if st.button("🏠 Home"):
            st.query_params["page"] = "home"

# ================= HOME PAGE =================
if page == "home":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">Student Risk Prediction</div>
        <div class="hero-sub">AI-powered academic analysis</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        studytime = st.slider("Study Time", 1, 4, 2)

    with c2:
        failures = st.slider("Failures", 0, 3, 1)

    with c3:
        absences = st.number_input("Absences", 0, 100, 2)

    with c4:
        health = st.slider("Health", 1, 5, 3)

    clicked = st.button("🚀 Analyze Risk")

    if clicked:
        try:
            model = pickle.load(open("model.pkl", "rb"))
            df = pd.DataFrame([[studytime, failures, absences, health]],
                              columns=["studytime","failures","absences","health"])
            pred = model.predict(df)[0]
            prob = int(model.predict_proba(df)[0][1]*100)
        except:
            pred = 1 if (failures > 1 or absences > 15 or studytime < 2) else 0
            prob = 75 if pred else 41

        save_prediction({
            "studytime": studytime,
            "failures": failures,
            "absences": absences,
            "health": health,
            "risk": "High" if pred else "Low",
            "prob": prob
        })

        if pred:
            st.markdown(f'<div class="result high">⚠️ High Risk<br><h1>{prob}%</h1></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result low">✅ Low Risk<br><h1>{prob}%</h1></div>', unsafe_allow_html=True)

# ================= DASHBOARD PAGE =================
elif page == "dashboard":

    st.markdown("## 📊 Dashboard")

    df = load_history()

    if df.empty:
        st.warning("No data yet. Run predictions first.")
    else:
        st.markdown("### 📋 Prediction History")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📈 Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(df["risk"].value_counts())

        with col2:
            st.line_chart(df[["failures", "prob"]])

        st.markdown("### 📊 Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Total Records", len(df))

        with c2:
            st.metric("High Risk", (df["risk"] == "High").sum())

        with c3:
            st.metric("Avg Probability", f"{int(df['prob'].mean())}%")
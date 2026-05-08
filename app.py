import streamlit as st
import pandas as pd
import pickle
import os
import time
from logic import get_insights
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(layout="wide", page_title="Student Risk AI", initial_sidebar_state="collapsed")

FILE = "history.csv"
USER_FILE = "users.csv"

# ---------- MODEL ----------
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except:
        return None

model = load_model()

# ---------- USER ----------
def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    return pd.DataFrame(columns=["username","password"])

def save_user(username, password):
    username = username.strip().lower()
    password = password.strip()
    df = load_users()
    df["username"] = df["username"].astype(str).str.strip().str.lower()
    if username in df["username"].values:
        return False
    df = pd.concat([df, pd.DataFrame([[username,password]], columns=["username","password"])])
    df.to_csv(USER_FILE, index=False)
    return True

def authenticate(username, password):
    df = load_users()
    username = username.strip().lower()
    password = password.strip()
    df["username"] = df["username"].astype(str).str.strip().str.lower()
    df["password"] = df["password"].astype(str).str.strip()
    return ((df["username"] == username) & (df["password"] == password)).any()

# ---------- STORAGE ----------
def save_prediction(entry):
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df = pd.concat([df, pd.DataFrame([entry])])
    else:
        df = pd.DataFrame([entry])
    df.to_csv(FILE, index=False)

def load_history():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame()

# ---------- INSIGHTS ----------
def safe_insights(studytime, failures, absences, health):
    try:
        reasons, tips = get_insights(studytime, failures, absences, health)
    except:
        reasons, tips = [], []

    if not reasons:
        reasons = ["Study consistency affected prediction","Attendance impacted result","Past failures contributed"]

    if not tips:
        tips = ["Increase study time","Reduce absences","Focus on weak subjects"]

    return reasons, tips

def simple_explain(studytime, failures, absences, health):
    factors = []
    if failures > 1: factors.append("High failures")
    if absences > 15: factors.append("High absences")
    if studytime < 2: factors.append("Low study time")
    if health < 3: factors.append("Poor health")
    if not factors: factors = ["Balanced performance"]
    return factors

# ---------- PDF ----------
def generate_pdf(entry, reasons, tips):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    c.setFont("Helvetica", 12)

    c.drawString(50, y, "STUDENT RISK REPORT")
    y -= 40

    for k, v in entry.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 20

    y -= 20
    c.drawString(50, y, "Reasons:")
    y -= 20
    for r in reasons:
        c.drawString(60, y, f"- {r}")
        y -= 15

    y -= 10
    c.drawString(50, y, "Recommendations:")
    y -= 20
    for t in tips:
        c.drawString(60, y, f"- {t}")
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

# ---------- STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- UI ----------
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.stApp {background:#0b0f19; color:white;}

.stButton > button {
    background:#22c55e !important;
    color:#0b0f19 !important;
    border-radius:10px !important;
    font-weight:600 !important;
    padding:10px 18px !important;
}

.nav-btn button {
    width:120px !important;
    white-space:nowrap !important;
}

.card {
    padding:25px;
    border-radius:20px;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
}

.section {
    padding:20px;
    border-radius:15px;
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.06);
    margin-bottom:15px;
}

.result-box {
    text-align:center;
    padding:50px;
    border-radius:25px;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    font-size:70px;
    font-weight:800;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if st.session_state.page == "login":
    st.title("🔐 Student Risk AI")

    tab1, tab2 = st.tabs(["Login","Signup"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(u,p):
                st.session_state.user = u
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if save_user(u,p):
                st.success("Account created")
            else:
                st.error("Username exists")

# ================= NAV =================
elif st.session_state.page in ["home","dashboard"]:

    c1,c2,c3 = st.columns([8,1,1])

    with c1:
        st.write(f"👋 {st.session_state.user}")

    with c2:
        if st.session_state.page=="home":
            if st.button("Dashboard", key="dash", help="Go to dashboard"):
                st.session_state.page="dashboard"
                st.rerun()

    with c3:
        if st.session_state.page=="dashboard":
            if st.button("Home", key="home"):
                st.session_state.page="home"
                st.rerun()

# ================= HOME =================
if st.session_state.page=="home":

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        studytime = st.slider("Study Time",1,4,2)
    with c2:
        failures = st.slider("Failures",0,3,1)
    with c3:
        absences = st.number_input("Absences",0,100,2)
    with c4:
        health = st.slider("Health",1,5,2)

    if st.button("🚀 Analyze Risk"):

        with st.spinner("Analyzing..."):
            time.sleep(0.4)

            if model:
                df = pd.DataFrame([[studytime,failures,absences,health]],
                                  columns=["studytime","failures","absences","health"])
                pred = model.predict(df)[0]
                prob = int(model.predict_proba(df)[0][1]*100)
            else:
                pred = 1 if (failures>1 or absences>15 or studytime<2) else 0
                prob = 75 if pred else 41

        entry = {
            "user":st.session_state.user,
            "studytime":studytime,
            "failures":failures,
            "absences":absences,
            "health":health,
            "risk":"High" if pred else "Low",
            "prob":prob
        }

        save_prediction(entry)

        st.markdown(f'<div class="result-box">{"🟢" if pred==0 else "🔴"} {prob}%</div>', unsafe_allow_html=True)

        reasons, tips = safe_insights(studytime, failures, absences, health)
        explain = simple_explain(studytime, failures, absences, health)

        st.markdown("### 🧠 Key Factors")
        st.markdown('<div class="section">' + "<br>".join([f"• {f}" for f in explain]) + '</div>', unsafe_allow_html=True)

        st.markdown("### 🧠 Why")
        st.markdown('<div class="section">' + "<br>".join([f"• {r}" for r in reasons]) + '</div>', unsafe_allow_html=True)

        st.markdown("### 🎯 Recommendations")
        st.markdown('<div class="section">' + "<br>".join([f"• {t}" for t in tips]) + '</div>', unsafe_allow_html=True)

        st.download_button("⬇ CSV", pd.DataFrame([entry]).to_csv(index=False), "report.csv")
        st.download_button("⬇ PDF", generate_pdf(entry, reasons, tips), "report.pdf")

# ================= DASHBOARD =================
if st.session_state.page=="dashboard":

    st.title("📊 Dashboard")
    df = load_history()

    if df.empty:
        st.warning("No data yet")

    else:
        df = df[df["user"]==st.session_state.user]

        st.markdown("<br>", unsafe_allow_html=True)

        c1,c2,c3 = st.columns(3)

        with c1:
            st.markdown(f'<div class="card"><h2>{len(df)}</h2><p>Total Predictions</p></div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f'<div class="card"><h2>{len(df[df["risk"]=="High"])}</h2><p>High Risk</p></div>', unsafe_allow_html=True)

        with c3:
            st.markdown(f'<div class="card"><h2>{int(df["prob"].mean())}%</h2><p>Avg Risk</p></div>', unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)
        st.bar_chart(df["risk"].value_counts())
        st.line_chart(df["prob"])

        st.download_button("⬇ Download Data", df.to_csv(index=False), "history.csv")
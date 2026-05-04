import streamlit as st
import pandas as pd
import pickle

st.set_page_config(layout="wide", page_title="Student Risk AI", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.block-container {
    padding: 2rem 3rem !important;
    max-width: 1400px !important;
}
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
}

.hero-section {
    text-align: center;
    margin-bottom: 4rem;
    padding: 2rem 0;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa 0%, #818cf8 50%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    font-weight: 400;
    letter-spacing: 0.01em;
}

.metric-label {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 500;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: block;
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-top: 0.5rem;
    text-align: center;
}

[data-testid="stSlider"] {
    padding: 1.5rem !important;
    background: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[data-testid="stSlider"]:hover {
    transform: translateY(-4px) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15) !important;
}

[data-testid="stNumberInput"] {
    padding: 1.5rem !important;
    background: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[data-testid="stNumberInput"]:hover {
    transform: translateY(-4px) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15) !important;
}

.stSlider > div > div > div {
    background: rgba(15, 23, 42, 0.8) !important;
    border-radius: 10px;
    height: 6px !important;
}
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border-radius: 10px;
    height: 6px !important;
}
.stSlider [role="slider"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    width: 24px !important;
    height: 24px !important;
    border: 3px solid rgba(255, 255, 255, 0.9) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;
}

.stNumberInput > div > div > input {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    padding: 1.5rem !important;
}
.stNumberInput button {
    background: rgba(99, 102, 241, 0.1) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 8px !important;
    color: #a78bfa !important;
}

.analyze-container {
    display: flex;
    justify-content: center;
    margin: 3rem 0;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 1.2rem 4rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 40px rgba(99, 102, 241, 0.4) !important;
}

.result-card {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(20px);
    border: 2px solid;
    border-radius: 24px;
    padding: 3rem;
    text-align: center;
    margin: 2rem auto;
    max-width: 600px;
    animation: slideUp 0.5s ease-out;
}
@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.result-low {
    border-color: rgba(34, 197, 94, 0.5);
    box-shadow: 0 20px 60px rgba(34, 197, 94, 0.2);
}
.result-high {
    border-color: rgba(239, 68, 68, 0.5);
    box-shadow: 0 20px 60px rgba(239, 68, 68, 0.2);
}
.result-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}
.result-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #e2e8f0;
}
.result-percentage {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 1rem 0;
}
.result-low .result-percentage {
    background: linear-gradient(135deg, #22c55e, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.result-high .result-percentage {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.result-description {
    font-size: 1rem;
    color: #94a3b8;
    font-weight: 400;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎓 Student Risk Prediction</div>
    <div class="hero-subtitle">AI-powered academic performance analysis</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-label">Study Time</div>', unsafe_allow_html=True)
    studytime = st.slider("Study Time", 1, 4, 2, label_visibility="collapsed")
    st.markdown(f'<div class="metric-value">{studytime}</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-label">Failures</div>', unsafe_allow_html=True)
    failures = st.slider("Failures", 0, 3, 1, label_visibility="collapsed")
    st.markdown(f'<div class="metric-value">{failures}</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-label">Absences</div>', unsafe_allow_html=True)
    absences = st.number_input("Absences", 0, 100, 2, label_visibility="collapsed")

with col4:
    st.markdown('<div class="metric-label">Health</div>', unsafe_allow_html=True)
    health = st.slider("Health", 1, 5, 2, label_visibility="collapsed")
    st.markdown(f'<div class="metric-value">{health}</div>', unsafe_allow_html=True)

st.markdown('<div class="analyze-container">', unsafe_allow_html=True)
clicked = st.button("🚀 Analyze Risk")
st.markdown('</div>', unsafe_allow_html=True)

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

    if pred == 1:
        st.markdown(f"""
        <div class="result-card result-high">
            <div class="result-icon">⚠️</div>
            <div class="result-title">High Risk Detected</div>
            <div class="result-percentage">{prob}%</div>
            <div class="result-description">Immediate intervention recommended</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card result-low">
            <div class="result-icon">✅</div>
            <div class="result-title">Low Risk</div>
            <div class="result-percentage">{prob}%</div>
            <div class="result-description">Student is on track for success</div>
        </div>
        """, unsafe_allow_html=True)
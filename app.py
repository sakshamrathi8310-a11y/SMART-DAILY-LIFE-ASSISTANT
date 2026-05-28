import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from model import load_models
from database import init_db, insert_data, load_data
from llm_helper import get_ai_suggestion   # 🔥 IMPORTANT

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(layout="wide")
st.title("🚀 Smart Life AI")

# Init DB
init_db()

# Load ML Models
stress_model, prod_model, health_model = load_models()

# -----------------------
# INPUT SECTION
# -----------------------
st.header("Enter Daily Data")

col1, col2, col3 = st.columns(3)

with col1:
    sleep = st.slider("Sleep Hours", 0, 12, 6)
    steps = st.slider("Steps", 0, 15000, 4000)

with col2:
    screen = st.slider("Screen Time", 0, 12, 6)
    work = st.slider("Work Hours", 0, 12, 5)

with col3:
    mood = st.slider("Mood (1-5)", 1, 5, 3)
    food = st.slider("Food Quality (1-5)", 1, 5, 3)

# -----------------------
# ANALYZE BUTTON
# -----------------------
if st.button("Analyze"):

    input_df = pd.DataFrame([{
        'sleep': sleep,
        'screen_time': screen,
        'steps': steps,
        'work_hours': work,
        'mood': mood,
        'food': food,
        'sleep_eff': sleep / 8,
        'activity': steps / 10000
    }])

    # Predictions
    stress = int(stress_model.predict(input_df)[0])
    prod = int(prod_model.predict(input_df)[0])
    health = int(health_model.predict(input_df)[0])

    # -----------------------
    # RESULTS
    # -----------------------
    st.subheader("📊 Results")

    c1, c2, c3 = st.columns(3)
    c1.metric("Productivity", prod)
    c2.metric("Health", health)
    c3.metric("Stress", "High" if stress else "Low")

    # -----------------------
    # SAVE TO DATABASE
    # -----------------------
    insert_data([
        float(sleep),
        float(screen),
        float(steps),
        float(work),
        float(mood),
        float(food),
        int(stress),
        float(prod),
        float(health)
    ])

    # -----------------------
    # 🔥 AI SUGGESTIONS (STRICT API)
    # -----------------------
    st.subheader("🤖 AI Suggestions")

    try:
        ai = get_ai_suggestion(input_df.iloc[0], stress, prod, health)
        st.write(ai)

    except Exception as e:
        st.error(f"API ERROR: {e}")

# -----------------------
# HISTORY + GRAPHS
# -----------------------
st.header("📈 History Dashboard")

data = load_data()

if not data.empty:

    # CLEAN DATA
    numeric_cols = [
        "sleep","screen_time","steps","work_hours",
        "mood","food","stress","productivity","health"
    ]

    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna().reset_index()

    st.write(f"Total Records: {len(data)}")

    # -----------------------
    # PRODUCTIVITY GRAPH
    # -----------------------
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=data["index"],
        y=data["productivity"],
        mode='lines+markers',
        name="Productivity"
    ))

    fig1.update_layout(
        title="Productivity Trend",
        xaxis_title="Days",
        yaxis_title="Score"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # -----------------------
    # HEALTH GRAPH
    # -----------------------
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=data["index"],
        y=data["health"],
        mode='lines+markers',
        name="Health"
    ))

    fig2.update_layout(
        title="Health Trend",
        xaxis_title="Days",
        yaxis_title="Score"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------
    # STRESS GRAPH
    # -----------------------
    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x=data["index"],
        y=data["stress"],
        mode='lines+markers',
        name="Stress (0=Low,1=High)"
    ))

    fig3.update_layout(
        title="Stress Trend",
        xaxis_title="Days",
        yaxis_title="Level"
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("No data yet. Click Analyze to generate history.")

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CampusFlow AI",
    page_icon="🏫",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #111936 50%, #0b1020 100%);
    color: white;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    color: #aeb8d0;
    font-size: 18px;
    margin-top: 5px;
}

.card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.metric-title {
    color: #aeb8d0;
    font-size: 14px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
}

.ai-box {
    background: rgba(80,120,255,0.12);
    border: 1px solid rgba(100,140,255,0.35);
    border-radius: 18px;
    padding: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🏫 CampusFlow AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Predictive Intelligence for Smarter Campus Operations</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("🎛️ Campus Controls")

    location = st.selectbox(
        "📍 Campus Location",
        [
            "Canteen A",
            "Canteen B",
            "Main Block",
            "Library",
            "Bus Stand"
        ]
    )

    hour = st.slider(
        "🕐 Current Hour",
        8,
        18,
        13
    )

    day = st.selectbox(
        "📅 Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )

    current_count = st.number_input(
        "👥 Current Students",
        min_value=0,
        max_value=1000,
        value=180
    )

    previous_count = st.number_input(
        "👥 Previous Crowd",
        min_value=0,
        max_value=1000,
        value=170
    )

    event = st.selectbox(
        "🎉 Campus Event",
        ["No", "Yes"]
    )

    predict = st.button(
        "🔮 PREDICT CROWD",
        use_container_width=True
    )

# ---------------- DEFAULT VALUES ----------------
prediction = 0
risk = "WAITING"
recommendation = "Enter campus information and run the prediction."

# ---------------- PREDICTION ----------------
if predict:

    day_number = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ].index(day)

    event_number = 1 if event == "Yes" else 0

    input_data = pd.DataFrame({
        "hour": [hour],
        "day": [day_number],
        "current_count": [current_count],
        "event": [event_number],
        "previous_count": [previous_count]
    })

    prediction = round(model.predict(input_data)[0])

    if prediction < 150:
        risk = "LOW"
        recommendation = "Normal campus operation. No immediate action required."
    elif prediction < 300:
        risk = "MEDIUM"
        recommendation = "Monitor crowd movement and prepare staff if required."
    elif prediction < 400:
        risk = "HIGH"
        recommendation = "Open an additional counter and increase staff monitoring."
    else:
        risk = "CRITICAL"
        recommendation = (
            "Open an additional counter and redirect students "
            "to another available location."
        )

# ---------------- TOP METRICS ----------------
st.markdown(
    '<div class="section-title">📊 Campus Operations Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">📍 LOCATION</div>
        <div class="metric-value">{location}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">👥 CURRENT CROWD</div>
        <div class="metric-value">{current_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">🔮 PREDICTED CROWD</div>
        <div class="metric-value">{prediction if prediction else "--"}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    risk_icon = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🟠",
        "CRITICAL": "🔴",
        "WAITING": "⚪"
    }.get(risk, "⚪")

    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">⚠️ RISK LEVEL</div>
        <div class="metric-value">{risk_icon} {risk}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- MAIN DASHBOARD ----------------
left, right = st.columns([1.4, 1])

with left:

    st.markdown(
        '<div class="section-title">📈 Crowd Prediction Analytics</div>',
        unsafe_allow_html=True
    )

    if prediction:

        hours = [
            hour - 2,
            hour - 1,
            hour,
            hour + 1,
            hour + 2
        ]

        values = [
            max(0, previous_count - 30),
            previous_count,
            current_count,
            round(prediction * 0.90),
            round(prediction * 0.95)
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hours,
                y=values,
                mode="lines+markers",
                name="Crowd",
                line=dict(width=4)
            )
        )

        fig.add_hline(
            y=300,
            line_dash="dash",
            annotation_text="High Risk Threshold"
        )

        fig.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            xaxis_title="Hour",
            yaxis_title="Students",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "🔮 Run a prediction to display crowd analytics."
        )

with right:

    st.markdown(
        '<div class="section-title">🤖 AI Decision Center</div>',
        unsafe_allow_html=True
    )

    if prediction:

        if risk == "LOW":
            st.success("🟢 LOW RISK")

        elif risk == "MEDIUM":
            st.warning("🟡 MEDIUM RISK")

        elif risk == "HIGH":
            st.warning("🟠 HIGH RISK")

        else:
            st.error("🔴 CRITICAL RISK")

        st.markdown(
            f"""
            <div class="ai-box">
            <h3>💡 Recommended Action</h3>
            <p style="font-size:17px;">
            {recommendation}
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "AI recommendations will appear here after prediction."
        )

# ---------------- BOTTOM ----------------
st.divider()

st.markdown(
    '<div class="section-title">🧠 How CampusFlow AI Helps</div>',
    unsafe_allow_html=True
)

b1, b2, b3 = st.columns(3)

with b1:
    st.markdown(
        """
        <div class="card">
        <h3>🔮 Predict</h3>
        <p>
        Forecasts upcoming campus crowd levels
        using machine learning.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with b2:
    st.markdown(
        """
        <div class="card">
        <h3>⚠️ Detect Risk</h3>
        <p>
        Identifies LOW, MEDIUM, HIGH and
        CRITICAL congestion levels.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with b3:
    st.markdown(
        """
        <div class="card">
        <h3>🤖 Recommend</h3>
        <p>
        Suggests operational actions before
        congestion becomes a problem.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.caption(
    "CampusFlow AI • Predict Before Problems Happen"
)


import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="CampusFlow AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOAD MODEL
# =========================

model = joblib.load("model.pkl")

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #07111f, #101d35, #172554);
    color: white;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #172554);
}

.hero {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg, #172554, #312e81);
    border: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
    opacity: 0.85;
}

.card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    min-height: 130px;
}

.card-title {
    font-size: 14px;
    opacity: 0.75;
}

.card-value {
    font-size: 30px;
    font-weight: bold;
    margin-top: 8px;
}

.student-box {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0f766e, #164e63);
    border: 1px solid rgba(255,255,255,0.2);
}

.info-box {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.08);
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("## 🏫 CampusFlow AI")

    st.caption("Predictive Intelligence for Smarter Campus Operations")

    st.divider()

    page = st.radio(
        "Select View",
        [
            "👨‍💼 Admin Dashboard",
            "🎓 Student View"
        ]
    )

    st.divider()

    st.markdown("### 📍 Campus Locations")

    st.caption("Canteen • Library • Main Block")
    st.caption("Bus Stand • Student Services")

    st.divider()

    st.success("🟢 AI System Online")

# =========================
# HERO
# =========================

st.markdown("""
<div class="hero">
    <h1>🏫 CampusFlow AI</h1>
    <p>Predictive Intelligence for Smarter Campus Operations</p>
    <small>
    Predict crowd congestion before it happens and make better campus decisions.
    </small>
</div>
""", unsafe_allow_html=True)

# =========================
# ADMIN DASHBOARD
# =========================

if page == "👨‍💼 Admin Dashboard":

    st.subheader("📊 Campus Operations Dashboard")

    col1, col2 = st.columns(2)

    with col1:

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

        current_count = st.number_input(
            "👥 Current Students",
            min_value=0,
            max_value=1000,
            value=180
        )

    with col2:

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

        event = st.selectbox(
            "🎉 Campus Event?",
            ["No", "Yes"]
        )

        previous_count = st.number_input(
            "👥 Previous Crowd",
            min_value=0,
            max_value=1000,
            value=170
        )

    st.divider()

    if st.button(
        "🔮 PREDICT CAMPUS CROWD",
        use_container_width=True
    ):

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

        prediction = model.predict(input_data)[0]
        prediction = max(0, round(prediction))

        # =========================
        # RISK LEVEL
        # =========================

        if prediction < 150:

            risk = "LOW"
            risk_icon = "🟢"
            recommendation = (
                "Normal campus operation. "
                "No immediate action required."
            )

        elif prediction < 300:

            risk = "MEDIUM"
            risk_icon = "🟡"
            recommendation = (
                "Monitor the crowd and prepare "
                "for possible congestion."
            )

        elif prediction < 400:

            risk = "HIGH"
            risk_icon = "🟠"
            recommendation = (
                "Open an additional counter "
                "and increase staff monitoring."
            )

        else:

            risk = "CRITICAL"
            risk_icon = "🔴"
            recommendation = (
                "Open additional counters, "
                "increase staff and redirect students."
            )

        # =========================
        # METRICS
        # =========================

        st.subheader("🤖 AI Prediction")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "📍 Location",
                location
            )

        with c2:
            st.metric(
                "👥 Current Crowd",
                current_count
            )

        with c3:
            st.metric(
                "🔮 Predicted Crowd",
                prediction
            )

        with c4:
            st.metric(
                "⚠️ Risk Level",
                f"{risk_icon} {risk}"
            )

        st.divider()

        # =========================
        # CHART
        # =========================

        st.subheader("📈 Crowd Prediction Analytics")

        hours = list(range(8, 19))

        predicted_values = []

        for h in hours:

            temp = pd.DataFrame({
                "hour": [h],
                "day": [day_number],
                "current_count": [current_count],
                "event": [event_number],
                "previous_count": [previous_count]
            })

            value = model.predict(temp)[0]
            predicted_values.append(round(value))

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hours,
                y=predicted_values,
                mode="lines+markers",
                name="Predicted Crowd"
            )
        )

        fig.add_hline(
            y=300,
            line_dash="dash",
            annotation_text="High Risk Threshold"
        )

        fig.update_layout(
            template="plotly_dark",
            height=400,
            xaxis_title="Hour",
            yaxis_title="Students",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =========================
        # AI DECISION CENTER
        # =========================

        st.subheader("🤖 AI Decision Center")

        if risk == "LOW":
            st.success(
                f"🟢 LOW RISK — {recommendation}"
            )

        elif risk == "MEDIUM":
            st.warning(
                f"🟡 MEDIUM RISK — {recommendation}"
            )

        elif risk == "HIGH":
            st.warning(
                f"🟠 HIGH RISK — {recommendation}"
            )

        else:
            st.error(
                f"🔴 CRITICAL — {recommendation}"
            )

        st.markdown(
            f"""
            <div class="info-box">
            <b>💡 AI Recommendation</b><br><br>
            {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "CampusFlow AI • Predict Before Problems Happen"
        )

# =========================
# STUDENT VIEW
# =========================

else:

    st.subheader("🎓 Student View")

    st.markdown("""
    <div class="student-box">
        <h2>🚶 Plan Your Campus Visit</h2>
        <p>
        Check the predicted crowd level before visiting
        a campus location.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        student_location = st.selectbox(
            "📍 Where do you want to go?",
            [
                "Library",
                "Canteen A",
                "Canteen B",
                "Main Block",
                "Bus Stand"
            ]
        )

        student_hour = st.slider(
            "🕐 What time are you planning to go?",
            8,
            18,
            13
        )

    with col2:

        student_day = st.selectbox(
            "📅 Select Day",
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

        student_event = st.selectbox(
            "🎉 Is there a campus event?",
            ["No", "Yes"]
        )

    st.divider()

    student_current = st.number_input(
        "👥 Estimated Current Students",
        min_value=0,
        max_value=1000,
        value=150
    )

    student_previous = st.number_input(
        "👥 Previous Crowd",
        min_value=0,
        max_value=1000,
        value=140
    )

    if st.button(
        "🎯 CHECK CROWD",
        use_container_width=True
    ):

        day_number = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ].index(student_day)

        event_number = (
            1 if student_event == "Yes" else 0
        )

        student_input = pd.DataFrame({
            "hour": [student_hour],
            "day": [day_number],
            "current_count": [student_current],
            "event": [event_number],
            "previous_count": [student_previous]
        })

        student_prediction = model.predict(
            student_input
        )[0]

        student_prediction = max(
            0,
            round(student_prediction)
        )

        # =========================
        # STUDENT STATUS
        # =========================

        if student_prediction < 150:

            status = "🟢 NOT CROWDED"
            advice = (
                "Great time to visit! "
                "The location is expected to be comfortable."
            )

        elif student_prediction < 300:

            status = "🟡 MODERATELY BUSY"
            advice = (
                "The location may be somewhat busy. "
                "You can still visit."
            )

        elif student_prediction < 400:

            status = "🟠 CROWDED"
            advice = (
                "Consider visiting a little later "
                "to avoid waiting."
            )

        else:

            status = "🔴 VERY CROWDED"
            advice = (
                "Avoid this location for now. "
                "Try visiting later when the crowd decreases."
            )

        st.subheader("🔮 Your Campus Crowd Forecast")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📍 Location",
                student_location
            )

        with c2:
            st.metric(
                "👥 Expected Crowd",
                f"{student_prediction}"
            )

        with c3:
            st.metric(
                "🚦 Status",
                status
            )

        st.divider()

        if student_prediction < 150:
            st.success(
                f"### {status}\n\n{advice}"
            )

        elif student_prediction < 300:
            st.info(
                f"### {status}\n\n{advice}"
            )

        elif student_prediction < 400:
            st.warning(
                f"### {status}\n\n{advice}"
            )

        else:
            st.error(
                f"### {status}\n\n{advice}"
            )

        st.markdown(
            f"""
            <div class="info-box">
            <h3>🎓 Student Recommendation</h3>
            <p>
            Based on the current campus conditions,
            CampusFlow AI expects approximately
            <b>{student_prediction} students</b>
            at <b>{student_location}</b>.
            </p>
            <p>
            💡 <b>{advice}</b>
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.caption(
            "CampusFlow AI • Helping students move smarter around campus"
        )

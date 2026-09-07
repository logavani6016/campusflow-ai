
import streamlit as st
import pandas as pd
import joblib

# Load trained AI model
model = joblib.load("model.pkl")

# Page settings
st.set_page_config(
    page_title="CampusFlow AI",
    page_icon="🏙️",
    layout="wide"
)

# Title
st.title("🏙️ CampusFlow AI")
st.subheader("Predictive Smart Campus Management")

st.write(
    "Predict campus crowd levels before congestion happens "
    "and receive AI-powered recommendations."
)

st.divider()

# Input section
st.header("📊 Campus Information")

col1, col2 = st.columns(2)

with col1:

    location = st.selectbox(
        "📍 Campus Location",
        ["Canteen A", "Canteen B", "Main Block", "Library", "Bus Stand"]
    )

    hour = st.slider(
        "🕐 Current Hour",
        8,
        18,
        13
    )

    current_count = st.number_input(
        "👥 Current Student Count",
        min_value=0,
        max_value=1000,
        value=180
    )

with col2:

    day = st.selectbox(
        "📅 Day",
        ["Monday", "Tuesday", "Wednesday",
         "Thursday", "Friday", "Saturday", "Sunday"]
    )

    event = st.selectbox(
        "🎉 Is there an event?",
        ["No", "Yes"]
    )

    previous_count = st.number_input(
        "👥 Previous Crowd",
        min_value=0,
        max_value=1000,
        value=170
    )

# Prediction button
st.divider()

if st.button("🔮 PREDICT CAMPUS CROWD", use_container_width=True):

    # Convert inputs
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

    # Prepare input
    input_data = pd.DataFrame({
        "hour": [hour],
        "day": [day_number],
        "current_count": [current_count],
        "event": [event_number],
        "previous_count": [previous_count]
    })

    # AI prediction
    prediction = model.predict(input_data)[0]

    prediction = round(prediction)

    # Risk and recommendation
    if prediction < 150:

        risk = "🟢 LOW"
        recommendation = "Normal campus operation."

    elif prediction < 300:

        risk = "🟡 MEDIUM"
        recommendation = "Monitor the crowd."

    elif prediction < 400:

        risk = "🟠 HIGH"
        recommendation = "Open an additional counter."

    else:

        risk = "🔴 CRITICAL"
        recommendation = (
            "Open an additional counter and "
            "redirect students to another location."
        )

    # Results
    st.header("🤖 AI Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Predicted Crowd",
            f"{prediction} students"
        )

    with col2:
        st.metric(
            "Risk Level",
            risk
        )

    with col3:
        st.metric(
            "Location",
            location
        )

    st.divider()

    st.subheader("💡 AI Recommendation")

    st.info(recommendation)

    st.success(
        f"CampusFlow AI predicts approximately "
        f"{prediction} students at {location}."
    )

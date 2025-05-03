import streamlit as st
import pandas as pd
import time
import datetime
import os

from utils.notifications import trigger_alert, send_email_alert
from utils.pdf_exporter import export_stress_report_to_pdf

from modules.facial_analysis import analyze_facial_expression
from modules.voice_analysis import analyze_voice_tone
from modules.typing_analysis import analyze_typing_behavior

# Initialize session state
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'stress_data' not in st.session_state:
    st.session_state.stress_data = []

# Page settings
st.set_page_config(page_title="AI Stress Monitor", layout="wide")
st.title("🧠 AI-Powered Stress Detection Dashboard")

# Sidebar controls
st.sidebar.header("Live Monitoring Controls")

if not st.session_state.monitoring:
    if st.sidebar.button("▶️ Start Monitoring"):
        st.session_state.monitoring = True
        st.success("Live monitoring started...")
else:
    if st.sidebar.button("⏸ Pause Monitoring"):
        st.session_state.monitoring = False
        st.warning("Live monitoring paused.")
    if st.sidebar.button("⏹ Stop Monitoring"):
        st.session_state.monitoring = False
        st.success("Monitoring stopped. Displaying recorded data...")

# Date filters for historical data
st.sidebar.header("Filter by Date/Time")
start_date = st.sidebar.date_input("Start Date", datetime.date.today())
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Live monitoring loop
placeholder = st.empty()

if st.session_state.monitoring:
    with placeholder.container():
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        facial_stress = analyze_facial_expression()
        voice_stress = analyze_voice_tone()
        typing_stress = analyze_typing_behavior()
        overall_stress = (facial_stress + voice_stress + typing_stress) / 3

        st.session_state.stress_data.append({
            "timestamp": timestamp,
            "facial": facial_stress,
            "voice": voice_stress,
            "typing": typing_stress,
            "overall": overall_stress
        })

        df = pd.DataFrame(st.session_state.stress_data)
        st.line_chart(df.set_index("timestamp")[["facial", "voice", "typing", "overall"]])

        if overall_stress > 0.7:
            st.warning("⚠️ High stress levels detected!")
            trigger_alert("High stress alert!", "Stress levels exceeded threshold.")
            send_email_alert("High Stress Alert", f"Stress levels exceeded threshold at {timestamp}.", "recipient@example.com")

        time.sleep(2)

# Show recorded data in table
if not st.session_state.monitoring and len(st.session_state.stress_data) > 0:
    st.subheader("📊 Recorded Stress Data")
    df = pd.DataFrame(st.session_state.stress_data)
    st.dataframe(df)

# Export report
if st.button("📄 Export Report as PDF"):
    export_stress_report_to_pdf(st.session_state.stress_data, "stress_report.pdf")
    st.success("Report exported successfully.")
    with open("stress_report.pdf", "rb") as file:
        st.download_button("Download PDF", file, file_name="stress_report.pdf", mime="application/pdf")

import streamlit as st
from modules.visualizer import StressVisualizer
from modules.facial_analysis import analyze_facial_expression
from modules.voice_analysis import analyze_voice_tone
from modules.typing_analysis import analyze_typing_behavior
import time

st.set_page_config(page_title="AI Stress Monitor", layout="wide")
st.title("🧠 AI-Powered Stress Detection Dashboard")

st.sidebar.header("Live Monitoring Controls")
run_monitoring = st.sidebar.button("Start Monitoring")

visualizer = StressVisualizer()
chart_placeholder = st.empty()

if run_monitoring:
    st.success("Live monitoring started...")
    for _ in range(30):  # Run for ~30 cycles (30 seconds or adjust)
        facial = analyze_facial_expression()
        voice = analyze_voice_tone()
        typing = analyze_typing_behavior()
        visualizer.add_stress_data(facial, voice, typing)

        with chart_placeholder.container():
            st.line_chart(visualizer.data.set_index("timestamp"))

        time.sleep(1)

    visualizer.export_report()
    st.success("Monitoring complete! Report saved.")
    st.dataframe(visualizer.data)

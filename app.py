import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from pothole_detector import detect_potholes, play_alert_sound  # Ensure this module is updated

# Set up the Streamlit app
st.set_page_config(page_title="Pothole Detection System", page_icon="🛣️", layout="wide")

# Sidebar Controls
st.sidebar.header("Settings")
enable_alerts = st.sidebar.checkbox("Enable Audio Alerts", value=True)
threshold_value = st.sidebar.slider("Threshold Value", 50, 255, 140)
min_area = st.sidebar.slider("Min Pothole Area", 100, 5000, 3093)
sensitivity = st.sidebar.slider("Detection Sensitivity", 0.1, 1.0, 0.10, 0.05)

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])

# Main UI Sections
st.title("Pothole Detection System")
col1, col2 = st.columns([2, 1])

with col1:
    video_placeholder = st.empty()
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

with col2:
    st.markdown("### Detection Stats")
    pothole_count_placeholder = st.empty()
    avg_size_placeholder = st.empty()
    severity_placeholder = st.empty()
    alert_placeholder = st.empty()
    chart_placeholder = st.empty()

# Process Video Function
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if fps == 0:
        fps = 30  # Fallback for unknown FPS

    total_potholes = 0
    pothole_sizes = []
    frame_pothole_counts = []

    current_frame = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        current_frame += 1
        progress = current_frame / total_frames
        progress_placeholder.progress(progress)
        status_placeholder.text(f"Processing frame {current_frame} of {total_frames}")

        # Detect potholes in the frame
        processed_frame, potholes = detect_potholes(frame, threshold_value, min_area, sensitivity)

        # Update stats
        frame_pothole_count = len(potholes)
        total_potholes += frame_pothole_count
        frame_pothole_counts.append(frame_pothole_count)

        for pothole in potholes:
            pothole_sizes.append(pothole["area"])

        # Play alert if potholes detected
        if enable_alerts and frame_pothole_count > 0:
            play_alert_sound()
            alert_placeholder.markdown("⚠️ **POTHOLE DETECTED!**", unsafe_allow_html=True)
        else:
            alert_placeholder.empty()

        # Display processed frame
        processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(processed_frame_rgb, channels="RGB", use_column_width=True)

        # Update Statistics
        update_statistics(total_potholes, pothole_sizes, frame_pothole_counts)

        # Slow down for real-time effect
        time.sleep(1 / fps)

    cap.release()
    status_placeholder.text("Processing complete!")
    # Play alert sound at the end if potholes were detected
    if total_potholes > 0 and enable_alerts:
        play_alert_sound()
    update_statistics(total_potholes, pothole_sizes, frame_pothole_counts, final=True)

# Update Stats Display
def update_statistics(total_potholes, pothole_sizes, frame_pothole_counts, final=False):
    pothole_count_placeholder.markdown(f"**Total Potholes:** {total_potholes}")
    
    avg_size = np.mean(pothole_sizes) if pothole_sizes else 0
    avg_size_placeholder.markdown(f"**Avg. Size:** {int(avg_size)} px²")

    # Severity Level
    if total_potholes == 0:
        severity = "Excellent"
        color = "green"
    elif total_potholes < 5:
        severity = "Good"
        color = "lightgreen"
    elif total_potholes < 10:
        severity = "Fair"
        color = "orange"
    else:
        severity = "Poor"
        color = "red"

    severity_placeholder.markdown(f"**Road Condition:** <span style='color:{color};'>{severity}</span>", unsafe_allow_html=True)

    # Chart Display
    if frame_pothole_counts:
        df = pd.DataFrame({"Frame": range(len(frame_pothole_counts)), "Potholes": frame_pothole_counts})
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(df["Frame"], df["Potholes"], color="#1E88E5")
        ax.set_xlabel("Frame")
        ax.set_ylabel("Potholes Detected")
        ax.grid(True, linestyle="--", alpha=0.7)
        chart_placeholder.pyplot(fig)

# Start Processing if Video is Uploaded
if uploaded_file is not None:
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_file.read())
    temp_video.close()
    process_video(temp_video.name)
    os.unlink(temp_video.name)
else:
    video_placeholder.image("https://via.placeholder.com/640x360.png?text=Upload+a+video+to+begin", use_column_width=True)
    status_placeholder.text("Waiting for video upload...")

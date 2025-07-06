import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info and warning messages
import tensorflow as tf
tf.get_logger().setLevel('ERROR')  # Suppress TensorFlow warnings

import streamlit as st
import cv2
import numpy as np
import tempfile
from datetime import datetime
from keras.models import load_model
from email.message import EmailMessage
import smtplib
import time
import pathlib
import threading

# ---------------- Configuration ----------------
MODEL_PATH = "Models/violence.h5"
SEQUENCE_LENGTH = 8
FRAME_SIZE = (48, 48)
CONFIDENCE_THRESHOLD = 0.65

# ---------------- Load Model ----------------
@st.cache_resource(show_spinner="Loading violence detection model...")
def load_violence_model():
    try:
        # Suppress the specific abseil warning
        import absl.logging
        absl.logging.set_verbosity(absl.logging.ERROR)
        
        model = load_model(MODEL_PATH)
        # Compile the model to avoid the metrics warning
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    except Exception as e:
        st.error(f"Model failed to load: {str(e)}")
        st.stop()

model = load_violence_model()

# ---------------- Initial Branding ----------------
st.title("🛡️ Violence Detection System")
st.caption("Developed by Gopal Patil")
st.markdown("""🔍 Our AI-powered system analyzes real-time video to detect potential violence and alert the registered individual.""")

# ---------------- Register User Email ----------------
if "email_registered" not in st.session_state:
    st.session_state.email_registered = False
if not st.session_state.email_registered:
    with st.form("register_form"):
        st.subheader("📩 Register Email for Receiving Alerts")
        email_user = st.text_input("Enter Your Email ID", placeholder="example@gmail.com")
        submitted = st.form_submit_button("Register and Proceed")

        if submitted:
            if email_user and "@" in email_user:
                st.session_state.email_user = email_user
                st.session_state.email_registered = True
                st.success("✅ Email registered successfully! Scroll to start detection.")
                st.rerun()
            else:
                st.warning("Please enter a valid email address.")
    st.stop()

email_user = st.session_state.email_user

# ---------------- Helper Functions ----------------
def play_alert_sound():
    """Play a simple alert sound (beep)"""
    try:
        import winsound  # Windows only
        winsound.Beep(1000, 500)  # Frequency 1000Hz, duration 500ms
    except:
        pass  # Skip sound if not on Windows or if fails

# ---------------- Email Alert Function ----------------
def send_email_alert(image_path, label, confidence, receiver):
    msg = EmailMessage()
    msg['Subject'] = '📸 Violence Detected!'
    msg['From'] = "x.security.alert@gmail.com"  # Static sender
    msg['To'] = receiver
    msg.set_content(f'Detection Alert\nLabel: {os.path.basename(image_path)}\nPrediction: {label}\nConfidence: {confidence:.2f}\nTime: {datetime.now()}')

    with open(image_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("your@gmail.com", "password")  # Replace with app password
            smtp.send_message(msg)
    except Exception as e:
        st.warning(f"⚠️ Could not send email: {str(e)}")

# ---------------- Video Processing Thread ----------------
def video_processing_thread(video_path, progress_bar, video_display, violence_count):
    """Thread for processing video files"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            st.error("❌ Failed to open video file")
            return 0

        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if total_frames < SEQUENCE_LENGTH:
            st.error(f"❌ Video too short! Needs at least {SEQUENCE_LENGTH} frames, got {total_frames}.")
            cap.release()
            return 0

        st.info(f"📹 Video Info: {total_frames} frames | {fps:.2f} FPS")
        
        frame_buffer = []
        processed_frames = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frames += 1
            
            
            # Process frame
            resized = cv2.resize(frame, FRAME_SIZE)
            normalized = resized.astype("float32") / 255.0
            frame_buffer.append(normalized)
            
            if len(frame_buffer) > SEQUENCE_LENGTH:
                frame_buffer.pop(0)
            
            # Make prediction when we have enough frames
            if len(frame_buffer) == SEQUENCE_LENGTH:
                input_data = np.expand_dims(frame_buffer, axis=0)
                prediction = model.predict(input_data, verbose=0)[0][0]
                
                label = "Violence" if prediction >= CONFIDENCE_THRESHOLD else "Normal"
                confidence = float(prediction)
                
                # Annotate frame
                color = (0, 0, 255) if label == "Violence" else (0, 255, 0)
                cv2.putText(frame, f"{label} ({confidence:.2f})", (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(frame, f"Frame: {processed_frames}/{total_frames}", (10, 70),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Display frame - FIXED DEPRECATION WARNING
                video_display.image(frame, channels="BGR", use_container_width=True)
                
                # Handle violence detection
                if label == "Violence":
                    violence_count[0] += 1
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    snapshot_path = f"snapshots/violence_{timestamp}.jpg"
                    os.makedirs("snapshots", exist_ok=True)
                    cv2.imwrite(snapshot_path, frame)
                    send_email_alert(snapshot_path, label, confidence, email_user)
                    play_alert_sound()
            
            # Update progress
            progress_bar.progress(min(processed_frames / total_frames, 1.0))
            
            # Add small delay to allow UI updates
            time.sleep(0.01)
        
        cap.release()
        return violence_count[0]
        
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        return 0

# ---------------- Live Camera Processing ----------------
def process_live_camera():
    """Process live camera feed"""
    stframe = st.empty()
    stop_button = st.button("🛑 Stop Camera")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Could not access webcam. Please check permissions.")
        return
    
    frame_buffer = []
    st.info("🟢 Live camera started. Press 'Stop Camera' to end.")
    
    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Failed to capture frame")
            break
            
        # Process frame
        resized = cv2.resize(frame, FRAME_SIZE)
        normalized = resized.astype("float32") / 255.0
        frame_buffer.append(normalized)
        
        if len(frame_buffer) > SEQUENCE_LENGTH:
            frame_buffer.pop(0)
        
        # Make prediction when we have enough frames
        if len(frame_buffer) == SEQUENCE_LENGTH:
            input_data = np.expand_dims(frame_buffer, axis=0)
            prediction = model.predict(input_data, verbose=0)[0][0]
            
            label = "Violence" if prediction >= CONFIDENCE_THRESHOLD else "Normal"
            confidence = float(prediction)
            
            # Annotate frame with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            color = (0, 0, 255) if label == "Violence" else (0, 255, 0)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (10, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, timestamp, (10, 70), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Display frame - FIXED DEPRECATION WARNING
            stframe.image(frame, channels="BGR", use_container_width=True)
            
            # Handle violence detection
            if label == "Violence":
                os.makedirs("snapshots", exist_ok=True)
                snapshot_path = f"snapshots/violence_{timestamp.replace(':', '-')}.jpg"
                cv2.imwrite(snapshot_path, frame)
                send_email_alert(snapshot_path, label, confidence, email_user)
                play_alert_sound()
                st.success(f"📸 Violence detected! Confidence: {confidence:.2f}")
        
        # Small delay to prevent UI freeze
        time.sleep(0.03)
    
    cap.release()
    st.success("🛑 Camera stopped")

# ---------------- Main Application ----------------
st.markdown("**Choose a mode to start:**")

# Initialize session state
if "processing_video" not in st.session_state:
    st.session_state.processing_video = False
if "video_file" not in st.session_state:
    st.session_state.video_file = None
if "violence_count" not in st.session_state:
    st.session_state.violence_count = 0

col1, col2 = st.columns(2)

# Live camera mode
if col1.button("📹 Start Camera Monitoring"):
    process_live_camera()

# Video upload mode
if col2.button("📁 Analyze Uploaded Video"):
    st.session_state.processing_video = False
    st.session_state.video_file = None

# File uploader (always visible)
uploaded_file = st.file_uploader("Upload video file", type=['mp4', 'avi', 'mov'], key="file_uploader")

# Process uploaded file if exists
if uploaded_file is not None and not st.session_state.processing_video:
    # Save uploaded file to temporary location
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=pathlib.Path(uploaded_file.name).suffix)
    tfile.write(uploaded_file.read())
    tfile.close()
    
    st.session_state.video_file = tfile.name
    st.session_state.processing_video = True
    st.session_state.violence_count = 0
    st.rerun()

# Process video if we have one to process
if st.session_state.processing_video and st.session_state.video_file:
    st.info(f"Processing: {pathlib.Path(st.session_state.video_file).name}")
    
    # Create UI elements
    progress_bar = st.progress(0)
    video_display = st.empty()
    
    # Start processing in a thread
    violence_count = [0]  # Mutable container for thread
    violence_count[0] = video_processing_thread(
        st.session_state.video_file, 
        progress_bar, 
        video_display,
        violence_count
    )
    
    # Update session state with final count
    st.session_state.violence_count = violence_count[0]
    
    # Clean up
    try:
        os.unlink(st.session_state.video_file)
    except:
        pass
    
    st.success(f"✅ Processing complete. Violence detected in {st.session_state.violence_count} frames")
    st.session_state.processing_video = False
    st.session_state.video_file = None
# Real-Time Violence Detection System

**AI-powered system to detect violent behavior in live videos or uploaded clips.**  
Uses **3D CNN**, **OpenCV**, and **Streamlit** for a lightweight, real-time monitoring solution.

---

## Features

- Real-time webcam monitoring  
- Upload and analyze video files  
- Snapshots saved automatically on detection  
- Plays an alert sound (`alert.wav`)  
- Sends an email with the snapshot attached  
- Runs efficiently on mid-range systems  
- Simple Streamlit UI for ease of use  

---

## Model Details

- Input: 64×64 RGB frames  
- Sequence length: 16 frames  
- Model: Binary classifier (`Violence` vs `Normal`)  
- Framework: TensorFlow/Keras  
- File: `Models/violence.h5`  

*You can replace the model with your own trained version in the same format.*

---

## Dataset

- Dataset: **RWF-2000** (2,000 short clips, 5–10 seconds each)  
- 1,000 fight videos + 1,000 non-fight videos  
- Original resolution: 320×240 → resized to 64×64  

[RWF-2000 on Kaggle](https://www.kaggle.com/datasets/vulamnguyen/rwf2000)  

> Dataset is not included. Please download manually.

---

## Project Structure

```

Violence-Detection/
│
├── app.py              # Streamlit app
├── alert.wav           # Sound alert
├── requirements.txt    # Dependencies
├── Models/
│   └── violence.h5     # Trained model
├── snapshots/          # Saved frames on detection
├── test_videos/        # Optional test clips
└── README.md

````

---

## Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

---

## Run the App

```bash
streamlit run app.py
```

Modes available:

* Live Camera Monitoring
* Upload a Video

Detected violence triggers: snapshot saved, sound alert, and email notification.

---

## Email Alerts

1. Enable 2-Step Verification in your Gmail account
2. Generate an App Password
3. Update `app.py` with your credentials:

```python
msg['From'] = "your_email@gmail.com"
smtp.login("your_email@gmail.com", "your_app_password")
```

---

## Sound Alerts

* Plays `alert.wav` on detection
* Replaceable with any `.wav` file

---

## Detection Workflow

* Snapshot saved in `snapshots/`
* Alert sound played
* Email sent with snapshot attached
* Live frame annotated in the UI

**Pipeline:**

```
Video Input → Preprocessing → 3D CNN → Prediction → Snapshot / Sound / Email Alert
```

---

## Customization & Future Enhancements

* Swap in your own trained model
* Adjust confidence threshold in `app.py`
* Change frame size if required by model
* Replace sound or modify email behavior
* Add bounding boxes, multi-camera support, or dashboard
* Deploy on Raspberry Pi or cloud

---
## Demo Preview

![Demo](https://github.com/user-attachments/assets/61ebea80-3cde-475d-949e-023de75cf853)

## Impact

> Helps security personnel detect violent behavior automatically, reducing response time and improving safety.


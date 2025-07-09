# 🛡️ Real-Time Violence Detection System

This project implements a real-time violence detection system using **deep learning**, **OpenCV**, and **Streamlit**. It leverages a pre-trained binary classification model (e.g.3D CNN) to identify violent behavior in videos, either live from a webcam or from an uploaded video file.

---

## 🚀 Features

✅ Real-time video feed violence detection  
✅ Video upload and batch processing support  
✅ Automatic snapshot capture when violence is detected  
✅ 🔊 Sound alert on detection (`alert.wav`)  
✅ 📧 Email notification with attached snapshot  
✅ Lightweight and efficient – works on low-end systems  
✅ Friendly user interface via [Streamlit](https://streamlit.io/)

---

## 🧠 Model Info

- **Input size:** 64x64 RGB frames  
- **Sequence length:** 16 frames  
- **Model type:** Binary classifier (`Violence` vs `Normal`)  
- **Framework:** TensorFlow/Keras  
- **File:** `Models/violence.h5`

> You can replace `violence.h5` with your own trained model in the same format.

---
📊 Dataset Information

The model was trained on the RWF-2000 dataset.

Dataset Details:
----------------
- Total Videos: 2,000
  - Fight: 1,000 videos
  - NonFight: 1,000 videos

- Clip Duration: 5–10 seconds
- Original Resolution: 320×240
- Preprocessed Size: 64×64

Source:
-------
Dataset Name: RWF-2000
Kaggle URL: https://www.kaggle.com/datasets/vulamnguyen/rwf2000

Download Command (for Kaggle CLI):
-----------------------------------
!kaggle datasets download -d vulamnguyen/rwf2000

Note:
-----
This dataset is not included in this repository.
Please download it manually from Kaggle before training or inference.


## 🗂️ Project Structure

```
Violence-Detection/
│
├── app.py                     # Main Streamlit application
├── alert.wav                  # Sound alert played on detection
├── requirements.txt           # All dependencies
├── README.md                  # You're reading it
│
├── Models/
│   └── violence.h5            # Trained Keras model file
│
├── snapshots/                 # Auto-generated snapshots of violence
├── test_videos/               # (Optional) Videos for offline testing
└── .gitignore                 # Ignores model files, snapshots, etc.
```

---

## ⚙️ Installation

### 🐍 Python Environment

```bash
# (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install required packages
pip install -r requirements.txt
```

---

## 💻 How to Run

```bash
streamlit run app.py
```

> This will launch a browser interface with two modes:
> - 📹 Live Camera Monitoring
> - 📁 Upload a Video

---

## 📧 Email Alert Configuration

The email system uses a static sender Gmail account (e.g., `xyz.security.alert@gmail.com`) with an app password.

**To set up your own:**
1. Enable **2-Step Verification** on your Gmail
2. Generate an **App Password** in your Google Account settings
3. Update `app.py` with:
   ```python
   msg['From'] = "your_email@gmail.com"
   smtp.login("your_email@gmail.com", "your_app_password")
   ```

---

## 🔊 Sound Alert

On detecting violence, a short warning sound (`alert.wav`) is played using `pygame`.  
You can replace it with any other sound file.

---

## 🧪 Sample Output

When violence is detected:
- Frame is saved to `snapshots/` with timestamp
- Sound is played
- Email is sent with attached snapshot
- Live frame is annotated and displayed

---

## 🛠️ Customization

You can modify:
- **Model**: Replace `Models/violence.h5` with your own
- **Confidence Threshold**: Adjust `CONFIDENCE_THRESHOLD` in `app.py`
- **Frame Size**: Change `FRAME_SIZE` to match your model input
- **Sound or Email Behavior**

---



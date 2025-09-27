
````markdown
# 🛡️ Real-Time Violence Detection System

![Python](https://img.shields.io/badge/Python-3.11-blue) ![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-orange) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)

**Detect violent behavior in live videos or uploaded clips using AI in real-time.**  
Leveraging **deep learning (3D CNN)**, **OpenCV**, and **Streamlit**, this system is lightweight and deployable on low-end machines.

---

## 🚀 Features

- ✅ Real-time live webcam detection  
- ✅ Video upload & batch processing  
- ✅ Automatic snapshots on violence detection  
- ✅ 🔊 Sound alert (`alert.wav`)  
- ✅ 📧 Email notifications with snapshots  
- ✅ Friendly, interactive UI via [Streamlit](https://streamlit.io/)  
- ✅ Lightweight and efficient  

---

## 🧠 Model Info

- **Type:** Binary classifier (`Violence` vs `Normal`)  
- **Framework:** TensorFlow/Keras  
- **Input:** 64×64 RGB frames, sequence length 16  
- **File:** `Models/violence.h5` (replaceable with your own trained model)  

---

## 📊 Dataset

- **Name:** RWF-2000 (Kaggle)  
- **Total Videos:** 2,000 (1,000 Fight / 1,000 NonFight)  
- **Clip Duration:** 5–10 sec, original resolution 320×240  
- **Preprocessed:** 64×64  

```bash
# Kaggle CLI download
!kaggle datasets download -d vulamnguyen/rwf2000
````

> Dataset not included — download manually from Kaggle.

---

## 🗂️ Project Structure

```
Violence-Detection/
│
├── app.py                # Main Streamlit application
├── alert.wav             # Sound alert
├── requirements.txt
├── README.md
│
├── Models/
│   └── violence.h5
├── snapshots/            # Auto-saved snapshots
├── test_videos/          # Optional test videos
└── .gitignore
```

---

## ⚙️ Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 💻 Usage

```bash
streamlit run app.py
```

* Modes:

  * 📹 Live Camera Monitoring
  * 📁 Upload a Video

* Violence triggers: snapshot saved, sound alert, and email notification.

---

## 📧 Email Alert Setup

1. Enable **2-Step Verification** in Gmail
2. Generate **App Password**
3. Update `app.py`:

```python
msg['From'] = "your_email@gmail.com"
smtp.login("your_email@gmail.com", "your_app_password")
```

---

## 🔊 Sound Alert

* File: `alert.wav`
* Replaceable with your own sound

---

## 🧪 Sample Output

* Frame saved to `snapshots/`
* Sound alert played
* Email sent with snapshot
* Live frame annotated

---

## 🛠️ Customization

* Replace model: `Models/violence.h5`
* Adjust confidence threshold: `CONFIDENCE_THRESHOLD`
* Change frame size: `FRAME_SIZE`
* Modify sound/email behavior

---

### 💡 Tips to Make It Stand Out

* Add a **GIF of live detection** at the top
* Include a **1-minute demo video** link
* Add a **workflow diagram**: `Video → Preprocessing → Model → Alert/Email`

```

---

If you want, I can now **rewrite the README for your Multi-Agent Debate and Gym-AI-Trainer projects** in this **same polished Markdown style**, so your GitHub profile looks like a professional AI portfolio with **three top pinned projects**.  

Do you want me to do that next?
```

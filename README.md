# 🖐️ Hand Gesture Controlled Computer System

An AI-powered computer vision application that enables users to control their computer using hand gestures instead of a traditional mouse and keyboard. The system uses real-time hand tracking to recognize gestures and perform various computer operations, providing a touchless and intuitive user experience.

---

## 🚀 Features

- 🖱️ Cursor Movement using hand gestures
- 👆 Left Click
- 👉 Right Click=
- 🔄 Scrolling
- 📸 Take Screenshots
- 🔆 Brightness Control
- ⌨️ Virtual Keyboard
- 💻 Launch Visual Studio Code
- 🤚 Real-time Hand Tracking
- ⚡ Smooth and responsive gesture recognition

---

## 🛠️ Tech Stack

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- Pynput
- Screen Brightness Control

---

## 📂 Project Structure

```text
Hand-Gesture-Controlled-System-AI-ML/
│
├── main.py
├── controller.py
├── requirements.txt
│
├── core/
│   ├── hand_tracker.py
│   ├── gesture_recognition.py
│
├── features/
│   ├── mouse_control.py
│   ├── keyboard_mode.py
│   ├── brightness_control.py
│   ├── screenshot.py
│   ├── vs_mode.py
│
├── assets/
│   └── images
│
└── README.md
```

---

## ⚙️ How It Works

1. Captures live video using the webcam.
2. Detects and tracks hand landmarks using MediaPipe.
3. Recognizes predefined hand gestures.
4. Maps each gesture to a specific computer action.
5. Executes the corresponding system command in real time.

---

## 🎯 Supported Gestures

| Gesture | Action |
|---------|--------|
| Index Finger | Move Cursor |
| Pinch Gesture | Left Click |
| Two Fingers | Adjust Screen Brightness |
| Swipe Three Fingers | Scroll |
| Brightness Gesture | Adjust Screen Brightness |
| Keyboard Mode Gesture Four Fingers | Open Virtual Keyboard |
| VS Mode Gesture Thumbs Up | Launch Visual Studio Code |

---

## 💡 Applications

- Touchless Human-Computer Interaction
- Accessibility Support
- Smart Workstations
- Interactive Presentations
- Healthcare & Sterile Environments
- Computer Vision Learning Projects

---

## 🔮 Future Improvements

- Multi-hand gesture support
- Custom gesture mapping
- Volume control
- Media playback controls
- Cross-platform optimization
- Voice command integration
- Gesture customization by users

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/Aastha1326/Hand-Gesture-Controlled-System-AI-ML.git
```

Navigate to the project folder:

```bash
cd Hand-Gesture-Controlled-System-AI-ML
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## 👩‍💻 Author

**Aastha Dua**

- GitHub: https://github.com/Aastha1326
- LinkedIn: https://linkedin.com/in/aastha-dua-a3a164318
- Email: aastha.dua2006@gmail.com

---

⭐ If you found this project helpful, consider giving it a star!

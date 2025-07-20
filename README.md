
# 👁️ Gaze Controller Cursor and Acoustic Input System

Empowering **amputee individuals** and those with limited motor ability to control a computer using just **eye movement** and **voice commands**. This assistive system uses **eye-tracking for cursor control** and **speech recognition for executing commands and typing**, making digital environments accessible without physical input devices.

---

## 🧠 Key Features

- 🎯 **Eye Tracking Cursor Control** using right and left eye landmarks.
  - Right eye blink ➜ *Right-click*
  - Left eye blink ➜ *Left-click + Double-click*
- 🎙️ **Acoustic Voice Input System**
  - Open applications, folders, or files using your voice.
  - Control speech-to-text typing and system operations hands-free.
- 🦾 **Designed for Accessibility**
  - Ideal for amputee or physically impaired users to regain digital independence.

---

## 🛠️ Technologies Used

| Technology | Description |
|-----------|-------------|
| `Python` | Core programming language |
| `OpenCV` | Real-time camera feed handling and image processing |
| `MediaPipe` | Eye landmark detection (face mesh) |
| `PyAutoGUI` | Mouse control based on eye coordinates |
| `SpeechRecognition` | Converts spoken language to text |
| `Pyttsx3` | Text-to-speech engine for feedback |
| `Threading` | Runs continuous voice recognition in the background |
| `Subprocess & OS` | Launches files, applications, and folders |

---

## 📂 Project Structure

```
├── Task_6(Task3+Task4).py        # Main Python script
├── Description.txt               # Project overview and purpose
├── Description-1.txt             # Additional explanation and phase-2 use cases
├── README.md                     # Project documentation (this file)
```

---

## 🚀 How It Works

1. **Cursor Control via Eye Tracking**  
   - Uses MediaPipe FaceMesh to detect landmarks around both eyes.
   - Maps right-eye movement to cursor position.
   - Detects blinks to perform mouse clicks.

2. **Voice Assistant for Commands**
   - Listens continuously in the background.
   - Recognizes predefined voice commands like:
     - `"Open Chrome"`
     - `"Open Documents"`
     - `"Stop"` ➜ Exit the program

3. **Combining Eye + Voice**
   - Users move the cursor with eyes and trigger actions with voice or blinks.

---

## 🎯 Use Case: For Amputee or Paralyzed Users

This system enables people without hand mobility to:

- Operate a computer completely hands-free.
- Open and use essential tools like WordPad, Notepad, VS Code, etc.
- Type using voice, navigate with gaze — no keyboard or mouse needed.

---

## 🧪 Requirements

Before running the project, ensure the following Python packages are installed:

```bash
pip install opencv-python mediapipe pyautogui SpeechRecognition pyttsx3
```

---

## ▶️ Running the Project

```bash
python Task_6(Task3+Task4).py
```

- Make sure your webcam is working.
- Use your **right eye to move the cursor**.
- Blink **left eye for left/double click**, **right eye for right click**.
- Speak commands like `"open chrome"`.

---

## 📌 Notes

- Adjust blink detection threshold if needed for your webcam.
- You can customize the `paths` dictionary in the script to launch other applications/files.
- Currently tested on Windows.

---

## 🙌 Final Thoughts

> “A small 1 cm cursor—when powered by eyes and voice—can empower millions.”

This system isn’t just a tech demo; it's a step toward **inclusive innovation**. Perfect for accessibility-focused hackathons, assistive tech projects, or real-world deployment for individuals with physical disabilities.

import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import os
import threading

# Initialize MediaPipe FaceMesh and text-to-speech engine
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Paths dictionary
paths = {
    "google chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "microsoft edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "canva": "C:\\Users\\DHARSHINI_RAMASAMY\\AppData\\Local\\Programs\\Canva\\Canva.exe",
    "pdf": "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe",
    "java": "C:\\Users\\DHARSHINI_RAMASAMY\\eclipse\\java-2024-09\\eclipse\\eclipse.exe",
    "vs code": "C:\\Users\\DHARSHINI_RAMASAMY\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "opera": "C:\\Users\\DHARSHINI_RAMASAMY\\AppData\\Local\\Programs\\Opera\\opera.exe",
    "pictures": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Pictures",
    "documents": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Desktop\\Dokumen",
    "downloads": "C:\\Users\\DHARSHINI_RAMASAMY\\Downloads",
    "personal files": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Desktop\\Dharshini - Personal",
    "future dna": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Desktop\\Dokumen\\THE FUTURE DNA.pptx",
    "image": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Pictures\\Saved Pictures\\dove.jpg",
    "final": "F:\\Amputees_&_Paraplegics\\Gaze_Controller_Mouse\\Gazer_Pdf.pdf"
}

# Function for text-to-speech
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to open applications, folders, and files
def open_application(app_name):
    app_path = paths.get(app_name.lower())
    if app_path:
        if os.path.isdir(app_path):
            subprocess.Popen(f'explorer "{app_path}"')
        elif os.path.isfile(app_path):
            os.startfile(app_path)
        else:
            subprocess.Popen(app_path)
        speak_text(f"Opened {app_name}, Dharshini.")
    else:
        speak_text(f"Sorry, I don't have a path for {app_name}.")

# Voice command listener function
def listen_for_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if "open" in command.lower():
                found = False
                for name in paths.keys():
                    if name in command.lower():
                        open_application(name)
                        found = True
                        break
                if not found:
                    speak_text("Sorry, I didn't understand.")

            elif "stop" in command.lower():
                speak_text("Stopping the voice assistant. Goodbye, Dharshini.")
                sys.exit()

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
        except (sr.UnknownValueError, sr.RequestError):
            pass

# Separate thread to keep listening for voice commands
def voice_command_thread():
    while True:
        listen_for_command()

# Start the voice command listener in a separate thread
threading.Thread(target=voice_command_thread, daemon=True).start()

# Main loop for eye tracking and cursor control
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Cursor movement using right eye landmarks
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            if id == 1:
                screen_x = min(max(0, screen_w / frame_w * x), screen_w - 1)
                screen_y = min(max(0, screen_h / frame_h * y), screen_h - 1)
                pyautogui.moveTo(screen_x, screen_y)

        # Left eye blink detection (landmarks 145 and 159)
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        if (left_eye[0].y - left_eye[1].y) < 0.007:
            pyautogui.leftClick()
            pyautogui.doubleClick()
            pyautogui.sleep(1)

        # Right eye blink detection (landmarks 374 and 386)
        right_eye = [landmarks[374], landmarks[386]]
        for landmark in right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)

        if (right_eye[0].y - right_eye[1].y) < 0.007:
            pyautogui.rightClick()
            pyautogui.sleep(1)

    # Display the video feed with annotations
    cv2.imshow('Eye Control', frame)
    cv2.waitKey(1)

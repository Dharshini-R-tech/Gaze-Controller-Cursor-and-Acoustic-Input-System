import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import os
import threading
import time
import mss

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

paths = {
    # Applications
    "google": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "microsoft": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "canva": "C:\\Users\\DHARSHINI_RAMASAMY\\AppData\\Local\\Programs\\Canva\\Canva.exe",
    "pdf": "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe",
    "java": "C:\\Users\\DHARSHINI_RAMASAMY\\eclipse\\java-2024-09\\eclipse\\eclipse.exe",
    "vs code": "C:\\Users\\DHARSHINI_RAMASAMY\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "opera": "C:\\Users\\DHARSHINI_RAMASAMY\\AppData\\Local\\Programs\\Opera\\opera.exe",

    # Folders
    "pictures": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Pictures",
    "documents": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Desktop\\Dokumen",
    "downloads": "C:\\Users\\DHARSHINI_RAMASAMY\\Downloads",
    "personal files": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Desktop\\Dharshini - Personal",

    # Files
    "future dna": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Desktop\\Dokumen\\THE FUTURE DNA.pptx",
    "image": "C:\\Users\\DHARSHINI_RAMASAMY\\OneDrive\\Pictures\\Saved Pictures\\dove.jpg",
    "final": "C:\\Amputees_&_Paraplegics\\Gaze_Controller_Mouse\\Gazer_Pdf.pdf"
}

scrolling = False

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

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

def listen_for_commands():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Ready to receive commands...")
        while True:
            try:
                print("Listening for command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Command: {command}")
                process_command(command)
            except sr.UnknownValueError:
                print("Could not understand the command. Please try again.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

def process_command(command):
    global scrolling
    if "type" in command:
        text_to_type = command.split("type")[-1].strip()
        print(f"Typing: {text_to_type}")
        type_text(text_to_type)
        speak_text(f"Done Dharshini.")
    elif "close" in command:
        try:
            pyautogui.hotkey('alt', 'f4')
            print("Attempting to close the current window.")
            speak_text(f"Done Dharshini.")
        except Exception as e:
            print(f"Error while closing the window: {e}")
            pyautogui.press('esc')
            print("Pressed Escape as an alternative to close.")
            speak_text(f"Done Dharshini.")
    elif "copy" in command:
        pyautogui.hotkey('ctrl', 'c')
        print("Copied selected text.")
        speak_text(f"copied Dharshini.")
    elif "paste" in command:
        pyautogui.hotkey('ctrl', 'v')
        print("Pasted copied text.")
        speak_text(f"Pasted Dharshini.")
    elif "scroll down" in command:
        if not scrolling:
            scrolling = True
            threading.Thread(target=continuous_scroll, args=("down",), daemon=True).start()
            print("Scrolling down.")
            speak_text(f"Scrolled down Dharshini.")
    elif "scroll up" in command:
        if not scrolling:
            scrolling = True
            threading.Thread(target=continuous_scroll, args=("up",), daemon=True).start()
            print("Scrolling up.")
            speak_text(f"Scrolled up Dharshini.")
    elif "stop" in command:
        scrolling = False
        print("Stopped scrolling.")
        speak_text(f" Stopped scrolling Dharshini.")
    elif "window" in command:
        pyautogui.hotkey('win', 'd')
        print("Minimized all windows to show desktop.")
        speak_text(f"Done Dharshini.")
    elif "press enter" in command:
        pyautogui.press('enter')
        print("Pressed Enter.")
        speak_text(f"Done Dharshini.")
    elif "zoom in" in command:  
        pyautogui.hotkey('ctrl', '+')
        print("Zoomed in.")
        speak_text(f"Zoomed in Dharshini.")
    elif "zoom out" in command:  
        pyautogui.hotkey('ctrl', '-')
        print("Zoomed out.")
        speak_text(f"Zoomed out Dharshini.")
    elif "screenshot" in command:
        take_screenshot()
    else:
        found = False
        for name in paths.keys():
            if name in command:
                open_application(name)
                found = True
                break
        if not found:
            speak_text("Sorry, I didn't understand.")

def type_text(text):
    pyautogui.write(text, interval=0.05)

def continuous_scroll(direction):
    global scrolling
    scroll_amount = -10 if direction == "down" else 10
    while scrolling:
        pyautogui.scroll(scroll_amount)
        time.sleep(0.01)
    print(f"Stopped scrolling {direction}.")

def take_screenshot():
    try:
        save_path = r"C:\Users\DHARSHINI_RAMASAMY\OneDrive\Pictures\Screenshots"
        with mss.mss() as sct:
            i = 1
            while True:
                screenshot_path = os.path.join(save_path, f"screenshot{i}.png")
                if not os.path.exists(screenshot_path):
                    break
                i += 1
            sct.shot(output=screenshot_path)
        print(f"Screenshot taken and saved as {screenshot_path}.")
        speak_text(f"Done Dharshini, Screenshot taken and saved.")
    except Exception as e:
        print(f"Error while taking screenshot: {e}")

threading.Thread(target=listen_for_commands, daemon=True).start()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    if landmark_points:
        landmarks = landmark_points[0].landmark

        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            if id == 1:
                screen_x = min(max(0, screen_w / frame_w * x), screen_w - 1)
                screen_y = min(max(0, screen_h / frame_h * y), screen_h - 1)
                pyautogui.moveTo(screen_x, screen_y)

        # Blink detection for left eye
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        if (left_eye[0].y - left_eye[1].y) < 0.007:
            pyautogui.leftClick()
            pyautogui.doubleClick()
            time.sleep(1)

        # Blink detection for right eye
        right_eye = [landmarks[374], landmarks[386]]
        for landmark in right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)

        if (right_eye[0].y - right_eye[1].y) < 0.004:
            pyautogui.rightClick()
            time.sleep(1)

    cv2.imshow('Eye Control', frame)
    cv2.waitKey(1)

import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import os

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Dictionary of applications, folders, and file paths
paths = {
    # Applications
    "google chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "microsoft edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
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
    "final": "F:\\Amputees_&_Paraplegics\\Gaze_Controller_Mouse\\Gazer_Pdf.pdf"
}

# Function to provide voice feedback
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to open applications, folders, and files
def open_application(app_name):
    app_path = paths.get(app_name.lower())
    if app_path:
        if os.path.isdir(app_path):
            # Open folders with explorer
            subprocess.Popen(f'explorer "{app_path}"')
        elif os.path.isfile(app_path):
            # Open files with the default associated application
            os.startfile(app_path)
        else:
            # Open executables directly
            subprocess.Popen(app_path)
        speak_text(f"Opened {app_name} Dharshini")
    else:
        speak_text(f"Sorry, I don't have a path for {app_name}.")

# Listening and recognizing commands
def listen_for_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Noise adjustment
        print("Listening...")  # Print statement only for debugging purposes

        try:
            # Capture audio with a longer timeout
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            # Recognize using Google Speech Recognition
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            # Check if the command includes keywords for opening apps, folders, or files
            if "open" in command.lower():
                found = False
                for name in paths.keys():
                    if name in command.lower():
                        open_application(name)
                        found = True
                        break
                if not found:
                    speak_text("Sorry, I didn't understand.")

            # Check if the command is to stop
            elif "stop" in command.lower():
                speak_text("Stopping the voice assistant. Goodbye, Dharshini.")
                sys.exit()

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
        except (sr.UnknownValueError, sr.RequestError):
            pass

# Run the command listener in a loop
while True:
    listen_for_command()

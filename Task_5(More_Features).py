import pyautogui
import os
import mss
import speech_recognition as sr
import threading
import time

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Speech recognition setup
recognizer = sr.Recognizer()

# Global flag for controlling scrolling
scrolling = False

# Function to listen for voice commands
def listen_for_commands():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Ready to receive commands...")
        while True:
            try:
                print("Listening for command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Command: {command}")

                # Process the received command
                process_command(command)

            except sr.UnknownValueError:
                print("Could not understand the command. Please try again.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
    

# Function to process commands
def process_command(command):
    global scrolling
    if "type" in command:
        text_to_type = command.split("type")[-1].strip()
        print(f"Typing: {text_to_type}")
        type_text(text_to_type)
    elif "close" in command:
        try:
            pyautogui.hotkey('alt', 'f4')
            print("Attempting to close the current window.")
        except Exception as e:
            print(f"Error while closing the window: {e}")
            pyautogui.press('esc')
            print("Pressed Escape as an alternative to close.")
    elif "copy" in command:
        pyautogui.hotkey('ctrl', 'c')
        print("Copied selected text.")
    elif "paste" in command:
        pyautogui.hotkey('ctrl', 'v')
        print("Pasted copied text.")
    elif "scroll down" in command:
        if not scrolling:
            scrolling = True
            threading.Thread(target=continuous_scroll, args=("down",), daemon=True).start()
            print("Scrolling down.")
    elif "scroll up" in command:
        if not scrolling:
            scrolling = True
            threading.Thread(target=continuous_scroll, args=("up",), daemon=True).start()
            print("Scrolling up.")
    elif "stop" in command:
        scrolling = False
        print("Stopped scrolling.")
    elif "open" in command:
        pyautogui.hotkey('win', 'd')
        print("Minimized all windows to show desktop.")
    elif "zoom in" in command:  # Added Zoom In command
        pyautogui.hotkey('ctrl', '+')
        print("Zoomed in.")
    elif "zoom out" in command:  # Added Zoom Out command
        pyautogui.hotkey('ctrl', '-')
        print("Zoomed out.")
    elif "press enter" in command:
        pyautogui.press('enter')
        print("Pressed Enter.")
    elif "press ok" in command:
        pyautogui.press('ok')
        print("Pressed ok.")
    elif "press cancel" in command:
        pyautogui.press('cancel')
        print("Pressed cancel.")
    elif "press tab" in command:
        pyautogui.press('tab')
        print("Pressed Tab.")
    elif "press space" in command:
        pyautogui.press('space')
        print("Pressed Space.")
    elif "select word" in command:
        pyautogui.hotkey('ctrl', 'shift', 'right')
        print("Selected a word.")
    elif "select sentence" in command:
        for _ in range(20):
            pyautogui.hotkey('shift', 'right')
            time.sleep(0.05)
        print("Selected a sentence.")
    elif "select paragraph" in command:
        while True:
            pyautogui.hotkey('ctrl', 'shift', 'down')
            time.sleep(0.1)
            # Assuming break when the end of paragraph reached
        print("Selected a paragraph.")
    elif "screenshot" in command:
        take_screenshot()
    else:
        print("Command not recognized.")

# Function to type text as if using the keyboard
def type_text(text):
    pyautogui.write(text, interval=0.05)

# Function to scroll continuously with increased speed
def continuous_scroll(direction):
    global scrolling
    scroll_amount = -60 if direction == "down" else 60  # Increased scroll amount for faster scrolling
    while scrolling:
        pyautogui.scroll(scroll_amount)
        time.sleep(0.01)
    print(f"Stopped scrolling {direction}.")

# Function to take a screenshot with incremental filenames
def take_screenshot():
    try:
        # Define the base path where screenshots will be saved
        save_path = r"C:\Users\DHARSHINI_RAMASAMY\OneDrive\Pictures\Screenshots"

        # Initialize mss for screenshot
        with mss.mss() as sct:
            # Find the next available filename (e.g., screenshot1.png, screenshot2.png, ...)
            i = 1
            while True:
                screenshot_path = os.path.join(save_path, f"screenshot{i}.png")
                if not os.path.exists(screenshot_path):  # Check if the file already exists
                    break
                i += 1

            # Grab the screenshot and save directly to the generated path
            sct.shot(output=screenshot_path)

        print(f"Screenshot taken and saved as {screenshot_path}.")
    
    except Exception as e:
        print(f"Error while taking screenshot: {e}")


# Start voice command listener in a separate thread
threading.Thread(target=listen_for_commands, daemon=True).start()

# Keep the program running so it can always listen for voice commands
while True:
    time.sleep(1)

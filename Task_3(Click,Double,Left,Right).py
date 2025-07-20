import cv2
import mediapipe as mp
import pyautogui

# Initialize camera and MediaPipe FaceMesh
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

pyautogui.FAILSAFE = False  # Disable the fail-safe for smoother cursor movement

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
                # Ensure screen_x and screen_y are within bounds
                screen_x = min(max(0, screen_w / frame_w * x), screen_w - 1)
                screen_y = min(max(0, screen_h / frame_h * y), screen_h - 1)
                pyautogui.moveTo(screen_x, screen_y)

        # Left eye blink detection (landmarks 145 and 159)
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        # Left-click and double-click based on left eye blink
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

        # Right-click based on right eye blink
        if (right_eye[0].y - right_eye[1].y) < 0.007:
            pyautogui.rightClick()
            pyautogui.sleep(1)

    # Display the video feed with annotations
    cv2.imshow('Eye Control', frame)
    cv2.waitKey(1)

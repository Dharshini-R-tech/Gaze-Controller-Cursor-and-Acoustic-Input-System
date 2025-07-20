import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

pyautogui.FAILSAFE = False

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    if landmark_points:
        landmarks = landmark_points[0].landmark
        # Move the cursor using the right eye landmarks
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = min(max(0, screen_w / frame_w * x), screen_w - 1)
                screen_y = min(max(0, screen_h / frame_h * y), screen_h - 1)
                pyautogui.moveTo(screen_x, screen_y)

        # Right eye blink detection (landmarks 374 and 386)
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))

        # Detect blink by comparing y-coordinates of right eye landmarks
        if (left_eye[0].y - left_eye[1].y) < 0.007:
            pyautogui.leftClick()
            pyautogui.doubleClick()
            pyautogui.sleep(1)

    cv2.imshow('eye', frame)
    cv2.waitKey(1)

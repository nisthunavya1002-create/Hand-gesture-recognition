import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

cap=cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:

    while True:
        ret,frame=cap.read()
        if not ret:
            break
        h,w,c=frame.shape
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=hands.process(rgb)
        gesture=""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks=hand_landmarks.landmark
        cv2.imshow("hand gesture recognition",frame)
        if cv2.waitKey(1) & 0xFF==27:
            break
cap.release()
cv2.destroyAllWindows()
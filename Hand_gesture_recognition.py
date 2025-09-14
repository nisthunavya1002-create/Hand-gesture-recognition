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

                fingers_up=[]
                tip_ids=[4,8,12,16,20]

                for i in range(1,5):
                    if landmarks[tip_ids[i]].y<landmarks[tip_ids[i]-2].y:
                        fingers_up.append(1)
                    else:
                        fingers_up.append(0)
                if landmarks[tip_ids[0]].x>landmarks[tip_ids[0]-2].x:
                    fingers_up.insert(0,1)
                else:
                    fingers_up.insert(0,0)
                if fingers_up==[0,1,1,0,0]:
                    gesture="victory"
                elif fingers_up==[1,0,0,0,0]:
                    gesture="thumbs up"
                elif fingers_up==[0,0,0,0,0]:
                    gesture="closed palm"
                elif fingers_up==[1,1,1,1,1]:
                    gesture="open palm"
                elif fingers_up==[0,0,1,1,1]:
                    gesture="ok"
                elif fingers_up==[0,1,1,1,0]:
                    gesture="three"
                else:
                    gesture="no gestures found"
        cv2.putText(frame,f'Gesture:{gesture}',(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow("hand gesture recognition",frame)
        if cv2.waitKey(1) & 0xFF==27:
            break
cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import mouse
import threading
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

frameR = 100
cam_w, cam_h = 640, 480
cap = cv2.VideoCapture(1)
cap.set(3, cam_w)
cap.set(4, cam_h)

l_delay = 0
r_delay = 0
double_delay = 0

def l_clk_delay():
    global l_delay
    time.sleep(1)
    l_delay = 0

def r_clk_delay():
    global r_delay
    time.sleep(1)
    r_delay = 0

def double_clk_delay():
    global double_delay
    time.sleep(2)
    double_delay = 0

while True:
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        hands = None
        with mp_hands.Hands(min_detection_confidence=0.9, max_num_hands=1) as hands:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]

                for lm in hand_landmarks.landmark:
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Mouse movement and clicks
                if results.multi_hand_landmarks:
                    if abs(cx - mid_x) < 25:
                        mouse.move(conv_x, conv_y)

                    if abs(cx - mid_x) < 25 and fingers[4] == 0:
                        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
                            mouse.click(button="left")
                            threading.Thread(target=l_clk_delay).start()

                        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
                            mouse.click(button="right")
                            threading.Thread(target=r_clk_delay).start()

                        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[4] == 0:
                            mouse.wheel(delta=-1)

                        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[4] == 1:
                            mouse.wheel(delta=1)

                        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and double_delay == 0:
                            mouse.double_click(button="left")
                            threading.Thread(target=double_clk_delay).start()

        cv2.imshow("Camera Feed", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

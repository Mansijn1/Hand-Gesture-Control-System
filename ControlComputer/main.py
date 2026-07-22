import cv2
import math
import pyautogui
import time

from core.keyboard import create_keyboard, draw_keyboard  
from pynput.keyboard import Controller as KeyController

from core.hand_tracking import HandTracker
from core.gesture_utils import fingers_up
from controller import Controller


# =========================
# SETUP
# =========================
keyboard = create_keyboard()
keyboard_controller = KeyController()

mouse_click_active = False
key_click_active = False

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

screen_w, screen_h = pyautogui.size()

tracker = HandTracker()
controller = Controller(screen_w, screen_h)


# =========================
# STATE
# =========================
mode = "NORMAL"
typing_mode = False
window_topmost=False

four_timer = 0
thumb_timer = 0
fist_timer = 0

last_screenshot_time = 0
screenshot_delay = 4

last_key_time = 0
key_delay = 0.3

prev_x, prev_y = 0, 0
smoothening = 5


# =========================
# LOOP
# =========================
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)

    lmList, img = tracker.get_landmarks(img)

    if lmList:

        fingers = fingers_up(lmList)

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # Smooth movement
        curr_x, curr_y = x2, y2
        prev_x = prev_x + (curr_x - prev_x) / smoothening
        prev_y = prev_y + (curr_y - prev_y) / smoothening
        x2, y2 = int(prev_x), int(prev_y)

        length = math.hypot(x2 - x1, y2 - y1)
        current_time = time.time()

        # =========================
        # MODE SWITCH
        # =========================

        # Keyboard mode
        if mode == "NORMAL" and fingers == [0,1,1,1,1]:
            if four_timer == 0:
                four_timer = current_time
            elif current_time - four_timer > 1:
                mode = "KEYBOARD"
                four_timer = 0
        else:
            four_timer = 0

        # Exit (fist)
        if fingers == [0,0,0,0,0]:
            if fist_timer == 0:
                fist_timer = current_time
            elif current_time - fist_timer > 0.7:
                mode = "NORMAL"
                typing_mode = False
                fist_timer = 0
        else:
            fist_timer = 0

        # VS Code
        if mode == "NORMAL" and fingers == [1,0,0,0,0]:
            if thumb_timer == 0:
                thumb_timer = current_time
            elif current_time - thumb_timer > 1:
                controller.open_app()
                mode = "VS"
                thumb_timer = 0
        else:
            thumb_timer = 0

        # =========================
        # KEYBOARD MODE
        # =========================
        if mode == "KEYBOARD":

            cv2.putText(img, "KEYBOARD MODE", (40,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

            # TARGETING MODE
            if not typing_mode:

                controller.move_mouse(x2, y2, img.shape)

                cv2.putText(img, "Click to start typing", (40,100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

                if length < 40 and not mouse_click_active:
                    mouse_click_active = True
                    controller.click()
                    typing_mode = True

                elif length > 60:
                    mouse_click_active = False

            # TYPING MODE
            else: 

                img = draw_keyboard(img, keyboard)


                for button in keyboard:
                    x, y = button.pos
                    w, h = button.size

                    if x < x2 < x+w and y < y2 < y+h:

                        # highlight
                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), cv2.FILLED)
                        cv2.putText(img, button.text, (x+10,y+35),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

                        if length < 40:
                            key_click_active = True

                        elif length > 60:
                            if key_click_active:

                                if current_time - last_key_time > key_delay:

                                    key = button.text

                                    if key == "SPACE":
                                        keyboard_controller.press(" ")
                                        keyboard_controller.release(" ")

                                    elif key == "DEL":
                                        keyboard_controller.press("\b")
                                        keyboard_controller.release("\b")

                                    else:
                                        keyboard_controller.press(key.lower())
                                        keyboard_controller.release(key.lower())

                                    last_key_time = current_time

                            key_click_active = False

        # =========================
        # VS MODE
        # =========================
        elif mode == "VS":

            cv2.putText(img, "VS MODE", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            controller.move_mouse(x2, y2, img.shape)

            if length < 50 and not mouse_click_active:
                mouse_click_active = True
                controller.click()

            elif length > 80:
                mouse_click_active = False

        # =========================
        # NORMAL MODE
        # =========================
        else:

            cv2.putText(img, "NORMAL MODE", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            # Mouse
            if fingers[1] == 1:   # index finger up → movement always allowed
            
                controller.move_mouse(x2, y2, img.shape)
            
                pinch_start = 40
                pinch_end = 65
            
                # pinch = click (independent of finger pattern)
                if length < pinch_start and not mouse_click_active:
                    mouse_click_active = True
                    controller.click()
            
                elif length > pinch_end:
                    mouse_click_active = False
            
                cv2.putText(img, "MOUSE", (50,100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Scroll
            elif fingers == [0,1,1,1,0]:

                cv2.putText(img, "SCROLL", (40,100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                if y2 < 200:
                    pyautogui.scroll(40)
                elif y2 > 300:
                    pyautogui.scroll(-40)

            # Brightness
            elif fingers == [0,1,1,0,0]:

                cv2.putText(img, "BRIGHTNESS", (40,100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                brightness_value = int((1 - y2/img.shape[0]) * 100)
                controller.set_brightness(brightness_value)

            # Screenshot
            elif fingers == [1,1,1,1,1]:

                cv2.putText(img, "SCREENSHOT...", (40,100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                if current_time - last_screenshot_time > screenshot_delay:
                    controller.take_screenshot()
                    last_screenshot_time = current_time


    else:
        cv2.putText(img, "NO HAND", (50,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Hand Detection", img)

    # 🔥 APPLY TOPMOST ONLY ONCE (NO LAG)
    if not window_topmost:
        cv2.setWindowProperty("Hand Detection", cv2.WND_PROP_TOPMOST, 1)
        window_topmost = True
    
    time.sleep(0.01)
    
    key = cv2.waitKey(10)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()
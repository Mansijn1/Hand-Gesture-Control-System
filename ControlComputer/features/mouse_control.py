import pyautogui

prev_x, prev_y = 0, 0
smoothening = 4
frameR = 40

def move_mouse(x2, y2, img_shape, screen_w, screen_h, mode):
    global prev_x, prev_y

    screen_x = int((x2 - frameR) * screen_w / (img_shape[1] - 2*frameR) * 1.8)
    screen_y = int((y2 - frameR) * screen_h / (img_shape[0] - 2*frameR) * 1.8)

    screen_x = max(0, min(screen_w - 1, screen_x))
    screen_y = max(0, min(screen_h - 1, screen_y))

    curr_x = prev_x + (screen_x - prev_x) / smoothening
    curr_y = prev_y + (screen_y - prev_y) / smoothening

    if mode == "MOUSE":
        pyautogui.moveTo(curr_x, curr_y)
        

    prev_x, prev_y = curr_x, curr_y
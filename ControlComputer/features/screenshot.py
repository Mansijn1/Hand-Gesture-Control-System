import pyautogui
import time

last_time = 0

def take_screenshot():
    global last_time

    current = time.time()

    if current - last_time > 2:
        filename = f"screenshot_{int(current)}.png"
        pyautogui.screenshot(filename)
        print("Saved:", filename)

        last_time = current
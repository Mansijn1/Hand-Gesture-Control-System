import pyautogui

def scroll(y2, mode):
    if mode == "SCROLL":
        if y2 < 200:
            pyautogui.scroll(40)
        elif y2 > 300:
            pyautogui.scroll(-40)
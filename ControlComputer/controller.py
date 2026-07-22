import pyautogui
import time
import os
import subprocess
import screen_brightness_control as sbc

pyautogui.FAILSAFE = False

class Controller:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.prev_x = 0
        self.prev_y = 0
        
        self.smoothening = 5
        self.min_movement_threshold = 3  # minimum pixels to move before updating mouse position

        self.last_click_time = 0
        self.click_delay = 0.3   # slightly faster response

    # =========================
    # 🔥 OPEN APP (IMPROVED)
    # =========================
    def open_app(self):
        try:
            # Better: use system command (works even if path changes)
            subprocess.Popen("code")   # requires VS Code in PATH
            print("VS Code opened")
        except:
            try:
                # fallback (your original path)
                subprocess.Popen(r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                print("VS Code opened (fallback)")
            except:
                print("VS Code not found")

    # =========================
    # 🌞 BRIGHTNESS (SMOOTHED)
    # =========================
    def set_brightness(self, value):
        value = max(0, min(100, int(value)))
        try:
            sbc.set_brightness(value)
        except:
            pass  # avoid crash if brightness control fails

    # =========================
    # 🖱️ MOUSE MOVEMENT (IMPROVED)
    # =========================
    def move_mouse(self, x, y, img_shape):

        # 🔥 Define active region (important!)
        margin_x = 60
        margin_y = 60
    
        # Clamp hand movement inside active region
        x = max(margin_x, min(img_shape[1] - margin_x, x))
        y = max(margin_y, min(img_shape[0] - margin_y, y))
    
        # Map ONLY active region → full screen
        screen_x = int((x - margin_x) * self.screen_w / (img_shape[1] - 2 * margin_x))
        screen_y = int((y - margin_y) * self.screen_h / (img_shape[0] - 2 * margin_y))
    
        # Clamp final output
        screen_x = max(0, min(self.screen_w - 1, screen_x))
        screen_y = max(0, min(self.screen_h - 1, screen_y))
    
                # 🔥 IGNORE SMALL JITTERS
        dx = screen_x - self.prev_x
        dy = screen_y - self.prev_y

        if abs(dx) < self.min_movement_threshold and abs(dy) < self.min_movement_threshold:
            return

        # 🔥 DYNAMIC SMOOTHING (VERY IMPORTANT)
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 20:
            smooth_factor = 8
        elif distance < 50:
            smooth_factor = 5
        else:
            smooth_factor = 3

        curr_x = self.prev_x + dx / smooth_factor
        curr_y = self.prev_y + dy / smooth_factor

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x, self.prev_y = curr_x, curr_y

    # =========================
    # 🔽 SCROLL (CONTROLLED)
    # =========================
    def scroll(self, direction):
        pyautogui.scroll(direction)

    # =========================
    # 🖱️ SAFE CLICK (NEW)
    # =========================
    def click(self):
        current_time = time.time()

        if current_time - self.last_click_time > self.click_delay:
            pyautogui.click()
            self.last_click_time = current_time

    # =========================
    # 📸 SCREENSHOT
    # =========================
    def take_screenshot(self):
        os.makedirs("Screenshots", exist_ok=True)
        filename = f"Screenshots/screenshot_{int(time.time())}.png"
        img = pyautogui.screenshot()
        img.save(filename)
        print("Saved:", filename)
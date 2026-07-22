import cv2

class Button:
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.text = text
        self.size = size

def create_keyboard():
    keys = [
        ["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M"],
        ["SPACE", "DEL"]
    ]

    buttonList = []

    for i in range(len(keys)):
        x_offset = 20   # ✅ SHIFT LEFT (was 50)

        for j, key in enumerate(keys[i]):

            # ✅ SMALLER KEYS
            w, h = 50, 50

            if key == "SPACE":
                w = 260   # reduced from 300
            elif key == "DEL":
                w = 80    # reduced from 100

            # ✅ LESS GAP
            buttonList.append(Button([x_offset, 65*i+50], key, [w, h]))

            x_offset += w + 8   # smaller spacing (was 10)

    return buttonList

def draw_keyboard(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        cv2.rectangle(img, (x,y), (x+w, y+h), (180,0,255), cv2.FILLED)

        #Better text for space

        display_text = "SPACE" if button.text == "SPACE" else button.text

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2
        
        (text_w, text_h), _ = cv2.getTextSize(display_text, font, font_scale, thickness)
        
        text_x = x + (w - text_w) // 2
        text_y = y + (h + text_h) // 2
        
        cv2.putText(img, display_text, (text_x, text_y),
                    font, font_scale, (255,255,255), thickness)


    return img

def get_clicked_key(buttonList, x, y):
    for button in buttonList:
        bx, by = button.pos
        bw, bh = button.size

        if bx < x < bx + bw and by < y < by + bh:
            return button.text

    return None
def get_mode(fingers):
    total = fingers.count(1)

    if total >= 4:
        return "MOUSE"

    elif fingers[1] == 1 and fingers[2] == 1:
        return "SCROLL"

    elif fingers[0] == 1 and total == 1:
        return "SCREENSHOT"

    elif total == 0:
        return "IDLE"

    return "IDLE"
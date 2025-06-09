
import cv2
import numpy as np
import pyautogui

def detect_image_on_screen(template_path, threshold=0.8):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    template = cv2.imread(template_path)
    if template is None:
        return None

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    points = list(zip(*locations[::-1]))
    if points:
        return points[0]
    return None

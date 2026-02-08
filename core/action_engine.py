import pyautogui
import time
import pygetwindow as gw

pyautogui.FAILSAFE = True

def focus(app_name):
    windows = gw.getWindowsWithTitle(app_name)
    if windows:
        windows[0].activate()
        time.sleep(0.6)
        return True
    return False

pyautogui.FAILSAFE = False

def move(x, y, duration=0.12):
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)

def click(x, y):
    pyautogui.moveTo(x, y, duration=0.1, tween=pyautogui.easeOutQuad)
    pyautogui.click()


def type_text(text):
    pyautogui.write(text, interval=0.04)

def press(key):
    pyautogui.press(key)

def hotkey(*keys):
    pyautogui.hotkey(*keys)

def wait(seconds):
    time.sleep(seconds)

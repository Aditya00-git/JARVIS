import pyautogui
import time
import pygetwindow as gw

pyautogui.FAILSAFE = True

def focus_window(name):
    windows = gw.getWindowsWithTitle(name)
    if windows:
        windows[0].activate()
        time.sleep(0.5)
        return True
    return False

def type_text(text):
    pyautogui.write(text, interval=0.05)

def press_enter():
    pyautogui.press("enter")

import pyautogui
import pyperclip
import time
import win32gui


# -------------------------
# ACTIVE WINDOW NAME
# -------------------------
def get_active_app():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)

    if not title:
        return "unknown"

    return title


# -------------------------
# COPY SELECTED TEXT
# -------------------------
def copy_selected_text():
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.15)

    text = pyperclip.paste()
    return text.strip()


# -------------------------
# READ SELECTED TEXT
# -------------------------
def read_selected_text():
    text = copy_selected_text()
    return text if text else None
def get_clipboard():
    return pyperclip.paste().strip()


def paste_clipboard():
    pyautogui.hotkey("ctrl", "v")


# -------------------------
# WINDOW CONTROL
# -------------------------
def minimize_window():
    pyautogui.hotkey("win", "down")


def maximize_window():
    pyautogui.hotkey("win", "up")


def close_window():
    pyautogui.hotkey("alt", "f4")


def switch_window():
    pyautogui.hotkey("alt", "tab")


# -------------------------
# SCREENSHOT
# -------------------------
def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot(filename)
    return filename


# -------------------------
# SCROLL
# -------------------------
def scroll_down():
    pyautogui.scroll(-600)


def scroll_up():
    pyautogui.scroll(600)
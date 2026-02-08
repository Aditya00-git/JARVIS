import time
import pyautogui
from core.actions import focus_window, type_text, press_enter

def send_whatsapp_message(contact, message):
    if not focus_window("WhatsApp"):
        return False

    time.sleep(0.5)

    # Click search box (adjust once if needed)
    pyautogui.hotkey("ctrl", "f")
    type_text(contact)
    time.sleep(0.5)
    press_enter()

    time.sleep(0.8)
    type_text(message)
    press_enter()

    return True

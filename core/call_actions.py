import pyautogui
import time
import threading
from core.app_launcher import open_app_by_name
from core.screen_awareness import get_active_app
CALL_MENU = (1683, 79)     
VOICE_CALL = (1426, 233) 
VIDEO_CALL = (1659,239)   
AUTO_ANSWER_DELAY = 10   # seconds
watcher_running = True
def whatsapp_voice_call():
    pyautogui.FAILSAFE = False
    time.sleep(2)
    pyautogui.moveTo(1683, 79, duration=0.2)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(1426, 233, duration=0.2)
    pyautogui.click()
def whatsapp_video_call():
    pyautogui.FAILSAFE = False
    time.sleep(1)
    pyautogui.moveTo(1683, 79, duration=0.2)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(1659, 239, duration=0.2)
    pyautogui.click()
def detect_accept():
    if "WhatsApp" not in get_active_app():
        return None
    try:
        return pyautogui.locateOnScreen(
            "accept_call.png",
            confidence=0.65,
            grayscale=True
        )
    except:
        return None
def click_accept():
    loc = detect_accept()
    if loc:
        x, y = pyautogui.center(loc)
        pyautogui.moveTo(x,y,duration=0.2)
        pyautogui.click(x,y)
        return True
    return False
def whatsapp_answer_call():
    open_app_by_name("whatsapp")
    time.sleep(0.5)
    loc = detect_accept()
    if loc:
        x, y = pyautogui.center(loc)
        pyautogui.moveTo(x,y,duration=0.2)
        pyautogui.click(x, y)
def call_watcher():
    while watcher_running:
        try:
            loc = detect_accept()
            if loc:
                start = time.time()
                while time.time() - start < AUTO_ANSWER_DELAY:
                    time.sleep(0.5)
                    if not detect_accept():
                        break
                if detect_accept():
                    click_accept()
                else:
                    click_decline()
            time.sleep(1)
        except Exception as e:
            print("Call watcher error:", e)
            time.sleep(1)
def detect_decline():
    if "WhatsApp" not in get_active_app():
        return None
    try:
        return pyautogui.locateOnScreen(
            "decline_call.png",
            confidence=0.65,
            grayscale=True
        )
    except:
        return None
def click_decline():
    loc = detect_decline()
    if loc:
        x, y = pyautogui.center(loc)
        pyautogui.click(x, y)
        return True
    return False
def whatsapp_cut_call():
    open_app_by_name("whatsapp")
    time.sleep(0.4)
    click_decline()

def detect_mute():
    if "WhatsApp" not in get_active_app():
        return None
    try:
        return pyautogui.locateOnScreen(
            "mute_call.png",
            confidence=0.65,
            grayscale=True
        )
    except:
        return None


def detect_end():
    if "WhatsApp" not in get_active_app():
        return None
    try:
        return pyautogui.locateOnScreen(
            "end_call.png",
            confidence=0.65,
            grayscale=True
        )
    except:
        return None


def whatsapp_mute_call():
    open_app_by_name("whatsapp")
    time.sleep(0.4)

    loc = detect_mute()
    if loc:
        pyautogui.click(pyautogui.center(loc))
        print("CALL MUTED")


def whatsapp_end_call():
    open_app_by_name("whatsapp")
    time.sleep(0.4)

    loc = detect_end()
    if loc:
        pyautogui.click(pyautogui.center(loc))
        print("CALL ENDED")
def start_call_watcher():
    t = threading.Thread(target=call_watcher, daemon=True)
    t.start()
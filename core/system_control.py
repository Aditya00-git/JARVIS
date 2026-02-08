import os
import keyboard
import screen_brightness_control as sbc


# ---------- VOLUME ----------
def volume_up():
    keyboard.send("volume up")


def volume_down():
    keyboard.send("volume down")


def mute():
    keyboard.send("volume mute")


# ---------- BRIGHTNESS ----------
def brightness_up():
    try:
        sbc.set_brightness("+10")
    except:
        pass


def brightness_down():
    try:
        sbc.set_brightness("-10")
    except:
        pass


# ---------- POWER ----------
def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")


def sleep_pc():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def shutdown_pc():
    os.system("shutdown /s /t 1")


def restart_pc():
    os.system("shutdown /r /t 1")


# ---------- WIFI (toggle airplane quick hack) ----------
def toggle_wifi():
    keyboard.send("win+a")  # quick settings

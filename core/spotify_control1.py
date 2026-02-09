import keyboard
import time
from core.app_launcher import open_app_by_name


def play_song(song):
    open_app_by_name("spotify")

    time.sleep(2)   

    keyboard.send("ctrl+l")
    time.sleep(0.3)

    keyboard.write(song)
    time.sleep(0.3)

    keyboard.send("enter")   
    time.sleep(0.7)

    keyboard.send("tab")     
    time.sleep(0.2)

    keyboard.send("enter")
    time.sleep(0.5)
    keyboard.send("enter")   

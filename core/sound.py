import os
import winsound

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

def play_sound(name):
    path = os.path.join(SOUND_DIR, name)
    if os.path.exists(path):
        winsound.PlaySound(path, winsound.SND_FILENAME)

import subprocess
import time
import pyautogui
from core.speaker import jarvis_say


SPOTIFY_URI = r'explorer shell:AppsFolder\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify'


# ---------------------------
# OPEN SPOTIFY (SAFE)
# ---------------------------
def open_spotify():
    jarvis_say("Opening Spotify")

    # 🔥 SAFE launch (no encoding / no charmap crash)
    subprocess.Popen(
        SPOTIFY_URI,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    time.sleep(3)


# ---------------------------
# MEDIA CONTROLS
# ---------------------------
def play_pause():
    pyautogui.press("playpause")
    jarvis_say("Toggled playback")


def next_song():
    pyautogui.press("nexttrack")
    jarvis_say("Next song")


def previous_song():
    pyautogui.press("prevtrack")
    jarvis_say("Previous song")

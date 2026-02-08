import os
from core.speaker import speak

def open_app(command):

    if "chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "spotify" in command:
        speak("Opening Spotify")
        os.system("start spotify")

    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("start notepad")

    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("start calc")

    elif "explorer" in command:
        speak("Opening File Explorer")
        os.system("start explorer")

    else:
        speak(f"Opening {command.replace('open', '')}")
        os.system(f"start {command.replace('open', '').strip()}")


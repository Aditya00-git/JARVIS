import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from core.state import listening, running
from core.speaker import speak

def create_icon():
    image = Image.new('RGB', (64, 64), 'black')
    d = ImageDraw.Draw(image)
    d.ellipse((8, 8, 56, 56), outline='cyan', width=4)
    return image

def on_start(icon, item):
    import core.state
    core.state.listening = True
    speak("Listening resumed")

def on_pause(icon, item):
    import core.state
    core.state.listening = False
    speak("Listening paused")

def on_exit(icon, item):
    import core.state
    core.state.running = False
    speak("Jarvis shutting down")
    icon.stop()

def run_tray():
    icon = pystray.Icon(
        "Jarvis",
        create_icon(),
        menu=pystray.Menu(
            item("Start Listening", on_start),
            item("Pause Listening", on_pause),
            item("Exit", on_exit)
        )
    )
    icon.run()

import pyttsx3

# UI reference will be injected later
_ui = None

def set_ui(ui):
    global _ui
    _ui = ui

def jarvis_say(text):
    print(f"Jarvis: {text}")

    if _ui:
        _ui.state_signal.emit("speaking")

    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

    if _ui:
        _ui.state_signal.emit("idle")

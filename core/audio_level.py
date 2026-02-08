import sounddevice as sd
import numpy as np

audio_level = 0.0

def audio_callback(indata, frames, time, status):
    global audio_level
    volume_norm = np.linalg.norm(indata) * 10
    audio_level = min(volume_norm, 1.5)

def start_audio_listener():
    stream = sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=16000
    )
    stream.start()

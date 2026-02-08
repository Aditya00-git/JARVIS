import pyaudio
import struct
import math
import threading


class AudioLevel:
    def __init__(self):
        self.level = 0
        self.running = True

        self.pa = pyaudio.PyAudio()

        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=512
        )

        # ⭐ start background reader thread
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    # ⭐ background mic loop
    def _loop(self):
        while self.running:
            try:
                data = self.stream.read(512, exception_on_overflow=False)
                samples = struct.unpack(str(len(data)//2) + "h", data)

                rms = math.sqrt(sum(s*s for s in samples) / len(samples))

                self.level = min(rms / 2000.0, 1.0)

            except:
                self.level = 0

    # ⭐ UI only reads cached value (NO mic read here)
    def read(self):
        return self.level


audio_level = AudioLevel()

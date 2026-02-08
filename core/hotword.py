import pvporcupine
import pyaudio
import struct
import time
class HotwordDetector:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keywords=["jarvis"]
        )
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        self.should_stop = False
    def start(self):
        if self.running:
            return
        self.stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        self.running = True
    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.running = False
    def wait(self):
        self.start()

        while self.running:
            time.sleep(0.005)   # ⭐ prevent CPU spike

            pcm = self.stream.read(
                self.porcupine.frame_length,
                exception_on_overflow=False
            )

            pcm = struct.unpack_from(
                "h" * self.porcupine.frame_length,
                pcm
            )

            if self.porcupine.process(pcm) >= 0:
                self.stop()
                return

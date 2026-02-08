import requests
import threading
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QColor, QFont
from ui.glow import add_glow


CYAN = QColor(0, 220, 255)


class WeatherWidget:
    def __init__(self, scene, x, y):
        self.text = QGraphicsTextItem("WEATHER --")
        self.text.setDefaultTextColor(CYAN)

        # 🔥 bigger + premium font
        self.text.setFont(QFont("Consolas", 18))

        self.text.setPos(x, y)
        scene.addItem(self.text)

        add_glow(self.text, 35)

        self.cached = "--"
        self.condition = "clear"

        self.start_worker()

    # background thread (no lag)
    def start_worker(self):
        def worker():
            while True:
                try:
                    url = (
                        "https://api.open-meteo.com/v1/forecast"
                        "?latitude=19.07&longitude=72.87"
                        "&current_weather=true"
                    )

                    r = requests.get(url, timeout=4).json()

                    temp = r["current_weather"]["temperature"]
                    code = r["current_weather"]["weathercode"]

                    self.cached = f"{temp}°C"

                    # simple condition mapping
                    if code < 3:
                        self.condition = "CLEAR"
                    elif code < 60:
                        self.condition = "CLOUDY"
                    else:
                        self.condition = "RAIN"

                except:
                    self.cached = "--"
                    self.condition = "N/A"

                import time
                time.sleep(600)

        threading.Thread(target=worker, daemon=True).start()

    def update(self):
        self.text.setPlainText(f"{self.cached}  {self.condition}")

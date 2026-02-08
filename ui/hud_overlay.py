import psutil, datetime
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QGraphicsTextItem
from core.spotify_nowplaying import SpotifyWatcher
from ui.widgets_panel import Panel
from ui.widgets_weather import WeatherWidget
from ui.widgets_network import NetworkWidget
from ui.widgets_now_playing import NowPlayingWidget

CYAN = QColor(0, 220, 255)


class HudOverlay:
    def __init__(self, scene):
        rect = scene.sceneRect()

        # 🔥 BIG CLOCK
        self.clock = QGraphicsTextItem("")
        self.clock.setDefaultTextColor(CYAN)
        self.clock.setFont(QFont("Consolas", 38))
        self.clock.setPos(rect.width()/2-120, 20)
        scene.addItem(self.clock)

        # 🔥 PANELS
        self.cpu = Panel(scene, 60, 150, 200, 90, "CPU")
        self.battery = Panel(scene, rect.width()-260, 150, 200, 90, "BAT")
        self.now_playing = NowPlayingWidget(
            scene,
            rect.width()/2 - 190,
            rect.height() - 120
)
        
        self.weather = WeatherWidget(scene, 80, rect.height()-120)
        self.network = NetworkWidget(scene, rect.width()-260, rect.height()-120)
        self.spotify = SpotifyWatcher()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def set_state(self, state):
        pass

    def update(self):
        self.clock.setPlainText(datetime.datetime.now().strftime("%H:%M:%S"))

        self.cpu.update(f"{int(psutil.cpu_percent())}%")

        batt = psutil.sensors_battery()
        if batt:
            self.battery.update(f"{batt.percent}%")

        self.weather.update()
        # self.weather_fx.set_condition(self.weather.cached)
        self.network.update()
        title, artist = self.spotify.get_song()
        self.now_playing.set_song(title, artist)


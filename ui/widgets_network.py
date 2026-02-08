import psutil
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QColor, QFont


CYAN = QColor(0, 220, 255)


class NetworkWidget:
    def __init__(self, scene, x, y):
        self.prev = psutil.net_io_counters()

        self.text = QGraphicsTextItem("NET ...")
        self.text.setDefaultTextColor(CYAN)
        self.text.setFont(QFont("Consolas", 10))
        self.text.setPos(x, y)
        scene.addItem(self.text)

    def update(self):
        cur = psutil.net_io_counters()

        down = (cur.bytes_recv - self.prev.bytes_recv)/1024
        up = (cur.bytes_sent - self.prev.bytes_sent)/1024

        self.prev = cur

        self.text.setPlainText(f"↓{int(down)}kB/s  ↑{int(up)}kB/s")

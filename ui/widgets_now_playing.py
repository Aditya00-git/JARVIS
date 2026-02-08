from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QPen, QFont


CYAN = QColor(0, 220, 255)


class NowPlayingWidget:
    def __init__(self, scene, x, y):
        self.box = QGraphicsRectItem(x, y, 380, 60)
        self.box.setPen(QPen(CYAN, 2))
        scene.addItem(self.box)

        self.title = QGraphicsTextItem("Nothing Playing")
        self.title.setDefaultTextColor(CYAN)
        self.title.setFont(QFont("Consolas", 11))
        self.title.setPos(x+10, y+8)
        scene.addItem(self.title)

        self.subtitle = QGraphicsTextItem("")
        self.subtitle.setDefaultTextColor(QColor(0,200,255,120))
        self.subtitle.setFont(QFont("Consolas", 9))
        self.subtitle.setPos(x+10, y+30)
        scene.addItem(self.subtitle)

    def set_song(self, name, artist=""):
        self.title.setPlainText(name)
        self.subtitle.setPlainText(artist)

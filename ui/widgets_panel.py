from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
from ui.glow import add_glow

CYAN = QColor(0, 220, 255)


class Panel:
    def __init__(self, scene, x, y, w, h, title):
        self.box = QGraphicsRectItem(x, y, w, h)
        self.box.setPen(QPen(CYAN, 2))
        self.box.setBrush(QBrush(QColor(0, 40, 60, 60)))  # glass look
        scene.addItem(self.box)

        self.title = QGraphicsTextItem(title)
        self.title.setDefaultTextColor(CYAN)
        self.title.setFont(QFont("Consolas", 10))
        self.title.setPos(x+8, y+5)
        scene.addItem(self.title)

        self.value = QGraphicsTextItem("--")
        self.value.setDefaultTextColor(CYAN)
        self.value.setFont(QFont("Consolas", 22))  # 🔥 BIG
        self.value.setPos(x+12, y+25)
        scene.addItem(self.value)

    def update(self, text):
        self.value.setPlainText(text)

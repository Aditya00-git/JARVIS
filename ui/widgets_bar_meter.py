from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QPen, QBrush, QFont


CYAN = QColor(0, 220, 255)


class BarMeter:
    def __init__(self, scene, x, y, label):
        self.w = 200

        self.bg = QGraphicsRectItem(x, y, self.w, 12)
        self.bg.setPen(QPen(QColor(0,120,150,80), 1))
        scene.addItem(self.bg)

        self.fill = QGraphicsRectItem(x, y, 0, 12)
        self.fill.setBrush(QBrush(CYAN))
        self.fill.setPen(QPen(CYAN, 0))
        scene.addItem(self.fill)

        self.text = QGraphicsTextItem(label)
        self.text.setDefaultTextColor(CYAN)
        self.text.setFont(QFont("Consolas", 9))
        self.text.setPos(x, y-18)
        scene.addItem(self.text)

    def update(self, percent):
        self.fill.setRect(self.bg.rect().x(),
                          self.bg.rect().y(),
                          self.w * percent/100,
                          12)

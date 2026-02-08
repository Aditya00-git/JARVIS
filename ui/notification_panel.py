from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
from PyQt5.QtCore import QTimer
from ui.glow import add_glow


CYAN = QColor(0, 220, 255)


class Notification:
    def __init__(self, scene, x, y, text):
        self.scene = scene
        self.life = 0

        self.box = QGraphicsRectItem(x, y, 320, 45)
        self.box.setPen(QPen(CYAN, 2))
        self.box.setBrush(QBrush(QColor(0, 40, 60, 120)))
        scene.addItem(self.box)

        self.label = QGraphicsTextItem(text)
        self.label.setDefaultTextColor(CYAN)
        self.label.setFont(QFont("Consolas", 10))
        self.label.setPos(x + 12, y + 12)
        scene.addItem(self.label)

        add_glow(self.box, 30)
        add_glow(self.label, 20)

    def step(self):
        self.life += 1
        if self.life > 180:  # ~3 seconds
            self.scene.removeItem(self.box)
            self.scene.removeItem(self.label)
            return False
        return True


class NotificationPanel:
    def __init__(self, scene):
        self.scene = scene
        self.notifications = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def push(self, text):
        rect = self.scene.sceneRect()

        y = rect.height() - 80 - (len(self.notifications) * 55)

        note = Notification(self.scene, rect.width() - 360, y, text)
        self.notifications.append(note)

    def update(self):
        self.notifications = [n for n in self.notifications if n.step()]

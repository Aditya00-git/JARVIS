from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor


def add_glow(item, strength=25):
    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(strength)
    glow.setColor(QColor(0, 220, 255))
    glow.setOffset(0)
    item.setGraphicsEffect(glow)

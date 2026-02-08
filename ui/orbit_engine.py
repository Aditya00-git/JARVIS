from PyQt5.QtWidgets import (
    QGraphicsPathItem,
    QGraphicsLineItem,
    QGraphicsEllipseItem
)
import random
from PyQt5.QtGui import QPen, QColor, QPainterPath, QTransform, QBrush
import random
import time
import math
def lerp(a, b, t):
    return a + (b - a) * t
JARVIS_BLUE = QColor(0, 200, 255)
class OrbitSegment(QGraphicsPathItem):
    def __init__(self, radius, start_angle, span_angle, speed, width, alpha, tilt):
        super().__init__()
        self.radius = radius
        self.angle = start_angle
        self.span = span_angle
        self.speed = speed
        self.base_width = width
        self.base_alpha = alpha
        self.tilt = tilt
        self.pulse = random.random() * 10
        self.pen = QPen()
        self.pen.setCapStyle(1)
        self.setPen(self.pen)
        self.update_path()
    def update_path(self):
        path = QPainterPath()
        path.arcMoveTo(
            -self.radius, -self.radius,
            self.radius * 2, self.radius * 2,
            self.angle
        )
        path.arcTo(
            -self.radius, -self.radius,
            self.radius * 2, self.radius * 2,
            self.angle, self.span
        )
        self.setPath(path)
        transform = QTransform()
        transform.scale(1.0, self.tilt)
        self.setTransform(transform)
    def step(self, speed_mul, pulse_strength, color=None):

        self.angle += self.speed * speed_mul
        self.pulse += 0.06

        glow = (math.sin(self.pulse) + 1) / 2

        width = self.base_width + glow * pulse_strength
        alpha = self.base_alpha + glow * 80

        self.pen.setWidthF(width)

        # ⭐ APPLY STATE COLOR SAFELY
        if color:
            r, g, b = color
            self.pen.setColor(QColor(r, g, b, int(alpha)))
        else:
            self.pen.setColor(QColor(0, 200, 255, int(alpha)))

        self.setPen(self.pen)

        self.update_path()
class OrbitTick(QGraphicsLineItem):
    def __init__(self, radius, angle, length, speed, tilt):
        super().__init__()
        self.radius = radius
        self.angle = angle
        self.length = length
        self.speed = speed
        self.tilt = tilt
        pen = QPen(QColor(0, 200, 255, 120))
        pen.setWidth(1)
        self.setPen(pen)
        self.update_line()
    def update_line(self):
        a = math.radians(self.angle)
        x1 = math.cos(a) * self.radius
        y1 = math.sin(a) * self.radius * self.tilt
        x2 = math.cos(a) * (self.radius + self.length)
        y2 = math.sin(a) * (self.radius + self.length) * self.tilt
        self.setLine(x1, y1, x2, y2)
    def step(self):
        self.angle += self.speed
        self.update_line()
class OrbitDot(QGraphicsEllipseItem):
    def __init__(self, radius, angle, size, speed, tilt):
        super().__init__(-size / 2, -size / 2, size, size)
        self.radius = radius
        self.angle = angle
        self.speed = speed
        self.tilt = tilt
        self.setBrush(QColor(0, 200, 255, 140))
        self.update_pos()
    def update_pos(self):
        a = math.radians(self.angle)
        x = math.cos(a) * self.radius
        y = math.sin(a) * self.radius * self.tilt
        self.setPos(x, y)
    def step(self):
        self.angle += self.speed
        self.update_pos()
class OrbitEngine:
    def __init__(self, scene):
        self.scene = scene
        rect = scene.sceneRect()
        self.cx = rect.width() / 2
        self.cy = rect.height() / 2
        self.audio_level = 0.0
        self.audio_level = 0
        self.segments = []
        self.ticks = []
        self.dots = []
        self.current_speed_mul = 1.0
        self.target_speed_mul = 1.0
        self.current_pulse = 0.4
        self.target_pulse = 0.4
        self.create_ring(120,  4,  0.45, "thin", 0.92)
        self.create_ring(160,  6, -0.35, "thick", 0.88)
        self.create_ring(200,  8,  0.25, "micro", 0.85)
        self.create_ring(240, 10, -0.22, "thin", 0.80)
        self.create_ring(280, 12, 0.18, "thick", 0.75)
        self.create_ring(320, 14, -0.15, "micro", 0.70)
        self.create_ring(360, 16, 0.12, "thin", 0.66)
        self.create_ring(400, 18, -0.10, "thick", 0.62)
        self.create_ticks(300, 28, 0.78)
        self.create_dots(340, 18, 0.74)
        for item in self.segments + self.ticks + self.dots:
            item.setPos(self.cx, self.cy)
            self.scene.addItem(item)
    def create_ring(self, radius, count, speed, style, tilt):
        for _ in range(count):
            start = random.randint(0, 360)
            if style == "thick":
                span = random.randint(35, 70)
                width = random.uniform(3.0, 4.5)
                alpha = 220
            elif style == "thin":
                span = random.randint(20, 50)
                width = random.uniform(1.5, 2.2)
                alpha = 180
            else:
                span = random.randint(10, 25)
                width = random.uniform(1.0, 1.5)
                alpha = 150
            seg = OrbitSegment(radius, start, span, speed, width, alpha, tilt)
            self.segments.append(seg)
    def create_ticks(self, radius, count, tilt):
        for i in range(count):
            angle = i * (360 / count)
            self.ticks.append(OrbitTick(radius, angle, 6, 0.05, tilt))
    def create_dots(self, radius, count, tilt):
        for i in range(count):
            angle = i * (360 / count)
            self.dots.append(OrbitDot(radius, angle, 3, -0.08, tilt))
    def update(self, state):
        speed_mul = 1.0
        pulse = 0.5
        color = (0, 180, 255) 
        if state == "idle":
            speed_mul = 1.0
            pulse = 0.4
            color = (0, 150, 255)      # calm azure blue

        elif state == "listening":
            speed_mul = 2.0
            pulse = 1.0
            color = (0, 255, 230)      # neon cyan (mic active glow)

        elif state == "speaking":
            speed_mul = 3.0
            pulse = 1.5
            color = (120, 240, 255)    # ice blue (voice energy)

        elif state == "thinking":
            speed_mul = 0.7
            pulse = 0.3
            color = (30, 90, 200)  
        elif state=="system":
            speed_mul = 0.6
            pulse = 0.25
        energy = self.audio_level
        if state == "speaking":
            pulse += energy * 2.5
            speed_mul += energy * 1.5
        elif state == "listening":
            pulse += energy * 1.2

        for seg in self.segments:
            seg.step(speed_mul, pulse, color)

        for tick in self.ticks:
            tick.step()
        for dot in self.dots:
            dot.step()
       
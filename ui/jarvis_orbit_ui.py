from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor
import sys
import time
from core.audio_level1 import audio_level
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QTimer
# from core.audio_level import audio_level
from ui.orbit_engine import OrbitEngine
from ui.hud_overlay import HudOverlay
from ui.notification_panel import NotificationPanel
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
class JarvisOrbitUI(QGraphicsView):
    notify_signal = pyqtSignal(str)
    flash_signal = pyqtSignal(tuple)
    scan_show_signal = pyqtSignal(str)
    scan_hide_signal = pyqtSignal()
    state_signal = pyqtSignal(str)   # ⭐ NEW
    close_signal = pyqtSignal()  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        self.showFullScreen()
        self.setWindowFlags(Qt.FramelessWindowHint )
        self.setStyleSheet("background-color: black; border: none;")
        screen = QApplication.primaryScreen().geometry()
        self.scene = QGraphicsScene(0, 0, screen.width(), screen.height())
        self.setSceneRect(self.scene.sceneRect())
        self.setScene(self.scene)
        self.hud = HudOverlay(self.scene)
        self.scan_show_signal.connect(self.show_scan_text)
        self.scan_hide_signal.connect(self.hide_scan_text)  
        self.notify = NotificationPanel(self.scene)
        self.notify_signal.connect(self.notify.push)
        self.engine = OrbitEngine(self.scene)
        self.flash_signal.connect(self._flash_safe)
        self.state = "idle"
        self.current_scale = 1.0
        self.target_scale = 1.0
        # ⭐ scan overlay text
        self.scan_text = QGraphicsTextItem("")
        self.scan_text.setDefaultTextColor(QColor(0, 220, 255))
        self.scan_text.setZValue(999)  # always top

        font = QFont("Consolas", 42, QFont.Bold)
        self.scan_text.setFont(font)
        

        self.scene.addItem(self.scan_text)
        self.scan_text.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33) 
        self.state_signal.connect(self.set_state)
        self.close_signal.connect(self.close) # ~60 FPS
    def show_scan_text(self, text="SYSTEM INITIALIZING..."):
        self.scan_text.setPlainText(text)

        rect = self.scene.sceneRect()
        self.scan_text.setPos(
            rect.width()/2 - self.scan_text.boundingRect().width()/2,
            rect.height()/2 - self.scan_text.boundingRect().height()/2
        )

        self.scan_text.show()


    def hide_scan_text(self):
        self.scan_text.hide()

    def update_frame(self):
        try:
            
            self.engine.audio_level = audio_level.level
            self.engine.update(self.state)
        except Exception as e:
            print(e)
    

    def set_state(self, state):
        self.state = state
        self.hud.set_state(state)
        
        # ---------- FLASH EFFECTS ----------
        if state == "success":
            self.flash((0, 255, 120))   # green

        elif state == "error":
            self.flash((255, 60, 60))   # red

    def notify_msg(self, text):
        self.notify_signal.emit(text)
    def flash(self, color):
    # called from brain thread → emit only
        self.flash_signal.emit(color)
    def _flash_safe(self, color):
        """
        Runs only in UI thread.
        Flickers twice then resets.
        """
        r, g, b = color
        def on():
            self.setStyleSheet(f"background-color: rgba({r},{g},{b},80); border:none;")
        def off():
            self.setStyleSheet("background-color:black; border:none;")
        QTimer.singleShot(0, on)
        QTimer.singleShot(120, off)
        QTimer.singleShot(240, on)
        QTimer.singleShot(360, off)
def run_ui():
    app = QApplication(sys.argv)
    ui = JarvisOrbitUI()
    ui.show()
    sys.exit(app.exec_())
import sys 
import threading 
from PyQt5.QtWidgets import QApplication 
from core.audio_level import start_audio_listener 
from ui.jarvis_orbit_ui import JarvisOrbitUI 
from core.brain1 import run_jarvis 
import os 
os.environ["PYTHONUTF8"] = "1" 
def start_brain(ui): 
	run_jarvis(ui) 
if __name__ == "__main__": 
	# 🔑 QApplication MUST come first 
	app = QApplication(sys.argv) 
	# start_audio_listener() 
	# 🎨 Create UI in main thread 
	ui = JarvisOrbitUI() 
	ui.show() 
	# 🧠 Start brain in background thread
	brain_thread = threading.Thread(
		target=start_brain,
		args=(ui,), 
		daemon=True
	) 
	brain_thread.start()
	sys.exit(app.exec_())
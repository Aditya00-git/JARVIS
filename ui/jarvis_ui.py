import tkinter as tk
import threading
import time

class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis")
        self.root.geometry("300x120")
        self.root.configure(bg="black")
        self.root.overrideredirect(True)  # no title bar
        self.root.attributes("-topmost", True)

        self.label = tk.Label(
            self.root,
            text="Jarvis Online",
            fg="cyan",
            bg="black",
            font=("Segoe UI", 14)
        )
        self.label.pack(expand=True)

        # position bottom-right
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = self.root.winfo_screenwidth() - w - 20
        y = self.root.winfo_screenheight() - h - 60
        self.root.geometry(f"+{x}+{y}")

    def update_text(self, text):
        self.label.config(text=text)
        self.root.update()

    def run(self):
        self.root.mainloop()


ui = JarvisUI()

def start_ui():
    ui.run()

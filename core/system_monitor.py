import threading
import time
import psutil
from core.speaker import jarvis_say


class SystemMonitor:
    def __init__(self):
        self.running = True

        # prevent repeating alerts
        self.cpu_alert = False
        self.ram_alert = False
        self.battery_alert = False
        self.net_alert = False

    # ---------------------

    def check_cpu(self):
        cpu = psutil.cpu_percent()

        if cpu > 90 and not self.cpu_alert:
            jarvis_say("Warning. CPU usage is very high")
            self.cpu_alert = True

        elif cpu < 70:
            self.cpu_alert = False

    # ---------------------

    def check_ram(self):
        ram = psutil.virtual_memory().percent

        if ram > 80 and not self.ram_alert:
            jarvis_say("Memory usage is high")
            self.ram_alert = True

        elif ram < 60:
            self.ram_alert = False

    # ---------------------

    def check_battery(self):
        battery = psutil.sensors_battery()

        if battery is None:
            return

        percent = battery.percent

        if percent < 20 and not self.battery_alert:
            jarvis_say("Battery is low")
            self.battery_alert = True

        elif percent > 30:
            self.battery_alert = False

    # ---------------------

    def check_network(self):
        try:
            online = psutil.net_if_stats()

            connected = any(v.isup for v in online.values())

            if not connected and not self.net_alert:
                jarvis_say("Internet disconnected")
                self.net_alert = True

            elif connected:
                self.net_alert = False

        except:
            pass

    # ---------------------

    def loop(self):
        while self.running:
            try:
                self.check_cpu()
                self.check_ram()
                self.check_battery()
                self.check_network()

                time.sleep(12)  # check every 12 sec

            except Exception as e:
                print("Monitor error:", e)
                time.sleep(5)


# ---------------------

def start_system_monitor():
    monitor = SystemMonitor()
    t = threading.Thread(target=monitor.loop, daemon=True)
    t.start()

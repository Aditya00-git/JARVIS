import psutil
import socket


def system_scan():

    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent

    try:
        battery = psutil.sensors_battery().percent
    except:
        battery = None

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        net = "Connected"
    except:
        net = "Offline"

    return {
        "cpu": int(cpu),
        "ram": int(ram),
        "battery": battery,
        "network": net
    }

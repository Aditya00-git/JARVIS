import psutil

for proc in psutil.process_iter(['pid', 'name']):
    if proc.info['name'] == 'pythonw.exe':
        proc.kill()

import subprocess
from core.speaker import jarvis_say

def open_app_by_name(app_name):
    ps_command = f'''
    $app = Get-StartApps |
           Where-Object {{$_.Name -like "*{app_name}*"}} |
           Select-Object -First 1

    if ($app) {{
        Start-Process explorer ("shell:AppsFolder\\" + $app.AppID)
    }}
    '''
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_command],
        capture_output=True
    )
    jarvis_say(f"Opening {app_name}")

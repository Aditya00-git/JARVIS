import subprocess

def get_apps():
    command = """
    powershell -command "
    Get-StartApps | Select-Object Name, AppID
    "
    """
    result = subprocess.check_output(command, shell=True, text=True)
    return result

import shutil
import subprocess
import sys

def open_app(app_name: str):
    app = app_name.strip().lower()
    if sys.platform.startswith("win"):
        command = {"chrome": ["start", "chrome"], "notepad": ["notepad"], "code": ["code"]}.get(app, ["start", app])
        subprocess.Popen(command, shell=command[0] == "start")
    elif sys.platform == "darwin":
        subprocess.Popen(["open", "-a", app_name])
    else:
        executable = shutil.which(app) or app
        subprocess.Popen([executable])

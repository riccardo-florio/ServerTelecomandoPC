# startup_manager.py

import os
import sys
import win32com.client
from constants import STARTUP_SHORTCUT_NAME

def is_in_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, STARTUP_SHORTCUT_NAME)
    return os.path.exists(shortcut_path)

def add_to_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_path = sys.argv[0]
    shortcut_path = os.path.join(startup_folder, STARTUP_SHORTCUT_NAME)
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    if getattr(sys, 'frozen', False):
        # Eseguibile
        target = sys.executable
    else:
        # Script
        target = sys.executable
    shortcut.Targetpath = target
    shortcut.Arguments = f'"{os.path.abspath(script_path)}" --minimized'
    shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(script_path))
    shortcut.IconLocation = target
    shortcut.save()

def remove_from_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, STARTUP_SHORTCUT_NAME)
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)

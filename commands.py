# commands.py

import subprocess
import pyautogui
import comtypes
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def volume_up():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(currentVolumeDb + 2.0, None)

def volume_down():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(currentVolumeDb - 2.0, None)

def move_left():
    pyautogui.press('left')

def move_right():
    pyautogui.press('right')

def move_up():
    pyautogui.press('up')

def move_down():
    pyautogui.press('down')

def play_pause():
    pyautogui.press('playpause')

def power_off():
    subprocess.call("shutdown /s /t 60", shell=True)
    return 'Il computer si spegnerà tra 60 secondi.'

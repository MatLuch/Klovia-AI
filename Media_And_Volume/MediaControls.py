from pycaw.pycaw import AudioUtilities
import pyautogui

vol = AudioUtilities.GetSpeakers().EndpointVolume

def Mute(): 
    vol.setMute(1, None)

def Unmute():
    vol.setMute(0, None)

def Media_Control(action):
    if action in ['playpause', 'next', 'prev']:
        pyautogui.press(action + 'track' if action != 'playpause' else 'playpause')
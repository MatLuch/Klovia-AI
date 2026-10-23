from pycaw.pycaw import AudioUtilities
import pyautogui

vol = AudioUtilities.GetSpeakers().EndpointVolume

def Mute(): 
    try:
        vol.setMute(1, None)
    except Exception:
        return None 
    
def Unmute():
    try:
        vol.setMute(0, None)
    except Exception:
        return None
    
def Play_Pause():
    try: 
        pyautogui.press('playpause')
    except Exception:
        return None
    
def Next_Track():
    try:
        pyautogui.press('nexttrack')
    except Exception:
        return None
    
def Prev_Track():
    try:
        pyautogui.press('prevtrack')
    except Exception:
        return None
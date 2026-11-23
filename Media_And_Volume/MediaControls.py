from pycaw.pycaw import AudioUtilities
import pyautogui

# Creates a control object for the computers primary audio
vol = AudioUtilities.GetSpeakers().EndpointVolume

# Function to Mute the audio
def Mute(): 
    try:
        vol.SetMute(1, None)
    except Exception:
        return None 

# Function to Unmute the audio 
def Unmute():
    try:
        vol.SetMute(0, None)
    except Exception:
        return None

# Function to play or pause the audio 
def Play_Pause():
    try: 
        pyautogui.press('playpause')
    except Exception:
        return None

# Function to go to the next track
def Next_Track():
    try:
        pyautogui.press('nexttrack')
    except Exception:
        return None

# Functi to go to the last track
def Prev_Track():
    try:
        pyautogui.press('prevtrack')
    except Exception:
        return None
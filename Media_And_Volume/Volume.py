from pycaw.pycaw import AudioUtilities

# Creates a control object for the computers primary audio
vol = AudioUtilities.GetSpeakers().EndpointVolume

# Function to set the volume to a exact ammount 
def Set_Volume(input):
    try: 
        input /= 100  

        vol.SetMasterVolumeLevelScalar(input, None)  

    except Exception:
        return None

# Function to Increase the volume to a exact ammount
def Increase_Volume(input):
    try: 
        currVolume = vol.GetMasterVolumeLevelScalar() * 100
        NewPrecent = currVolume + float(input)

        vol.SetMasterVolumeLevelScalar(NewPrecent / 100.0, None) 

    except Exception: 
        return None 

# Function to Decrease the volume by a exact ammount 
def Decrease_Volume(input):
    try: 
        currVolume = vol.GetMasterVolumeLevelScalar() * 100
        NewPrecent = currVolume - float(input)

        vol.SetMasterVolumeLevelScalar(NewPrecent / 100.0, None) 

    except Exception:
        return None 
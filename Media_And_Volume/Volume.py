from pycaw.pycaw import AudioUtilities

vol = AudioUtilities.GetSpeakers().EndpointVolume

def Set_Volume(input):
    input /= 100  

    vol.SetMasterVolumeLevelScalar(input, None)  

def Change_Volume(input): 
    CurrVolume = vol.GetMasterVolumeLevelScalar() * 100
    NewPercent = max(0, min(100, CurrVolume + input))
    
    vol.SetMasterVolumeLevelScalar(NewPercent / 100.0, None)
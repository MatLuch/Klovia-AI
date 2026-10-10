from pycaw.pycaw import AudioUtilities

vol = AudioUtilities.GetSpeakers().EndpointVolume

def Set_Volume(input):
    input /= 100  
    vol.SetMasterVolumeLevelScalar(input, None)  
from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import *
from Media_And_Volume.Brightness import * 
from AI_Training.Run1 import GeneralModelAnswer
from Tools.numberLocator import numLocate

command_map = {
    "VolumeUp": lambda: Increase_Volume(loc),
    "VolumeDown": lambda: Decrease_Volume(loc),
    "SetVolume" : lambda : Set_Volume(loc),
    "BrightnessUp" : lambda : Increase_Brightness(loc), 
    "BrightnessDown" : lambda : Decrease_Brightness(loc),
    "SetBrightness" : lambda : Set_Brightness(loc), 
    "PlayPause": Play_Pause,
    "NextSong": Next_Track,
    "PrevSong": Prev_Track,
    "Mute": Mute,
    "Unmute": Unmute
}

text = ""

while True:
    text = input("Enter the text you wish to send: ").strip()
    if text in ("-1", "stop"): break

    out = GeneralModelAnswer(text)
    loc = numLocate(text)

    print("the model said:", out)
    print("The number found is:", loc)

    if out in command_map:
        command_map[out]()
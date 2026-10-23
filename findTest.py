from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import * 
from AI_Training.TestRun2 import ModelAnswer

command_map = {
    "VolumeUp": Increase_Volume,
    "VolumeDown" : Decrease_Volume,
    "PlayPause" : Play_Pause,
    "NextSong" : Next_Track,
    "PrevSong" : Prev_Track
}

while True:
    
    text = input("Enter your text: ")
    if text == "exit":
        break 

    out = ModelAnswer(text)

    if out in command_map: 
        command_map[out]()
    else:
        print("Command not found")
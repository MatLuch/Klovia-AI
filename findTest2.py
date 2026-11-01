from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import *
from AI_Training.Run1 import ModelAnswer

command_map = {
    "VolumeUp": lambda: Increase_Volume(text),
    "VolumeDown": lambda: Decrease_Volume(text),
    "PlayPause": Play_Pause,
    "NextSong": Next_Track,
    "PrevSong": Prev_Track,
    "Mute": Mute,
    "Unmute": Unmute
}

while True:
    text = input("Enter your text: ").strip()

    if text.lower() == "exit":
        break

    out = ModelAnswer(text)
    print("Detected command:", out)

    if out in command_map:
        command_map[out]()
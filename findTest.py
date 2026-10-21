from Media_And_Volume.Volume import *
from AI_Training.TestRun2 import ModelAnswer

command_map = {
    "volumeUp": Increase_Volume,
    "volumeDown" : Decrease_Volume
}

while True:
    
    text = input("Enter your text: ")
    if text == "exit":
        break 

    out = ModelAnswer(text)

    if out in command_map: 
        command_map[out](10) # will execute function directly 
    else:
        print("Command not found")
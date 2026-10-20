from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import * 

x = "hello"

while x != "-1": 
    x = input("chose how to set your volume: ")

    Media_Control(x)

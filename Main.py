# Imports and setup 
import speech_recognition as sr
from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import *
from Media_And_Volume.Brightness import * 
from AI_Training.Run1 import GeneralModelAnswer
from Tools.numberLocator import numLocate
recognizer = sr.Recognizer()

# Command map the AI uses to call functions
command_map = {
    "VolumeUp": lambda: Increase_Volume(amount),
    "VolumeDown": lambda: Decrease_Volume(amount),
    "SetVolume" : lambda : Set_Volume(amount),
    "IncreaseBrightness" : lambda : Increase_Brightness(amount), 
    "DecreaseBrightness" : lambda : Decrease_Brightness(amount),
    "SetBrightness" : lambda : Set_Brightness(amount), 
    "PlayPause": Play_Pause,
    "NextSong": Next_Track,
    "PrevSong": Prev_Track,
    "Mute": Mute,
    "Unmute": Unmute
}


# Microphone setup
with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1) # Samples audio to measure how loud the room is and set a loudness threshold

    # Listening and turning speech into text
    while True:
        print("Klovia is waiting for you too speak: ")

        try:
            audio = recognizer.listen(source, phrase_time_limit=15) # Uses the loudness threshold and, listends until you pause long enough or hit 15 seconds of speaking 

            print("Recognizing...")
            text = recognizer.recognize_google(audio) # Sends audio to google to get turned into text 

            out = GeneralModelAnswer(text) # Variable for the model text 
            amount = numLocate(text) # Variable for the first found number/s

            print("You said:", text, "\n")

            # Runs the command if in command map
            if out in command_map: 
                command_map[out]() # Klovia then runs the commands
                print("Detected command:" , out)
                print("Detected number:", amount)

        # Error handling and stopping Klovia
        except sr.UnknownValueError: # Speech recognizer couldn't turn audio into text 
            print("Didn't catch that. Try again.")

        except sr.RequestError as e: # Means the google speech request failed
            print("Speech service error:", e)

        except KeyboardInterrupt: # When you interupt with the keyboard
            print("Voice input stopped.")
            break
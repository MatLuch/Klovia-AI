import speech_recognition as sr
from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import *
from AI_Training.Run1 import ModelAnswer
from Tools.numberLocator import numLocate
recognizer = sr.Recognizer()

command_map = {
    "VolumeUp": lambda: Increase_Volume(amount),
    "VolumeDown": lambda: Decrease_Volume(amount),
    "PlayPause": Play_Pause,
    "NextSong": Next_Track,
    "PrevSong": Prev_Track,
    "Mute": Mute,
    "Unmute": Unmute
}

with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:

        print("Klovia is waiting for you too speak: ")

        try:
            audio = recognizer.listen(source, phrase_time_limit=15)

            print("Recognizing...")
            text = recognizer.recognize_google(audio)

            out = ModelAnswer(text)
            amount = numLocate(text)

            print("You said:", text, "\n")

            if out in command_map: 
                command_map[out]()
                print("Detected command:" , out)
                print("Detected number:", amount)

        except sr.UnknownValueError:
            print("Didn't catch that. Try again.")

        except sr.RequestError as e:
            print("Speech service error:", e)

        except KeyboardInterrupt:
            print("Voice input stopped.")
            break
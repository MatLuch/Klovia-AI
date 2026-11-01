import speech_recognition as sr
from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import *
from AI_Training.Run1 import ModelAnswer

recognizer = sr.Recognizer()

command_map = {
    "VolumeUp": lambda: Increase_Volume(text),
    "VolumeDown": lambda: Decrease_Volume(text),
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
            print("You said:", text, "\n")

            if out in command_map: 
                command_map[out]()
                print("Detected command: ", out, "\n")

        except sr.UnknownValueError:
            print("Didn't catch that. Try again.")

        except sr.RequestError as e:
            print("Speech service error:", e)

        except KeyboardInterrupt:
            print("Voice input stopped.")
            break
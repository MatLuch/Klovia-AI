import speech_recognition as sr
from Media_And_Volume.Volume import *
from Media_And_Volume.MediaControls import *
from AI_Training.Run1 import ModelAnswer

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:

        print("Klovia is waiting for you too speak: ")

        try:
            audio = recognizer.listen(source, phrase_time_limit=15)

            print("Recognizing...")
            text = recognizer.recognize_google(audio)

            print("You said:", text, "\n")

        except sr.UnknownValueError:
            print("Didn't catch that. Try again.")

        except sr.RequestError as e:
            print("Speech service error:", e)

        except KeyboardInterrupt:
            print("Voice input stopped.")
            break
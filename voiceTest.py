import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

print("Klovia is listening. Speak anytime!")

while True:
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, phrase_time_limit=15)

        print("Recognizing...")

        text = recognizer.recognize_google(audio)

        print("You said:", text)

    except sr.UnknownValueError:
        print("Didn't catch that. Try again.")

    except sr.RequestError as e:
        print("Speech service error:", e)

    except KeyboardInterrupt:
        print("Voice input stopped.")
        break
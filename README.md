                    # Klovia

Klovia is a Python voice assistant for Windows. I want to be able to control my laptop with my voice such as music, windows, apps and more. It’s still a work in progress, but it can already play or pause music, skip songs, go back a track, mute or unmute, and change the system volume.

## stuff you can say

- “Pause the music” or “resume the music”
- “Skip this song” or “go back one track”
- “Mute the audio” or “unmute the audio”
- “Turn the volume up by 10” or “turn the volume down by 5”

For volume changes, Klovia looks for a number written as digits in the transcript. If your volume is at 30 and it hears “turn it up by 10,” it goes to 40.

Play and pause use the same media key, so what happens depends on whether music is already playing. The track controls work with apps that respond to Windows media keys. Mute and unmute also affect any other sound coming through the same audio device.

## how the local AI works

Klovia uses Google speech recognition to turn audio into text. Then a ultra small PyTorch model runs on my computer and figures out which command I meant. I train it on example phrases from a JSON file, so things like “skip this song” and “next track” both point to the same command, i also train it on more niche things so most of the time it will pick it up. I will contuine to improve the data.

The model counts the words it recognizes from training and uses those counts to pick a command. The training script saves the model as `music_model.pth`. Klovia uses `PyAutoGUI` to press the media keys and `pycaw` to control the Windows volume.

The training file has 306 examples across seven commands and an `Other` category for unrelated phrases. The model has one hidden layer with 32 neurons. If it picks `Other`, Klovia leaves the music alone and keeps listening.

## how to run it

Open a terminal in the full project folder on Windows. You’ll need the Python dependencies installed, the trained model in place, a mic, and internet for speech recognition. Then run

```bash
python Main.py
```

Klovia spends about a second checking the background noise before it starts listening for commands. The terminal shows what it heard and, when it matches a command, which one it picked and any number it found. That helps me see if it heard me wrong or picked the wrong command. Press `Ctrl+C` to stop it.

## what I’m still working on

I want to add and improve the training data so it can be more accurate. 

I am also currently fixing a bunch of bugs

                    # Klovia

Klovia is a Python voice assistant I’m making for Windows. Basically, I wanted to control my music without having to click around or reach for the keyboard. It’s still a work in progress, but it can already play or pause music, skip songs, go back a track, mute or unmute, and change the system volume.

## stuff you can say

- “Pause the music” or “resume the music”
- “Skip this song” or “go back one track”
- “Mute the audio” or “unmute the audio”
- “Turn the volume up by 10” or “turn the volume down by 5”

For volume changes, Klovia looks for a number written as digits in the transcript. If your volume is at 30 and it hears “turn it up by 10,” it goes to 40.

Play and pause use the same media key, so what happens depends on whether music is already playing. The track controls work with apps that respond to Windows media keys. Mute and unmute also affect any other sound coming through the same audio device.

## how the local AI works

Klovia uses Google speech recognition to turn what I say into text. Then a small PyTorch model runs on my computer and figures out which command I meant. I train it on example phrases from a JSON file, so things like “skip this song” and “next track” both point to the same command.

The model counts the words it recognizes from training and uses those counts to pick a command. The training script saves the model as `music_model.pth`. Klovia uses `PyAutoGUI` to press the media keys and `pycaw` to control the Windows volume.

The training file has 306 examples across seven commands and an `Other` category for unrelated phrases. The model has one hidden layer with 32 neurons. If it picks `Other`, Klovia leaves the music alone and keeps listening.

## how to run it

Open a terminal in the full project folder on Windows. You’ll need the Python dependencies installed, the trained model in place, a mic, and internet for speech recognition. Then run

```bash
python Main.py
```

Klovia spends about a second checking the background noise before it starts listening for commands. The terminal shows what it heard and, when it matches a command, which one it picked and any number it found. That helps me see if it heard me wrong or picked the wrong command. Press `Ctrl+C` to stop it.

## what I’m still working on

I still want to add more training phrases and make volume commands like “turn it up a bit” work without having to say a specific number.

When I find a phrase Klovia keeps getting wrong, I can add it to the JSON and retrain the model. That’s how I can teach it more ways to ask for the same thing.
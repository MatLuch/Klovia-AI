# Install first: python -m pip install torch

import re
from pathlib import Path

import torch
from torch import nn

# Choose where to save the trained model.
save_folder = Path.home() / "Documents" / "Klovia" / "AI_Training" / "Training_test"
save_folder.mkdir(parents=True, exist_ok=True)
save_path = save_folder / "music_model.pth"

# Training phrases grouped by their correct command.
examples = {
    "pause": [
        "pause",
        "pause the music",
        "pause this song",
        "stop the music",
        "stop playing",
        "please pause playback",
        "can you pause my music",
        "stop this song",
        "pause the audio",
        "stop playback",
        "pause it for a moment",
        "please stop the track",
    ],
    "resume": [
        "resume",
        "unpause",
        "play",
        "play the music",
        "resume the music",
        "unpause my music",
        "continue playing",
        "keep playing",
        "start the music",
        "resume playback",
        "start playing again",
        "please resume the track",
        "stop dont stop my music",
    ],
    "other": [
        "hello",
        "what is the weather",
        "open my browser",
        "tell me a joke",
        "turn up the volume",
        "turn down the volume",
        "next song",
        "skip this track",
        "what song is this",
        "i like this music",
        "set a timer",
        "what time is it",
        "pause the video",
        "stop the timer",
        "play a game",
        "don't pause the music",
        "do not pause the music",
        "don't stop playing",
        "do not stop the music",
        "don't resume the music",
        "do not play the music",
    ],
}


def tokenize(text):
    # Convert text to lowercase and split it into words.
    return re.findall(r"[a-z']+", text.lower().replace("’", "'"))


commands = list(examples)

# Collect every unique word from the training phrases.
words = sorted({
    word
    for sentences in examples.values()
    for sentence in sentences
    for word in tokenize(sentence)
})

# Give each word its own position in a numeric vector.
vocabulary = {word: index for index, word in enumerate(words)}


def encode(text):
    # Represent a sentence by counting its known words.
    numbers = torch.zeros(len(vocabulary))

    for word in tokenize(text):
        if word in vocabulary:
            numbers[vocabulary[word]] += 1

    return numbers


inputs = []
answers = []

# Pair each encoded sentence with its command number.
for command_index, command in enumerate(commands):
    for sentence in examples[command]:
        inputs.append(encode(sentence))
        answers.append(command_index)

# Combine the examples into tensors for PyTorch.
inputs = torch.stack(inputs)
answers = torch.tensor(answers, dtype=torch.long)

torch.manual_seed(42)       # Make training more repeatable.
torch.set_num_threads(1)    # Use one CPU thread for this tiny model.

# Input: word counts. Hidden layer: 32 neurons. Output: 3 command scores.
model = nn.Sequential(
    nn.Linear(len(vocabulary), 32),
    nn.ReLU(),
    nn.Linear(32, len(commands)),
)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_function = nn.CrossEntropyLoss()  # Measures prediction errors.

model.train()

# Train on all the examples 300 times.
for epoch in range(300):
    optimizer.zero_grad()  # Clear gradients from the previous step.

    predictions = model(inputs)
    loss = loss_function(predictions, answers)

    loss.backward()       # Calculate how the weights should change.
    optimizer.step()      # Update the weights.

    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch + 1}: loss = {loss.item():.4f}")

# Save the weights and mappings needed to load the model later.
torch.save({
    "weights": model.state_dict(),
    "vocabulary": vocabulary,
    "commands": commands,
    "hidden_size": 32,
}, save_path)

print(f"\nModel saved to: {save_path}")
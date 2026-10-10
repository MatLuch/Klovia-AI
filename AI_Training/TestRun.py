import re
from pathlib import Path

import torch
from torch import nn

# Load your saved model.
path = Path.home() / "Documents" / "Klovia" / "AI_Training" / "Training_test" / "music_model.pth"
saved = torch.load(path, map_location="cpu", weights_only=True)

vocabulary = saved["vocabulary"]
commands = saved["commands"]

model = nn.Sequential(
    nn.Linear(len(vocabulary), saved["hidden_size"]),
    nn.ReLU(),
    nn.Linear(saved["hidden_size"], len(commands)),
)

model.load_state_dict(saved["weights"])
model.eval()

while True:
    text = input("Your text (exit to quit): ")

    if text.strip().lower() == "exit":
        break

    # Convert your text into word counts.
    numbers = torch.zeros(len(vocabulary))
    words = re.findall(r"[a-z']+", text.lower().replace("’", "'"))

    for word in words:
        if word in vocabulary:
            numbers[vocabulary[word]] += 1

    if not numbers.any():
        print("other")
        continue

    # Predict and print the command.
    with torch.no_grad():
        result = model(numbers.unsqueeze(0))
        print(commands[result.argmax().item()])
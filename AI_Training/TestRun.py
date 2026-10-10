import re
from pathlib import Path

import torch
from torch import nn

model_path = Path.home() / "Documents" / "Klovia" / "music_model.pth"

saved = torch.load(
    model_path,
    map_location="cpu",
    weights_only=True,
)

vocabulary = saved["vocabulary"]
commands = saved["commands"]

# Recreate the same structure used during training.
model = nn.Sequential(
    nn.Linear(len(vocabulary), saved["hidden_size"]),
    nn.ReLU(),
    nn.Linear(saved["hidden_size"], len(commands)),
)

model.load_state_dict(saved["weights"])
model.eval()


def predict(text):
    words = re.findall(
        r"[a-z']+",
        text.lower().replace("’", "'"),
    )

    numbers = torch.zeros(len(vocabulary))

    for word in words:
        if word in vocabulary:
            numbers[vocabulary[word]] += 1

    if not numbers.any():
        return "other"

    with torch.no_grad():
        output = model(numbers.unsqueeze(0))
        index = output.argmax(dim=1).item()

    return commands[index]


print("Type a command, or 'exit' to quit.")

while True:
    text = input("> ")

    if text.strip().lower() == "exit":
        break

    print("Prediction:", predict(text))
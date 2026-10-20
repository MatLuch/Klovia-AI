import re
from pathlib import Path

import torch
from torch import nn

# Load the saved model and its training information.
path = Path.home() / "Documents" / "Klovia" / "AI_Training" / "Training_test" / "music_model.pth"
saved = torch.load(path, map_location="cpu", weights_only=True)

# Retrieve the vocabulary and command labels used during training.
vocabulary = saved["vocabulary"]
commands = saved["commands"]

# Recreate the same neural network architecture used during training.
model = nn.Sequential(
    nn.Linear(len(vocabulary), saved["hidden_size"]),
    nn.ReLU(),
    nn.Linear(saved["hidden_size"], len(commands)),
)

# Load the trained weights into the network.
model.load_state_dict(saved["weights"])

# Set the model to evaluation mode for making predictions.
model.eval()

print("Klovia music command model loaded!")
print("Type a command to test the model, or type 'exit' to quit.\n")

while True:
    # Get a sentence from the user.
    text = input("Your text: ")

    # Stop the program when the user types 'exit'.
    if text.strip().lower() == "exit":
        print("Exiting...")
        break

    # Convert the input into lowercase words.
    words = re.findall(r"[a-z']+", text.lower().replace("’", "'"))

    # Create a numerical vector using the training vocabulary.
    numbers = torch.zeros(len(vocabulary))

    for word in words:
        if word in vocabulary:
            numbers[vocabulary[word]] += 1

    # If no known words were found, return the default command.
    if not numbers.any():
        print("Predicted command: other\n")
        continue

    # Run the model without calculating training gradients.
    with torch.no_grad():
        result = model(numbers.unsqueeze(0))

        # Find the command with the highest prediction score.
        prediction = result.argmax(dim=1).item()

    # Display the predicted command.
    print(f"Predicted command: {commands[prediction]}\n")
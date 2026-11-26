from pathlib import Path
import re
import torch
from torch import nn

# Load the saved model and its training information.
path = Path(__file__).resolve().parent / "GenralQuestionModel.pth"

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


# Load the NameFinder model and its training information.
name_path = Path(__file__).resolve().parent / "NameFinderModel.pth"

name_saved = torch.load(name_path, map_location="cpu", weights_only=True)

name_vocabulary = name_saved["vocabulary"]
name_commands = name_saved["commands"]

name_model = nn.Sequential(
    nn.Linear(len(name_vocabulary), name_saved["hidden_size"]),
    nn.ReLU(),
    nn.Linear(name_saved["hidden_size"], len(name_commands)),
)

name_model.load_state_dict(name_saved["weights"])
name_model.eval()


def GeneralModelAnswer(text):
  # Handle exit case
  if text.strip().lower() == "exit":
    return "exit"

  # Convert the input into lowercase words.
  words = re.findall(r"[a-z']+", text.lower().replace("’", "'"))

  # Create a numerical vector using the training vocabulary.
  numbers = torch.zeros(len(vocabulary))

  for word in words:
    if word in vocabulary:
      numbers[vocabulary[word]] += 1

  # If no known words were found, return the default command.
  if not numbers.any():
    return "other"

  # Run the model without calculating training gradients.
  with torch.no_grad():
    result = model(numbers.unsqueeze(0))
    prediction = result.argmax(dim=1).item()

  # Return the predicted command label.
  return commands[prediction]


def NameFinderModelAnswer(text):
  # Handle exit case
  if text.strip().lower() == "exit":
    return "exit"

  # Convert the input into lowercase words.
  words = re.findall(r"[a-z']+", text.lower().replace("’", "'"))

  # Create a numerical vector using the training vocabulary.
  numbers = torch.zeros(len(name_vocabulary))

  for word in words:
    if word in name_vocabulary:
      numbers[name_vocabulary[word]] += 1

  # If no known words were found, return the default command.
  if not numbers.any():
    return "other"

  # Run the model without calculating training gradients.
  with torch.no_grad():
    result = name_model(numbers.unsqueeze(0))
    prediction = result.argmax(dim=1).item()

  # Return the predicted command label.
  return name_commands[prediction]
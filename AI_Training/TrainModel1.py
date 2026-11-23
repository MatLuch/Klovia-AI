import json
import re
from pathlib import Path

import torch
from torch import nn

# Locate the JSON file containing the training phrases.
# The JSON file must be in the same folder as this Python script.
data_path = Path(__file__).with_name("TrainingDataTest.json")

print("config")

# Open the JSON file and load the training examples into Python.
# Each command contains a list of phrases associated with that command.
with open(data_path, "r", encoding="utf-8") as file:
    examples = json.load(file)

# Create the folder where the trained model will be saved.
# If the folder already exists, it will not be created again.
save_folder = Path.home() / "Documents" / "Klovia" / "AI_Training"
save_folder.mkdir(parents=True, exist_ok=True)

# Define the full path for the saved PyTorch model.
save_path = Path(__file__).resolve().with_name("music_model.pth")


def tokenize(text):
    # Convert text to lowercase and extract individual words.
    # Keep letters and apostrophes so contractions remain recognizable.
    return re.findall(r"[a-z']+", text.lower().replace("’", "'"))


# Collect every unique word used in the training phrases.
# Sorting the words makes the vocabulary order consistent.
words = sorted({
    word
    for sentences in examples.values()
    for sentence in sentences
    for word in tokenize(sentence)
})

# Assign each word a unique integer index.
# These indices determine where each word is represented in the input vector.
vocabulary = {word: index for index, word in enumerate(words)}

# Store the command names in a list.
# Each command's position will represent its numerical class label.
commands = list(examples)


def encode(text):
    # Create a vector containing one position for every vocabulary word.
    # Each position counts how many times that word appears in the sentence.
    numbers = torch.zeros(len(vocabulary))

    # Convert the sentence into a numerical representation.
    for word in tokenize(text):
        if word in vocabulary:
            numbers[vocabulary[word]] += 1

    return numbers


# Prepare the input vectors and their corresponding command labels.
inputs = []
answers = []

# Process every training phrase and assign it the index of its command.
for command_index, command in enumerate(commands):
    for sentence in examples[command]:
        # Convert the text into a numerical vector for PyTorch.
        inputs.append(encode(sentence))

        # Store the correct command index for this phrase.
        answers.append(command_index)

# Combine all input vectors into one tensor.
# Each row represents one training phrase.
inputs = torch.stack(inputs)

# Convert the command labels into a tensor of integer class indices.
answers = torch.tensor(answers, dtype=torch.long)

# Set the random seed so the model's initial weights are repeatable.
torch.manual_seed(42)

# Use one CPU thread because this is a small model.
torch.set_num_threads(1)

# Create a neural network with three main stages:
# 1. Input layer: receives the word-count vector.
# 2. Hidden layer: learns patterns using 32 neurons and ReLU activation.
# 3. Output layer: produces one score for each possible command.
model = nn.Sequential(
    nn.Linear(len(vocabulary), 32),
    nn.ReLU(),
    nn.Linear(32, len(commands)),
)

# Adam adjusts the model's weights during training.
# The learning rate controls the size of each weight update.
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Cross-entropy measures how far the model's predictions are from the
# correct command labels. Lower loss generally indicates better learning
# on the training examples.
loss_function = nn.CrossEntropyLoss()

# Set the model to training mode.
print("Model training starting")
model.train()

# Train the model for 300 epochs.
# One epoch means the model processes the complete training dataset once.
for epoch in range(300):

    # Clear gradients left over from the previous training step.
    optimizer.zero_grad()

    # Pass all training inputs through the neural network.
    # The output contains a score for each possible command.
    predictions = model(inputs)

    # Compare the predictions against the correct command labels.
    loss = loss_function(predictions, answers)

    # Calculate gradients to determine how the weights should change.
    loss.backward()

    # Update the model's weights to reduce the prediction loss.
    optimizer.step()

    # Display the loss every 100 epochs to track training progress.
    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch + 1}: loss = {loss.item():.4f}")

# Save everything required to reconstruct the trained model later:
# - weights: the neural network's learned parameters.
# - vocabulary: the word-to-index mapping used for encoding text.
# - commands: the list of command labels in their original order.
# - hidden_size: the number of neurons in the hidden layer.
torch.save({
    "weights": model.state_dict(),
    "vocabulary": vocabulary,
    "commands": commands,
    "hidden_size": 32,
}, save_path)

# Print ammount of params
total_params = sum(p.numel() for p in model.parameters())
print(f"Total trainable parameters: {total_params}")

# Display the location of the saved model.
print(f"\nModel saved to: {save_path}")
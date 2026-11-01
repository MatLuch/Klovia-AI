from AI_Training.Run1 import ModelAnswer
from Media_And_Volume.MediaControls import *
from Media_And_Volume.Volume import *

print("start entering inputs")

while True:
  text = input("Enter command: ")
  
  # Get the answer from your trained model function
  response = ModelAnswer(text)
  
  if response == "exit":
      print("Exiting")
      break
      
  print(f"Predicted command: {response}\n")
  

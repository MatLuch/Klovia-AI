import re 

# Function to locate a number in a string
def numLocate(text):
    match = re.search(r'\d+', text) # Searches the text for the first sequance of postive digits 0-9

    if match: 
        return match.group()

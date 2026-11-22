import re 

def numLocate(text):
    match = re.search(r'\d+', text)

    if match: 
        return match.group()

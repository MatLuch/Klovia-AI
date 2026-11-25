import screen_brightness_control as sbc

def Set_Brightness(input):
    try:
        input = float(input)
        sbc.set_brightness(input)

    except Exception: 
        return None

def Increase_Brightness(input):
    try:
        if input == None: input = 10
        input = float(input)
        currentBrightness = sbc.get_brightness()[0]

        if currentBrightness + input >= 100: newBright = 100
        else: newBright = currentBrightness + input 

        sbc.set_brightness(newBright)

    except Exception: 
        return None

def Decrease_Brightness(input):
    try:
        if input == None: input = 10
        input = float(input)
        currentBrightness = sbc.get_brightness()[0]

        if currentBrightness - input <= 0: newBright = 0
        else: newBright = currentBrightness - input
    
        sbc.set_brightness(newBright)

    except Exception: 
        return None


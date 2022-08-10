from playsound import playsound
from text_to_text import text_to_text
import tts
import os

def draw():
    print("Command stuff goes here")


Commands = {
    "Draw": draw
}


def checkCommand(command, voice = "en-GB-Wavenet-B"):
    print("Check command worked: " + command)

    commandNotFound = True
    for pre_command in Commands:
        if command.lower() == pre_command.lower():
            Commands[pre_command]() # the fucntnion assoiated with the command goes here
            commandNotFound = False
            

    if commandNotFound:
        print("Unreconised Command") # pass this along to GPT3
        text = text_to_text()
        response = text.query(command)
        filename = tts.text_to_wav(voice ,response)
        playsound(filename)
        # os.remove("en-GB.wav")
from threading import Thread
import pygame, enum
from requests import RequestException

# Create an enum for the animations
class LoadPath(enum.Enum):
    #        Filepath, start image number, ending image number
    RIGHT = ("pygame/assets/move_right/{num:04d}.png", 40, 60)
    LEFT = ("pygame/assets/move_left/{num:04d}.png", 1, 20)
    R_CENTER = ("pygame/assets/R_center/{num:04d}.png", 61, 79)
    L_CENTER = ("pygame/assets/L_center/{num:04d}.png", 21, 39)
    BLINK = ("pygame/assets/eye_blink/{num:04d}.png", 80, 100)


class Load(Thread):
    # Start the thread and initizlize variables
    def __init__(self):
        Thread.__init__(self)
        self.load_progress = 0
        self.returnArray = {}
        self.still_loading = False

    def run(self):
        # must have variable name be the same as enum name
        left = []
        right = []
        l_center = []
        r_center = []
        blink = []
        
        # look through enum and load images into an assosiatve array to pass back
        for animation in LoadPath:
            self.still_loading = True
            for i in range(animation.value[1], animation.value[2]):
                filePath = animation.value[0]
                filePath = filePath.format(num=i)
                locals() [animation.name.lower()].append(pygame.image.load(filePath))
                self.load_progress += 1
            self.returnArray[animation.name] = locals() [animation.name.lower()]
        
        self.still_loading = False
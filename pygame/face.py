import enum
from turtle import forward
import pygame
import enum
from load import Load


class Looking(enum.Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    NONE = 4


class Face(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.current_sprite = 0     # Index of the current sprite

    def loadAnimations(self, animationArray):
        # Load in the data from the image array
        self.moveLeft = animationArray["LEFT"]
        self.moveRight = animationArray["RIGHT"]
        self.r_center = animationArray["R_CENTER"]
        self.l_center = animationArray["L_CENTER"]
        self.blink = animationArray["BLINK"]

        # Set up the sprites image
        self.image = self.moveRight[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

    def update(self):
        pass

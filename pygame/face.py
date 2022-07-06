import enum
import pygame
import enum
import calc


class State(enum.Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    BLINK = 5
    NONE = 4


class Face(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.current_sprite = 0     # Index of the current sprite
        self.animationState = State.NONE
        self.index = 0

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
        match self.animationState:
            case State.NONE:
                self.image = self.moveRight[0]
            case State.RIGHT:
                if self.index >= len(self.moveRight) - 1:
                    index = calc.scale(self.index, 20, 40, 0, 20)
                    if index == len(self.r_center):
                        self.animationState = State.NONE
                        self.index = 0
                    else:
                        self.image = self.r_center[index]
                        self.index += 1
                else:
                    self.image = self.moveRight[self.index]
                    self.index += 1
            case State.LEFT:
                if self.index >= len(self.moveLeft) - 1:
                    index = calc.scale(self.index, 20, 40, 0, 20)
                    if index == len(self.l_center):
                        self.animationState = State.NONE
                        self.index = 0
                    else:
                        self.image = self.l_center[index]
                        self.index += 1
                else:
                    self.image = self.moveLeft[self.index]
                    self.index += 1
            case State.BLINK:
                self.image = self.blink[self.index]
                if self.index == len(self.blink) - 1:
                    self.index = 0
                    self.animationState = State.NONE
                else:
                    self.index += 1

    def StartBlink(self):
        self.animationState = State.BLINK
    
    def Right(self):
        self.animationState = State.RIGHT
    
    def Left(self):
        self.animationState = State.LEFT

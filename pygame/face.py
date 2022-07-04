import enum
import pygame
import enum
import calc


class Looking(enum.Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    NONE = 4


class Eyes(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, screen_width):
        super().__init__()
        self.blink_array = []
        self.move_center = []
        self.move_left = []
        self.move_right = []
        self.is_looking = Looking.NONE
        self.is_blinking = False
        self.x = x
        self.y = y
        self.width = width
        self.wait_time = 0
        self.wait_time_start = False
        self.SCREEN_WIDTH = screen_width
        self.move_amount = 0
        self.iteration = 1

        # Load sprites into array
        for num in range(1, 21):
            text = "pygame/assets/eye_blink/{number:04d}.png"
            text = text.format(number=num)

            sprite = pygame.image.load(text)
            sprite = pygame.transform.scale(sprite, (width, height))

            self.blink_array.append(sprite)

            #load moving right sprites
        for num in range(40, 61):
            text = "pygame/assets/move_right/{number:04d}.png"
            text = text.format(number=num)

            sprite = pygame.image.load(text)
            sprite = pygame.transform.scale(sprite, (width, height))

            self.move_right.append(sprite)

            #Load moving left sprites
        for num in range(1, 21):
            text = "pygame/assets/move_left/{number:04d}.png"
            text = text.format(number=num)

            sprite = pygame.image.load(text)
            sprite = pygame.transform.scale(sprite, (width, height))

            self.move_left.append(sprite)

            #load return center sprites
        for num in range(20, 41):
            text = "pygame/assets/return_center/{number:04d}.png"
            text = text.format(number=num)

            sprite = pygame.image.load(text)
            sprite = pygame.transform.scale(sprite, (width, height))

            self.move_center.append(sprite)
        
        self.current_sprite = 0     # Index of the current sprite
        self.image = self.blink_array[0]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]


    def blink(self):
        self.is_blinking = True
        print("blink")

    def look_left(self):
       self.is_looking = Looking.LEFT
       print("left")

    def look_right(self):
        self.is_looking = Looking.RIGHT
        print("right")

    def update(self):

        # This is for adding to the wait time once at the edge of the screen
        if self.wait_time_start:
            self.wait_time += 1

        # This is for making the robot blink
        if self.is_blinking:
            self.current_sprite += 1

            if self.current_sprite >= len(self.blink_array):
                self.current_sprite = 0
                self.is_blinking = False

            self.image = self.blink_array[self.current_sprite]


        # These handle looking left and right
        if self.is_looking == Looking.LEFT:
            self.rect.x -= self.move_amount
            if self.iteration < len(self.move_left):
                self.image = self.move_left[self.iteration]
            self.iteration += 1
            if self.rect.x < 10: 
                self.wait_time_start = True
                self.iteration = 1
                self.is_looking = Looking.NONE

        if self.is_looking == Looking.RIGHT:
            self.rect.x += self.move_amount
            if self.iteration < len(self.move_right):
                self.image = self.move_right[self.iteration]
            self.iteration += 1
            if self.rect.x > self.SCREEN_WIDTH - (self.width + 10): 
                self.iteration = 1
                self.wait_time_start = True
                self.is_looking = Looking.NONE

        # This is for reseting the face to center
        if self.is_looking == Looking.NONE:
            if self.wait_time > 200:
                if self.iteration < len(self.move_center):
                    self.image = self.move_center[self.iteration]
                
                if self.rect.x < self.x - 20 or self.rect.x > self.x + 20:
                    if self.rect.x < self.x:
                        self.iteration += 1
                        self.rect.x += self.move_amount
                    else:
                        self.iteration += 1
                        self.rect.x -= self.move_amount
                else:
                    self.iteration = 1
                    self.wait_time = 0
                    self.wait_time_start = False
        print(self.iteration)
        self.move_amount = calc.moveIteration(self.iteration)



class Mouth(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, image_path):
        super().__init__()
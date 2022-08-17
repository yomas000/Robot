from cProfile import run
from itertools import count
from pickle import TRUE
import pyxel
from enum import Enum
from playsound import playsound


SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128
class Directions(Enum):
    LEFT = 1
    RIGHT = 2
    NONE = 3

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 16
        self.direction = Directions.RIGHT
        self.image = 1
        self.jumpHeight = 10
        self.playOnce = True
        self.count = 1
        self.jump_cooldown = 50
        self.jumpSpeed = 3
        self.not_jumping = True
        self.health = 3
    
    def draw(self):
        
        # Walking animation
        if self.x % 4 == 0:
            if self.playOnce:
                self.switchImage()
                self.playOnce = False
        else:
            self.playOnce = True

        if pyxel.frame_count % self.jump_cooldown == 0:
            self.count = 1
            self.not_jumping = True
        
        # Check for collisions with floor of tilemap
        if pyxel.tilemap(0).pget((self.x + 0)/8, (self.y + 12)/8) == (0, 0) and self.not_jumping:
            self.y += 3

        # change left right animations
        if self.direction == Directions.RIGHT:
            if self.image == 1:
                pyxel.blt(self.x, self.y, 0, 32, 0, self.w, self.h, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h, 0)
        
        if self.direction == Directions.LEFT:
            if self.image == 1:
                pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 24, 0, self.w, self.h, 0)

        self.move()
        self.drawHealth()
    
    def move(self):
         # Move the player
        if self.x > 0 and self.x < SCREEN_WIDTH - self.w:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x += 1
                self.direction = Directions.RIGHT
            
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x -= 1
                self.direction = Directions.LEFT
            
            if pyxel.btn(pyxel.KEY_UP):
                self.jump()
        else:
            if self.x < 0:
                self.x += 2
            else:
                self.x -= 1


    def jump(self):
        self.not_jumping = False
        if self.count < self.jumpHeight:
            self.y -= self.jumpSpeed
            self.count += 1
        else:
            self.not_jumping = True
    
    def switchImage(self):
        if self.direction != Directions.NONE:
            self.image *= -1
    
    def drawHealth(self):
        offset = 0
        for i in range(0, self.health):
            pyxel.blt(1 + offset, 1, 0, 0, 64, 8, 8, 0)
            offset += 9


class App:
    def __init__(self):
        playsound("pyxel/assets/8 Bit Dungeon.wav", False)
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")
        pyxel.load("assets/first.pyxres")


        self.player = Player(8, 0)
        self.torch_num = 1

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        
        playOnce = True
        for i in range(0, 17):
            for j in range(0, 17):
                if pyxel.tilemap(0).pget(i, j) == (0, 10):


                    if pyxel.frame_count % 3 == 0:
                        if playOnce:
                            if self.torch_num == 3:
                                self.torch_num = 1
                            else:
                                self.torch_num += 1
                            playOnce = False
                    

                    # This is for weird offset reasons IDK
                    var = 8
                    i *= var
                    j *= var


                    if self.torch_num == 1:
                        pyxel.blt(i, j, 0, 0, 80, 8, 8)
                    elif self.torch_num == 2:
                        pyxel.blt(i, j, 0, 8, 80, 8, 8)
                    elif self.torch_num == 3:
                        pyxel.blt(i, j, 0, 16, 80, 8, 8)

        self.player.draw()


App()
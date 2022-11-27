from cProfile import run
from itertools import count
from pickle import TRUE
import pyxel
from enum import Enum
from playsound import playsound


SCREEN_WIDTH = 256
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
        self.playOnce = True
        self.y_vel = 0
        self.health = 3
        self.keyCount = 0
        self.coins = 0
        self.coinAnimation = False
        self.count = 1
        self.isAttacking = False
    
    def draw(self):
        
        # Walking animation
        if self.x % 4 == 0:
            if self.playOnce:
                self.switchImage()
                self.playOnce = False
        else:
            self.playOnce = True


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
        

        # Grab blocks to use later for checking
        current_block_check = pyxel.tilemap(0).pget((self.x)/8, (self.y + 14)/8)
        item_check_block = pyxel.tilemap(0).pget((self.x)/8, (self.y + 8)/8)
        
        # grab keys
        if item_check_block == (0, 6):
            self.keyCount += 1
            pyxel.tilemap(0).pset(self.x / 8, (self.y + 8) / 8, (0, 0))

        # check for chests
        if item_check_block == (2, 7): # TODO: play sound effect here
            if self.keyCount >= 1:
                self.keyCount -= 1
                self.coinAnimation = True
                self.coins += 10
                pyxel.tilemap(0).pset(self.x / 8, (self.y + 8) / 8, (3, 7))       


        # if not touching ground increase y velocity
        if  current_block_check == (0, 0) or current_block_check == (0, 10) or current_block_check == (2, 9):
            self.y_vel += 0.5
        else:
            self.y_vel = 0
            if pyxel.btnp(pyxel.KEY_UP): # only allow jump when touching something
                self.y_vel = -5
        
        
        self.y += self.y_vel


        # Check if player has attacked
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.isAttacking = True

        self.move()
        self.drawHealth()
        self.drawKeys()
        self.drawCoins()
        self.coinPlay()
        self.attackSequence()
    
    def move(self):
        # Move the player
        if self.x > 0 and self.x < SCREEN_WIDTH - self.w: # if not touching walls move if so bounce back
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x += 1
                self.direction = Directions.RIGHT
            
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x -= 1
                self.direction = Directions.LEFT
        
        else:
            if self.x < 0:
                self.x += 2
            else:
                self.x -= 1

    
    def switchImage(self):
        if self.direction != Directions.NONE:
            self.image *= -1
    
    def drawHealth(self):
        offset = 0
        for i in range(0, self.health):
            pyxel.blt(1 + offset, 1, 0, 0, 64, 8, 8, 0)
            offset += 9
    
    def coinPlay(self):
        if self.coinAnimation:
            if pyxel.frame_count % 2 == 0:
                self.count += 1

                if self.count > 7:
                    self.count = 1
                    self.coinAnimation = False

            pyxel.blt(self.x, self.y - (9 + (self.count)), 0, 24 + (self.count * 8), 48, 8, 8, 0)

    
    def drawKeys(self):
        pyxel.blt(35, 0, 0, 0, 48, 8, 8, 0)
        pyxel.text(45, 1, str(self.keyCount), 7)
    
    def drawCoins(self):
        pyxel.blt(55, 0, 0, 24, 48, 8, 8, 0)
        pyxel.text(65, 1, str(self.coins), 7)
    
    def attackSequence(self):
        if self.isAttacking:
            if pyxel.frame_count % 3:
                self.count += 1

                if self.count > 4:
                    self.count = 1
                    self.isAttacking = False

            if self.direction == Directions.RIGHT:
                pyxel.blt(self.x, self.y, 0, 48 + (self.count * 16), 0, 16, 16, 0)
            else:
                pyxel.blt(self.x - 8, self.y, 0, 48 + (self.count * 16), 0, -16, 16, 0)


class BadGuy:
    def __init__(self, x, y, direction, ignoreFallEdges, willJump = False, walkingLength = 20): # Set it to false and he will go back and forth on the platform
        self.x = x * 8
        self.y = y * 8
        self.w = 8
        self.h = 16
        self.animation = 1
        self.direction = direction
        self.speed = 1
        self.y_vel = 0
        self.ignoreFalls = not ignoreFallEdges
        self.walkLength = walkingLength
        self.health = 3
        self.willJump = willJump
    
    def update(self):
        
        # Check if he is at the edge if he is change direction
        if self.x < 0 or self.x > SCREEN_WIDTH - self.w:
            if self.direction == Directions.RIGHT:
                    self.direction = Directions.LEFT
            else:
                self.direction = Directions.RIGHT

        # This is determine if the bad guy will move back and forth or in straight lines
        if self.ignoreFalls:
            if pyxel.frame_count % self.walkLength == 0:
                if self.direction == Directions.RIGHT:
                    self.direction = Directions.LEFT
                else:
                    self.direction = Directions.RIGHT


        # Move the bad guy and changes direction
        if self.direction == Directions.RIGHT:
            if self.animation == 1:
                pyxel.blt(self.x, self.y, 0, 0, 32, self.w, self.h)
            else:
                pyxel.blt(self.x, self.y, 0, 8, 32, self.w, self.h)
            
            self.x += self.speed

        if self.direction == Directions.LEFT:
            if self.animation == 1:
                pyxel.blt(self.x, self.y, 0, 0, 32, -self.w, self.h)
            else:
                pyxel.blt(self.x, self.y, 0, 8, 32, -self.w, self.h)
        
            self.x -= self.speed
        
        # This will change the animation
        if pyxel.frame_count % 4 == 0:
            self.animation *= -1

        
        current_block_check = pyxel.tilemap(0).pget((self.x)/8, (self.y + 14)/8)

        # if not touching ground increase y velocity
        if  current_block_check == (0, 0) or current_block_check == (0, 10) or current_block_check == (2, 9):
            self.y_vel += 0.5
        else:
            self.y_vel = 0
            if self.willJump:
                if pyxel.btnp(pyxel.KEY_UP): # only allow jump when touching something
                    self.y_vel = -5

        self.y += self.y_vel

        self.drawHealth()
    
    def drawHealth(self):
        offset = -4
        for i in range(1, self.health + 1):
            pyxel.blt(self.x + offset, self.y - 4, 0, 0, 88, 5, 4, 0)
            offset += 6
        


class App:
    def __init__(self):
        playsound("pyxel/assets/8 Bit Dungeon.wav", False)
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Hello Pyxel")
        pyxel.load("assets/first.pyxres")


        self.player = Player(8, 0)
        self.badguys1 = [BadGuy(18, 1, Directions.RIGHT, False, willJump=True)]


        self.torch_num = 1
        self.canDie = True
        self.game = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.checkCollitions()

    def draw(self):
        pyxel.cls(0)
        
        
        if pyxel.frame_count == 5170:
            playsound("pyxel/assets/8 Bit Dungeon.wav", False)


        if self.game == True:
            self.player.draw()

            for badguy in self.badguys1:
                badguy.update()
            
            pyxel.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

            self.tilemapUpdate()
        
        if self.game == False:
            pyxel.cls(12)
            pyxel.text(1, 1, "Pyxel Dungeon", 2)

    def tilemapUpdate(self):
        playOnce = True
        for i in range(0, 36):
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

    def checkCollitions(self):
        for badguy in self.badguys1:
            if self.player.x >= badguy.x and self.player.x <= (badguy.x + badguy.w):
                if (self.player.y + self.player.h / 2) >= badguy.y and (self.player.y + self.player.h / 2) <= (badguy.y + badguy.h):
                    if self.canDie:
                        self.player.health -= 1
                        self.canDie = False
        
        if pyxel.frame_count % 50 == 0:
            self.canDie = True


App()
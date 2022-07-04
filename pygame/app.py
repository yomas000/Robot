from numpy import eye
import pygame
import face
from random import randint

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1024

screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
pygame.display.set_caption("First Game")

clock = pygame.time.Clock()

running = True
eyes = face.Eyes((SCREEN_WIDTH / 2) - (480 / 2), (SCREEN_HEIGHT / 2) - (270 / 2), 480, 270, SCREEN_WIDTH)

face_group = pygame.sprite.Group() # Sprites work in groups so add it to a group
face_group.add(eyes)

while running:
    rand_num = randint(0, 10000)
    screen.fill((0, 0, 0))

     # gets a loop of all events (button, mouse, etc) and iterates through to see what to do
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    # Randomly move
    if rand_num > 80 and rand_num < 90:
        eyes.look_left()
    
    if rand_num < 10:
        eyes.look_right()
    
    if rand_num > 20 and rand_num < 50:
        eyes.blink()

    face_group.draw(screen)
    face_group.update()
    pygame.display.update() #updates the display
    clock.tick(24)

pygame.quit()
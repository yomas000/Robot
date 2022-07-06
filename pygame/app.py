import pygame
from Face import Face
from load import Load
import calc

pygame.init()

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1024

screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
pygame.display.set_caption("First Game")
sprite_group = pygame.sprite.Group() # Sprites work in groups so add it to a group
clock = pygame.time.Clock()
running = True

face = Face(0, 0)

load = Load()
load.start()


while running:
    screen.fill((0, 0, 0))

     # gets a loop of all events (button, mouse, etc) and iterates through to see what to do
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # if we are still waiting for it to load - display loading sbar
    if load.still_loading:
        pygame.draw.circle(screen, (0, 255, 0), (512, 200), 150)
        pygame.draw.circle(screen, (255, 0, 0), (512, 200), 120)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1024, 200))
        pygame.draw.circle(screen, (0, 0, 0), (500, 200), 40)
        pygame.draw.circle(screen, (0, 0, 0), (555, 200), 30)
        pygame.draw.circle(screen, (0, 0, 0), (530, 300), 10)
        pygame.draw.circle(screen, (0, 0, 0), (450, 260), 10)
        pygame.draw.circle(screen, (0, 0, 0), (570, 290), 10)
        text = pygame.image.load("pygame/assets/loading_bar/text.png")
        text = pygame.transform.scale(text, (600, 100))
        screen.blit(text, (220, 30, 600, 100))
        screen.blit(pygame.image.load("pygame/assets/loading_bar/Bar_bkng.png"), (127, 400, 771, 165))
        width = calc.scale(load.load_progress, 0, 95, 0, 720)
        pygame.draw.rect(screen, (228,68,100), (150, 430, width, 105), border_radius = 5)
    else:
        if (load.load_progress == 95):
            load.join()
            face.loadAnimations(load.returnArray)
            sprite_group.add(face)
            load.load_progress = 0



    sprite_group.draw(screen)
    sprite_group.update()
    pygame.display.update() #updates the display
    clock.tick(24)

pygame.quit()
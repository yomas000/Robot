import commands
import pygame
from Face import Face
from load import Load
import calc
from speech import Speech
import menuUI
import menuOptions

pygame.init()

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1024
LOAD_AMOUNT = 95

screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
pygame.display.set_caption("First Game")
sprite_group = pygame.sprite.Group() # Sprites work in groups so add it to a group
clock = pygame.time.Clock()


face = Face(0, 0)
load = Load()
speech = Speech()

if menuOptions.displayMenu:
    menu = menuUI.menu()


running = True
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# start the loading thread
load.start()
# Start speech only if enabled
if menuOptions.voiceActivation: 
    speech.start()


previousCommand = ""
speechFound = False

while running:
    screen.fill((0, 0, 0))
    


     # gets a loop of all events (button, mouse, etc) and iterates through to see what to do
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos() 
        mouse_buttons = pygame.mouse.get_pressed()

        if menuOptions.displayMenu:
            if calc.checkHitbox(mouse_pos, menu.getMenuRect()) and mouse_buttons[0]:
                menu.show = not menu.show # TODO Switch this for fucntion

            if mouse_buttons[0] and menu.show:
                menu.mouse_cords(mouse_pos)

        if mouse_buttons[2]:
            face.Left()

        if event.type == pygame.QUIT:
            if menuOptions.voiceActivation:
                speech.Kill_Thread()
            running = False

    if previousCommand != speech.output:
        previousCommand = speech.output
        speechFound = True

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
        width = calc.scale(load.load_progress, 0, LOAD_AMOUNT, 0, 720)
        pygame.draw.rect(screen, (228,68,100), (150, 430, width, 105), border_radius = 5)
    else:
        if (load.load_progress == LOAD_AMOUNT):
            load.join()
            face.loadAnimations(load.returnArray)
            # Add sprites here
            sprite_group.add(face)

            if menuOptions.displayMenu:
                sprite_group.add(menu)

            load.load_progress = 0


    # If we found speech load it into a global variable
    if speechFound:
        if menuOptions.voiceActivation:
            commands.checkCommand(speech.output)
        
        speechFound = False
        print("Speech Found: " + speech.output)
        
    # If they want to stop the robot
    if speech.output == "hey robot shut down" or speech.output == "hey robot shutdown":
        running = False
        speech.kill()


    sprite_group.draw(screen)
    sprite_group.update()
    pygame.display.update() #updates the display
    clock.tick(24)
pygame.quit()
import pygame
import calc

class menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.show = False
        self.gearImage = pygame.image.load("pygame/assets/menu/menuGear.png")
        self.menuImage = pygame.image.load("pygame/assets/menu/RobotMenuLv1.png")
        self.rect = self.gearImage.get_rect()
        
        
        self.gearImage = pygame.transform.scale(self.gearImage, (50, 50))
        self.menuImage = pygame.transform.scale(self.menuImage, (800, 800))
        
        self.rect.topleft = [10, 650]
        self.image = self.gearImage

        self.angle = 0

    def update(self):
        if self.show:
            self.rect.topleft = [-400, 320]

            
            self.image = self.menuImage

            print(self.angle)

        else:
            self.rect.topleft = [10, 650]
            self.image = self.gearImage

    def mouse_cords(self, mouse_cords):
        self.angle = calc.scale(mouse_cords[1], 300, 715, 0, 360)
        self.menuImage = calc.rot_center(self.menuImage, self.angle)

    def getMenuRect(self):
        return (10, 650, 50, 50)
import pygame
from numpy import interp
import math

def scale(number ,minRange, maxRange, scaledMinRange, scaledMaxRange):
    return math.floor(interp(number, [minRange, maxRange], [scaledMinRange, scaledMaxRange]))


def checkHitbox(click_pos, rect):
    mouse_x = click_pos[0]
    mouse_y = click_pos[1]

    rect_x = rect[0]
    rect_y = rect[1]
    rect_width = rect[2]
    rect_height = rect[3]


    if mouse_x > rect_x and mouse_x < rect_x + rect_width:
        if mouse_y > rect_y and mouse_y < rect_y + rect_height:
            return True
        else:
            return False
    else:
        return False


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
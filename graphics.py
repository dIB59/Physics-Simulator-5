import pygame, sys, random

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius *2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0,0,0))
    return surf

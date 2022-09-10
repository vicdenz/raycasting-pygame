import pygame
from const import *

class Line:# a = startpoint, b = endpoint
    def __init__(self, a, b):
        self.a = pygame.Vector2(a)
        self.b = pygame.Vector2(b)

    def draw(self, screen):
        pygame.draw.line(screen, LINE_COLOR, self.a, self.b, 4)
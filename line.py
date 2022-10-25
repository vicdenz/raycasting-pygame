import pygame
from const import *
import random
class Line:# a = startpoint, b = endpoint
    def __init__(self, a, b, color=LINE_COLOR, width=1):
        self.a = pygame.Vector2(a)
        self.b = pygame.Vector2(b)
        self.color = color
        self.width = width

    def draw(self, screen):
        # pygame.draw.line(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), self.a, self.b, 4)
        pygame.draw.line(screen, self.color, self.a, self.b, self.width)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
    
    def __str__(self):
        return str(self.a) + " " + str(self.b)
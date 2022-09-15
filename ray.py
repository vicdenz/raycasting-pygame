import pygame
import math
from const import *

class Ray:# a = initial point, b = terminal point
    extend = 10

    def __init__(self, pos, dir):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(dir)

    def point_to(self, new_x, new_y):
        dis_x = new_x-self.pos.x
        dis_y = new_y-self.pos.y

        if dis_x != 0:
            angle = math.atan(dis_y/dis_x)

            if dis_x < 0:
                angle += math.radians(180)

            self.dir.x = math.cos(angle)
            self.dir.y = math.sin(angle)

    def intersect(self, line):#1-2 = ray, 3-4 = line segment. t >= 0, 0 <= u <= 1. t can be greater than 1 because a ray does have an endpoint.
        x1 = line.a.x
        y1 = line.a.y
        x2 = line.b.x
        y2 = line.b.y

        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        denominator = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))

        if denominator != 0:
            t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/denominator
            u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/denominator

            p = ((x1 + t*(x2-x1)), (y1 + t*(y2-y1)))
            if 0 <= t <= 1 and 0 <= u:
                return p
            return False
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, RAY_COLOR, self.pos, 2)
        pygame.draw.line(screen, RAY_COLOR, self.pos, [self.pos.x + self.dir.x * self.extend, self.pos.y + self.dir.y * self.extend])
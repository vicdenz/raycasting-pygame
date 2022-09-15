import pygame
import math, numpy
from const import *
from ray import Ray

class Player:# pos = position, angle = direction facing, scope = FOV of the player
    def __init__(self, pos, angle, scope):
        self.pos = pygame.Vector2(pos)
        self.angle = math.radians(angle)#radians
        self.scope = scope#degrees
        self.rays = [Ray(self.pos, (math.cos(radian), math.sin(radian))) for radian in numpy.arange(self.angle-math.radians(self.scope/2), self.angle+math.radians(self.scope/2), math.pi/(180/DEGREE_INCREMENT))]

    def get_x(self):
        return self.pos.x

    def get_y(self):
        return self.pos.y

    def set_pos(self, new_pos):
        self.pos = pygame.Vector2(new_pos)

        for ray in self.rays:
            ray.pos = self.pos

    def set_angle(self, new_angle):#radians
        # angle_diff = new_angle - self.angle
        self.angle = new_angle

        self.rays = [Ray(self.pos, (math.cos(radian), math.sin(radian))) for radian in numpy.arange(self.angle-math.radians(self.scope/2), self.angle+math.radians(self.scope/2), math.pi/(180/DEGREE_INCREMENT))]

        # for ray in self.rays:
        #     ray_angle = math.atan2(ray.pos.x, ray.pos.y)

        #     theta = ray_angle+angle_diff
        #     new_x = ray.dir.x * math.cos(theta) - ray.dir.x * math.sin(theta)
        #     new_y = ray.dir.x * math.sin(theta) + ray.dir.y * math.cos(theta)

        #     ray.dir.x = new_x
        #     ray.dir.y = new_y

    def set_scope(self, new_scope):
        if MIN_SCOPE <= new_scope <= MAX_SCOPE:
            self.scope = new_scope

            self.rays = [Ray(self.pos, (math.cos(radian), math.sin(radian))) for radian in numpy.arange(self.angle-math.radians(self.scope/2), self.angle+math.radians(self.scope/2), math.pi/(180/DEGREE_INCREMENT))]

    def draw(self, screen):        
        for ray in self.rays:
            ray.draw(screen)
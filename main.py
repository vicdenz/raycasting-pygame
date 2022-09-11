import pygame
from const import *
from ray import Ray
from line import Line
import numpy, math, random

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RayCasting")

clock = pygame.time.Clock()

light_source = [Ray((200, 200), (math.cos(radian), math.sin(radian))) for radian in numpy.arange(0.0, math.pi*2, math.pi/(180/DEGREE_INCREMENT))]

boundaries = []
light_area = []

def randomize_boundaries():
    global boundaries

    boundaries = [Line((0, 0), (WIDTH, 0)), Line((0, HEIGHT-1), (WIDTH, HEIGHT-1)), Line((0, 0), (0, HEIGHT)), Line((WIDTH-1, 0), (WIDTH-1, HEIGHT))]

    for r in range(0, random.randint(0, MAX_BOUNDARIES)):
        boundaries.append(Line((random.randint(0, WIDTH), random.randint(0, HEIGHT)), (random.randint(0, WIDTH), random.randint(0, HEIGHT))))

def update_light():
    global light_area
    light_area = []
    for ray in light_source:
        intersect_points = {}
        for boundary in boundaries:
            intersect_point = ray.intersect(boundary)
            if intersect_point:
                intersect_points[intersect_point] = 0
    
        if len(intersect_points) != 0:        
            for point in intersect_points:
                intersect_points[point] = math.sqrt(math.pow(point[0]-ray.pos.x, 2)+math.pow(point[1]-ray.pos.y, 2))

            intersect_points = dict(sorted(intersect_points.items(), key=lambda item: item[1]))

            light_area.append(list(intersect_points.keys())[0])

def redrawGameWindow():
    screen.fill(BG_COLOR)

    for boundary in boundaries:
        boundary.draw(screen)

    # for ray in light_source:
    #     ray.draw(screen)

    pygame.draw.polygon(screen, RAY_COLOR, light_area)

    pygame.display.update()

randomize_boundaries()
update_light()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.KMOD_LCTRL:
                running = False
            
            if event.key == pygame.K_SPACE:
                randomize_boundaries()
                update_light()

        if event.type == pygame.MOUSEMOTION:
            update_light()

            mouse_pos = pygame.mouse.get_pos()
            for ray in light_source:
                ray.pos.x = mouse_pos[0]
                ray.pos.y = mouse_pos[1]

    redrawGameWindow()

pygame.quit()
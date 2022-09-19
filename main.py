import pygame
from const import *
from ray import Ray
from line import Line
from player import Player
from maze import *
import numpy, math, random

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RayCasting")

clock = pygame.time.Clock()

mouse = [Ray((0, 0), (math.cos(radian), math.sin(radian))) for radian in numpy.arange(0.0, math.pi*2, math.pi/(180/DEGREE_INCREMENT))]

boundaries = []
light_area = []

player = Player((10, 10), 90, 90)

#m = mouse
#p = player
mode = "m"

def randomize_boundaries():
    global boundaries

    boundaries = []

    rows = WIDTH//GRID_SIZE
    columns = HEIGHT//GRID_SIZE
    maze = generate_maze(rows, columns, GRID_SIZE, interative_maze)

    for row in maze:
        for cell in row:
            line_x = cell.x*cell.size
            line_y = cell.y*cell.size

            if cell.walls[N]:
                a, b = (line_x, line_y), (line_x+cell.size, line_y)
                for boundary in boundaries:
                    if boundary.a == a and boundary.b == b:
                        break
                else:
                    boundaries.append(Line(a, b))
            if cell.walls[W]:
                a, b = (line_x+cell.size, line_y), (line_x+cell.size, line_y+cell.size)
                for boundary in boundaries:
                    if boundary.a == a and boundary.b == b:
                        break
                else:
                    boundaries.append(Line(a, b))
            if cell.walls[S]:
                a, b = (line_x, line_y+cell.size), (line_x+cell.size, line_y+cell.size)
                for boundary in boundaries:
                    if boundary.a == a and boundary.b == b:
                        break
                else:
                    boundaries.append(Line(a, b))
            if cell.walls[E]:
                a, b = (line_x, line_y), (line_x, line_y+cell.size)
                for boundary in boundaries:
                    if boundary.a == a and boundary.b == b:
                        break
                else:
                    boundaries.append(Line(a, b))

    # boundaries = [Line((0, 0), (WIDTH, 0)), Line((0, HEIGHT-1), (WIDTH, HEIGHT-1)), Line((0, 0), (0, HEIGHT)), Line((WIDTH-1, 0), (WIDTH-1, HEIGHT))]

    # for r in range(0, random.randint(MIN_BOUNDARIES, MAX_BOUNDARIES)):
    #     start_point = (random.randint(0, WIDTH/GRID_SIZE)*GRID_SIZE, random.randint(0, HEIGHT/GRID_SIZE)*GRID_SIZE)

    #     dir = [random.randint(0, 1)]
    #     dir.append(abs(dir[0]-1))

    #     end_point = (start_point[0] + dir[0] * (GRID_SIZE * random.randint(MIN_LENGTH, WIDTH/GRID_SIZE)), start_point[1] + dir[1] * (GRID_SIZE * random.randint(MIN_LENGTH, WIDTH/GRID_SIZE)))
    #     boundaries.append(Line(start_point, end_point))

def update_light(mode):
    global mouse, player

    if mode == "m":
        rays = mouse
    elif mode == "p":
        rays = player.rays

    light_area = []
    for ray in rays:
        intersect_points = {}
        for boundary in boundaries:
            intersect_point = ray.intersect(boundary)
            if intersect_point:
                intersect_distance = math.sqrt(math.pow(intersect_point[0]-ray.pos.x, 2)+math.pow(intersect_point[1]-ray.pos.y, 2))
                intersect_points[intersect_distance] = intersect_point

        if len(intersect_points) != 0:
            closest_distances = sorted(list(intersect_points.keys()))

            light_area.append(intersect_points[closest_distances[0]])
    
    return light_area

def redrawGameWindow():
    screen.fill(BG_COLOR)

    for boundary in boundaries:
        boundary.draw(screen)

    if mode == "m":
        # for ray in mouse:
        #     ray.draw(screen)

        pygame.draw.polygon(screen, RAY_COLOR, light_area)
    elif mode == "p":
        # player.draw(screen)

        pygame.draw.polygon(screen, RAY_COLOR, light_area+[player.pos])

    pygame.display.update()

randomize_boundaries()
light_area = update_light(mode)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.KMOD_LCTRL:
                running = False

        if event.type == pygame.MOUSEMOTION and mode == "m":
            light_area = update_light(mode)

            # t = timeit.Timer(lambda: update_light(mode))
            # print(t.timeit(1))

            mouse_pos = pygame.mouse.get_pos()
            for ray in mouse:
                ray.pos.x = mouse_pos[0]
                ray.pos.y = mouse_pos[1]

    key_pressed = pygame.key.get_pressed()
    retrace = False

    if key_pressed[pygame.K_SPACE]:
        randomize_boundaries()
        retrace = True

    if key_pressed[pygame.K_w]:
        player.set_pos((player.get_x(), player.get_y()-MOVEMENT_SPEED))
        retrace = True

    if key_pressed[pygame.K_a]:
        player.set_pos((player.get_x()-MOVEMENT_SPEED, player.get_y()))
        retrace = True

    if key_pressed[pygame.K_s]:
        player.set_pos((player.get_x(), player.get_y()+MOVEMENT_SPEED))
        retrace = True
    
    if key_pressed[pygame.K_d]:
        player.set_pos((player.get_x()+MOVEMENT_SPEED, player.get_y()))
        retrace = True
    
    if key_pressed[pygame.K_p]:
        mode = "p"
        player.set_pos(mouse[0].pos)
        retrace = True
    
    if key_pressed[pygame.K_m]:
        mode = "m"
        for ray in mouse:
            ray.pos.x = player.get_x()
            ray.pos.y = player.get_y()
        retrace = True

    if key_pressed[pygame.K_LEFT]:
        player.set_angle(player.angle - math.radians(ROTATE_SPEED))
        retrace = True

    if key_pressed[pygame.K_RIGHT]:
        player.set_angle(player.angle + math.radians(ROTATE_SPEED))
        retrace = True

    if key_pressed[pygame.K_UP]:
        player.set_scope(player.scope + 1)
        retrace = True

    if key_pressed[pygame.K_DOWN]:
        player.set_scope(player.scope - 1)
        retrace = True

    if retrace:
        light_area = update_light(mode)

    redrawGameWindow()

pygame.quit()
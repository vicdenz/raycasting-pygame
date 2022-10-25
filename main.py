import pygame
from const import *
from ray import Ray
from line import Line
from player import Player
from maze import *
import numpy, math, random

screen = pygame.display.set_mode(SCREEN_SIZE)
display = pygame.Surface((WIDTH*2, HEIGHT))
pygame.display.set_caption("RayCasting")

clock = pygame.time.Clock()

mouse = [Ray((0, 0), (math.cos(radian), math.sin(radian))) for radian in numpy.arange(0.0, math.pi*2, math.pi/(180/DEGREE_INCREMENT))]

boundaries = []
light_area = []
wall_hit = []

cells = []

player = Player((10, 10), 90, 60)

mode = "p"

def angle_difference(a1, a2):
    a = a1 - a2
    a -= 360 if a > 180 else 0
    a += 360 if a < -180 else 0
    return a

def generate_maze_boundaries():
    global boundaries, cells

    boundaries = []
    cells = []

    rows = WIDTH//GRID_SIZE
    columns = HEIGHT//GRID_SIZE
    maze = generate_maze(rows, columns, GRID_SIZE, recursive_maze)

    for row in maze:
        c_row = []
        for cell in row:
            line_x = cell.x*cell.size
            line_y = cell.y*cell.size

            new_lines = []
            if cell.walls[N]:
                a, b = Cell.direction_to_coord(N, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines.append(new_line)
            if cell.walls[W]:
                a, b = Cell.direction_to_coord(W, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines.append(new_line)
            if cell.walls[S]:
                a, b = Cell.direction_to_coord(S, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines.append(new_line)
            if cell.walls[E]:
                a, b = Cell.direction_to_coord(E, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines.append(new_line)

            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for new_line in new_lines:
                new_line.color = color
                boundaries.append(new_line)
            c_row.append(new_lines)
        cells.append(c_row)

def generate_random_boundaries():
    global boundaries

    boundaries = [Line((0, 0), (WIDTH, 0)), Line((0, HEIGHT-1), (WIDTH, HEIGHT-1)), Line((0, 0), (0, HEIGHT)), Line((WIDTH-1, 0), (WIDTH-1, HEIGHT))]

    for r in range(0, random.randint(MIN_BOUNDARIES, MAX_BOUNDARIES)):
        start_point = (random.randint(0, WIDTH/GRID_SIZE)*GRID_SIZE, random.randint(0, HEIGHT/GRID_SIZE)*GRID_SIZE)

        dir = [random.randint(0, 1)]
        dir.append(abs(dir[0]-1))

        end_point = (start_point[0] + dir[0] * (GRID_SIZE * random.randint(MIN_LENGTH, WIDTH/GRID_SIZE)), start_point[1] + dir[1] * (GRID_SIZE * random.randint(MIN_LENGTH, WIDTH/GRID_SIZE)))
        boundaries.append(Line(start_point, end_point))

def get_neighbours(i, j, rows, columns):
	neighbours = []

	for x in range(max(0, i - 1), min(i + 1, rows-1) + 1, 1):
		for y in range(max(0, j - 1), min(j + 1, columns-1) + 1, 1):
				neighbours.append([x, y])

	return neighbours

def nearest_intersection(ray, r, c, cells, row_limit, column_limit):
    p_neighbours = get_neighbours(r, c, row_limit, column_limit)
    skip_neighbours = []

    for i, j in p_neighbours:
        skip = False

        if ray.dir.x < 0 and ray.pos.x < j*GRID_SIZE:
            skip = True
        if ray.dir.x > 0 and ray.pos.x > j*GRID_SIZE:
            skip = True

        if ray.dir.y < 0 and ray.pos.y < i*GRID_SIZE:
            skip = True
        if ray.dir.y > 0 and ray.pos.y > i*GRID_SIZE:
            skip = True

        if skip:
            skip_neighbours.append((i, j))
            continue

        c_neighbours = get_neighbours(i, j, row_limit, column_limit)

        for x, y in c_neighbours:
            cell_boundaries = cells[y][x]

            intersect_points = {}

            for boundary in cell_boundaries:
                intersect_point = ray.intersect(boundary)
                intersect_distance = math.sqrt(math.pow(intersect_point[0]-ray.pos.x, 2)+math.pow(intersect_point[1]-ray.pos.y, 2))
                intersect_points[intersect_distance] = intersect_point

            if len(intersect_points) != 0:
                closest_distance = sorted(list(intersect_points.keys()))[0]
                
                return intersect_points[closest_distance]
    else:
        for i, j in p_neighbours:
            if (i, j) not in skip_neighbours:
                return nearest_intersection(ray, i, j, cells, row_limit, column_limit)

def update_light(mode):
    global mouse, player

    if mode == "m":
        rays = mouse
    elif mode == "p":
        rays = player.rays

    light_area = []
    wall_hit = []
    for ray in rays:
        intersect_points = {}

        for boundary in boundaries:
            intersect_point = ray.intersect(boundary)
            if intersect_point:
                intersect_distance = math.sqrt(math.pow(intersect_point[0]-ray.pos.x, 2)+math.pow(intersect_point[1]-ray.pos.y, 2))
                intersect_points[intersect_distance] = [intersect_point, boundary]

        if len(intersect_points) != 0:
            closest_distance = sorted(list(intersect_points.keys()))[0]
            light_area.append(intersect_points[closest_distance][0])
            wall_hit.append(intersect_points[closest_distance][1])
        
        # intersect_point = nearest_intersection(ray, math.floor(ray.pos.x/GRID_SIZE), math.floor(ray.pos.y/GRID_SIZE), cells, len(cells), len(cells[0]))

        # if intersect_point:
        #     light_area.append(intersect_point)

    return light_area, wall_hit

def redrawGameWindow():
    display.fill(BG_COLOR)

    for boundary in boundaries:
        boundary.draw(display)

    if mode == "m":
        # for ray in mouse:
        #     ray.draw(display)

        if len(light_area) > 2:
            pygame.draw.polygon(display, RAY_COLOR, light_area)
    elif mode == "p":
        # player.draw(display)

        if len(light_area) > 2:
            pygame.draw.polygon(display, RAY_COLOR, light_area+[player.pos])

            line_width = WIDTH//player.scope
            for x, ray in enumerate(light_area):
                player_distance = max(1, math.sqrt(math.pow(ray[0]-player.get_x(), 2) + math.pow(ray[1]-player.get_y(), 2)))

                rise = ray[1]-player.get_y()
                run = ray[0]-player.get_x()

                angle = math.degrees(math.atan2(rise, run)) + 360 * (rise<0)
                angle_diff = abs(angle_difference(math.degrees(player.angle), angle))

                player_distance = player_distance * math.cos(math.radians(angle_diff))
                line_height = max(0, 200-player_distance)

                color_offset = max(0.2, 1-player_distance*0.005)

                if line_height > 0:
                    pygame.draw.line(display, [channel*color_offset for channel in wall_hit[x].color] if color_offset < 1 else RAY_COLOR, (WIDTH + x*line_width, HEIGHT/2-line_height/2), (WIDTH + x*line_width, HEIGHT/2+line_height/2), line_width)

    surf = pygame.transform.scale(display, (WIDTH*4, HEIGHT*2))
    screen.blit(surf, (0, 0))
    pygame.display.update()

generate_maze_boundaries()
light_area, wall_hit = update_light(mode)

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
            light_area, wall_hit = update_light(mode)

            # t = timeit.Timer(lambda: update_light(mode))
            # print(t.timeit(1))

            mouse_pos = pygame.mouse.get_pos()
            for ray in mouse:
                ray.pos.x = mouse_pos[0]/2
                ray.pos.y = mouse_pos[1]/2

    key_pressed = pygame.key.get_pressed()
    retrace = False

    if key_pressed[pygame.K_SPACE]:
        generate_maze_boundaries()
        retrace = True

    if key_pressed[pygame.K_w]:
        player.set_pos((player.get_x()+math.cos(player.angle)*MOVEMENT_SPEED, player.get_y()+math.sin(player.angle)*MOVEMENT_SPEED))
        retrace = True

    if key_pressed[pygame.K_s]:
        player.set_pos((player.get_x()-math.cos(player.angle)*MOVEMENT_SPEED, player.get_y()-math.sin(player.angle)*MOVEMENT_SPEED))
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
        new_angle = player.angle - math.radians(ROTATE_SPEED)
        player.set_angle(2 * math.pi if new_angle < 0 else new_angle)
        retrace = True

    if key_pressed[pygame.K_RIGHT]:
        new_angle = player.angle + math.radians(ROTATE_SPEED)
        player.set_angle(0 if new_angle >= 2 * math.pi else new_angle)
        retrace = True

    if key_pressed[pygame.K_UP]:
        player.set_scope(player.scope + 1)
        retrace = True

    if key_pressed[pygame.K_DOWN]:
        player.set_scope(player.scope - 1)
        retrace = True

    if retrace:
        light_area, wall_hit = update_light(mode)

        if player.get_x() < 1:#left
            player.set_pos((1, player.get_y()))
        if player.get_x() > WIDTH-1:#right
            player.set_pos((WIDTH-1, player.get_y()))
        if player.get_y() < 1:#up
            player.set_pos((player.get_x(), 1))
        if player.get_y() > HEIGHT-1:#down
            player.set_pos((player.get_x(), HEIGHT-1))

    redrawGameWindow()

pygame.quit()
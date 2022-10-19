import pygame
from const import *
from ray import Ray
from line import Line
from player import Player
from maze import *
import numpy, math, random

screen = pygame.display.set_mode(SCREEN_SIZE)
display = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("RayCasting")

clock = pygame.time.Clock()

mouse = [Ray((0, 0), (math.cos(radian), math.sin(radian))) for radian in numpy.arange(0.0, math.pi*2, math.pi/(180/DEGREE_INCREMENT))]

boundaries = []
light_area = []

cells = []

player = Player((10, 10), 90, 90)

mode = "m"

def randomize_boundaries():
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

            new_lines = {}
            if cell.walls[N]:
                a, b = Cell.direction_to_coord(N, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines[N] = new_line
            if cell.walls[W]:
                a, b = Cell.direction_to_coord(W, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines[W] = new_line
            if cell.walls[S]:
                a, b = Cell.direction_to_coord(S, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines[S] = new_line
            if cell.walls[E]:
                a, b = Cell.direction_to_coord(E, line_x, line_y, cell.size)
                new_line = Line(a, b)

                if new_line not in boundaries:
                    new_lines[E] = new_line

            c_cell = []
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for dir, new_line in new_lines.items():
                new_line.color = color
                boundaries.append(new_line)
                c_cell.append(len(boundaries)-1)
                # row, col = next_coord(cell.x, cell.y, dir)
                # a, b = Cell.direction_to_coord(dir, row*cell.size, col*cell.size, cell.size)
                # opposite_line = Line(a, b)
                # # print(cell.x, cell.y, row, col)
                # # print(str(dir), new_line, opposite_line)
                # # print([str(b) for b in boundaries])
                # if opposite_line in boundaries:
                #     boundaries.remove(opposite_line)
                #     boundaries.append(Line(a, new_line.b))
                #     print('LOLLLLL')
                #     # pygame.time.delay(1000)
                # else:
                #     boundaries.append(new_line)
                # # print()
            c_row.append(c_cell)
        cells.append(c_row)
    
    # last_cell = {(0, 0): 0}
    # visited = []
    # cx, cy = 0, 0
    # # walls = {}#[start_point, direction] : boundaries to remove
    # walls = {}#[start_point, direction] : end_point

    # while len(last_cell) != 0:
    #     cell = maze[cx][cy]

    #     for dir in directions:
    #         dx, dy = next_coord(cx, cy, dir)

    #         print(cx, cy, dx, dy)
    #         dir_cell = maze[dx][dy]
    #         print((cx, cy), visited)
    #         if 0 <= dy < len(maze) and 0 <= dx < len(maze[dy]) and (cx, cy) not in visited:
    #             print('visit')
    #             print(cell)
    #             print(dir_cell)
    #             print()
    #             if cell.walls[dir] == dir_cell.walls[dir]:
    #                 print('next')
    #                 a = cell.get_pos()
    #                 b = Cell.direction_to_coord(dir, a[0], a[1], cell.size)[1]

    #                 walls[(a, dir)] = b
    #                 last_cell[(cx, cy)] = (dx, dy)
    #                 visited.append((cx, cy))
    #                 cx, cy = dx, dy
    #                 break
    #         print(last_cell, walls, dir)
    #     else:
    #         print('remove', last_cell)
    #         cx, cy = list(last_cell.values())[-1]
    #         last_cell.popitem()
    
    # print(walls)
    # for wall in walls:
    #     boundaries.append(Line(wall[0], walls[wall], (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    # boundaries = [Line((0, 0), (WIDTH, 0)), Line((0, HEIGHT-1), (WIDTH, HEIGHT-1)), Line((0, 0), (0, HEIGHT)), Line((WIDTH-1, 0), (WIDTH-1, HEIGHT))]

    # for r in range(0, random.randint(MIN_BOUNDARIES, MAX_BOUNDARIES)):
    #     start_point = (random.randint(0, WIDTH/GRID_SIZE)*GRID_SIZE, random.randint(0, HEIGHT/GRID_SIZE)*GRID_SIZE)

    #     dir = [random.randint(0, 1)]
    #     dir.append(abs(dir[0]-1))

    #     end_point = (start_point[0] + dir[0] * (GRID_SIZE * random.randint(MIN_LENGTH, WIDTH/GRID_SIZE)), start_point[1] + dir[1] * (GRID_SIZE * random.randint(MIN_LENGTH, WIDTH/GRID_SIZE)))
    #     boundaries.append(Line(start_point, end_point))

def get_neighbours(i, j, rows, columns):
    neighbours = []

    for x in range(max(0, i-1), min(i+1, rows)+1, 1):
        for y in range(max(0, j-1), min(j+1, columns)+1, 1):
            if(x != i or y != j):
                neighbours.append([x, y])
    
    return neighbours

def update_light(mode):
    global mouse, player

    if mode == "m":
        rays = mouse
    elif mode == "p":
        rays = player.rays

    light_area = []
    for ray in rays:
        intersect_points = {}

        # i = math.floor(ray.pos.y//GRID_SIZE)
        # j = math.floor(ray.pos.x//GRID_SIZE)

        # row_limit = len(cells)
        # column_limit = len(cells[0])

        # neighbours = get_neighbours(i, j, row_limit, column_limit)
        # current_nb = 0
        # max_nb = len(neighbours)

        # while len(intersect_points) < 3:
        #     i, j = neighbours[current_nb]
        #     current_nb += 1
        #     if current_nb == max_nb:
        #         break

        #     print(i, j)
        #     print(list(range(max(0, i-1), min(i+1, row_limit), 1)))
        #     print(list(range(max(0, j-1), min(j+1, column_limit), 1)))
        #     for x in range(max(0, i-1), min(i+1, row_limit), 1):
        #         for y in range(max(0, j-1), min(j+1, column_limit), 1):
        #             if(x != i or y != j):
        #                 cell_boundaries = [boundaries[index] for index in cells[x][y]]
        for boundary in boundaries:#cell_boundaries:
            intersect_point = ray.intersect(boundary)
            if intersect_point:
                intersect_distance = math.sqrt(math.pow(intersect_point[0]-ray.pos.x, 2)+math.pow(intersect_point[1]-ray.pos.y, 2))
                intersect_points[intersect_distance] = intersect_point

        if len(intersect_points) != 0:
            closest_distance = sorted(list(intersect_points.keys()))[0]
            light_area.append(intersect_points[closest_distance])

    return light_area

def redrawGameWindow():
    display.fill(BG_COLOR)

    for boundary in boundaries:
        boundary.draw(display)

    if mode == "m":
        # for ray in mouse:
        #     ray.draw(display)

        pygame.draw.polygon(display, RAY_COLOR, light_area)
    elif mode == "p":
        # player.draw(display)

        pygame.draw.polygon(display, RAY_COLOR, light_area+[player.pos])

    surf = pygame.transform.scale(display, screen.get_size())
    screen.blit(surf, (0, 0))
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
                ray.pos.x = mouse_pos[0]/2
                ray.pos.y = mouse_pos[1]/2

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
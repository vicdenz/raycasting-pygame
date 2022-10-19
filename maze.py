import random
import pygame
import timeit

N, S, E, W = 0, 1, 2, 3
directions = {N: (0, -1), S: (0, 1), E: (1, 0), W: (-1, 0)}
opposite = {N: S, S: N, E: W, W: E}

def next_coord(x, y, adj):
    return x + directions[adj][0], y + directions[adj][1]

class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.visited = False
        #N, S, E, W
        self.walls = [True, True, True, True]
        self.color = (240, 210, 190)
    
    def visit(self):
        self.visited = True
    
    def get_pos(self):
        return self.x*self.size, self.y*self.size

    def draw(self, screen):
        draw_x, draw_y = self.get_pos()

        if self.walls[N]:
            a, b = Cell.direction_to_coord(N, draw_x, draw_y, self.size)
            pygame.draw.line(screen, self.color, a, b)
        if self.walls[W]:
            a, b = Cell.direction_to_coord(W, draw_x, draw_y, self.size)
            pygame.draw.line(screen, self.color, a, b)
        if self.walls[S]:
            a, b = Cell.direction_to_coord(S, draw_x, draw_y, self.size)
            pygame.draw.line(screen, self.color, a, b)
        if self.walls[E]:
            a, b = Cell.direction_to_coord(E, draw_x, draw_y, self.size)
            pygame.draw.line(screen, self.color, a, b)

    @staticmethod
    def direction_to_coord(dir, x, y, size):
        if dir == N:
            return [[x, y], [x+size, y]]
        if dir == W:
            return [[x, y], [x, y+size]]
        if dir == S:
            return [[x, y+size], [x+size, y+size]]
        if dir == E:
            return [[x+size, y], [x+size, y+size]]
    
    def __str__(self):
        return f"{self.x}, {self.y}, {self.size}, {self.visited}, {self.walls}"

def recursive_maze(cx, cy, grid):
    adjacent = [N, S, E, W]
    random.shuffle(adjacent)

    for adj in adjacent:
        nx, ny = next_coord(cx, cy, adj)

        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and not grid[ny][nx].visited:
            if grid[ny][nx].walls.count(True) > 3:
                grid[cy][cx].visit()
                grid[cy][cx].walls[adj] = False
                grid[ny][nx].walls[opposite[adj]] = False
                recursive_maze(nx, ny, grid)

def generate_maze(width, height, size, method=None, seed=0):
    if seed:
        random.seed(seed)

    grid = [[Cell(x, y, size) for x in range(width)] for y in range(height)]

    if method != None:
        method(0, 0, grid)

    return grid
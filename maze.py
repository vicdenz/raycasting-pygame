from turtle import end_fill
import numpy, random

width = 10
height = 10

grid = numpy.zeros((height, width), numpy.int8)

N, S, E, W = 1, 2, 4, 8
directions = {N: (0,-1), S: (0,1), E: (-1,0), W: (1,0)}
opposite = { N: S, S: N, E: W, W: E}

def carve_passages_from(cx, cy, grid):
    adjacent = [N, S, E, W]
    random.shuffle(adjacent)

    for adj in adjacent:
        direction = directions[adj]
        nx, ny = cx + direction[0], cy + direction[1]

        if 0 <= ny < height and 0 <= nx < width and grid[ny][nx] == 0:
            grid[cy][cx] |= adj
            grid[ny][nx] |= opposite[adj]
            carve_passages_from(nx, ny, grid)


carve_passages_from(0, 0, grid)

print(grid)

print(" " + "_" * (width * 2 - 1))
for y in range(height):
    print_row = ""
    print_row += "|"
    for x in range(width):
        print_row += " " if (grid[y][x] & S != 0) else "_"
        if grid[y][x] & E != 0 and x < width-1:
            print_row += " " if ((grid[y][x] | grid[y][x+1]) & S != 0) else "_"
        else:
            print_row += "|"
    print(print_row)
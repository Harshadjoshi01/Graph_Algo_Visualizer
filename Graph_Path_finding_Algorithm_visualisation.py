import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk
import pygame
import math
from queue import PriorityQueue


def bfs():
    size = (width, height) = 640, 480
    pygame.init()

    win = pygame.display.set_mode(size)
    pygame.display.set_caption('Breadth First Search')
    clock = pygame.time.Clock()

    cols, rows = 64, 48

    w = width // cols
    h = height // rows

    grid = []
    queue, visited = deque(), []
    path = []

    class Spot:
        def __init__(self, i, j):
            self.x, self.y = i, j
            self.f, self.g, self.h = 0, 0, 0
            self.neighbors = []
            self.prev = None
            self.wall = False
            self.visited = False
            # if random.randint(0, 100) < 20:
            #     self.wall = True

        def show(self, win, col):
            if self.wall == True:
                col = (0, 0, 0)
            pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))

        def add_neighbors(self, grid):
            if self.x < cols - 1:
                self.neighbors.append(grid[self.x + 1][self.y])
            if self.x > 0:
                self.neighbors.append(grid[self.x - 1][self.y])
            if self.y < rows - 1:
                self.neighbors.append(grid[self.x][self.y + 1])
            if self.y > 0:
                self.neighbors.append(grid[self.x][self.y - 1])
            # Add Diagonals
            # if self.x < cols - 1 and self.y < rows - 1:
            #     self.neighbors.append(grid[self.x+1][self.y+1])
            # if self.x < cols - 1 and self.y > 0:
            #     self.neighbors.append(grid[self.x+1][self.y-1])
            # if self.x > 0 and self.y < rows - 1:
            #     self.neighbors.append(grid[self.x-1][self.y+1])
            # if self.x > 0 and self.y > 0:
            #     self.neighbors.append(grid[self.x-1][self.y-1])

    def clickWall(pos, state):
        i = pos[0] // w
        j = pos[1] // h
        grid[i][j].wall = state

    def place(pos):
        i = pos[0] // w
        j = pos[1] // h
        return w, h

    for i in range(cols):
        arr = []
        for j in range(rows):
            arr.append(Spot(i, j))
        grid.append(arr)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors(grid)

    start = grid[cols // 2][rows // 2]
    end = grid[cols - 1][rows - cols // 2]
    start.wall = False
    end.wall = False

    queue.append(start)
    start.visited = True

    def bfs_strt():
        flag = False
        noflag = True
        startflag = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pressed(0):
                        clickWall(pygame.mouse.get_pos(), True)
                    if pygame.mouse.get_pressed(2):
                        clickWall(pygame.mouse.get_pos(), False)
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        clickWall(pygame.mouse.get_pos(), True)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        startflag = True

            if startflag:
                if len(queue) > 0:
                    current = queue.popleft()
                    if current == end:
                        temp = current
                        while temp.prev:
                            path.append(temp.prev)
                            temp = temp.prev
                        if not flag:
                            flag = True
                            print("Done")
                        elif flag:
                            continue
                    if flag == False:
                        for i in current.neighbors:
                            if not i.visited and not i.wall:
                                i.visited = True
                                i.prev = current
                                queue.append(i)
                else:
                    if noflag and not flag:
                        Tk().wm_withdraw()
                        messagebox.showinfo("No Solution", "There was no solution")
                        noflag = False
                    else:
                        continue

            win.fill((0, 20, 20))
            for i in range(cols):
                for j in range(rows):
                    spot = grid[i][j]
                    spot.show(win, (255, 255, 255))
                    if spot in path:
                        spot.show(win, (25, 120, 250))
                    elif spot.visited:
                        spot.show(win, (255, 0, 0))
                    if spot in queue:
                        spot.show(win, (0, 255, 0))
                    if spot == end:
                        spot.show(win, (0, 120, 255))

            pygame.display.flip()

    bfs_strt()


def dijikstra():
    size = (width, height) = 640, 480
    pygame.init()

    win = pygame.display.set_mode(size)
    pygame.display.set_caption("Dijktdtra's Path Finding")
    clock = pygame.time.Clock()

    cols, rows = 64, 48

    w = width // cols
    h = height // rows

    grid = []
    queue, visited = deque(), []
    path = []

    class Spot:
        def __init__(self, i, j):
            self.x, self.y = i, j
            self.f, self.g, self.h = 0, 0, 0
            self.neighbors = []
            self.prev = None
            self.wall = False
            self.visited = False
            # if random.randint(0, 100) < 20:
            #     self.wall = True

        def show(self, win, col, shape=1):
            if self.wall == True:
                col = (0, 0, 0)
            if shape == 1:
                pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
            else:
                pygame.draw.circle(win, col, (self.x * w + w // 2, self.y * h + h // 2), w // 3)

        def add_neighbors(self, grid):
            if self.x < cols - 1:
                self.neighbors.append(grid[self.x + 1][self.y])
            if self.x > 0:
                self.neighbors.append(grid[self.x - 1][self.y])
            if self.y < rows - 1:
                self.neighbors.append(grid[self.x][self.y + 1])
            if self.y > 0:
                self.neighbors.append(grid[self.x][self.y - 1])

    def clickWall(pos, state):
        i = pos[0] // w
        j = pos[1] // h
        grid[i][j].wall = state

    def place(pos):
        i = pos[0] // w
        j = pos[1] // h
        return w, h

    for i in range(cols):
        arr = []
        for j in range(rows):
            arr.append(Spot(i, j))
        grid.append(arr)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors(grid)

    start = grid[cols // 2][rows // 2]
    end = grid[cols - 50][rows - cols // 2]
    start.wall = False
    end.wall = False

    queue.append(start)
    start.visited = True

    def dij_strt():
        flag = False
        noflag = True
        startflag = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pressed(0):
                        clickWall(pygame.mouse.get_pos(), True)
                    if pygame.mouse.get_pressed(2):
                        clickWall(pygame.mouse.get_pos(), False)
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        clickWall(pygame.mouse.get_pos(), True)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        startflag = True

            if startflag:
                if len(queue) > 0:
                    current = queue.popleft()
                    if current == end:
                        temp = current
                        while temp.prev:
                            path.append(temp.prev)
                            temp = temp.prev
                        if not flag:
                            flag = True
                            print("Done")
                        elif flag:
                            continue
                    if flag == False:
                        for i in current.neighbors:
                            if not i.visited and not i.wall:
                                i.visited = True
                                i.prev = current
                                queue.append(i)
                else:
                    if noflag and not flag:
                        Tk().wm_withdraw()
                        messagebox.showinfo("No Solution", "There was no solution")
                        noflag = False
                    else:
                        continue

            win.fill((0, 20, 20))
            for i in range(cols):
                for j in range(rows):
                    spot = grid[i][j]
                    spot.show(win, (44, 62, 80))
                    if spot in path:
                        spot.show(win, (192, 57, 43))
                    elif spot.visited:
                        spot.show(win, (39, 174, 96))
                    if spot in queue:
                        spot.show(win, (44, 62, 80))
                        spot.show(win, (39, 174, 96), 0)
                    if spot == start:
                        spot.show(win, (0, 255, 200))
                    if spot == end:
                        spot.show(win, (0, 120, 255))

            pygame.display.flip()

    dij_strt()


def a_star():
    WIDTH = 500
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* Path Finding Algorithm")

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 255, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)

    class Spot:
        def __init__(self, row, col, width, total_rows):
            self.row = row
            self.col = col
            self.x = row * width
            self.y = col * width
            self.color = WHITE
            self.neighbors = []
            self.width = width
            self.total_rows = total_rows

        def get_pos(self):
            return self.row, self.col

        def is_closed(self):
            return self.color == RED

        def is_open(self):
            return self.color == GREEN

        def is_barrier(self):
            return self.color == BLACK

        def is_start(self):
            return self.color == ORANGE

        def is_end(self):
            return self.color == TURQUOISE

        def reset(self):
            self.color = WHITE

        def make_start(self):
            self.color = ORANGE

        def make_closed(self):
            self.color = RED

        def make_open(self):
            self.color = GREEN

        def make_barrier(self):
            self.color = BLACK

        def make_end(self):
            self.color = TURQUOISE

        def make_path(self):
            self.color = PURPLE

        def draw(self, win):
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

        def update_neighbors(self, grid):
            self.neighbors = []
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
                self.neighbors.append(grid[self.row + 1][self.col])

            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])

            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
                self.neighbors.append(grid[self.row][self.col - 1])

        def __lt__(self, other):
            return False

    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()

    def algorithm(draw, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = h(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                reconstruct_path(came_from, end, draw)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()

        return False

    def make_grid(rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)

        return grid

    def draw_grid(win, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    def draw(win, grid, rows, width):
        win.fill(WHITE)

        for row in grid:
            for spot in row:
                spot.draw(win)

        draw_grid(win, rows, width)
        pygame.display.update()

    def get_clicked_pos(pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    def astar_start(win, width):
        ROWS = 50
        grid = make_grid(ROWS, width)

        start = None
        end = None

        run = True
        while run:
            draw(win, grid, ROWS, width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)

        pygame.quit()

    astar_start(WIN, WIDTH)


if __name__ == "__main__":
    print("For BFS press 1")
    print("For Dijeckstra Press 2")
    print("For A* Press 3")
    choice = int(input())
    if (choice == 1):
        bfs()
    elif(choice == 2):
        dijikstra()
    elif(choice == 3):
        a_star()
    else:
        print("Choose Correct Choice!!!")
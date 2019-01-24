import pygame
import random
import math

pygame.init()
widthS = heightS = 700
screen = pygame.display.set_mode((widthS, widthS))
pygame.display.flip()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board = [[0] * width for _ in range(height)]
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = random.randint(2, 7)
        # значения по умолчанию
        self.left = 25
        self.top = 50
        self.cell_size = (widthS - 2 * self.left) // self.width
        self.square = [[0] * width for _ in range(height)]
        self.shape = [[[]] * width for _ in range(height)]

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                  self.cell_size), 1)

    def createShapes(self):
        for i in range(self.height):
            for j in range(self.width):
                r = random.randint(self.cell_size // 4 - 2, self.cell_size // 2 - 3)
                if self.board[i][j] == 1:
                    pygame.draw.line(screen, pygame.Color("blue"),
                                     (self.left + j * self.cell_size + 2, self.top + i * self.cell_size + 2),
                                     (self.left + (j + 1) * self.cell_size - 2,
                                      self.top + (i + 1) * self.cell_size - 2), 2)
                    pygame.draw.line(screen, pygame.Color("blue"),
                                     (self.left + j * self.cell_size + 2, self.top + (i + 1) * self.cell_size - 2),
                                     (self.left + (j + 1) * self.cell_size - 2,
                                      self.top + i * self.cell_size + 2), 2)
                elif self.board[i][j] == 2:
                    self.shape[i][j] = [(self.left + int((j + 0.5) * self.cell_size),
                                         self.top + int((i + 0.5) * self.cell_size)), int(0.85 * r)]
                else:
                    self.shape[i][j] = self.createPoligon(self.board[i][j], r, (i, j))

    def render2(self):
        for i in range(self.height):
            for j in range(self.width):
                r = random.randint(self.cell_size // 4 - 2, self.cell_size // 2 - 3)
                if self.board[i][j] == 1:
                    pygame.draw.line(screen, pygame.Color("blue"),
                                     (self.left + j * self.cell_size + 2, self.top + i * self.cell_size + 2),
                                     (self.left + (j + 1) * self.cell_size - 2,
                                      self.top + (i + 1) * self.cell_size - 2), 2)
                    pygame.draw.line(screen, pygame.Color("blue"),
                                     (self.left + j * self.cell_size + 2, self.top + (i + 1) * self.cell_size - 2),
                                     (self.left + (j + 1) * self.cell_size - 2,
                                      self.top + i * self.cell_size + 2), 2)
                elif self.board[i][j] == 2:
                    pygame.draw.circle(screen, pygame.Color("red"), self.shape[i][j][0], self.shape[i][j][1], 0)
                else:
                    pygame.draw.polygon(screen, pygame.Color("red"), self.shape[i][j], 0)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
            print(self.squaref(cell))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or y < self.top or x > self.left + self.width * self.cell_size or y > self.top + self.height * self.cell_size:
            return None
        j = (x - self.left) // self.cell_size
        i = (y - self.top) // self.cell_size
        return [i, j]

    def on_click(self, cell_coords):
        if not self.board[cell_coords[0]][cell_coords[1]]:
            self.board[cell_coords[0]][cell_coords[1]] = self.hod + 1
            self.hod = (self.hod + 1) % 2

    def squaref(self, cell_coords):
        s = 0
        for i in range(self.left + cell_coords[1] * self.cell_size + 1,
                       self.left + (cell_coords[1] + 1) * self.cell_size - 1):
            for j in range(self.top + cell_coords[0] * self.cell_size + 1,
                           self.top + (cell_coords[0] + 1) * self.cell_size - 1):
                if screen.get_at((i, j)) != pygame.Color("black"):
                    # print(screen.get_at((i, j)), pygame.Color("black"), (i, j))
                    s += 1
        return s

    def createPoligon(self, n, r, cell_coords):
        angles = []
        points = []
        for i in range(n):
            angles.append(random.randint(0, 359))
        angles.sort()
        for angle in angles:
            points.append((self.left + int((cell_coords[1] + 0.5) * self.cell_size) + int(math.cos(angle / 57) * r),
                           self.top + int((cell_coords[0] + 0.5) * self.cell_size) - math.sin(angle / 57) * r))
        return points


board = Board(20, 20)

board.render()
board.createShapes()
board.render2()
pygame.display.flip()
maxs = 0
for i in range(board.height):
    for j in range(board.width):
        board.square[i][j] = board.squaref((i, j))
        if board.square[i][j] > maxs:
            maxs = board.square[i][j]

print(board.square)
print(board.board)
print(maxs)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    pygame.display.flip()

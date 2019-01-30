import pygame
import random
import math
import sys

pygame.init()
pygame.mixer.init()
global soundVictory, soundLose
soundVictory = [pygame.mixer.Sound("vic_ura_1.wav"), pygame.mixer.Sound("vic_aplodis_2.wav"),
                pygame.mixer.Sound("vic_tarelka_3.wav")]
soundLose = pygame.mixer.Sound("luse_1.wav")
widthS = heightS = 700
screen = pygame.display.set_mode((widthS, widthS))
clock = pygame.time.Clock();
pygame.display.flip()

global screen_rect
screen_rect = (0, 0, widthS, heightS)

all_sprites = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


class Particle(pygame.sprite.Sprite):
    global screen_rect
    # сгенерируем частицы разного размера
    # fire = [load_image("star.png")]
    fire = [pygame.image.load("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.15

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


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
        self.colors = [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow"), pygame.Color("green"),
                       pygame.Color("blue"), pygame.Color("purple"), pygame.Color("pink"), pygame.Color("grey")]
        self.color = [[0] * width for _ in range(height)]
        if self.width > len(self.colors) - 1:
            self.len2 = len(self.colors) - 1
        else:
            self.len2 = self.width
        for i in range(self.height):
            for j in range(self.width):
                self.color[i][j] = (i - j) % (self.len2)
        self.t = 0
        self.time = 0
        self.timer = 15

        self.clicked = False

        self.maxs = 0
        self.maxs2 = 0
        self.maxij = []
        self.maxij2 = []

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
                    self.shape[i][j] = [(self.left + int((i + 0.5) * self.cell_size),
                                         self.top + int((j + 0.5) * self.cell_size)), int(0.85 * r)]
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
                    pygame.draw.circle(screen, self.colors[self.color[i][j]], self.shape[i][j][0], self.shape[i][j][1],
                                       0)
                else:
                    pygame.draw.polygon(screen, self.colors[self.color[i][j]], self.shape[i][j], 0)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and not self.clicked:
            self.on_click(cell)
            print(self.squaref(cell), cell)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or y < self.top or x > self.left + self.width * self.cell_size or y > self.top + self.height * self.cell_size:
            return None
        i = (x - self.left) // self.cell_size
        j = (y - self.top) // self.cell_size
        return [i, j]

    def on_click(self, cell_coords):
        global score, victory, soundVictory, soundLose
        self.clicked = True
        victory = self.square[cell_coords[0]][cell_coords[1]] == self.maxs
        if victory:
            pygame.mixer.Sound.play(random.choice(soundVictory))
            self.maxij = cell_coords
            score += (1000 * self.timer // (self.maxs - self.maxs2) + 1) * self.width * self.height
            create_particles(pygame.mouse.get_pos())

        else:
            pygame.mixer.Sound.play(soundLose)
            self.color[cell_coords[0]][cell_coords[1]] = len(self.colors) - 1

    def squaref(self, cell_coords):
        s = 0
        for i in range(self.left + cell_coords[0] * self.cell_size + 1,
                       self.left + (cell_coords[0] + 1) * self.cell_size - 1):
            for j in range(self.top + cell_coords[1] * self.cell_size + 1,
                           self.top + (cell_coords[1] + 1) * self.cell_size - 1):
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
            points.append((self.left + int((cell_coords[0] + 0.5) * self.cell_size) + int(math.cos(angle / 57) * r),
                           self.top + int((cell_coords[1] + 0.5) * self.cell_size) - math.sin(angle / 57) * r))
        return points

    def changeColor(self, tick):
        self.t += tick
        self.time += tick
        if self.t > 200:
            self.color[self.maxij[0]][self.maxij[1]] = (self.color[self.maxij[0]][self.maxij[1]] + 1) % self.len2
            self.t = 0

    def updateTimer(self, tick):
        global victory
        self.t += tick
        if self.t > 1000:
            self.timer -= 1
            self.t = 0

        if not self.timer:
            self.clicked = True
            victory = False


def newBoard(razmer):
    global victory
    board = Board(razmer, razmer)

    screen.fill((0, 0, 0))
    board.render()
    board.createShapes()
    board.render2()
    pygame.display.flip()

    for i in range(board.height):
        for j in range(board.width):
            board.square[i][j] = board.squaref((i, j))
            if board.square[i][j] > board.maxs:
                board.maxij2 = board.maxij
                board.maxs2 = board.maxs
                board.maxij = [i, j]
                board.maxs = board.square[i][j]
            elif board.square[i][j] > board.maxs2 and board.square[i][j] != board.maxs:
                board.maxij2 = [i, j]
                board.maxs2 = board.square[i][j]

    print(board.square)
    print(board.board)
    print(board.maxs, board.maxij)
    print(board.maxs2, board.maxij2)
    running = True
    while running:
        tick = clock.tick(100)
        screen.fill((0, 0, 0))
        board.render()
        board.render2()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
        if board.clicked:
            board.changeColor(tick)
            running = all_sprites or board.time < 1500
        else:
            board.updateTimer(tick)

        font = pygame.font.Font(None, 50)
        textScore = font.render("Очки: " + str(score), 1, (100, 255, 100))
        screen.blit(textScore, (5, 5))

        textTimer = font.render("Время: " + str(board.timer), 1, (100, 255, 100))
        screen.blit(textTimer, (500, 5))

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
    print("a")


def play():
    global victory
    victory = True
    global score
    score = 0
    razmer = 2
    i = 0
    while victory:
        if i == razmer:
            razmer += 1
            i = 0
        newBoard(razmer)
        i += 1
    end()


def begin():
    pass

def drawMenu():
    pass



def end():
    global score, name
    name = ''
    save_rect = pygame.Rect(370, 500, 300, 100)
    not_save_rect = pygame.Rect(30, 500, 300, 100)
    drawEnd()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_rect = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
                    if save_rect.contains(mouse_rect):
                        saveRecord()
                    elif not_save_rect.contains(mouse_rect):
                        print("not save")

            if event.type == pygame.KEYDOWN:
                print(event)
                if event.unicode == '\x08':
                    if name:
                        name = name[0: -1]
                        drawEnd()
                elif event.unicode == '\r':
                    saveRecord()
                elif len(name) < 10:
                    name += event.unicode
                    drawEnd()

            pygame.display.flip()

def drawEnd():
    global score, name
    screen.fill((0, 0, 0))
    font1 = pygame.font.Font(None, 100)
    font2 = pygame.font.Font(None, 50)
    textScore = font1.render("Очки: " + str(score), 1, (100, 255, 100))
    screen.blit(textScore, ((700 - 37 * len("Очки: " + str(score))) // 2, 30))

    textVvedite = font2.render("Введите ваше имя", 1, (100, 255, 100))
    screen.blit(textVvedite, (190, 250))

    textName = font2.render(name, 1, (100, 255, 100))
    screen.blit(textName, (110, 320))

    textSave = font2.render("сохранить", 1, (100, 255, 100))
    screen.blit(textSave, (435, 530))

    textNotSave = font2.render("не сохранять", 1, (100, 255, 100))
    screen.blit(textNotSave, (65, 530))

    name_rect = pygame.Rect(100, 300, 500, 75)
    pygame.draw.rect(screen, pygame.Color("white"), name_rect, 5)

    save_rect = pygame.Rect(370, 500, 300, 100)
    pygame.draw.rect(screen, pygame.Color("white"), save_rect, 5)

    not_save_rect = pygame.Rect(30, 500, 300, 100)
    pygame.draw.rect(screen, pygame.Color("white"), not_save_rect, 5)
    pygame.display.flip()


def saveRecord():
    global score, name
    f = open("records", 'a', encoding="utf8")
    f.write(name + " " + str(score) + "\n")


play()

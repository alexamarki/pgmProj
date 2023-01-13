import pygame
import random

(width, height) = (320, 640)
all_sprites = pygame.sprite.Group()
current_tetromino = []
tickSpeed = 200
tempTick = 200

classicBase = [[' ' for x in range(10)] for y in range(20)]
class tetrominoBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        screen.blit(self.image, (self.x * 32, self.y * 32))

class tableHandler():
    def convertToFallen(self):
        for i in current_tetromino:
            classicBase[i[1]][i[0]] = classicBase[i[1]][i[0]].lower()
        current_tetromino.clear()
        global tickSpeed
        tickSpeed = 200
    def lineEraser(self):
        for i in range(19, 0, -1):
            if ' ' not in classicBase[i]:
                for it in range(10):
                    classicBase[i][it] = ' '
                for j in range(i, 9, -1):
                    for l in range(10):
                        if classicBase[j-1][l].islower():
                            item = classicBase[j-1][l]
                            classicBase[j-1][l] = ' '
                            print(j - 1)
                            classicBase[j][l] = item


class screenRefresh():
    def refresh(self):
            all_sprites.empty()
            for y in range(20):
                for x in range(10):
                    if classicBase[y][x] != ' ':
                        block = tetrominoBlock(x, y, classicBase[y][x].upper() + 'mino.png')
                        block.update()

class tetrominoDisplay():
    def __init__(self, x=0, y=0, letter=' '):
        self.x, self.y = x, y
        self.letter = letter
        self.coords = {
            'l': [(x + 2, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)],
            'j': [(x, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)],
            'i': [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y + 1)],
            's': [(x + 1, y), (x + 2, y), (x, y + 1), (x + 1, y + 1)],
            'z': [(x, y), (x + 1, y), (x + 1, y + 1), (x + 2, y + 1)],
            't': [(x + 1, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)],
            'o': [(x + 1, y), (x + 2, y), (x + 1, y + 1), (x + 2, y + 1)]
        }

    def display(self):
        x1, y1 = (self.coords.get(self.letter)[0])
        x2, y2 = (self.coords.get(self.letter)[1])
        x3, y3 = (self.coords.get(self.letter)[2])
        x4, y4 = (self.coords.get(self.letter)[3])
        classicBase[y1][x1] = self.letter.upper()
        classicBase[y2][x2] = self.letter.upper()
        classicBase[y3][x3] = self.letter.upper()
        classicBase[y4][x4] = self.letter.upper()
        current_tetromino.append([x1, y1])
        current_tetromino.append([x2, y2])
        current_tetromino.append([x3, y3])
        current_tetromino.append([x4, y4])
        screenRefresh().refresh()

    def movementCheck(self, yMod, xMod):
        allowed = True
        for i in current_tetromino:
            if i[1] + yMod >= 20 or i[0] + xMod >= 10 or i[0] - xMod < 0:
                allowed = False
        if allowed:
            for i in current_tetromino:
                if classicBase[i[1] + yMod][i[0] + xMod] in ('j','l','i','o','s','z','t'):
                    allowed = False
        if allowed:
            self.move(yMod, xMod)
        elif not allowed and not xMod:
            tableHandler().convertToFallen()
            tableHandler().lineEraser()

    def move(self, yMod, xMod):
        a = []
        for i in current_tetromino:
            i[1] += yMod
            i[0] += xMod
            a.append(classicBase[i[1] - yMod][i[0] - xMod])
            classicBase[i[1] - yMod][i[0] - xMod] = ' '
        n = 0
        for i in current_tetromino:
            classicBase[i[1]][i[0]] = a[n]
            n+=1

    def rotationCheck(self, n):
        allowed = True
        for i in current_tetromino:
            if i[0] - self.x + self.y >= 20 or (n - 1) - (i[1] - self.y) + self.x >= 10 or (n - 1) - (i[1] - self.y) + self.x < 0:
                allowed = False
        if allowed:
            for i in current_tetromino:
                if classicBase[i[0] - self.x + self.y][(n - 1) - (i[1] - self.y) + self.x] in ('j','l','i','o','s','z','t'):
                    allowed = False
        if allowed:
            self.rotate(n)

    def rotate(self, n):
        a=[]
        for i in current_tetromino:
            a.append(classicBase[i[1]][i[0]])
            classicBase[i[1]][i[0]] = ' '
            i[1], i[0] = i[0] - self.x + self.y, (n - 1) - (i[1] - self.y) + self.x
        n = 0
        for i in current_tetromino:
            classicBase[i[1]][i[0]] = a[n]
            n += 1
        screenRefresh().refresh()



screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetromino Test')
screen.fill((255, 255, 255))
x = 4
y = 0
xCorner = x
yCorner = y
running = True
keyed = ''
rotator = ''
elapsedT = 0
timeClock = pygame.time.Clock()
movementStop = False
while running:
    for i in current_tetromino:
        if i[1] == 19:
            movementStop, movementPauseL, movementPauseR, rotLock = True, True, True, True
        if i[0] == 9:
            movementPauseR = True
        if i[0] == 0:
            movementPauseL = True
    dt = timeClock.tick()
    elapsedT += dt
    if elapsedT > tickSpeed and not movementStop:
        tetrominoDisplay().movementCheck(1, 0)
        screenRefresh().refresh()
        yCorner += 1
        elapsedT = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not movementPauseL:
                tetrominoDisplay().movementCheck(0, -1)
                screenRefresh().refresh()
                xCorner -= 1
            elif event.key == pygame.K_RIGHT and not movementPauseR:
                tetrominoDisplay().movementCheck(0, 1)
                screenRefresh().refresh()
                xCorner += 1
            elif event.key == pygame.K_DOWN:
                tempTick = tickSpeed
                tickSpeed = 10
            elif event.key == pygame.K_UP and rotator and not rotLock:
                if rotator == 'i':
                    tetrominoDisplay(xCorner, yCorner, rotator).rotationCheck(4)
                elif rotator == 'o':
                    screenRefresh().refresh()
                else:
                    tetrominoDisplay(xCorner, yCorner, rotator).rotationCheck(3)
            elif event.key in (pygame.K_o, pygame.K_l, pygame.K_j, pygame.K_s, pygame.K_z, pygame.K_i, pygame.K_t):
                if event.key in (pygame.K_o, pygame.K_i):
                    x = 3
                else:
                    x = 4
                keyed = chr(event.key)
                xCorner, yCorner = x, y
                movementStop = False
                for i in current_tetromino:
                    classicBase[i[1]][i[0]] = ' '
                current_tetromino.clear()
            if keyed:
                tetrominoDisplay(x, y, keyed).display()
                rotator, keyed = keyed, ''
    if not movementStop:
        movementPauseL, movementPauseR, rotLock = False, False, False
    else:
        tableHandler().convertToFallen()
        tickSpeed = tempTick
        tableHandler().lineEraser()
    screen.fill((255, 255, 255))
    screenRefresh().refresh()

    pygame.display.flip()

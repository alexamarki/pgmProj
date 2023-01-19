import pygame
import random

pygame.font.init()
blockScale = 24
gameWidth, gameHeight = 40, 40
global classicBase

with open("input.txt", "r") as file:
    classicBase = [[x for x in line.split()] for line in file]
    gameHeight = len(classicBase)
    gameWidth = len(classicBase[0])

(width, height) = (60 * blockScale, 40 * blockScale)
all_sprites = pygame.sprite.Group()
current_tetromino = []
tickSpeed = (1 / 3) * 1000
tempTick = tickSpeed
boardCentreX = 20
boardCentreY = 20
boardTopX = boardCentreX - gameWidth / 2
boardTopY = boardCentreY - gameHeight / 2
rotor = 0
score = 0
holdContainer = ''
nextLetter = ''
holdPause = False


class randomiser():
    def randomiseletter(self):
        global nextLetter
        nextLetter = random.choice(['j', 'l', 'o', 'i', 's', 'z', 't'])
        return nextLetter

    def defineSpawn(self, keyer=''):
        if not keyer:
            keyer = nextLetter
            self.randomiseletter()
        if keyer in ('i', 'o'):
            return keyer, (gameWidth - 4) // 2
        else:
            return keyer, (gameWidth - 4) // 2 + 1


class infoBlock():
    def displayTestTetros(self, letter, xdisc, ydisc):
        x1, y1 = (tetrominoDisplay().coords.get(letter)[0])
        x2, y2 = (tetrominoDisplay().coords.get(letter)[1])
        x3, y3 = (tetrominoDisplay().coords.get(letter)[2])
        x4, y4 = (tetrominoDisplay().coords.get(letter)[3])
        tetrominoBlock(x1 + xdisc, y1 + ydisc, letter + 'mino.png', False).update()
        tetrominoBlock(x2 + xdisc, y2 + ydisc, letter + 'mino.png', False).update()
        tetrominoBlock(x3 + xdisc, y3 + ydisc, letter + 'mino.png', False).update()
        tetrominoBlock(x4 + xdisc, y4 + ydisc, letter + 'mino.png', False).update()


class tetrominoBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, screen=True):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        if screen:
            self.x += boardTopX
            self.y += boardTopY
            self.rotationSit()

    def rotationSit(self):
        if rotor % 4 == 1:
            pass
        elif rotor % 4 == 2:
            self.x, self.y = boardCentreX + boardCentreY - self.y - 1, -boardCentreX + boardCentreY + self.x
        elif rotor % 4 == 3:
            self.x, self.y = boardCentreX * 2 - self.x - 1, boardCentreY * 2 - self.y - 1
        else:
            self.x, self.y = boardCentreX - boardCentreY + self.y, boardCentreX + boardCentreY - self.x - 1

    def update(self):
        screen.blit(self.image, ((self.x) * blockScale, (self.y) * blockScale))


class tableHandler():
    def convertToFallen(self):
        for i in current_tetromino:
            classicBase[i[1]][i[0]] = classicBase[i[1]][i[0]].lower()
        current_tetromino.clear()
        global tickSpeed
        tickSpeed = 300
        global holdPause
        holdPause = False

    def lineEraser(self):
        score = 0
        count = 0
        for i in range(gameHeight):
            if 'BACK' not in classicBase[i]:
                count += 1
                for it in range(gameWidth):
                    if classicBase[i][it] != '*':
                        classicBase[i][it] = 'BACK'
                for j in range(i, gameHeight - 1):
                    for l in range(15, gameWidth - 15):
                        if classicBase[j - 1][l].islower():
                            item = classicBase[j - 1][l]
                            if classicBase[j - 1][l] != '*':
                                classicBase[j - 1][l] = 'BACK'
                                classicBase[j][l] = item
        if count == 1:
            score = 40
        elif count == 2:
            score = 100
        elif count == 3:
            score = 200
        elif score == 4:
            score = 300
        return score, count


class screenRefresh():
    def refresh(self):
        all_sprites.empty()
        for y in range(gameHeight):
            for x in range(gameWidth):
                if classicBase[y][x] not in ('*', 'BACK'):
                    block = tetrominoBlock(x, y, classicBase[y][x].upper() + 'mino.png')
                    block.update()


class tetrominoDisplay():
    def __init__(self, x=0, y=0, letter=''):
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
            if i[1] + yMod >= gameHeight or i[0] + xMod >= gameWidth or i[0] - xMod < 0:
                allowed = False
        if allowed:
            for i in current_tetromino:
                if classicBase[i[1] + yMod][i[0] + xMod] in ('j', 'l', 'i', 'o', 's', 'z', 't', '*'):
                    allowed = False
        if allowed:
            self.move(yMod, xMod)
        elif not allowed and not xMod:
            tableHandler().convertToFallen()
            return tableHandler().lineEraser()
        return 0, 0

    def move(self, yMod, xMod):
        a = []
        for i in current_tetromino:
            i[1] += yMod
            i[0] += xMod
            a.append(classicBase[i[1] - yMod][i[0] - xMod])
            classicBase[i[1] - yMod][i[0] - xMod] = 'BACK'
        n = 0
        for i in current_tetromino:
            classicBase[i[1]][i[0]] = a[n]
            n += 1

    def rotationCheck(self, n):
        allowed = True
        for i in current_tetromino:
            if i[0] - self.x + self.y >= gameHeight or (n - 1) - (i[1] - self.y) + self.x >= gameWidth or (n - 1) - (
                    i[1] - self.y) + self.x < 0:
                allowed = False
        if allowed:
            for i in current_tetromino:
                if classicBase[i[0] - self.x + self.y][(n - 1) - (i[1] - self.y) + self.x] in (
                        'j', 'l', 'i', 'o', 's', 'z', 't', '*'):
                    allowed = False
        if allowed:
            self.rotate(n)

    def rotate(self, n):
        a = []
        for i in current_tetromino:
            a.append(classicBase[i[1]][i[0]])
            classicBase[i[1]][i[0]] = 'BACK'
            i[1], i[0] = i[0] - self.x + self.y, (n - 1) - (i[1] - self.y) + self.x
        n = 0
        for i in current_tetromino:
            classicBase[i[1]][i[0]] = a[n]
            n += 1
        screenRefresh().refresh()


nextLetter = randomiser().randomiseletter()
font = pygame.font.SysFont('boldTestFont.ttf', 24)
img = font.render('SCORE', True, (0, 23, 43))
rect = img.get_rect()
pygame.draw.rect(img, (255, 255, 255), rect, 1)
img2 = font.render('NEXT', True, (0, 23, 43))
rect = img2.get_rect()
pygame.draw.rect(img, (255, 255, 255), rect, 1)
img3 = font.render('HOLD', True, (0, 23, 43))
rect = img3.get_rect()
pygame.draw.rect(img, (255, 255, 255), rect, 1)

bg = pygame.image.load('test_bg.PNG')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris-0')
screen.fill((255, 255, 255))
x = (gameWidth - 4) // 2 + 1
y = 0
xCorner = x
yCorner = y
running = True
keyed = ''
rotator = ''
elapsedT = 0
timeClock = pygame.time.Clock()
movementStop = False
holdPause = False


class holding():
    def holder(self):
        if not holdContainer:
            keyed, x = randomiser().defineSpawn()
        else:
            keyed = holdContainer
            _, x = randomiser().defineSpawn(keyed)
        xCorner, yCorner = x, y
        movementStop = False
        for i in current_tetromino:
            classicBase[i[1]][i[0]] = 'BACK'
        current_tetromino.clear()
        tetrominoDisplay(x, y, keyed).display()
        return keyed, xCorner, yCorner, movementStop


class keyMovement():
    def moveDown(self):
        pass

    def moveRight(self):
        pass

    def moveLeft(self):
        pass

    def moveDownQuick(self):
        pass


linesCleared = 0
stage = 0
while running:
    ROTATESCREEN = False
    stage = int(linesCleared / 10)
    if tickSpeed != 0.05:
        tickSpeed = (1 / (3 + stage)) * 1000
        tempTick = tickSpeed
    else:
        tempTick = (1 / (3 + stage)) * 1000
    imgScore = font.render(str(score), True, (0, 23, 43))
    rect = imgScore.get_rect()
    pygame.draw.rect(img, (255, 255, 255), rect, 1)
    for i in current_tetromino:
        if i[1] == gameHeight - 1:
            movementStop, movementPauseL, movementPauseR, rotLock = True, True, True, True
        if i[0] == gameWidth - 1:
            movementPauseR = True
        if i[0] == 0:
            movementPauseL = True
    dt = timeClock.tick()
    elapsedT += dt
    if elapsedT > tickSpeed and not movementStop:
        scoreTemp, linesClearedTemp = tetrominoDisplay().movementCheck(1, 0)
        score += scoreTemp * (1 + stage)
        linesCleared += linesClearedTemp
        screenRefresh().refresh()
        yCorner += 1
        elapsedT = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not movementPauseL:
                scoreTemp, linesClearedTemp = tetrominoDisplay().movementCheck(0, -1)
                score += scoreTemp * (1 + stage)
                linesCleared += linesClearedTemp
                screenRefresh().refresh()
                xCorner -= 1
            elif event.key == pygame.K_RIGHT and not movementPauseR:
                scoreTemp, linesClearedTemp = tetrominoDisplay().movementCheck(0, 1)
                score += scoreTemp * (1 + stage)
                linesCleared += linesClearedTemp
                screenRefresh().refresh()
                xCorner += 1
            elif event.key == pygame.K_DOWN:
                tempTick = tickSpeed
                tickSpeed = 0.05
            elif event.key == pygame.K_UP and rotator and not rotLock:
                if rotator == 'i':
                    tetrominoDisplay(xCorner, yCorner, rotator).rotationCheck(4)
                elif rotator == 'o':
                    screenRefresh().refresh()
                else:
                    tetrominoDisplay(xCorner, yCorner, rotator).rotationCheck(3)
            elif event.key == pygame.K_h and not holdPause:
                holdPause = True
                keyed, xCorner, yCorner, movementStop = holding().holder()
                holdContainer = rotator
                rotator, keyed = keyed, ''
    if not movementStop:
        movementPauseL, movementPauseR, rotLock = False, False, False
    else:
        tableHandler().convertToFallen()
        tickSpeed = tempTick
        scoreTemp, linesClearedTemp = tableHandler().lineEraser()
        score += scoreTemp * (1 + stage)
        linesCleared += linesClearedTemp
        holdPause = False
    if not current_tetromino:
        rotor += 1
        classicBase = list(zip(*classicBase))[::-1]
        classicBase = list([list(elem) for elem in classicBase])
        keyed, x = randomiser().defineSpawn()
        xCorner, yCorner = x, y
        movementStop = False
        tetrominoDisplay(x, y, keyed).display()
        rotator, keyed = keyed, ''

    screen.blit(bg, (0, 0))
    screenRefresh().refresh()
    screen.blit(img, (50 * blockScale, 5 * blockScale))
    screen.blit(img2, (50 * blockScale, 10 * blockScale))
    screen.blit(img3, (50 * blockScale, 15 * blockScale))
    screen.blit(imgScore, (50 * blockScale, 7 * blockScale))
    if holdContainer:
        infoBlock().displayTestTetros(holdContainer, 50, 17)
    infoBlock().displayTestTetros(nextLetter, 50, 12)
    pygame.display.flip()

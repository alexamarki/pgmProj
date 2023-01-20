import constants, variables, guiTetris
import random

class randomiser():
    def randomiseletter(self):
        variables.nextLetter = random.choice(constants.letters)

    def defineSpawn(self, keyer=''):
        if not keyer:
            keyer = variables.nextLetter
            self.randomiseletter()
        if keyer in ('i', 'o'):
            return keyer, (variables.gameWidth - 4) // 2
        else:
            return keyer, (variables.gameWidth - 4) // 2 + 1

class infoBlock():
    def displayTestTetros(self, letter, xdisc, ydisc, screen):
        x1, y1 = (constants.tetrominod(0, 0).get(letter)[0])
        x2, y2 = (constants.tetrominod(0, 0).get(letter)[1])
        x3, y3 = (constants.tetrominod(0, 0).get(letter)[2])
        x4, y4 = (constants.tetrominod(0, 0).get(letter)[3])
        guiTetris.tetrominoBlock(x1 + xdisc, y1 + ydisc, letter + 'mino.png', False).update(screen)
        guiTetris.tetrominoBlock(x2 + xdisc, y2 + ydisc, letter + 'mino.png', False).update(screen)
        guiTetris.tetrominoBlock(x3 + xdisc, y3 + ydisc, letter + 'mino.png', False).update(screen)
        guiTetris.tetrominoBlock(x4 + xdisc, y4 + ydisc, letter + 'mino.png', False).update(screen)

class tableHandler():
    def convertToFallen(self):
        for i in variables.current_tetromino:
            variables.classicBase[i[1]][i[0]] = variables.classicBase[i[1]][i[0]].lower()
        variables.current_tetromino.clear()
        variables.tickSpeed = (1 / (3 + variables.stage)) * 1000
        variables.holdPause = False

    def lineEraser(self):
        score = 0
        count = 0
        for _ in range(4):
            for i in range(0, 15):
                if 'BACK' not in variables.classicBase[i]:
                    count += 1
                    for it in range(15, variables.gameWidth - 15):
                        variables.classicBase[i][it] = 'BACK'
                    for j in range(i, 0, -1):
                        for l in range(15, variables.gameWidth - 15):
                            if variables.classicBase[j-1][l].islower():
                                item = variables.classicBase[j-1][l]
                                variables.classicBase[j-1][l] = 'BACK'
                                variables.classicBase[j][l] = item
            variables.classicBase = list(zip(*variables.classicBase))[::-1]
            variables.classicBase = list([list(elem) for elem in variables.classicBase])
        if count == 1:
            score = 40
        elif count == 2:
            score = 100
        elif count == 3:
            score = 200
        elif count >= 4:
            score = 300 * (count / 4)
        return score, count


class screenRefresh():
    def refresh(self, screen):
        variables.all_sprites.empty()
        for y in range(variables.gameHeight):
            for x in range(variables.gameWidth):
                if variables.classicBase[y][x] not in ('*', 'BACK'):
                    block = guiTetris.tetrominoBlock(x, y, variables.classicBase[y][x].upper() + 'mino.png')
                    block.update(screen)

class tetrominoDisplay():
    def __init__(self, x=0, y=0, letter=''):
        self.x, self.y = x, y
        self.letter = letter

    def display(self):
        x1, y1 = (constants.tetrominod(self.x, self.y).get(self.letter)[0])
        x2, y2 = (constants.tetrominod(self.x, self.y).get(self.letter)[1])
        x3, y3 = (constants.tetrominod(self.x, self.y).get(self.letter)[2])
        x4, y4 = (constants.tetrominod(self.x, self.y).get(self.letter)[3])
        # if classicBase[y1][x1] != 'BACK':
        #     finale().deathScreen()
        # elif classicBase[y1][x1] != 'BACK':
        #     finale().deathScreen()
        # elif classicBase[y1][x1] != 'BACK':
        #     finale().deathScreen()
        # elif classicBase[y1][x1] != 'BACK':
        #     finale().deathScreen()
        variables.classicBase[y1][x1] = self.letter.upper()
        variables.classicBase[y2][x2] = self.letter.upper()
        variables.classicBase[y3][x3] = self.letter.upper()
        variables.classicBase[y4][x4] = self.letter.upper()
        variables.current_tetromino.append([x1, y1])
        variables.current_tetromino.append([x2, y2])
        variables.current_tetromino.append([x3, y3])
        variables.current_tetromino.append([x4, y4])
        screenRefresh().refresh(variables.screen)

    def movementCheck(self, yMod, xMod):
        allowed = True
        for i in variables.current_tetromino:
            if i[1] + yMod >= variables.gameHeight or i[0] + xMod >= variables.gameWidth or i[0] - xMod < 0:
                allowed = False
        if allowed:
            for i in variables.current_tetromino:
                if variables.classicBase[i[1] + yMod][i[0] + xMod] in ('j', 'l', 'i', 'o', 's', 'z', 't', '*'):
                    allowed = False
        if allowed:
            self.move(yMod, xMod)
        elif not allowed and not xMod:
            tableHandler().convertToFallen()
            return *tableHandler().lineEraser(), False
        else:
            return 0, 0, False
        return 0, 0, True

    def move(self, yMod, xMod):
        a = []
        for i in variables.current_tetromino:
            i[1] += yMod
            i[0] += xMod
            a.append(variables.classicBase[i[1] - yMod][i[0] - xMod])
            variables.classicBase[i[1] - yMod][i[0] - xMod] = 'BACK'
        n = 0
        for i in variables.current_tetromino:
            variables.classicBase[i[1]][i[0]] = a[n]
            n += 1

    def rotationCheck(self, n):
        allowed = True
        for i in variables.current_tetromino:
            if i[0] - self.x + self.y >= variables.gameHeight or (n - 1) - (i[1] - self.y) + self.x >= variables.gameWidth or (n - 1) - (
                    i[1] - self.y) + self.x < 0:
                allowed = False
        if allowed:
            for i in variables.current_tetromino:
                if variables.classicBase[i[0] - self.x + self.y][(n - 1) - (i[1] - self.y) + self.x] in (
                        'j', 'l', 'i', 'o', 's', 'z', 't', '*'):
                    allowed = False
        if allowed:
            self.rotate(n)

    def rotate(self, n):
        a = []
        for i in variables.current_tetromino:
            a.append(variables.classicBase[i[1]][i[0]])
            variables.classicBase[i[1]][i[0]] = 'BACK'
            i[1], i[0] = i[0] - self.x + self.y, (n - 1) - (i[1] - self.y) + self.x
        n = 0
        for i in variables.current_tetromino:
            variables.classicBase[i[1]][i[0]] = a[n]
            n += 1
        screenRefresh().refresh(variables.screen)


class holding():
    def holder(self):
        if not variables.holdContainer:
            keyed, x = randomiser().defineSpawn()
        else:
            keyed = variables.holdContainer
            _, x = randomiser().defineSpawn(keyed)
        xCorner, yCorner = x, constants.startCornerY
        movementStop = False
        for i in variables.current_tetromino:
            variables.classicBase[i[1]][i[0]] = 'BACK'
        variables.current_tetromino.clear()
        tetrominoDisplay(x, constants.startCornerY, keyed).display()
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
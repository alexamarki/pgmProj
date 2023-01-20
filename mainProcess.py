import pygame
import tableManagementTetris, variables
import constants
pygame.font.init()
gameWidth, gameHeight = 40, 40
boardTopX = constants.boardCentreX - gameWidth / 2
boardTopY = constants.boardCentreY - gameHeight / 2
bg = pygame.image.load('test_bg.PNG')

pygame.display.set_caption('Tetris-0')
xCorner = (gameWidth - 4) // 2 + 1
yCorner = constants.startCornerY


elapsedT = 0
timeClock = pygame.time.Clock()


# class finale():
#     def deathScreen(self):
#         print('lmao')

tableManagementTetris.randomiser().randomiseletter()

running = True
while running:
    ROTATESCREEN = False
    variables.stage = int(variables.linesCleared / 10)
    imgScore = constants.font.render(str(variables.score), True, (0, 23, 43))
    rect = imgScore.get_rect()
    for i in variables.current_tetromino:
        if i[1] == gameHeight - 1:
            variables.movementStop, movementPauseL, movementPauseR, rotLock = True, True, True, True
        if i[0] == gameWidth - 1:
            movementPauseR = True
        if i[0] == 0:
            movementPauseL = True
    dt = timeClock.tick()
    elapsedT += dt
    if elapsedT > variables.tickSpeed and not variables.movementStop:
        scoreTemp, linesClearedTemp, moveFurther = tableManagementTetris.tetrominoDisplay().movementCheck(1, 0)
        variables.score += scoreTemp * (1 + variables.stage)
        variables.linesCleared += linesClearedTemp
        tableManagementTetris.screenRefresh().refresh(variables.screen)
        if moveFurther:
            yCorner += 1
            elapsedT = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not movementPauseL:
                scoreTemp, linesClearedTemp, moveFurther = tableManagementTetris.tetrominoDisplay().movementCheck(0, -1)
                variables.score += scoreTemp * (1 + variables.stage)
                variables.linesCleared += linesClearedTemp
                tableManagementTetris.screenRefresh().refresh(variables.screen)
                if moveFurther:
                    xCorner -= 1
            elif event.key == pygame.K_RIGHT and not movementPauseR:
                scoreTemp, linesClearedTemp, moveFurther = tableManagementTetris.tetrominoDisplay().movementCheck(0, 1)
                variables.score += scoreTemp * (1 + variables.stage)
                variables.linesCleared += linesClearedTemp
                tableManagementTetris.screenRefresh().refresh(variables.screen)
                if moveFurther:
                    xCorner += 1
            elif event.key == pygame.K_DOWN:
                variables.tickSpeed = constants.dropTick
            elif event.key == pygame.K_UP and variables.rotator and not rotLock:
                if variables.rotator == 'i':
                    tableManagementTetris.tetrominoDisplay(xCorner, yCorner, variables.rotator).rotationCheck(4)
                elif variables.rotator == 'o':
                    tableManagementTetris.screenRefresh().refresh(variables.screen)
                else:
                    tableManagementTetris.tetrominoDisplay(xCorner, yCorner, variables.rotator).rotationCheck(3)
            elif event.key == pygame.K_h and not variables.holdPause:
                variables.holdPause = True
                variables.keyed, xCorner, yCorner, variables.movementStop = tableManagementTetris.holding().holder()
                variables.holdContainer = variables.rotator
                variables.rotator, variables.keyed = variables.keyed, ''
    if not variables.movementStop:
        movementPauseL, movementPauseR, rotLock = False, False, False
    else:
        tableManagementTetris.tableHandler().convertToFallen()
        scoreTemp, linesClearedTemp = tableManagementTetris.tableHandler().lineEraser()
        variables.score += scoreTemp * (1 + variables.stage)
        variables.linesCleared += linesClearedTemp
        variables.holdPause = False
    if not variables.current_tetromino:
        variables.rotor += 1
        variables.classicBase = list(zip(*variables.classicBase))[::-1]
        variables.classicBase = list([list(elem) for elem in variables.classicBase])
        variables.keyed, x = tableManagementTetris.randomiser().defineSpawn()
        xCorner, yCorner = x, constants.startCornerY
        variables.movementStop = False
        tableManagementTetris.tetrominoDisplay(x, constants.startCornerY, variables.keyed).display()
        variables.rotator, variables.keyed = variables.keyed, ''

    variables.screen.blit(bg, (0, 0))
    tableManagementTetris.screenRefresh().refresh(variables.screen)
    variables.screen.blit(constants.img, (50 * constants.blockScale, 5 * constants.blockScale))
    variables.screen.blit(constants.img2, (50 * constants.blockScale, 10 * constants.blockScale))
    variables.screen.blit(constants.img3, (50 * constants.blockScale, 15 * constants.blockScale))
    variables.screen.blit(imgScore, (50 * constants.blockScale, 7 * constants.blockScale))
    if variables.holdContainer:
        tableManagementTetris.infoBlock().displayTestTetros(variables.holdContainer, 50, 17, variables.screen)
    tableManagementTetris.infoBlock().displayTestTetros(variables.nextLetter, 50, 12, variables.screen)
    pygame.display.flip()

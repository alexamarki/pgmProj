import pygame
import tableManagementTetris, variables, guiScreens
import constants

boardTopX = constants.boardCentreX - variables.gameWidth / 2
boardTopY = constants.boardCentreY - variables.gameHeight / 2
pygame.display.set_caption('The Tetris experience')
xCorner = (variables.gameWidth - 4) // 2 + 1
yCorner = constants.startCornerY
elapsedT = 0
timeClock = pygame.time.Clock()

tableManagementTetris.randomiser().randomiseletter()
variables.pygame.mixer.music.play(-1)

running = True
while running:
    variables.screen.blit(variables.bg, (0, 0))
    if variables.gameState == 'mainMenu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    guiScreens.screens().setScreenTo(constants.tet, 'Tetris', 'Tetris')
                elif event.key == pygame.K_l:
                    guiScreens.screens().setScreenTo(constants.leaderBoard, 'High Scores', 'leaders')
    elif variables.gameState == 'Tet-a-tet' or variables.gameState == 'Tetris':
        ROTATESCREEN = False
        variables.stage = int(variables.linesCleared / 10)
        imgScore = constants.font.render(str(variables.score), True, (0, 23, 43))
        rect = imgScore.get_rect()
        for i in variables.current_tetromino:
            if i[1] == variables.gameHeight - 1:
                variables.movementStop, movementPauseL, movementPauseR, rotLock = True, True, True, True
            if i[0] == variables.gameWidth - 1:
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
                elif event.key in (pygame.K_DOWN, pygame.K_SPACE):
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
                elif event.key == pygame.K_SLASH and variables.gameState == 'Tetris':
                    variables.rotor += 1
        if not variables.movementStop:
            movementPauseL, movementPauseR, rotLock = False, False, False
        else:
            tableManagementTetris.tableHandler().convertToFallen()
            scoreTemp, linesClearedTemp = tableManagementTetris.tableHandler().lineEraser()
            variables.score += scoreTemp * (1 + variables.stage)
            variables.linesCleared += linesClearedTemp
            variables.holdPause = False
        if not variables.current_tetromino:
            if variables.gameState == 'Tet-a-tet':
                variables.rotor += 1
                variables.classicBase = list(zip(*variables.classicBase))[::-1]
                variables.classicBase = list([list(elem) for elem in variables.classicBase])
            variables.keyed, x = tableManagementTetris.randomiser().defineSpawn()
            xCorner, yCorner = x, constants.startCornerY
            variables.movementStop = False
            tableManagementTetris.tetrominoDisplay(x, constants.startCornerY, variables.keyed).display()
            variables.rotator, variables.keyed = variables.keyed, ''
        tableManagementTetris.screenRefresh().refresh(variables.screen)
        variables.screen.blit(constants.img, (50 * constants.blockScale, 5 * constants.blockScale))
        variables.screen.blit(constants.img2, (50 * constants.blockScale, 10 * constants.blockScale))
        variables.screen.blit(constants.img3, (50 * constants.blockScale, 15 * constants.blockScale))
        variables.screen.blit(imgScore, (50 * constants.blockScale, 7 * constants.blockScale))
        if variables.holdContainer:
            tableManagementTetris.infoBlock().displayTestTetros(variables.holdContainer, 50, 17, variables.screen)
        tableManagementTetris.infoBlock().displayTestTetros(variables.nextLetter, 50, 12, variables.screen)
    elif variables.gameState == 'gameOver':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    guiScreens.screens().setScreenTo(constants.mainMenu, 'The Tetris experience', 'mainMenu')
                elif event.key == pygame.K_DOWN:
                    variables.inputAct = True
                elif event.key == pygame.K_RETURN and variables.inputAct:
                    variables.inputAct = False
                    tableManagementTetris.leader().add(variables.username, variables.score)
                    guiScreens.screens().setScreenTo(constants.mainMenu, 'The Tetris experience', 'mainMenu')
                elif event.key == pygame.K_BACKSPACE and variables.inputAct:
                    variables.username = variables.username[:-1]
                elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL and variables.inputAct:
                    variables.username = ''
                elif variables.inputAct:
                    variables.username += event.unicode
    elif variables.gameState == 'leaders':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    guiScreens.screens().setScreenTo(constants.mainMenu, 'The Tetris experience', 'mainMenu')

    pygame.display.flip()

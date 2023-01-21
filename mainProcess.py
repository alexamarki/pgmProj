import pygame
import tableManagementTetris, variables, guiScreens, guiTetris
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
cursor = pygame.image.load('Zmini.PNG').convert_alpha()
pygame.mouse.set_visible(False)
cursor_rect = cursor.get_rect()

running = True
while running:
    variables.screen.blit(variables.bg, (0, 0))
    if variables.gameState == 'mainMenu':
        guiTetris.AnimationExc().blitIt()
        variables.framed += 0.3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif cursor_rect.colliderect(
                    constants.tetrisParamRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                guiScreens.screens().setScreenTo(constants.tetrisMenu, 'Tetris - Parameters', 'tetMenu')
            elif cursor_rect.colliderect(
                    constants.tetrisTetARect) or event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                guiScreens.screens().setScreenTo(constants.tet_A, 'Tet-a-tetris', 'Tet-a-tet')
            elif cursor_rect.colliderect(
                    constants.tetrisLeaderRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                guiScreens.screens().setScreenTo(constants.leaderBoard, 'High Scores', 'leaders')
    elif variables.gameState == 'Tet-a-tet' or variables.gameState == 'Tetris':
        if variables.gameState == 'Tetris':
            if variables.rotor % 2:
                pygame.draw.rect(variables.screen, (140, 60, 63),
                                 pygame.Rect(variables.boardTopX * constants.blockScale,
                                             variables.boardTopY * constants.blockScale,
                                             variables.gameWidth * constants.blockScale,
                                             variables.gameHeight * constants.blockScale), 0)
            else:
                pygame.draw.rect(variables.screen, (140, 60, 63), pygame.Rect(
                    (constants.boardCentreX - constants.boardCentreY + variables.boardTopY) * constants.blockScale,
                    (
                            constants.boardCentreX + constants.boardCentreY - variables.boardTopX - variables.gameWidth) * constants.blockScale,
                    variables.gameHeight * constants.blockScale,
                    variables.gameWidth * constants.blockScale), 0)
        ROTATESCREEN = False
        variables.stage = int(variables.linesCleared / 10)
        imgScore = constants.font.render(str(variables.score), True, (0, 23, 43))
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
                    scoreTemp, linesClearedTemp, moveFurther = tableManagementTetris.tetrominoDisplay().movementCheck(0,
                                                                                                                      -1)
                    variables.score += scoreTemp * (1 + variables.stage)
                    variables.linesCleared += linesClearedTemp
                    tableManagementTetris.screenRefresh().refresh(variables.screen)
                    if moveFurther:
                        xCorner -= 1
                elif event.key == pygame.K_RIGHT and not movementPauseR:
                    scoreTemp, linesClearedTemp, moveFurther = tableManagementTetris.tetrominoDisplay().movementCheck(0,
                                                                                                                      1)
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
            elif cursor_rect.colliderect(
                    constants.tetrisMRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                guiScreens.screens().setScreenTo(constants.mainMenu, 'The Tetris experience', 'mainMenu')
            elif cursor_rect.colliderect(
                    constants.tetrisTRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                variables.inputAct = True
            elif (cursor_rect.colliderect(
                    constants.tetrisENTERRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) and variables.inputAct:
                variables.inputAct = False
                tableManagementTetris.leader().add(variables.username, variables.score)
                guiScreens.screens().setScreenTo(constants.mainMenu, 'The Tetris experience', 'mainMenu')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and variables.inputAct:
                variables.username = variables.username[:-1]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL and variables.inputAct:
                variables.username = ''
            elif variables.inputAct:
                variables.username += event.unicode
        inp = constants.fontL.render(f"User: {variables.username}", True, (0, 23, 43))
        scr = constants.fontExtra.render(f"Score: {variables.score}", True, (0, 23, 43))
        variables.screen.blit(scr, (60, 300))
        variables.screen.blit(inp, (60, 720))
    elif variables.gameState == 'leaders':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif cursor_rect.colliderect(
                    constants.tetrisMenuRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                guiScreens.screens().setScreenTo(constants.mainMenu, 'The Tetris experience', 'mainMenu')
        tableManagementTetris.leader().acquireLeaders()
    elif variables.gameState == 'tetMenu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                guiScreens.screens().setScreenTo(constants.mainMenu, 'The Tetris experience', 'mainMenu')
            elif cursor_rect.colliderect(
                    constants.tetrisPlayRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                guiScreens.screens().setScreenTo(constants.tet,
                                                 f'Tetris - {variables.gameHeight}x{variables.gameWidth}', 'Tetris')
            elif cursor_rect.colliderect(
                    constants.tetrisHRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                variables.tetrisMenuModifier = 'height'
            elif cursor_rect.colliderect(
                    constants.tetrisWRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                variables.tetrisMenuModifier = 'width'
            elif cursor_rect.colliderect(
                    constants.tetrisSRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                variables.tetrisMenuModifier = 'stage'
            elif event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_EQUALS, pygame.K_MINUS) and variables.tetrisMenuModifier:
                if variables.tetrisMenuModifier == 'width':
                    if variables.gameWidth < 40 and event.key == pygame.K_EQUALS:
                        variables.gameWidth += 1
                    elif variables.gameWidth > 0 and event.key == pygame.K_MINUS:
                        variables.gameWidth -= 1
                elif variables.tetrisMenuModifier == 'height':
                    if variables.gameHeight < 40 and event.key == pygame.K_EQUALS:
                        variables.gameHeight += 1
                    elif variables.gameHeight > 0 and event.key == pygame.K_MINUS:
                        variables.gameHeight -= 1
                else:
                    if variables.linesCleared < 81 and event.key == pygame.K_EQUALS:
                        variables.linesCleared += 10
                    elif variables.linesCleared > 9 and event.key == pygame.K_MINUS:
                        variables.linesCleared -= 10
                    variables.linesModified = True
            elif cursor_rect.colliderect(
                    constants.tetrisCRect) or event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                variables.choosingLevelManually = True
            elif cursor_rect.colliderect(
                    constants.tetris1Rect) or event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                variables.levelTet = 'level1.txt'
            elif cursor_rect.colliderect(
                    constants.tetris2Rect) or event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                variables.levelTet = 'level2.txt'
            elif cursor_rect.colliderect(
                    constants.tetris3Rect) or event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                variables.levelTet = 'level3.txt'
        hei = constants.fontL.render(str(variables.gameHeight), True, (0, 23, 43))
        wid = constants.fontL.render(str(variables.gameWidth), True, (0, 23, 43))
        stg = constants.fontL.render(str(variables.linesCleared / 10), True, (0, 23, 43))
        variables.screen.blit(hei, (430, 640))
        variables.screen.blit(wid, (430, 700))
        variables.screen.blit(stg, (430, 760))
    cursor_rect.center = pygame.mouse.get_pos()
    variables.screen.blit(cursor, cursor_rect)
    pygame.display.flip()

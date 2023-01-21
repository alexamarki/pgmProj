import pygame, constants, variables
import tableManagementTetris


class screens():
    def setScreenTo(self, backgroundLink, winName, gs):
        variables.bg = pygame.image.load(backgroundLink)
        pygame.display.set_caption(winName)
        variables.gameState = gs
        if gs == 'gameOver':
            variables.linesModified = False
        if gs == 'Tet-a-tet' or gs == 'Tetris':
            variables.username = ''
            variables.tickSpeed = 1000 / 3
            variables.nextLetter = ''
            variables.score = 0
            variables.all_sprites = pygame.sprite.Group()
            variables.holdPause = False
            if not variables.linesModified:
                variables.linesCleared = 0
            variables.stage = 0
            variables.keyed = ''
            variables.rotator = ''
            variables.movementStop = False
            if gs == 'Tet-a-tet':
                variables.rotor = 0
            else:
                variables.rotor = 1
            variables.holdContainer = ''
            tableManagementTetris.randomiser().randomiseletter()
            variables.currentTetromino = []
            variables.screen = pygame.display.set_mode((constants.width, constants.height))

            if gs == 'Tet-a-tet':
                with open("input.txt", "r") as file:
                    variables.classicBase = [[x for x in line.split()] for line in file]
                    variables.gameHeight = 40
                    variables.gameWidth = 40
            else:
                if not variables.choosingLevelManually:
                    variables.classicBase = [['BACK' for x in range(variables.gameWidth)] for line in
                                             range(variables.gameHeight)]
                else:
                    with open(variables.levelTet, "r") as file:
                        variables.classicBase = [[x for x in line.split()] for line in file]
                        variables.gameHeight = len(variables.classicBase)
                        variables.gameWidth = len(variables.classicBase[0])
            variables.boardTopX = constants.boardCentreX - variables.gameWidth / 2
            variables.boardTopY = constants.boardCentreY - variables.gameHeight / 2

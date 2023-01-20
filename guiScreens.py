import pygame, constants, variables

import guiTetris
import tableManagementTetris


class screens():
    def setScreenTo(self, backgroundLink, winName, gs):
        variables.bg = pygame.image.load(backgroundLink)
        pygame.display.set_caption(winName)
        variables.gameState = gs
        if gs == 'Tet-a-tet' or gs == 'Tetris':
            variables.tickSpeed = 1000 / 3
            variables.nextLetter = ''
            variables.score = 0
            variables.all_sprites = pygame.sprite.Group()
            variables.holdPause = False
            variables.linesCleared = 0
            variables.stage = 0
            variables.keyed = ''
            variables.rotator = ''
            variables.movementStop = False
            variables.rotor = 0
            variables.holdContainer = ''
            tableManagementTetris.randomiser().randomiseletter()
            variables.currentTetromino = []
            variables.boardTopX = constants.boardCentreX - variables.gameWidth / 2
            variables.boardTopY = constants.boardCentreY - variables.gameHeight / 2
            variables.screen = pygame.display.set_mode((constants.width, constants.height))
            # with open("input.txt", "r") as file:
            #     variables.classicBase = [[x for x in line.split()] for line in file]
            #     variables.gameHeight = len(variables.classicBase)
            #     variables.gameWidth = len(variables.classicBase[0])
            variables.classicBase = [['BACK' for x in range(10)] for line in range(20)]
            variables.gameHeight = len(variables.classicBase)
            variables.gameWidth = len(variables.classicBase[0])


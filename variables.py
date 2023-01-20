import pygame, constants

current_tetromino = []
all_sprites = pygame.sprite.Group()
gameWidth, gameHeight = 40, 40
with open("input.txt", "r") as file:
    classicBase = [[x for x in line.split()] for line in file]
    gameHeight = len(classicBase)
    gameWidth = len(classicBase[0])
boardTopX = constants.boardCentreX - gameWidth / 2
boardTopY = constants.boardCentreY - gameHeight / 2
rotor = 0
holdContainer = ''
screen = pygame.display.set_mode((constants.width, constants.height))
tickSpeed = 1000/3
score = 0
nextLetter = ''
holdPause = False
linesCleared = 0
stage = 0
keyed = ''
rotator = ''
movementStop = False
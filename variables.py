import pygame, constants

current_tetromino = []
all_sprites = pygame.sprite.Group()
gameWidth, gameHeight = 10, 20
# with open("input.txt", "r") as file:
#     variables.classicBase = [[x for x in line.split()] for line in file]
#     variables.gameHeight = len(variables.classicBase)
#     variables.gameWidth = len(variables.classicBase[0])
classicBase = [['BACK' for x in range(10)] for line in range(20)]
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
bg = pygame.image.load('mainMenu_bg.jpg')
gameState = 'mainMenu'

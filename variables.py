import pygame, constants

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
current_tetromino = []
all_sprites = pygame.sprite.Group()
gameWidth, gameHeight = 10, 20
gameState = 'mainMenu'
classicBase = []
boardTopX = constants.boardCentreX - gameWidth / 2
boardTopY = constants.boardCentreY - gameHeight / 2
rotor = 0
holdContainer = ''
screen = pygame.display.set_mode((constants.width, constants.height))
tickSpeed = 1000 / 3
score = 0
nextLetter = ''
holdPause = False
linesCleared = 0
stage = 0
keyed = ''
rotator = ''
username = ''
inputAct = False
movementStop = False
leaderList = []
bg = pygame.image.load(constants.mainMenu)
pygame.mixer.music.load("sweden.mp3")
pygame.mixer.music.set_volume(0.1)
dropSound = pygame.mixer.Sound("Tink.wav")
clearSound = pygame.mixer.Sound("Glass.wav")
tetrisMenuModifier = ''
linesModified = False
choosingLevelManually = False
levelTet = 'level1.txt'
framed = 0

import pygame

pygame.font.init()

dropTick = 0.05
boardCentreX = 20
boardCentreY = 20
blockScale = 24
(width, height) = (60 * blockScale, 40 * blockScale)
startCornerXtet = 3
startCornerY = 0
letters = ['j', 'l', 'o', 'i', 's', 'z', 't']
gameOver = 'death_bg.PNG'
mainMenu = 'mainMenu_bg.PNG'
leaderBoard = 'leader_bg.PNG'
tetrisMenu = 'tetrisMenu_bg.PNG'
tet_A = 'test_bg.PNG'
tet = 'tetrisGame_bg.PNG'


def tetrominod(x, y):
    tetrominos = {
        'l': [(x + 2, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)],
        'j': [(x, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)],
        'i': [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y + 1)],
        's': [(x + 1, y), (x + 2, y), (x, y + 1), (x + 1, y + 1)],
        'z': [(x, y), (x + 1, y), (x + 1, y + 1), (x + 2, y + 1)],
        't': [(x + 1, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)],
        'o': [(x + 1, y), (x + 2, y), (x + 1, y + 1), (x + 2, y + 1)]
    }
    return tetrominos


# cnst.text+.sprites
font = pygame.font.Font('boldTestFont.ttf', 24)
fontL = pygame.font.Font('boldTestFont.ttf', 48)
fontExtra = pygame.font.Font('boldTestFont.ttf', 128)
img = font.render('SCORE', True, (0, 23, 43))
img2 = font.render('NEXT', True, (0, 23, 43))
img3 = font.render('HOLD', True, (0, 23, 43))

# main menu rects
tetrisParamRect = pygame.Rect((73, 428, 36, 36))
tetrisTetARect = pygame.Rect((73, 534, 36, 36))
tetrisLeaderRect = pygame.Rect((73, 639, 36, 36))
# leaderboard rect
tetrisMenuRect = pygame.Rect((1190, 41, 7, 7))
# tetris rects
tetrisCRect = pygame.Rect((66, 158, 15, 15))
tetris1Rect = pygame.Rect((64, 228, 1, 10))
tetris2Rect = pygame.Rect((64, 228, 1, 10))
tetris3Rect = pygame.Rect((64, 228, 1, 10))
tetrisHRect = pygame.Rect((235, 659, 18, 18))
tetrisWRect = pygame.Rect((235, 720, 18, 18))
tetrisSRect = pygame.Rect((235, 782, 18, 18))
tetrisPlayRect = pygame.Rect((1267, 0, 176, 960))
# death rects
tetrisMRect = pygame.Rect((913, 614, 11, 11))
tetrisTRect = pygame.Rect((913, 676, 11, 11))
tetrisENTERRect = pygame.Rect((943, 740, 87, 17))

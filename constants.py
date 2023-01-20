import pygame
pygame.font.init()

dropTick = 0.05
boardCentreX = 20
boardCentreY = 20
blockScale = 24
(width, height) = (60 * blockScale, 40 * blockScale)
startCornerXtet = 19
startCornerY = 0
letters = ['j', 'l', 'o', 'i', 's', 'z', 't']
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

#cnst.text+.sprites
font = pygame.font.SysFont('boldTestFont.ttf', 24)
img = font.render('SCORE', True, (0, 23, 43))
img2 = font.render('NEXT', True, (0, 23, 43))
img3 = font.render('HOLD', True, (0, 23, 43))
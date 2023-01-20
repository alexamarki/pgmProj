import constants, variables
import pygame
with open("input.txt", "r") as file:
    classicBase = [[x for x in line.split()] for line in file]
    gameHeight = len(classicBase)
    gameWidth = len(classicBase[0])
class tetrominoBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, screen=True):
        super().__init__(variables.all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        if screen:
            self.x += variables.boardTopX
            self.y += variables.boardTopY
            self.rotationSit()

    def rotationSit(self):
        if variables.rotor % 4 == 1:
            pass
        elif variables.rotor % 4 == 2:
            self.x, self.y = constants.boardCentreX + constants.boardCentreY - self.y - 1, -constants.boardCentreX + constants.boardCentreY + self.x
        elif variables.rotor % 4 == 3:
            self.x, self.y = constants.boardCentreX * 2 - self.x - 1, constants.boardCentreY * 2 - self.y - 1
        else:
            self.x, self.y = constants.boardCentreX - constants.boardCentreY + self.y, constants.boardCentreX + constants.boardCentreY - self.x - 1

    def update(self, screen):
        screen.blit(self.image, ((self.x) * constants.blockScale, (self.y) * constants.blockScale))

def override():
    exit()
import pygame

class Tile(object):
    
    def __init__(self, name, image, untraversable, heal):
        self.name = name
        self.image = image
        self.untraversable = untraversable
        self.heal = heal
        
    def drawTile(self, screen, data, xPos, yPos):
        screen.blit(self.image, (xPos*data.tileWidth, yPos*data.tileHeight))
        
################################################################################
       
forest = pygame.image.load('forest.png')
fort = pygame.image.load('fort.png')
grass = pygame.image.load('grass.png')
mountain = pygame.image.load('mountain.png')
trees = pygame.image.load('trees.png')

################################################################################

forestTile = Tile('Forest', forest, False, 0)
fortTile = Tile('Fort', fort, False, 10)
grassTile = Tile('Plain', grass, False, 0)
mountainTile = Tile('Mountain', mountain, True, 0)
treesTile = Tile('Forest', trees, False, 0)

################################################################################

# tiles to add/change:
#     village: 3x3 , untraversable except for the middle bottom tile, visiting a 
#             village gives that unit some sort of buff
#     sand: reduces unit movement
#     forest: increases defense but reduces spd

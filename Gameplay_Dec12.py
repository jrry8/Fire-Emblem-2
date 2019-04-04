import pygame
from Data import *

def runGame(data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data.runningGame = False
            data.playingMap = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = mouseLocation(data, *event.pos)
            #clicking on a unit selects it, clicking on it again deselects it
            for unit in (data.playerUnits + data.enemyUnits):
               if unit.pos == (x,y):
                    if data.selectedUnit == unit:
                        data.selectedUnit = None
                    else:
                        data.selectedUnit = unit 
    
def drawGame(data, screen):
    #draws each map tile
    for x, row in enumerate(data.grid):
        for y, tile in enumerate(row):
            tile.drawTile(screen, data, x, y)
    #draws each unit
    for unit in (data.playerUnits + data.enemyUnits):
        unit.drawUnit(screen, data)
    #draws the selected units move/attack range
    if data.selectedUnit != None:
        data.selectedUnit.getMoveRange(data)
        data.selectedUnit.getAttackRange(data)
        for pos in data.selectedUnit.moveRange:
            x, y = pos
            rect=(x*(data.tileWidth), y*(data.tileHeight), data.tileWidth, data.tileHeight)
            pygame.draw.rect(screen, (50,100,255), rect, 1)
        for pos in data.selectedUnit.atkRange:
            x, y = pos
            rect=(x*(data.tileWidth), y*(data.tileHeight), data.tileWidth, data.tileHeight)
            pygame.draw.rect(screen, (200,0,0), rect, 1)
            
def makeBlankMap(rows, cols):
    grid = []
    for row in range(rows):
        grid += [[grassTile] * cols]
    return grid
    
def mouseLocation(data, x, y):
    row = x//data.tileWidth
    col = y//data.tileHeight
    #returns which tile in the grid the cursor is at
    return (row, col)
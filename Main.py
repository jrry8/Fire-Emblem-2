import pygame
from Gameplay import *
from MapEditor import *
    
def run(width=500, height=500):
    clock = pygame.time.Clock() 
    
    #screen is the base white surface everything is drawn on 
    screen = pygame.display.set_mode((width, height))
    
    #moveTile and atkTile are translucent surfaces drawn on top to show movement/atk range
    moveTile = pygame.Surface((data.tileWidth-2, data.tileHeight-2))
    moveTile.set_alpha(100)
    moveTile.fill((50,100,255))
    atkTile = pygame.Surface((data.tileWidth-2, data.tileHeight-2))
    atkTile.set_alpha(100)
    atkTile.fill((255,0,0))
    
    #Objective overlay
    objOverlay = pygame.Surface((width/4, height/5))
    objOverlay.set_alpha(175)
    
    #Terrain Info overlay
    tInfoOverlay = pygame.Surface((width/4, height/5))
    tInfoOverlay.set_alpha(175)
    
    #Character Info overlay
    cInfoOverlay = pygame.Surface((width/4, height/5))
    cInfoOverlay.set_alpha(175)
    cInfoOverlay.fill((255,255,255))
    
    #data.grid stores tile objects in a 2d list representing the map
    data.grid = makeBlankMap(data.gridRows, data.gridCols) 
    
    ###for testing###
    for i in range(3,12):
        data.grid[i][i] = mountainTile
    ###for testing###
    
    while data.runningGame:
        while data.playingMap:
            clock.tick()
            runGame(data)
            screen.fill((255,255,255))
            drawGame(data, screen, width, height, moveTile, atkTile, objOverlay, 
                    tInfoOverlay, cInfoOverlay)
            # print(data.choosingWeapon)
            # if data.selectedUnit != None:
            #     print(data.selectedUnit.weapons)
            #     print(data.selectedUnit.equipped)
            pygame.display.flip()
            
    pygame.quit()
    
    #while runningGame:
        #while onStartScreen:
            #blah blah
        #while playing:
            #runGame()
        #while mapEditing:
            #runMapEditor()

init(data)
run(16*data.tileHeight, 16*data.tileWidth)
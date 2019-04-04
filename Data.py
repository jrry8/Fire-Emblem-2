import pygame
from Tile import *
from Unit import *

class Data(object):
    pass
data = Data()

def init(data):
    data.grid = []
    data.gridRows = 16
    data.gridCols = 16
    data.tileWidth, data.tileHeight = grass.get_size()
    
    data.runningGame = True
    data.startScreen = False
    data.playingMap = True
    data.mapEditing = False
    
    data.playerTurn = True
    data.selectedUnit = None
    
    data.playerUnits = playerUnits #see Unit file
    data.enemyUnits = enemyUnits #see Unit file
    data.currTurnUnits = data.playerUnits
    data.opposTurnUnits = data.enemyUnits
    
    data.cursorLoc = (0,0)
    data.cursorLocArea = 'NW'
    data.unitUnderCursor = None
    
    data.mapMenuOpen = False
    data.commandMenuOpen = False
    data.currMenuOption = 0
    
    data.mapOptions = ['End']
    data.commandOptions = ['Wait']
    data.atkTargets = []
    
    data.choosingWeapon = False
    data.weaponOption = 0
    
    data.choosingAtk = False
    data.atkOption = 0
    

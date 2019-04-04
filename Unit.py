import pygame
from Item import *

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (128,128,128)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class Unit(object):
    def __init__(self, name, hp, str, skill, spd, luck, defense, res, move, con, 
    melee, ranged, pos):
        self.name = name
        self.hp = hp
        self.totalhp = hp
        self.str = str
        self.skill = skill
        self.spd = spd
        self.luck = luck
        self.defense = defense
        self.res = res
        self.move = move
        self.con = con
        # self.melee = melee
        # self.ranged = ranged
        self.pos = pos
        self.color = BLUE
        self.weapons = []
        self.equipped = 0
        self.consumables = []
        self.inventory = self.weapons + self.consumables
        self.moveRange = []
        self.atkRange = []
        self.moved = False
        
    def atkSpd(self):
        return self.spd - max(0, self.weapons[self.equipped].wt - self.con)
        
    def hitRate(self):
        return roundHalfUp(self.weapons[self.equipped].hit + (self.skill*2) + (self.luck/2))
        
    def avoid(self): #terrain bonus needs to be calculated in Gameplay.py
        return (self.spd*2) + self.luck 
        
    def critRate(self):
        return self.weapons[self.equipped].crit + roundHalfUp(self.skill/2)
        
    def critEvade(self):
        return self.luck
        
    def drawUnit(self, screen, data):
        x, y = self.pos
        cx = int((x+0.5)*data.tileWidth)
        cy = int((y+0.5)*data.tileHeight)
        radius = int(data.tileWidth/2 - 3)
        self.color = BLUE
        if self.moved:
            self.color = GREY
        pygame.draw.circle(screen, self.color, (cx,cy), radius)
        
    def getMoveRange(self, data):
        depth = 0
        x, y = self.pos
        tilesInRange = [(x, y, depth)]
        enemyLocations = []
        for unit in data.enemyUnits:
            enemyLocations.append(unit.pos)
        while(tilesInRange != []):
            x, y, currDepth = tilesInRange.pop(0)
            if((x,y) in self.moveRange or (x,y) in enemyLocations or not isInGrid(data,x,y) 
            or currDepth>self.move or data.grid[x][y].untraversable):
                continue
            self.moveRange.append((x,y))
            currDepth += 1
            tilesInRange.append((x-1, y, currDepth))
            tilesInRange.append((x+1, y, currDepth))
            tilesInRange.append((x, y-1, currDepth))
            tilesInRange.append((x, y+1, currDepth))
            
    def getAttackRange(self, data):
        moveRangeEdge = []
        self.melee = False
        self.ranged = False
        for weapon in self.weapons:
            if weapon.melee:
                self.melee = True
            if weapon.ranged:
                self.ranged = True
        for pos in self.moveRange:
            x, y = pos
            if self.melee:
                if ((x+1, y) not in self.moveRange) and ((x+1,y) not in self.atkRange)\
                and isInGrid(data, x+1, y):
                    self.atkRange.append((x+1, y))
                if ((x-1, y) not in self.moveRange) and ((x-1,y) not in self.atkRange)\
                and isInGrid(data, x-1, y):
                    self.atkRange.append((x-1, y))
                if ((x, y+1) not in self.moveRange) and ((x,y+1) not in self.atkRange)\
                and isInGrid(data, x, y+1):
                    self.atkRange.append((x, y+1))
                if ((x, y-1) not in self.moveRange) and ((x,y-1) not in self.atkRange)\
                and isInGrid(data, x, y-1):
                    self.atkRange.append((x, y-1))
            if self.ranged: 
                if ((x+2, y) not in self.moveRange) and ((x+2,y) not in self.atkRange)\
                and isInGrid(data, x+2, y):
                    self.atkRange.append((x+2, y))
                if ((x-2, y) not in self.moveRange) and ((x-2,y) not in self.atkRange)\
                and isInGrid(data, x-2, y):
                    self.atkRange.append((x-2, y))
                if ((x, y+2) not in self.moveRange) and ((x,y+2) not in self.atkRange)\
                and isInGrid(data, x, y+2):
                    self.atkRange.append((x, y+2))
                if ((x, y-2) not in self.moveRange) and ((x,y-2) not in self.atkRange)\
                and isInGrid(data, x, y-2):
                    self.atkRange.append((x, y-2))
                if ((x-1,y-1) not in self.moveRange) and ((x-1,y-1) not in self.atkRange)\
                and isInGrid(data, x-1, y-1):
                    self.atkRange.append((x-1,y-1))
                if ((x+1,y-1) not in self.moveRange) and ((x+1,y-1) not in self.atkRange)\
                and isInGrid(data, x+1, y-1):
                    self.atkRange.append((x+1,y-1))
                if ((x-1,y+1) not in self.moveRange) and ((x-1,y+1) not in self.atkRange)\
                and isInGrid(data, x-1, y+1):
                    self.atkRange.append((x-1,y+1))
                if ((x+1,y+1) not in self.moveRange) and ((x+1,y+1) not in self.atkRange)\
                and isInGrid(data, x+1, y+1):
                    self.atkRange.append((x+1,y+1))    
        
class enemySoldier(Unit):
    def __init__(self, name, pos):
        self.name = name
        self.hp = 2300 #inflated for testing purposes
        self.totalhp = 2300 #inflated for testing purposes
        self.str = 1 #decreased for testing purposes
        self.skill = 4
        self.spd = 7
        self.luck = 0
        self.defense = 2
        self.res = 0
        self.con = 11
        self.move = 5
        # self.melee = True
        # self.ranged = False
        self.pos = pos
        self.color = RED
        self.weapons = []
        self.equipped = 0
        self.consumables = []
        self.inventory = self.weapons + self.consumables
        self.moveRange = []
        self.atkRange = []
        self.moved = False
        
    def drawUnit(self, screen, data):
        x, y = self.pos
        cx = int((x+0.5)*data.tileWidth)
        cy = int((y+0.5)*data.tileHeight)
        radius = int(data.tileWidth/2 - 3)
        self.color = RED
        if self.moved:
            self.color = GREY
        pygame.draw.circle(screen, self.color, (cx,cy), radius)
        
    def getMoveRange(self, data):
        depth = 0
        x, y = self.pos
        tilesInRange = [(x, y, depth)]
        enemyLocations = []
        for unit in data.playerUnits:
            enemyLocations.append(unit.pos)
        while(tilesInRange != []):
            x, y, currDepth = tilesInRange.pop(0)
            if((x,y) in self.moveRange or (x,y) in enemyLocations or x<0 or 
            x>=data.gridRows or y<0 or y>=data.gridCols or currDepth>self.move 
            or data.grid[x][y].untraversable):
                continue
            self.moveRange.append((x,y))
            currDepth += 1
            tilesInRange.append((x-1, y, currDepth))
            tilesInRange.append((x+1, y, currDepth))
            tilesInRange.append((x, y-1, currDepth))
            tilesInRange.append((x, y+1, currDepth))
 
class enemyArcher(Unit): #THIS UNIT CURRENTLY IS NOT USED
    def __init__(self, name, pos):
        self.name = name
        self.hp = 20
        self.totalhp = 20
        self.str = 15
        self.spd = 10
        self.defense = 11
        self.move = 6
        # self.melee = False
        # self.ranged = True
        self.pos = pos
        self.color = RED
        self.weapons = []
        self.equipped = 0
        self.consumables = []
        self.inventory = self.weapons + self.consumables
        self.moveRange = []
        self.atkRange = []
        self.moved = False
        
    def getMoveRange(self, data):
        depth = 0
        x, y = self.pos
        tilesInRange = [(x, y, depth)]
        enemyLocations = []
        for unit in data.playerUnits:
            enemyLocations.append(unit.pos)
        while(tilesInRange != []):
            x, y, currDepth = tilesInRange.pop(0)
            if((x,y) in self.moveRange or (x,y) in enemyLocations or x<0 or 
            x>=data.gridRows or y<0 or y>=data.gridCols or currDepth>self.move 
            or data.grid[x][y].untraversable):
                continue
            self.moveRange.append((x,y))
            currDepth += 1
            tilesInRange.append((x-1, y, currDepth))
            tilesInRange.append((x+1, y, currDepth))
            tilesInRange.append((x, y-1, currDepth))
            tilesInRange.append((x, y+1, currDepth))
    
class enemyMage(Unit): #THIS UNIT CURRENTLY IS NOT USED
    def __init__(self, name, pos):
        self.name = name
        self.hp = 20
        self.totalhp = 20
        self.str = 15
        self.spd = 10
        self.defense = 11
        self.move = 6
        # self.melee = True
        # self.ranged = True
        self.pos = pos
        self.color = RED
        self.weapons = []
        self.equipped = 0
        self.consumables = []
        self.inventory = self.weapons + self.consumables
        self.moveRange = []
        self.atkRange = []
        self.moved = False
        
    def drawUnit(self, screen, data):
        x, y = self.pos
        cx = int((x+0.5)*data.tileWidth)
        cy = int((y+0.5)*data.tileHeight)
        radius = int(data.tileWidth/2 - 3)
        self.color = RED
        if self.moved:
            self.color = GREY
        pygame.draw.circle(screen, self.color, (cx,cy), radius)
        
    def getMoveRange(self, data):
        depth = 0
        x, y = self.pos
        tilesInRange = [(x, y, depth)]
        enemyLocations = []
        for unit in data.playerUnits:
            enemyLocations.append(unit.pos)
        while(tilesInRange != []):
            x, y, currDepth = tilesInRange.pop(0)
            if((x,y) in self.moveRange or (x,y) in enemyLocations or x<0 or 
            x>=data.gridRows or y<0 or y>=data.gridCols or currDepth>self.move 
            or data.grid[x][y].untraversable):
                continue
            self.moveRange.append((x,y))
            currDepth += 1
            tilesInRange.append((x-1, y, currDepth))
            tilesInRange.append((x+1, y, currDepth))
            tilesInRange.append((x, y-1, currDepth))
            tilesInRange.append((x, y+1, currDepth))
        
#helper function 
def isInGrid(data, x, y):
    if x>=0 and x<data.gridRows and y>=0 and y<data.gridCols:
        return True
    return False
    
        
Eirika = Unit('Eirika', 18, 5, 10, 10, 11, 4, 2, 5, 5, True, False, (0,0))
Eirika.weapons = [ironSword, slimSword, steelSword, shamshir, killingEdge]

Ephraim = Unit('Ephraim', 2300, 8, 9, 11, 8, 7, 2, 8, 5, True, False, (10,11))
#hp inflated for testing
Ephraim.weapons = [ironLance, slimLance, steelLance, killerLance, javelin]

grunt1 = enemySoldier('Grunt 1', (15,15))
grunt1.weapons = [ironAxe]

grunt2 = enemySoldier('Grunt 2', (15,14))
grunt2.weapons = [ironAxe]

playerUnits = [Eirika, Ephraim]
enemyUnits = [grunt1, grunt2]


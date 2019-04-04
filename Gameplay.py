import pygame
import random
from Data import *
pygame.init()

overlayFont = pygame.font.SysFont('Arial', 22)

########### would be helpful to create a helper function for calculating distance between two units

def runGame(data):
    #update unit deaths
    for unit in data.playerUnits:
        if unit.hp <= 0:
            data.playerUnits.remove(unit)
    for unit in data.enemyUnits:
        if unit.hp <= 0:
            data.enemyUnits.remove(unit)
    
    #changes the turn
    turnCheck = 0
    for unit in data.currTurnUnits:
        if not unit.moved:
            turnCheck += 1
    if turnCheck == 0: #if all units have moved, the turn automatically ends
        for unit in data.currTurnUnits:
            #resets the states of all the units
            unit.moved = False
            unit.moveRange = []
            unit.atkRange = []
        if data.currTurnUnits == data.playerUnits:
            data.currTurnUnits = data.enemyUnits
            data.opposTurnUnits = data.playerUnits
        else:
            data.currTurnUnits = data.playerUnits 
            data.opposTurnUnits = data.enemyUnits
        if data.playerTurn:
            data.playerTurn = False
        else:
            data.playerTurn = True
           
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #closing the window tells the game to stop running
            data.runningGame = False
            data.playingMap = False
        elif event.type == pygame.KEYDOWN:
            gameKeyPressed(event, data)
    
    #holding 'a' and using arrow keys allows for fast cursor scrolling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and keys[pygame.K_a]:
        pygame.time.delay(100)
        x, y = data.cursorLoc
        if isInGrid(data, x, y-1):
            data.cursorLoc = (x,y-1)
    elif keys[pygame.K_DOWN] and keys[pygame.K_a]:
        pygame.time.delay(100)
        x, y = data.cursorLoc
        if isInGrid(data, x, y+1):
            data.cursorLoc = (x,y+1)
    elif keys[pygame.K_LEFT] and keys[pygame.K_a]:
        pygame.time.delay(100)
        x, y = data.cursorLoc
        if isInGrid(data, x-1, y):
            data.cursorLoc = (x-1,y)
    elif keys[pygame.K_RIGHT] and keys[pygame.K_a]:
        pygame.time.delay(100)
        x, y = data.cursorLoc
        if isInGrid(data, x+1, y):
            data.cursorLoc = (x+1,y)
    
                      
def gameKeyPressed(event, data):
    # if data.atkMenuOpen:
    #     #arrow keys left and right change which target to attack
    #     if event.key == pygame.K_LEFT:
    #        data.atkOption -= 1
    #        if data.atkOption < 0:
    #            data.atkOption = len(data.atkTargets)-1
    #     elif event.key == pygame.K_RIGHT:
    #         data.atkOption += 1
    #         if data.atkOption >= len(data.atkTargets):
    #             data.atkOption = 0
    #     elif event.key == pygame.K_a: #press 'a' to go back
    #         data.atkMenuOpen = False
    #         data.commandMenuOpen = True
    #     elif event.key == pygame.K_s: #press 's' to confirm and attack your target
    #         target = data.atkTargets[data.atkOption]
    #         data.selectedUnit.attack(target)
    #         data.atkMenuOpen = False
    #         data.selectedUnit.moved = True
    #         data.selectedUnit = None
    #         data.atkTargets = []
    #         data.atkOption = 0
    
    if data.choosingWeapon:
        if event.key == pygame.K_UP and data.weaponOption > 0:
            data.weaponOption -= 1
        elif event.key == pygame.K_DOWN and data.weaponOption < \
        (len(data.selectedUnit.weapons)-1):
            data.weaponOption += 1
        elif event.key == pygame.K_a:
            data.choosingWeapon = False
            data.weaponOption = 0
            data.commandMenuOpen = True
        elif event.key == pygame.K_s:
            data.choosingWeapon = False
            data.choosingAtk = True
            data.selectedUnit.equipped = data.weaponOption
            data.weaponOption = 0
            
    elif data.choosingAtk:
        if event.key == pygame.K_LEFT:
            data.atkOption -= 1
            if data.atkOption < 0:
               data.atkOption = len(data.atkTargets)-1
        elif event.key == pygame.K_RIGHT:
            data.atkOption += 1
            if data.atkOption >= len(data.atkTargets):
                data.atkOption = 0
        elif event.key == pygame.K_a:
            data.choosingAtk = False
            data.atkOption = 0
            data.choosingWeapon = True
        elif event.key == pygame.K_s:
            target = data.atkTargets[data.atkOption]
            x1, y1 = data.selectedUnit.pos
            x2, y2 = target.pos
            diff = abs(x1-x2) + abs(y1-y2)
            
            #case where charB can attack back
            if (diff == 1 and target.weapons[target.equipped].melee) or (diff == 2
            and target.weapons[target.equipped].ranged):
                
                #case where charA attacks, charB attacks, charA attacks
                if (data.selectedUnit.spd - target.spd) >= 4:
                    makeAttack(data.selectedUnit, target)
                    if target.hp <= 0: #check if unit dies
                        if target in data.playerUnits:
                            data.playerUnits.remove(target)
                        else:
                            data.enemyUnits.remove(target)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                            
                    makeAttack(target, data.selectedUnit)
                    if data.selectedUnit.hp <= 0: #check if unit dies
                        if data.selectedUnit in data.playerUnits:
                            data.playerUnits.remove(data.selectedUnit)
                        else:
                            data.enemyUnits.remove(data.selectedUnit)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                    
                    makeAttack(data.selectedUnit, target)
                    if target.hp <= 0: #check if unit dies
                        if target in data.playerUnits:
                            data.playerUnits.remove(target)
                        else:
                            data.enemyUnits.remove(target)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                        
                #case where charA attacks, charB attacks twice
                if (target.spd - data.selectedUnit.spd) >= 4:
                    makeAttack(data.selectedUnit, target)
                    if target.hp <= 0: #check if unit dies
                        if target in data.playerUnits:
                            data.playerUnits.remove(target)
                        else:
                            data.enemyUnits.remove(target)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                    
                    makeAttack(target, data.selectedUnit)
                    if data.selectedUnit.hp <= 0: #check if unit dies
                        if data.selectedUnit in data.playerUnits:
                            data.playerUnits.remove(data.selectedUnit)
                        else:
                            data.enemyUnits.remove(data.selectedUnit)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                    
                    makeAttack(target, data.selectedUnit)
                    if data.selectedUnit.hp <= 0: #check if unit dies
                        if data.selectedUnit in data.playerUnits:
                            data.playerUnits.remove(data.selectedUnit)
                        else:
                            data.enemyUnits.remove(data.selectedUnit)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                    
                #case where charA attacks, charB attacks
                else:
                    makeAttack(data.selectedUnit, target)
                    if target.hp <= 0: #check if unit dies
                        if target in data.playerUnits:
                            data.playerUnits.remove(target)
                        else:
                            data.enemyUnits.remove(target)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                    
                    makeAttack(target, data.selectedUnit)
                    if data.selectedUnit.hp <= 0: #check if unit dies
                        if data.selectedUnit in data.playerUnits:
                            data.playerUnits.remove(data.selectedUnit)
                        else:
                            data.enemyUnits.remove(data.selectedUnit)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                    
            #case where charA and charB cannot counter-attack:
            else:
                if (data.selectedUnit.spd - target.spd) >= 4: #charA attacks twice
                    makeAttack(data.selectedUnit, target)
                    if target.hp <= 0: #check if unit dies
                        if target in data.playerUnits:
                            data.playerUnits.remove(target)
                        else:
                            data.enemyUnits.remove(target)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                        
                    makeAttack(data.selectedUnit, target)
                    if target.hp <= 0: #check if unit dies
                        if target in data.playerUnits:
                            data.playerUnits.remove(target)
                        else:
                            data.enemyUnits.remove(target)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return

                else: #charA attacks once
                    makeAttack(data.selectedUnit, target)
                    if target.hp <= 0: #check if unit dies
                        if target in data.playerUnits:
                            data.playerUnits.remove(target)
                        else:
                            data.enemyUnits.remove(target)
                        data.choosingAtk = False
                        data.atkOption = 0
                        data.atkTargets = []
                        data.selectedUnit.moved = True
                        data.selectedUnit = None
                        return
                        
            #case where all attacks have finished and no unit died
            data.choosingAtk = False
            data.atkOption = 0
            data.atkTargets = []
            data.selectedUnit.moved = True
            data.selectedUnit = None
            return         
    
    elif data.commandMenuOpen:
        #up and down arrow keys scroll through the menu
        if event.key == pygame.K_UP and data.currMenuOption > 0:
            data.currMenuOption -= 1
        elif event.key == pygame.K_DOWN and data.currMenuOption < (len(data.commandOptions)-1):
            data.currMenuOption += 1  
        elif event.key == pygame.K_a: 
        #pressing 'a' exits the menu and returns unit to original position
            data.commandMenuOpen = False
            data.selectedUnit.pos = data.selectedUnitStartPos
            data.atkTargets = []
            data.commandOptions = ['Wait']
        elif event.key == pygame.K_s:
            if data.commandOptions[data.currMenuOption] == 'Wait':
                data.selectedUnit.moved = True
                data.selectedUnit = None
                data.commandMenuOpen = False
                data.currMenuOption = 0
                data.atkTargets = []
                data.commandOptions = ['Wait']
            elif data.commandOptions[data.currMenuOption] == 'Attack':
                # we need to create a list of weapons the selected unit can use
                # at this point depending on ranged needed to attack possible targets
                data.validWeapons = list()
###############
                data.choosingWeapon = True
                data.commandMenuOpen = False
                data.currMenuOption = 0
                data.commandOptions = ['Wait']
            
    elif data.mapMenuOpen:
        #up and down arrow keys scroll through the menu
        if event.key == pygame.K_UP and data.currMenuOption > 0:
            data.currMenuOption -= 1
        elif event.key == pygame.K_DOWN and data.currMenuOption < (len(data.mapOptions)-1):
            data.currMenuOption += 1 
        elif event.key == pygame.K_a: #pressing 'a' exits the menu
            data.mapMenuOpen = False
            data.currMenuOption = 0
        elif event.key == pygame.K_s:
            if data.mapOptions[data.currMenuOption] == 'End':
                #code below ends player's turn
                for unit in data.currTurnUnits:
                    unit.moved = False
                    unit.moveRange = []
                    unit.atkRange = []
                if data.currTurnUnits == data.playerUnits:
                    data.currTurnUnits = data.enemyUnits
                    data.opposTurnUnits = data.playerUnits
                else:
                    data.currTurnUnits = data.playerUnits 
                    data.opposTurnUnits = data.enemyUnits
                if data.playerTurn:
                    data.playerTurn = False
                else:
                    data.playerTurn = True
                data.mapMenuOpen = False
                data.currMenuOption = 0
    
    elif event.key == pygame.K_s:
        x, y = data.cursorLoc
        #selects the unit if no unit is currently selected and the tile currently 
        #selected by the cursor has a unit on it that has not moved yet
        if data.selectedUnit == None:
            for unit in (data.playerUnits + data.enemyUnits):    
                if unit.pos == (x,y) and unit.moved == False:
                    data.selectedUnit = unit 
                    data.selectedUnitStartPos = (x,y)
        #moves the selected unit if the tile selected is within the movement range
        #of the selected unit and it is that player's turn
        elif data.selectedUnit in data.currTurnUnits and (x,y) in data.selectedUnit.moveRange:
            data.selectedUnit.pos = (x,y)
            data.currMenuOption = 0
            data.commandMenuOpen = True
            #check to see if there is enemy within range to attack
            if data.selectedUnit.melee:
                for unit in data.opposTurnUnits:
                    if unit.pos == (x-1,y) or unit.pos == (x+1,y) or unit.pos == (x,y+1) \
                    or unit.pos == (x,y-1):
                        data.atkTargets.append(unit)
            if data.selectedUnit.ranged:
                for unit in data.opposTurnUnits:
                    if unit.pos == (x+2,y) or unit.pos == (x-2,y) or unit.pos == (x,y+2) \
                    or unit.pos == (x,y-2) or unit.pos == (x+1,y+1) or unit.pos == (x+1,y-1) \
                    or unit.pos == (x-1,y-1) or unit.pos == (x-1,y+1):
                        data.atkTargets.append(unit)
            if data.atkTargets != []:
                data.commandOptions.insert(0, 'Attack')
        if data.selectedUnit == None: 
            data.currMenuOption = 0
            data.mapMenuOpen = True
            
    elif event.key == pygame.K_a: #pressing 'a' de-selects
        if data.selectedUnit != None:
            data.selectedUnit = None
                  
    elif event.key == pygame.K_UP: #moves cursor up
        x, y = data.cursorLoc
        if isInGrid(data, x, y-1):
            data.cursorLoc = (x,y-1)
    elif event.key == pygame.K_DOWN: #moves cursor down
        x, y = data.cursorLoc
        if isInGrid(data, x, y+1):
            data.cursorLoc = (x,y+1)
    elif event.key == pygame.K_LEFT: #moves cursor left
        x, y = data.cursorLoc
        if isInGrid(data, x-1, y):
            data.cursorLoc = (x-1,y)
    elif event.key == pygame.K_RIGHT: #moves cursor right
        x, y = data.cursorLoc
        if isInGrid(data, x+1, y):
            data.cursorLoc = (x+1,y)
            
    
def drawGame(data, screen, width, height, moveTile, atkTile, objOverlay, tInfoOverlay,
            cInfoOverlay):
    #draws each map tile
    for x, row in enumerate(data.grid):
        for y, tile in enumerate(row):
            tile.drawTile(screen, data, x, y)
            
    #draws each unit
    for unit in (data.playerUnits + data.enemyUnits):
        unit.drawUnit(screen, data)
    
    #draws unit atk range if it has moved within range of enemy unit
    if data.commandMenuOpen or data.choosingWeapon or data.choosingAtk:
        if data.atkTargets != []:
            x, y = data.selectedUnit.pos
            if data.selectedUnit.melee:
                screen.blit(atkTile, ((x-1)*data.tileWidth, y*data.tileHeight))
                screen.blit(atkTile, ((x+1)*data.tileWidth, y*data.tileHeight))
                screen.blit(atkTile, (x*data.tileWidth, (y+1)*data.tileHeight))
                screen.blit(atkTile, (x*data.tileWidth, (y-1)*data.tileHeight))
            if data.selectedUnit.ranged:
                screen.blit(atkTile, ((x-2)*data.tileWidth, y*data.tileHeight))
                screen.blit(atkTile, ((x+2)*data.tileWidth, y*data.tileHeight))
                screen.blit(atkTile, (x*data.tileWidth, (y+2)*data.tileHeight))
                screen.blit(atkTile, (x*data.tileWidth, (y-2)*data.tileHeight))
                screen.blit(atkTile, ((x-1)*data.tileWidth, (y-1)*data.tileHeight))
                screen.blit(atkTile, ((x+1)*data.tileWidth, (y+1)*data.tileHeight))
                screen.blit(atkTile, ((x-1)*data.tileWidth, (y+1)*data.tileHeight))
                screen.blit(atkTile, ((x+1)*data.tileWidth, (y-1)*data.tileHeight))
        
    #draws the selected units move/attack range
    elif data.selectedUnit != None and not data.selectedUnit.moved:
        data.selectedUnit.getMoveRange(data)
        data.selectedUnit.getAttackRange(data)
        for pos in data.selectedUnit.moveRange:
            x, y = pos
            screen.blit(moveTile, (x*data.tileWidth, y*data.tileHeight))
        for pos in data.selectedUnit.atkRange:
            x, y = pos
            screen.blit(atkTile, (x*data.tileWidth, y*data.tileHeight))
    
    #current position of cursor 
    if data.choosingAtk:
        x, y = data.atkTargets[data.atkOption].pos
    else:
        x, y = data.cursorLoc
    position = (x*data.tileWidth,y*data.tileHeight,data.tileWidth,data.tileHeight)
            
    #draw the cursor
    pygame.draw.rect(screen, (255,255,0), position, 1)
    
    cursorOnUnit = False
    data.unitUnderCursor = None
    for unit in (data.playerUnits + data.enemyUnits):    
        if unit.pos == (x,y):
            cursorOnUnit = True
            data.unitUnderCursor = unit
    if data.selectedUnit != None:
        cursorOnUnit = True
        data.unitUnderCursor = data.selectedUnit
    if data.playerTurn:
        objOverlay.fill((0,0,255))
        tInfoOverlay.fill((0,0,255))
    else:
        objOverlay.fill((255,0,0))
        tInfoOverlay.fill((255,0,0))
        
    #gets cursor location area for use below
    if x < data.gridCols/3 and y < data.gridRows/3:
        data.cursorLocArea = 'NW'
    elif x >= 2*data.gridCols/3 and y < data.gridRows/3:
        data.cursorLocArea = 'NE'
    elif x >= 2*data.gridCols/3 and y >= 2*data.gridRows/3:
        data.cursorLocArea = 'SE'
    elif x < data.gridCols/3 and y >= 2*data.gridRows/3:
        data.cursorLocArea = 'SW'
        
    if data.choosingWeapon: 
        #draws menu for choosing weapon before combat
        menu = pygame.Surface((120, 35 * len(data.selectedUnit.weapons)))
        menu.fill((50,150,250))
        screen.blit(menu, (20,20))
        for i, weapon in enumerate(data.selectedUnit.weapons):
            weaponTxt = overlayFont.render(weapon.name, 0, (255,255,255))
            screen.blit(weaponTxt, (20+5, 20+5 + i*35))
        pygame.draw.rect(screen, (255,255,255), (20+3, 20+5+35*data.weaponOption, 
                        110, 26), 1)
        #draws info window about currently selected weapon
        info = pygame.Surface((240, 70))
        info.fill((50,150,250))
        screen.blit(info, (width-260, height-90))
        
        txt = overlayFont.render('Atk', 0, (255,255,255))
        screen.blit(txt, (width-255, height-85))
        
        txt = overlayFont.render('Hit', 0, (255,255,255))
        screen.blit(txt, (width-255, height-55))
        
        txt = overlayFont.render('Crit', 0, (255,255,255))
        screen.blit(txt, (width-140, height-85))
        
        txt = overlayFont.render('Avoid', 0, (255,255,255))
        screen.blit(txt, (width-140, height-55))
        
        currWeapon = data.selectedUnit.weapons[data.weaponOption]
        
        atk = data.selectedUnit.str + currWeapon.mt
        atkTxt = overlayFont.render(str(atk), 0, (255,255,255))
        atkTxt_rect = atkTxt.get_rect()
        atkTxt_rect.topright = (width-145, height-85)
        screen.blit(atkTxt, atkTxt_rect)
        
        hit = currWeapon.hit + (data.selectedUnit.skill*2) + (data.selectedUnit.luck//2)
        hitTxt = overlayFont.render(str(hit), 0, (255,255,255))
        hitTxt_rect = hitTxt.get_rect()
        hitTxt_rect.topright = (width-145, height-55)
        screen.blit(hitTxt, hitTxt_rect)
        
        crit = currWeapon.crit + (data.selectedUnit.skill//2)
        critTxt = overlayFont.render(str(crit), 0, (255,255,255))
        critTxt_rect = critTxt.get_rect()
        critTxt_rect.topright = (width-25, height-85)
        screen.blit(critTxt, critTxt_rect)
        
        avoid = (data.selectedUnit.spd*2) + data.selectedUnit.luck
        avoidTxt = overlayFont.render(str(avoid), 0, (255,255,255))
        avoidTxt_rect = avoidTxt.get_rect()
        avoidTxt_rect.topright = (width-25, height-55)
        screen.blit(avoidTxt, avoidTxt_rect)
        
    #draw command menu
    elif data.commandMenuOpen:
        if data.atkTargets != []:
            menu = pygame.Surface((60, 35*2))
            menu.fill((50,150,250))
            menuTxt1 = overlayFont.render('Attack', 0, (255,255,255))
            menuTxt2 = overlayFont.render('Wait', 0, (255,255,255))
            if data.cursorLocArea == 'NW' or data.cursorLocArea == 'SW':
                screen.blit(menu, (width-80, 40))
                screen.blit(menuTxt1, (width-80+5, 40+5))
                screen.blit(menuTxt2, (width-80+5, 40+5+35))
                pygame.draw.rect(screen, (255,255,255), (width-80+3, 
                40+5+35*data.currMenuOption, 49+4, 26), 1)
            else:
                screen.blit(menu, (20, 40))
                screen.blit(menuTxt1, (20+5, 40+5))
                screen.blit(menuTxt2, (20+5, 40+5+35))
                pygame.draw.rect(screen, (255,255,255), (20+3, 40+5+35*data.currMenuOption,
                                49+4, 26), 1)
        else:
            menu = pygame.Surface((60, 35))
            menu.fill((50,150,250))
            menuTxt1 = overlayFont.render('Wait', 0, (255,255,255))
            if data.cursorLocArea == 'NW' or data.cursorLocArea == 'SW':
                screen.blit(menu, (width-80, 40))
                screen.blit(menuTxt1, (width-80+5, 40+5))
                pygame.draw.rect(screen, (255,255,255), (width-80+3, 40+5, 49+4, 26), 1)
            else:
                screen.blit(menu, (20, 40))
                screen.blit(menuTxt1, (20+5, 40+5))
                pygame.draw.rect(screen, (255,255,255), (20+3, 40+5, 49+4, 26), 1)
    
    #draw map menu    
    elif data.mapMenuOpen:
        menu = pygame.Surface((60, 35))
        menu.fill((50,150,250))
        menuTxt1 = overlayFont.render('End', 0, (255,255,255))
        if data.cursorLocArea == 'NW' or data.cursorLocArea == 'SW':
            screen.blit(menu, (width-80, 40))
            screen.blit(menuTxt1, (width-80+5, 40+5))
            pygame.draw.rect(screen, (255,255,255), (width-80+3, 40+5, 49+4, 26), 1)
        else:
            screen.blit(menu, (20, 40))
            screen.blit(menuTxt1, (20+5, 40+5))
            pygame.draw.rect(screen, (255,255,255), (20+3, 40+5, 49+4, 26), 1)
     
    #display info panel overlays 
    #each overlay's location depends on the cursor's location 
    #the clockwise order is always cursor, objOverlay, tInfoOverlay, cInfoOverlay        
    elif data.cursorLocArea == 'NW':
        screen.blit(objOverlay, (3*width/4, 0))
        screen.blit(tInfoOverlay, (3*width/4, 4*height/5))
        if cursorOnUnit:
            screen.blit(cInfoOverlay, (0, 4*height/5))
            charTxt1 = overlayFont.render(data.unitUnderCursor.name, 0, (0,0,0))
            charTxt1_rect = charTxt1.get_rect(center=(0.5*width/4, 4.33*height/5))
            screen.blit(charTxt1, charTxt1_rect)
            charTxt2 = overlayFont.render("HP: %d / %d" %(data.unitUnderCursor.hp,
                        data.unitUnderCursor.totalhp), 0, (0,0,0))
            charTxt2_rect = charTxt2.get_rect(center=(0.5*width/4, 4.66*height/5))
            screen.blit(charTxt2, charTxt2_rect)
        objTxt = overlayFont.render('Defeat Enemy', 0, (255,255,255))
        objTxt_rect = objTxt.get_rect(center=(3.5*width/4, height/10))
        screen.blit(objTxt, objTxt_rect)
        terrainTxt = overlayFont.render(data.grid[x][y].name, 0, (255,255,255)) 
        terrainTxt_rect = terrainTxt.get_rect(center=(3.5*width/4, 4.5*height/5))
        screen.blit(terrainTxt, terrainTxt_rect)
    elif data.cursorLocArea == 'NE':
        screen.blit(objOverlay, (3*width/4, 4*height/5))
        screen.blit(tInfoOverlay, (0, 4*height/5))
        if cursorOnUnit:
            screen.blit(cInfoOverlay, (0, 0))
            charTxt1 = overlayFont.render(data.unitUnderCursor.name, 0, (0,0,0))
            charTxt1_rect = charTxt1.get_rect(center=(0.5*width/4, 0.33*height/5))
            screen.blit(charTxt1, charTxt1_rect)
            charTxt2 = overlayFont.render("HP: %d / %d" %(data.unitUnderCursor.hp,
                        data.unitUnderCursor.totalhp), 0, (0,0,0))
            charTxt2_rect = charTxt2.get_rect(center=(0.5*width/4, 0.66*height/5))
            screen.blit(charTxt2, charTxt2_rect)
        objTxt = overlayFont.render('Defeat Enemy', 0, (255,255,255))
        objTxt_rect = objTxt.get_rect(center=(3.5*width/4, 4.5*height/5))
        screen.blit(objTxt, objTxt_rect)
        terrainTxt = overlayFont.render(data.grid[x][y].name, 0, (255,255,255)) 
        terrainTxt_rect = terrainTxt.get_rect(center=(0.5*width/4, 4.5*height/5))
        screen.blit(terrainTxt, terrainTxt_rect)
    elif data.cursorLocArea == 'SE':
        screen.blit(objOverlay, (0, 4*height/5))
        screen.blit(tInfoOverlay, (0,0))
        if cursorOnUnit:
            screen.blit(cInfoOverlay, (3*width/4, 0))
            charTxt1 = overlayFont.render(data.unitUnderCursor.name, 0, (0,0,0))
            charTxt1_rect = charTxt1.get_rect(center=(3.5*width/4, 0.33*height/5))
            screen.blit(charTxt1, charTxt1_rect)
            charTxt2 = overlayFont.render("HP: %d / %d" %(data.unitUnderCursor.hp,
                        data.unitUnderCursor.totalhp), 0, (0,0,0))
            charTxt2_rect = charTxt2.get_rect(center=(3.5*width/4, 0.66*height/5))
            screen.blit(charTxt2, charTxt2_rect)
        objTxt = overlayFont.render('Defeat Enemy', 0, (255,255,255))
        objTxt_rect = objTxt.get_rect(center=(0.5*width/4, 4.5*height/5))
        screen.blit(objTxt, objTxt_rect)
        terrainTxt = overlayFont.render(data.grid[x][y].name, 0, (255,255,255)) 
        terrainTxt_rect = terrainTxt.get_rect(center=(0.5*width/4, 0.5*height/5))
        screen.blit(terrainTxt, terrainTxt_rect)
    elif data.cursorLocArea == 'SW':
        screen.blit(objOverlay, (0,0))
        screen.blit(tInfoOverlay, (3*width/4, 0))
        if cursorOnUnit:
            screen.blit(cInfoOverlay, (3*width/4, 4*height/5))
            charTxt1 = overlayFont.render(data.unitUnderCursor.name, 0, (0,0,0))
            charTxt1_rect = charTxt1.get_rect(center=(3.5*width/4, 4.33*height/5))
            screen.blit(charTxt1, charTxt1_rect)
            charTxt2 = overlayFont.render("HP: %d / %d" %(data.unitUnderCursor.hp,
                        data.unitUnderCursor.totalhp), 0, (0,0,0))
            charTxt2_rect = charTxt2.get_rect(center=(3.5*width/4, 4.66*height/5))
            screen.blit(charTxt2, charTxt2_rect)
        objTxt = overlayFont.render('Defeat Enemy', 0, (255,255,255))
        objTxt_rect = objTxt.get_rect(center=(0.5*width/4, 0.5*height/5))
        screen.blit(objTxt, objTxt_rect)
        terrainTxt = overlayFont.render(data.grid[x][y].name, 0, (255,255,255)) 
        terrainTxt_rect = terrainTxt.get_rect(center=(3.5*width/4, 0.5*height/5))
        screen.blit(terrainTxt, terrainTxt_rect)
        

#currently missing weapon triangle and terrain bonuses
def makeAttack(atkUnit, defUnit): 
    accuracy = atkUnit.hitRate() - defUnit.avoid()
    accuracy = max(accuracy, 0)
    accuracy = min(100, accuracy)
    
    critChance = atkUnit.critRate() - defUnit.critEvade()
    critChance = max(critChance, 0)
    
    damage = atkUnit.str + atkUnit.weapons[atkUnit.equipped].mt - defUnit.defense
    critDamage = 3*(atkUnit.str + atkUnit.weapons[atkUnit.equipped].mt) - defUnit.defense
    
    hitRoll = random.randint(1, 100)
    critRoll = random.randint(1, 100)
    if accuracy >= hitRoll: 
        if critChance >= critRoll:
            defUnit.hp -= critDamage
        else:
            defUnit.hp -= damage
            
            
def makeBlankMap(rows, cols):
    grid = []
    for row in range(rows):
        grid += [[grassTile] * cols]
    return grid

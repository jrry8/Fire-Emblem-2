import pygame

class Weapon(object):
    def __init__(self, name, Mt, Melee, Ranged, Hit, Wt, Crit, durability):
        self.name = name
        self.mt = Mt
        self.melee = Melee
        self.ranged = Ranged
        self.hit = Hit
        self.wt = Wt
        self.crit = Crit
        self.durab = durability
        self.currDurab = durability
    
    
class Consumable(object):
    def __init__(self, name, heal, durability):
        self.name = name
        self.heal = heal
        self.durab = durability
        self.currDurab = durability
       
#SWORDS =   Weapon(name                 Mt   Melee  Rnged   Hit   Wt   Crit  Durab       
ironSword = Weapon('Iron Sword',        5,   1,     0,      90,   5,   0,    46)
slimSword = Weapon('Slim Sword',        3,   1,     0,      100,  2,   5,    30)
steelSword = Weapon('Steel Sword',      8,   1,     0,      75,   10,  0,    30)
silverSword = Weapon('Silver Sword',    13,  1,     0,      80,   8,   0,    20)
ironBlade = Weapon('Iron Blade',        9,   1,     0,      70,   12,  0,    35)
steelBlade = Weapon('Steel Blade',      11,  1,     0,      65,   14,  0,    25)
silverBlade = Weapon('Silver Blade',    13,  1,     0,      60,   13,  0,    15)
shamshir = Weapon('Shamshir',           8,   1,     0,      75,   5,   35,   20)
killingEdge = Weapon('Killing Edge',    9,   1,     0,      75,   7,   30,   20)
#LANCES =   Weapon(name                 Mt   Melee  Rnged   Hit   Wt   Crit  Durab  
ironLance = Weapon('Iron Lance',        7,   1,     0,      80,   8,   0,    45)
slimLance = Weapon('Slim Lance',        4,   1,     0,      85,   4,   5,    30)
steelLance = Weapon('Steel Lance',      10,  1,     0,      70,   13,  0,    30)
silverLance = Weapon('Silver Lance',    14,  1,     0,      75,   10,  0,    20)
killerLance = Weapon('Killer Lance',    10,  1,     0,      70,   9,   30,   20)
javelin = Weapon('Javelin',             6,   1,     1,      65,   11,  0,    20)
spear = Weapon('Spear',                 12,  1,     1,      70,   10,  5,    15)
#AXES =     Weapon(name                 Mt   Melee  Rnged   Hit   Wt   Crit  Durab
ironAxe = Weapon('Iron Axe',            8,   1,     0,      75,   10,  0,    45)
steelAxe = Weapon('Steel Axe',          11,  1,     0,      65,   15,  0,    30)
silverAxe = Weapon('Silver Axe',        15,  1,     0,      70,   12,  0,    20)
killerAxe = Weapon('Killer Axe',        11,  1,     0,      65,   11,  30,   20)
handAxe = Weapon('Hand Axe',            7,   1,     1,      60,   12,  0,    20)
tomahawk = Weapon('Tomahawk',           13,  1,     1,      65,   14,  0,    15)
hatchet = Weapon('Hatchet',             4,   1,     1,      85,   5,   0,    50)
battleAxe = Weapon('Battle Axe',        13,  1,     0,      60,   15,  5,    20)
#BOWS =     Weapon(name                 Mt   Melee  Rnged   Hit   Wt   Crit  Durab
ironBow = Weapon('Iron Bow',            6,   0,     1,      85,   5,   0,    45)
steelBow = Weapon('Steel Bow',          9,   0,     1,      70,   9,   0,    30)
silverBow = Weapon('Silver Bow',        13,  0,     1,      75,   6,   0,    20)
killerBow = Weapon('Killer Bow',        9,   0,     1,      75,   7,   30,   20)
shortBow = Weapon('Short Bow',          5,   0,     1,      85,   3,   0,    22)
#CONSUMABLES
vulnerary = Consumable('Vulnerary', 10, 3)
elixir = Consumable('Elixir', 100, 3)


    
# Fire-Emblem-2
inspired by FE Sacred Stones

CONTROLS:
arrows keys move the cursor
's' button is equivalent to 'a' button on gameboy --> pressing 's' typically selects something
'a' button is equivalent to 'b' button on gameboy --> pressing 'a' typically un-selects or goes back to previous screen

Place the cursor on one of your units and press 's' to show the movement and attack range of that unit
Choose where you want to move the unit with the arrow keys. Press 's' to move. Press 'a' to cancel. 
After the unit moves, the command menu will appear. 
Use the arrow keys to scroll through the menu and select 'Attack'. Press 's' to confirm your decision. 
If there are no enemies within range, then select 'Wait' and press 's' to confirm your move. 
### MISSING FEATURES ###
Select weapon you want to use. 
If there are multiple enemies within your attack range, you will have to select which enemy you want to attack. 
See how well your unit matches up to your foe using the combat information window, then confirm your decision to attack. 
### ---------------- ###
To display the map menu, place the cursor on unoccupied spaces or on units that have completed their actions for that turn
and press 's'. 

### THINGS UNIMPLEMENTED OR IMPLEMENTED INCORRECTLY ###
- ranged attacks
- holding down arrow keys to move cursor fast (currently need to press 'a' and hold down arrow key)
- not displaying combat information window
### ----------------------------------------------- ###

UNIT PROPERTIES:
Unit name
Unit type
HP
Str
Skill
Spd
Luck
Def
Res
Move
Con

WEAPON PROPERTIES:
Item name
Item durability
Mt
Rng
Hit
Wt
Crit

BATTLE FORMULA:
if weapon weight <= unit con: atk spd = unit spd
if weapon weight > unit con: atk spd = unit spd - (weapon weight - unit con)

combat btw charA and charB
if charA spd - charB spd >= 4: A attacks twice
	if A initiates combat: A attacks, B attacks, A attacks
	if B initiates combat: B attacks, A attacks, A attacks
hit rate = weapon accuracy + (skill * 2) + (luck / 2)
avoid = (unit spd * 2) + luck + terrain bonus
accuracy = hit rate - avoid + triangle bonus
	accuracy is bound btw 0 and 100
	triangle bonus: weapon advtg = +15; weapon disadvtg = -15
critical rate = weapon critical + (skill / 2)
critical evade = luck
critical chance = critical rate - critical evade
atk power = unit str + weapon might + triangle bonus
	triangle bonus: weapon advtg = +1; weapon disadvtg = -1
def power = unit def + terrain bonus
damage = atk power - def power
	capped to be at least 0
critical damage: (3 * atk power) - def power
	capped to be at least 0

COMBAT INFO:
HP
Atk
Hit
Crit

ITEMS TO ADD:
weapons:
- swords (lances > swords > axes)
- lances (axes > lances > swords)
- axes (swords > axes > lances)
- bows 
- anima (dark > anima > light)
- light (anima > light > dark)
- dark (light > dark > anima)

consumables:
- vulnerary: restore 10 hp
- elixir: restore hp to full (really it just restores 100 hp; heal is capped at unit's max hp)

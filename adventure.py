# Adventure
# This is my first time using Python in years... so this might take a while. I am a bit rusty with this language

# null=input("")

import sys
import random
import math

# VARIABLES
balance = 50
hp = 100
generalinventory = []
weaponinventory = []


# BUFFS
healingmultiplier = 1 # healing x mult | throughout game should increase
damagemultiplier = 1 # damage x mult | throughout game should increase
resistancemultiplier = 1 # damage about to take x mult | throughout game should decrease

# MEMORY
wenttomuseum = False

# FUNCTIONS

def take_damage(amount):
    global hp
    damage = math.floor(amount * resistancemultiplier * random.uniform(0.90, 1.10))
    hp = hp - damage
    if 0 > hp:
        print("lmao dead")
        sys.exit()
    else:
        null=input("Took " + str(damage) + " points of damage!")
        null=input(str(hp) + " points left.")

def attack(weapon, type):
    if not weapon in weaponinventory:
        return("You don't have that weapon!")
    else:
        damage = math.floor(weapon["damage"] * damagemultiplier * random.uniform(0.90, 1.10))
        weapon["durability"] = weapon["durability"] - 1
        if weapon["durability"] < 0:
            null=input("Your weapon broke!")
            weaponinventory.remove(weapon)
        if type == "BUG":
            damage = damage * weapon["BugMultiplier"]
            null = input("Your weapon does " + str(weapon["BugMultiplier"]) + "x damage against bugs!")
        if type == "GOBLIN":
            damage = damage * weapon["GoblinMultiplier"]
        if type == "FUNGUS":
            damage = damage * weapon["FungusMultiplier"]
        if type == "SLIME":
            damage = damage * weapon["SlimeMultiplier"]
        if type == "ROBOT":
            damage = damage * weapon["RobotMultiplier"]
        null=input("You did " + str(damage) + " damage!")

# ITEMS (stored as dictionary)

STICK = {
    "name": "Stick",
    "damage": 1,
    "durability" : 10,
    "BugMultiplier":1,
    "GoblinMultiplier":1,
    "FungusMultiplier":1,
    "SlimeMultiplier": 1,
    "RobotMultiplier":1,
}


STRAW = {
    "name": "Stick",
    "damage": 0.1,
    "durability": 10,
    "BugMultiplier":1,
    "GoblinMultiplier":1,
    "FungusMultiplier":1,
    "SlimeMultiplier": 99999999999999,
    "RobotMultiplier":1,
}

print("Down The Trail")
print("R. Kiselev, Fall 2026")
null=input("Press ENTER to start. You will need to press ENTER to progress throughout the game. ")

name = input("What is your name? ")
print("Hello, " + name + ". Welcome to Mushroom Town!")
print("Mushroom Town is the last speckle of civilization before the trail begins... I assume you're here for that?")
null = input("")
print("In any case, you'll want to gear up before you tackle the trail... feel free to visit me in my shop!")
while True:
    choice = input("Where would you like to go? [SHOP/TRAIL/MUSEUM/] ")
    if choice.upper() == "SHOP":
        null = input("You decide to go to the shop. After all, only fools embark on a pilgrimage without shoes.")
        choice = input("A young boy sells sausages out of a bucket outside the shop. Do you buy one? [Y/N] ")
        if choice.upper() == "Y":
            null=input("You buy a sausage for 50 coins.")
            null=input("Sausage obtained.")
            null=input("You have 0 coins left.")
            balance = balance - 50
            generalinventory.append("SAUSAGE")
        else: 
            null=input("The boy sticks out his tongue, but says nothing.")
            null=input("You open the door and walk into the shop.")
        null = input("The old man from the prologue sits behind the counter counting his coins.")
        null=input('"Don\'t ask me how I know this," he said. "But you have ' + str(balance) + ' coins in that pocket of yours."')
        if balance == 0:
            null=input("The old man frowns.")
            null=input('"Wait... did you actually buy a sausage from my grandson?')
            null=input("The little boy runs in, smiling ear-to-ear.")
            null=input('"Well", says the old man. "I guess you can\'t buy ANYTHNG. You could\'ve purchased a sword, a potion, something."')
            null=input('"And you chose a sausage. Good luck on the trail!')
        else:
            null=input("There are a few things on the counter you could buy.")
            null=input("Most of it looks like junk. A used plastic straw, a used paper napkin, and a used religious statue.")
            choice=input("You should leave. [LEAVE/LEAVE/LEAVE] ")
            if choice.upper() == "LEAVE":
                null=input("Good choice.")
                break
            else: 
                choice=input("Seriously. [LEAVE/LEAVE/LEAVE] ")
                if choice.upper() == "LEAVE":
                    null=input("Good.")
                    break
                else:
                    null=input("FINE.")
                    null=input("BUY SOMETHING.")
                    choice=input("[STRAW / NAPKIN / STATUE] ")
                    if choice.upper() == "STRAW":
                        weaponinventory.append(STRAW)
                        null=input("Straw obtained. You spent all of your money.")
                        null=input("On a used plastic straw.")
                        null=input("Good job.")
                        balance = balance - 50
                        break
                    if choice.upper() == "NAPKIN":
                        generalinventory.append("NAPKIN")
                        null=input("Napkin obtained. You spent all your money.")
                        null=input("On a used paper napkin.")
                        null=input("Wow.")
                        balance = balance - 50
                        break
                    if choice.upper() == "STATUE":
                        generalinventory.append("STATUE")
                        null=input("Statue obtained. You spent all your money.")
                        null=input("On a used religious statue.")
                        null=input("Cool.")
                        balance = balance - 50
                        break
        break
    if choice.upper() == "TRAIL":
        null=input("Eh, who needs supplies? Maybe you're just built different.")
        break
    if choice.upper() == "MUSEUM" and wenttomuseum == True:
            null=input("...")
            null=input("I SAID, LET'S NOT GO BACK THERE AGAIN.")
    if choice.upper() == "MUSEUM" and wenttomuseum == False:
        null=input("You don't know why, but you feel the pressing urge to go to the Mushroom Museum.")
        null=input("When you walk in, it doesn't look very interesting. An employee lights up when she sees you.")
        null=input('"PLEASE", she cries. "IT\'S BEEN YEARS SINCE I\'VE SEEN A CUSTOMER!"')
        null=input("She clings on to you tightly. You peel her off and run out the door. Let's not go back there again.")
        wenttomuseum = True
    else:
        print("Oops! Item not found.")
null=input("So, the trail it is.")
null=input("You take the first step, and the journey begins.")
null = input("You take a step.")
null = input("You take a step.")
null = input("You take a step.")
null = input("You take a step.")
null = input("You take a step.")
if weaponinventory == []:
    null = input("You see a cool stick, so you pick it up.")
    weaponinventory.append(STICK)
null = input("You take a step.")
null = input("You take a step.")
null = input("You take a step.")
null = input("You take a step.")
null = input("You take a step.")
null = input("You step on an anthill.")
null = input("An ant storms out. He must be at least 5 feet tall.")
null = input('"Hey, you destroyed my house!"')
null = input('"Now, I shall destroy you!"')
null = input("The ant charges!")
null = input("The fight begins!")
null = input('Hint: this is what is commonly referred to as a "tutorial".')
while True:
    null = input("The ant runs at you!")
    if random.randint(1,2) == 1:
        null = input("He hits you!")
        take_damage(8)
    else: 
        null = input("He misses.")
    null = input("Your turn!")
    null = input("You can FIGHT or use an ITEM.")
    choice = input("[FIGHT/ITEM] ")
    if choice.upper() == "FIGHT":
        choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME/LIST] ')
        if choice.upper() == "LIST":
         null = input(", ".join(weapon["name"] for weapon in weaponinventory))
        else:
            attack(choice.upper()) 
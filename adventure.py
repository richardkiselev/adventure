
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
damage = 0


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
    if hp <= 0:
        print("lmao dead")
        sys.exit()
    else:
        null=input("Took " + str(damage) + " points of damage!")
        null=input(str(hp) + " points left.")

def useitem(item):
    global hp
    if item not in generalinventory:
        null=input("You don't have " + str(item) + " in your inventory!")
        return

    item_name = item["name"] if isinstance(item, dict) else item
    if item_name.upper() == "HONEYCOMB":
        old_hp = hp
        healing = math.floor(HONEYCOMB["healing"] * healingmultiplier)
        hp += min(healing, max(0, 100 - hp))
        healed = hp - old_hp
        null=input("You used the honeycomb and healed " + str(healed) + " points. Honeycomby.")
        generalinventory.remove(item)
    elif item_name.upper() == "NAPKIN":
        healed = max(0, 100 - hp)
        hp = max(100, hp)
        null=input("You used the napkin and healed " + str(healed) + " points. Napkiny.")
        generalinventory.remove(item)
    elif item_name.upper() == "SAUSAGE":
        hp *= 10
        null=input("You ate the sausage. You now have " + str(hp) + " health points. Sausagey.")
        generalinventory.remove(item)
    elif item_name.upper() == "POPCORN":
            old_hp = hp
            healing = math.floor(POPCORN["healing"] * healingmultiplier)
            hp += min(healing, max(0, 100 - hp))
            healed = hp - old_hp
            null=input("You used the popcorn and healed " + str(healed) + " points. Buttery.")
            generalinventory.remove(item)
    else:
        null=input("You can't use that item.")

def attack(weapon, type):
    if weapon not in weaponinventory:
        print("You don't have that weapon!")
        return 0
    else:
        damage = math.floor(weapon["damage"] * damagemultiplier * random.uniform(0.90, 1.10))
        weapon["durability"] = weapon["durability"] - 1
        if weapon["durability"] <= 0:
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
        return damage

# ITEMS (stored as dictionary)

STICK = {
    "name": "Stick",
    "damage": 4,
    "durability" : 10,
    "BugMultiplier":1,
    "GoblinMultiplier":1,
    "FungusMultiplier":1,
    "SlimeMultiplier": 1,
    "RobotMultiplier":1,
}


STRAW = {
    "name": "Straw",
    "damage": 0.1,
    "durability": 10,
    "BugMultiplier":1,
    "GoblinMultiplier":1,
    "FungusMultiplier":1,
    "SlimeMultiplier": 99999999999999,
    "RobotMultiplier":1,
}

SHARD = {
    "name": "Shard",
    "damage": 15,
    "durability": 30,
    "BugMultiplier":1.25,
    "GoblinMultiplier":1.5,
    "FungusMultiplier":1,
    "SlimeMultiplier": 1,
    "RobotMultiplier":1,
}

TORCH = {
    "name": "Torch",
    "damage": 25,
    "durability": 3,
    "BugMultiplier":2,
    "GoblinMultiplier":1,
    "FungusMultiplier":5,
    "SlimeMultiplier": 1,
    "RobotMultiplier":0.5,
}

GREATSTINGER = {
    "name": "Great Stinger",
    "damage": 999999999,
    "durability": 1,
    "BugMultiplier":9999,
    "GoblinMultiplier": 9999,
    "FungusMultiplier":9999,
    "SlimeMultiplier": 9999,
    "RobotMultiplier":9999,
}

HONEYCOMB = {
    "name": "Honeycomb",
    "healing": 25,
}

POPCORN = {
    "name": "Popcorn",
    "healing": 30,
}

# ENEMY VARIABLES
AntHP = 10
PikaHP = 40
waspHP = 75

# GAME BEGINS

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
        choice = input("A young boy sells sausages out of a bucket outside the shop. Do you buy one? [Y / N] ")
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
            choice=input("You should leave. [LEAVE / LEAVE / LEAVE] ")
            if choice.upper() == "LEAVE":
                null=input("Good choice.")
                break
            else: 
                choice=input("Seriously. [LEAVE / LEAVE / LEAVE] ")
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
                        null=input("Statue obtained. You spent all your money.")
                        null=input("On a used religious statue.")
                        null=input("It increases your healing by 10%.")
                        healingmultiplier += 0.1
                        balance = balance - 50
                        break
        break
    if choice.upper() == "TRAIL":
        null=input("Eh, who needs supplies? Maybe you're just built different.")
        break
    if choice.upper() == "MUSEUM" and wenttomuseum == True:
            null=input("...")
            null=input("I SAID, LET'S NOT GO BACK THERE AGAIN.")
    elif choice.upper() == "MUSEUM" and wenttomuseum == False:
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
while True: # Battle loop
    null = input("The ant runs at you!")
    if random.randint(1,2) == 1:
        null = input("He hits you!")
        take_damage(8)
    else: 
        null = input("He misses.")
    null = input("Your turn!")
    null = input("You can FIGHT or use an ITEM.")
    choice = input("[FIGHT / ITEM] ")
    if choice.upper() == "FIGHT":
        choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
        if choice.upper() == "LIST":
            null = input(", ".join(weapon["name"] for weapon in weaponinventory))
            continue

        weapon_found = False
        for weapon in weaponinventory:
            if choice.upper() == weapon["name"].upper():
                damage = attack(weapon, "BUG")
                weapon_found = True
                AntHP = AntHP - damage
                null = input("Ant has " + str(AntHP) + " points left.")
                break
        if AntHP < 1:
            null = input("You killed the ant!")
            break
        if not weapon_found:
            null = input("Item not found. For a list of your weapons, see the list.")
    elif choice.upper() == "ITEM":
        choice = input('What item do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
        if choice.upper() == "LIST":
            item_names = [item["name"] if isinstance(item, dict) else item for item in generalinventory]
            null = input(", ".join(item_names))
            continue
        item_found = False
        for item in generalinventory:
            item_name = item["name"] if isinstance(item, dict) else item
            if choice.upper() == item_name.upper():
                useitem(item)
                item_found = True
                break
        if not item_found:
            null = input("Item not found. For a list of your items, see the list.")
    else:
        null = input("Please choose FIGHT or ITEM.")
null = input("The ant is dead.")
choice = input("Do you loot its corpse? [Y / N] ")
if choice.upper() == "Y":
    null=input("You find a picture of the ant with his family.")
    null=input("He has a wife and two young children.")
    null=input("There's something seriously wrong with you.")
null=input("And so you continue on the great trail.")
null=input("Along the way, you come across a friendly bumblebee.")
null=input("The bee buzzes buzzily.")
null=input('"Come partake in my village\'s Honey Festival", she tells you.')
choice=input("Do you go? [Y / N] ")
if choice.upper() == "Y":
    null=input("She smiles at you and slowly starts to fly towards the village.")
    null=input("You follow her through the brambles and the branches.")
else: 
    null=input("Look, honestly, this is a whole thing with like the magical honeycomb and the stinger sword... can you please just go?")
    choice=input("Do you go? [Y / N] ")
    if choice.upper() == "Y":
        null=input("Great. You follow the bee through the woods.")
    else:
        null=input("...")
        null=input("Okay, give me a second to think of something.")
        null=input("...")
        null=input("...")
        null=input("...")
        null=input("Okay. The bee stings you and you pass out and you wake up in the village. Your health is set to 1.")
        hp = 1
null=input("The village is wonderful. Bumbles float lazily through the air.")
null=input("Thatched huts and tall temples adorn the hillside.")
null=input("This seems strange to you. Don't bees live in hives?")
null=input("You ask your new bee friend. She seems offended.")
null=input('"Not all bees live like that. We\'re country folk."')
null=input("She names a few places you might want to check out. Where do you go?")
while True:
    location = input("[SHOP / HOSPITAL / MUSEUM / CAVE] ")
    if location.upper() == "SHOP":
        null=input('The shop\'s sign reads "Jasper\'s Emporium".')
        null=input("A short bee snoozes behind the counter.")
        null=input("His glasses have fallen a little bit and they rest on his nose while he snores.")
        null=input("As you open the door, a little bell rings and he falls out of his seat.")
        null=input("A variety of items lay on the table. Glistening honeycomb, a stinger shard, and a little bee plushie.")
        choice=input("You can buy an item. Or leave. [HONEYCOMB / SHARD / PLUSH / LEAVE] ")
        if choice.upper() == "HONEYCOMB":
            if balance >= 20:
                null=input("You buy the honeycomb for 20 coins. It will heal you during battle.")
                balance -= 20
                generalinventory.append(HONEYCOMB)
            else:
                null=input("You don't have enough coins for the honeycomb.")
        elif choice.upper() == "SHARD":
            if balance >= 40:
                null=input("You buy the shard for 40 coins.")
                null=input('"It\'s a capable weapon," Jasper says.')
                null=input('"But it\'s only a piece that fractured off the Great Stinger. Not sure where the whole thing is.')
                balance -= 40
                weaponinventory.append(SHARD)
            else:
                null=input("You don't have enough coins for the shard.")
        elif choice.upper() == "PLUSH":
            if balance >= 15:
                null=input("You buy the plush for 15 coins. It will provide a healing bonus. All healing items are more effective.")
                balance -= 15
                healingmultiplier += 0.1
            else:
                null=input("You don't have enough coins for the plush.")
        elif choice.upper() == "LEAVE":
            null=input("You leave. Jasper goes back to sleep.")
        else:
            null=input("Jasper looks at you. He doesn't sell that.")
    elif location.upper() == "HOSPITAL":
        null=input("The hospital's doors slide open as you walk up.")
        null=input("A nurse sits behind the counter.")
        if hp < 100: 
            null=input("With a kiss on the cheek and a spoonful of honey, he heals you back to full health.")
            hp = 100
        
    elif location.upper() == "MUSEUM":
        null=input("A chipper preteen sits, his nose buried in a thick book about bee history.")
        null=input("You feel like if he sees you, he'll jump into an ardous monologue.")
        null=input("You have the chance to slip back out the door before he spots you.")
        choice=input("Do you try? [Y / N] ")
        if choice.upper() == "Y":
            null=input("You quietly open the door and run away.")
        else:
            null=input("You step forward. The bee child looks up and his face lights up.")
            null=input('"You\'re here to learn about bee history!?"')
            null=input("He tells you that you're the first person to come by in years.")
            null=input("Then, the story begins...")
            null=input("[3 hours later]")
            null=input('"And that\'s how the wasps got banished to the cave!"')
            null=input("After a few seconds, he unties you and gives you a gold star sticker.")
            null=input("Your bones creak as you stand up and stumble out the door.")

    elif location.upper() == "CAVE":
        null=input("The Cave of Wasps stands before you, ominously.")
        null=input("It's pretty spooky.")
        null=input("Your bee friend looks worried.")
        null=input('"Why would you ever want to go in there?"')
        null=input("Honestly, it doesn't matter what you tell her. You have to enter the cave anyway. Plot progression and all.")
        null=input("You walk inside. As you continue, it gets darker and darker, until you can't even see her face.")
        null=input("You are well into the Cave of Wasps.")
        null=input("Faint buzzing noises echo off the stone walls...")
        break
    else:
        null=input('Your bee friend looks confused. "Sorry, could you say that again?"')
null=input("You find a burnt out torch on the ground. You can try to light it.")
choice=input("Do you try? [Y / N] ")
if choice.upper() == "Y":
    null=input("You pick up the torch and attempt to spark it.")
    null=input("You're succesful! A lovely fire starts up and you can see the entire cave.")
    null=input("Burning Torch added to Weapons.")
    null=input("You take a look around. There are no wasps.")
    null=input("But you can feel an ominous presence...")
    null=input("A whoosh of air... the imposing aura of a soul...")
    null=input("No, not a soul. Souls... hundreds of them.")
    null=input("You know what's coming for you before you see them.")
    null=input("Five hundred moths barrel towards the light in your hand.")
    null=input("You can throw the torch away from you. You could try swiping at the moths. Or you could set yourself on fire.")
    choice=input("[THROW / ATTACK / WHYWOULDYOUDOTHIS]")
    if choice.upper() == "THROW":
        null=input("You throw the torch far away from you. The torch hits the floor and breaks.")
        null=input("Burning Torch removed from Weapons.")
        null=input("The light goes out and the moths stop in their tracks.")
        null=input("Then they collectively move in a single direction.")
    elif choice.upper() == "ATTACK":
        null=input("You swipe the torch at the moths.")
        null=input("Dozens burn to a crisp as flames roast their sides.")
        null=input("Enraged, the rest fly into your eyes.")
        null=input("They don't do much physical damage, but the psychological harm does 40 damage.")
        hp = hp - 40
        null=input("Then, the moths run away. You hold on to the torch, now imbued with 50 souls.")
        weaponinventory.append(TORCH)
    else:
        null=input("You set yourself on fire for some reason.")
        null=input("Your flailing body manages to put itself out. You are left on 1 health point.")
        null=input("Unfortunately, a single hair on your head maintains a small flame. A lost moth zooms into you and does 1 damage.")
        hp = 0
        print("lmao dead")
        sys.exit()
else:
    null=input("Since you're boring as hell, you move on without touching the torch.")
null=input("You proceed into the cave.")
null=input("A hazelnut tree sits in a clearing by a creek.")
null=input("You could choose to eat the hazelnuts. Or you could pick them and hold on to them.")
choice=input("What do you do? [EAT / STORE]")
if choice.upper() == "EAT":
    null=input("Okay, fatty.")
    null=input("You eat 50 hazelnuts.")
    null=input("They make you feel pretty sick, but otherwise you're okay.")
else: 
    null=input("You grab the hazelnuts and store them in your bag.")
    null=input("Hazelnuts have been added to your item inventory.")
    generalinventory.append("HAZELNUTS")
    null=input("Someone else might like them.")
null=input("And you keep on moving.")
null=input("Finally, you spot it.")
null=input("In the Cave of Wasps, is a wasp.")
null=input("It doesn't see you. You can attack it without it seeing you.")
choice=input("Attack? [Y / N] ")
attacked_wasp = choice.upper() == "Y"
if attacked_wasp:
    null=input("You bean the wasp in the back of the head with a rock.")
    null=input("The wasp's body crumbles like a straw.")
    null=input("Looking a bit closer, it looks like a little child...")
    null=input("The child of someone...something bigger...")
    null=input("A shadow grows bigger across the cavern...")
    null=input("It's a pika!")
    null=input("(not pikachu, this is like a cave rat thing that eats grasses and moss and nuts and stuff)")
    null=input('"HEY!", the pika says. "YOU KILLED MY DAUGHTER!"')
    null=input("uh oh")
    null=input("battle time!")
else:
    null=input("you leave the wasp alone.")
    null=input("after all, she didn't do anything to you.")
    null=input("The wasp's mother appreciates that. Unfortunately, she doesn't particularly appreciate you being in her house.")
while attacked_wasp: # Battle loop
    null = input("Pika charges!")
    if random.randint(1,2) == 1:
        null = input("She hits you!")
        take_damage(20)
    else: 
        null = input("She misses.")
    null = input("Your turn!")
    null = input("You can FIGHT or use an ITEM.")
    choice = input("[FIGHT / ITEM] ")
    if choice.upper() == "FIGHT":
        choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
        if choice.upper() == "LIST":
            null = input(", ".join(weapon["name"] for weapon in weaponinventory))
            continue

        weapon_found = False
        for weapon in weaponinventory:
            if choice.upper() == weapon["name"].upper():
                damage = attack(weapon, "N/A")
                weapon_found = True
                PikaHP = PikaHP - damage
                null = input("Pika has " + str(PikaHP) + " points left.")
                break
        if PikaHP < 1:
            null = input("You killed the pika!")
            break
        if not weapon_found:
            null = input("Item not found. For a list of your weapons, see the list.")
    elif choice.upper() == "ITEM":
        choice = input('What item do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
        if choice.upper() == "LIST":
            item_names = [item["name"] if isinstance(item, dict) else item for item in generalinventory]
            null = input(", ".join(item_names))
            continue
        item_found = False
        for item in generalinventory:
            item_name = item["name"] if isinstance(item, dict) else item
            if choice.upper() == item_name.upper():
                if item_name.upper() == "HAZELNUTS":
                    null = input("You offer the hazelnuts to the pika. She stops fighting to eat them.")
                    PikaHP = 0
                    generalinventory.remove(item)
                else:
                    useitem(item)
                item_found = True
                break
        if PikaHP < 1:
            null = input("The pika is distracted by the hazelnuts and leaves you alone.")
            break
        if not item_found:
            null = input("Item not found. For a list of your items, see the list.")
    else:
        null = input("Please choose FIGHT or ITEM.")
null = input("Bye, bye pika!")
null=input("And so, you move on.")
null=input("Behind you, you hear a buzzing.")
null=input("Quick time event!")
null=input("Ready?")
null=input("3...")
null=input("2...")
null=input("1...")
null=input("0.75...")
null=input("0.50...")
null=input("0.40...")
null=input("0.30...")
null=input("0.20...")
null=input("0.10...")
null=input("0.09...")
null=input("0.08...")
null=input("0.07...")
choice=input('Type "TURN AROUND!"')
if choice == "TURN AROUND!":
    null=input("Huh... you reacted in time...")
    null=input("Uhh... +1 health for you")
    hp += 1
elif choice == "TURN AROUND":
    null=input("You forgot the exclamation mark.")
    null=input("-1 health for you!")
    hp -= 1
else: 
    null=input("uhh.. okay")
    null=input("you missed the quick time event")
    null=input("somehow")
    null=input("you get beaned on the head. -10 health for you")
null=input("You turn around to see Sammy the Sentient Microwave buzzing.")
null=input("Do you buy microwave popcorn from him?")
choice=input("[Y / N] ")
if choice.upper() == "Y":
    if balance > 10:
        balance = balance - 10
        null=input("You buy the popcorn for 10 coins.")
        null=input("You open the bag to find a wasp.")
        null=input('"Thank you for freeing me", it says.')
        null=input("Then it stings you on the nose. The fight has begun.")
    else: 
        null=input("You grab the popcorn and start eating.")
        null=input("Unfortunately, you cannot afford the popcorn.")
        null=input("For scamming him, Sammy socks you in the face.")
        null=input("-10 hp")
        hp = hp - 10
else: 
    null=input("You don't buy the popcorn.")
    null=input("Kind of a mistake on your part, but whatever.")
    null=input("Sammy goes away, dejected.")
    null=input("Behind him sits the giant wasp.")
    null=input("So... you have to fight it anyway.")
boss_wasp = True
while boss_wasp: # Battle loop
    null = input("wasp charges!")
    if random.randint(1,2) == 1:
        null = input("She hits you!")
        take_damage(30)
    else: 
        null = input("She misses.")
    null = input("Your turn!")
    null = input("You can FIGHT or use an ITEM.")
    choice = input("[FIGHT / ITEM] ")
    if choice.upper() == "FIGHT":
        choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
        if choice.upper() == "LIST":
            null = input(", ".join(weapon["name"] for weapon in weaponinventory))
            continue

        weapon_found = False
        for weapon in weaponinventory:
            if choice.upper() == weapon["name"].upper():
                damage = attack(weapon, "N/A")
                weapon_found = True
                waspHP = waspHP - damage
                null = input("wasp has " + str(waspHP) + " points left.")
                break
        if waspHP < 1:
            null = input("You killed the wasp!")
            break
        if not weapon_found:
            null = input("Item not found. For a list of your weapons, see the list.")
    elif choice.upper() == "ITEM":
        choice = input('What item do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
        if choice.upper() == "LIST":
            item_names = [item["name"] if isinstance(item, dict) else item for item in generalinventory]
            null = input(", ".join(item_names))
            continue
        item_found = False
        for item in generalinventory:
            item_name = item["name"] if isinstance(item, dict) else item
            if choice.upper() == item_name.upper():
                if item_name.upper() == "POPCORN":
                    null = input("Look, wasps LOVE popcorn. But this one in particular doesn't seem interested.")
                else:
                    useitem(item)
                item_found = True
                break
        if waspHP < 1:
            null = input("The wasp dies.")
            break
        if not item_found:
            null = input("Item not found. For a list of your items, see the list.")
    else:
        null = input("Please choose FIGHT or ITEM.")
null = input("The wasp is gone.")
choice = input("Do you loot the body? [Y / N] ")
if choice.upper() == "Y":
    null = input("You plant your foot on the wasp and grab the stinger with both hands.")
    null = input("With a sickening snap, you rip the stinger off the wasp.")
    null = input("Great Stinger obtained.")
    null = input("It feels fragile... like it's made of glass.")
    null = input("It's sharp, but you can't help but worry that even a single hit will shatter the tip instantly.")
    weaponinventory.append(GREATSTINGER)
else: 
    null = input("You decide to leave the body alone.")
null = input("A light creeps through the rocks. You peek your head out.")
null = input("You can see the bee village far off in the distance. You must've walked for hours in that cave...")
choice = input("Go back? [Y/N] ")
if choice.upper() == "Y":
    null = input("You get up and start moving towards the village.")
else:
    null = input("You decide to move on, down the trail.")
null = input("Just then, you feel a strange presence behind you.")
null = input("Grubby hands grab your neck and press hard on your artery.")
null = input("Everything goes dark...")
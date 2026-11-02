    # Adventure
    # This is my first time using Python in years... so this might take a while. I am a bit rusty with this language

import sys
import random
import math
import re
import pygame
import threading

# VARIABLES
balance = 50
hp = 100
maxHP = 100
generalinventory = []
weaponinventory = []
damage = 0
screencolor = (34, 139, 34)
fillcolor = (42, 86, 42)
chapter = ""
adding = ""
spell = None
slimeballs = 0
patience_timer = None
patience_completed = False
accountbalance = 0
loan = 0
interest = 1.20

# PYGAME
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Down The Trail")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 26)
hpfont = pygame.font.Font(None, 50)
chapterfont = pygame.font.Font(None, 40)
clock = pygame.time.Clock()



def input(prompt: str = "") -> str:
    match = re.search(r"\[([^\]]+)\]", prompt)
    options = []
    if match:
        options = [
            option.strip().upper()
            for option in match.group(1).split("/")
            if option.strip() and "ITEMNAME" not in option.upper()
        ]

    answer = ""
    pygame.key.start_text_input()
    try:
        while True:
            hptext = hpfont.render(f"HP: {hp}", True, (255, 50, 50))
            hprect = hptext.get_rect(topright=(1200, 255))
            textcolor = (255, 255, 255)
            chaptertext = hpfont.render(chapter, True, (textcolor))
            chapterrect = chaptertext.get_rect(topright=(1200, 410))
            balancetext =  hpfont.render(f"Coins: {balance}", True, (120, 120, 180))
            balancerect =  balancetext.get_rect(topright=(1200, 300))
            button_rects = []
            screen.fill((fillcolor))
            pygame.draw.rect(screen, (screencolor), (40, 40, 1200, 640), border_radius=18)
            screen.blit(hptext, hprect)
            screen.blit(chaptertext, chapterrect)
            screen.blit(balancetext, balancerect)
            y = 75
            for line in _wrap_text(prompt, font, 920):
                text_surface = font.render(line, True, (242, 238, 220))
                screen.blit(text_surface, (80, y))
                y += 42
            if options:
                button_y = 535
                gap = 12
                button_width = min(1120 // len(options) - gap, 300)
                total_width = len(options) * button_width + (len(options) - 1) * gap
                button_x = (1280 - total_width) // 2
                for option in options:
                    rect = pygame.Rect(button_x, button_y, button_width, 54)
                    pygame.draw.rect(screen, (192, 132, 71), rect, border_radius=10)
                    label = small_font.render(option, True, (24, 35, 44))
                    screen.blit(label, label.get_rect(center=rect.center))
                    button_rects.append((rect, option))
                    button_x += button_width + gap
                instruction = "Anything you type will show up here"
            else:
                instruction = "Anything you type will show up here"
            pygame.draw.rect(screen, (18, 27, 34), (80, 610, 1120, 46), border_radius=8)
            answer_surface = small_font.render(answer or instruction, True, (220, 220, 205))
            screen.blit(answer_surface, (96, 622))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        raise SystemExit
                    if event.key == pygame.K_BACKSPACE:
                        answer = answer[:-1]
                    elif event.key == pygame.K_RETURN:
                        return answer
                elif event.type == pygame.TEXTINPUT:
                    answer += event.text
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, option in button_rects:
                        if rect.collidepoint(event.pos):
                            return option
                    if not options:
                        return answer
            clock.tick(60)
    finally:
        pygame.key.stop_text_input()

def patience_reward():
    global patience_completed
    patience_completed = True

def _wrap_text(text, selected_font, max_width):
    lines = []
    for paragraph in text.splitlines() or [""]:
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}".strip()
            if line and selected_font.size(candidate)[0] > max_width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines
# BUFFS
healingmultiplier = 1 # healing x mult | throughout game should increase
damagemultiplier = 1 # damage x mult | throughout game should increase
resistancemultiplier = 1 # damage about to take x mult | throughout game should decrease

# MEMORY
wenttomuseum = False
sdcounter = 0
escapedocean = False
meditationcounter = 0
charity = True
attacked_goblin = False
# FUNCTIONS
def say(text):
    input(text)

def input_integer(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            say("Please enter a whole number.")
            continue
        if value < minimum:
            say("Please enter a number of at least " + str(minimum) + ".")
            continue
        return value

def take_damage(amount):
    global hp
    damage = math.floor(amount * resistancemultiplier * random.uniform(0.90, 1.10))
    hp = hp - damage
    if hp <= 0:
        print("lmao dead")
        sys.exit()
    else:
        say("Took " + str(damage) + " points of damage!")
        say(str(hp) + " points left.")

def lose_health(amount):
    global hp
    hp -= amount
    if hp <= 0:
        say("lmao dead")
        sys.exit()

def useitem(item):
    global hp
    if item not in generalinventory:
        say("You don't have " + str(item) + " in your inventory!")
        return
    item_name = item["name"] if isinstance(item, dict) else item
    if item_name.upper() == "HONEYCOMB":
        old_hp = hp
        healing = math.floor(HONEYCOMB["healing"] * healingmultiplier)
        hp += min(healing, max(0, maxHP - hp))
        healed = hp - old_hp
        say("You used the honeycomb and healed " + str(healed) + " points. Honeycomby.")
        generalinventory.remove(item)
    elif item_name.upper() == "NAPKIN":
        old_hp = hp
        hp = maxHP
        healed = hp - old_hp
        say("You used the napkin and healed " + str(healed) + " points. Napkiny.")
        generalinventory.remove(item)
    elif item_name.upper() == "SAUSAGE":
        hp *= 10
        say("You ate the sausage. You now have " + str(hp) + " health points. Sausagey.")
        generalinventory.remove(item)
    elif item_name.upper() == "POPCORN":
            old_hp = hp
            healing = math.floor(POPCORN["healing"] * healingmultiplier)
            hp += min(healing, max(0, maxHP - hp))
            healed = hp - old_hp
            say("You used the popcorn and healed " + str(healed) + " points. Buttery.")
            generalinventory.remove(item)
    else:
        say("You can't use that item.")
def attack(weapon, type):
    if weapon not in weaponinventory:
        print("You don't have that weapon!")
        return 0
    if type == "SLIME" and weapon["name"].upper() != "STRAW":
        say("Your weapon fails to pierce the thick goo.")
        say("It bounces off harmlessly.")
        return 0
    if type == "SLIME":
        damage = 100
    else:
        damage = max(1, math.floor(weapon["damage"] * damagemultiplier * random.uniform(0.90, 1.10)))
        if type == "BUG":
            damage = damage * weapon["BugMultiplier"]
            say("Your weapon does " + str(weapon["BugMultiplier"]) + "x damage against bugs!")
        if type == "GOBLIN":
            damage = damage * weapon["GoblinMultiplier"]
        if type == "FUNGUS":
            damage = damage * weapon["FungusMultiplier"]
        if type == "ROBOT":
            damage = damage * weapon["RobotMultiplier"]
    weapon["durability"] -= 1
    if weapon["durability"] <= 0:
        say("Your weapon broke!")
        weaponinventory.remove(weapon)
    say("You did " + str(damage) + " damage!")
    return damage
# ITEMS (stored as dictionary)
STICK = {
    "name": "Stick",
    "damage": 4,
    "durability" : 10,
    "BugMultiplier":1,
    "GoblinMultiplier":1,
    "SlimeMultiplier": 9999,
    "FungusMultiplier":1,
    "RobotMultiplier":1,
}
STRAW = {
    "name": "Straw",
    "damage": 0.1,
    "durability": 3,
    "BugMultiplier":1,
    "GoblinMultiplier":1,
    "SlimeMultiplier": 1000,
    "FungusMultiplier":1,
    "RobotMultiplier":1,
}
SHARD = {
    "name": "Shard",
    "damage": 15,
    "durability": 30,
    "BugMultiplier":1.25,
    "GoblinMultiplier":1.5,
    "SlimeMultiplier": 1,
    "FungusMultiplier":1,
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
    "SlimeMultiplier": 9999,
    "FungusMultiplier":9999,
    "RobotMultiplier":0,
}
HONEYCOMB = {
    "name": "Honeycomb",
    "healing": 25,
}
POPCORN = {
    "name": "Popcorn",
    "healing": 30,
}
CHIPS = {
    "name": "Chips",
    "healing": 30,
}
GUMMIES = {
    "name": "Gummies",
    "healing": 25,
}
JERKY = {
    "name": "Jerky",
    "healing": 35,
}

weapons = {
    "STICK": STICK,
    "STRAW": STRAW,
    "SHARD": SHARD,
    "TORCH": TORCH,
    "GREATSTINGER": GREATSTINGER
}

SPELLS = {
    "LIGHTNING": {"name": "Lightning", "cost": 5, "damage": 100},
    "FIREBLAST": {"name": "Fireblast", "cost": 5, "damage": 80},
    "RAIN": {"name": "Scary Rain", "cost": 5, "damage": 60},
}

# ENEMY VARIABLES
AntHP = 10
PikaHP = 40
waspHP = 50
GoblinHP = 50
collector_hp = 75
slimeHP = 30
giantslimeHP = 300

checkpoint = ""
startgame = False
# GAME BEGINS
say("Down The Trail")
say("Click or press ENTER to advance the story, or choose an option with the mouse.")
say("Anything you type will show up in that box down there.")
password = input("Admin?")
if password == "oh yeah":
    checkpoint = input("If you have a checkpoint, input it here.")
    balance = input_integer("How much money?")
    while True:
        if startgame == False:
            addingweapon = input("Weapons?")
            if addingweapon.lower() == "stop":
                break
            elif addingweapon.upper() in weapons:
                weaponinventory.append(weapons[addingweapon.upper()])
            else:
                say("Weapon not found.")

if checkpoint in {"GoblinsRCool", "SlimeTime"} and not weaponinventory:
    say("You find a cool stick, so you pick it up.")
    weaponinventory.append(STICK)
    
if checkpoint != "GoblinsRCool" and checkpoint != "SlimeTime":
    name = input("What is your name? (use keyboard) ")
    say("Hello, " + name + ". Welcome to Mushroom Town!")
    say("Mushroom Town is the last speckle of civilization before the trail begins... I assume you're here for that?")
    say("In any case, you'll want to gear up before you tackle the trail... feel free to visit me in my shop!")
    while True:
        choice = input("Where would you like to go? [SHOP/TRAIL/MUSEUM/] ")
        if choice.upper() == "SHOP":
            say("You decide to go to the shop. After all, only fools embark on a pilgrimage without shoes.")
            choice = input("A young boy sells sausages out of a bucket outside the shop. Do you buy one? [Y / N] ")
            if choice.upper() == "Y":
                say("You buy a sausage for 50 coins.")
                say("Sausage obtained.")
                say("You have 0 coins left.")
                balance = balance - 50
                generalinventory.append("SAUSAGE")
            else: 
                say("The boy sticks out his tongue, but says nothing.")
                say("You open the door and walk into the shop.")
            say("The old man from the prologue sits behind the counter counting his coins.")
            say('"Don\'t ask me how I know this," he said. "But you have ' + str(balance) + ' coins in that pocket of yours."')
            if balance == 0:
                say("The old man frowns.")
                say('"Wait... did you actually buy a sausage from my grandson?')
                say("The little boy runs in, smiling ear-to-ear.")
                say('"Well", says the old man. "I guess you can\'t buy ANYTHNG. You could\'ve purchased a sword, a potion, something."')
                say('"And you chose a sausage. Good luck on the trail!')
            else:
                say("There are a few things on the counter you could buy.")
                say("Most of it looks like junk. A used plastic straw, a used paper napkin, and a used religious statue.")
                choice=input("You should leave. [LEAVE / LEAVE / LEAVE] ")
                if choice.upper() == "LEAVE":
                    say("Good choice.")
                    break
                else: 
                    choice=input("Seriously. [LEAVE / LEAVE / LEAVE] ")
                    if choice.upper() == "LEAVE":
                        say("Good.")
                        break
                    else:
                        say("FINE.")
                        say("BUY SOMETHING.")
                        choice=input("[STRAW / NAPKIN / STATUE] ")
                        if choice.upper() == "STRAW":
                            weaponinventory.append(STRAW)
                            say("Straw obtained. You spent all of your money.")
                            say("On a used plastic straw.")
                            say("Looks like it could be good at sucking up goop.")
                            say("Good job.")
                            balance = 0
                            break
                        if choice.upper() == "NAPKIN":
                            generalinventory.append("NAPKIN")
                            say("Napkin obtained. You spent all your money.")
                            say("On a used paper napkin.")
                            say("Wow.")
                            say("You fold it into your pocket like a hankerchief.")
                            say("Somehow, you feel healthier.")
                            maxHP = maxHP + 20
                            balance = 0
                            break
                        if choice.upper() == "STATUE":
                            say("Statue obtained. You spent all your money.")
                            say("On a used religious statue.")
                            say("It increases your healing by 10%, though.")
                            healingmultiplier += 0.1
                            balance = 0
                            break
            break
        if choice.upper() == "TRAIL":
            say("Eh, who needs supplies? Maybe you're just built different.")
            break
        if choice.upper() == "MUSEUM" and wenttomuseum == True:
                say("...")
                say("I SAID, LET'S NOT GO BACK THERE AGAIN.")
        elif choice.upper() == "MUSEUM" and wenttomuseum == False:
            say("You don't know why, but you feel the pressing urge to go to the Mushroom Museum.")
            say("When you walk in, it doesn't look very interesting. An employee lights up when she sees you.")
            say('"PLEASE", she cries. "IT\'S BEEN YEARS SINCE I\'VE SEEN A CUSTOMER!"')
            say("She clings on to you tightly. You peel her off and run out the door. Let's not go back there again.")
            wenttomuseum = True
        else:
            print("Oops! Item not found.")
    say("So, the trail it is.")
    say("You take the first step, and the journey begins.")
    chapter = "Chapter: A World of Bugs"
    say("You take a step.")
    say("You take a step.")
    say("You take a step.")
    say("You take a step.")
    say("You take a step.")
    if weaponinventory == []:
        say("You see a cool stick, so you pick it up.")
        weaponinventory.append(STICK)
    say("You take a step.")
    say("You take a step.")
    say("You take a step.")
    say("You take a step.")
    say("You take a step.")
    say("You step on an anthill.")
    say("An ant storms out. He must be at least 5 feet tall.")
    say('"Hey, you destroyed my house!"')
    say('"Now, I shall destroy you!"')
    say("The ant charges!")
    say("The fight begins!")
    say('Hint: this is what is commonly referred to as a "tutorial".')
    while True: # Battle loop
        say("The ant runs at you!")
        if random.randint(1,2) == 1:
            say("He hits you!")
            take_damage(8)
        else: 
            say("He misses.")
        say("Your turn!")
        say("You can FIGHT or use an ITEM.")
        choice = input("[FIGHT / ITEM] ")
        if choice.upper() == "FIGHT":
            choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                say(", ".join(weapon["name"] for weapon in weaponinventory))
                continue

            weapon_found = False
            for weapon in weaponinventory:
                if choice.upper() == weapon["name"].upper():
                    damage = attack(weapon, "BUG")
                    weapon_found = True
                    AntHP = AntHP - damage
                    say("Ant has " + str(AntHP) + " points left.")
                    break
            if AntHP < 1:
                say("You killed the ant!")
                break
            if not weapon_found:
                say("Item not found. For a list of your weapons, see the list.")
        elif choice.upper() == "ITEM":
            choice = input('What item do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                item_names = [item["name"] if isinstance(item, dict) else item for item in generalinventory]
                say(", ".join(item_names))
                continue
            item_found = False
            for item in generalinventory:
                item_name = item["name"] if isinstance(item, dict) else item
                if choice.upper() == item_name.upper():
                    useitem(item)
                    item_found = True
                    break
            if not item_found:
                say("Item not found. For a list of your items, see the list.")
        else:
            say("Please choose FIGHT or ITEM.")
    say("The ant is dead.")
    choice = input("Do you loot its corpse? [Y / N] ")
    if choice.upper() == "Y":
        say("You find a picture of the ant with his family.")
        say("He has a wife and two young children.")
        say("There's something seriously wrong with you.")
    say("And so you continue on the great trail.")
    say("Along the way, you come across a friendly bumblebee.")
    say("The bee buzzes buzzily.")
    say('"Come partake in my village\'s Honey Festival", she tells you.')
    choice=input("Do you go? [Y / N] ")
    if choice.upper() == "Y":
        say("She smiles at you and slowly starts to fly towards the village.")
        say("You follow her through the brambles and the branches.")
    else: 
        say("Look, honestly, this is a whole thing with like the magical honeycomb and the stinger sword... can you please just go?")
        choice=input("Do you go? [Y / N] ")
        if choice.upper() == "Y":
            say("Great. You follow the bee through the woods.")
        else:
            say("...")
            say("Okay, give me a second to think of something.")
            say("...")
            say("...")
            say("...")
            say("Okay. The bee stings you and you pass out and you wake up in the village. Your health is set to 1.")
            hp = 1
    screencolor = (255, 190, 66)
    fillcolor = (237, 140, 0)
    say("The village is wonderful. Bumbles float lazily through the air.")
    say("Thatched huts and tall temples adorn the hillside.")
    say("This seems strange to you. Don't bees live in hives?")
    say("You ask your new bee friend. She seems offended.")
    say('"Not all bees live like that. We\'re country folk."')
    say("She names a few places you might want to check out. Where do you go?")
    while True:
        location = input("[SHOP / HOSPITAL / MUSEUM / CAVE / CASINO] ")
        if location.upper() == "CASINO":
            say("You walk into the casino. A few bees are playing cards at a table.")
            say("A bee dealer sits behind the counter. He looks at you and says, \"Welcome to the Beesino!\"")
            say("We call it the Beesino because we don't have a lot of imagination.")
            say("Also because you'll lose an unBEElievable amount of money here.")
            say("There are three games. Roulette, Blackjack, and Slots.")
            casino_game = input("Which game do you play? [ROULETTE / BLACKJACK / SLOTS / LEAVE] ").upper()
            if casino_game == "ROULETTE":
                wager = input_integer("You decide to play roulette. How much money do you wager? [Type it in the box.]", 1)
                if wager > balance:
                    say("You don't have enough money for that wager.")
                else:
                    say("You place your wager of " + str(wager) + " coins.")
                    say("The wheel spins...")
                    if random.randint(1, 2) == 1:
                        say("You win! You gain " + str(wager * 2) + " coins!")
                        balance += wager
                    else:
                        say("You lose! You lose " + str(wager) + " coins!")
                        balance -= wager
            if casino_game == "BLACKJACK":
                say("You decide to play blackjack.")
                if balance < 10:
                    say("You don't have enough money to play blackjack. The minimum bet is 10 coins.")
                else:
                    say("You place a bet of 10 coins.")
                    balance -= 10
                    blackjack = True
                    card = 0
                    total = 0
                    while blackjack:
                        card = random.randint(1,13)
                        if card == 1:
                            say("You draw an Ace! You can choose to count it as 1 or 11.")
                            choice=input("[1 / 11] ")
                            if choice == "1":
                                total += 1
                            else:
                                total += 11
                        if card == 2:
                            say("You draw a 2!")
                            total += 2
                        if card == 3:
                            say("You draw a 3!")
                            total += 3
                        if card == 4:
                            say("You draw a 4!")
                            total += 4
                        if card == 5:
                            say("You draw a 5!")
                            total += 5
                        if card == 6:
                            say("You draw a 6!")
                            total += 6
                        if card == 7:
                            say("You draw a 7!")
                            total += 7
                        if card == 8:
                            say("You draw an 8!")
                            total += 8
                        if card == 9:
                            say("You draw a 9!")
                            total += 9
                        if card == 10:
                            say("You draw a 10!")
                            total += 10
                        if card == 11: 
                            say("You draw a Jack!")
                            total += 10
                        if card == 12:
                            say("You draw a Queen!")
                            total += 10
                        if card == 13:
                            say("You draw a King!")
                            total += 10
                        say("Your total is " + str(total) + ".")
                        if total > 21:
                            say("You bust! The dealer wins.")
                            blackjack = False
                            continue
                        choice=input("Do you want to hit or stand? [HIT / STAND] ")
                        if choice.upper() == "HIT":
                            endturn = False
                        else:
                            endturn = True
                        if endturn:
                            dealer_total = random.randint(17, 23)
                            say("The dealer's total is " + str(dealer_total) + ".")
                            if dealer_total > 21:
                                say("The dealer busts! You win!")
                                balance += 20
                            elif dealer_total > total:
                                say("The dealer wins! You lose!")
                            elif dealer_total < total:
                                say("You win! You gain 20 coins!")
                                balance += 20
                            else:
                                say("It's a tie! You get your bet back.")
                                balance += 10
                            blackjack = False
            if casino_game == "SLOTS":
                say("You decide to play slots.")
                wager = input_integer("How much money do you wager? [Type it in the box.]", 1)
                if wager > balance:
                    say("You don't have enough money for that wager.")
                else:
                    say("You place your wager of " + str(wager) + " coins.")
                    balance -= wager
                    say("The slots spin...")
                    slot1 = random.randint(1, 3)
                    if slot1 == 1:
                        slot1 = "🍯"
                    elif slot1 == 2:
                        slot1 = "🍬"
                    elif slot1 == 3:
                        slot1 = "🐝"
                    slot2 = random.randint(1, 3)
                    if slot2 == 1:
                        slot2 = "🍯"
                    elif slot2 == 2:
                        slot2 = "🍬"
                    elif slot2 == 3:
                        slot2 = "🐝"
                    slot3 = random.randint(1, 3)
                    if slot3 == 1:
                        slot3 = "🍯"
                    elif slot3 == 2:
                        slot3 = "🍬"
                    elif slot3 == 3:
                        slot3 = "🐝"
                    say("The slots show: " + str(slot1) + " | " + str(slot2) + " | " + str(slot3))
                    if slot1 == slot2 == slot3:
                        say("You win! You gain " + str(wager * 5) + " coins!")
                        balance += wager * 5
                    else:
                        say("You lose! You lose " + str(wager) + " coins!")
            if casino_game == "LEAVE":
                say("You leave the casino.")
            elif casino_game not in {"ROULETTE", "BLACKJACK", "SLOTS"}:
                say("Please choose one of the listed games or LEAVE.")

        if location.upper() == "SHOP":
            say('The shop\'s sign reads "Jasper\'s Emporium".')
            say("A short bee snoozes behind the counter.")
            say("His glasses have fallen a little bit and they rest on his nose while he snores.")
            say("As you open the door, a little bell rings and he falls out of his seat.")
            say("A variety of items lay on the table. Glistening honeycomb, a stinger shard, and a little bee plushie.")
            choice=input("You can buy an item. Or leave. [HONEYCOMB / SHARD / PLUSH / LEAVE] ")
            if choice.upper() == "HONEYCOMB":
                if balance >= 20:
                    say("You buy the honeycomb for 20 coins. It will heal you during battle.")
                    balance -= 20
                    generalinventory.append(HONEYCOMB)
                else:
                    say("You don't have enough coins for the honeycomb.")
            elif choice.upper() == "SHARD":
                if balance >= 40:
                    say("You buy the shard for 40 coins.")
                    say('"It\'s a capable weapon," Jasper says.')
                    say('"But it\'s only a piece that fractured off the Great Stinger. Not sure where the whole thing is.')
                    balance -= 40
                    weaponinventory.append(SHARD)
                else:
                    say("You don't have enough coins for the shard.")
            elif choice.upper() == "PLUSH":
                if balance >= 15:
                    say("You buy the plush for 15 coins. It will provide a healing bonus. All healing items are more effective.")
                    balance -= 15
                    healingmultiplier += 0.1
                else:
                    say("You don't have enough coins for the plush.")
            elif choice.upper() == "LEAVE":
                say("You leave. Jasper goes back to sleep.")
            else:
                say("Jasper looks at you. He doesn't sell that.")
        elif location.upper() == "HOSPITAL":
            say("The hospital's doors slide open as you walk up.")
            say("A nurse sits behind the counter.")
            if hp < maxHP: 
                say("With a kiss on the cheek and a spoonful of honey, he heals you back to full health.")
                hp = maxHP

        elif location.upper() == "MUSEUM":
            say("A chipper preteen sits, his nose buried in a thick book about bee history.")
            say("You feel like if he sees you, he'll jump into an ardous monologue.")
            say("You have the chance to slip back out the door before he spots you.")
            choice=input("Do you try? [Y / N] ")
            if choice.upper() == "Y":
                say("You quietly open the door and run away.")
            else:
                say("You step forward. The bee child looks up and his face lights up.")
                say('"You\'re here to learn about bee history!?"')
                say("He tells you that you're the first person to come by in years.")
                say("Then, the story begins...")
                say("[3 hours later]")
                say('"And that\'s how the goblins got banished to the cave!"')
                say("After a few seconds, he unties you and gives you a gold star sticker.")
                say("Your bones creak as you stand up and stumble out the door.")

        elif location.upper() == "CAVE":
            say("The Cave of Goblins stands before you, ominously.")
            say("It's pretty spooky.")
            say("Your bee friend looks worried.")
            say('"Why would you ever want to go in there?"')
            say("Honestly, it doesn't matter what you tell her. You have to enter the cave anyway. Plot progression and all.")
            say("You walk inside. As you continue, it gets darker and darker, until you can't even see her face.")
            screencolor = (163, 167, 173)
            fillcolor = (79, 81, 87)
            say("You are well into the Cave of Goblins.")
            say("Faint buzzing noises echo off the stone walls...")
            break
        else:
            say('Your bee friend looks confused. "Sorry, could you say that again?"')
    say("You find a burnt out torch on the ground. You can try to light it.")
    choice=input("Do you try? [Y / N] ")
    if choice.upper() == "Y":
        say("You pick up the torch and attempt to spark it.")
        say("You're succesful! A lovely fire starts up and you can see the entire cave.")
        say("Burning Torch added to Weapons.")
        say("You take a look around. There are no goblins.")
        say("But you can feel an ominous presence...")
        say("A whoosh of air... the imposing aura of a soul...")
        say("No, not a soul. Souls... hundreds of them.")
        say("You know what's coming for you before you see them.")
        say("Five hundred moths barrel towards the light in your hand.")
        say("You can throw the torch away from you. You could try swiping at the moths. Or you could set yourself on fire.")
        choice=input("[THROW / ATTACK / WHYWOULDYOUDOTHIS]")
        if choice.upper() == "THROW":
            say("You throw the torch far away from you. The torch hits the floor and breaks.")
            say("Burning Torch removed from Weapons.")
            say("The light goes out and the moths stop in their tracks.")
            say("Then they collectively move in a single direction.")
        elif choice.upper() == "ATTACK":
            say("You swipe the torch at the moths.")
            say("Dozens burn to a crisp as flames roast their sides.")
            say("Enraged, the rest fly into your eyes.")
            say("They don't do much physical damage, but the psychological harm does 40 damage.")
            lose_health(40)
            say("Then, the moths run away. You hold on to the torch, now imbued with 50 souls.")
            weaponinventory.append(TORCH)
        else:
            say("You set yourself on fire for some reason.")
            say("Your flailing body manages to put itself out. You are left on 1 health point.")
            say("Unfortunately, a single hair on your head maintains a small flame. A lost moth zooms into you and does 1 damage.")
            take_damage(999)
            print("lmao dead")
            sys.exit()
    else:
        say("Since you're boring as hell, you move on without touching the torch.")
    say("You proceed into the cave.")
    say("A hazelnut tree sits in a clearing by a creek.")
    say("You could choose to eat the hazelnuts. Or you could pick them and hold on to them.")
    choice=input("What do you do? [EAT / STORE]")
    if choice.upper() == "EAT":
        say("Okay, fatty.")
        say("You eat 50 hazelnuts.")
        say("They make you feel pretty sick, but otherwise you're okay.")
    else: 
        say("You grab the hazelnuts and store them in your bag.")
        say("Hazelnuts have been added to your item inventory.")
        generalinventory.append("HAZELNUTS")
        say("Someone else might like them.")
    say("And you keep on moving.")
    say("Finally, you spot it.")
    say("In the Cave of Goblins, is a goblin.")
    say("It doesn't see you. You can attack it without it seeing you.")
    choice=input("Attack? [Y / N] ")
    if choice.upper() == "Y":
        attacked_goblin = True
    else: 
        attacked_goblin = False
    if attacked_goblin:
        say("You bean the goblin in the back of the head with a rock.")
        say("The goblin's body crumbles like a straw.")
        say("Looking a bit closer, it looks like a little child...")
        say("The child of someone...something bigger...")
        say("A shadow grows bigger across the cavern...")
        say("It's a pika!")
        say("(not pikachu, this is like a cave rat thing that eats grasses and moss and nuts and stuff)")
        say('"HEY!", the pika says. "YOU KILLED MY DAUGHTER!"')
        say("uh oh")
        say("battle time!")
    else:
        say("you leave the goblin alone.")
        say("after all, she didn't do anything to you.")
        say("The goblin's mother appreciates that. Unfortunately, she doesn't particularly appreciate you being in her house.")
    adding = ""
    attacked_goblin = True # this is intentional. at this stage, flipping attacked_goblin just starts the battle
    while attacked_goblin: # Battle loop
        say("Pika charges!")
        if random.randint(1,3) == 1:
            say("She hits you!")
            take_damage(25)
        else: 
            say("She misses.")
        say("Your turn!")
        say("You can FIGHT or use an ITEM.")
        choice = input("[FIGHT / ITEM] ")
        if choice.upper() == "FIGHT":
            choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                say(", ".join(weapon["name"] for weapon in weaponinventory))
                continue

            weapon_found = False
            for weapon in weaponinventory:
                if choice.upper() == weapon["name"].upper():
                    damage = attack(weapon, "N/A")
                    weapon_found = True
                    PikaHP = PikaHP - damage
                    say("Pika has " + str(PikaHP) + " points left.")
                    break
            if PikaHP < 1:
                say("You killed the pika!")
                attacked_goblin = False
                break
            if not weapon_found:
                say("Item not found. For a list of your weapons, see the list.")
        elif choice.upper() == "ITEM":
            choice = input('What item do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                item_names = [item["name"] if isinstance(item, dict) else item for item in generalinventory]
                say(", ".join(item_names))
                continue
            item_found = False
            for item in generalinventory:
                item_name = item["name"] if isinstance(item, dict) else item
                if choice.upper() == item_name.upper():
                    if item_name.upper() == "HAZELNUTS":
                        say("You offer the hazelnuts to the pika. She stops fighting to eat them.")
                        say("Out of her pockets (because yes she has pockets) fall some coins.")
                        say("Distracted by the nuts, she doesn't even notice you stealing the coins.")
                        balance = balance + 10
                        adding = ", you poisoned the nuts"
                        PikaHP = 0
                        attacked_goblin = False
                        generalinventory.remove(item)
                    else:
                        useitem(item)
                    item_found = True
                    break
            if PikaHP < 1:
                say("lmao pika dies" + adding)
                attacked_goblin = False
                break
            if not item_found:
                say("Item not found. For a list of your items, see the list.")
        else:
            say("Please choose FIGHT or ITEM.")
    say("Bye, bye pika!")
    say("And so, you move on.")
    say("Behind you, you hear a buzzing.")
    say("Quick time event!")
    say("Ready?")
    say("3...")
    say("2...")
    say("1...")
    say("0.75...")
    say("0.50...")
    say("0.40...")
    say("0.30...")
    say("0.20...")
    say("0.10...")
    say("0.09...")
    say("0.08...")
    say("0.07...")
    choice=input('Type "TURN AROUND!"')
    if choice == "TURN AROUND!":
        say("Huh... you reacted in time...")
        say("Uhh... +1 health for you")
        hp += 1
    elif choice == "TURN AROUND":
        say("You forgot the exclamation mark.")
        say("-1 health for you!")
        lose_health(1)
    else: 
        say("uhh.. okay")
        say("you missed the quick time event")
        say("somehow")
        say("you get beaned on the head. -10 health for you")
        lose_health(10)
    say("You turn around to see Sammy the Sentient Microwave buzzing.")
    say("Do you buy microwave popcorn from him?")
    choice=input("[Y / N] ")
    if choice.upper() == "Y":
        if balance >= 10:
            balance = balance - 10
            say("You buy the popcorn for 10 coins.")
            say("You open the bag to find a goblin.")
            say('"Thank you for freeing me", it says.')
            say("You are fulled with warmth and love.")
            maxHP = maxHP + 10
            hp = hp + 10
            say("Then it stings you on the nose. The fight has begun.")
        else: 
            say("You grab the popcorn and start eating.")
            say("Unfortunately, you cannot afford the popcorn.")
            say("For scamming him, Sammy socks you in the face.")
            say("-10 hp")
            lose_health(10)
    else: 
        say("You don't buy the popcorn.")
        say("Kind of a mistake on your part, but whatever.")
        say("Sammy goes away, dejected.")
        say("Behind him sits the giant wasp.")
        say("So... you have to fight it anyway.")
    boss_wasp = True
    while boss_wasp: # Battle loop
        say("Wasp flies at you!")
        if random.randint(1, max(1, math.floor(hp / 25))) == 1:
            say("She hits you!")
            take_damage(30)
        else: 
            say("She misses.")
        say("Your turn!")
        say("You can FIGHT or use an ITEM.")
        choice = input("[FIGHT / ITEM] ")
        if choice.upper() == "FIGHT":
            choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                say(", ".join(weapon["name"] for weapon in weaponinventory))
                continue

            weapon_found = False
            for weapon in weaponinventory:
                if choice.upper() == weapon["name"].upper():
                    damage = attack(weapon, "N/A")
                    weapon_found = True
                    waspHP = waspHP - damage
                    say("Wasp has " + str(waspHP) + " points left.")
                    break
            if waspHP < 1:
                say("You killed the wasp!")
                break
            if not weapon_found:
                say("Item not found. For a list of your weapons, see the list.")
        elif choice.upper() == "ITEM":
            choice = input('What item do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                item_names = [item["name"] if isinstance(item, dict) else item for item in generalinventory]
                say(", ".join(item_names))
                continue
            item_found = False
            for item in generalinventory:
                item_name = item["name"] if isinstance(item, dict) else item
                if choice.upper() == item_name.upper():
                    if item_name.upper() == "POPCORN":
                        say("Look, wasps LOVE popcorn. But this one in particular doesn't seem interested.")
                    else:
                        useitem(item)
                    item_found = True
                    break
            if waspHP < 1:
                say("The wasp is dead.")
                break
            if not item_found:
                say("Item not found. For a list of your items, see the list.")
        else:
            say("Please choose FIGHT or ITEM.")
    say("The wasp is gone.")
    choice = input("Do you loot the body? [Y / N] ")
    if choice.upper() == "Y":
        say("You plant your foot on the wasp and grab the stinger with both hands.")
        say("With a sickening snap, you rip the stinger off the wasp.")
        say("Great Stinger obtained.")
        say("It feels fragile... like it's made of glass.")
        say("It's sharp, but you can't help but worry that even a single hit will shatter the tip instantly.")
        weaponinventory.append(GREATSTINGER)
    else: 
        say("You decide to leave the body alone.")
        say("You find a few coins on the ground, though.")
        balance = balance + 20
    say("A light creeps through the rocks. You peek your head out.")
    screencolor = (34, 139, 34)
    fillcolor = (42, 86, 42)
    say("You can see the bee village far off in the distance. You must've walked for hours in that cave...")
    choice = input("Go back? [Y/N] ")
    if choice.upper() == "Y":
        say("You get up and start moving towards the village.")
    else:
        say("You decide to move on, down the trail.")
    say("Just then, you feel a strange presence behind you.")
    say("Grubby hands grab your neck and press hard on your artery.")
    say("Everything goes dark...")
    chapter = ""
    screencolor = (0, 0, 0)
    fillcolor = (0, 0, 0)
    say("")
    say("")
    say("You open your eyes.")
    say("It's dark... too dark.")
    say("Something pokes you in your face.")
    say("You can hear illegible speech.")
    say("Then, little clicking sounds.")
    say("After a moment, a flame appears. Small at first, but growing.")
    say("As it gets bigger, you observe your surroundings.")
    screencolor = (255, 154, 0)
    fillcolor = (255, 90, 0)
    say("The torch illuminates blue walls.")
    say("They look as if they're made of glass...")
    say("Water drips down from the ceiling and hits you on the nose.")
    say("You look up. The ceiling appears to be melting.")
    say("You're very thirsty, so you open your mouth.")
    say("A droplet hits you on the nose, then on the forehead, then finally one lands in your mouth.")
    say("It tastes vaguely ancient.")
    say("You look around for anyone else in the room, but you can't see anyone. The torch is being held up by a clump of moss.")
    choice = input("Eat the moss? [Y / N]")
    if choice.upper() == "Y":
        say("You pick up the moss and sink your teeth into it.")
        say("It screams a mossy scream.")
        say("Surprised, you throw it to the ground.")
        say('The moss looks at you, spits in your face, and says "Well, I TRIED being nice."')
        screencolor = (0, 0, 0)
        fillcolor = (0, 0, 0)
        say("It snuffs out the light.")
    else:
        say("You leave the moss alone.")
        say("It seems to appreciate that.")
        say("You sit with the moss in silence.")
        say("To pass the time, the moss gives you a sudoku book and you work on the puzzles.")
        screencolor = (0, 0, 0)
        fillcolor = (0, 0, 0)
        say("After an hour or so, the torch burns out. The moss apologizes and runs off to find a new one.")
        say("But hours pass, and your friend is nowhere to be found.")
    say("You are left in complete darkness.")
    say("All alone... no  moss... no friends... no food...")
    say("It's cold... so, so, cold...")
    say("Hours pass, then days, then weeks, months, and years.")
    say("You find inner peace through meditation.")
    say("You learn the secrets of kung fu.")
    say("You are finally strong enough to escape the prison.")
    say("You break all the bones in your fingers and tie them into yarn.")
    say("Then, you tightly knit them together into a fist.")
    say("With a deafening crack, you punch the wall of your prison.")
    say("The wall shatters. Water pours at an extreme rate.")
    say("It's extremely salty.")
    say("If you don't do something quickly, you'll drown.")
    choice=input("You could try to fit through the crack, meditate, or be patient.")
    while not escapedocean:
        choice=input("[FIT / MEDITATE / PATIENCE]" )
        if patience_completed:
            maxHP += 10
            hp = min(maxHP, hp + 10)
            patience_completed = False
            patience_timer = None
            say("You have mastered the art of patience. Your reward, as promised.")
            escapedocean = True
            break
        if choice.upper() != "PATIENCE" and patience_timer is not None and patience_timer.is_alive():
            patience_timer.cancel()
            patience_timer = None
        if choice.upper() == "MEDITATE" and meditationcounter < 2:
            say("You meditate. You gain 1 max health.")
            maxHP = maxHP + 1
            hp = hp + 1
            meditationcounter = meditationcounter + 1
        elif choice.upper() == "MEDITATE":
            say("You meditate. You lose 10 max health.")
            say("Shouldn't have been so greedy, friend.")
            maxHP = max(1, maxHP - 10)
            hp = max(1, min(hp - 10, maxHP))
        if choice.upper() == "PATIENCE":
            say("You use the power of patience.")
            say("Waiting...")
            say("Waiting...")
            say("Okay, here's the deal. I've set a timer in the code for 10 minutes. If you wait for 10 miuntes before you go to the next tab, you'll escape AND I'll get you +10 max health. How about that?")
            if patience_timer is None:
                say("Oops, forgot to set the timer. Now I've got it. 10 minutes, okay? Go!")
                patience_timer = threading.Timer(600, patience_reward)
                patience_timer.daemon = True
                patience_timer.start()
            else:
                say("Your patience timer is already running.")
        if choice.upper() == "FIT":
            screencolor = (0, 0, 200)
            fillcolor = (0, 0, 139)
            say("Your emaciated body easily fits through the cracks.")
            say("You are surrounded by water. Your eyes sting from the salt.")
            say("What do you do from here? You could try to swim up or down. You could also ask this nearby fish for directions.")
            choice=input("[SWIM UP / SWIM DOWN / ASK]")
            if choice.upper() == "SWIM UP":
                say("You swim and swim. The water gets lighter and you can see the Sun.")
                say("Unfortunately, your yarnball-hand isn't very good for the job, and you fail to reach the surface before you start drowning.")
                say("Luckily, a friendly whale eats you. You climb into the whale's blowhole, and it shoots you right out of the water.")
                say("You land on a wheel of cheese.")
                escapedocean = True
                break
            if choice.upper() == "SWIM DOWN" and sdcounter == 0:
                say("You swim down... for some reason.")
                say("You exhaust yourself.")
                say("Tired, you stop pushing and float back to where you started.")
                sdcounter = 1
            if choice.upper() == "SWIM DOWN" and sdcounter == 1:
                say("You swim down... for some reason.")
                say("You exhaust yourself even more.")
                say("Extremely tired, you stop pushing and float back to where you started.")
                sdcounter = 2
            if choice.upper() == "SWIM DOWN" and sdcounter == 2:
                say("You swim down... for some reason.")
                say("You exhaust yourself to the point of collapse.")
                say("You drown.")
                take_damage(999)
            if choice.upper() == "ASK":
                say("You ask the fish for directions.")
                say("It shows you a map and explains that you are in the middle of the ocean.")
                say("It then charges a consultation fee of 10 coins.")
                if balance >= 10:
                    balance = balance - 10
                else:
                    say("It responds to your lack of funds with violence and slaps you across the face.")
                    lose_health(1)
                    say('"Why do I even do this job", he says.')
                    say('"I should\'ve gone to law school."')
                    say("He swims away.")
        else:
            say("You do nothing as the water pours in. It's getting colder...")
    say("You look around.")
    say("You're on an iceberg in the middle of a vast ocean.")
    say("Little green goblins are running around.")
    say('A sign in the background says "Iceberg Town".')
if checkpoint == "GoblinsRCool":
    chapter = "Chapter: Iceberg Town"
    fillcolor = (13, 137, 214)
    screencolor = (79, 195, 247)
    say("It's the only sign you can read. Every other sign is written in some goblinish script.")
    say("Even though you can't read the signs, you can intuitively tell what each location is.")
    planecost = 100
    cat = True
    while True:
        choice=input("Where do you go? [BANK / ICE CREAM / CONVENIENCE STORE / GOBLIN PIT / AIRPORT]")
        destination = choice.upper()
        if destination == "AIRPORT":
            say("A tiny airport sits on a far iceberg.")
            say("You head over. A single-propeller airplane sits on the tarmac.")
            say("A ticket to leave costs " + str(planecost) + " coins.")
            choice = input("Leave? [Y / N]")
            if choice.upper() == "Y" and balance >= planecost:
                say("You decide to leave.")
                balance = balance - planecost
                say("You pay the ticket and board the plane.")
                accountbalance = math.floor(accountbalance * interest)
                break
            else:
                say("You decide to stay, for now.")
        if destination == "GOBLIN PIT":
            say("For SOME reason, you decide to venture into the goblin pit.")
            say("The rules are posted on a giant sign. You can find the same sentence written over and over in hundreds of languages.")
            say('You finally find your own. "Fight goblins, win money", it says.')
            say("You walk over to the entrance.")
            say("Apparently, you need to wager a bet as to how many goblins you can beat at the start.")
            say("If you beat all the goblins, you win the bet (and money).")
            say("You can also die.")
            choice=input("Do you want to fight? [Y / N] ")
            if choice.upper() == "Y":
                goblin_count = input_integer("How many goblins do you want to fight? ", 1)
                for goblin_number in range(goblin_count):
                    goblin_hp = 50
                    goblin_alive = True
                    say(f"Goblin {goblin_number + 1} approaches!")

                    while goblin_alive:
                        say("The goblin attacks!")
                        if random.randint(1, max(1, math.floor(hp / 25))) == 1:
                            say("It hits you!")
                            take_damage(10)
                        else:
                            say("It misses.")

                        say("Your turn!")
                        say("You can FIGHT or use an ITEM.")
                        choice = input("[FIGHT / ITEM] ")

                        if choice.upper() == "FIGHT":
                            choice = input(
                                'What weapon do you use? For a list of options, '
                                'type "LIST". [ITEMNAME / LIST] '
                            )
                            if choice.upper() == "LIST":
                                say(", ".join(
                                    weapon["name"] for weapon in weaponinventory
                                ))
                                continue

                            weapon_found = False
                            for weapon in weaponinventory:
                                if choice.upper() == weapon["name"].upper():
                                    damage = attack(weapon, "N/A")
                                    goblin_hp -= damage
                                    weapon_found = True
                                    say(
                                        "Goblin has " + str(goblin_hp) + " points left."
                                    )
                                    break
                            if goblin_hp < 1:
                                say("You killed the goblin!")
                                goblin_alive = False
                            elif not weapon_found:
                                say(
                                    "Item not found. For a list of your weapons, see the list."
                                )
                        elif choice.upper() == "ITEM":
                            choice = input(
                                'What item do you use? For a list of options, '
                                'type "LIST". [ITEMNAME / LIST] '
                            )
                            if choice.upper() == "LIST":
                                item_names = [
                                    item["name"] if isinstance(item, dict) else item
                                    for item in generalinventory
                                ]
                                say(", ".join(item_names))
                                continue

                            item_found = False
                            for item in generalinventory:
                                item_name = item["name"] if isinstance(item, dict) else item
                                if choice.upper() == item_name.upper():
                                    if item_name.upper() == "POPCORN":
                                        say(
                                            "This goblin doesn't seem interested in popcorn. Stop offering it popcorn."
                                        )
                                    else:
                                        useitem(item)
                                    item_found = True
                                    break

                            if not item_found:
                                say(
                                    "Item not found. For a list of your items, see the list."
                                )
                        else:
                            say("Please choose FIGHT or ITEM.")

                say("The goblins are gone.")
            else:
                say("Booooring...")
        if destination == "BANK":
            say("You walk into the bank.")
            say("The floors are a cold marble.")
            say("You walk up to a window and sit down. The banker looks at you funny.")
            say("Luckily, the bank has translators. They send another human over.")
            say('"Please help me", she says.')
            say('"I\'ve been trapped here for years."')
            say("Anyway, what do you do?")
            choice=input("[DEPOSIT / WITHDRAW / LOAN]")
            if choice.upper() == "DEPOSIT":
                say("You decide to put some money in the bank.")
                amount = input_integer("How much?")
                if amount > balance:
                    say("You don't have that much money.")
                else:
                    say("You put the money away. It will accumulate interest over time.")
                    say("The teller's hand shakes as she slides a pamphlet over to you.")
                    say("Apparently, there are goblin-run banks across the world. You'll be able to withdraw your money anywhere.")
                    accountbalance += amount
                    balance -= amount
            elif choice.upper() == "WITHDRAW":
                amount = input_integer("How much?")
                if amount > accountbalance:
                    say("You don't have that much money in your account!")
                else:
                    balance += amount
                    accountbalance -= amount
            elif choice.upper() == "LOAN":
                if loan > 0:
                    say("You already have an outstanding loan of " + str(loan) + " coins.")
                else:
                    say("The translator tells you that you can take any amount of money out.")
                    say("Unfortunately, you'll have to provide that money soon, plus " + str(round((interest - 1) * 100, 2)) + " percent interest.")
                    say('"Or they\'ll kill you", she whispers.')
                    amount = input_integer("How much do you take out?", 1)
                    loan = math.ceil(amount * interest)
                    balance += amount
                    say("You will owe " + str(loan) + " soon.")
            else:
                say("The teller just looks at you and quivers.")
        if destination == "ICE CREAM":
            say("Feeling cold, you decide to eat ice cream in the hopes that it will warm you up.")
            say("There's a little stand on a nearby iceberg, so you hop over.")
            say("A bored teenager scrolls on his phone. What flavor do you ask for? (each is 10 coins)")
            flavor = input("[CHOCOLATE / VANILLA / STRAWBERRY / MINT / PISTACHIO] ").upper()
            flavors = {"CHOCOLATE", "VANILLA", "STRAWBERRY", "MINT", "PISTACHIO"}
            if flavor not in flavors:
                say("They don't have that.")
            else:
                if balance < 10 and charity:
                    gift = 10 - balance
                    say("You can't afford ice cream, buddy.")
                    say("Look, I get it. Financial irresponsibility is sad.")
                    say("But maybe if you weren't eating so much avocado toast and watching Netflix, you'd be able to afford it.")
                    say("Here's " + str(gift) + " coins so you can afford one. I'm not heartless, after all.")
                    balance += gift
                    charity = False
                elif balance < 10:
                    say("Nice try, buddy.")
                    continue
                balance -= 10
            if flavor == "CHOCOLATE":
                say("mmmm yummy")
                say("based choice honestly. more max HP!")
                maxHP += 5
                hp = min(maxHP, hp + 5)
            elif flavor == "VANILLA":
                say("basic asl, but tasty choice")
                say("you're prob a finance bro, so i'll give you slightly more interest.")
                interest *= 1.05
            elif flavor == "STRAWBERRY":
                say("Aww... strawberry.")
                say("Only cute people pick strawberry ice cream.")
                say("ykw, might as well")
                say("full health for you!")
                hp = maxHP
            elif flavor == "MINT":
                say("Who the hell actually enjoys mint?")
                say("You're a psychopath, you know that?")
                say("You don't get any positive or negative effect.")
                say("Your mental illness is punishment enough.")
            elif flavor == "PISTACHIO":
                say("What are you, 42 years old?")
                say("You become a middle aged parent of 2. -10 health. Also you lose a bunch of money (kids are expensive)")
                lose_health(10)
                balance = math.floor(balance * (2 / 3))
        if destination == "CONVENIENCE STORE":
            say("You decide to take a trip down to the convenience store.")
            say("Neon lights illuminate the windows, and a bell rings when you push open the doors.")
            while True:
                say("The store has three sections. Which do you visit?")
                choice = input("[SNACKS / SLUSHIES / CAT]")
                if choice.upper() == "SNACKS":
                    say("You move over to the snack section.")
                    say("Mmmmmm... yummy!")
                    say("Lots of fun choices. Chips, gummies, jerky.")
                    say("You can have one for 20 coins.")
                    snack = input("[CHIPS / GUMMIES / JERKY] ").upper()
                    snacks = {"CHIPS": CHIPS, "GUMMIES": GUMMIES, "JERKY": JERKY}
                    if snack not in snacks:
                        say("The store doesn't carry that.")
                    elif balance < 20:
                        say("You can't afford anything. Economy, inflation, whatever.")
                    else:
                        balance -= 20
                        generalinventory.append(snacks[snack])
                        say("You buy the " + snack.lower() + ". Might be useful in battle.")
                        say("You move on.")
                elif choice.upper() == "SLUSHIES":
                    say("You visit the slushy machines.")
                    say("A row of machines sits in front of you.")
                    say("Cola, Cherry, and Blue Raspberry. Which do you choose?")
                    choice = input("[COLA / CHERRY / BLUERASP]")
                    if choice.upper() == "COLA" and balance >= 15:
                        balance -= 15
                        say("It's sweet.")
                        say("SOMETHING good happens. Can't tell you what tho, would ruin the fun.")
                        resistancemultiplier = max(0, resistancemultiplier - 0.05)
                    elif choice.upper() == "CHERRY" and balance >= 15:
                        balance -= 15
                        say("It's sour.")
                        say("SOMETHING good happens. Can't tell you what tho, would ruin the fun.")
                        damagemultiplier = damagemultiplier + 0.05
                    elif choice.upper() == "BLUERASP" and balance >= 15:
                        balance -= 15
                        say("It's blue.")
                        say("SOMETHING good happens. Can't tell you what tho, would ruin the fun.")
                        healingmultiplier = healingmultiplier + 0.05
                    elif choice.upper() in {"COLA", "CHERRY", "BLUERASP"}:
                        say("Guess you can't afford anything.")
                    else:
                        say("That's... not a flavor.")
                elif choice.upper() == "CAT" and cat:
                    say("On the shelf sleeps a cute little bodega cat.")
                    say("You grab it by the tail, crush its neck, and eat it whole.")
                    say("+ 2 health!")
                    cat = False
                    hp = min((hp + 2), maxHP)
                elif choice.upper() == "CAT" and not cat:
                    say("You try to eat the cat again. But there is no cat. So you just throw up.")
                    say("- 30 health.")
                    lose_health(30)
                else:
                    say("You leave.")
                    break
        if destination not in {"BANK", "ICE CREAM", "CONVENIENCE STORE", "GOBLIN PIT", "AIRPORT"}:
            say("I'm sorry... where do you want to go?")
    say("The propeller roars to life.")
    say("With a sputter and a spit, the airplane begins to taxi down the runway.")
    say("The iceberg civilization becomes smaller and smaller through your plastic window.")
    say("Huh, there's an ocean liner close by. Maybe you could've caught a ride on that.")
    chapter = ""
    say("A flight attendant asks you whether you'd like some peanuts.")
    choice = input("Do you take them? [Y / N] ")
    if choice.upper() == "Y":
        say("You take the peanuts and eat some.")
        say("You are allergic to peanuts.")
        say("You die.")
    else:
        say("You decline.")
        say("Unfortunately, you haven't eaten anything recently.")
        say("You starve to death.")
    screencolor = (0, 0, 0)
    fillcolor = (0, 0, 0)
    say("")
    say("")
    screencolor = (152, 251, 152)
    fillcolor = (79, 121, 66)
    say("Just kidding!")
    say("Hey... why is everything so green?")
    say("And why is the engine on fire?")
    say("And why is the plane losing altitude?")
    say("uh oh")
    choice = input("The plane is plummeting. Do you jump out of the emergency exit? You have no parachute. [Y / N] ")
    if choice.upper() == "Y":
        say("Fortune favors the bold...")
        say("You open the door and instantly get sucked out.")
    else:
        say("You stay stuck in your seat.")
        say("A ")
    say("You plummet through the air.")
    say("Some sort of green island appears below you.")
    say("You have practically no shot at survival.")
    choice = input("Who do you pray to? [Type name of a deity]")
    if choice.upper() == "GOD":
        say("You pray to God. Unfortunately, you are a Catholic. And God only accepts prayers from Anglicans.")
    elif choice.upper() == "ALLAH":
            say("You pray to Allah. Unfortunately, you are a Sunni. And Allah only accepts prayers from Shi'a Muslims.")
    elif choice.upper() == "YAHWEH":
            say("You pray to Yahweh. Unfortunately, you he doesn't care. You ate bread on Passover (it was midnight in Jerusalem).")
    elif choice.upper() == "BRAHMA":
            say("You pray to Brahma. Unfortunately, he's a little busy. 400 million other prayers to answer.")
    elif choice.upper() == "BUDDHA":
            say("You pray to the Buddha. Unfortunately, Buddhism is non-theistic. So it doesn't work.")
    elif choice.upper() == "ZEUS":
            say("You pray to God. Unfortunately, he strikes the plane with a lightning bolt. You start going down faster.")
    else:
        say("You pray to " + str(choice) + ". Nothing much happens.")
    say("You close your eyes as you get closer to the ground.")
    say('You land on the ground with a sickening "BOING".')
    say("You open your eyes, puzzled.")
    say("You're sinking into green goo.")
    say("Slimey slime.")
    say("You thank " + str(choice) + ". You managed to land on the best possible island. An island full of squishy slime!")
    say("The slime begins to move...")
    say("It's not just squishy slime- it's sentient slime!")
    say("You try swimming away, but the slime is impossible to move through.")
    say("Your high school physics professor shows up.")
    say('"Slime is a non-Newtonian fluid", he says.')
    say('"This allows it to have both the properties of a solid and a liquid."')
    say("The professor stops moving and sinks deep down into the slime.")
    say("You decide to follow his lead, and you stop squirming.")
    say("Holding your breath, your head dips below the surface of the goo.")
    say("You are now submerged in the slime.")
    say("Interestingly, you find yourself breathing through your nose.")
    say("The professor explains this is due to the slime's high oxygen content.")
    say("At least, you think he says that. It's hard to hear him through the slime.")
    say("Suddenly, you feel your feet being exposed to air. You look down and see the slime is thinning.")
    say("You fall through the slime and land in a pool of water.")
    say("This must be the mythical Slime Lake!")
if checkpoint == "SlimeTime":
    screencolor = (132, 205, 142)
    fillcolor = (119, 161, 106)
    chapter = "Chapter: Slime Lake"
    say("You look around. The lake is surrounded by cute little carnivorous blobs of slime.")
    say("They look at you hungrily with their big, round eyes.")
    say("You can see small islands scattered across the lake. You certainly don't want to be eaten by the slime, so you decide to swim to one of the islands.")
    while True:
        choice=input("Which do you go to? [COCONUT ISLAND / BANK / WIZARD TOWER" + adding + "]")
        destination = choice.upper()
        if destination == "COCONUT ISLAND":
            say("You swim over to an island full of coconuts.")
            say("It feels... disingenuous...")
            say("On the coconut island lives a coconut man.")
            say("Come eat my coconuts, he says. 1 coin each.")
            choice=input("Do you eat a coconut? [Y / N] ")
            if choice.upper() == "Y" and balance > 0:
                say("You pay a coin and grab a coconut.")
                balance = balance - 1
                say("Something happens...")
                say("You feel stronger.")
                diceroll = random.randint(1,3)
                if diceroll == 1:
                    damagemultiplier = damagemultiplier + 0.005
                if diceroll == 2:
                    resistancemultiplier = max(0, resistancemultiplier - 0.005)
                if diceroll == 3:
                    healingmultiplier = healingmultiplier + 0.005
            else:
                say("You decide not to eat a coconut.")
        if destination == "BANK":
            say("You go to the bank.")
            if loan > 0:
                say("Armed men are waiting for you at the door.")
                say('"Hand over the money", they say.')
                if 1 == 1:
                    choice=input("Pay the money? (" + str(loan) + " coins) [Y / N]")
                    if choice.upper() == "N" or balance < loan:
                        say("You decline to pay. The loan collectors glare at you and draw their guns.")
                        say("Honestly, I don't know how you're going to survive this. You can't say I didn't warn you.")
                        collectors_alive = True
                        while collectors_alive:
                            say("The collectors attack!")
                            say("They shoot you!")
                            take_damage(30)
                            say("Your turn!")
                            say("You can FIGHT or use an ITEM.")
                            choice = input("[FIGHT / ITEM] ")
                            if choice.upper() == "FIGHT":
                                choice = input(
                                    'What weapon do you use? For a list of options, '
                                    'type "LIST". [ITEMNAME / LIST] '
                                )
                                if choice.upper() == "LIST":
                                    say(", ".join(
                                        weapon["name"] for weapon in weaponinventory
                                    ))
                                    continue
                                weapon_found = False
                                for weapon in weaponinventory:
                                    if choice.upper() == weapon["name"].upper():
                                        damage = attack(weapon, "N/A")
                                        collector_hp -= damage
                                        weapon_found = True
                                        say(
                                            "Collectors have " + str(collector_hp) + " points left."
                                        )
                                        break

                                if collector_hp < 1:
                                    say("You killed them! Somehow...")
                                    collectors_alive = False
                                elif not weapon_found:
                                    say(
                                        "Item not found. For a list of your weapons, see the list."
                                    )
                            elif choice.upper() == "ITEM":
                                choice = input(
                                    'What item do you use? For a list of options, '
                                    'type "LIST". [ITEMNAME / LIST] '
                                )
                                if choice.upper() == "LIST":
                                    item_names = [
                                        item["name"] if isinstance(item, dict) else item
                                        for item in generalinventory
                                    ]
                                    say(", ".join(item_names))
                                    continue

                                item_found = False
                                for item in generalinventory:
                                    item_name = item["name"] if isinstance(item, dict) else item
                                    if choice.upper() == item_name.upper():
                                        if item_name.upper() == "POPCORN":
                                            say(
                                                "They don't want popcorn. They want your money!"
                                            )
                                        else:
                                            useitem(item)
                                        item_found = True
                                        break

                                if not item_found:
                                    say(
                                        "Item not found. For a list of your items, see the list."
                                    )
                            else:
                                say("Please choose FIGHT or ITEM.")
                    else: 
                        say("You pay off the loan.")
                        balance = balance - loan
                        loan = 0
            say("You walk up to a slime teller.")
            say("It slides a sheet of paper across to you. Your account information.")
            say("You have " + str(accountbalance) + " coins in your account. Your current interest rate is " + str(round((interest - 1) * 100, 2)) + "%.")
            choice=input("What do you do? [WITHDRAW / DEPOSIT]")
            if choice.upper() == "DEPOSIT":
                say("You decide to put some money in the bank.")
                amount = input_integer("How much?")
                if amount > balance:
                    say("You don't have that much money.")
                else:
                    say("You put the money away. It will accumulate interest over time.")
                    accountbalance += amount
                    balance -= amount
            elif choice.upper() == "WITHDRAW":
                amount = input_integer("How much?")
                if amount > accountbalance:
                    say("You don't have that much money in your account!")
                else:
                    balance += amount
                    accountbalance -= amount
            else:
                say("Please choose WITHDRAW or DEPOSIT.")
        if destination == "WIZARD TOWER":
            say("You climb the wizard tower. ")
            say("An old, robed, and long-bearded man sits at the top of the tower, stirring something green in a cauldron.")
            say("You decide to ask him about magic.")
            say('"Oh, I don\'t know anything about magic", he says.')
            say('"Ask my wife, she\'s the real expert here. This cauldron is full of split pea soup."')
            say("You take a sip. It is DELICIOUS.")
            say("It heals you fully.")
            hp = maxHP
            say("He points you to her study and you walk in. She's stirring a cauldron of green goop.")
            say("She says hello and explains to you her system of slime magic.")
            say("When you kill slimes, you can collect them and put them in a jar.")
            say("Then you can use slime to cast magic spells.")
            say("She gives you a jar to store the slime.")
            say('"This is an old one of mine. Holds quite a bit in there."')
            say('"Be careful out there", she says. There are lots of dangerous creatures that want to eat you.')
            say('"I\'ve been trapped here for years", she claims. The only way out is covered by a giant slime, larger than a cloud.')
            say('"Now, because this is a game, you\'re going to have to beat the slime to move on to the next chapter. My advice is to use magic on him."')
            say('"Off you go!"')
            adding = " / MAINLAND"
        if destination == "MAINLAND":
            if adding != " / MAINLAND":
                say("uhhh... how?????")
            else:
                break
        else:
            say("You keep on treading water.")
    accountbalance = accountbalance * interest
    say("You head out to the mainland.")
    say("Slimes crowd near the shore, just waiting to have a bite.")
    say("Luckily, it looks like they can't swim.")
    say("You step onto the beach and begin to attack slimes!")
    slimes = 10
    burn = 0
    for n in range(1, slimes + 1):
        say("There are " + str(slimes - n + 1) + " slimes. They form a neat line and are waiting to eat you. ")
        say("There are so many slimes that you have no way to use items. You'll have to fight your way out!")
        slimeHP = 30
        if 0 < n < 4:
            say("This slime is a watery one. It doesn't really like you.")
            slime_type = "regular"
        elif 3 < n < 8:
            say("This slime is on fire! It really loves you. In fact, it wants to give you hugs!")
            slime_type = "fire"
        elif 7 < n < 11:
            say("This slime is charged with electricity! It looks pretty dangerous.")
            slime_type = "electric"

        while slimeHP > 0:
            say("Since slimes are kind of stupid, you attack first.")
            choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                say(", ".join(weapon["name"] for weapon in weaponinventory))
                continue

            weapon_found = False
            for weapon in weaponinventory:
                if choice.upper() == weapon["name"].upper():
                    damage = attack(weapon, "SLIME")
                    slimeHP -= damage
                    weapon_found = True
                    say("Slime has " + str(max(0, slimeHP)) + " points left.")
                    break

            if slimeHP <= 0:
                say("You killed the slime!")
                break
            if not weapon_found:
                say("Item not found. For a list of your weapons, see the list.")

            if random.randint(1, 2) == 1:
                say("It hits you!")
                if slime_type == "regular":
                    take_damage(8)
                elif slime_type == "fire":
                    burn += 2
                    take_damage(4)
                else:
                    take_damage(15)
            else:
                say("It misses.")

            if burn > 0:
                say("You're on fire!")
                take_damage(3)
                burn -= 1
    say("The slimes are dead. From their corpses, you collect 15 slimeballs.")
    slimeballs = 15
    choice = input("Eat one? [Y / N] ")
    if choice.upper() == "Y":
        say("You eat one.")
        say("The mucus coats your throat and you feel sick.")
        slimeballs = 14
    else:
        say("You refrain from eating any balls.")
        say("You find some coconut milk in the sand, though. It's healing.")
        hp = maxHP
    say("You can now use magic in fights!")
    say("But you don't know any spells. Luckily, the witch gave you a map of Slime Lake.")
    say("You can go into the Sky Dimension and pick up a Lightning Spellbook, which will teach you the Lightning Spell.")
    say("You can go into the Underworld and pick up a Fireblast Spellbook, which will teach you the Fireblast Spell.")
    say("You can go into the Water Realm and pick up a Scary Rain Spellbook, which will teach you the Scary Rain Spell.")
    choice = input("Where do you go? [SKY / UNDERWORLD / WATER] ")
    while choice.upper() not in {"SKY", "UNDERWORLD", "WATER"}:
        say("Please choose SKY, UNDERWORLD, or WATER.")
        choice = input("Where do you go? [SKY / UNDERWORLD / WATER] ")
    if choice.upper() == "SKY":
        say("You decide to go to the Sky Dimension.")
        say("With a skip, jump, and hop, you launch yourself above the clouds.")
        say("This place is full of lightning slimes.")
        say("They glare at you angrily as you hop from cloud to cloud.")
        say("Angrily, they clump together and form one giant slime.")
        slimes = 1
        for n in range(1, slimes + 1):
            say("The giant slime looms overhead. ")
            say("All your things fell out of your pockets when you jumped up. You have no way to use items. You'll have to fight your way out!")
            slimeHP = 50
            while slimeHP > 0:
                say("Since slimes are kind of stupid, you attack first.")
                choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
                if choice.upper() == "LIST":
                    say(", ".join(weapon["name"] for weapon in weaponinventory))
                    continue
                weapon_found = False
                for weapon in weaponinventory:
                    if choice.upper() == weapon["name"].upper():
                        damage = attack(weapon, "SLIME")
                        slimeHP -= damage
                        weapon_found = True
                        say("Slime has " + str(max(0, slimeHP)) + " points left.")
                        break
        
                if slimeHP <= 0:
                    say("You killed the slime!")
                    break
                if not weapon_found:
                    say("Item not found. For a list of your weapons, see the list.")
                if random.randint(1, 2) == 1:
                    say("It hits you!")
                    take_damage(24)
                else:
                    say("It misses.")
        say("The clump falls apart. Dead slimes litter the ground. From their corpses, you collect 30 slimeballs.")
        slimeballs += 30
        say("You move on to the sky castle.")
        say("In the sky castle, you find a book of spells.")
        say("You flip it open to a random page and learn the Lightning spell.")
        spell = "LIGHTNING"
    elif choice.upper() == "UNDERWORLD":
        say("You decide to the Underworld.")
        say("Sounds like a pretty chill place. And a hot tourist destination.")
        say("You grab a spoon and start digging.")
        say("A short while later, you've made it.")
        say("You land on top of a giant fire slime.")
        say("To find the spellbook, you probably need to defeat it.")
        slimes = 1
        burn = 0
        for n in range(1, slimes + 1):
            say("The king slime gets hotter. ")
            say("All of your items melted, so you can't use them. You'll have to fight your way out!")
            slime_type = "fire"
            slimeHP = 60
            while slimeHP > 0:
                say("Since slimes are kind of stupid, you attack first.")
                choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
                if choice.upper() == "LIST":
                    say(", ".join(weapon["name"] for weapon in weaponinventory))
                    continue
                weapon_found = False
                for weapon in weaponinventory:
                    if choice.upper() == weapon["name"].upper():
                        damage = attack(weapon, "SLIME")
                        slimeHP -= damage
                        weapon_found = True
                        say("Slime has " + str(max(0, slimeHP)) + " points left.")
                        break
                if slimeHP <= 0:
                    say("You killed the slime!")
                    break
                if not weapon_found:
                    say("Item not found. For a list of your weapons, see the list.")
                if random.randint(1, 2) == 1:
                    say("It hits you!")
                    if slime_type == "regular":
                        take_damage(8)
                    elif slime_type == "fire":
                        burn += 2
                        take_damage(17)
                    else:
                        take_damage(15)
                else:
                    say("It misses.")

                if burn > 0:
                    say("You're on fire!")
                    take_damage(3)
                    burn -= 1
        say("The slime burns to a crisp. You collect 15 slightly singed slimeballs.")
        slimeballs += 15
        say("You find the book next to you.")
        say("Oh. Looks like you didn't need to kill him after all.")
        say("You learn the Fireblast Spell!")
        spell = "FIREBLAST"
    else:
        say("You decide to go to the Water Realm.")
        say("You do a perfect swan dive into the lake and swim down, down, down.")
        say("There appears a little man.")
        say('"I am the king of the lake", he says.')
        choice = input("Kill him? [Y / N] ")
        say("You grab the king and twist his head off.")
        say("It's easy, like opening a jar of pickles.")
        if choice.upper() == "Y":
            say("Why would YOU do this?")
        else:
            say("Oops... you didn't mean to do that, did you?")
        say("YOUR actions draw the attention of the 3 royal guards.")
        say("The slimes charge!")
        say("Well... honestly... they can't REALLY charge.")
        say("Because they're slimes in water. It's a miracle they haven't dissolved yet.")
        say("They're pretty easy to defeat. If you lose to these guys, you REALLY suck at this.")
        slimes = 3
        for n in range(1, slimes + 1):
            say("There are " + str(slimes - n + 1) + " slimes. They form a neat line and are waiting to eat you. ")
            say("All your things floated away when you went underwater. You have no way to use items. You'll have to fight your way out!")
            slimeHP = 30
            slime_type = "regular"
            while slimeHP > 0:
                say("Since slimes are kind of stupid, you attack first.")
                choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
                if choice.upper() == "LIST":
                    say(", ".join(weapon["name"] for weapon in weaponinventory))
                    continue

                weapon_found = False
                for weapon in weaponinventory:
                    if choice.upper() == weapon["name"].upper():
                        damage = attack(weapon, "SLIME")
                        slimeHP -= damage
                        weapon_found = True
                        say("Slime has " + str(max(0, slimeHP)) + " points left.")
                        break

                if slimeHP <= 0:
                    say("You killed the slime!")
                    break
                if not weapon_found:
                    say("Item not found. For a list of your weapons, see the list.")

                if random.randint(1, 2) == 1:
                    say("It hits you!")
                    if slime_type == "regular":
                        take_damage(12)
                else:
                    say("It misses.")
        say("The guards are dead. From their corpses, you collect 30 slimeballs.")
        slimeballs = slimeballs + 30
        say("You enter the sea castle and make your way to the top of the tower.")
        say('There\'s a leather-bound book at the top. The title is "Casting Spells For Dummies".')
        say("That's not nice...")
        say('Anyway, you open the book to a random page and learn how to do the "Scary Rain" spell.')
        say("Doesn't seem to be too powerful... but it'll probably be FINE.")
        spell = "RAIN"
        say("You learn the spell!")
    say("Equipped with your spell, you move on to fight the giant slime.")
    while giantslimeHP > 0:
        say("The slime slimes!")
        say("He hits you!")
        say("It's so giant, that thing can't miss!")
        take_damage(17)
        say("Your turn!")
        say("You can FIGHT or use MAGIC.")
        choice = input("[FIGHT / MAGIC] ")
        if choice.upper() == "FIGHT":
            choice = input('What weapon do you use? For a list of options, type "LIST". [ITEMNAME / LIST] ')
            if choice.upper() == "LIST":
                say(", ".join(weapon["name"] for weapon in weaponinventory))
                continue
    
            weapon_found = False
            for weapon in weaponinventory:
                if choice.upper() == weapon["name"].upper():
                    damage = attack(weapon, "SLIME")
                    weapon_found = True
                    giantslimeHP -= damage
                    say("The giant slime has " + str(max(0, giantslimeHP)) + " points left.")
                    break
            if giantslimeHP <= 0:
                say("You defeated the giant slime!")
            if not weapon_found:
                say("Weapon not found. For a list of your weapons, see the list.")
        elif choice.upper() == "MAGIC":
            if spell not in SPELLS:
                say("You don't know a spell to use!")
                continue
            spell_data = SPELLS[spell]
            choice = input(
                'What spell do you use? Type "LIST" to check it. ['
                + spell_data["name"] + " / LIST] "
            )
            if choice.upper() == "LIST":
                say(spell_data["name"] + " (" + str(spell_data["cost"]) + " slimeballs; you have " + str(slimeballs) + ")")
                continue
            if choice.upper() != spell_data["name"].upper() and choice.upper() != spell:
                say("You haven't learned that spell. Type LIST to see your spell.")
                continue
            if slimeballs < spell_data["cost"]:
                say("You don't have enough slimeballs to cast " + spell_data["name"] + ".")
                continue
            slimeballs -= spell_data["cost"]
            giantslimeHP -= spell_data["damage"]
            say(spell_data["name"] + " hits the giant slime for " + str(spell_data["damage"]) + " damage!")
            say("You have " + str(slimeballs) + " slimeballs left.")
            say("The giant slime has " + str(max(0, giantslimeHP)) + " points left.")
            if giantslimeHP <= 0:
                say("You defeated the giant slime!")
        else:
            say("Please choose FIGHT or MAGIC.")
    say("The giant slime collapses. The trail is clear!")
    say("You follow the trail.")
    say("You walk. And walk. It feels like forever.")
    say("Hours... days... weeks...")
    say("You walk during the day and sleep during the night.")
    say("Eventually.... you see something in the distance... is that?")
    say("")
    screencolor = (0, 0, 0)
    fillcolor = (0, 0, 0)
    say("")
    screencolor = (34, 139, 34)
    fillcolor = (42, 86, 42)
    say("")
    name1 = input("What is your name? (use keyboard) ")
    if name == name1:
        say("Hello, " + name + ". Welcome to Mushroom Town!")
    else:
        say("")
        finallycolor = (0, 0, 0)
        screencolor = (0, 0, 0)
        textcolor = (255, 0, 0)
        say("are you lying to me?")
        say("are you lying to me?")
        say("are you lying to me?") 
        textcolor = (255, 255, 255)
        screencolor = (34, 139, 34)
        fillcolor = (42, 86, 42)
    say("Mushroom Town is the last speckle of civilization before the trail begins... I assume you're here for that?")
    say("In any case, you'll want to gear up before you tackle the trail... feel free to visit me in my shop!")
    choice = input("Where would you like to go? [SHOP/TRAIL/MUSEUM/] ")
    say("But you fail.")
    say("There's too much fungus.")
    say("Too much fungus... too much fungus...")
    say("Mushroom Town is covered in spores and mycelium and connections and fibers and growths.")
    say("The townspeople lay dead, covered in their own blood.") #woaahhhh, is this too dark for HackClub Terra 🤔
    say("The infection has spread, and it will keep spreading.")
    say("Your high school professor shows up.")
    say('"This is a hemorrhagic fungus", he says.')
    say('"It first enters the body when spores are inhaled. It recodes the cells in the stomach lining to quickly divide and produce more spores."')
    say('"And then it makes you vomit blood and infect everyone else."')
    say("The professor dissapears into a fine cloud of dust.")
    choice = input("Inhale the dust? [Y / N]")
    if choice.upper() == "Y":
        say("vro it's ebola dust 💔")
        sys.exit()
    else:
        say("You avoid the ebola dust, like a normal person.")
    say("You carefully look around.")
    say("You're going to have to remove this blight... one way or another.")
    say("You're going to have to start a fire.")
    say("Or something, idk")

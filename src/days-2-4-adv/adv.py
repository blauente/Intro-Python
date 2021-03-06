import random
from room import Room
from player import Player
from item import Item, Treasure, Lightsource, Food
from monster import Monster

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                    "   North of you, the cave mount beckons",
                    [Treasure("golden cup", "a shimmering goblet studded with jewels", 100, 10)], False),

    'foyer':    Room("Foyer", 
    """    Dim light filters in from the south. 
    Dusty passages run north and east.""",
                    [Lightsource("lamp", "looks like it has a genie inside", 10)], True),

    'overlook': Room("Grand Overlook", 
    """    A steep cliff appears before you, 
    falling into the darkness. Ahead to the north, 
    a light flickers in the distance, but there 
    is no way across the chasm.""",
                    [Item("long sword", "a sharp, heavy blade", 75),
                    Item("rusty sword", "a dull and dingy blade", 30),
                    Food("bread", "a crusty loaf", 5, 20)], False),

    'narrow':   Room("Narrow Passage", 
    """    The narrow passage bends here from west
    to north. The smell of gold permeates the air.""",
                    [Food("apple", "a shiny red orb", 5, 10)], False),

    'treasure': Room("Treasure Chamber", 
    """    You've found the long-lost treasure
    chamber! Sadly, it has already been completely 
    emptied by earlier adventurers. There is a 
    bookshelf along the north wall. The only exposed 
    exit is to the south. """,
                    [Item("leather-bound book", "a mysterious tome with missing pages", 5)], True),
    
    'hidden': Room("Hidden Room", 
    """    You've found a tiny, musty, hidden room 
    behind a bookshelf. Exits are to the west 
    and south. A bright, revolving light appears west.""",
                    [Treasure("pile of silver coins", "maybe they're real silver", 100, 5), 
                    Lightsource("lit candle", "a burning flame to help in the dark night", 20)], False),
    
    'lighthouse': Room("Glimmering Lighthouse", 
    """    A tall, white-and-red lighthouse 
    stands towering above you. The door is 
    locked. Paths lead east, and west to a beach.""", 
                    [Item("broken mirror", "sharp edges and big cracks", 15),
                    Treasure("shiny ruby", "a deep red precious stone", 200, 5)], True),
    
    'beach': Room("Sandy Beach", 
    """    A broad sandy beach lies before you. 
    Sea shells are scattered around. 
    The ocean looks cold and uninviting. 
    the only exit is east.""", 
                    [Item("conch shell", "a pale shell with an opening", 15),
                    Food("mac and cheese", "cheesy pasta", 5, 50)], False)
}

roomList = ['outside', 'foyer', 'overlook', 'narrow', 'treasure', 'hidden', 'lighthouse', 'beach']
directions = ['n_to', 's_to', 'e_to', 'w_to']
# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

room['treasure'].n_to = room['hidden']
room['hidden'].s_to = room['treasure']
room['hidden'].w_to = room['lighthouse']
room['lighthouse'].e_to = room['hidden']
room['lighthouse'].w_to = room['beach']
room['beach'].e_to = room['lighthouse']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.


# initialize player
playerName = input("""================================================
What is your name? """)
player = Player(playerName, room['outside'], [Item("iron chestplate", "a durable armor piece", 20)])

# initialize monsters
monsters = [Monster("vampire", "a pale being\n with long fangs and a black cape. He sparkles.", room[f"{random.choice(roomList)}"], [Item("skating magazine", "with photos of gnarly tricks", 5)], 15),
            Monster("mutant squirrel", "a \nferocious, slobbering bundle of radioactive fur.", room[f"{random.choice(roomList)}"], [Item("acorns", "some tree seeds", 5)], 10)]


suppressRoomPrint = False
# Input loop
while True:
    if player.health <= 0:
        print("\nYOU ARE DEAD!\n")
        break
    if len(monsters) == 0:
        print("\nCongratulations, you won!\n")
        break

    def printNoMove():
        print('\nSorry, %s, you cannot move in that direction.' % player.name)
        print()

    def treasureOnTake(treasure):
        if not treasure.takenAlready:
            player.increaseScore(treasure.value)

    def printMonsters():
        for monster in monsters:
            if monster.monsterCurrentRoom == player.currentRoom:
                print(f"\nThere is a {monster.name} in the room. It appears to be {monster.description}\n")
    
    def moveMonsters():
        for monster in monsters:
            randMove = random.choice(directions)
            if hasattr(monster.monsterCurrentRoom, randMove):
                monster.monsterCurrentRoom = getattr(monster.monsterCurrentRoom, randMove)

    def monsterAttacks(monster):
        player.health -= monster.attack
        print(f"You have taken {monster.attack} damage from the \n{monster.name}. Your health is now {player.health}.")

    playerHasLight = False
    roomHasLight = False
    for item in player.inventory:
        if isinstance(item, Lightsource):
            playerHasLight = True
    for item in player.currentRoom.inventory:
        if isinstance(item, Lightsource):
            roomHasLight = True
    if player.currentRoom.naturalLight or playerHasLight or roomHasLight:
        player.currentRoom.is_light = True
    else:
        player.currentRoom.is_light = False

    moveMonsters()

    if suppressRoomPrint:
        suppressRoomPrint = False
    elif player.currentRoom.is_light:
        print("------------------------------------------------")
        player.currentRoom.printName()
        player.currentRoom.printDesc()
        print()
        printMonsters()
        willItAttack = random.randint(0, 20)
        for monster in monsters:
            if monster.monsterCurrentRoom.name == player.currentRoom.name:
                if willItAttack <= 10:
                    monsterAttacks(monster)

        player.currentRoom.printInv()
        print()
    else:
        print("It's pitch black!")

    cmd = input("""================================================
What would you like to do, %s? """ % player.name)


    if cmd.upper() == 'N' or cmd.upper() == 'NORTH':
        if hasattr(player.currentRoom, 'n_to'):
            player.currentRoom = player.currentRoom.n_to
        else:
            printNoMove()
            printMonsters()
            suppressRoomPrint = True
    elif cmd.upper() == 'S' or cmd.upper() == 'SOUTH':
        if hasattr(player.currentRoom, 's_to'):
            player.currentRoom = player.currentRoom.s_to
        else:
            printNoMove()
            printMonsters()
            suppressRoomPrint = True
    elif cmd.upper() == 'E' or cmd.upper() == 'EAST':
        if hasattr(player.currentRoom, 'e_to'):
            player.currentRoom = player.currentRoom.e_to
        else:
            printNoMove()
            printMonsters()
            suppressRoomPrint = True
    elif cmd.upper() == 'W' or cmd.upper() == 'WEST':
        if hasattr(player.currentRoom, 'w_to'):
            player.currentRoom = player.currentRoom.w_to
        else:
            printNoMove()
            printMonsters()
            suppressRoomPrint = True
    elif cmd.upper() == 'INV' or cmd.upper() == 'I':
        player.printInv()
    elif "TAKE" in cmd.upper() and len(cmd) > 4:
        if cmd[5:].upper() == "ALL":
            while len(player.currentRoom.inventory) > 0:
                for item in player.currentRoom.inventory:
                    if isinstance(item, Treasure):
                        treasureOnTake(item)
                        item.on_take(player, player.currentRoom)
                    else:
                        item.on_take(player, player.currentRoom)
        else:
            isInInv = False
            stringCount = 0
            for item in player.currentRoom.inventory:
                if cmd[5:] in item.name:
                    isInInv = True
                    stringCount += 1
                    itemToTake = item
            if isInInv:
                if stringCount > 1:
                    print(f"I don't know which type of {cmd[5:]} you mean.")
                else:
                    if isinstance(item, Treasure):
                        treasureOnTake(itemToTake)
                        itemToTake.on_take(player, player.currentRoom)
                    else:
                        itemToTake.on_take(player, player.currentRoom)
            else:
                print("Sorry, %s, that item is not in this room." % player.name)
    elif cmd.upper() == "TAKE":
        print("Please specify what you would like to take.")
    elif "DROP" in cmd.upper():
        if cmd[5:].upper() == "ALL":
            while len(player.inventory) > 0:
                for item in player.inventory:
                    item.on_drop(player, player.currentRoom)
        else:
            isInInv = False
            for item in player.inventory:
                if cmd[5:] in item.name:
                    isInInv = True
                    item.on_drop(player, player.currentRoom)
            if not isInInv:
                print("You are not carrying that item.")
    elif cmd.upper() == "SCORE":
        print("Your score: %s" % player.score)
    elif cmd.upper() == "LOOK":
        if player.currentRoom.is_light:
            print("------------------------------------------------")
            player.currentRoom.printName()
            player.currentRoom.printDesc()
            print()
            player.currentRoom.printInv()
            print()
            suppressRoomPrint = True
        else:
            print("It's pitch black!")
    elif len(cmd) > 4 and "LOOK" in cmd.upper():
        if cmd[5:].upper() == 'N' or cmd[5:].upper() == 'NORTH':
            if hasattr(player.currentRoom, 'n_to'):
                if player.currentRoom.n_to.is_light:
                    print("Looking towards: ")
                    player.currentRoom.n_to.printName()
                    player.currentRoom.n_to.printDesc()
                else:
                    print("\nIt is too dark to see what is in that room.")
            else:
                print("\nThere is nothing to look at in that direction.\n")
        if cmd[5:].upper() == 'S' or cmd[5:].upper() == 'SOUTH':
            if hasattr(player.currentRoom, 's_to'):
                if player.currentRoom.s_to.is_light:
                    print("Looking towards: ")
                    player.currentRoom.s_to.printName()
                    player.currentRoom.s_to.printDesc()
                else:
                    print("\nIt is too dark to see what is in that room.")
            else:
                print("\nThere is nothing to look at in that direction.\n")
        if cmd[5:].upper() == 'E' or cmd[5:].upper() == 'EAST':
            if hasattr(player.currentRoom, 'e_to'):
                if player.currentRoom.e_to.is_light:
                    print("Looking towards: ")
                    player.currentRoom.e_to.printName()
                    player.currentRoom.e_to.printDesc()
                else:
                    print("\nIt is too dark to see what is in that room.")
            else:
                print("\nThere is nothing to look at in that direction.\n")
        if cmd[5:].upper() == 'W' or cmd[5:].upper() == 'WEST':
            if hasattr(player.currentRoom, 'w_to'):
                if player.currentRoom.w_to.is_light:
                    print("Looking towards: ")
                    player.currentRoom.w_to.printName()
                    player.currentRoom.w_to.printDesc()
                else:
                    print("\nIt is too dark to see what is in that room.")
            else:
                print("\nThere is nothing to look at in that direction.\n")
    elif "ATTACK" in cmd.upper():
        maxDmg = 0
        for item in player.inventory:
            if item.dmg > maxDmg:
                maxDmg = item.dmg
        for monster in monsters:
            if cmd[7:].upper() in monster.name.upper():
                monster.health -= maxDmg
                print(f"You hurt the {monster.name} by {maxDmg}.")
                if monster.health <= 0:
                    print(f"You have killed the {monster.name}!")
                    while len(monster.inventory) > 0:
                        for item in monster.inventory:
                            player.currentRoom.inventory.append(item)
                            monster.inventory.remove(item)
                    monsters.remove(monster)
                else:
                    willItAttack = random.randint(0, 20)
                    if willItAttack <= 10:
                        monsterAttacks(monster)
    elif cmd.upper() == "HEALTH":
        print(f"Your health: {player.health}")
    elif "EAT" in cmd.upper():
        for item in player.inventory:
            if cmd[4:] in item.name:
                if isinstance(item, Food):
                    player.health += item.healValue
                    if player.health > 100:
                        player.health = 100
                    player.inventory.remove(item)
                    print(f"You have eaten the {item.name} and your health is now {player.health}.")
                else:
                    print("You can't eat that!")
    elif cmd.upper() == 'Q' or cmd.upper() == 'QUIT':
        print("\nThanks for playing.\n")
        break
    elif cmd.upper() == 'H' or cmd.upper() == 'HELP':
        print("""\nCommands:
    'n' or 'north' to move north
    's' or 'south' to move south
    'e' or 'east' to move east
    'w' or 'west' to move west
    'i' or 'inv' to look in inventory
    'health' for health
    'look' or 'look <direction>' to get description of a room
    'score' for score
    'take <item>' to take
    'drop <item>' to drop
    'attack <monster>' to attack
    'q' or 'quit' to quit
    'h' or 'help' for help\n""")
    else:
        print("That command is not valid.")
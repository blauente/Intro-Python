# Write a class to hold player information, e.g. what room they are in
# currently.

class Player:
    def __init__(self, name, currentRoom, inventory):
        self.name = name
        self.currentRoom = currentRoom
        self.inventory = inventory
        self.score = 0
    def increaseScore(self, value):
        self.score += value
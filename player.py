from character import Character
from position import Position

class Player:
    def __init__(self, name = "NewPlayer", character = None, position = None, loadedcells = None,
                 inputs = None, connection = None):
        self.name = name
        if character:
            self.character = character
        else:
            self.character = Character()
        if position:
            self.position = position
        else:
            self.position = Position()
        if loadedcells:
            self.loadedcells = loadedcells
        else:
            self.loadedcells = []
        if inputs:
            self.inputs = inputs
        else:
            self.inputs = []
        if connection:
            self.connection = connection
        else:
            self.connection = None
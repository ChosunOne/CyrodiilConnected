from character import Character

class Player:
    def __init__(self, name = "NewPlayer", character = None, position = None, loadedcells = None,
                 inputs = None):
        self.name = name
        if character:
            self.character = character
        else:
            self.character = Character()
        if position:
            self.position = position
        else:
            pass #TODO make a default position
        if loadedcells:
            self.loadedcells = loadedcells
        else:
            pass #TODO make a default list of loadedcells
        if inputs:
            self.inputs = inputs
        else:
            pass #TODO make a default list of inputs
class Item:
    def __init__(self, name = "default_item", id = "00000000", weight = 0, value = 0, effects = None, 
                 quest = False, equipped = False, position = None):
        self.name = name
        self.id = id
        self.weight = weight
        self.value = value
        self.quest = quest
        self.equipped = equipped
        if effects:
            self.effects = effects
        else:
            self.effects = []
        if position:
            self.position = position
        else:
            pass #TODO make default position
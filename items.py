import inspect
from position import Position

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
            self.position = Position()

    def compare(self, other):
        """Compares this item with another, and returns the fields and values that differ with the other item, 
        returning a list of the other item's values"""
        changes = []

        ourAttributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        ourAttributes = [a for a in ourAttributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        theirAttributes = inspect.getmembers(other, lambda a:not(inspect.isroutine(a)))
        theirAttributes = [a for a in theirAttributes if not(a[0].startswith('__') and abs[0].endswith('__'))]

        for i in range(len(ourAttributes)):
            if ourAttributes[i][1] != theirAttributes[i][1]:
                changes.append(theirAttributes[i])

        return changes
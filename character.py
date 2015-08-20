import inspect
from attributes import Attributes
from skills import Skills
from inventory import Inventory
from position import Position

class Character:
    def __init__(self, name = "prisoner", inventory = None, equipped = None, attributes = None,
                 skills = None, level = 1, health = 100, fatigue = 100, magicka = 10, race = "imperial", 
                 encumbrance = 0, sneak = False, effects = None, spells = None, 
                 actions = None, gold = 0, quests = None, notoriety = 0, bounty = 0, fame = 0):
        self.name = name
        self.level = level
        self.health = health
        self.fatigue = fatigue
        self.magicka = magicka
        self.race = race
        self.encumbrance = encumbrance
        self.sneak = sneak
        self.notoriety = notoriety
        self.bounty = bounty
        self.gold = gold
        self.fame = fame
        if inventory:
            self.inventory = inventory
        else:
            self.inventory = Inventory()
        if equipped:
            self.equipped = equipped
        else:
            self.equipped = []
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = Attributes()
        if skills:
            self.skills = skills
        else:
            self.skills = Skills()
        if effects:
            self.effects = effects
        else:
            self.effects = []
        if spells:
            self.spells = spells
        else:
            self.spells = []
        if actions:
            self.actions = actions
        else:
            self.actions = []
        if quests:
            self.quests = quests
        else:
            self.quests = []

    def compare(self, character):
        """Compares this character with another, and outputs a list of attributes and values that are different with the other values"""
        ourAttributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        ourAttributes = [a for a in ourAttributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        theirAttributes = inspect.getmembers(character, lambda a:not(inspect.isroutine(a)))
        theirAttributes = [a for a in theirAttributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        changes = []

        for i in range(len(ourAttributes)):
            if ourAttributes[i][1] != theirAttributes[i][1]:
                changes.append(theirAttributes[i])

        return changes

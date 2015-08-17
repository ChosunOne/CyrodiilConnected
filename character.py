from attributes import Attributes
from skills import Skills
from inventory import Inventory

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
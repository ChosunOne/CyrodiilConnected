import inspect

class Attributes:
    def __init__(self, agility = 1, endurance = 1, intelligence = 1, luck = 1, personality = 1,
                 speed = 1, strength = 1, willpower = 1, aggression = 0, confidence = 0,
                 disposition = 0, energy = 0, responsibility = 0):
        self.agility = agility
        self.endurance = endurance
        self.intelligence = intelligence
        self.luck = luck
        self.personality = personality
        self.speed = speed
        self.strength = strength
        self.willpower = willpower
        self.aggression = aggression
        self.confidence = confidence
        self.disposition = disposition
        self.energy = energy
        self.responsibility = responsibility

    def compare(self, other):
        """Compares the attributes of this object with those of another, 
        and returns a list of the fields and the values of the other if they differ"""

        ourAttributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        ourAttributes = ourAttributes = [a for a in ourAttributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        theirAttributes = inspect.getmembers(other, lambda a:not(inspect.isroutine(a)))
        theirAttributes = [a for a in theirAttributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        changes = []

        for i in range(len(ourAttributes)):
            if ourAttributes[i][1] != theirAttributes[i][1]:
                changes.append(theirAttributes[i])

        return changes
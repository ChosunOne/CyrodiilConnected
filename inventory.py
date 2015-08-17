class Inventory:
    def __init__(self, items = None, weight = 0):
        if items:
            self.items = items
        else:
            self.items = []
        self.weight = weight

    def calcWeight(self):
        self.weight = 0
        for i in self.items:
            self.weight += i.weight

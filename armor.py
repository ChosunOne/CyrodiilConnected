from items import Item

class Armor(Item):
    def __init__(self, rating=1, health=100):
        super(Armor, self).__init__(name="default_armor", id="00000001")
        
        self.rating = rating
        self.health = health
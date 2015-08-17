from items import Item

class Weapon(Item):
    def __init__(self, damage=1, health=100):
        super(Weapon, self).__init__(name="default_weapon", id="00000002")
        
        self.damage = damage
        self.health = health
    
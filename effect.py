class Effect:
    def __init__(self, name = "default_effect", skill = None, magnitude = 0, duration = 1, disease = False,
                 spell = False, enchant = False):
        self.name = name
        self.magnitude = magnitude
        self.duration = duration
        self.disease = disease
        self.spell = spell
        self.enchant = enchant
        if skill:
            self.skill = skill
        else:
            pass #TODO add default skill
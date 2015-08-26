from cell import Cell

class Position:
    def __init__(self, local = None, world = None, heading = 0):
        if local:
            self.local = local
        else:
            self.local = (0, 0, 0)
        if world:
            self.world = world
        else:
            self.world = Cell()
        
        self.heading = heading

    def compare(self, other):
        """Compares this position with another, and returns a list of the fields and values of the other if it differs"""
        changes = []

        if self.local[0] != other.local[0] or self.local[1] != other.local[1] or self.local[2] != other.local[2]:
            changes.append(("local", other.local))
        if self.world.name != other.world.name:
            changes.append(("world", other.world))
        if self.heading != other.heading:
            changes.append(("heading", other.heading))

        return changes
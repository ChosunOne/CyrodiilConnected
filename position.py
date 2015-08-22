from cell import Cell

class Position:
    def __init__(self, local = None, world = None, orientation = None):
        if local:
            self.local = local
        else:
            self.local = 0
        if world:
            self.world = world
        else:
            self.world = Cell()
        if orientation:
            self.orientation = orientation
        else:
            self.orientation = 0

    def compare(self, other):
        """Compares this position with another, and returns a list of the fields and values of the other if it differs"""
        changes = []

        if self.local != other.local:
            changes.append(("local", other.local))
        if self.world.name != other.world.name:
            changes.append(("world", other.world))
        if self.orientation != other.orientation:
            changes.append(("orientation", other.orientation))

        return changes
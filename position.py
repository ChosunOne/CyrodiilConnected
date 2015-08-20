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
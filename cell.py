class Cell:
	def __init__(self, name = "default_cell", adjacentcells = None, items = None):
		self.name = name
		if adjacentcells:
			self.adjacentcells = adjacentcells
		else:
			self.adjacentcells = []
		if items:
			self.items = items
		else:
			self.items = []
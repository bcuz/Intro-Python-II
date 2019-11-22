class Item:
	def __init__(self, name, description):
		self.name = name
		self.description = description


	def on_take(self):
		input(f"\nYou have picked up {self.name}. Press [ENTER] to continue ")
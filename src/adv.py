from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
	'outside':  Room("Outside Cave Entrance", 
					 "North of you, the cave mount beckons", [Item('backpack', 'put in stuff'), Item('pencil', 'stab someone')]),

	'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

	'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", [Item('gun', 'make holes in stuff')]),

	'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", [Item('potion', 'heal yo\'self')]),

	'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", [Item('dust', 'nothing 4 u')]),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player('Adam', room['outside'])
# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
eligibleMoves = {
	'n': 'n_to',
	's': 's_to', 
	'e': 'e_to',
	'w': 'w_to',
	't': True,
	'd': True
}

def getItem(item):
	for idx, obj in enumerate(player.currentRoom.items):
		if obj.name == item:
			player.items.append(obj)
			obj.on_take()
			del player.currentRoom.items[idx]
			break

def dropItem(item):
	for idx, obj in enumerate(player.items):
		if obj.name == item:
			player.currentRoom.items.append(obj)
			obj.on_drop()
			del player.items[idx]
			break

def invalidCommand():
	input('Error, please enter a valid command. Press [ENTER] to try again ')

input('Introduction: Move north, south, east, or west with: n, s, e, or w. Take or drop an item by typing: t item or d item. q to quit and inv for current inventory. Press [ENTER] to start game ')
while True:
	print('----------------------------')
	print(f'Room: {player.currentRoom.name}')
	print(f'Description: {player.currentRoom.description}\n')

	if len(player.currentRoom.items) != 0:
		print("Items in the room: ")
		for i, v in enumerate(player.currentRoom.items):
			print(f'{i+1}. {v.name}')
	else:
		print('No items in room')
	response = input("\nWhat do you want to do? ").lower().split()
	if response[0] == 'q':
		print('Goodbye')
		break
	if response[0] == 'inv':
		if len(player.items) != 0:
			print("\nItems in your inventory: ")			
			for i, v in enumerate(player.items):
				print(f'{i+1}. {v.name}')
		else:
			print('\nYou have no items.')			
		input('Press [ENTER] to continue ')			

	elif len(response) == 1:
		if response[0] in eligibleMoves.keys():
			checkMove = getattr(player.currentRoom, eligibleMoves[response[0]])

			if checkMove != None:
				# change current room
				player.currentRoom = getattr(player.currentRoom, eligibleMoves[response[0]])
			else:
				input('Cant move in this direction. Press [ENTER] to try again ')
		else:
			invalidCommand()
	elif len(response) == 2:
		if response[0] in eligibleMoves.keys():

			if response[0] == 't' and response[1] in [item.name for item in player.currentRoom.items]:
				getItem(response[1])
			elif response[0] == 'd' and response[1] in [item.name for item in player.items]:
				dropItem(response[1])
			else:
				input('Item not found there. Press [ENTER] to try again ')				
		else:
			invalidCommand()
	else:
		invalidCommand()
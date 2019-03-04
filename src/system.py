import sys
import random


# ------------------------------------Gobal Variables-------------------------------

ACTION_MAP = {
	# gives offset in (x, y), do NOT overwrite
	'Up' : (-1, 0),
	'Right' : (0, 1),
	'Down' : (1, 0), 
	'Left' : (0, -1)
}

OFFSETS = {
	# self-explanatory
	'Up' : [(-1, -1), (-1, 1)], 
	'Right' : [(-1, 1), (1, 1)],
	'Down' : [(1, -1), (1, 1)],
	'Left' : [(-1, -1), (1, -1)]
}


# ------------------------------------Helper Functions-------------------------------

def move(mazegrid, state, action):
	"""Probabilistic formulation of the problem:

	Parameters: 

	- to be obtained by the init_problem function
	- action is one of the keys of ACTION_MAP

	I decided here to take the system equation model approach, because most of the system is anyways already
	encapsuled in the mazegrid and the probability p, as given in the assignment sheet. A completely 
	probabilistic description would be a lot of overhead both in parsing as well as in data. Especially 
	for large and more complex problems this would definitely kill the memory, and take a lot of handcraft 
	as well. Another thing is that a system equation model should generally, not always but in general,
	perform better in non-stationary systems."""

	p = 0.1 # see task sheet

	r = random.random() # between 0 and 1, equal distribution
	if r < 1-2*p:
		# go the desired way
		new_state = mazegrid[state[0] + ACTION_MAP[action][0], state[1] + ACTION_MAP[action][1]]
		return new_state
		# note: we checked already whether this action is allowed in this state, hence we do not have to worry about
		# the try: ... except: ... as below as well as check on '1'


	elif r < 1-p:
		# slip to one side
		try:
			new_state = mazegrid[state[0] + OFFSETS[action][0][0], state[1] + OFFSETS[action][0][1]]
			if new_state == '1': 
				new_state = mazegrid[state[0] + ACTION_MAP[action][0], state[1] + ACTION_MAP[action][1]]
			return new_state
		except IndexError:
			# we went out of the mazegrid with this command
			return None

	else:
		# slip to the other side
		try:
			new_state = mazegrid[state[0] + OFFSETS[action][1][0], state[1] + OFFSETS[action][1][1]]
			if new_state == '1': 
				new_state = mazegrid[state[0] + ACTION_MAP[action][0], state[1] + ACTION_MAP[action][1]]
			return new_state
		except IndexError:
			# we went out of the mazegrid with this command
			return None


import sys
import numpy as np

sys.path.insert(0, '../src/')
from system import ACTION_MAP


#-----------------------------------------------For IMPORT--------------------------------------------------

def init_problem(path):

	mazegrid = parse_file(path)
	start, action_state_map = get_grid(mazegrid)

	return start, mazegrid, action_state_map


#-----------------------------------------------HELPER FUNCTIONS--------------------------------------------------


def move(mazegrid, coordinates, action): 
	# coordinates are tuples, action is either 'Up', 'Down', 'Left' or 'Right'. Return successor state or None
	try: 
		new_state =  mazegrid[coordinates[0] + ACTION_MAP[action][0], coordinates[1] + ACTION_MAP[action][1]]
		if not new_state == '1': 
			return new_state
		else:
			return None 
	except: 
		# when falling out of the grid, i.e. array-overflow
		return None
	

def get_grid(mazegrid):
	# get the actions for a state parsing the mazegrid
	# my implementation is a bit of stupid and inefficient, it'd make sense to save the 'S' from when compiling the mazegrid,
	# but it's just small files, and there is marginal time loss here for such small files

	start = None
	action_state_map = [] # will be rather complex array. contains list of tuples for every state in (x,y) with (action, new_state) if action is possible in this state

	for x in range(mazegrid.shape[0]):
		y_dir = []
		for y in range(mazegrid.shape[1]):
			current_state = []
			for action in ACTION_MAP:

				new_state = move(mazegrid, (x, y), action)
				if new_state == None:
					continue

				current_state.append((action, new_state))
				if new_state == 'S' and start == None:
					start = (x + ACTION_MAP[action][0], y + ACTION_MAP[action][1])

			y_dir.append(np.array(current_state))
		action_state_map.append(np.array(y_dir))
	action_state_map = np.array(action_state_map)

	return start, action_state_map



def parse_file(path):
	# parse the file for the problem-mazegrid as defined by the task

	def isnum(n):
		# test on int-type
	    try:
	        int(n)
	        return True
	    except ValueError:
	        return False

	mazegrid = None
	start = None
	with open(path) as file:

		for line in file:
			line = line.split()
			if not line[0].startswith('#') and (isnum(line[0]) or line[0] in ['T', 'G', 'S']):

				newline = []
				for entry in line:
					if isnum(entry):
						newline.append(int(entry))
					elif entry in ['T', 'G', 'S']:
						newline.append(entry)


				if mazegrid is None: 
					mazegrid = newline
				else: 
					mazegrid = np.vstack((mazegrid, newline)) # must have same length as per problem description

	return mazegrid






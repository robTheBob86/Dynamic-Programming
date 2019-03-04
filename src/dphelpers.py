from system import ACTION_MAP, OFFSETS
import random

import numpy as np

# ------------------------------------Helper Functions-------------------------------



def T_g(J, state, alpha, cost_function):
	"""Apply the greedy T operator on to the state, return the new value"""

	if not cost_function in ['v1', 'v2']:
		raise Exception("Cost function must be either v1 or v2 as string.")

	(min_value, action) = (None, None)
	for act in ACTION_MAP:

		g_value, J_s  = _compute_expectation(J, state, act, cost_function)

		if g_value == None:
			continue # the action is not possible => wall

		TJ = g_value + alpha*J_s
		if min_value == None or min_value > TJ:
			min_value = TJ
			action = act

	return min_value, action



def init_values(mazegrid, cost_function):
	"""1. Initialize the values randomly as a grid, representing the states, 
	. This is needed for value iteration

	2. We linearize the states as a vector that we can parse throughout, containing 
	tuples ((x, y), J(s), g(s)), so we get both the value and the tuple for this state"""

	J = []
	for i in range(mazegrid.shape[0]):
		for j in range(mazegrid.shape[1]):

			if mazegrid[i, j] == '1':
				# we do not need this state
				continue
			if cost_function == 'v_1':
				J.append((i, j), 5*random.random(), _get_cost1(mazegrid, (i, j))) # we initialize probabilistic by values in between 0 and 5
			elif cost_function == 'v_2':
				J.append((i, j), 5*random.random(), _get_cost2(mazegrid, (i, j))) # we initialize probabilistic by values in between 0 and 5
	
	return J



def init_policy(mazegrid):
	"""Initialize the policy randomly as a grid, representing the states, 
	with up, down, left, right with equal probabilities. This is needed for 
	policy iteration"""

	policy = np.empty(mazegrid.shape)
	for i in range(mazegrid.shape[0]):
		for j in range(mazegrid.shape[1]):

			if mazegrid[i, j] == '1':
				policy[i, j] = '-' # useless
				continue

			r = random.random()
			if r < 0.25:
				policy[i, j] = 'Up'
			elif r < 0.5:
				policy[i, j] = 'Down'
			elif r < 0.75:
				policy[i, j] = 'Left'
			else:
				policy[i, j] = 'Right'

	return policy


# ------------------------------------Do not import-------------------------------

def _get_cost1(mazegrid, state): 
	"""This is g1 from task"""
	s = mazegrid[state[0], state[1]]

	if s == 'T': 
		return 50
	elif s == 'G':
		return -1
	else:
		return 0


def _get_cost2(mazegrid, state): 
	"""This is g2 from task"""
	s = mazegrid[state[0], state[1]]

	if s == 'T': 
		return 50
	elif s == 'G':
		return -1
	elif s == 'S':
		return 0
	else:
		return 1


def _compute_expectation(J, state, action, cost_function):
	"""Here we do compute the expectation values both on J(f(state, action, p)) and g(state, action), 
	where p here describes the whole sliding encapsulation"""

	def get_possible_states(J, state, action):
		# we return the states that are possible in this state due to the slippery ground
		states = [(state[0] + ACTION_MAP[action][0], state[1] + ACTION_MAP[action][1])] # the simple action commanded

		if (state[0] + OFFSETS[action][0][0], state[1] + OFFSETS[action][0][1]) in zip(*J)[0]:
			states.append(state[0] + OFFSETS[action][0][0], state[1] + OFFSETS[action][0][1])
		if (state[0] + OFFSETS[action][1][0], state[1] + OFFSETS[action][1][1]) in zip(*J)[0]:
			states.append(state[0] + OFFSETS[action][1][0], state[1] + OFFSETS[action][1][1])

		return states

	print("Here is the unzipping command of J")
	print(zip(*J)[0])

	if (state[0] + ACTION_MAP[action][0], state[1] + ACTION_MAP[action][1]) not in zip(*J)[0]:
		return None, None # the case when we hit a wall

	# init the expectation values
	g_value = 0
	J_s = 0

	possible_states = get_possible_states(J, state, action)
	if len(possible_states) == 1:
		g_value = J



import sys, os
import argparse

sys.path.insert(0, './utils/')
sys.path.insert(0, './src/')
from mazeparser import init_problem
from system import ACTION_MAP
from dphelpers import * # get_cost1(mazegrid, state), get_cost2(mazegrid, state), init_policy(mazegrid), init_values(mazegrid), get_costp


def main(path): 
	"""Obviously the main function in this assigment"""

	start, mazegrid, action_state_map = init_problem(path)
	value_iteration(start, mazegrid, action_state_map, 'v1')




def value_iteration(start, mazegrid, action_state_map, cost_function, alpha = 0.99):
	"""The whole value iteration algorithm is encapsuled in this function. As for the function J,
	I have decided to have a 1D-list object with tuples (cost, state, action_performed_getting_here). The action incorporates all 
	the information to the relevant path, and the cost are self-explanatory.

	cost_function can be 'v1' or 'v2', corredponding to get_cost1 or get_cost2 respectively

	NOTE: Since value iteration applies the optimal-operator, i.e. the minization operator, it is not 
	"""

	if not cost_function in ['v1', 'v2']:
		raise Exception("Cost function must be either v1 or v2 as string.")

	values = init_values(mazegrid)
	J = []
	paths = [[(0, start, 'start')]] # we need to store all the paths as well as J
	new_paths = []

	while not converged:

		for path in path:
			last_state = path[-1]
			for action, next_state in action_state_map[last_state[0], last_state[1]]:
				actions_states = action_state_map[last_state[0], last_state[1]]

				if cost_function == 'v1':
					new_paths.append(path.append((get_cost1(mazegrid, actions_states[1]))))
				else:
					new_paths.append(path.append((get_cost2(mazegrid, actions_states[1]))))

		paths = new_paths
		new_paths = []



def policy_iteration():
	pass
	


if __name__ == "__main__": 
	# Parse the stuff and go into the main function
	parser = argparse.ArgumentParser(description = "Copyright:\n Robert Baumgartner, \nga94kux(at)mytum.de, \n03688434")
	parser.add_argument('-f', '--filepath', type = str, help = 'Please give the absolute path to the problem file you want to solve \n\
		(see task description). The default value is the example problem from the task sheet.', default = 'utils/example.txt')
	args = parser.parse_args()

	path = args.filepath
	main(path)
import matplotlib.pyplot as pyplot
import math
import numpy as np 



def gridworld_policyiter(grid_size):

	n_states = grid_size**2

	target_states = [1,n_states]
	actions = [1,2,3,4] 	# 'N':1, 'S':2, 'E':3, 'W':4

	policy =  0.25 #[0.25,0.25,0.25,0.25] 			# 'N':0.25, 'S':0.25, 'E':0.25, 'W':0.25

	value_func_old = [0]*(n_states)
	value_func_new = [0]*(n_states)

	reward = -1				# 'N':-1, 'S':-1, 'E':-1, 'W':-1
	iterations = 11

	for iter in range(0,iterations):

		print('iteration number %d' %(iter))

		print (value_func_new)
		value_func_old = value_func_new
		value_func_new = [0]*n_states

		for state in range(1,n_states+1):

			if state == target_states[0] or state == target_states[1]:
				# print (" \n \nTarget state reached ")
				continue
				
			else:		

				for act in range(1, len(actions)+1):

					if state <= grid_size and act == 1:
						next_state = state
				
					elif n_states - state < grid_size and act == 2:
						next_state = state
				
					elif state%grid_size == 0 and act == 3:
						next_state = state
				
					elif (state - 1)%grid_size == 0 and act == 4:
						next_state = state

					else:	
						if act == 1:
							next_state = state - grid_size

						if act == 2:
							next_state = state + grid_size

						if act == 3:	
							next_state = state + 1 

						if act == 4:	
							next_state = state - 1 
						
					value_func_new[state-1] = value_func_new[state-1] + policy * ( reward + value_func_old[next_state-1])	

def gridworld_valueiter(grid_size):

	n_states = grid_size**2

	target_states = [1,n_states]
	actions = [1,2,3,4] 	# 'N':1, 'S':2, 'E':3, 'W':4

	policy =  0.25 #[0.25,0.25,0.25,0.25] 			# 'N':0.25, 'S':0.25, 'E':0.25, 'W':0.25

	value_func_old = [0]*(n_states)
	value_func_new = [0]*(n_states)

	reward = -1				# 'N':-1, 'S':-1, 'E':-1, 'W':-1
	iterations = 11


gridworld_policyiter(10)
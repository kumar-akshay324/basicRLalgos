# CartPole environment has a pole mounted on a cart that is placed on a frictionless surface. Depending upon the speed/actions
# applied on the cart, the pole swings and results in a change in the state. 

# A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track.
# The pendulum starts upright, and the goal is to prevent it from falling over by increasing and reducing the cart's velocity.

# The action space has two actions -	1 - Push the Cart Right 
# 										0 - Push the Cart Left

# Observation Space	

# observation[0] - Cart Position				Range(Minimum, Maximum) -  [-2.4, 2.4]
# observation[1] - Cart Velocity				Range(Minimum, Maximum) -  [-Inf, Inf]
# observation[2] - Pole Angle					Range(Minimum, Maximum) -  [-41.8, 41.8]
# observation[3] - Pole Velocity At Tip			Range(Minimum, Maximum) -  [-Inf, Inf]

# Rewards 	- 	Each time-step where action is taken, gives a positive reward of +1 and also for the termination 

# Start State - All observations are assigned a uniform random value between -0.05, 0.05

# Episode Termination condition 				Pole Angle is more than -20.9, 20.9
# 												Cart Position is more than -2.4, 2.4 (center of the cart reaches the edge of the display
# 												Episode length is greater than 200

import gym 
# from gym import envs
import random 
import numpy as np
from math import pi, log10

cum_rew, min_learn_rate, min_epsilon = 0, 0.1, 0.01

environment = gym.make('CartPole-v0')
environment.reset()
environment.render()
def check_working():

	print (environment.action_space)
	print (environment.observation_space.high, environment.observation_space.low )


	for epi in range(1,10):											# Number of episodes to be run
		obs = environment.reset()									# Reset the environment at the start of every episode
		# environment.step(environment.action_space.sample())
		for iterations in range(1,100): 
			environment.render()
			# if iterations%2==0:
			# 	obs, rew, done, info = environment.step(0)
			# if epi%2==1:	
			obs, rew, done, info = environment.step(1) #environment.action_space.sample())
			if done == True:
				environment.reset()
				# print ("Done")
				break
			obs1 = [ float(format(obs[i], '0.3f')) for i in range(0, len(obs))]	
		# print (float(format(obs, '0.2f')))	
		# print (obs1)	

def new_states(observ):
	obs_new =[]																# obs_new is the discretized state values
	obs_new.append(round(observ[0],1))			#format(observ[0], '0.1f'))
	
	if (observ[1]>0):
		obs_new.append(1)
	elif observ[1]<0:
		obs_new.append(-1)
	else:
		obs_new.append(0)
	observ[2] = observ[2]*100
	obs_new.append((observ[2] - observ[2]%10))	
	
	if observ[3]>0:
		obs_new.append(1)
	elif observ[3]<0:
		obs_new.append(-1)
	else:
		obs_new.append(0)
	return obs_new			

def get_learning_rate(t):
    return max(min_learn_rate, min(0.5, 1.0 - np.log10((t+1)/25)))

def get_epsilon(t):
    return max(min_epsilon, min(1.0, 1.0 - np.log10((t+1)/25)))


def greedy_action(explore_rate):
	if np.random.uniform()<explore_rate:
		acti = random.randint(0,1)
	else:
		acti = 'a'
	return acti	


def states_collection():										# Defining each new state 	
	state = []
	pp = np.arange(-2.4,2.4,0.1)
	qq = [-1,0,1]
	rr = np.arange(-50,50,10)
	ss = [-1,0,1]

	for p in range(0,48):
		for q in range(0,3):
			for r in range(0,10):
				for s in range(0,3):
					state.append(tuple((round(pp[p],1), qq[q], rr[r], ss[s])))
	return state					


def simulate(disc_fac, num_episodes = 20, num_runs = 250, learn_rate =1):

	Q = np.zeros((4320, 2))							# Initialising the Action Value function matrix with zeros
													# Total number of discretized states is 4320 and each state has 2 actions
													# Each new observation is compared to the existing discretized state-space rep
													# When matched, that corresponding row in Q is the state's row  
	cum_rew = 0
	states = states_collection()

	learn_rate = get_learning_rate(0)
	epsilon = get_epsilon(0)

	# print (states)												
 # 	print(Q[2])
	for epi in range(0, num_episodes):
		observation = environment.reset()

		neww_state = new_states(observation)
		# print (neww_state, len(states))
		# state_index_old = [i for i in range(0, len(states)) if neww_state == states[i]]
		for comp in range(0, len(states)):
			if neww_state == states[comp]:
				break
		state_index_old = comp		

		# print("State index old", state_index_old)

		for runs in range(0, num_runs):

			acti = greedy_action(epsilon)
			if acti == 'a':
				act = np.argmax(Q[state_index_old])
			else:
				act = acti

			obse, rewa, done, info = environment.step(act) 
			environment.render()
			new_observ = new_states(obse)

			for comp in range(0, len(states)):
				if new_observ == states[comp]:
					break
			state_index_new = comp	

			best_Q = np.max(Q[state_index_new])
			Q[state_index_old][act] += learn_rate*(rewa + disc_fac*best_Q - Q[state_index_old][act])
			state_index_old = state_index_new

			print ("Episode = %d" %(epi))
			print ("Run = %d" %(runs))
			print ("Action = %d" %(act))
			print ("State = ", new_observ)
			print ("Reward = %f" %(rewa))
			print ("Best Q value = %f " %(best_Q))
			print ("Explore rate = %f \n Learning rate = %f \n \n " %(epsilon, learn_rate))
			print ("observation space shaped", environment.observation_space.shape[0])


			if done:
				print ("Episode finished after %d runs in  episode %d" %(runs+1, epi + 1))
				break
			cum_rew = cum_rew + rewa


		learn_rate   = get_learning_rate(epi+1)
		epsilon = get_epsilon(epi+1)
		# print ("Learning rate is %f" %(learn_rate))
		print ("Cumulative Reward is %d \n \n " %(cum_rew))
		print ("------------------------------------")

		cum_rew = 0


if __name__ == "__main__":
	# check_working()

	simulate(0.99,1000, 250, 0.8)
# check_working()
# Random Walk example

# Suppose you live in a city with grid setup. One evening you decide to go for a random walk and you realise that for 
# if your walk ends at more than 4 blocks away from your home in any direction, you will hava to take transport on your
# way back home

# Walk size is the number of blocks that you walk without being more than 4 blocks away from home

# Compute the highest walk length with more than half chances of you ending up in state where you don't need to take a
# transport on your way back home(Upto 4 blocks away from home)

# Using Monte Carlo Technique of random searches 

import math
import random
import matplotlib.pyplot as plt


def random_walk(n):
	x, y = 0, 0
	dir_available = ['N', 'S', 'E', 'W']
	
	for i in range(1,n):


		dir_random = random.choice(dir_available)

		if dir_random == 'E':
			x +=1
		elif dir_random == 'W':
			x -=1
		elif dir_random == 'N':
			y +=1
		else:
			y -=1
	return (x, y)	

number_walks =10000;
perc, walk_size_p, limit = [], [], [50]*30

# x, y = random_walk(25)
# # print (x,y)

for walk_size in range(1,31):
	no_trans = 0

	for count in range(number_walks):
		x, y = random_walk(walk_size)
		dist = abs(x) + abs(y)
		if dist <= 4:
			no_trans +=1

	no_trans_perc = float(no_trans)/number_walks
	perc.append( no_trans_perc * 100)
	walk_size_p.append(walk_size)	

	print ("Walk size ", walk_size, "Free transport chances", no_trans_perc)
plt.plot(walk_size_p, perc, 'ro--')
plt.plot(walk_size_p, limit, 'r*-' )
plt.show()




		

		


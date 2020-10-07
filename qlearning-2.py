import gym
import numpy as np

env = gym.make("MountainCar-v0")


# specify reward function parameters
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISOES = 25000
epsilon = 0.5 # adding randomness for exploration
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISOES // 2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

SHOW_EVERY = 2000

# creat Q table, 20 discrete values for each dimension in observation space
# making the entire Q table 20*20*3, 3 being 3 different possible actions
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

#print(discrete_os_win_size)

q_table = np.random.uniform(low=-2,high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))
print(q_table.shape)

# lumping continuous state into buckets of discrete states
def get_discrete_state(state):
	discrete_state = (state - env.observation_space.low) / discrete_os_win_size
	return tuple(discrete_state.astype(np.int))

# The Loop for Episodes
for episode in range(EPISOES):
	# render once every 2000 episodes, just to show program is still alive
	if episode % SHOW_EVERY == 0:
		render = True
		print(episode)
	else:
		render = False

	discrete_state = get_discrete_state(env.reset())
	'''
	print(env.reset())				# initial x,y position of vehicle
	print(discrete_state)			# initial position in discrete form
	print(q_table[discrete_state])	# randomized initial q value at initial position
	print(np.argmax(q_table[discrete_state]))	# best action based on q table
	'''
	done = False

	while not done:
		# exploration
		if np.random.random() > epsilon:
			action = np.argmax(q_table[discrete_state])
		else:
			action = np.random.randint(0, env.action_space.n)
		new_state, reward, done, _ = env.step(action)

		new_discrete_state = get_discrete_state(new_state)

		#print(reward, new_state)
		if render:
			env.render()

		if not done:
			# The Q learning formula, see https://youtu.be/Gq1Azv_B4-4?t=548
			max_future_q = np.max(q_table[new_discrete_state])
			current_q = q_table[discrete_state + (action, )]

			new_q = (1-LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
			q_table[discrete_state+(action, )] = new_q
		elif new_state[0] >= env.goal_position:
			q_table[discrete_state + (action, )] = 0	# if goal reached, no punishment
			print(f"We made it on episode {episode}")

		discrete_state = new_discrete_state

	# decrease exploration by a small amount each time, getting older, wiser and more reluctant to change
	if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
		epsilon -= epsilon_decay_value
env.close()
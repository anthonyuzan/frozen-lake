# Imported libraries
import numpy as np
import gym
import random
import time
from IPython.display import clear_output
import os

# Environment creation
env = gym.make("FrozenLake-v0")

# Q-table initialization
action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))

# Parameters initialization
num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.1
discount_rate = 0.99

exploration_rate = 1                # Epsilon value
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

print("Training in progress...")

# Implementing the algorithm
rewards_all_episodes = []

# Q-learning algorithm
for episode in range(num_episodes):
    state = env.reset()
    done = False
    rewards_current_episode = 0

    for step in range(max_steps_per_episode):
        # Exploration-exploitation trade-off
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])
        else:
            action = env.action_space.sample()

        new_state, reward, done, info = env.step(action)

        #Update Q-table for Q(s,a)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
        
        state = new_state
        rewards_current_episode += reward

        if done:
            break
        
    # Exploration rate decay
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

    rewards_all_episodes.append(rewards_current_episode)  


# Calculate and print the average reward per thousand episodes
os.system('cls')
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes/1000)
count = 1000
print("\tAverage reward per thousand episodes")
print("\t____________________________________\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000

# Print updated Q-table
print("\n\n\tQ-table")
print("\t_______\n")
print(q_table)

print("\n\nPress [ENTER] to watch a simulation of this training...")
input()
os.system('cls')
clear_output(wait=True)


# Simulation to see the agent after the training 
for episode in range(3):
    state = env.reset()
    done = False
    print("\tEPISODE ", episode+1)
    print("\t_________\n")
    time.sleep(1.5)

    for step in range(max_steps_per_episode):
        os.system('cls')
        clear_output(wait=True)
        env.render()
        time.sleep(0.3)

        action = np.argmax(q_table[state, :])
        new_state, reward, done, info = env.step(action)

        if done:
            os.system('cls')
            clear_output(wait=True)
            env.render()
            if reward == 1:
                print("\n--> You reached the goal! :)")
                time.sleep(3)
            else:
                print("\n--> You fell through a hole! :(")
                time.sleep(3)
            os.system('cls')
            clear_output(wait=True)
            break
        state = new_state

env.close()
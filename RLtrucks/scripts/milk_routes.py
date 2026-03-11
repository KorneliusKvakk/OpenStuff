# %% Import dependencies
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal, johan.stendal@sintef.no
"""
import os
import time
import numpy as np
from itertools import cycle

from env import Env
from utilities import *
from config import *

# %% milk route baseline, drive the entire road network in a circle, every depot is visited once per route
env = Env()
# env.episode_length = 1000
n_episodes = 1000
testing_time_start = time.time()
# milk route actions
milk_route_deg = np.array([270, 180, 90, 90, 0, 0, 0, 270, 270, 180, 90])

for episode in range(0, n_episodes):
    cycle_milk_route_deg = cycle(milk_route_deg)
    step = 0
    done = False
    while not done:
        if step == 0:
            action = 0
        else:
            action = next(cycle_milk_route_deg) / 90 # angle of depots resultant vector, converted from deg to action
        state, reward, done, truncated, info = env.step(action)
        step += 1
    env.reset()
env.close()
testing_time_end = time.time()
print('Time: ', formatSeconds((testing_time_end - testing_time_start)))





# # %% milk route baseline, drive the entire road network in a circle, every depot is visited once per route
# env = Env()
# n_milk_routes = 1000
# milk_route_degrees = np.array([270, 180, 90, 90, 0, 0, 0, 270, 270, 180, 90])
# milk_route_actions = milk_route_degrees / 90
# env.episode_length = n_milk_routes * len(milk_route_actions)
# milk_route_actions_all = []
# for i in range(n_milk_routes):
#     milk_route_actions_all.append(milk_route_actions) # milk route steps in degrees
# milk_route_actions_flat = [item for sublist in milk_route_actions_all for item in sublist]
# step = 0
# done = False
# testing_time_start = time.time()
# while not done:
#     action = milk_route_actions_flat[step] # milk route action from list of milk route actions
#     state, reward, done, truncated, info = env.step(action)
#     step += 1
# env.reset()
# env.close()
# testing_time_end = time.time()
# print('Milk routes time: ', formatSeconds((testing_time_end - testing_time_start)))

# # %%

# %%

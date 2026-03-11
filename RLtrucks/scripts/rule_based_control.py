# %% Import dependencies
"""
Created on April 12 09:47 2023
@author: Johan Andreas Stendal, johan.stendal@sintef.no
"""
import os
import time
import numpy as np

from env import Env
from utilities import *
from config import *

# %% rule based control, always drive the truck in the direction where it has most packages to (same angle as used for observations for RL agent)
env = Env()
# env.episode_length = 1000
n_episodes = 1000
testing_time_start = time.time()
for episode in range(0, n_episodes):
    step = 0
    done = False
    while not done:
        if step == 0:
            action = 0
        else:
            action = env.sim.depots_resultant_angle_deg / 90 # angle of depots resultant vector, converted from deg to action
        state, reward, done, truncated, info = env.step(action)
        step += 1
    env.reset()
env.close()
testing_time_end = time.time()
print('Time: ', formatSeconds((testing_time_end - testing_time_start)))

# %%

"""
The environment class defines the environment that the agent will interact with.

It is described by the three basic functions:
step() handles the logic of each environment time step.
reset() resets given initial conditions of the environment after each training episode.
render() handles the visualization of the environment during training.

seed() can be used to control the randomness of training to produce repeatable training evolutions.

We use  OpenAIGym to create the environment: http://gym.openai.com/docs
We will use the `upper_bound` parameter to scale our actions later.
"""
# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import math
import time
import json
import random

import gym

from sim import *
from utilities import *
from config import *

class Env(gym.Env):
    def __init__(self):
        # Initialize episode length, episode number and timestep number
        self.episode_length = EPISODE_LENGTH
        self.n_episode = N_EPISODE_0
        self.n_timestep = N_TIMESTEP_0

        # Initialize reward
        self.reward = REWARD_0

        # Initialize episode number, reward and eisode time lists
        self.n_episode_list           = []
        self.reward_list              = []
        self.episode_time_list        = []
        self.episode_time_cumsum_list = []
        self.model_input_list         = []
        self.obs_list                 = []

        # Observation ranges for normalizing the observations, all possible observations should fit inside these ranges
        self.obs_min = [0,     0,   0]
        self.obs_max = [10, 1500, 360]

        # Normalized observation ranges, used for defining the observation space for the agent
        self.obs_norm_min = [0, 0, 0]
        self.obs_norm_max = [1, 1, 1]

        # Define observation space
        self.observation_space = gym.spaces.Box(np.array(self.obs_norm_min, dtype=np.float32), np.array(self.obs_norm_max, dtype=np.float32))

        # Define action space
        self.action_space = gym.spaces.Discrete(4)

        # Initialize state
        self.state = []

        # Initialize sim
        self.sim = Sim()

        # Initialize rl metrics
        self.rl_metrics_df = pd.DataFrame(columns=['Truck position int', 'Truck capacity kg', 'Depots resultant angle deg', 'Action', 'Reward'])

        # Create main folder for training run
        createDir()

    def seed(self):
        pass

    def step(self, action):
        global truck_needs_action
        # Episode info
        info = {}
        
        if self.n_timestep == N_TIMESTEP_0:
            # Create new folder directory at beginning of episode
            newDir(self.n_episode)
            # Start episode timer
            self.episode_time_start = time.time()

        truck_needs_action = False
        while truck_needs_action == False:
            truck_needs_action, obs, reward = self.sim.run_sim(action) # run sim until truck has stopped at station
        else:
            truck_needs_action, obs, reward = self.sim.run_sim(action) # run sim one more step start driving truck

        # Normalize observations (interpolate to a value between 0 and 1 or alt. -1 and 1)
        obs_norm = []
        for i in range(len(obs)):
            obs_norm.append((obs[i] - self.obs_min[i]) / (self.obs_max[i] - self.obs_min[i]))

        # State/observations
        self.state = np.array(obs_norm, dtype=np.float32)

        # Reward Function
        self.reward = reward

        # Count Time Step
        self.n_timestep += 1

        # Check if episode is done
        if self.n_timestep >= self.episode_length:
            done = True
        else:
            done = False

        # output rl metrics
        rl_metrics = pd.DataFrame({'Truck position int': [obs[0]],
                                    'Truck capacity kg': [obs[1]],
                                    'Depots resultant angle deg': [obs[2]], 
                                    'Action': [action], 
                                    'Reward': [reward]})
        self.rl_metrics_df = pd.concat([self.rl_metrics_df, rl_metrics])
        
        if done:
            # rl metrics excel
            self.rl_metrics_df.to_excel('rl_metrics.xlsx', index=False)
            # sim metrics excel
            sim_metrics_df = pd.DataFrame(self.sim.sim_metrics).T
            sim_metrics_df.columns = ['Road', 'Distance', 'Total duration', 'Road duration', 'Consumption', 'Num packages']
            sim_metrics_df.to_excel('sim_metrics.xlsx', index=False)
            # Up one level in folder structure for next episode
            os.chdir('..')
            # Count episode
            self.n_episode += 1

        return self.state, self.reward, done, info

    def reset(self):
        # reset environment
        self.sim.timestep_counter = 0

        self.sim.truck00_roads_driven = []
        self.sim.truck00_km_driven = []
        self.sim.truck00_total_min = []
        self.sim.truck00_road_min = []
        self.sim.truck00_fuel_consumption = []
        self.sim.truck00_n_packages = []
        self.sim.truck00_n_packages_delivered = 0

        self.sim.sim_metrics = []

        for truck in self.sim.trucks:
            truck.position = get_station_position(self.sim.stations, 'Hub00')
            truck.capacity_kg = truck.capacity_kg_0
            truck.velocity_kmpm = truck.velocity_kmpm_0
            truck.fuel_consumption_lpkm = truck.fuel_consumption_lpkm_0
            truck.loaded_packages = []
            truck.ready_to_go = False
            truck.driving = False
            truck.driving_time_min = truck.driving_time_min_0
            truck.roadtrip_start_position = (0, 0)
            truck.roadtrip_end_position = (0, 0)
            truck.last_road_driven = []

        for hub in self.sim.hubs:
            hub.packages_at_station = []

        for depot in self.sim.depots:
            depot.packages_at_station = []

        self.n_timestep = N_TIMESTEP_0
        self.reward = REWARD_0

        pygame.display.quit()
        pygame.init()

        return self.state

    def close(self):
        pass
# %%

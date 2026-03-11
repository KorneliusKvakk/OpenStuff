# %%
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal, johan.stendal@sintef.no
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import math
import time
import json
import random

import gymnasium as gym

from sim import *
from utilities import *
from config import *

class Env(gym.Env):
    def __init__(self):
        # Initialize episode length, episode number and timestep number
        self.episode_length = EPISODE_LENGTH
        self.episode_number = 0
        self.timestep_rl = 0

        # Initialize reward
        self.reward = 0

        # # Initialize episode number, reward and eisode time lists
        # self.episode_number_list      = []
        # self.reward_list              = []
        # self.episode_time_list        = []
        # self.episode_time_cumsum_list = []
        # self.model_input_list         = []
        # self.obs_list                 = []

        # Observation ranges for normalizing the observations, all possible observations should fit inside these ranges
        self.obs_min = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.obs_max = [1500, 1.1, 10, 4, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]

        # Normalized observation ranges, used for defining the observation space for the agent
        self.obs_norm_min = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.obs_norm_max = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # Action ranges and scaling, defines the action space for the agent
        self.act_min = 0
        self.act_max = 1

        # Define observation space
        self.observation_space = gym.spaces.Box(np.array(self.obs_norm_min, dtype=np.float32), np.array(self.obs_norm_max, dtype=np.float32))

        # Define action space
        # self.action_space = gym.spaces.Box(np.array(self.act_min, dtype=np.float32), np.array(self.act_max, dtype=np.float32))
        self.action_space = gym.spaces.Discrete(4)

        # Initialize state
        self.state = []

        # Initialize sim with draw environment bool
        self.sim = Sim(draw_env = False)

        # Initialize rl metrics
        self.rl_metrics_df = pd.DataFrame(columns=['Truck position int', 'Truck capacity kg', 'Depots resultant angle deg', 'Depots resultant magnitude', 'Action deg', 'Timestep reward'])
        self.episode_reward = 0
        # TODO runnr in filename
        self.episodes_stats_df = pd.DataFrame(columns=['Episode packages delivered', 'Episode km driven', 'Episode fuel consumed', 'Episode reward'])

        # Create main folder for training run
        createDir()

    # def seed(self):
    #     pass

    def step(self, action):
        global update_action

        # Episode info
        info = {}
        
        if self.timestep_rl == 0:
            # Create new folder directory at beginning of episode
            newDir(self.episode_number)
            # Start episode timer
            self.episode_time_start = time.time()

        action_deg = action * 90

        update_action = False
        while update_action == False:
            update_action, obs, reward = self.sim.run_sim(action_deg) # run sim until truck has stopped at station
        else:
            update_action, obs, reward = self.sim.run_sim(action_deg) # run sim one more step to start driving truck

        # Normalize observations (interpolate to a value between 0 and 1 or alt. -1 and 1)
        obs_norm = []
        for i in range(len(obs)):
            obs_norm.append((obs[i] - self.obs_min[i]) / (self.obs_max[i] - self.obs_min[i]))

        # State/observations
        self.state = np.array(obs_norm, dtype=np.float32)

        # Reward Function
        self.reward = reward

        # Count Time Step
        self.timestep_rl += 1

        # Check if episode is done
        if self.timestep_rl >= self.episode_length:
            done = True
        else:
            done = False

        # output rl metrics
        self.rl_metrics = pd.DataFrame({'Truck position int': [obs[0]],
                                        'Truck capacity kg': [obs[1]],
                                        'Depots resultant angle deg': [obs[2]],
                                        'Depots resultant magnitude': [obs[3]],
                                        'Action deg': [action_deg], 
                                        'Timestep reward': [reward]})
        self.rl_metrics_df = pd.concat([self.rl_metrics_df, self.rl_metrics])

        self.episode_reward += reward
        
        if done:
            # episode stats
            self.episode_stats_df = pd.DataFrame({'Episode packages delivered': [self.sim.truck00_n_packages_delivered],
                                                  'Episode km driven': [np.sum(np.array(self.sim.truck00_km_driven))],
                                                  'Episode fuel consumed': [np.sum(np.array(self.sim.truck00_fuel_consumption) * np.array(self.sim.truck00_km_driven))],
                                                  'Episode reward': [self.episode_reward]})
            self.episodes_stats_df = pd.concat([self.episodes_stats_df, self.episode_stats_df])
            self.episodes_stats_df.to_excel('../../episodes_stats.xlsx', index=False)
            # rl metrics excel
            self.rl_metrics_df.to_excel('rl_metrics.xlsx', index=False)
            # sim metrics excel
            sim_metrics_df = pd.DataFrame(self.sim.sim_metrics).T
            sim_metrics_df.columns = ['Road', 'Distance', 'Total duration', 'Road duration', 'Consumption', 'Packages in truck']
            sim_metrics_df.to_excel('sim_metrics.xlsx', index=False)
            # Up one level in folder structure for next episode
            os.chdir('..')
            # Count episode
            self.episode_number += 1

        return self.state, self.reward, done, False, info

    def reset(self, seed=None, options=None):
        print('Episode reward: ' + str(self.episode_reward))

        super().reset(seed=seed)
        info = {}

        self.episode_reward = 0

        # reset environment
        self.sim.timestep_sim = 0

        self.sim.truck00_roads_driven = []
        self.sim.truck00_km_driven = []
        self.sim.truck00_total_min = []
        self.sim.truck00_road_min = []
        self.sim.truck00_fuel_consumption = []
        self.sim.truck00_n_packages = []
        self.sim.truck00_n_packages_delivered = 0

        self.rl_metrics_df = pd.DataFrame(columns=['Truck position int', 'Truck capacity kg', 'Depots resultant angle deg', 'Depots resultant magnitude', 'Action deg', 'Timestep reward'])
        self.rl_metrics = []
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

        self.timestep_rl = 0
        self.reward = 0

        return self.state, info

    def close(self):
        pass
# %%

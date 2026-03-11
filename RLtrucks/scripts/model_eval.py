# %% Import dependencies
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal, johan.stendal@sintef.no 
"""
import time

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

from env import Env
from utilities import *
from config import *

# %% Load and test environment with random sample actions
# Atleast 1 test episode has to be run to load the environment
env = Env()
n_test_episodes = 1
print('Observation space:', env.observation_space)
print('Action space:', env.action_space)
print('-----------------------------------------')
testing_time_start = time.time()
for episode in range(0, n_test_episodes):
    done = False
    while not done:
        action = env.action_space.sample()
        state, reward, done, truncated, info = env.step(action)
    env.reset()
env.close()
testing_time_end = time.time()
print('-----------------------------------------')
print('Avg. time per test episode: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes), '/ Avg. time per 100 test episodes: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes * 100))

# %% Load model
loaded_model = PPO.load(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\RL_run_GOOD\saved_model\saved_model.zip', env=env)
# print NN architectures
loaded_model.policy_kwargs

# %% Run environment with actions predicted by trained model
n_run_episodes = 1000
print('Observation space:', env.observation_space)
print('Action space:', env.action_space)
print('-----------------------------------------')
testing_time_start = time.time()
for episode in range(0, n_run_episodes):
    done = False
    while not done:
        action, state = loaded_model.predict(env.state)
        state, reward, done, truncated, info = env.step(action)
    env.reset()
env.close()
testing_time_end = time.time()
print('-----------------------------------------')
print('Avg. time per test episode: ', formatSeconds((testing_time_end - testing_time_start) / n_run_episodes), '/ Avg. time per 100 test episodes: ', formatSeconds((testing_time_end - testing_time_start) / n_run_episodes * 100))

# %% Evaluate model
n_eval_episodes = 5 # number of episodes to run for evaluation
mean_reward, std_reward = evaluate_policy(loaded_model, env, n_eval_episodes=n_eval_episodes)
mean_reward, std_reward

# %%

# %% Import dependencies
"""
Created on June 5 10:11 2023
@author: Johan Andreas Stendal, johan.stendal@sintef.no
"""
import os
import time
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
# from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise, NormalActionNoise

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
        action = env.action_space.sample() # random action sampled from action space
        state, reward, done, truncated, info = env.step(action)
    env.reset()
env.close()
testing_time_end = time.time()
print('-----------------------------------------')
print('Avg. time per test episode: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes), '/ Avg. time per 100 test episodes: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes * 100))

# %% training parameters
bestmodel_path       = '../best_model'
savemodel_path       = '../saved_model'

if not os.path.exists(bestmodel_path):
    os.makedirs(bestmodel_path)
if not os.path.exists(savemodel_path):
    os.makedirs(savemodel_path)

n_training_episodes = 1000
total_timesteps = n_training_episodes * env.episode_length # total number of training time steps
reward_threshold = 3000 # reward threshold at which to stop training
eval_freq = 50 * env.episode_length # evaluation frequency in time steps
n_eval_episodes = 3 # number of episodes to run in test environment during evaluation

# neural network architechtures; pi: actor, qf: quality function (critic)
n_neuron = 100
net_arch = dict(qf=[50, 300, 300, 300, 150, 50, 30, 5], pi=[50, 300, 300, 300, 150, 50, 30, 5])
# [30, 100, 100, 100, 50, 30, 15, 5] good
# [50, 300, 300, 300, 150, 50, 30, 5] better

# stop training threshold
stop_callback = StopTrainingOnRewardThreshold(reward_threshold=reward_threshold, verbose=1) 
# add callback to training stage
eval_callback = EvalCallback(env,                                
                            callback_on_new_best=stop_callback,
                            eval_freq=eval_freq,
                            n_eval_episodes=n_eval_episodes,
                            best_model_save_path=bestmodel_path,
                            verbose=1)

# %% Ceate and train RL model
model = PPO(
    policy = 'MlpPolicy',
    env = env,
    gamma = 0.99,
    policy_kwargs={'net_arch': net_arch},
    verbose = 1,
    ent_coef = 0.1,
    learning_rate = 1e-4,
    batch_size = 512,
    
    # tensorboard_log = tensorboard_log_path,
    # nb_train_steps=5000,
	# nb_rollout_steps=10000,
	# nb_eval_steps=10000,
    # actor_lr = 0.0001,
	# critic_lr = 0.001,
    # reward_scale = 1,
    # memory_limit = 10000000,
    # tau = 0.003,
	# batch_size = 256,
)

training_time_start = time.time()

model.learn(total_timesteps=total_timesteps, callback=eval_callback)

training_time_end = time.time()
print('Training time: ', formatSeconds(training_time_end - training_time_start))

model.save(savemodel_path)

# %%

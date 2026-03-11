"""
YouTube tutorial: https://www.youtube.com/watch?v=Mut_u40Sqz4&t=8181s
Stable Baselines homepage: https://stable-baselines3.readthedocs.io/en/master/
Gym homepage: https://gym.openai.com/
"""

# %% Import dependencies
import os
import numpy as np
import pandas as pd
import time

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise, NormalActionNoise

from env import Env # Import PRO3 environment: NaMo and AlEx
from utilities import *
from config import *

# %% Load and test environment with random sample actions
env = Env()

# Atleast 1 test episode has to be run for model.learn() to work
n_test_episodes = 20

print('Observation space:', env.observation_space)
print('Action space:', env.action_space)
print('-----------------------------------------')

testing_time_start = time.time()
for episode in range(0, n_test_episodes):
    done = False
    while not done:
        action = env.action_space.sample()
        n_state, reward, done, truncated, info = env.step(action)
    env.reset()
env.close()
testing_time_end = time.time()

print('-----------------------------------------')
print('Avg. time per test episode: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes), '/ Avg. time per 100 test episodes: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes * 100))

# %% training parameters
tensorboard_log_path = '../tensorboard_log'
bestmodel_path       = '../best_model'
savemodel_path       = '../saved_models'

if not os.path.exists(tensorboard_log_path):
    os.makedirs(tensorboard_log_path)
if not os.path.exists(bestmodel_path):
    os.makedirs(bestmodel_path)
if not os.path.exists(savemodel_path):
    os.makedirs(savemodel_path)

total_timesteps = 1500 * env.episode_length # total number of training time steps
reward_threshold = 8000 # reward threshold at which to stop training
eval_freq = 15 * env.episode_length # evaluation frequency in time steps
n_eval_episodes = 3 # number of episodes to run in test environment during evaluation

# neural network architechtures; pi: actor, qf: quality function (critic)
n_neuron = 300
net_arch = dict(qf=[n_neuron, n_neuron, n_neuron], pi=[n_neuron, n_neuron, n_neuron])

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
    # tensorboard_log = tensorboard_log_path,
    verbose = 1
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

# %% Load best model
model = PPO.load(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\RL\rlrun_00010\best_model\best_model.zip', env=env) # load model from Best Models
# model = PPO.load(savemodel_path, env=env) # load model from Saved Models

# %% Evaluate model
n_eval_episodes = 5 # number of episodes to run for evaluation
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=n_eval_episodes)
mean_reward, std_reward

# %% Run environment with actions predicted by trained model
n_run_episodes = 20

print('Observation space:', env.observation_space)
print('Action space:', env.action_space)
print('-----------------------------------------')

testing_time_start = time.time()
for episode in range(0, n_test_episodes):
    done = False
    while not done:
        action, n_state = model.predict(env.state)
        n_state, reward, done, truncated, info = env.step(action)
    env.reset()
env.close()
testing_time_end = time.time()

print('-----------------------------------------')
print('Avg. time per test episode: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes), '/ Avg. time per 100 test episodes: ', formatSeconds((testing_time_end - testing_time_start) / n_test_episodes * 100))




# n_run_episodes = 5
# for episode in range(1,n_run_episodes+1):
#     # initial
#     state = env.reset()
#     done = False
#     # main loop
#     while not done:
#         env.render()
#         action, _state = model.predict(state)
#         n_state, reward, done, info = env.step(action)
# env.close()

# %% Save model
model.save('../../best_model')

# %% Delete and load model
# del model # delete model
# model = DDPG.load(r'C:\Users\johans\SINTEF\PRO3 - 2021_Kjøling av profiler\Pro3__Runs\001_TestMappestruktur\Training\Best Models\best_model.zip', env=env) # load model from Best Models
# model = DDPG.load(savemodel_path, env=env) # load model from Saved Models

# # %% Viewing logs in tensorboard
# training_log_path = os.path.join(tensorboard_log_path, 'DDPG_1')
# !tensorboard --logdir = {tensorboard_log_path}
# # !tensorboard --logdir==training:training_log_path --host=127.0.0.1

# %%

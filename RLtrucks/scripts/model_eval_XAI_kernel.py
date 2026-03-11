# %% Import dependencies
"""
Created on June 19 22:15 2024
@author: Olga Ogorodnyk, olga.ogorodnyk@sintef.no
"""
import time
import pandas as pd

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

from shap import KernelExplainer, summary_plot, sample
import shap

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
#model = PPO.load(r'C:\Users\olgao\OneDrive - SINTEF\Skrivebord\PoP SEP XMANAI\ReLeVaMt2.0\output\run_00001\best_model\best_model.zip', env=env)
#model = PPO.load(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\run_00000\best_model\best_model.zip', env=env)

model = PPO.load(r'C:\Users\olgao\OneDrive - SINTEF\Skrivebord\PoP SEP XMANAI\ReLeVaMt2.0\saved_model.zip', env=env)


# %% Run environment with actions predicted by trained model
n_run_episodes = 20 #1000

print('Observation space:', env.observation_space)
print('Action space:', env.action_space)
print('-----------------------------------------')
testing_time_start = time.time()
observations = []
for episode in range(0, n_run_episodes):
    done = False
    while not done:
        action, state = model.predict(env.state)
        state, reward, done, truncated, info = env.step(action)
        observations.append(state)
    env.reset()
env.close()
testing_time_end = time.time()
print('-----------------------------------------')
print('Avg. time per test episode: ', formatSeconds((testing_time_end - testing_time_start) / n_run_episodes), '/ Avg. time per 100 test episodes: ', formatSeconds((testing_time_end - testing_time_start) / n_run_episodes * 100))

# %% Evaluate model
n_eval_episodes = 1 #5 # number of episodes to run for evaluation
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=n_eval_episodes)
mean_reward, std_reward


# %% Calculating SHAP values using KernelExplainer from SHAP library

# Convert to pandas dataframe
state_df = pd.DataFrame(observations, columns=["truck_capacity_kg", "truck_fuel_consumption[-1]", "truck_position_int", "length of available roads", "depots_n_packages[0]", "depots_weight_kg_packages[0]", "depots_n_packages[1]", "depots_weight_kg_packages[1]", "depots_n_packages[2]", "depots_weight_kg_packages[2]", "depots_n_packages[3]", "depots_weight_kg_packages[3]", "depots_n_packages[4]", "depots_weight_kg_packages[4]", "depots_n_packages[5]", "depots_weight_kg_packages[5]"])
#state_df = pd.DataFrame(observations, columns=["Truck position int", "Truck capacity kg", "Depots resultant angle deg", "Depots resultant magnitude"])
#state_df = pd.DataFrame(observations)

#print(model)
#print(state_df)

# Define a prediction function for the PPO model (this is needed to have a correct input to KernelExapliner)
def ppo_predict(data):
    return model.predict(data)[0]

# Initialize the SHAP explainer and calculate Shapley values
X = sample(state_df, 50)
explainer = KernelExplainer(ppo_predict, X)
#print(sample(state_df, 50))
shap_values = explainer.shap_values(X) # For summary plot
print(X, shap_values.size)

# Plot the results
summary_plot(shap_values, X)

shap_values_wf = explainer(X) # For waterfall plot - it outputs a different value type
print(f"length of shap_values: {len(shap_values_wf)} \n")
print(f"shape of elements within shap_values: {[i.shape for i in shap_values_wf]} \n")
shap.plots.waterfall(shap_values_wf[0])


#shap.dependence_plot(X_train_sample.columns.get_indexer(['monthly_subscr_amount']), shap_values[1], X_train_sample, interaction_index=False)
'''shap.force_plot(explainer.expected_value[1], # Note that we use the expected value of class [1] (defaulter) as a base value
                shap_values[1][j, :], # So we also want the SHAP vaues for class [1]
                X_train_sample.iloc[j, :], 
                matplotlib=True,
                text_rotation=20)'''

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# data all
data_all = pd.read_excel(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\random_1000_runs\all.xlsx', engine='openpyxl')

# data individual
data_random = pd.read_excel(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\random_1000_runs\episodes_stats.xlsx', engine='openpyxl')
data_rulebased = pd.read_excel(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\rulebased_1000_runs\episodes_stats.xlsx', engine='openpyxl')
data_rlagent = pd.read_excel(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\rl_GOOD_1000_runs\episodes_stats.xlsx', engine='openpyxl')
data_milkroute = pd.read_excel(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\milkroutes_1000_runs\episodes_stats.xlsx', engine='openpyxl')

# data training evolution
data_training = pd.read_excel(r'D:\Projects\ReLeVamt\ReLeVaMt\v3_RL_one_truck\output\RL_run_GOOD\episodes_stats.xlsx', engine='openpyxl')

# training evolution
plt.figure(figsize=(8, 6), dpi=150)
plt.plot(data_training.loc[:,'Episode reward'], color='green', label = 'RL')
plt.title('Training Evolution') 
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.legend(loc='lower right')
plt.grid()
plt.xlim((0, 1000))
plt.ylim((-1000, 1500))
plt.show()

# all
plt.figure(figsize=(8, 6), dpi=150)
plt.plot(data_all.loc[:,'Episode reward RL agent'], color='green', label = 'RL')
plt.plot(data_all.loc[:,'Episode reward milk routes'], color='red', label = 'Milk Route')
plt.plot(data_all.loc[:,'Episode reward rule based'], color='blue', label = 'Rule Based')
plt.plot(data_all.loc[:,'Episode reward random'], color='black', label = 'Random')
plt.title('Rewards Over 1000 Episodes') 
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.legend(loc='lower right')
plt.grid()
plt.xlim((0, 1000))
plt.ylim((-1000, 1500))
plt.show()

# without RL
plt.figure(figsize=(8, 6), dpi=150)
plt.plot(data_all.loc[:,'Episode reward milk routes'], color='red', label = 'Milk Route')
plt.plot(data_all.loc[:,'Episode reward rule based'], color='blue', label = 'Rule Based')
plt.plot(data_all.loc[:,'Episode reward random'], color='black', label = 'Random')
plt.title('Rewards Over 1000 Episodes') 
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.legend(loc='lower right')
plt.grid()
plt.xlim((0, 1000))
plt.ylim((-1000, 1500))
plt.show()

# RL vs milk route
plt.figure(figsize=(8, 6), dpi=150)
plt.plot(data_all.loc[:,'Episode reward RL agent'], color='green', label = 'RL')
plt.plot(data_all.loc[:,'Episode reward milk routes'], color='red', label = 'Milk Route')
plt.title('Rewards Over 1000 Episodes') 
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.legend(loc='lower right')
plt.grid()
plt.xlim((0, 1000))
plt.ylim((700, 1500))
plt.show()

# only random
plt.figure(figsize=(8, 6), dpi=150)
plt.plot(data_all.loc[:,'Episode reward random'], color='black', label = 'Random')
plt.title('Rewards Over 1000 Episodes') 
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.legend(loc='lower right')
plt.grid()
plt.xlim((0, 1000))
plt.ylim((-1000, 1500))
plt.show()

# random and milk routes
plt.figure(figsize=(8, 6), dpi=150)
plt.plot(data_all.loc[:,'Episode reward milk routes'], color='red', label = 'Milk Route')
plt.plot(data_all.loc[:,'Episode reward random'], color='black', label = 'Random')
plt.title('Rewards Over 1000 Episodes') 
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.legend(loc='lower right')
plt.grid()
plt.xlim((0, 1000))
plt.ylim((-1000, 1500))
plt.show()


# %% averages
# reward
avg_reward_random = data_random.loc[:,'Episode reward'].mean()
avg_reward_rulebased = data_rulebased.loc[:,'Episode reward'].mean()
avg_reward_rlagent = data_rlagent.loc[:,'Episode reward'].mean()
avg_reward_milkroute = data_milkroute.loc[:,'Episode reward'].mean()
print('avg reward random: ' + str(avg_reward_random))
print('avg reward rule based: ' + str(avg_reward_rulebased))
print('avg reward RL agent: ' + str(avg_reward_rlagent))
print('avg reward milk routes: ' + str(avg_reward_milkroute))
# packages
avg_packages_random = data_random.loc[:,'Episode packages delivered'].mean()
avg_packages_rulebased = data_rulebased.loc[:,'Episode packages delivered'].mean()
avg_packages_rlagent = data_rlagent.loc[:,'Episode packages delivered'].mean()
avg_packages_milkroute = data_milkroute.loc[:,'Episode packages delivered'].mean()
print('avg packages random: ' + str(avg_packages_random))
print('avg packages rule based: ' + str(avg_packages_rulebased))
print('avg packages RL agent: ' + str(avg_packages_rlagent))
print('avg packages milk routes: ' + str(avg_packages_milkroute))
# km
avg_km_random = data_random.loc[:,'Episode km driven'].mean()
avg_km_rulebased = data_rulebased.loc[:,'Episode km driven'].mean()
avg_km_rlagent = data_rlagent.loc[:,'Episode km driven'].mean()
avg_km_milkroute = data_milkroute.loc[:,'Episode km driven'].mean()
print('avg km random: ' + str(avg_km_random))
print('avg km rule based: ' + str(avg_km_rulebased))
print('avg km RL agent: ' + str(avg_km_rlagent))
print('avg km milk routes: ' + str(avg_km_milkroute))
# fuel
avg_fc_random = data_random.loc[:,'Episode fuel consumed'].mean()
avg_fc_rulebased = data_rulebased.loc[:,'Episode fuel consumed'].mean()
avg_fc_rlagent = data_rlagent.loc[:,'Episode fuel consumed'].mean()
avg_fc_milkroute = data_milkroute.loc[:,'Episode fuel consumed'].mean()
print('avg fuel random: ' + str(avg_fc_random))
print('avg fuel rule based: ' + str(avg_fc_rulebased))
print('avg fuel RL agent: ' + str(avg_fc_rlagent))
print('avg fuel milk routes: ' + str(avg_fc_milkroute))

# %%

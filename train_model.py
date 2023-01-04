import random
import stable_baselines3
from stable_baselines3 import PPO
import os
from connect_four_gym.env import C4Env, agent_by_color, check_game_status, after_action_state, to_color, next_color, get_dropped_loc
from stable_baselines3.common.env_checker import check_env
LOG_DIR = 'logs'
SAVE_DIR = 'models'




env = C4Env()
check_env(env)
# model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=LOG_DIR, learning_rate=0.001)
# TIMESTEPS=100000
# for i in range(30):
#     model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
#     model.save(f"{SAVE_DIR}/{TIMESTEPS*i}")
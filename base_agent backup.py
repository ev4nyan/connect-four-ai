#!/usr/bin/env python
import random
import stable_baselines3
from stable_baselines3 import PPO
import os
from connect_four_gym.env import C4Env, agent_by_color, check_game_status, after_action_state, to_color, next_color, get_dropped_loc


LOG_DIR = 'logs'
SAVE_DIR = 'models'




class BaseAgent(object):
    def __init__(self, color):
        self.color = color

    def act(self, state, ava_actions):
        for action in ava_actions:
            nstate = after_action_state(state, action)
            gstatus = check_game_status(nstate[0])
            if gstatus > 0:
                if to_color(gstatus) == self.color:
                    return action
        return random.choice(ava_actions)


def play(max_episode=10):
    start_color = 'O'
    env = C4Env()
    agents = [BaseAgent('O'),
              BaseAgent('X')]


    for _ in range(max_episode):
        env.set_start_color(start_color)
        state = env.reset()
        print(state)
        while not env.done:
            _, color = state
            env.show_turn(color, mode = 'developer')
            
            agent = agent_by_color(agents, color)
            ava_actions = env.available_actions()
            action = agent.act(state, ava_actions)
            state, reward, done, info = env.step(action)
            env.render(mode = 'developer')

        env.show_result(color, reward, mode = 'developer')

        # rotate start
        start_color = next_color(start_color)


if __name__ == '__main__':
    play()
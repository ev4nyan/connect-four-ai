import stable_baselines3
from stable_baselines3.common.env_util import make_vec_env

class MyMultiAgentEnv(stable_baselines3.common.env_util.MultiAgentEnv):
    def __init__(self):
        # Initialize the environment with two agents
        self.n_agents = 2
        self.agents = []
        self.agents.append(Agent1())
        self.agents.append(Agent2())
    
    def reset(self):
        # Reset the environment and the agents
        self.agents[0].reset()
        self.agents[1].reset()
        return self._get_obs()
    
    def step(self, action_n):
        # Step the environment and the agents
        self.agents[0].step(action_n[0])
        self.agents[1].step(action_n[1])
        return self._get_obs(), self._get_reward(), self._get_done(), self._get_info()
    
    def _get_obs(self):
        # Return the observations for each agent
        obs_n = []
        for agent in self.agents:
            obs_n.append(agent.get_observation())
        return obs_n
    
    def _get_reward(self):
        # Return the rewards for each agent
        reward_n = []
        for agent in self.agents:
            reward_n.append(agent.get_reward())
        return reward_n
    
    def _get_done(self):
        # Return the done flags for each agent
        done_n = []
        for agent in self.agents:
            done_n.append(agent.get_done())
        return done_n
    
    def _get_info(self):
        # Return the info for each agent
        info_n = []
        for agent in self.agents:
            info_n.append(agent.get_info())
        return info_n

# Create the environment
env = make_vec_env(lambda: MyMultiAgentEnv(), n_envs=1)


# Create the model
model = stable_baselines3.PPO('MlpPolicy', env)

# Train the model
model.learn(total_timesteps=10000)

# Test the model
obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()




--------------------------------------------------------------------------------------------------------------









def _learn(max_episode, epsilon, alpha, save_file):
    """Learn by episodes.
    Make two TD agent, and repeat self play for given episode count.
    Update state values as reward coming from the environment.
    Args:
        max_episode (int): Episode count.
        epsilon (float): Probability of exploration.
        alpha (float): Step size.
        save_file: File name to save result.
    """
    reset_state_values()

    env = TicTacToeEnv()
    agents = [TDAgent('O', epsilon, alpha),
              TDAgent('X', epsilon, alpha)]

    start_mark = 'O'
    for i in tqdm(range(max_episode)):
        episode = i + 1
        env.show_episode(False, episode)

        # reset agent for new episode
        for agent in agents:
            agent.episode_rate = episode / float(max_episode)

        env.set_start_mark(start_mark)
        state = env.reset()
        _, mark = state
        done = False
        while not done:
            agent = agent_by_mark(agents, mark)
            ava_actions = env.available_actions()
            env.show_turn(False, mark)
            action = agent.act(state, ava_actions)

            # update (no rendering)
            nstate, reward, done, info = env.step(action)
            agent.backup(state, nstate, reward)

            if done:
                env.show_result(False, mark, reward)
                # set terminal state value
                set_state_value(state, reward)

            _, mark = state = nstate

        # rotate start
        start_mark = next_mark(start_mark)

    # save states
    save_model(save_file, max_episode, epsilon, alpha)


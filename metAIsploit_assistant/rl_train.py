import gym
from metAIsploit_assistant.envs.msfconsole_env import MSFConsoleEnv
import numpy as np

# Simple random agent for demonstration
class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space
    def act(self, observation):
        return self.action_space.sample()

def train(num_episodes=5):
    env = MSFConsoleEnv()
    agent = RandomAgent(env.action_space)
    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        step_count = 0
        while not done and step_count < 10:
            action = agent.act(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            step_count += 1
            print(f"Episode {episode} Step {step_count}: Action={action}, Reward={reward}, Info={info}")
        print(f"Episode {episode} finished with total reward {total_reward}")
    env.close()

if __name__ == "__main__":
    train()

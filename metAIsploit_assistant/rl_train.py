import gymnasium as gym
from metAIsploit_assistant.envs.msfconsole_env import MSFConsoleEnv
import numpy as np
from metAIsploit_assistant.utilities.tensorboard_logger import TensorboardLogger
from metAIsploit_assistant.utilities.structured_logger import StructuredLogger
from metAIsploit_assistant.utilities.replay_buffer import ReplayBuffer

# Simple random agent for demonstration
class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space
    def act(self, observation):
        return self.action_space.sample()

def train(num_episodes=5):
    env = MSFConsoleEnv()
    agent = RandomAgent(env.action_space)
    tb_logger = TensorboardLogger(log_dir="runs")
    structured_logger = StructuredLogger(log_dir="logs", log_prefix="rl_episode")
    replay_buffer = ReplayBuffer(capacity=10000)
    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        step_count = 0
        structured_logger.new_episode()
        while not done and step_count < 10:
            action = agent.act(obs)
            next_obs, reward, done, info = env.step(action)
            # Logging and replay buffer
            step_log = {
                "episode": episode,
                "step": step_count,
                "action": action,
                "reward": reward,
                "info": info,
                "state": obs.tolist() if hasattr(obs, 'tolist') else obs,
                "next_state": next_obs.tolist() if hasattr(next_obs, 'tolist') else next_obs,
                "done": done,
            }
            structured_logger.log(step_log)
            replay_buffer.push(obs, action, reward, next_obs, done, info)
            obs = next_obs
            total_reward += reward
            tb_logger.log_scalar("reward", reward, step_count + episode * 10)
            if "reward_details" in info:
                for k, v in info["reward_details"].items():
                    tb_logger.log_scalar(f"reward_details/{k}", v, step_count + episode * 10)
            step_count += 1
            print(f"Episode {episode} Step {step_count}: Action={action}, Reward={reward}, Info={info}")
        tb_logger.log_scalar("episode_return", total_reward, episode)
        tb_logger.log_scalar("episode_steps", step_count, episode)
        structured_logger.log({"episode": episode, "total_reward": total_reward, "steps": step_count})
        print(f"Episode {episode} finished with total reward {total_reward}")
    tb_logger.close()
    env.close()

if __name__ == "__main__":
    train()

import gym
from gym import spaces
import numpy as np
from metAIsploit_assistant.utilities.executor import MetasploitExecutor

class MSFConsoleEnv(gym.Env):
    """
    OpenAI Gym environment for interacting with msfconsole via RPC.
    This environment is intended to be sandboxed and safe for RL agent training.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, host='metasploit', port=55552, user='msf', password='Meta2025SecurePass', target_ip='172.18.0.100'):
        super(MSFConsoleEnv, self).__init__()
        # Example actions: 0 = scan, 1 = exploit, 2 = get session, 3 = run custom command, 4 = noop
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=0, high=1, shape=(128,), dtype=np.float32)
        self.state = np.zeros(128, dtype=np.float32)
        self.done = False
        self.target_ip = target_ip  # Vulnerable web app target
        self.executor = MetasploitExecutor(host=host, port=port, user=user, password=password, connect_on_init=True)

    def step(self, action):
        # Map discrete action to msfconsole command
        if action == 0:
            cmd = f'db_nmap -Pn {self.target_ip}'
        elif action == 1:
            cmd = f'use exploit/unix/webapp/phpmyadmin_unauth_access; set RHOSTS {self.target_ip}; run'
        elif action == 2:
            cmd = 'sessions -l'
        elif action == 3:
            cmd = f'run custom'
        else:
            cmd = ''  # noop
        if cmd:
            success, output, error = self.executor.execute_command(cmd)
        else:
            success, output, error = True, '', None
        # Simple reward: +1 for success, 0 otherwise
        reward = 1.0 if success else 0.0
        # Observation: basic embedding (placeholder)
        self.state = np.random.rand(128).astype(np.float32)
        self.done = False  # Could set to True if session is obtained or exploit succeeds
        info = {'output': output, 'error': error}
        return self.state, reward, self.done, info

    def reset(self):
        # Optionally: Restart msfconsole or reset environment state
        self.state = np.zeros(128, dtype=np.float32)
        self.done = False
        return self.state

    def render(self, mode='human'):
        print(f"Current state: {self.state}")

    def close(self):
        # TODO: Cleanup msfconsole session
        pass

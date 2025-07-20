from collections import deque
from typing import Any, Deque, Tuple
import random

class ReplayBuffer:
    def __init__(self, capacity: int = 10000):
        self.buffer: Deque[Tuple[Any, ...]] = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done, info=None):
        self.buffer.append((state, action, reward, next_state, done, info))

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        return map(list, zip(*batch))

    def __len__(self):
        return len(self.buffer)

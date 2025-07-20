import json
import os
from datetime import datetime
import numpy as np

def to_serializable(val):
    if isinstance(val, (np.integer, np.int32, np.int64)):
        return int(val)
    if isinstance(val, (np.floating, np.float32, np.float64)):
        return float(val)
    if isinstance(val, np.ndarray):
        return val.tolist()
    return val

def convert_all(obj):
    if isinstance(obj, dict):
        return {k: convert_all(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_all(v) for v in obj]
    return to_serializable(obj)

class StructuredLogger:
    def __init__(self, log_dir="logs", log_prefix="rl_episode"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir
        self.log_prefix = log_prefix
        self.episode = 0
        self.log_file = None
        self._open_new_log()

    def _open_new_log(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(
            self.log_dir, f"{self.log_prefix}_{self.episode}_{timestamp}.jsonl"
        )
        self.episode += 1

    def log(self, data: dict):
        serializable_data = convert_all(data)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(serializable_data) + "\n")

    def new_episode(self):
        self._open_new_log()

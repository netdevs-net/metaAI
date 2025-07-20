from torch.utils.tensorboard import SummaryWriter
import os
from datetime import datetime

class TensorboardLogger:
    def __init__(self, log_dir="runs"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.writer = SummaryWriter(log_dir=os.path.join(log_dir, timestamp))

    def log_scalar(self, tag, value, step):
        self.writer.add_scalar(tag, value, step)

    def close(self):
        self.writer.close()

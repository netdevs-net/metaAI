#!/bin/bash
# Launch TensorBoard for RL training logs

# Usage: bash scripts/run_tensorboard.sh

TB_LOGDIR=${1:-runs}
TB_PORT=${2:-6006}

# Use poetry if available, fallback to system tensorboard
if command -v poetry &> /dev/null; then
    echo "[INFO] Launching TensorBoard via Poetry..."
    poetry run tensorboard --logdir "$TB_LOGDIR" --host 0.0.0.0 --port "$TB_PORT"
else
    echo "[INFO] Launching system TensorBoard..."
    tensorboard --logdir "$TB_LOGDIR" --host 0.0.0.0 --port "$TB_PORT"
fi

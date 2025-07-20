#!/bin/bash
# Docker startup script for MetAIsploit Assistant
# Poetry is installed and dependencies are up to date from Dockerfile build.

set -e

echo "Starting MetAIsploit Assistant..."

# Ensure models directory exists
mkdir -p /app/models

# Check if models are available, if not try to download
if [ ! "$(ls -A /app/models)" ]; then
    echo "No models found, attempting to download..."
    poetry run init || echo "Model download failed, continuing..."
fi

# Default to chat mode, but allow override via CMD
if [ $# -eq 0 ]; then
    echo "Starting interactive chat mode..."
    exec poetry run chat
else
    echo "Running custom command: $@"
    exec poetry run "$@"
fi

#!/bin/bash
# Docker startup script for MetAIsploit Assistant
# Poetry is installed and dependencies are up to date from Dockerfile build.

set -e

echo "Starting MetAIsploit Assistant..."

# Ensure models directory exists
mkdir -p /app/models

# Initialize database service
if [ ! -f "/root/.msf4/initialized" ]; then
    echo "Initializing Metasploit database..."
    mkdir -p /root/.msf4
    touch /root/.msf4/initialized
    
    # Wait for database to be ready
    echo "Waiting for database to be ready..."
    until PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h db -U $POSTGRES_USER -d $POSTGRES_DB; do
        echo "Waiting for database..."
        sleep 2
    done
    
    # Initialize database
    echo "Running database initialization..."
    cd /usr/src/metasploit-framework
    ./msfconsole -q -x "db_connect ${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}; exit"
    echo "Database initialization complete"
fi

# Check if models are available, if not try to download
if [ ! "$(ls -A /app/models)" ]; then
    echo "No models found, attempting to download..."
    poetry run init || echo "Model download failed, continuing..."
fi

# Start the database service
echo "Starting Metasploit database service..."
service metasploit-db start

# Wait for database service to be ready
echo "Waiting for database service to be ready..."
sleep 5

# Default to chat mode, but allow override via CMD
if [ $# -eq 0 ]; then
    echo "Starting interactive chat mode..."
    exec poetry run chat
else
    echo "Running custom command: $@"
    exec poetry run "$@"
fi

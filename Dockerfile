# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Poetry install
# Install the latest version of Poetry for bleeding-edge features and fixes.
RUN pip install --upgrade poetry

# Set workdir
WORKDIR /app

# Copy pyproject and poetry.lock first for caching
COPY pyproject.toml poetry.lock ./

# Copy all code (including README.md) before installing
COPY . .

# Install nmap for network scanning
RUN apt-get update && apt-get install -y nmap && rm -rf /var/lib/apt/lists/*

# Install all dependencies in one step, including latest langchain-community and llama-cpp-python
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    --mount=type=cache,target=/root/.cache/pip \
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip install --no-cache-dir llama-cpp-python

# Copy the rest of the code
COPY . .

# Create models directory and set permissions
RUN mkdir -p /app/models && chmod 755 /app/models

# Environment variables
ENV PYTHONPATH=/app
ENV METASPLOIT_ROOT=/opt/metasploit-framework
ENV GPT4ALL_MODEL_PATH=/app/models

# Models will be downloaded on first run and persisted via volume mount

# Make startup script executable
RUN chmod +x startup.sh

# Expose port for potential web interface
EXPOSE 8080

# Use startup script as entrypoint
ENTRYPOINT ["./startup.sh"]

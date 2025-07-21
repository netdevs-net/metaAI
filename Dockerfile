# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# --- Install system dependencies and Poetry early for caching ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    nmap \
    postgresql \
    postgresql-client \
    libpq-dev \
    expect \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (cached unless version changes)
RUN pip install --upgrade poetry

# Set workdir
WORKDIR /app

# --- Copy only dependency files first for maximum cache utilization ---
COPY pyproject.toml poetry.lock ./
# Ensure README.md is present for Poetry install
COPY README.md ./
# Copy the main package so poetry install works
COPY metAIsploit_assistant ./metAIsploit_assistant

# --- Install Python dependencies; this layer is cached unless deps change ---
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    --mount=type=cache,target=/root/.cache/pip \
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip install --no-cache-dir llama-cpp-python

# --- Now copy the rest of the application code ---
COPY . .

# Create models directory and set permissions (idempotent)
RUN mkdir -p /app/models && chmod 755 /app/models

# --- End of Dockerfile ---
# Best practices:
# - Poetry and dependencies are cached unless pyproject.toml/poetry.lock changes
# - Source code changes do not trigger full dependency reinstall
# - nmap and all system deps installed in one layer for cache efficiency

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

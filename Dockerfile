# syntax=docker/dockerfile:1
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Poetry install
ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"

# Set workdir
WORKDIR /app

# Copy pyproject and poetry.lock first for caching
COPY pyproject.toml poetry.lock ./

# Install dependencies and project
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy the rest of the code
COPY . .

# Reinstall the project to ensure entry points are properly registered
RUN poetry install --no-interaction --no-ansi

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

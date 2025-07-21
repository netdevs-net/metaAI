# syntax=docker/dockerfile:1.4
FROM metasploit-base:latest

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
    && pip install --no-cache-dir llama-cpp-python psycopg2-binary

# --- Now copy the rest of the application code ---
# Copy the rest of the application
COPY . .

# Ensure directories exist and set permissions
RUN mkdir -p /app/docker && \
    mkdir -p /app/models && \
    chmod +x /app/docker/entrypoint.sh && \
    chmod 755 /app/models

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

# Make scripts executable
RUN chmod +x startup.sh scripts/metasploit_db_service.py

# Set up systemd service for database connection
RUN mkdir -p /etc/systemd/system/
COPY docker/metasploit-db.service /etc/systemd/system/
RUN systemctl enable metasploit-db.service

# Create log directory for the service
RUN mkdir -p /var/log/metasploit && \
    chmod 755 /var/log/metasploit

# Expose port for potential web interface
EXPOSE 8080

# Use startup script as entrypoint
ENTRYPOINT ["/bin/bash", "-c", "systemctl start metasploit-db && ./startup.sh"]

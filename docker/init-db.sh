#!/bin/bash
set -e

# Wait for Postgres to be ready
until nc -z db 5432; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# Create .msf4 directory if it doesn't exist
mkdir -p /root/.msf4

# Initialize the database connection
echo "Initializing Metasploit database..."
/usr/src/metasploit-framework/msfconsole -q -x "db_connect postgresql://msf:Meta2025SecurePass@db:5432/msf; save; exit"

# Start the main process
exec "$@"

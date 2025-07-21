#!/bin/bash
set -e

echo "[+] Starting Metasploit container"

# Wait for Postgres to be ready
MAX_RETRIES=30
COUNTER=0
until pg_isready -h db -U $POSTGRES_USER -d $POSTGRES_DB || [ $COUNTER -eq $MAX_RETRIES ]; do
  echo "[!] Waiting for Postgres at db:5432... (attempt $((COUNTER+1))/$MAX_RETRIES)"
  sleep 2
  COUNTER=$((COUNTER+1))
done
if [ $COUNTER -eq $MAX_RETRIES ]; then
  echo "[!] ERROR: Failed to connect to Postgres after $MAX_RETRIES attempts"
  exit 1
fi





# Start msfconsole with the main RC file (msgrpc handles RPC)
echo "[+] Starting msfconsole with msgrpc..."
exec msfconsole -r /app/docker/msfconsole.rc

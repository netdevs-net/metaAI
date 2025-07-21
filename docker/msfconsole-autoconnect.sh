#!/bin/bash
set -e

# Wait for Postgres to be ready
until nc -z db 5432; do
  echo "Waiting for Postgres at db:5432..."
  sleep 2
done

while true; do
  # Try to connect to DB and check status
  /usr/src/metasploit-framework/msfconsole -x "db_connect postgresql://msf:Meta2025SecurePass@db:5432/msf; db_status; exit" | grep 'Connection type: postgresql'
  if [ $? -eq 0 ]; then
    echo "Metasploit DB connected!"
    break
  else
    echo "Retrying Metasploit DB connect..."
    sleep 2
  fi
done

# Now start msfconsole interactively, DB will be connected
exec /usr/src/metasploit-framework/msfconsole

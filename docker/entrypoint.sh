#!/bin/bash
set -e

# Wait for Postgres to be ready
until nc -z db 5432; do
  echo "Waiting for Postgres at db:5432..."
  sleep 2
done

# Start msfconsole with RC file
exec /usr/src/metasploit-framework/msfconsole -r /usr/src/metasploit-framework/docker/msfconsole-dbconnect.rc

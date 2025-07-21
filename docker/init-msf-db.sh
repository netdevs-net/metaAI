#!/bin/bash
set -e

# Create .msf4 directory if it doesn't exist
mkdir -p /root/.msf4

# Create database.yml with the correct connection details
cat > /root/.msf4/config <<EOL
---
framework:
  database:
    adapter: postgresql
    database: msf
    username: msf
    password: Meta2025SecurePass
    host: db
    port: 5432
    pool: 200
    timeout: 5
EOL

echo "Metasploit database configuration created successfully"

# Start the main process
exec "$@"

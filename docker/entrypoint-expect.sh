#!/usr/bin/expect -f
set timeout 60

# Wait for DB to be ready
spawn bash -c {until nc -z db 5432; do echo "Waiting for Postgres..."; sleep 2; done}
expect "Postgres..."

# Start msfconsole with the rc file
spawn /usr/src/metasploit-framework/msfconsole -r /usr/src/metasploit-framework/docker/msfconsole.rc
expect {
    "Connection type: postgresql" {
        send_user "DB connected via rc file!\n"
    }
    "postgresql selected, no connection" {
        send_user "DB not connected, trying manual connect...\n"
        send "db_connect postgresql://msf:Meta2025SecurePass@db:5432/msf\r"
        expect "Connection type: postgresql" {
            send_user "DB connected manually!\n"
            # Save the connection for future sessions
            send "save\r"
            expect "Configuration saved"
            send_user "Configuration saved for future sessions\n"
        }
    }
    timeout {
        send_user "Failed to connect to DB!\n"
        exit 1
    }
}

# Keep the container running
interact

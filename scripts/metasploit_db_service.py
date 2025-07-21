#!/usr/bin/env python3
"""
Metasploit Database Connection Service

This service ensures Metasploit maintains a persistent database connection.
It runs in the background and automatically reconnects if the connection is lost.
"""

import os
import time
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/var/log/metasploit/db_service.log')
    ]
)
logger = logging.getLogger('metasploit_db_service')

class MetasploitDBService:
    def __init__(self):
        self.msf_path = "/usr/src/metasploit-framework"
        self.msf_console = os.path.join(self.msf_path, "msfconsole")
        self.db_config = {
            'adapter': 'postgresql',
            'database': os.getenv('POSTGRES_DB', 'msf'),
            'username': os.getenv('POSTGRES_USER', 'msf'),
            'password': os.getenv('POSTGRES_PASSWORD', 'Meta2025SecurePass'),
            'host': os.getenv('POSTGRES_HOST', 'db'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'pool': '200',
            'timeout': '5'
        }
        self.ensure_config()

    def ensure_config(self):
        """Ensure the database configuration file exists with correct permissions"""
        config_dir = Path("/root/.msf4")
        config_dir.mkdir(exist_ok=True, mode=0o700)
        
        config_file = config_dir / "database.yml"
        config_content = f"""production:
  adapter: {self.db_config['adapter']}
  database: {self.db_config['database']}
  username: {self.db_config['username']}
  password: {self.db_config['password']}
  host: {self.db_config['host']}
  port: {self.db_config['port']}
  pool: {self.db_config['pool']}
  timeout: {self.db_config['timeout']}
"""
        config_file.write_text(config_content)
        config_file.chmod(0o600)
        logger.info("Database configuration file updated")

    def check_db_connection(self):
        """Check if the database connection is active"""
        try:
            cmd = [
                self.msf_console,
                '-x',
                'db_status; exit'
            ]
            result = subprocess.run(
                cmd,
                cwd=self.msf_path,
                capture_output=True,
                text=True
            )
            return "postgresql connected" in result.stdout.lower()
        except Exception as e:
            logger.error(f"Error checking database connection: {e}")
            return False

    def reconnect_db(self):
        """Reconnect to the database"""
        try:
            cmd = [
                self.msf_console,
                '-x',
                f'db_connect {self.db_config["username"]}:{self.db_config["password"]}@' \
                f'{self.db_config["host"]}:{self.db_config["port"]}/{self.db_config["database"]}; exit'
            ]
            subprocess.run(
                cmd,
                cwd=self.msf_path,
                capture_output=True,
                text=True
            )
            logger.info("Attempted to reconnect to the database")
        except Exception as e:
            logger.error(f"Error reconnecting to database: {e}")

    def run(self):
        """Run the database connection service"""
        logger.info("Starting Metasploit Database Connection Service")
        
        while True:
            if not self.check_db_connection():
                logger.warning("Database connection lost, attempting to reconnect...")
                self.reconnect_db()
                
                # Verify reconnection
                if not self.check_db_connection():
                    logger.error("Failed to reconnect to database")
                else:
                    logger.info("Successfully reconnected to database")
            
            # Check connection every 30 seconds
            time.sleep(30)

if __name__ == "__main__":
    # Ensure log directory exists
    Path("/var/log/metasploit").mkdir(exist_ok=True, mode=0o755)
    
    service = MetasploitDBService()
    service.run()

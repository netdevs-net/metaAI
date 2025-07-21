#!/usr/bin/env python3
"""
Optimized Metasploit RPC Client

A high-performance client for interacting with Metasploit's RPC interface.
Uses connection pooling and caching for better performance.
"""

import os
import time
import logging
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union
from pymetasploit3.msfrpc import MsfRpcClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('msf_client')

class MSFClient:
    """High-performance Metasploit RPC client with caching and connection pooling."""
    
    _instance = None
    _client = None
    _last_used = 0
    _connection_timeout = 300  # 5 minutes
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MSFClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the client with environment variables."""
        self.host = os.getenv('MSF_HOST', 'metasploit')
        self.port = int(os.getenv('MSF_PORT', '55552'))
        self.username = os.getenv('MSF_USER', 'msf')
        self.password = os.getenv('MSGRPC_PASS', 'Meta2025SecurePass')
        self.ssl = os.getenv('MSF_SSL', 'false').lower() == 'true'
        self._connect()
    
    def _connect(self):
        """Establish a new connection to the Metasploit RPC server."""
        try:
            self._client = MsfRpcClient(
                self.password,
                server=self.host,
                port=self.port,
                username=self.username,
                ssl=self.ssl
            )
            self._last_used = time.time()
            logger.info(f"Connected to Metasploit RPC at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to Metasploit RPC: {e}")
            raise
    
    def _ensure_connection(self):
        """Ensure we have a valid connection, reconnecting if necessary."""
        now = time.time()
        if (self._client is None or 
            (now - self._last_used > self._connection_timeout)):
            self._connect()
        self._last_used = now
        return self._client
    
    @property
    def client(self) -> MsfRpcClient:
        """Get the RPC client, ensuring the connection is fresh."""
        return self._ensure_connection()
    
    @lru_cache(maxsize=128)
    def get_module_info(self, module_type: str, module_name: str) -> Dict[str, Any]:
        """Get information about a module with caching."""
        try:
            return self.client.modules.use(module_type, module_name)
        except Exception as e:
            logger.error(f"Error getting module {module_type}/{module_name}: {e}")
            raise
    
    def execute_module(
        self, 
        module_type: str, 
        module_name: str, 
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a module with the given options."""
        try:
            module = self.get_module_info(module_type, module_name)
            for key, value in options.items():
                module[key] = value
            return module.execute()
        except Exception as e:
            logger.error(f"Error executing {module_type}/{module_name}: {e}")
            raise
    
    def search_modules(self, query: str) -> List[Dict[str, str]]:
        """Search for modules matching the query."""
        try:
            return self.client.modules.search(query)
        except Exception as e:
            logger.error(f"Error searching modules: {e}")
            raise

# Global instance for easy import
msf = MSFClient()

def main():
    """Example usage of the optimized MSF client."""
    try:
        # Example: List first 5 exploit modules
        print("Available exploit modules (first 5):")
        print(msf.client.modules.exploits[:5])
        
        # Example: Search for SSH modules
        print("\nSSH-related modules:")
        ssh_modules = msf.search_modules('ssh')
        for i, mod in enumerate(ssh_modules[:5], 1):
            print(f"{i}. {mod['name']} - {mod.get('description', 'No description')}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main()

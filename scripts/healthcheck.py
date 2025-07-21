#!/usr/bin/env python3
"""Health check script for Metasploit RPC service."""

import os
import sys
from pymetasploit3.msfrpc import MsfRpcError

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the msf_manager from chat.py
try:
    from metAIsploit_assistant.actions.chat import msf_manager
    
    # Test the connection
    if msf_manager.check_connection():
        print("Metasploit RPC is healthy")
        sys.exit(0)
    else:
        print("Metasploit RPC is not responding")
        sys.exit(1)
        
except MsfRpcError as e:
    print(f"Metasploit RPC error: {e}")
    sys.exit(1)
    
except Exception as e:
    print(f"Health check failed: {e}")
    sys.exit(1)

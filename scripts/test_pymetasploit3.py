#!/usr/bin/env python3

import os
import sys
from metAIsploit_assistant.actions.chat import msf_manager, handle_rpc_errors

def test_metasploit_connection():
    """Test the Metasploit RPC connection and list available modules."""
    print("\n=== Testing Metasploit RPC Connection ===")
    
    # Get the client from the manager
    client = msf_manager.client
    
    if not client:
        print("[ERROR] Failed to initialize Metasploit RPC client")
        return False
    
    # Test the connection
    try:
        # Get Metasploit version
        version = client.call('core.version')
        print(f"[SUCCESS] Connected to Metasploit RPC (Version: {version})")
        
        # List available modules
        print("\n[INFO] Available module types:")
        for mod_type in client.call('module.types'):
            count = len(client.call('module.list', mod_type))
            print(f"  - {mod_type}: {count} modules")
        
        # Show first 5 exploits as an example
        print("\n[INFO] First 5 exploit modules:")
        exploits = client.modules.exploits[:5]
        for i, exploit in enumerate(exploits, 1):
            print(f"  {i}. {exploit}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to communicate with Metasploit: {e}")
        return False

if __name__ == "__main__":
    # Add parent directory to path for module imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run the test
    success = test_metasploit_connection()
    sys.exit(0 if success else 1)

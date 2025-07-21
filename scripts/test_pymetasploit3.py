import os
from pymetasploit3.msfrpc import MsfRpcClient

# Use environment variable for password (default: changeme)
password = os.environ.get('MSGRPC_PASS', 'Meta2025SecurePass')
client = MsfRpcClient(password, server='metasploit', port=55552, username='msf')

print("[INFO] Connected to Metasploit RPC!")
print("[INFO] Available exploit modules (first 5):")
print(client.modules.exploits[:5])

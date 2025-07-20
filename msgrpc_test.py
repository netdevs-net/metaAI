from pymetasploit3.msfrpc import MsfRpcClient
import logging

logging.basicConfig(level=logging.INFO)

HOST = 'metasploit'
PORT = 55552
USER = 'msf'
PASS = 'Meta2025SecurePass'

try:
    print(f"Attempting to connect to msgrpc at {HOST}:{PORT} with user={USER} and pass={PASS}")
    client = MsfRpcClient(password=PASS, username=USER, port=PORT, server=HOST)
    print("SUCCESS: Connected to Metasploit RPC!")
    print(f"Auth token: {client.auth_token}")
    print(f"Server version: {client.call('core.version')}")
except Exception as e:
    print(f"ERROR: {e}")

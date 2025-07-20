from pymetasploit3.msfrpc import MsfRpcClient
print('Connecting...')
client = MsfRpcClient(password='Meta2025SecurePass', username='msf', port=55552, server='metasploit')
print('Connected!')

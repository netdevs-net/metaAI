from pymetasploit3.msfrpc import MsfRpcClient
print('Connecting...')
client = MsfRpcClient(password='CHANGEME-local-lab-only', username='msf', port=55552, server='metasploit')
print('Connected!')

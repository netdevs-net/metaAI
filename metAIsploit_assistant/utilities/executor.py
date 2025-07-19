import logging
from typing import Optional, Tuple
from pymetasploit3.msfrpc import MsfRpcClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetasploitExecutor:
    def __init__(self, host='127.0.0.1', port=55552, user='msf', password='msf'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = MsfRpcClient(
                password=self.password, username=self.user, port=self.port, server=self.host
            )
            logger.info(f"Connected to Metasploit RPC at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to Metasploit RPC: {e}")
            self.client = None

    def is_safe_command(self, command: str) -> Tuple[bool, str]:
        blocked = ['rm -rf', 'format', 'del /f', 'shutdown', 'reboot', 'halt']
        for b in blocked:
            if b in command.lower():
                return False, f"Blocked dangerous command: {b}"
        return True, "OK"

    def execute_command(self, command: str, timeout: int = 30) -> Tuple[bool, str, Optional[str]]:
        if not self.client:
            self.connect()
            if not self.client:
                return False, '', 'Could not connect to Metasploit RPC.'
        safe, reason = self.is_safe_command(command)
        if not safe:
            return False, '', reason
        try:
            console = self.client.consoles.console()
            console.write(command)
            output = ''
            import time
            elapsed = 0
            while elapsed < timeout:
                time.sleep(0.5)
                res = console.read()
                if res['data']:
                    output += res['data']
                if res['prompt'] and not res['busy']:
                    break
                elapsed += 0.5
            console.destroy()
            return True, output, None
        except Exception as e:
            return False, '', str(e)

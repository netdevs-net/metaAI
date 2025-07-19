import subprocess
import json
import os
import time
from typing import List, Dict, Any

def run_command_with_timeout(command: str, timeout: int) -> Dict[str, Any]:
    try:
        start = time.time()
        proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        duration = time.time() - start
        return {
            'success': proc.returncode == 0,
            'stdout': proc.stdout,
            'stderr': proc.stderr,
            'returncode': proc.returncode,
            'duration': duration
        }
    except subprocess.TimeoutExpired as e:
        return {
            'success': False,
            'stdout': e.stdout or '',
            'stderr': f'Timeout after {timeout}s',
            'returncode': -1,
            'duration': timeout
        }

def load_pipeline(json_path: str) -> List[Dict[str, Any]]:
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data['recon_pipeline']

def parse_nmap_ports(nmap_grepable_output: str) -> Dict[str, List[int]]:
    # Very basic parser for open ports from nmap -oG output
    ports = {'web': [], 'ssl': []}
    for line in nmap_grepable_output.splitlines():
        if '/open/' in line:
            if 'http' in line or 'https' in line:
                for part in line.split():
                    if '/open/' in part:
                        port = int(part.split('/')[0])
                        if 'https' in line or port in [443, 8443]:
                            ports['ssl'].append(port)
                        else:
                            ports['web'].append(port)
    return ports

def substitute_ports(command: str, web_ports: List[int], ssl_ports: List[int]) -> str:
    cmd = command.replace('<web_ports>', ','.join(str(p) for p in web_ports or [80,8080]))
    cmd = cmd.replace('<ssl_ports>', ','.join(str(p) for p in ssl_ports or [443,8443]))
    return cmd

def run_recon_pipeline(json_path: str, target_ip: str, output_dir: str = './recon_output'):
    os.makedirs(output_dir, exist_ok=True)
    pipeline = load_pipeline(json_path)
    web_ports = []
    ssl_ports = []
    for step in pipeline:
        print(f"[+] Step {step['step']}: {step['name']}")
        cmd = step['command'].replace('<target_ip>', target_ip)
        if '<web_ports>' in cmd or '<ssl_ports>' in cmd:
            # Try to load previous nmap output for port info
            grepable_path = os.path.join(output_dir, 'nmap_initial.gnmap')
            if os.path.exists(grepable_path):
                with open(grepable_path) as f:
                    port_info = parse_nmap_ports(f.read())
                    web_ports = port_info['web']
                    ssl_ports = port_info['ssl']
            cmd = substitute_ports(cmd, web_ports, ssl_ports)
        out_file = os.path.join(output_dir, f"step{step['step']}_{step['name'].replace(' ','_')}.txt")
        result = run_command_with_timeout(cmd, step['timeout_seconds'])
        with open(out_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"    Command: {cmd}")
        print(f"    Success: {result['success']} | Duration: {result['duration']:.1f}s")
        if not result['success']:
            print(f"    Error: {result['stderr']}")
    print(f"[+] Recon pipeline complete. Output in {output_dir}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automate recon pipeline using nmap and JSON plan.")
    parser.add_argument("plan", help="Path to JSON file with recon_pipeline definition.")
    parser.add_argument("target", help="Target IP or hostname.")
    parser.add_argument("--output", default="./recon_output", help="Output directory (default: ./recon_output)")
    args = parser.parse_args()
    run_recon_pipeline(args.plan, args.target, args.output)

import re
from typing import Dict, Optional

def compute_reward(output: str, error: Optional[str], action: int, elapsed_time: float = None) -> Dict[str, float]:
    """
    Compute reward components for RL agent based on msfconsole output and execution time.
    Returns a dict with keys: 'success', 'impact', 'stealth', 'precision', 'speed', 'total'.
    Speed is measured as a positive reward for faster actions (inverse of elapsed_time).
    """
    reward = {
        'success': 0.0,
        'impact': 0.0,
        'stealth': 0.0,
        'precision': 0.0,
        'speed': 0.0,
        'total': 0.0,
    }
    # 1. Success: Did the command succeed?
    if error is None and output:
        reward['success'] = 1.0
    # 2. Impact: Did we get a session or exploit succeed?
    if re.search(r"Meterpreter session|Command shell session|Session [0-9]+ opened", output):
        reward['impact'] = 2.0
    elif re.search(r"Exploit completed|Successful login|Vulnerable", output):
        reward['impact'] = 1.0
    # 3. Stealth: Penalize for noisy or obvious scans/exploits
    if action == 0 and ("-T5" in output or "Aggressive Scan" in output):
        reward['stealth'] = -0.5  # Aggressive scan
    elif action == 0 and ("-T3" in output or "Stealth Scan" in output):
        reward['stealth'] = 0.2   # Stealth scan
    else:
        reward['stealth'] = 0.0
    # 4. Precision: Reward for targeted, non-broadcast actions
    if action == 0 and 'scan' in output and 'open' in output:
        open_ports = re.findall(r"([0-9]+)/tcp\s+open", output)
        if open_ports and len(open_ports) < 10:
            reward['precision'] = 0.5  # Targeted scan
        elif open_ports and len(open_ports) >= 10:
            reward['precision'] = -0.2  # Too broad
    elif action == 1 and 'exploit' in output:
        reward['precision'] = 0.5
    # 5. Speed: Reward faster actions (lower elapsed_time)
    if elapsed_time is not None and elapsed_time > 0:
        reward['speed'] = min(1.0, 2.0 / elapsed_time)  # Cap at 1.0, scale for RL
    else:
        reward['speed'] = 0.0
    # 6. Total: Weighted sum (tune as needed)
    reward['total'] = (
        reward['success']
        + reward['impact']
        + reward['stealth']
        + reward['precision']
        + reward['speed']
    )
    return reward

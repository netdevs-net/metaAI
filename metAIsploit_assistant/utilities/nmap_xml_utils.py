import xml.etree.ElementTree as ET
from typing import List, Dict

def parse_nmap_xml(xml_path: str) -> Dict:
    """Parse nmap XML and return a summary dict of hosts, open ports, and services."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    hosts = []
    for host in root.findall('host'):
        status = host.find('status').get('state')
        if status != 'up':
            continue
        addr = host.find('address').get('addr')
        ports = []
        for port in host.findall('.//port'):
            portid = port.get('portid')
            protocol = port.get('protocol')
            state = port.find('state').get('state')
            service = port.find('service').get('name') if port.find('service') is not None else None
            if state == 'open':
                ports.append({'port': portid, 'protocol': protocol, 'service': service})
        hosts.append({'address': addr, 'open_ports': ports})
    return {'hosts': hosts}


def summarize_nmap_findings(parsed: Dict) -> str:
    """Format a summary of nmap findings for LLM prompt input."""
    summary = []
    for host in parsed['hosts']:
        summary.append(f"Host {host['address']} has open ports:")
        for port in host['open_ports']:
            summary.append(f"  - {port['port']}/{port['protocol']} ({port['service']})")
    return '\n'.join(summary) if summary else 'No live hosts or open ports found.'

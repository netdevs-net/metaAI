#!/usr/bin/env python3
"""
Automated script to find possible origin IPs behind Cloudflare using crt.sh and DNS resolution.
- Queries crt.sh for all certificates for a domain
- Extracts all subdomains
- Resolves each subdomain to its IP(s)
- Filters out Cloudflare IPs using the official IP ranges
"""
import requests
import socket
import ipaddress

CLOUDFLARE_IPV4 = requests.get('https://www.cloudflare.com/ips-v4').text.splitlines()
CLOUDFLARE_IPV6 = requests.get('https://www.cloudflare.com/ips-v6').text.splitlines()
CLOUDFLARE_NETS = [ipaddress.ip_network(cidr) for cidr in CLOUDFLARE_IPV4 + CLOUDFLARE_IPV6]

def is_cloudflare_ip(ip):
    ip_obj = ipaddress.ip_address(ip)
    return any(ip_obj in net for net in CLOUDFLARE_NETS)

def resolve_subdomain(sub):
    try:
        return socket.gethostbyname_ex(sub)[2]
    except Exception:
        return []

def main(domain):
    print(f"[*] Querying crt.sh for {domain}...")
    r = requests.get(f"https://crt.sh/?q={domain}&output=json")
    subs = set()
    for cert in r.json():
        for line in cert["name_value"].split("\n"):
            if domain in line:
                subs.add(line.strip().lower())
    print(f"[*] Found {len(subs)} unique subdomains.")
    for sub in sorted(subs):
        ips = resolve_subdomain(sub)
        if not ips:
            continue
        for ip in ips:
            if not is_cloudflare_ip(ip):
                print(f"[POTENTIAL ORIGIN] {sub} -> {ip}")
            else:
                print(f"[Cloudflare] {sub} -> {ip}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <domain>")
        sys.exit(1)
    main(sys.argv[1])

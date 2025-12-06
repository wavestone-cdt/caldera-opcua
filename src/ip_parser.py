import ipaddress
import re

def ipparser(input_value):
    ips = []

    if isinstance(input_value, list):
        for ip in input_value:
            if validate_ip(ip):
                ips.append(ip)
        return ips

    # Range d'IP avec -
    if '-' in input_value:
        range_pattern = r'^(\d+\.\d+\.\d+\.)(\d+)-(\d+)$'
        match = re.match(range_pattern, input_value)
        if match:
            base = match.group(1)
            start = int(match.group(2))
            end = int(match.group(3))
            for i in range(start, end + 1):
                ip = f"{base}{i}"
                if validate_ip(ip):
                    ips.append(ip)
            return ips

    # Sous-réseau CIDR
    if '/' in input_value:
        try:
            network = ipaddress.ip_network(input_value, strict=False)
            ips = [str(ip) for ip in network.hosts()]
            return ips
        except ValueError:
            return []
    # Liste d'IP séparées par des virgules
    if ',' in input_value:
        ips = [ip.strip() for ip in input_value.split(',')]
        valid_ips = [ip for ip in ips if validate_ip(ip)]
        return valid_ips

    # IP unique
    if validate_ip(input_value):
        return [input_value]

    return []

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

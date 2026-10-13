
import ipaddress
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from .network import get_ipv4_interfaces, select_scan_network


def check_host(ip):
    """Check whether a host responds to ping."""

    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1000", ip],
            capture_output=True,
            text=True,
            timeout=3
        )

        if result.returncode == 0:
            return {"ip": ip, "status": "UP"}

    except (subprocess.TimeoutExpired, OSError):
        pass

    return None


def discover_hosts(network, max_workers=40):
    """Discover hosts that respond to ping."""

    discovered = []
    addresses = [str(ip) for ip in network.hosts()]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(check_host, ip): ip
            for ip in addresses
        }

        for future in as_completed(futures):
            result = future.result()

            if result:
                discovered.append(result)

    return sorted(
        discovered,
        key=lambda host: ipaddress.ip_address(host["ip"])
    )


def resolve_hostname(ip):
    """Resolve a hostname using reverse DNS."""

    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return "Unknown"


if __name__ == "__main__":
    interfaces = get_ipv4_interfaces()
    interface, info = select_scan_network(interfaces)

    print("\nNetMapper - Host Discovery")
    print("=" * 55)
    print(f"Interface : {interface}")
    print(f"Network   : {info['network']}")
    print("Discovering hosts...")

    hosts = discover_hosts(info["network"])

    print("\nDiscovered Hosts")
    print("-" * 55)

    for host in hosts:
        hostname = resolve_hostname(host["ip"])
        print(f"{host['ip']:<20} {hostname:<25} {host['status']}")

    print("-" * 55)
    print(f"Total hosts found: {len(hosts)}")

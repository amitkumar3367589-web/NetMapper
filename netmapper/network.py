import socket
import ipaddress
import subprocess


def get_ipv4_interfaces():
    """Return active IPv4 interfaces and their network information."""

    interfaces = {}

    result = subprocess.run(
        ["ifconfig"],
        capture_output=True,
        text=True,
        check=True
    )

    current_interface = None

    for line in result.stdout.splitlines():

        # Interface declaration
        if line and not line.startswith((" ", "\t")) and ":" in line:
            current_interface = line.split(":")[0]

        # IPv4 address
        elif current_interface and "inet " in line:
            parts = line.strip().split()

            ip = parts[1]
            netmask_hex = parts[3]

            try:
                netmask = ipaddress.IPv4Address(
                    int(netmask_hex, 16)
                )

                network = ipaddress.ip_network(
                    f"{ip}/{netmask}",
                    strict=False
                )

                interfaces[current_interface] = {
                    "ip": ip,
                    "netmask": str(netmask),
                    "network": str(network),
                    "prefix": network.prefixlen,
                }

            except (ValueError, IndexError):
                continue

    return interfaces


def display_interfaces(interfaces):
    """Display detected IPv4 interfaces."""

    print("\nNetMapper - Network Interfaces")
    print("=" * 65)

    for interface, info in interfaces.items():

        print(f"\nInterface : {interface}")
        print(f"IP        : {info['ip']}")
        print(f"Netmask   : {info['netmask']}")
        print(f"Network   : {info['network']}")
        print(f"Prefix    : /{info['prefix']}")


if __name__ == "__main__":

    interfaces = get_ipv4_interfaces()

    display_interfaces(interfaces)
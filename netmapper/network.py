import ipaddress
import subprocess


def get_ipv4_interfaces():
    """Return IPv4 interfaces and their network information."""

    interfaces = {}
    result = subprocess.run(
        ["ifconfig"],
        capture_output=True,
        text=True,
        check=True
    )

    current_interface = None

    for line in result.stdout.splitlines():

        if line and not line.startswith((" ", "\t")) and ":" in line:
            current_interface = line.split(":")[0]

        elif current_interface and "inet " in line:
            parts = line.strip().split()

            try:
                ip = parts[1]
                netmask_hex = parts[3]

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
                    "network": network,
                    "prefix": network.prefixlen,
                }

            except (ValueError, IndexError):
                continue

    return interfaces


def select_scan_network(interfaces):
    """
    Select a suitable LAN network for host discovery.

    Ignores loopback and /32 point-to-point networks.
    """

    candidates = []

    for interface, info in interfaces.items():

        network = info["network"]

        # Ignore loopback
        if network.is_loopback:
            continue

        # Ignore point-to-point /32 interfaces
        if network.prefixlen == 32:
            continue

        candidates.append((interface, info))

    if not candidates:
        raise RuntimeError("No suitable LAN network found.")

    # Prefer Wi-Fi/Ethernet-style interfaces.
    preferred = ["en0", "en1", "en2", "en3", "en4"]

    for preferred_interface in preferred:
        for interface, info in candidates:
            if interface == preferred_interface:
                return interface, info

    return candidates[0]


def display_interfaces(interfaces):
    """Display detected interfaces."""

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

    interface, info = select_scan_network(interfaces)

    print("\nSelected Scan Network")
    print("=" * 65)
    print(f"Interface : {interface}")
    print(f"Network   : {info['network']}")
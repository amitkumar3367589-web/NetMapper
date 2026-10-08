import socket
import ipaddress


def get_local_ip():
    """Find the local IP address of this machine."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # We don't actually send data.
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
    finally:
        sock.close()

    return local_ip


def get_network(local_ip, prefix=24):
    """Create a network from the local IP and prefix length."""
    network = ipaddress.ip_network(
        f"{local_ip}/{prefix}",
        strict=False
    )

    return network


def get_network_info():
    """Collect basic network information."""
    local_ip = get_local_ip()
    network = get_network(local_ip)

    return {
        "local_ip": local_ip,
        "network": str(network),
        "netmask": str(network.netmask),
        "total_hosts": network.num_addresses - 2,
    }


if __name__ == "__main__":
    info = get_network_info()

    print("NetMapper - Network Information")
    print("--------------------------------")
    print(f"Local IP   : {info['local_ip']}")
    print(f"Network    : {info['network']}")
    print(f"Netmask    : {info['netmask']}")
    print(f"Total Hosts: {info['total_hosts']}")
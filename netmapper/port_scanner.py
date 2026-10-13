
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


COMMON_PORTS = [22, 53, 80, 443, 445, 5000, 8080, 8443, 58292, 7000]


def check_port(ip, port, timeout=0.5):
    """Return port details if a TCP connection succeeds."""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)

            if sock.connect_ex((ip, port)) == 0:
                return {
                    "ip": ip,
                    "port": port,
                    "status": "open"
                }

    except OSError:
        pass

    return None


def scan_host(ip, ports=COMMON_PORTS, max_workers=20):
    """Scan selected TCP ports on one authorized host."""

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(check_port, ip, port)
            for port in ports
        ]

        for future in as_completed(futures):
            result = future.result()

            if result:
                results.append(result)

    return sorted(results, key=lambda item: item["port"])


if __name__ == "__main__":
    target = input("Enter an IP address you own or have permission to scan: ").strip()

    try:
        socket.inet_pton(socket.AF_INET, target)
    except OSError:
        print("Invalid IPv4 address.")
    else:
        print(f"\nScanning selected TCP ports on {target}...")
        open_ports = scan_host(target)

        if open_ports:
            print("\nOpen Ports")
            print("-" * 40)

            for result in open_ports:
                print(f"Port {result['port']:<6} {result['status']}")
        else:
            print("No selected TCP ports responded as open.")

        print(f"\nTotal open ports found: {len(open_ports)}")

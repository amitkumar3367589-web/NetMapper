from datetime import datetime, timezone
from .network import get_ipv4_interfaces, select_scan_network
from .host_discovery import discover_hosts, resolve_hostname
from .port_scanner import scan_host
from .reporter import save_json, save_csv
from .traceroute import trace_route
from .services import identify_service

def run_scan():
    """Discover hosts, scan selected ports, and save results."""

    interfaces = get_ipv4_interfaces()
    interface, info = select_scan_network(interfaces)
    network = info["network"]

    print("\nNetMapper - Network Scan")
    print("=" * 55)
    print(f"Interface : {interface}")
    print(f"Network   : {network}")
    print("Discovering hosts...")

    hosts = discover_hosts(network)
    results = []

    for host in hosts:
        ip = host["ip"]
        hostname = resolve_hostname(ip)

        print(f"\nHost: {ip} ({hostname})")
        print("Scanning selected TCP ports...")

        open_ports = scan_host(ip)

        results.append({
            "ip": ip,
            "hostname": hostname,
            "status": host["status"],
            "open_ports": [
                item["port"] for item in open_ports
            ]
        })

        for item in open_ports:
            port = item["port"]
            service = identify_service(port)
            print(f"  Open TCP port: {port} ({service})")
            
if __name__ == "__main__":
    run_scan()
    destination = input(
    "\nEnter a destination for traceroute, or press Enter to skip: "
).strip()

route_data = None

if destination:
    route_data = trace_route(destination)

    report_data = {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "interface": interface,
        "network": str(network),
        "total_hosts_found": len(results),
        "hosts": results,
        "traceroute": route_data
    }

    save_json(report_data, "latest_scan.json")
    save_csv(results, "latest_scan.csv")

    print("\nScan complete!")
    print(f"Hosts discovered: {len(results)}")



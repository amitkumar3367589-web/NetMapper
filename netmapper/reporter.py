
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


REPORTS_DIR = Path("reports")


def save_json(data, filename="scan_report.json"):
    """Save the full scan report as JSON."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "tool": "NetMapper",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": data
    }

    output_path = REPORTS_DIR / filename

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"JSON report saved: {output_path}")


def save_csv(hosts, filename="scan_report.csv"):
    """Save one row per discovered host."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = REPORTS_DIR / filename

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "ip",
                "hostname",
                "status",
                "open_ports"
            ]
        )

        writer.writeheader()

        for host in hosts:
            row = host.copy()
            row["open_ports"] = ", ".join(
                str(port) for port in row.get("open_ports", [])
            )
            writer.writerow(row)

    print(f"CSV report saved: {output_path}")


if __name__ == "__main__":
    sample_hosts = [
        {
            "ip": "192.168.1.10",
            "hostname": "example-device",
            "status": "UP",
            "open_ports": [80, 443]
        }
    ]

    save_json({"hosts": sample_hosts})
    save_csv(sample_hosts)

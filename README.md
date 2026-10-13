# NetMapper

**A Python-based network discovery and analysis tool.**

NetMapper helps users discover active hosts on a local network, scan selected TCP ports, identify likely services, trace network routes, and save scan results for later analysis.

## Features

- **Network Detection:** Detects local IPv4 interfaces and selects a suitable network.
- **Host Discovery:** Finds hosts that respond to ping.
- **TCP Port Scanning:** Checks selected TCP ports to identify open ports.
- **Service Identification:** Provides likely service labels based on port numbers.
- **Hostname Resolution:** Attempts to resolve hostnames using reverse DNS.
- **Traceroute:** Displays network hops toward a specified destination.
- **Report Generation:** Exports scan results in JSON and CSV formats.
- **Automated Testing:** Includes unit tests for service identification and report generation.

## Technology Stack

- Python 3
- Socket programming
- `subprocess`
- `concurrent.futures`
- JSON and CSV
- `unittest`
- Git and GitHub

## Project Structure

```text
NetMapper/
├── netmapper/
│   ├── network.py
│   ├── host_discovery.py
│   ├── port_scanner.py
│   ├── services.py
│   ├── traceroute.py
│   ├── reporter.py
│   └── scanner.py
├── tests/
│   ├── test_services.py
│   └── test_reporter.py
├── reports/
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3
- macOS or another compatible environment with the required networking utilities
- Permission to scan the network and devices being tested

## Installation

Clone the repository:

```bash
git clone https://github.com/amitkumar3367589-web/NetMapper.git
cd NetMapper
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies if listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

Run the main scanner from the project root:

```bash
python3 -m netmapper.scanner
```

NetMapper detects a suitable local network, discovers responsive hosts, scans its configured TCP ports, and saves reports.

When prompted, enter a destination for traceroute or press Enter to skip it.

### Output Reports

The scanner generates reports in the `reports/` directory:

- `latest_scan.json` — structured scan results and metadata.
- `latest_scan.csv` — tabular host and port information.

These generated reports are excluded from version control by `.gitignore`.

## Run the Tests

From the project root:

```bash
python3 -m unittest discover -s tests -v
```

The current test suite covers service labels and JSON/CSV report generation.

## Limitations

- Hosts that do not respond to ping may not appear in discovery results.
- Only configured TCP ports are checked by the current scanner.
- Service labels are estimates based on port numbers; they do not confirm the actual software running on a port.
- Traceroute results depend on network configuration and whether intermediate devices respond.
- Results can vary depending on firewall rules, permissions, and network conditions.

## Responsible Use

Use NetMapper only on networks and devices you own or have explicit permission to assess. Follow applicable laws and organizational policies.

## Future Improvements

- Configurable port ranges
- Improved service detection
- Additional network and error-handling tests
- Scan comparison and historical reports
- More detailed reporting and visualization

## Author

Developed as a Python networking and cybersecurity portfolio project.

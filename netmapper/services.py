
SERVICE_NAMES = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    5000: "Common App / Development",
    7000: "Common App / Development",
    8080: "HTTP Alternate",
    8443: "HTTPS Alternate",
    58292: "Dynamic / Unknown",
}


def identify_service(port):
    """Return a likely service name for a TCP port."""
    return SERVICE_NAMES.get(port, "Unknown")

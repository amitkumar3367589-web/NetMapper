
import subprocess


def trace_route(destination, max_hops=20, timeout=2):
    """Trace the route and return parsed hop information."""

    command = [
        "traceroute",
        "-n",
        "-m", str(max_hops),
        "-w", str(timeout),
        "-q", "1",
        destination
    ]

    hops = []

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            parts = line.split(maxsplit=2)

            if not parts or not parts[0].isdigit():
                continue

            hop_number = int(parts[0])
            details = parts[1] if len(parts) > 1 else "*"

            hops.append({
                "hop": hop_number,
                "details": details,
                "response": line.strip()
            })

        process.wait()

        return {
            "destination": destination,
            "hops": hops
        }

    except (OSError, subprocess.SubprocessError) as error:
        print(f"Traceroute failed: {error}")

        return {
            "destination": destination,
            "hops": []
        }

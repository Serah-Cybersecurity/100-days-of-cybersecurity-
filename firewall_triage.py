import csv
import ipaddress
import sys
from collections import Counter
from pathlib import Path

REQUIRED_COLUMNS = {
    "timestamp",
    "src_ip",
    "src_port",
    "dst_ip",
    "dst_port",
    "protocol",
    "direction",
    "action",
    "interface",
    "state",
}

VALID_ACTIONS = {"ALLOW", "DENY", "DROP"}
VALID_PROTOCOLS = {"TCP", "UDP", "ICMP"}

def load_events(path: Path):
    """Load and validate synthetic firewall events from a CSV file."""
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no header row.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(sorted(missing))}"
            )

        events = []
        for line_number, raw in enumerate(reader, start=2):
            row = {
                key: (raw.get(key) or "").strip()
                for key in REQUIRED_COLUMNS
            }

            try:
                # Validate IP addresses
                ipaddress.ip_address(row["src_ip"])
                ipaddress.ip_address(row["dst_ip"])

                protocol = row["protocol"].upper()
                action = row["action"].upper()
                direction = row["direction"].upper()

                if protocol not in VALID_PROTOCOLS:
                    raise ValueError(f"Unsupported protocol: {protocol}")

                if action not in VALID_ACTIONS:
                    raise ValueError(f"Unsupported action: {action}")

                if direction not in {"INBOUND", "OUTBOUND", "INTRA"}:
                    raise ValueError(f"Unsupported direction: {direction}")

                # Validate port numbers if present
                for field in ("src_port", "dst_port"):
                    if row[field]:
                        port = int(row[field])
                        if not 0 <= port <= 65535:
                            raise ValueError(f"{field} must be between 0 and 65535")

                row["protocol"] = protocol
                row["action"] = action
                row["direction"] = direction

            except ValueError as error:
                raise ValueError(f"Line {line_number}: {error}") from error

            events.append(row)

    return events

def main():
    path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("sample_firewall_events.csv")
    )

    try:
        events = load_events(path)
    except (OSError, ValueError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        raise SystemExit(1)

    if not events:
        print("No events found.")
        return

    action_counts = Counter(event["action"] for event in events)

    denied = [
        event for event in events
        if event["action"] in {"DENY", "DROP"}
    ]

    denied_sources = Counter(event["src_ip"] for event in denied)

    patterns = Counter(
        (
            event["src_ip"],
            event["dst_ip"],
            event["dst_port"],
            event["protocol"],
        )
        for event in denied
    )

    print(f"Events analysed: {len(events)}")

    print("\nActions:")
    for action, count in sorted(action_counts.items()):
        print(f"  {action}: {count}")

    print("\nTop sources in DENY/DROP events:")
    for source, count in denied_sources.most_common(5):
        print(f"  {source}: {count}")

    print("\nRepeated DENY/DROP patterns (3 or more records):")
    repeated = [
        (key, count)
        for key, count in patterns.items()
        if count >= 3
    ]

    if not repeated:
        print("  None")
    else:
        repeated.sort(key=lambda item: item[1], reverse=True)
        for (src, dst, port, protocol), count in repeated:
            print(
                f"  {src} -> {dst}:{port}/{protocol}: "
                f"{count} records"
            )

    print(
        "\nInterpretation caution: a repeated block is "
        "a triage lead, not proof of malicious activity."
    )

if __name__ == "__main__":
    main()

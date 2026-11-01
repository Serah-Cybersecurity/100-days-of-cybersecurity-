import json
from collections import Counter
from typing import Dict, List, Tuple

def load_network_events(file_path: str) -> List[Dict]:
    """
    Reads a JSON log file containing network event records.
    Handles FileNotFoundError and JSONDecodeError gracefully.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"[-] Error: Expected a JSON array/list in {file_path}")
                return []
            return data
    except FileNotFoundError:
        print(f"[-] Error: Log file '{file_path}' was not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"[-] Error: Malformed JSON syntax in '{file_path}': {e}")
        return []

def validate_event_record(event: Dict) -> Tuple[bool, str]:
    """
    Validates mandatory schema fields, data types, and range checks.
    Returns (True, "OK") or (False, "Reason for rejection").
    """
    required_fields = ["timestamp", "source", "destination", "destination_port", "protocol"]
    
    # 1. Check for missing fields
    for field in required_fields:
        if field not in event:
            return False, f"Missing required field: '{field}'"

    # 2. Validate destination port
    port = event["destination_port"]
    if not isinstance(port, int):
        return False, f"Invalid port type '{type(port).__name__}'; expected integer"
    if not (1 <= port <= 65535):
        return False, f"Port number {port} out of valid RFC range (1-65535)"

    # 3. Protocol validation
    protocol = str(event["protocol"]).upper()
    if protocol not in ["TCP", "UDP", "ICMP"]:
        return False, f"Unrecognized/unsupported protocol: '{protocol}'"

    return True, "OK"

def analyze_network_events(events: List[Dict]):
    """
    Processes network events, maintains protocol/port counters, 
    and segregates valid records from malformed entries.
    """
    valid_records = []
    malformed_records = []

    protocol_counter = Counter()
    port_counter = Counter()

    for idx, record in enumerate(events, start=1):
        is_valid, reason = validate_event_record(record)
        if is_valid:
            valid_records.append(record)
            protocol_counter[record["protocol"].upper()] += 1
            port_counter[record["destination_port"]] += 1
        else:
            malformed_records.append({"record_index": idx, "reason": reason, "raw_record": record})

    # Print Summary Report
    print("==================================================")
    print("           NETWORK EVENT ANALYSIS REPORT          ")
    print("==================================================")
    print("[!] NOTICE: All data processed in this report is FAKE/SYNTHETIC.")
    print("--------------------------------------------------")
    print(f"Total Log Records Ingested:   {len(events)}")
    print(f"Valid Network Events:         {len(valid_records)}")
    print(f"Malformed/Skipped Records:    {len(malformed_records)}")
    print("--------------------------------------------------")
    
    print("\n[+] Events Breakdown by Protocol:")
    for proto, count in protocol_counter.items():
        print(f"    - {proto:<5}: {count}")

    print("\n[+] Events Breakdown by Destination Port:")
    for port, count in sorted(port_counter.items()):
        print(f"    - Port {port:<5}: {count} event(s)")

    if malformed_records:
        print("\n[-] Malformed/Incomplete Record Audit Log:")
        for bad in malformed_records:
            print(f"    - Record #{bad['record_index']}: Rejection Reason -> {bad['reason']}")

    print("==================================================\n")

def main():
    log_file_path = "sample_events.json"
    print(f"[*] Ingesting and parsing log file: '{log_file_path}'...")
    events = load_network_events(log_file_path)
    
    if events:
        analyze_network_events(events)

if __name__ == "__main__":
    main()

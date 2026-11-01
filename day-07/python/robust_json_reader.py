# Day 7 — Robust JSON Reader with Comprehensive Exception Handling & Validation

import json
from pathlib import Path

def process_log_file(filename):
    """Safely loads, parses, and validates security log files."""
    data_file = Path(__file__).resolve().parent.parent / "data" / filename
    
    print(f"\n--- Testing File: {filename} ---")
    
    # 1. Handle file system and parsing exceptions
    try:
        with data_file.open("r", encoding="utf-8") as file:
            events = json.load(file)
    except FileNotFoundError:
        print("[ERROR] The specified log file could not be found.")
        return
    except json.JSONDecodeError:
        print("[ERROR] The file contains invalid JSON syntax (Malformed data).")
        return

    # 2. Validate top-level data structure type
    if not isinstance(events, list):
        print(f"[ERROR] Invalid structure! Expected a list of events, but found {type(events).__name__}.")
        return

    # 3. Validate individual records within the list
    valid_record_count = 0
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            print(f"[WARNING] Record at index {index} is malformed (Not a dictionary object).")
        else:
            valid_record_count += 1
            print(f"[SUCCESS] Record {index} parsed correctly. User: {event.get('username', 'Unknown')}")

    print(f"Summary: Successfully processed {valid_record_count} valid record(s).")

# --- TEST ALL THREE SCENARIOS ---
if __name__ == "__main__":
    process_log_file("valid_events.json")
    process_log_file("malformed_events.json")
    process_log_file("wrong_type_events.json")
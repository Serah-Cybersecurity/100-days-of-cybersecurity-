# Day 7 — Capstone Project: Python Security Log Analyzer Version 1

import json
from collections import Counter
from pathlib import Path

# --- PART A: CONFIGURATION ---
# Define a robust relative path to our sample events dataset
DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sample_events.json"
)

# Define the mandatory schema fields required for every log record
REQUIRED_FIELDS = {
    "timestamp",
    "username",
    "event",
    "source_ip",
}


# --- PART B: FILE LOADING & EXCEPTION HANDLING ---
def load_events(file_path):
    """Load JSON data and verify that the top-level value is a list."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None

    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON syntax.")
        return None

    # Validate top-level data structure type
    if not isinstance(data, list):
        print("Error: Expected a JSON list of event records.")
        return None

    return data


# --- PART C: SCHEMA VALIDATION ---
def validate_events(events):
    """Separate basic valid records from invalid/malformed records."""
    valid_events = []
    invalid_records = []

    for index, event in enumerate(events):
        # 1. Check if record is a dictionary object
        if not isinstance(event, dict):
            invalid_records.append(
                {
                    "record_number": index,
                    "reason": "Record is not a JSON object",
                }
            )
            continue

        # 2. Check for missing required schema fields using set subtraction
        missing_fields = REQUIRED_FIELDS - event.keys()

        if missing_fields:
            invalid_records.append(
                {
                    "record_number": index,
                    "reason": (
                        "Missing required fields: "
                        + ", ".join(sorted(missing_fields))
                    ),
                }
            )
            continue

        # 3. Verify that all required fields contain string data types
        if not all(
            isinstance(event[field], str)
            for field in REQUIRED_FIELDS
        ):
            invalid_records.append(
                {
                    "record_number": index,
                    "reason": "Required fields must be strings",
                }
            )
            continue

        # If all checks pass, add to valid collection
        valid_events.append(event)

    return valid_events, invalid_records


# --- PART D: EVENT ANALYSIS & AGGREGATION ---
def analyze_events(events):
    """Summarize the supplied valid event records using Counter."""
    
    # Aggregate counts by event type
    event_counts = Counter(
        event["event"] for event in events
    )

    # Aggregate counts by username
    username_counts = Counter(
        event["username"] for event in events
    )

    # Filter specific failed login signatures
    failed_logins = [
        event
        for event in events
        if event["event"] == "login_failed"
    ]

    return {
        "total_events": len(events),
        "event_counts": event_counts,
        "username_counts": username_counts,
        "failed_login_count": len(failed_logins),
    }


# --- PART E: REPORTING & INTERPRETATION ---
def print_report(summary, invalid_records):
    """Print a professional, readable summary of the analysis."""
    print("=== Python Security Log Analyzer ===")
    print("Dataset: fictional training data")
    print("Valid records:", summary["total_events"])
    print("Invalid records:", len(invalid_records))
    print("Failed login events:", summary["failed_login_count"])

    print("\nEvents by type:")
    for event_type, count in sorted(
        summary["event_counts"].items()
    ):
        print(f"- {event_type}: {count}")

    print("\nEvents by username:")
    for username, count in sorted(
        summary["username_counts"].items()
    ):
        print(f"- {username}: {count}")

    if invalid_records:
        print("\nInvalid record details:")
        for record in invalid_records:
            print(
                f"- Record {record['record_number']}: "
                f"{record['reason']}"
            )

    print("\nInterpretation:")
    print(
        "These counts describe the supplied dataset. "
        "They do not prove malicious activity."
    )


# --- MAIN EXECUTION BLOCK ---
def main():
    # 1. Load file data
    events = load_events(DATA_FILE)
    if events is None:
        return

    # 2. Validate event schemas
    valid_events, invalid_records = validate_events(events)

    # 3. Analyze and aggregate valid records
    summary = analyze_events(valid_events)

    # 4. Generate final report
    print_report(summary, invalid_records)


if __name__ == "__main__":
    main()
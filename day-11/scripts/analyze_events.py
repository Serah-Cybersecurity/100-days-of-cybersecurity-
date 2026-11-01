#!/usr/bin/env python3
"""
Day 11: Synthetic security-event analyser.

Purpose:
    Summarise selected authentication and system events
    from a local JSONL file.

Scope:
    Defensive learning using supplied event records.

Limitations:
    This is a basic triage aid, not a complete SIEM,
    forensic tool, or malware detector.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarise a synthetic JSONL security-event dataset."
    )

    parser.add_argument(
        "logfile",
        type=Path,
        help="Path to the JSONL file to analyse.",
    )

    parser.add_argument(
        "--failure-threshold",
        type=int,
        default=3,
        help="Number of failed logins that triggers a review prompt.",
    )

    args = parser.parse_args()

    if args.failure_threshold < 1:
        parser.error("--failure-threshold must be at least 1")

    event_counts = Counter()
    failed_by_ip = Counter()
    successful_by_ip = Counter()
    privilege_events = []

    records_processed = 0
    malformed_records = 0

    try:
        with args.logfile.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):

                if not raw_line.strip():
                    continue

                try:
                    event = json.loads(raw_line)

                except json.JSONDecodeError as exc:
                    malformed_records += 1

                    print(
                        f"WARNING: malformed JSON on line "
                        f"{line_number}: {exc.msg}",
                        file=sys.stderr,
                    )
                    continue

                if not isinstance(event, dict):
                    malformed_records += 1

                    print(
                        f"WARNING: line {line_number} "
                        "does not contain a JSON object.",
                        file=sys.stderr,
                    )
                    continue

                records_processed += 1

                event_type = str(
                    event.get("event_type", "unknown")
                )

                event_counts[event_type] += 1

                if event_type == "authentication":

                    source_ip = str(
                        event.get("source_ip", "(unknown)")
                    )

                    result = event.get("result")

                    if result == "failed":
                        failed_by_ip[source_ip] += 1

                    elif result == "success":
                        successful_by_ip[source_ip] += 1

                if event_type == "privilege_use":
                    privilege_events.append(event)

    except OSError as exc:
        print(
            f"ERROR: could not read {args.logfile}: {exc}",
            file=sys.stderr,
        )
        return 2

    if records_processed == 0:
        print(
            "ERROR: no valid event records were processed.",
            file=sys.stderr,
        )
        return 1

    print("DAY 11 SECURITY-EVENT SUMMARY")
    print("=============================")

    print(f"Records processed: {records_processed}")
    print(f"Malformed records: {malformed_records}")

    print("\nEvent counts:")

    for event_type, count in sorted(event_counts.items()):
        print(f"  {event_type}: {count}")

    print("\nAuthentication summaries:")

    source_addresses = (
        set(failed_by_ip) | set(successful_by_ip)
    )

    for source_ip in sorted(source_addresses):

        failures = failed_by_ip[source_ip]
        successes = successful_by_ip[source_ip]

        print(
            f"  {source_ip}: "
            f"failures={failures}, successes={successes}"
        )

        if failures >= args.failure_threshold:
            print(
                "    [REVIEW] Failed-login count reached "
                "the configured threshold."
            )

        if failures > 0 and successes > 0:
            print(
                "    [CORRELATION] This source has both failed "
                "and successful authentication events."
            )

    print("\nPrivilege-use events:")

    if not privilege_events:
        print("  No privilege-use events were recorded.")

    for event in privilege_events:

        timestamp = event.get("timestamp", "(unknown time)")
        username = event.get("username", "(unknown user)")
        result = event.get("result", "(unknown result)")
        command = event.get("command", "(not recorded)")

        print(
            f"  - {timestamp}: "
            f"user={username}, "
            f"result={result}, "
            f"command={command}"
        )

    print("\nInterpretation limits:")
    print(
        "  These flags identify events for human review; "
        "they do not establish malicious activity."
    )
    print(
        "  Conclusions require context and additional evidence."
    )

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

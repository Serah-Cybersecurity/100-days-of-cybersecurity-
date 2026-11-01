#!/usr/bin/env python3
"""
Day 13: Mini-SIEM Event Correlation Tool

Purpose:
    Read synthetic multi-source JSONL security events,
    validate basic fields, and identify an authentication
    pattern requiring human review.

Scope:
    Local, supplied learning dataset only.

Limitations:
    This is an educational analysis tool.
    It is not a production SIEM or malware detector.
"""

import argparse
import ipaddress
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REQUIRED_FIELDS = {
    "timestamp",
    "host",
    "platform",
    "source",
    "event_type",
    "result",
}


def parse_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string.")

    timestamp = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    if timestamp.tzinfo is None:
        raise ValueError("Timestamp must include a timezone.")

    return timestamp.astimezone(timezone.utc)


def load_events(path):
    events = []
    malformed = 0

    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                if not raw_line.strip():
                    continue

                try:
                    event = json.loads(raw_line)

                    if not isinstance(event, dict):
                        raise ValueError(
                            "Record must be a JSON object."
                        )

                    missing = REQUIRED_FIELDS - event.keys()

                    if missing:
                        raise ValueError(
                            f"Missing required fields: {sorted(missing)}"
                        )

                    event["_parsed_time"] = parse_timestamp(
                        event["timestamp"]
                    )

                    source_ip = event.get("src_ip")

                    if source_ip:
                        ipaddress.ip_address(source_ip)

                    event["platform"] = str(
                        event["platform"]
                    ).casefold()

                    event["event_type"] = str(
                        event["event_type"]
                    ).casefold()

                    events.append(event)

                except (
                    json.JSONDecodeError,
                    ValueError,
                    TypeError,
                ) as exc:
                    malformed += 1
                    print(
                        f"WARNING line {line_number}: {exc}",
                        file=sys.stderr,
                    )

    except OSError as exc:
        print(
            f"ERROR: Could not read input file: {exc}",
            file=sys.stderr,
        )
        return None, malformed

    return events, malformed


def analyse_events(events, threshold, window_minutes):
    event_counts = Counter()
    source_counts = Counter()
    ip_activity = defaultdict(Counter)

    authentication_groups = defaultdict(list)

    for event in events:
        event_type = event["event_type"]
        platform = event["platform"]

        source = str(
            event.get("source", "unknown")
        )

        event_counts[event_type] += 1

        source_counts[
            (platform, source, event_type)
        ] += 1

        source_ip = event.get("src_ip")

        if source_ip:
            ip_activity[source_ip][
                (platform, event_type)
            ] += 1

        if event_type == "authentication":
            username = event.get("username")
            result = str(
                event.get("result", "unknown")
            ).casefold()

            if username and source_ip:
                authentication_groups[
                    (username, source_ip)
                ].append(event)

    window = timedelta(minutes=window_minutes)

    candidates = []

    for key, grouped_events in authentication_groups.items():
        grouped_events.sort(
            key=lambda item: item["_parsed_time"]
        )

        recent_failures = []

        for event in grouped_events:
            current_time = event["_parsed_time"]

            recent_failures = [
                failure
                for failure in recent_failures
                if timedelta(0)
                <= current_time - failure["_parsed_time"]
                <= window
            ]

            result = str(
                event.get("result", "")
            ).casefold()

            if result == "failure":
                recent_failures.append(event)

            elif result == "success":
                if len(recent_failures) >= threshold:
                    candidates.append({
                        "username": key[0],
                        "src_ip": key[1],
                        "failed_attempts": len(recent_failures),
                        "success_time": event["timestamp"],
                        "first_failure": recent_failures[0]["timestamp"],
                    })
                    break

    return event_counts, source_counts, ip_activity, candidates


def main():
    parser = argparse.ArgumentParser(
        description="Analyse synthetic multi-source security events."
    )

    parser.add_argument(
        "logfile",
        type=Path,
        help="Path to the JSONL event file."
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Failed authentication threshold."
    )

    parser.add_argument(
        "--window-minutes",
        type=int,
        default=10,
        help="Time window for the correlation rule."
    )

    args = parser.parse_args()

    if args.threshold < 1:
        parser.error("--threshold must be at least 1")

    if args.window_minutes < 1:
        parser.error("--window-minutes must be at least 1")

    events, malformed = load_events(args.logfile)

    if events is None:
        return 2

    if not events:
        print("ERROR: No valid records were processed.")
        return 1

    (
        event_counts,
        source_counts,
        ip_activity,
        candidates,
    ) = analyse_events(
        events,
        args.threshold,
        args.window_minutes,
    )

    print("\n===== MINI-SIEM SUMMARY =====")

    print(f"Valid events: {len(events)}")
    print(f"Malformed records: {malformed}")

    print("\nEvent counts:")

    for event_type, count in sorted(event_counts.items()):
        print(f"{event_type}: {count}")

    print("\nSource summary:")

    for key, count in sorted(source_counts.items()):
        platform, source, event_type = key
        print(
            f"{platform} | {source} | "
            f"{event_type}: {count}"
        )

    print("\nActivity grouped by source IP:")

    for source_ip, activities in sorted(ip_activity.items()):
        print(f"\n{source_ip}")
        for activity, count in sorted(activities.items()):
            platform, event_type = activity
            print(
                f"  {platform} | {event_type}: {count}"
            )

    print("\nAuthentication review candidates:")

    if not candidates:
        print("No candidates matched the configured rule.")

    for candidate in candidates:
        print(
            f"REVIEW: user={candidate['username']} "
            f"source={candidate['src_ip']} "
            f"failures={candidate['failed_attempts']} "
            f"success={candidate['success_time']}"
        )

    print("\nLimitations:")
    print(
        "A review candidate is not proof of malicious activity."
    )
    print(
        "The result depends on the supplied data, "
        "field quality and configured threshold."
    )
    print(
        "The tool does not inspect every possible attack pattern."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Day 14: SOC Alert Queue Utility.

Purpose:
    Organise and validate synthetic SOC alert records.

Scope:
    Local, fictional learning dataset.

Limitations:
    This tool does not determine whether an alert is malicious.
    Classification and investigation remain human responsibilities.
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FIELDS = {
    "alert_id",
    "created_at",
    "title",
    "severity",
    "status",
    "host",
    "summary",
    "rule_id",
}

SEVERITY_ORDER = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
    "informational": 5,
}

def parse_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string.")

    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    if parsed.tzinfo is None:
        raise ValueError(
            "Timestamp must include timezone information."
        )

    return parsed.astimezone(timezone.utc)

def load_alerts(path):
    alerts = []
    invalid_records = 0

    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                if not raw_line.strip():
                    continue

                try:
                    alert = json.loads(raw_line)

                    if not isinstance(alert, dict):
                        raise ValueError(
                            "Alert must be a JSON object."
                        )

                    missing = REQUIRED_FIELDS - alert.keys()

                    if missing:
                        raise ValueError(
                            f"Missing fields: {sorted(missing)}"
                        )

                    severity = str(
                        alert["severity"]
                    ).casefold()

                    if severity not in SEVERITY_ORDER:
                        raise ValueError(
                            f"Invalid severity: {severity}"
                        )

                    alert["_severity"] = severity
                    alert["_parsed_time"] = parse_timestamp(
                        alert["created_at"]
                    )

                    alerts.append(alert)

                except (
                    json.JSONDecodeError,
                    ValueError,
                    TypeError,
                ) as exc:
                    invalid_records += 1
                    print(
                        f"WARNING line {line_number}: {exc}",
                        file=sys.stderr,
                    )

    except OSError as exc:
        print(
            f"ERROR: Could not read alert queue: {exc}",
            file=sys.stderr,
        )
        return None, invalid_records

    return alerts, invalid_records

def display_alert_queue(alerts):
    sorted_alerts = sorted(
        alerts,
        key=lambda alert: (
            SEVERITY_ORDER[alert["_severity"]],
            alert["_parsed_time"],
            alert["alert_id"],
        )
    )

    print("\n===== SOC ALERT QUEUE =====")

    for alert in sorted_alerts:
        print("\n----------------------------")
        print(f"Alert ID: {alert['alert_id']}")
        print(f"Title: {alert['title']}")
        print(f"Severity: {alert['_severity'].upper()}")
        print(f"Status: {alert['status']}")
        print(f"Host: {alert['host']}")
        print(f"Rule: {alert['rule_id']}")
        print(f"Created: {alert['created_at']}")
        print(f"Summary: {alert['summary']}")

    print("\n===== SEVERITY SUMMARY =====")

    counts = Counter(
        alert["_severity"] for alert in alerts
    )

    for severity in SEVERITY_ORDER:
        if counts[severity]:
            print(f"{severity}: {counts[severity]}")

    print("\nReview the alerts manually.")
    print("Severity alone does not establish investigation priority.")
    print("No automatic malicious/benign verdict has been assigned.")

def main():
    parser = argparse.ArgumentParser(
        description="Organise and validate a synthetic SOC alert queue."
    )
    parser.add_argument(
        "alertfile",
        type=Path,
        help="Path to the JSONL alert queue."
    )

    args = parser.parse_args()

    alerts, invalid_records = load_alerts(args.alertfile)

    if alerts is None:
        return 2

    if not alerts:
        print("No valid alerts were loaded.")
        return 1

    print(f"Valid alerts: {len(alerts)}")
    print(f"Invalid records: {invalid_records}")

    display_alert_queue(alerts)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

# Technical Note: Building a Python Suricata EVE JSON Log Analyser

**Author:** Serah Mulwa

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

## 1. Executive Summary

In a live production environment, Suricata generates thousands of newline-delimited JSON records every minute inside its `eve.json` telemetry log. Manually reading through raw JSON event streams is inefficient and impractical for security analysts. 

To bridge the gap between raw data collection and actionable insight, we built a standalone Python log analyser (`src/eve_summary.py`). This script parses Suricata’s EVE JSON output, handles malformed records gracefully using robust exception handling, tallies event frequencies, and prints an executive summary directly to the terminal.

## 2. Python Script Implementation (`src/eve_summary.py`)

Below is the complete, self-contained Python script designed to parse Suricata EVE logs without requiring external third-party libraries:

```python
import json
import sys
from collections import Counter
from pathlib import Path

def analyse_eve_file(path: Path):
    """
    Read Suricata EVE JSON and summarise event types and alerts.

    EVE is newline-delimited JSON:
    one JSON object per line.
    """

    event_counts = Counter()
    signature_counts = Counter()
    severity_counts = Counter()

    total_records = 0
    malformed_records = 0
    alert_count = 0

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                event = json.loads(line)

            except json.JSONDecodeError:
                malformed_records += 1

                print(
                    f"Warning: malformed JSON at line {line_number}",
                    file=sys.stderr
                )

                continue

            if not isinstance(event, dict):
                malformed_records += 1
                continue

            total_records += 1

            event_type = event.get(
                "event_type",
                "unknown"
            )

            event_counts[event_type] += 1

            if event_type == "alert":

                alert_count += 1

                alert = event.get("alert") or {}

                signature = alert.get(
                    "signature",
                    "Unknown signature"
                )

                severity = alert.get(
                    "severity",
                    "Not supplied"
                )

                signature_counts[signature] += 1
                severity_counts[str(severity)] += 1

    return {
        "total_records": total_records,
        "malformed_records": malformed_records,
        "alert_count": alert_count,
        "event_counts": event_counts,
        "signature_counts": signature_counts,
        "severity_counts": severity_counts,
    }

def main():

    input_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("output/suricata/eve.json")
    )

    try:
        results = analyse_eve_file(input_path)

    except (OSError, ValueError) as error:

        print(
            f"Error: {error}",
            file=sys.stderr
        )

        raise SystemExit(1)

    print("\nSURICATA EVE ANALYSIS")
    print("=" * 35)

    print(
        f"Records analysed: "
        f"{results['total_records']}"
    )

    print(
        f"Alerts: "
        f"{results['alert_count']}"
    )

    print(
        f"Malformed records: "
        f"{results['malformed_records']}"
    )

    print("\nEVENT TYPES")

    for event_type, count in sorted(
        results["event_counts"].items()
    ):

        print(f"{event_type}: {count}")

    print("\nALERT SIGNATURES")

    if not results["signature_counts"]:

        print("No alert records found.")

    else:

        for signature, count in (
            results["signature_counts"].most_common()
        ):

            print(f"{signature}: {count}")

    print("\nALERT SEVERITY")

    if not results["severity_counts"]:

        print("No severity information available.")

    else:

        for severity, count in sorted(
            results["severity_counts"].items()
        ):

            print(f"{severity}: {count}")

    print(
        "\nNOTE: This tool summarises logged events. "
        "It does not determine whether activity is malicious."
    )

if __name__ == "__main__":
    main()
```

## 3. Core Python Concepts Explained

* **`json.loads()`:** Converts newline-delimited JSON strings from our log file into native Python dictionaries for easy data extraction.
* **`pathlib.Path`:** Provides a modern, secure, and cross-platform way to handle file system paths.
* **`collections.Counter`:** A specialized dictionary subclass that automatically counts occurrences of event types, signatures, and severity levels.
* **`enumerate(file, start=1)`:** Tracks exact line numbers while iterating through the log file, enabling precise warning messages if a log line is corrupted.
* **Defensive Exception Handling (`try...except`):** Ensures that if a single log line contains malformed JSON, the script catches the `JSONDecodeError`, logs a warning to `sys.stderr`, and continues processing the rest of the file without crashing.

## 4. Execution Output & Verification

Running our script against our generated Suricata output produced the following clean analyst summary:

```text
SURICATA EVE ANALYSIS
===================================
Records analysed: 17
Alerts: 4
Malformed records: 0

EVENT TYPES
alert: 4
dns: 8
flow: 4
stats: 1

ALERT SIGNATURES
LOCAL LAB DNS query for example.com: 4

ALERT SEVERITY
3: 4

NOTE: This tool summarises logged events. It does not determine whether activity is malicious.
```

## 5. Architectural Limitations

As a junior security engineer, it is essential to understand what this script **cannot** do:
1. **Does not determine malicious intent:** A rule match confirms that a pattern matched traffic; it does not prove an active cyberattack occurred (our test matched benign traffic to `example.com`).
2. **Does not replace a SIEM:** Enterprise security platforms (such as Splunk or Elastic) handle distributed log aggregation, cross-device correlation, and automated alerting at scale.
3. **Does not perform endpoint forensics:** It evaluates network telemetry alone without inspecting host processes or memory dumps.

## 6. Job Market Relevance

* **Security Automation Engineer:** Writes custom Python parsers to automate log ingestion, extract Indicators of Compromise (IoCs), and enrich ticketing pipelines prior to human triage.
* **SOC Analyst:** Uses command-line scripts to rapidly summarize large historical log archives during incident response investigations.

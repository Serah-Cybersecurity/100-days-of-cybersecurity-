# Part 8: Python Network-Event Analyzer

---

## Table of Contents
1. [Overview & Prerequisites](#overview--prerequisites)
2. [Section 8.1: Directory & File Structure Setup](#section-81-directory--file-structure-setup)
3. [Foundational Concepts Explained for Beginners](#foundational-concepts-explained-for-beginners)
   - [Variables & Data Types](#1-variables--data-types)
   - [Lists & Dictionaries](#2-lists--dictionaries)
   - [Loops & Control Flow](#3-loops--control-flow)
   - [Functions](#4-functions)
   - [File Handling](#5-file-handling)
   - [JSON Parsing (`json` module)](#6-json-parsing-json-module)
   - [Counters (`collections.Counter` & Dictionary Counters)](#7-counters-collections-counter--dictionary-counters)
   - [Error Handling (`try-except` blocks)](#8-error-handling-try-except-blocks)
4. [Section 8.2 & 8.3: Basic Network Event Analyzer (Step-by-Step)](#section-82--83-basic-network-event-analyzer-step-by-step)
   - [Sample Dataset (`sample_events.json`)](#sample-dataset-sample_eventsjson)
   - [Basic Script (`network_event_analyzer.py`)](#basic-script-network_event_analyzerpy)
5. [Section 8.4: Extending the Analyzer (Robust Validation & Error Handling)](#section-84-extending-the-analyzer-robust-validation--error-handling)
   - [Full Extended Code Walkthrough](#full-extended-code-walkthrough)
6. [Section 8.5: Systematic Testing Strategy](#section-85-systematic-testing-strategy)
   - [Test Matrix](#test-matrix)
   - [Sample Output Verification](#sample-output-verification)
7. [Industry & Real-World Application](#industry--real-world-application)

---

## Overview & Prerequisites

### Context & Purpose
In modern Security Operations Centers (SOCs) and Cloud Security Architecture, security analysts rarely inspect traffic manually packet by packet at scale. Instead, tools such as **SIEMs (Security Information and Event Management)** like Splunk or Microsoft Sentinel, and **SOAR (Security Orchestration, Automation, and Response)** platforms parse incoming log data formatted as JSON or Syslog messages. 

This project bridges programming fundamentals (Day 2 and Day 3) with networking and log analysis (Day 4 and Day 5). You will build a script that ingests, cleans, validates, and analyzes fictional network traffic event logs.

> ⚠️ **IMPORTANT NOTICE:** The data processed in this laboratory consists exclusively of synthetic, fictional training records. Do not collect, sniff, or process private network traffic or third-party log data without explicit written authorization.

---

## Section 8.1: Directory & File Structure Setup

### Directory Layout
Ensure your local cybersecurity repository follows this directory layout under `day-05/`:

```text
day-05/
└── python/
    ├── README.md
    ├── sample_events.json
    └── network_event_analyzer.py
```

### Commands to Setup Directories and Files
Execute the following commands in your Linux or macOS terminal to set up the environment:

```bash
# Navigate to your main repository root
cd path/to/your/cybersecurity-journey

# Create the nested directory structure
mkdir -p day-05/python

# Move into the python directory
cd day-05/python

# Create empty files for the data and the Python script
touch sample_events.json network_event_analyzer.py README.md
```

---

## Foundational Concepts Explained for Beginners

Before diving into code execution, let's break down the 10 core concepts used in this project.

### 1. Variables & Data Types
* **What it is:** A variable is a named storage location in memory holding data. Standard data types include integers (`int`), strings (`str`), booleans (`bool`), floating-point numbers (`float`), lists (`list`), and dictionaries (`dict`).
* **Why it matters:** Security scripts rely on variables to track state—such as current event counts, active IP addresses, or file paths.
* **How it works:**
  ```python
  total_events = 0               # Integer
  protocol_name = "TCP"          # String
  is_valid_event = True          # Boolean
  ```
* **Job Market Application:** Analysts write scripts to temporarily store API tokens, query results, and parsing flags during automation routines.

---

### 2. Lists & Dictionaries
* **What it is:** 
  * **List:** An ordered, mutable collection of items (indexed starting at 0).
  * **Dictionary:** A key-value store mapping unique keys to values.
* **Why it matters:** JSON logs natively load into Python as dictionaries or lists of dictionaries.
* **How it works:**
  ```python
  # A List of protocols
  protocols = ["TCP", "UDP", "ICMP"]

  # A Dictionary representing a single log entry
  event = {
      "source": "192.0.2.10",
      "destination_port": 443,
      "protocol": "TCP"
  }
  
  # Accessing dictionary values:
  port = event["destination_port"]  # Returns 443
  ```
* **What you must remember:** Trying to access a dictionary key that doesn't exist using `dict[key]` throws a `KeyError`. Use `.get(key)` to retrieve `None` safely instead of crashing.

---

### 3. Loops & Control Flow
* **What it is:** Statements (`for`, `while`, `if`, `elif`, `else`) that allow repetition and decision-making in code.
* **Why it matters:** Network log analysis requires iterating through thousands or millions of event records one at a time.
* **How it works:**
  ```python
  events = [{"protocol": "TCP"}, {"protocol": "UDP"}]

  for ev in events:
      if ev["protocol"] == "TCP":
          print("Connection uses Transmission Control Protocol")
      else:
          print("Connection uses another protocol")
  ```

---

### 4. Functions
* **What it is:** Reusable blocks of code that take inputs (arguments), process them, and return an output (`return`).
* **Why it matters:** Organizes code into logical units (e.g., reading a file, validating data, building reports) to make scripts scalable, clean, and testable.
* **How it works:**
  ```python
  def validate_port(port):
      """Validates if a port is within the valid TCP/UDP range (1-65535)."""
      if isinstance(port, int) and 1 <= port <= 65535:
          return True
      return False
  ```

---

### 5. File Handling
* **What it is:** Opening, reading, writing, and closing files from the local filesystem using Python's context manager (`with open(...)`).
* **Why it matters:** Logs are stored on disk. Opening files safely prevents resource leaks or file corruption.
* **How it works:**
  ```python
  with open("sample_events.json", "r", encoding="utf-8") as file_handle:
      content = file_handle.read()
  # File automatically closes here upon exiting the block
  ```
* **What you must remember:** Always use `with open(...)` rather than `file = open(...)` because `with` guarantees the file closes properly even if the program throws an error.

---

### 6. JSON Parsing (`json` module)
* **What it is:** JSON (JavaScript Object Notation) is a lightweight text format for structured data exchange. Python’s `json` standard module deserializes (converts) JSON strings/files into native Python objects (`dict` and `list`).
* **Why it matters:** Almost all modern log formats (AWS CloudTrail, Suricata, Elastic, CrowdStrike) emit JSON logs.
* **How it works:**
  ```python
  import json

  # Reading directly from a file pointer
  with open("sample_events.json", "r") as f:
      data = json.load(f)  # 'data' is now a Python list or dictionary
  ```

---

### 7. Counters (`collections.Counter` & Dictionary Counters)
* **What it is:** Techniques to keep track of frequencies of elements (e.g., counting how many times port 443 appears).
* **Why it matters:** Security reporting relies on aggregation (e.g., top 10 targeted ports, IP request rates).
* **How it works:**
  ```python
  # Method A: Manual Dictionary Counter
  protocol_counts = {}
  for proto in ["TCP", "UDP", "TCP"]:
      protocol_counts[proto] = protocol_counts.get(proto, 0) + 1

  # Method B: standard collections.Counter
  from collections import Counter
  counts = Counter(["TCP", "UDP", "TCP"])
  # Output: Counter({'TCP': 2, 'UDP': 1})
  ```

---

### 8. Error Handling (`try-except` blocks)
* **What it is:** Trapping runtime errors (exceptions) without letting the entire program crash.
* **Why it matters:** Real-world network logs are messy, incomplete, or corrupted. A parser shouldn't crash on line 5,000 of a 1,000,000 line log file due to one missing bracket.
* **How it works:**
  ```python
  try:
      with open("missing_file.json", "r") as f:
          data = json.load(f)
  except FileNotFoundError:
      print("Error: The requested log file was not found.")
  except json.JSONDecodeError:
      print("Error: The log file contains malformed JSON syntax.")
  ```

---

## Section 8.2 & 8.3: Basic Network Event Analyzer (Step-by-Step)

### Sample Dataset (`sample_events.json`)
Populate `day-05/python/sample_events.json` with the following initial dataset:

```json
[
  {
    "timestamp": "2026-10-13T09:00:00Z",
    "source": "192.0.2.10",
    "destination": "198.51.100.20",
    "destination_port": 443,
    "protocol": "TCP",
    "event": "connection_established"
  },
  {
    "timestamp": "2026-10-13T09:00:05Z",
    "source": "192.0.2.11",
    "destination": "198.51.100.20",
    "destination_port": 53,
    "protocol": "UDP",
    "event": "dns_query"
  },
  {
    "timestamp": "2026-10-13T09:00:10Z",
    "source": "192.0.2.12",
    "destination": "198.51.100.20",
    "destination_port": 443,
    "protocol": "TCP",
    "event": "connection_established"
  },
  {
    "timestamp": "2026-10-13T09:00:15Z",
    "source": "192.0.2.13",
    "destination": "198.51.100.20",
    "destination_port": 80,
    "protocol": "TCP",
    "event": "http_request"
  },
  {
    "timestamp": "2026-10-13T09:00:20Z",
    "source": "192.0.2.14",
    "destination": "198.51.100.20",
    "destination_port": 53,
    "protocol": "UDP",
    "event": "dns_query"
  }
]
```

---

### Basic Script (`network_event_analyzer.py`)
Below is a foundational script satisfying task requirement **8.2**:

```python
import json
from collections import Counter

def analyze_events(file_path):
    """
    Reads a JSON log file and prints event count, protocol frequency,
    and destination port distribution.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            events = json.load(file)
    except FileNotFoundError:
        print(f"[!] Error: File '{file_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"[!] Error: File '{file_path}' contains invalid JSON.")
        return

    # Initialize counters
    total_events = len(events)
    protocol_counter = Counter()
    port_counter = Counter()

    # Process events
    for event in events:
        # Extract protocol and port safely
        protocol = event.get("protocol", "UNKNOWN")
        port = event.get("destination_port", "UNKNOWN")

        protocol_counter[protocol] += 1
        port_counter[port] += 1

    # Display Report
    print("Network Event Summary")
    print("---------------------")
    print(f"Total events: {total_events}\n")

    print("Events by protocol:")
    for proto, count in protocol_counter.items():
        print(f"{proto}: {count}")

    print("\nEvents by destination port:")
    for port, count in port_counter.items():
        print(f"{port}: {count}")

if __name__ == "__main__":
    analyze_events("sample_events.json")
```

---

## Section 8.4: Extending the Analyzer (Robust Validation & Error Handling)

In real security operations, data is often incomplete, formatted improperly, or invalid. We need to add strict validation requirements:
1. Validate destination ports (integer between 1 and 65535).
2. Check for required log fields (`timestamp`, `source`, `destination`, `destination_port`, `protocol`, `event`).
3. Handle unknown or non-standard protocols.
4. Separate malformed/incomplete records from valid records.
5. Clearly mark reports as using synthetic training data.

> ⚠️ **Context Notice:** Never label a port or protocol as inherently "malicious." A connection on port 443 or port 80 is not malicious by virtue of its port number alone; context, payload, and threat intelligence dictate threat classification.

---

### Full Extended Code Walkthrough

Replace `network_event_analyzer.py` with this production-grade, modular analyzer script:

```python
#!/usr/bin/env python3
"""
Network Event Analyzer - Security Log Processor
Processes network traffic events from JSON logs, validates fields,
traps malformed entries, and generates summary metrics.

DISCLAIMER: All log data processed by this script is synthetic and fictional.
"""

import json
import sys
from collections import Counter

# Standard defined protocols
KNOWN_PROTOCOLS = {"TCP", "UDP", "ICMP", "IGMP", "SCTP"}
REQUIRED_FIELDS = {"timestamp", "source", "destination", "destination_port", "protocol", "event"}

def is_valid_port(port):
    """
    Validates whether destination_port is an integer in the valid range (1-65535).
    """
    if isinstance(port, int) and not isinstance(port, bool):
        return 1 <= port <= 65535
    return False

def validate_and_parse_event(event):
    """
    Validates log record schema and value constraints.
    Returns: (is_valid, reason)
    """
    if not isinstance(event, dict):
        return False, "Record is not a JSON object"

    # Check for missing required fields
    missing_fields = REQUIRED_FIELDS - set(event.keys())
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    # Validate Destination Port
    port = event.get("destination_port")
    if not is_valid_port(port):
        return False, f"Invalid destination port: {port}"

    return True, "Valid"

def process_log_file(file_path):
    """
    Ingests and classifies network event logs into valid and malformed sets.
    """
    valid_events = []
    malformed_records = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            if not isinstance(raw_data, list):
                print(f"[!] Critical Error: Root JSON element in '{file_path}' must be an array/list.")
                sys.exit(1)
    except FileNotFoundError:
        print(f"[!] Error: Specified log file '{file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError as err:
        print(f"[!] Error: Failed to parse JSON file '{file_path}'. Details: {err}")
        sys.exit(1)

    # Process individual entries
    for index, record in enumerate(raw_data, start=1):
        is_valid, reason = validate_and_parse_event(record)
        if is_valid:
            valid_events.append(record)
        else:
            malformed_records.append({
                "record_index": index,
                "record_data": record,
                "reason": reason
            })

    return valid_events, malformed_records

def generate_report(valid_events, malformed_records):
    """
    Prints structured analytical summary to stdout.
    """
    total_records = len(valid_events) + len(malformed_records)
    protocol_counts = Counter()
    port_counts = Counter()
    unknown_protocol_count = 0

    for ev in valid_events:
        protocol = str(ev.get("protocol")).upper()
        port = ev.get("destination_port")

        if protocol not in KNOWN_PROTOCOLS:
            unknown_protocol_count += 1
            protocol_counts[f"{protocol} (Unknown Protocol)"] += 1
        else:
            protocol_counts[protocol] += 1

        port_counts[port] += 1

    # Output Formatting
    print("==================================================")
    print("           NETWORK EVENT ANALYZER REPORT          ")
    print("==================================================")
    print("NOTICE: All analyzed data is synthetic/fictional.\n")
    
    print(f"Total Log Records Ingested : {total_records}")
    print(f"Valid Records Processed    : {len(valid_events)}")
    print(f"Malformed Records Dropped  : {len(malformed_records)}")
    print("--------------------------------------------------")

    print("\nEvents by Protocol:")
    if protocol_counts:
        for proto, count in protocol_counts.most_common():
            print(f"  - {proto}: {count}")
    else:
        print("  None")

    print("\nEvents by Destination Port:")
    if port_counts:
        for port, count in port_counts.most_common():
            print(f"  - Port {port}: {count}")
    else:
        print("  None")

    if malformed_records:
        print("\n--------------------------------------------------")
        print("Incomplete/Malformed Records Details:")
        for entry in malformed_records:
            print(f"  * Record #{entry['record_index']} Rejected -> Reason: {entry['reason']}")
            print(f"    Data: {entry['record_data']}")

    print("==================================================")

if __name__ == "__main__":
    file_target = "sample_events.json"
    valid_logs, rejected_logs = process_log_file(file_target)
    generate_report(valid_logs, rejected_logs)
```

---

## Section 8.5: Systematic Testing Strategy

To test data-analysis logic systematically, create an extended test dataset in `sample_events.json` containing edge cases and invalid entries:

### Comprehensive `sample_events.json` Test Data
Overwrite your `sample_events.json` with the test suite below:

```json
[
  {
    "timestamp": "2026-10-13T09:00:00Z",
    "source": "192.0.2.10",
    "destination": "198.51.100.20",
    "destination_port": 443,
    "protocol": "TCP",
    "event": "connection_established"
  },
  {
    "timestamp": "2026-10-13T09:01:00Z",
    "source": "192.0.2.11",
    "destination": "198.51.100.20",
    "protocol": "UDP",
    "event": "dns_query"
  },
  {
    "timestamp": "2026-10-13T09:02:00Z",
    "source": "192.0.2.12",
    "destination": "198.51.100.20",
    "destination_port": 80,
    "protocol": "CUSTOM_PROTO",
    "event": "raw_stream"
  },
  {
    "timestamp": "2026-10-13T09:03:00Z",
    "source": "192.0.2.13",
    "destination": "198.51.100.20",
    "destination_port": 99999,
    "protocol": "TCP",
    "event": "out_of_bounds_port"
  },
  "THIS_IS_A_MALFORMED_STRING_NOT_A_DICTIONARY",
  {
    "timestamp": "2026-10-13T09:05:00Z",
    "source": "192.0.2.14",
    "destination": "198.51.100.20",
    "destination_port": 53,
    "protocol": "UDP",
    "event": "dns_query"
  }
]
```

---

### Test Matrix

| Test Case # | Description / Condition | Input Data Characteristics | Expected Behavior / Outcome |
| :--- | :--- | :--- | :--- |
| **TC-01** | Normal Valid Event | Complete fields, Port 443, Protocol TCP | Added to `valid_events`, included in protocol and port counts. |
| **TC-02** | Missing Required Field | Missing `destination_port` field | Identified as malformed; rejected with "Missing required fields" reason. |
| **TC-03** | Unknown Protocol | Protocol set to `"CUSTOM_PROTO"` | Valid record accepted; protocol flagged as `CUSTOM_PROTO (Unknown Protocol)`. |
| **TC-04** | Invalid Destination Port | Port number set to `99999` (>65535) | Identified as malformed; rejected with "Invalid destination port" reason. |
| **TC-05** | Malformed Record Type | String entry instead of JSON object | Identified as malformed; rejected with "Record is not a JSON object" reason. |

---

### Sample Output Verification

Run the Python analyzer in your terminal:

```bash
python3 network_event_analyzer.py
```

#### Expected Execution Output:

```text
==================================================
           NETWORK EVENT ANALYZER REPORT          
==================================================
NOTICE: All analyzed data is synthetic/fictional.

Total Log Records Ingested : 6
Valid Records Processed    : 3
Malformed Records Dropped  : 3
--------------------------------------------------

Events by Protocol:
  - UDP: 1
  - TCP: 1
  - CUSTOM_PROTO (Unknown Protocol): 1

Events by Destination Port:
  - Port 443: 1
  - Port 80: 1
  - Port 53: 1

--------------------------------------------------
Incomplete/Malformed Records Details:
  * Record #2 Rejected -> Reason: Missing required fields: destination_port
    Data: {'timestamp': '2026-10-13T09:01:00Z', 'source': '192.0.2.11', 'destination': '198.51.100.20', 'protocol': 'UDP', 'event': 'dns_query'}
  * Record #4 Rejected -> Reason: Invalid destination port: 99999
    Data: {'timestamp': '2026-10-13T09:03:00Z', 'source': '192.0.2.13', 'destination': '198.51.100.20', 'destination_port': 99999, 'protocol': 'TCP', 'event': 'out_of_bounds_port'}
  * Record #5 Rejected -> Reason: Record is not a JSON object
    Data: THIS_IS_A_MALFORMED_STRING_NOT_A_DICTIONARY
==================================================
```

---

## Industry & Real-World Application

### Where This Fits in Security Engineering
1. **Log Ingestion Pipelines:** In enterprise Security Operations (SOC), log collectors built using Python, Go, or Logstash ingest millions of events per second. Filtering corrupted entries early prevents database corruption in SIEM platforms.
2. **Custom Detection Scripts:** Security Engineers build custom Python parsers when working with proprietary network appliances, microservices, or custom API integrations that lack out-of-the-box SIEM connectors.
3. **Automated Incident Response (SOAR):** When an alert triggers, SOAR playbooks execute Python routines to extract source IPs, validate ports, calculate query frequencies, and determine whether to block traffic or trigger analyst intervention.

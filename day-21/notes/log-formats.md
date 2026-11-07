# Technical Note: Enterprise Log Formats, Parsing & Streaming Architectures

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Insights

When building security ingestion pipelines, one of the first major engineering hurdles is dealing with data heterogeneity. Systems across an enterprise—from Linux servers and Windows domain controllers to firewalls and cloud APIs—do not speak the same language. 

If a Security Information and Event Management (SIEM) pipeline cannot correctly ingest, parse, and handle diverse log formats without crashing, the entire security monitoring posture collapses. Throughout my engineering work on Day 21, I have learned that understanding the underlying structure of **JSON, JSON Lines, Syslog, and Windows Event Logs** is just as important as writing the correlation logic itself. This technical note breaks down these four core formats, examines memory-efficient streaming strategies for Big Tech scale, and details essential Windows auditing event IDs.

---

## 2. JSON (JavaScript Object Notation): The Modern Standard

### What It Is & Why It Matters:
JSON is a lightweight data-interchange format built on key-value pairs and ordered lists (arrays). Unlike messy flat-text logs, JSON preserves native data types (strings, integers, booleans, and nested objects), making it the native format for modern security monitoring tools like Suricata EVE JSON and cloud audit trails.

### Engineering Advantages:
* **Structured Context:** Key-value pairs eliminate the need for brittle, complex regular expression (regex) parsing rules.
* **Native Programmatic Support:** Languages like Python parse JSON objects directly into dictionaries (`json.loads()`).

### Example Security JSON Object:
```json
{
  "timestamp": "2026-11-07T10:30:00Z",
  "event_type": "authentication_failure",
  "username": "alex",
  "source_ip": "192.0.2.25",
  "auth_metadata": {
    "protocol": "SSH",
    "port": 22
  }
}
```

---

## 3. JSON Lines (JSONL / NDJSON): Streaming Scale for Big Tech

### The Memory Scaling Problem:
When working with large log files in enterprise environments (gigabytes or terabytes of data), standard JSON files wrapped in a massive global array (`[...]`) present a severe operational risk: **Out-of-Memory (OOM) crashes**. If a script or parser attempts to load an entire 10 GB JSON file into RAM using `json.load()`, system memory is immediately exhausted.

### The JSONL Solution:
* **Newline-Delimited JSON (JSONL / NDJSON):** Stores one valid, independent JSON object per line, separated by a newline character (`\n`).
* **Streaming Architecture:** In my Python ingestion pipeline (`scripts/siem_pipeline.py`), JSONL allows line-by-line iteration (`for line in file:`), ensuring that memory consumption remains flat and constant regardless of whether the file contains 1,000 or 10,000,000 records.

### Example JSONL Stream:
```json
{"timestamp":"2026-11-07T10:30:00Z","event_type":"authentication_failure","username":"alex"}
{"timestamp":"2026-11-07T10:31:00Z","event_type":"authentication_success","username":"alex"}
{"timestamp":"2026-11-07T10:32:00Z","event_type":"network_connection","source_ip":"192.0.2.25"}
```

---

## 4. Syslog (RFC 5424 / RFC 3164): The Infrastructure Backbone

### Overview:
Syslog is the veteran standard protocol used across Linux systems, routers, firewalls, and network switches to transmit system messages over UDP or TCP to central log collectors.

### Core Anatomy of a Syslog Message:
1. **Priority (PRIVAL):** An integer wrapped in angle brackets (e.g., `<34>`) that encodes two vital metrics:
   * **Facility:** The subsystem generating the log (e.g., Kernel = 0, Mail = 2, Auth = 4, Daemon = 5).
   * **Severity:** Event criticality on a scale from 0 (Emergency) to 7 (Debug).
2. **Timestamp & Hostname:** When and where the event originated.
3. **App-Name / Tag:** The specific daemon (e.g., `sshd`, `iptables`).
4. **Message Body:** The unstructured text payload describing the action.

### Production Realities:
In real-world networks, different hardware vendors (Cisco, Juniper, Linux distros) frequently deviate slightly from strict RFC specifications. Robust ingestion pipelines must implement flexible parsing logic to handle message body variations without dropping records.

---

## 5. Windows Event Logs (`.EVTX` & XML)

### Overview:
Windows operating systems do not utilize flat-text syslog. Instead, they log system, security, and application events into structured binary event logs (`.evtx`), which are parsed into XML or JSON objects when forwarded to a SIEM.

### Critical Windows Security Event IDs for Analysts:
* **Event ID 4624:** Successful Logon (Monitors account logons and logon types such as Interactive, Network, or RemoteInteractive/RDP).
* **Event ID 4625:** Failed Logon (Essential for detecting brute-force attacks, password spraying, and unauthorized access attempts).
* **Event ID 4634:** Account Logoff.
* **Event ID 4672:** Special Privileges Assigned to New Logon (Fires when administrative accounts like Administrator or SYSTEM establish a session).
* **Event ID 4688:** Process Creation (Logs every new process spawned on the system, critical for tracking command-line arguments and script execution).
* **Event ID 1102:** Audit Log Cleared (High-severity indicator that an adversary or malicious insider is attempting to destroy forensic evidence).

---

## 6. Summary Checklist for Portfolio Verification

| Log Format | Primary Use Case | Engineering Advantage | Ingestion Consideration |
| :--- | :--- | :--- | :--- |
| **JSON** | Cloud audit trails, Suricata alerts, API responses. | Native key-value structure; eliminates complex regex. | Nested objects require flattening during normalization. |
| **JSONL / NDJSON** | High-volume log streams, SIEM data lakes. | Line-by-line processing prevents OOM memory crashes. | Requires strict syntax validation per line. |
| **Syslog** | Linux servers, firewalls, network switches. | Ubiquitous infrastructure support. | Vendor format variations require flexible parsing rules. |
| **Windows EVTX / XML** | Windows endpoint and domain controller auditing. | Rich security context (Logon types, process creation). | High log volume requires aggressive filtering and indexing. |

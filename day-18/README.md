# Day 18: Network Security Monitoring & Intrusion Detection with Suricata

## Overview

Welcome to my **Day 18** .Yesterday on Day 17, I focused on perimeter defense and network controls (firewalls, routing, NAT, and ACLs). Today, I shifted from controlling traffic to **monitoring traffic**, detecting anomalous activity, and analyzing structured security telemetry.

This repository documents my hands-on experience setting up **Suricata** as a Network Intrusion Detection System (NIDS), writing custom signature rules, running offline packet analysis on custom PCAP files, inspecting structured **EVE JSON** logs, and automating log triage using a custom Python script.

---

## Learning Objectives

- **Understand NSM Architecture:** Grasp the operational differences between Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS), passive vs. inline deployment, and NIDS vs. HIDS.
- **Master Detection Engineering:** Learn the anatomy of Suricata signatures, including actions, transport headers, flow state tracking, rule options, SIDs, and thresholds.
- **Telemetry & Log Analysis:** Interpret structured JSON events (`eve.json`) and flat alert logs (`fast.log`) to distinguish true security incidents from false positives.
- **Offline Forensic Analysis:** Replay custom PCAP files through Suricata to perform post-mortem network investigations.
- **Python Security Automation:** Build a standalone Python triage tool (`suricata_triage.py`) to parse, aggregate, and highlight high-priority Suricata alerts.

---

## Tools & Technologies Used

- **Operating System:** Parrot OS (Linux virtual workstation environment)
- **Detection Engine:** Suricata (Open-source NIDS/IPS engine)
- **Packet Capture & Inspection:** Wireshark, `tcpdump`
- **Scripting & Automation:** Python 3 (standard libraries: `json`, `sys`, `collections`, `pathlib`)
- **Version Control:** Git & GitHub

---

## Project Folder Structure

```text
day-18/
├── README.md
├── notes/
│   ├── nsm-architecture.md
│   ├── suricata-rules.md
│   └── eve-json-telemetry.md
├── rules/
│   └── local.rules
├── lab/
│   ├── captures/
│   │   └── dns-security-investigation.pcapng
│   └── data/
│       └── eve.json
├── src/
│   └── suricata_triage.py
├── reports/
│   └── nsm-investigation.md
└── screenshots/
    ├── 131-suricata-installation.png
    ├── 132-custom-rule-configuration.png
    ├── 133-pcap-replay-execution.png
    ├── 134-eve-json-inspection.png
    └── 135-python-triage-output.png
```

---

## Key Hands-On Activities & Findings

### 1. Suricata Installation & Configuration
- Installed Suricata on Parrot OS and verified system dependencies and default rule directory configurations (`/etc/suricata/`).
- Confirmed multi-threaded packet processing capabilities and configured log output parameters for structured EVE JSON output.

### 2. Custom Detection Rule Engineering
- Created custom signature rules targeting specific application-layer traffic patterns and suspicious DNS queries.
- Utilized stateful flow tracking (`flow:to_server,established`) and frequency thresholding to prevent alert fatigue.

### 3. PCAP Replay & EVE JSON Analysis
- Captured live DNS and network traffic using Wireshark and `tcpdump`.
- Processed the PCAP file offline using `suricata -r` to simulate forensic threat hunting.
- Analyzed `eve.json` log entries, extracting detailed metadata including source/destination IP addresses, flow IDs, protocol headers, and alert severity classifications.

### 4. Automated Python Telemetry Triage
- Developed `suricata_triage.py` to automatically ingest and parse multi-line EVE JSON records.
- Summarized top triggered alert categories, identified offending source IP addresses, and isolated high-frequency alert patterns.

---

## Limitations & Real-World Context

- **Synthetic & Lab Data:** Testing was conducted within an isolated lab environment using generated PCAP captures.
- **No Encrypted Payload Inspection:** Suricata inspected unencrypted packet headers and metadata; inspecting TLS-encrypted payload content in production requires dedicated SSL/TLS decryption proxies.
- **Correlation Requirement:** A triggered IDS alert indicates that a rule matched, not necessarily that an endpoint was compromised. Real-world triage requires correlating network telemetry with endpoint logs (Sysmon/EDR) and identity provider context.

---

## Safety and Scope

All activities documented in this project were performed strictly on authorized lab systems, private virtual machine instances, and synthetic packet captures. No public networks or unauthorized infrastructure were scanned or monitored.

---

## Author

**Serah Kathini**  
*Cybersecurity & Digital Marketing Specialist | Women Techsters Fellow*  
*Passionate about SOC operations, security engineering, and threat analysis.*

# Day 18: Network Security Monitoring & Intrusion Detection System (NIDS) Lab

**Author:** Serah Mulwa  

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection  

---

## Executive Overview

This repository houses a comprehensive, portfolio-ready Network Security Monitoring (NSM) and Intrusion Detection System (IDS) practical project. 

The primary objective of this lab is to demonstrate end-to-end network traffic inspection: capturing live DNS protocol traffic, dissecting packet headers in Wireshark, authoring custom Suricata detection rules, replaying captures offline, parsing EVE JSON security telemetry, and building a custom Python log analysis automation tool.

```
+------------------+     +--------------------+     +-----------------------+
|  tcpdump / PCAP  | --> | Suricata Engine    | --> | EVE JSON Telemetry    |
| (Packet Capture) |     | (Local Rule: DNS)  |     | (output/eve.json)     |
+------------------+     +--------------------+     +-----------------------+
                                                                |
                                                                v
                                                    +-----------------------+
                                                    | Python EVE Analyser   |
                                                    | (src/eve_summary.py)  |
                                                    +-----------------------+
```

---

## Repository Structure

```text
day18-network-security-monitoring/
│
├── README.md                                    <- Master portfolio overview (this file)
├── .gitignore                                   <- Protects sensitive PCAPs and raw logs
│
├── notes/                                       <- Core technical documentation
│   ├── nsm-architecture.md                      <- IDS vs. IPS, NIDS vs. HIDS foundations
│   ├── suricata-rules.md                        <- Custom rule syntax & signature engineering
│   ├── pcap-analysis.md                         <- Wireshark packet analysis findings
│   ├── offline-analysis.md                      <- Offline PCAP replay & EVE JSON telemetry
│   ├── eve-analyzer.md                          <- Python EVE log analyzer documentation
│   ├── detection-engineering.md                 <- Rule quality, tuning, & Suricata vs Zeek
│   └── alert-triage.md                          <- SOC 5-stage alert triage framework
│
├── rules/
│   └── local.rules                              <- Custom Suricata detection rule (SID: 1000001)
│
├── src/
│   └── eve_summary.py                           <- Standalone Python EVE JSON log parser
│
├── reports/
│   └── network-monitoring-investigation.md      <- Formal SOC incident triage report
│
└── screenshots/                                 <- Forensic evidence screenshots
    ├── 131-suricata-version.png
    ├── 141-wireshark-dns-packet-overview.png
    ├── 144-suricata-custom-rule-syntax-test-passed.png
    ├── 145-suricata-offline-output-directory-and-logs.png
    ├── 146-jq-eve-json-alert-matching.png
    └── 149-python-eve-summary-script-execution.png
```

---

## Key Achievements & Technical Deliverables

1. **Environment Setup & Audit:** Validated host NIDS deployment running Suricata `7.0.10` on Parrot Security OS.
2. **Live Traffic Capture:** Captured raw DNS requests using `tcpdump` into `pcap/dns-example.pcap`.
3. **Wireshark Deep Packet Inspection:** Analyzed transaction IDs, query types (`A`, `AAAA`), response flags, and hex payloads.
4. **Signature Engineering:** Authored a local detection rule (`sid:1000001;`) targeting DNS queries for `example.com` and validated syntax via `suricata -T`.
5. **Offline Analysis & Telemetry Generation:** Replayed PCAPs using `suricata -r`, generating structured `eve.json` telemetry.
6. **Command-Line Telemetry Parsing:** Filtered alerts and protocol events using `jq`.
7. **Python Automation Tool:** Developed a self-contained log parser (`src/eve_summary.py`) utilizing `json`, `collections.Counter`, and `pathlib.Path` with defensive exception handling (`try...except`).

---

## Security & Privacy Considerations

This repository adheres to operational security best practices. Raw packet captures (`*.pcap`), raw log files (`*.log`), and temporary outputs (`output/`) are excluded via `.gitignore` to prevent leaking private IP addresses or network metadata.

---

## How to Run the Python Analyser

To execute the Python EVE JSON analyzer against generated telemetry:

```bash
python3 src/eve_summary.py output/suricata/eve.json
```

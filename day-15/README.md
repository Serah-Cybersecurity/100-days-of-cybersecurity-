# Day 15 - Network Traffic Analysis, TShark Automation & Forensic Reporting

## Executive Overview

Day 15 of my Cybersecurity Journey focuses on advanced network traffic analysis (NTA), packet structure dissection, CLI automation using Python and TShark, systematic tool validation, multi-source SIEM log correlation, and professional forensic reporting.

Rather than relying solely on graphical user interfaces, this module demonstrates the ability to programmatically parse packet metadata, build testable security utilities with robust error handling, and produce objective incident investigation deliverables.

---

## 1. Automated TShark Metadata Utility (`pcap_summary.py`)

A custom command-line Python utility designed for Security Operations Center (SOC) pipelines. It interacts with the system's TShark binary to extract structural metadata (`frame.number`, `frame.len`, protocol names, source/destination IPs, and TCP/UDP ports) without inspecting sensitive application payloads.

### Key Features:
* **Executable Safety:** Verifies TShark installation via `shutil.which()`.
* **Injection Prevention:** Invokes `subprocess.run()` using explicit argument lists (avoiding `shell=True`).
* **Structured Parsing:** Utilizes `csv.DictReader` to convert comma-separated TShark output into clean Python dictionaries.
* **Statistical Aggregation:** Leverages `collections.Counter` to compute protocol distributions, top talkers, and communication pairs.
* **Robust Exception Handling:** Catches missing files or invalid formats, outputting clean error messages and returning **Exit Code 2**.

---

## 2. Systematic Testing & Validation Matrix

The automation script and environment were subjected to an 8-stage rigorous test suite on Parrot OS:

| Test ID | Objective | Command / Tool | Status |
| :--- | :--- | :--- | :--- |
| **TEST 1** | Python Version Check | `python3 --version` (v3.11+) | ✅ Passed |
| **TEST 2** | Syntax Compilation | `python3 -m py_compile pcap_summary.py` | ✅ Passed |
| **TEST 3** | TShark Binary Path | `command -v tshark` (`/usr/bin/tshark`) | ✅ Passed |
| **TEST 4** | Low-Level Metadata | `capinfos http_redirects.pcapng` (271 packets, ~47 KB) | ✅ Passed |
| **TEST 5** | Cryptographic Baseline | `sha256sum` (`ff432a6b71d06cd20720...`) | ✅ Passed |
| **TEST 6** | Functional Execution | `python3 pcap_summary.py http_redirects.pcapng` | ✅ Passed |
| **TEST 7** | Missing File Handling | `missing.pcapng` $\rightarrow$ Caught, Exit Code `2` | ✅ Passed |
| **TEST 8** | Corrupted Input | `invalid-capture.txt` $\rightarrow$ Caught, Exit Code `2` | ✅ Passed |

---

## 3. Comprehensive Documentation & Knowledge Base

The `notes/` directory contains complete, peer-ready markdown modules explaining the *what*, *why*, *how*, and *job market applications* for every core concept:
* **Packet Anatomy & Encapsulation:** Deep dive into OSI layers, MAC addresses, IPv4 vs. IPv6 headers, TCP/UDP transport differences, and the 5-Tuple.
* **Protocol Analysis:** Detailed breakdowns of TCP session states, DNS record types (A, AAAA, CNAME, MX, TXT), and HTTP/TLS handshake structures.
* **Wireshark Filter Reference:** Documenting exact display filters (`tcp`, `http`, `dns`, `icmp`, `arp`, `tcp.analysis.retransmission`, `http.response.code == 302`, `ip.addr`) with analyst rationale and forensic limitations.
* **SIEM Correlation:** Multi-source log correlation linking Windows Event Logs, Sysmon Event ID 1, firewall rules, DNS records, and PCAP data while avoiding temporal fallacies.

---

## 4. Professional Investigation Deliverable

The `reports/packet-analysis-report.md` file serves as an executive-ready Incident Investigation Report (`DAY15-NTA-001`) conducted by **Serah Kathini Mulwa**. It follows strict forensic standards:
* **Chain of Custody:** Documents SHA-256 integrity hashes and file size parameters.
* **Separation of Findings:** Strictly separates factual technical observations from analytical interpretations.
* **Operational Limitations:** Outlines interface boundaries, missing host context, and encryption constraints.
* **Evidence-Based Conclusion:** Concludes objectively without making unsupported assumptions of malicious activity.

---

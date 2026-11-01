# Day 5: Network Analysis, Python Scripting, and Evidence-Based Investigation

## 1. Project Overview
Day 5 of the cybersecurity curriculum bridges foundational networking protocols (DNS, TCP/UDP, HTTP/HTTPS) with practical command-line diagnostics, Python log analysis, and rigorous evidence-based incident investigation. Operating in a hybrid environment (Windows Host running Parrot OS via VirtualBox shared folders), this project demonstrates how to inspect network telemetry, parse JSON logs safely, and structure professional incident reports without making unverified assumptions.

---

## 2. Resources Used
* **Operating Systems & Environment:**
  * Host OS: Microsoft Windows (Base System)
  * Guest OS: Parrot OS Security Edition (running inside Oracle VirtualBox with bidirectional shared folder mounting `sf_cyber-repo`)
* **Core Tools & Utilities:**
  * Wireshark (Packet analysis, display filters, protocol inspection)
  * Linux Command Line Utilities (`ss`, `ip`, `ping`, `getent`)
  * Python 3 (Custom log analysis script with input validation and error handling)
* **Learning Platforms & Curriculum:**
  * TryHackMe (Pre Security Path & Network Fundamentals modules)
  * Microsoft Learn (Fundamentals of Computer Networking module)
* **Documentation & Version Control:**
  * Git & GitHub (Repository structure, version tracking, and remote code synchronization)

---

## 3. What Was Learned
* **Network Interfacing & Troubleshooting:** How to inspect network interfaces, routing tables, and active listening sockets using Linux CLI tools.
* **Packet Capture Analysis:** Using Wireshark to filter and examine DNS queries, TCP handshakes, and application layer traffic.
* **Defensive Python Scripting:** Writing a robust log parser (`network_event_analyzer.py`) capable of handling schema validation, port bounds checking, and malformed records gracefully without crashing.
* **Evidence-Based Analytical Reasoning:** Mastering the distinction between **Observation** (raw facts), **Interpretation** (testable hypotheses), and **Conclusion** (bounded findings) to prevent false positives and confirmation bias in incident response.

---

## 4. Technical Implementation & Python Analyzer
The Python script (`network_event_analyzer.py`) processes synthetic network logs (`sample_events.json`) by performing the following steps:
1. **Ingestion:** Reads JSON log records from the local directory.
2. **Schema & Input Validation:** Verifies required keys, validates integer port ranges ($1 \le \text{port} \le 65535$), and catches malformed data types.
3. **Aggregation:** Counts valid records by protocol (TCP vs. UDP) and destination ports (Ports 22, 53, 80, 443).
4. **Audit Logging:** Isolates and logs malformed or out-of-range records into a rejection audit trail.

---

## 5. Investigation Summary & Limitations
* **Scenario:** An alert indicated that training host `192.0.2.10` communicated with an unfamiliar destination (`198.51.100.20`).
* **What the Data Establishes:** Confirms 7 valid connection events across standard transport ports and isolates 3 malformed records.
* **Analytical Conclusion:** The available network metadata is **INSUFFICIENT** to establish whether the activity is malicious or benign. Without Layer 7 payload inspection (PCAP/TLS SNI) and host endpoint process trees (EDR/Sysmon), intent cannot be proven.

---

## 6. How to Reproduce This Exercise
1. Clone the repository into your local or virtual environment:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/100-DAYS-OF-CYBERSECURITY-From-Scratch-.git](https://github.com/YOUR-USERNAME/100-DAYS-OF-CYBERSECURITY-From-Scratch-.git)

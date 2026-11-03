# Day 15 - TShark Python Automation & PCAP Metadata Summarization

## Overview
While graphical user interfaces like Wireshark are ideal for manual incident investigations, enterprise Security Operations Centers (SOCs) require programmatic automation to parse, summarize, and triage packet captures at scale.

This module documents the creation and execution of `pcap_summary.py`, a custom command-line Python utility that leverages `tshark` under the hood to extract structured network metadata from offline `.pcap` / `.pcapng` files without inspecting sensitive application payloads.

---

## 1. Utility Architecture & Script Mechanics

The `pcap_summary.py` script bridges command-line packet extraction with statistical Python aggregation:

* **Executable Verification (`shutil.which`):** Programmatically ensures `tshark` is installed in the system PATH before execution.
* **Subprocess Execution (`subprocess.run`):** Calls `tshark` as a child process using explicit list parameters (`-T fields -E header=y -E separator=,`) to avoid command-injection vulnerabilities.
* **Structured Parsing (`csv.DictReader`):** Ingests comma-separated TShark stdout directly into Python dictionaries for fast key-value querying.
* **Statistical Aggregation (`collections.Counter`):** Calculates protocol distribution, top talkers, and endpoint communication pairs (`Source <-> Destination`).

---

## 2. Terminal Execution & Verification

### Command Executed:
```bash
cd ~/cybersecurity-journey
chmod +x day-15/scripts/pcap_summary.py
python3 day-15/scripts/pcap_summary.py day-15/lab/data/http_redirects.pcapng
```
---

## 3. Extracted Summary Metrics

* **Total Packets Analyzed:** 271
* **Total Volume:** 38,512 bytes
* **Primary Source/Destination Endpoint:** `127.0.0.1` (Local Loopback)
* **Top Communication Pairs:** `127.0.0.1:47662 <-> 127.0.0.1:80` (6 packets per stream)

---

## 4. Scope, Limitations & Privacy Safeguards

> ⚠️ **Important Technical Limitations:**
> 1. **Metadata Only:** This tool extracts structural headers (IPs, ports, protocols, packet lengths). It does **not** inspect or extract raw application payloads, credentials, or decrypted session text.
> 2. **Context-Dependent:** High packet volume or frequent endpoint pairs do **not** automatically indicate malicious activity. Threat determination requires contextual correlation with SIEM alerts, threat intelligence, and host logs.

---

## 5. Job Market & Enterprise Application
In security engineering and SOC automation, Python scripts wrapping TShark or Zeek CLI tools are used in automated Incident Response pipelines. When an intrusion detection system (IDS) flags an endpoint, an automated playbook invokes scripts like `pcap_summary.py` to extract a metadata summary and attach it directly to the alert ticket for rapid analyst triage.

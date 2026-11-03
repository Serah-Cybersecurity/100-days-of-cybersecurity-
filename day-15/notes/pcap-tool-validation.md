# Day 15 - Systematic Testing & Validation of TShark Analysis Utility

## Overview

In enterprise security engineering and SOC playbook automation, custom scripts must undergo systematic verification before deployment into production environments. A utility used during incident response must fail gracefully when encountering missing or corrupted input files and return precise operating system exit codes to orchestrators.

This module documents the comprehensive 8-stage testing framework executed against `pcap_summary.py` on Parrot OS, establishing Python environment health, syntax integrity, low-level PCAP metadata verification via `capinfos`, cryptographic baselining, functional execution, and error handling.

---

## 1. Test Suite Framework & Execution Matrix

| Test ID | Test Objective | Execution Command | Target Input / Context | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TEST 1** | Python Environment Check | `python3 --version` | Local Parrot OS | Python `3.11+` | ✅ PASSED |
| **TEST 2** | Code Syntax Compilation | `python3 -m py_compile ...` | `pcap_summary.py` | Silent exit (Zero syntax errors) | ✅ PASSED |
| **TEST 3** | TShark Binary Check | `command -v tshark` | System PATH | `/usr/bin/tshark` | ✅ PASSED |
| **TEST 4** | Low-Level Metadata | `capinfos ...` | `http_redirects.pcapng` | Header metadata & 271 packet count | ✅ PASSED |
| **TEST 5** | Forensic Integrity Baseline | `sha256sum ...` | `http_redirects.pcapng` | `ff432a6b71d06cd20720...` | ✅ PASSED |
| **TEST 6** | Functional Summary Run | `python3 pcap_summary.py ...` | `http_redirects.pcapng` | Clean stdout statistical summary | ✅ PASSED |
| **TEST 7** | Missing File Handling | `python3 pcap_summary.py ...` | `missing.pcapng` | `ERROR: Capture file does not exist` (Exit 2) | ✅ PASSED |
| **TEST 8** | Corrupted Input Handling | `python3 pcap_summary.py ...` | `invalid-capture.txt` | `ERROR: tshark: ... isn't a capture file` (Exit 2) | ✅ PASSED |

---

## 2. Low-Level Capture Metadata & Forensic Baseline

### 2.1 `capinfos` Header Extraction (Test 4)
Executing `capinfos` against the primary exercise capture established the following physical and temporal baseline without processing higher-level protocol structures:

* **Target File:** `day-15/lab/data/http_redirects.pcapng`
* **File Type:** `Wireshark/... - pcapng`
* **File Encapsulation:** `Ethernet`
* **Packet Count:** `271`
* **File Size:** `47 kB` (Data size: `38 kB`)
* **Capture Duration:** `53018.5296` seconds
* **Time Range:** `2018-03-28 02:37:41` to `2018-03-28 17:21:20`

### 2.2 Cryptographic Hash Verification (Test 5)
To preserve the legal chain of custody and verify post-execution file integrity:
* **SHA-256 Fingerprint:** `ff432a6b71d06cd20720f7763e584014edd0a43c3b55981c682d1b7640207abc`
* **SHA-1 Fingerprint:** `281b85eebcbeda5d47fe146c5223f1cff96405a0`

> **Forensic Note:** Re-computing `sha256sum` post-testing confirmed zero bytes were modified by our Python execution pipeline.


---

## 3. Key Learnings & SOC Automation Value

1. **Non-Zero Exit Codes for SOAR Compatibility:** Returning `exit code 2` upon handling caught exceptions (`FileNotFoundError`, `RuntimeError`) allows Security Orchestration, Automation, and Response (SOAR) engines to catch pipeline failures cleanly rather than hanging on broken processes.
2. **Defensive Shell Execution:** Building command lists for `subprocess.run` without using `shell=True` ensures input filenames are safely treated as arguments rather than executable shell code.
3. **Decoupled Verification:** Validating PCAP characteristics via `capinfos` independently of custom scripts ensures analysts can distinguish between tool bugs and raw data anomalies.

# Day 15 - Technical Setup, Environment Verification & TShark Mastery

## Overview

Before diving into advanced network packet analysis, establishing a reliable, verified, and standardized engineering environment is essential. For a Security Operations Centre (SOC) analyst, verifying tool availability, dependency integrity, and command-line execution readiness ensures that your forensic workflows run smoothly during live incident triage.

This module documents the technical setup of Wireshark, TShark, and Python 3 within our Parrot OS virtualized environment.

---

## 1. Environment Architecture & Tool Stack

Our Day 15 lab environment consists of:
* **Operating System:** Parrot OS (Debian-based Linux Security Distribution running in Oracle VirtualBox).
* **Core Analyzers:** Wireshark v4.4.15 (GUI Protocol Analyzer) & TShark v4.4.15 (Headless Command-Line Protocol Analyzer).
* **Automation Runtime:** Python 3.x for custom packet parsing and TShark automation scripts.

---

## 2. Environment Verification & Binary Checks

To verify that packet analysis tools are accessible in the system's execution path (`$PATH`), we execute binary verification commands in the Parrot OS terminal.

### 2.1 Checking Binary Paths
Run the `command -v` utility to locate the binary executables:

```bash
command -v wireshark
command -v tshark
command -v capinfos
```

* **What this does:** Queries the shell environment to locate where each tool is installed without launching the application.
* **Observed Output:** Successfully resolved to `/usr/bin/wireshark`, `/usr/bin/tshark`, and `/usr/bin/capinfos`.

### 2.2 Verifying Software Versions
To ensure our packet dissection libraries support modern `.pcap` and `.pcapng` formats, we check the version baseline:

```bash
wireshark --version
tshark --version
capinfos --version
```

* **Observed Output:** Both Wireshark and TShark confirmed version `4.4.15`, ensuring complete compatibility between graphical and command-line analysis.

---

## 3. Package Management & Installation

If tools are missing or require updates on Debian-based systems like Parrot OS, standard package management (`apt`) is utilized.

### 3.1 Updating Repositories and Installing Packages
```bash
sudo apt update
sudo apt install wireshark tshark
```

* **Lab Observation:** The package manager successfully processed dependencies, upgrading internal shared libraries (`libwireshark18`, `libwiretap15`, `libwsutil16`) and confirming a clean installation.
* **Security Best Practice:** During installation prompts regarding non-superuser packet capture privileges, selecting **No** ensures that standard user accounts adhere to the principle of least privilege, as offline PCAP analysis does not require raw socket sniffing capabilities.

---

## 4. Introduction to TShark (Command-Line Packet Analysis)

While Wireshark provides a robust graphical interface, **TShark** is its headless, command-line counterpart.

### Why TShark is Critical for SOC Analysts:
1. **Automation & Scripting:** TShark outputs clean text streams that can be piped into shell scripts or parsed programmatically using Python.
2. **Headless Operations:** Ideal for remote Linux servers, cloud triage instances, and automated CI/CD security pipelines.
3. **Batch Processing:** Enables analysts to process hundreds of historical PCAP files in seconds via simple loops.

---

## 5. Job Market Application

In modern SOC environments, security engineers and automation analysts rarely rely solely on desktop GUIs. Being able to leverage TShark via command-line scripts allows teams to automatically parse incoming sensor captures, extract indicators of compromise (IOCs), and feed structured telemetry directly into SIEM platforms for rapid threat detection.

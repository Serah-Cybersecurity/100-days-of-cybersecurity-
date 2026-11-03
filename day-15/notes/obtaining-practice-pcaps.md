# Day 15 - Obtaining & Managing Practice Packet Captures

## Overview

In digital forensics and incident response (DFIR), raw packet telemetry serves as primary evidence. Rather than conducting live packet captures on production environments—which introduces noise, legal implications, and privacy risks—analysts utilize pre-recorded packet captures (`.pcap` / `.pcapng`) to practice protocol analysis and threat hunting.

This module covers the acquisition of standardized practice capture files, proper lab directory architecture, and cryptographic evidence hashing.

---

## 1. Practice PCAP Sources

| Source / Resource | File Name | Primary Analysis Focus |
| :--- | :--- | :--- |
| **TryHackMe:** *Wireshark: The Basics* | `Exercise.pcapng` | Primary practice capture for protocol navigation, display filter evaluation, and guided lab questions. |
| **Wireshark Foundation Samples** | `http_redirects.pcapng` | Secondary exercise capture containing TCP streams and HTTP 302 redirection chains. |

---

## 2. Evidence Acquisition & Cryptographic Hashing

### 2.1 Downloading the Practice Capture
To acquire the official Wireshark sample capture for HTTP redirection analysis, execute `wget` within the lab data directory:

```bash
cd ~/cybersecurity-journey/day-15/lab/data
wget https://wiki.wireshark.org/uploads/__moin_import__/attachments/SampleCaptures/http_redirects.pcapng
```

### 2.2 Verification of Chain of Custody (SHA-256)
Before conducting analysis, compute the SHA-256 cryptographic hash to establish an unalterable forensic baseline:

```bash
sha256sum http_redirects.pcapng
```

* **Target File:** `http_redirects.pcapng`
* **Recorded SHA-256 Hash:** `ff432a6b71d06cd20720f7763e584014edd0a43c3b55981c682d1b7640207abc`

>  **Forensic Note:** Any post-acquisition modification to `http_redirects.pcapng` will alter this hash value, signaling evidence corruption or tampering.

---


## 3. Job Market Application

In enterprise Security Operations Centers (SOCs), network taps and intrusion detection systems (IDS) write automated PCAP slices to remote storage when alerts trigger. Analysts retrieve these static PCAP files, compute cryptographic hashes to verify integrity, and load them into headless command-line tools or analytical sandboxes. Demonstrating this exact acquisition and hashing workflow reflects real-world DFIR standards.

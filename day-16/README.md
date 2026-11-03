# Day 16 - DNS Security, Investigation & Threat Detection

## Executive Overview

Day 16 of my Cybersecurity Journey focuses on mastering the **Domain Name System (DNS)** from a defensive security perspective. Building directly on yesterday's network traffic analysis foundation, this module explores the complete DNS resolution hierarchy, core resource records (`A`, `AAAA`, `CNAME`, `MX`, `TXT`), command-line forensic tools (`dig`, `nslookup`, `Resolve-DnsName`), Wireshark packet inspection, and threat detection techniques for identifying DNS abuse such as tunneling and Domain Generation Algorithms (DGA).

Rather than relying purely on theoretical knowledge, this module establishes structured analytical frameworks for Security Operations Center (SOC) analysts to triage anomalous DNS telemetry.

## Repository Structure

```
day-16/
├── lab/
│   └── data/                 # Sample practice DNS capture files (.pcapng)
├── scripts/                  # Custom DNS investigation utilities
├── tests/                    # Script validation suites and error-handling tests
├── screenshots/              # Terminal execution and tool evidence captures
├── notes/                    # Comprehensive technical knowledge base (.md)
│   └── dns-security-fundamentals.md
├── reports/                  # Executive-level DNS incident investigation reports
└── README.md                 # Day 16 specific master landing page (this file)

```

## 1. Core Learning Objectives & Modules

* **DNS Hierarchy & Resolution:** Mastering the 4-tier resolution path from stub resolvers and recursive resolvers to root, TLD, and authoritative name servers.
* **Protocol Record Analysis:** Deep-dive examination of `A`, `AAAA`, `CNAME`, `MX`, and `TXT` records, paying special attention to high-risk abuse vectors like DNS tunneling.
* **CLI Diagnostic Mastery:** Using `dig` (with `+trace` and specific server queries), `nslookup`, and PowerShell's `Resolve-DnsName` to inspect live and offline DNS infrastructure.
* **Advanced Concepts:** Evaluating Time To Live (TTL) manipulation in Fast Flux networks, DNSSEC cryptographic verification, and the operational security challenges introduced by DoH (DNS over HTTPS) and DoT (DNS over TLS).

## 2. Threat Detection & SOC Analysis

* **Domain Generation Algorithms (DGA):** Identifying malware command-and-control communication characterized by massive spikes in `NXDOMAIN` (RCODE 3) responses from randomized subdomains.
* **DNS Exfiltration & Tunneling:** Recognizing encoded data smuggling over `TXT` or high-entropy subdomain queries that bypass perimeter firewalls.
* **MITRE ATT&CK Alignment:** Mapping DNS-based threats to adversary tactics such as Command and Control (T1071.004 - Application Layer Protocol: DNS) and Exfiltration (T1048 - Exfiltration Over Alternative Protocol).

## 3. Professional Standards & Analyst Habits

* Never assuming single queries indicate compromise without contextual correlation.
* Normalizing timestamps to UTC across resolver logs, firewall records, and endpoint telemetry.
* Preserving evidence integrity and documenting analysis steps systematically.

## Author & Fellowship Information

* **Analyst & Engineer:** Serah Mulwa
* **Core Curriculum:** Cybersecurity Journey - 100 Days From Scratch (Day 16)

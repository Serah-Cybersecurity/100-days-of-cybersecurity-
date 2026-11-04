# Day 17 — Network Control & Boundary Defence (DHCP, ARP, Routing, NAT, Firewalls, and Log Analysis)

**Author:** Serah Mulwa    
**Date:** November 4, 2026  
**Module:** Day 17 - Network Control & Boundary Defence  

---

## 1. Overview

Day 17 bridges the gap between low-level packet observation (Day 15) and application-layer telemetry analysis (Day 16) by exploring the core infrastructure that dictates how network devices obtain identities, resolve neighbors, route packets, and enforce perimeter security boundaries. This project documents practical network configuration inventories, core theoretical breakdowns, packet journey mappings, firewall rule evaluation principles, and a custom Python firewall log analysis utility.

---

## 2. Learning Objectives

* **DHCP Mechanics:** Explain how devices obtain dynamic network configurations through the DORA (Discover, Offer, Request, Acknowledge) process and troubleshoot lease failures.
* **ARP Resolution:** Understand how IPv4 devices discover local MAC addresses and examine local ARP cache tables.
* **Routing & Gateways:** Identify system default gateways and trace packet path selection across subnets using routing tables.
* **NAT Operations:** Explain how private RFC 1918 addresses are translated via SNAT, DNAT, and PAT for external communication.
* **Firewalls & ACLs:** Distinguish between stateful and stateless packet filtering, evaluate sequential access control lists (ACLs), and understand implicit deny rules.
* **Network Troubleshooting:** Apply a methodical, bottom-up troubleshooting methodology to isolate addressing, neighbor-resolution, and routing problems.
* **Log Analysis & Automation:** Build and test a custom Python script to ingest, parse, and analyze firewall event logs.

---

## 3. Environment & Tools

* **Host Operating System:** Windows / Linux Mint Base
* **Virtualization:** Oracle VirtualBox
* **Guest Operating System:** Parrot Security OS
* **Network Utilities:** `ip`, `route`, `arp`, `ping`, `traceroute`, `iptables`
* **Programming Language:** Python 3 (Standard Library: `argparse`, `json`, `ipaddress`, `pathlib`, `collections`)

---

## 4. Directory Structure

```text
day-17/
├── README.md
├── notes/
│   ├── network-inventory.md
│   ├── core-networking-theory.md
│   └── firewall-fundamentals.md
├── diagrams/
│   └── packet-journey.md
├── lab/
│   └── data/
│       └── firewall-events.log
├── scripts/
│   └── firewall_analyzer.py
├── reports/
│   ├── firewall-investigation-report.md
│   └── test-results.md
├── tests/
└── screenshots/
```

---

## 5. Main Project: Python Firewall Log Analyzer

To automate the detection of suspicious network traffic, I developed `firewall_analyzer.py`. This utility reads raw firewall syslog streams, validates event records, groups activity by source and destination IPs, counts `DROP` versus `ALLOW` verdicts, identifies top communicating ports, and flags hosts exhibiting high-frequency dropped connection attempts or potential scanning behavior.

---

## 6. Testing & Validation

The firewall log analyzer underwent rigorous unit and integration testing covering:
* Successful ingestion of synthetic firewall event logs (`firewall-events.log`).
* Error handling for missing input files (returning operational exit code `2`).
* Resilience against malformed log lines and corrupt entries without script termination.
* Command-line argument flexibility for custom drop-threshold tuning.

---

## 7. Findings & Summary

Offline analysis of synthetic firewall telemetry successfully categorized traffic flows, identified routine inbound/outbound service allowances, and isolated blocked drop events. The findings emphasize that firewall drop logs serve as crucial investigative leads for detecting unauthorized egress, port scans, or misconfigured application traffic.

---

## 8. Limitations

* The dataset utilized for this analysis is synthetic and educational.
* Heuristic log parsing provides visibility into logged firewall verdicts but lacks live stateful socket inspection or endpoint process attribution.

---

## 9. Skills Demonstrated

* Network configuration and interface inventory management across operating systems.
* Low-level troubleshooting of DHCP, ARP, routing tables, and NAT translations.
* Security boundary analysis, firewall rule auditing, and ACL evaluation.
* Python-based log parsing, exception handling, and automated security reporting.

---

## 10. References & Resources

* IETF RFC 791 / RFC 1918 (Internet Protocol & Private Address Space)
* IETF RFC 2131 (Dynamic Host Configuration Protocol)
* NIST Special Publication 800-41 (Guidelines on Firewalls and Firewall Policy)
* Cisco Networking Academy Fundamentals

# Day 15 - Advanced Protocol Filtering & Statistical Triage

## Overview
In professional Security Operations Centers (SOCs), examining individual packets one by one is inefficient. Analysts must leverage advanced display filters to isolate specific protocol families (such as DNS, ICMP, ARP, and TCP analysis flags) and utilize high-level statistical menus to establish macro-level traffic profiles during incident triage.

This module documents our advanced protocol filtering execution and statistical analysis using Wireshark on Parrot OS.

---

## 1. Advanced Protocol-Specific Display Filters

When analyzing capture files like `http_redirects.pcapng`, applying targeted filters allows us to isolate specific behavioral events or hunt for indicators of compromise (IoCs).

| Display Filter String | Target Protocol / Metric | Lab Observation & Result | Forensic Meaning |
| :--- | :--- | :--- | :--- |
| `dns` | Domain Name System | `Displayed: 0 (0.0%)` | No DNS resolution traffic present in this capture. |
| `icmp` | Internet Control Message Protocol | `Displayed: 0 (0.0%)` | No ping/traceroute messages present. |
| `arp` | Address Resolution Protocol | `Displayed: 0 (0.0%)` | No Layer 2 ARP broadcast frames present. |
| `tcp` | Transmission Control Protocol | `Displayed: 271 (100.0%)` | All packet flows in the capture utilize TCP. |
| `tcp.analysis.retransmission` | TCP Retransmissions / Loss | `Displayed: 0 (0.0%)` | Clean session with zero packet loss or congestion flags. |

>  **Beginner Note:** Getting zero displayed packets for specialized filters (like DNS or retransmissions) is a **fully legitimate and expected result**. It confirms the baseline health and absence of specific anomalies in the capture.

---

## 2. Macro-Level Statistical Triage

To understand the macro structure of a capture before diving into deep packet forensics, Wireshark's **Statistics** menu provides critical bird's-eye views.

### 2.1 Protocol Hierarchy Statistics
Navigating to **Statistics $\rightarrow$ Protocol Hierarchy** provides a complete percentage breakdown of all protocol layers present in the file.
* **Lab Finding:** 100% of packets encapsulated Ethernet $\rightarrow$ IPv4 $\rightarrow$ TCP, with Hypertext Transfer Protocol (HTTP) comprising **17.7% of packets** and **40.5% of total bytes**.

### 2.2 Endpoints Analysis
Navigating to **Statistics $\rightarrow$ Endpoints** ($\rightarrow$ IPv4 tab) reveals the active communicating entities in the capture session.
* **Lab Finding:** Mapped communications strictly to local loopback (`127.0.0.1`), moving 542 total packets across transmitted and received streams (77 KB total volume).

---

## 3. Job Market Application
In enterprise threat hunting, automated sensors ingest raw PCAP dumps when alerts trigger. Level 2 and Level 3 SOC analysts immediately open the Protocol Hierarchy and Endpoints tables to scope the blast radius of an incident—quickly determining whether they are looking at standard web traffic, lateral movement scans, or anomalous protocol tunneling.

# Day 15 - Wireshark Display Filters & Capture Filter Reference

## Overview

When investigating network packet captures (PCAP) containing thousands or millions of packets, manual inspection is impossible. Analysts rely on filtering to separate noise from signal. This guide details the critical operational distinction between Capture Filters and Display Filters, and provides a reference library of essential display filter syntax for Security Operations Centre (SOC) analysts.

---

## 1. Capture Filters vs. Display Filters

Wireshark provides two distinct filtering systems. Mixing them up is a common beginner mistake that can disrupt an investigation.

| Feature | Capture Filters | Display Filters |
| :--- | :--- | :--- |
| **When They Execute** | **Before** packets are recorded and saved to disk. | **After** packets have been captured and loaded into Wireshark. |
| **Syntax Standard** | Berkeley Packet Filter (BPF) syntax (e.g., `tcp port 80`). | Wireshark Display Filter syntax (e.g., `tcp.port == 80`). |
| **Data Impact** | **Destructive / Permanent:** Unmatched packets are permanently discarded and never recorded. | **Non-Destructive:** All packets remain in memory; the filter simply hides non-matching packets from view. |
| **Primary Use Case** | Live sniffing on high-speed enterprise networks to prevent storage exhaustion. | Offline incident investigations, PCAP analysis, and evidence extraction. |

> 🛡️ **SOC Analyst Golden Rule:** During historical incident investigations, **always use display filters**. Using a capture filter on an existing PCAP or live triage can permanently destroy forensic evidence needed for an investigation.

---

## 2. Essential Protocol Display Filters

Typing these strings into the display filter bar instantly isolates specific protocol layers:

* **ARP (Address Resolution):** `arp`
* **ICMP (Ping / Diagnostics):** `icmp`
* **DNS (Domain Name System):** `dns`
* **TCP (Transport Layer):** `tcp`
* **UDP (Transport Layer):** `udp`
* **HTTP (Unencrypted Web):** `http`
* **TLS (Encrypted Web):** `tls`

---

## 3. Filtering by IP Address and Ports

### 3.1 IP Address Filters
To isolate traffic involving a specific target IP address:

* **Any Traffic (Source or Destination):**
  ```text
  ip.addr == 192.0.2.10
  ```
* **Originating Source Only:**
  ```text
  ip.src == 192.0.2.10
  ```
* **Target Destination Only:**
  ```text
  ip.dst == 192.0.2.10
  ```

### 3.2 Port Filters
Ports identify specific network services. 

* **Filter by TCP Port:**
  ```text
  tcp.port == 443
  ```
* **Filter by UDP Port:**
  ```text
  udp.port == 53
  ```

> ⚠️ **What You Must Remember:** Port numbers indicate standard services, but they are **context, not absolute proof**. Attackers frequently run malicious payloads on non-standard ports to evade basic firewall rules.

---

## 4. Advanced Behavioral & Investigative Filters

Elite SOC analysts combine operators (`&&`, `||`, `!`) to hunt for specific security anomalies:

### A. Examining TCP Connection Establishment (SYN Scans / Inits)
```text
tcp.flags.syn == 1 && tcp.flags.ack == 0
```
* **Purpose:** Isolates initial `SYN` packets sent by clients that are not acknowledging a prior packet. Useful for analyzing port scans or session handshakes.

### B. Identifying TCP Retransmissions
```text
tcp.analysis.retransmission
```
* **Purpose:** Locates packets where TCP had to resend data due to dropped packets, network congestion, or unstable links.

### C. Examining DNS Resolution Errors
```text
dns.flags.rcode != 0
```
* **Purpose:** Isolates DNS responses where the server returned an error code (such as `NXDOMAIN` or `SERVFAIL`). Critical for hunting Domain Generation Algorithms (DGAs) and malware C2 beaconing.

### D. Examining HTTP Redirects
```text
http.response.code == 302
```
* **Purpose:** Isolates HTTP responses with status code `302 Found`. Essential when tracing multi-step phishing redirect chains.

---

## 5. Job Market Application

During SOC technical interviews and practical assessments, interviewers frequently evaluate your ability to construct complex display filters under pressure. Knowing how to combine IP, port, and protocol filters (e.g., `ip.src == 10.0.0.5 && dns`) demonstrates professional efficiency and practical mastery of network forensics.

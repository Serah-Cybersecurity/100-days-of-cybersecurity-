# Detection Mapping & MITRE ATT&CK Telemetry Analysis

## 1. Overview
This document establishes an evidence-based framework for mapping network telemetry and security alerts to the MITRE ATT&CK framework. In defensive security operations, telemetry data sources provide visibility into network activity, but collecting data or generating a signature alert does not inherently indicate malicious adversary behavior.

---

## 2. Telemetry Data Component Mapping Matrix

| MITRE ATT&CK Data Component | Data Source Scope & Description | Primary Lab Tool Source | Key Investigative Questions Answered | Technical & Visibility Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Network Traffic Flow** | 5-tuple session summary, byte counts, duration, and flow hashes (Community ID). | Zeek (`conn.log`), Suricata EVE (`flow`). | Did host A talk to host B? What was the volume and duration of data transferred? Can flows be correlated across sensors? | No payload visibility; no application URI/domain context; subject to 5-tuple hash collisions over extended windows. |
| **Network Traffic Content** | Unencrypted application payloads, transaction headers, and signature pattern matches. | Suricata EVE (`alert`), Wireshark (`.pcap`). | Did the payload match a known signature? What specific command or payload string was transmitted? | Fully blinded by modern TLS/SSL encryption without inline proxy decryption; high storage/processing overhead. |
| **Domain Name Resolution** | Application-layer DNS queries (`A`, `AAAA`, `TXT`), response codes (`rcode`), and answer records. | Zeek (`dns.log`), Suricata EVE (`dns`). | What domain was requested? Did resolution succeed or fail (`NXDOMAIN`)? Is DNS being used for C2 or exfiltration? | DNS resolution does not guarantee an established TCP/UDP connection; obscured by DNS over HTTPS (DoH) / DNS over TLS (DoT). |
| **Network Connection Creation** | Endpoint process socket creation events linking process IDs (PID), executables, and local/remote sockets. | Endpoint Telemetry (Sysmon Event ID 3, Linux Auditd, EDR). | Which specific process/executable on the host initiated the connection? Was it spawned by a suspicious parent process? | Cannot be observed by network wire sensors alone; requires installed host agents and generates massive log volumes. |

---

## 3. Evidence-Based Mapping Guidelines
* **Avoid Artificial Mapping:** Benign network traffic (such as routine DNS lookups for `example.com`) must not be mapped to ATT&CK technique IDs (e.g., T1071.004) solely to make documentation appear more complex.
* **Focus on Data Components:** Data components define defensive visibility boundaries. Wire telemetry (Suricata/Zeek) must be combined with host-level socket creation events to build complete investigative chains.

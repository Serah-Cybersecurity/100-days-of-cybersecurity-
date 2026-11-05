# Network Security Monitoring Investigation

## 1. Investigation Details
- **Investigation ID:** INV-2026-DAY19-001
- **Date:** November 5, 2026
- **Analyst:** Serah Mulwa (Junior SOC Analyst)
- **Operating System:** Parrot OS / Debian-based Linux Kernel
- **Zeek Version:** Zeek LTS 9.0.1 (Docker Containerized & Native)
- **Data Source:** Local Network Packet Capture (`day19.pcap`)
- **Capture Method:** `tcpdump` on virtual interface `enp0s3`

---

## 2. Objective
To execute a complete offline Network Security Monitoring (NSM) workflow using Zeek LTS 9.0.1, transforming raw packet captures (`.pcap`) into structured JSON telemetry logs (`conn.log`, `dns.log`, `ssl.log`), performing cross-log event correlation via Unique Identifiers (UIDs), writing a custom event-driven detection script (`watch_dns.zeek`), and building an automated Python multi-protocol log parser (`zeek_log_summary.py`).

---

## 3. Scope
- **Systems Included:** Local host client interface (`10.0.2.15`) and upstream local resolver (`192.168.100.1`).
- **Traffic Captured:** Local DNS queries (`dig`), HTTPS web traffic (`curl`), and background connection handshakes.
- **Protocols Examined:** TCP, UDP, DNS (Port 53), TLSv1.3 (Port 443).
- **Time Period:** 15-minute educational lab session window.
- **Exclusions:** Production enterprise subnets, unauthorized external host enumeration, and unencrypted HTTP payload inspections.

---

## 4. Environment
- **Operating System:** Parrot OS (Linux)
- **Zeek Version:** 9.0.1 LTS
- **Wireshark Version:** 4.x CLI / GUI Inspector
- **Python Version:** Python 3.11+
- **Network Interface:** `enp0s3`
- **Capture Filter:** Standard packet capture without restrictive BPF filters (`-w pcap/day19.pcap`)

---

## 5. Evidence Collection
- **PCAP Generation:** Captured using live `tcpdump` interface monitoring and manually validated via Wireshark and `tcpdump -nn -r`.
- **Packet Count:** ~14 packets recorded.
- **Capture File Size:** 11.39 KB (`day19.pcap`).
- **Protocols Observed:** UDP, TCP, DNS, TLS.
- **Collection Limitations:** Single-host synthetic lab traffic; lack of complex enterprise lateral movement vectors.

---

## 6. Connection Analysis (`conn.log`)
- **Number of Connection Records:** 6 total connection flows.
- **Transport Protocols:** UDP (3 flows) and TCP (3 flows).
- **Destination Ports:** Port 53 (DNS) and Port 443 (HTTPS TLS).
- **Recognised Services:** `dns`, `ssl`.
- **Connection States:** `SF` (Normal Successful Finish: 4 flows) and `REJ` (Connection Attempt Rejected: 2 flows).

---

## 7. DNS Analysis (`dns.log`)
- **Query Names:** `example.com` (4 queries total).
- **Record Types:** Type `A` (IPv4) and Type `AAAA` (IPv6).
- **Response Codes:** `NOERROR` (Successful resolution).
- **Resolver Information:** Originator `10.0.2.15` querying resolver `192.168.100.1`.

---

## 8. TLS Analysis (`ssl.log`)
- **TLS Records Observed:** 1 successful encrypted session record.
- **Versions Recorded:** `TLSv13`.
- **Cipher Information:** `TLS_AES_256_GCM_SHA384`.
- **Server Names Visible (SNI):** `example.com`.
- **Limitations Caused by Encryption:** Payload inspection is prevented by TLS encryption; analysis is strictly limited to handshake metadata (SNI, cipher suite, certificate parameters).

---

## 9. Event Correlation (UID Pivoting)
- **Methodology:** Isolated specific DNS query events for `"example.com"` in `dns.log` using `jq`, extracted the unique session identifier (`uid: C1ylQ419432UMYnqn2`), and successfully pivoted to `conn.log` using `grep -F` to match transport-layer session metadata.
- **Result:** Proved direct causal link between application-layer DNS intent and transport-layer UDP session completion.

---

## 10. Custom Zeek Script (`watch_dns.zeek`)
- **Script Purpose:** Demonstrates event-driven programming by hooking into Zeek's internal Event Engine to monitor real-time `dns_request` events.
- **Code Logic:** Filters for queries matching `"example.com"` and prints formatted terminal debug statements (`LAB DNS QUERY: originator=... resolver=... qtype=...`).
- **Execution Result:** Successfully triggered in real time against `day19.pcap`, verifying live event hooks.

---

## 11. Python Automated Analysis (`zeek_log_summary.py`)
- **Input Files:** `conn.log`, `dns.log`, `ssl.log` (Newline-delimited JSON format).
- **Data Parsing:** Robust file reading handling UTF-8 decoding and `json.JSONDecodeError` exception resilience.
- **Aggregation:** Leveraged Python's `collections.Counter` to compute frequency distributions for transport protocols, destination ports, connection states, and TLS versions.
- **UID Correlation:** Mapped DNS query UIDs directly in memory.
- **Output:** Generated a structured, executive multi-protocol terminal report summary.

---

## 12. Findings

### Confirmed Observations
- The host `10.0.2.15` generated standard DNS queries for `example.com` over UDP port 53.
- The host successfully initiated TLSv1.3 encrypted sessions to external IPs over TCP port 443 with SNI `example.com`.
- Zeek successfully processed the offline PCAP, generated JSON logs, and enabled cross-log UID pivoting.

### Interpretations
- The observed activity represents normal, benign web-browsing and domain name resolution behavior consistent with testing or educational navigation.

### Unknowns
- The exact user intent behind the manual `dig` and `curl` commands cannot be determined beyond technical execution logs.

---

## 13. Limitations
- **Capture Visibility:** Limited to a single virtual network interface (`enp0s3`).
- **Missing Records:** Absence of unencrypted HTTP traffic (`http.log`), as all target web traffic utilized modern TLS encryption.
- **Single-Device Lab Scope:** Traffic lacks multi-host enterprise complexity, lateral movement, or domain controller authentication exchanges.

---

## 14. Conclusion
The network telemetry extracted from `day19.pcap` via Zeek 9.0.1 confirms standard DNS and TLS session handshakes associated with `example.com`. All traffic evaluated conformed to expected benign parameters with no indicators of compromise (IoCs) or anomalous threat behaviors detected.

---

## 15. Recommendations
1. **Deploy Network Sensors at Strategic Bottlenecks:** Enterprise deployments should place Zeek sensors at core gateway chokepoints and internal VLAN boundaries to capture east-west lateral movement.
2. **Integrate SIEM Forwarding:** Configure Zeek to stream JSON telemetry logs directly into an enterprise SIEM (such as Splunk or Elastic Stack) for real-time threat intelligence correlation.
3. **Enhance TLS Visibility:** Implement enterprise SSL/TLS decryption inspection proxy policies where legally permissible to inspect encrypted payload contents for sophisticated malware.

# Network Traffic Analysis Report

## 1. Investigation Metadata

* **Case ID:** DAY15-NTA-001
* **Investigation Type:** Offline PCAP Analysis
* **Analyst:** Serah Mulwa
* **Date:** November 3, 2026

---

## 2. Objective

The objective of this investigation was to conduct a comprehensive offline network traffic triage of an authorized sample packet capture (`http_redirects.pcapng`). 

The primary goals were to:
1. Establish cryptographic evidence baselines to guarantee chain of custody.
2. Profile the macro-level protocol composition and identify active host endpoints.
3. Group TCP socket conversations to analyze session metrics and data transfer volumes.
4. Triage application-layer HTTP requests, response headers, and redirection behavior.
5. Evaluate transport-layer TCP health and verify whether packet loss or retransmission flags were present.
6. Produce an objective, evidence-based SOC assessment that separates verified technical observations from analytical interpretations.

---

## 3. Scope

* **Target Artifact:** `day-15/lab/data/http_redirects.pcapng`
* **Capture Source:** Local loopback network interface (`127.0.0.1` / `lo`).
* **Authorization & Environment:** The investigation was conducted within an isolated lab environment on Parrot OS using authorized practice capture files provided for network security training. No live network sniffing or unauthorized packet extraction was performed.

---

## 4. Evidence Information

* **Filename:** `http_redirects.pcapng`
* **Capture Format:** Wireshark/Dumpcap pcapng (`-` format)
* **SHA-256 Hash:** `ff432a6b71d06cd20720f7763e584014edd0a43c3b55981c682d1b7640207abc`
* **Packet Count:** 271 packets
* **File Size:** 47 KB (38 KB payload data size)

---

## 5. Tools

* **Wireshark (v4.4.15):** Graphical packet analysis, protocol hierarchy statistics, endpoints table, conversation streaming, and targeted display filtering.
* **TShark (v4.4.15):** Command-line packet metadata extraction and automated filtering.
* **Python 3 (v3.11+):** Execution of custom automated metadata triage utility (`pcap_summary.py`) utilizing `subprocess`, `csv.DictReader`, and `collections.Counter`.
* **Capinfos & OpenSSL (`sha256sum`):** Low-level PCAP header extraction and cryptographic file integrity verification.

---

## 6. Methodology

The investigation followed a 6-stage structured forensic framework:

1. **Chain of Custody & Verification:** Calculated the SHA-256 cryptographic hash of `http_redirects.pcapng` and queried header properties using `capinfos` prior to analysis.
2. **Automated Metadata Extraction:** Programmatically parsed packet fields (`frame.number`, `frame.len`, `_ws.col.Protocol`, `ip.src`, `ip.dst`, `tcp.srcport`, `tcp.dstport`) using the custom Python tool `pcap_summary.py`.
3. **Macro-Level Protocol Profiling:** Utilized Wireshark's **Protocol Hierarchy** statistics to calculate percentage breakdowns across OSI layers.
4. **Endpoint & Conversation Mapping:** Grouped IP addresses and 5-tuple socket pairs (**Statistics $\rightarrow$ Endpoints / Conversations**) to evaluate connection count, byte volume, and session durations.
5. **Targeted Protocol Filtering:** Applied Wireshark display filters (`tcp`, `http`, `dns`, `icmp`, `arp`, `tcp.analysis.retransmission`, `http.response.code == 302`) to audit application and transport behavior.
6. **Documentation & Reporting:** Synthesized findings, identified analytical boundaries, and documented recommendations.

---

## 7. Protocol Analysis

Analysis of the protocol hierarchy revealed a single, highly uniform encapsulation stack across the entire capture:

```
Frame (100%) ── Ethernet (100%) ── IPv4 (100%) ── TCP (100%) ── HTTP (17.7%)
```

### Observed Protocol Breakdown:
* **Transmission Control Protocol (TCP):** Accounted for **100% of all packets** (271 frames) and 100% of bytes (38,512 bytes).
* **Hypertext Transfer Protocol (HTTP):** Represented **17.7% of total packet count** (48 packets) and **40.5% of total byte volume** (15,591 bytes).
* **Domain Name System (DNS):** 0 packets (0.0%). No domain name queries or DNS responses were present.
* **Address Resolution Protocol (ARP) / ICMP:** 0 packets (0.0%). No Layer 2 broadcast discovery or ICMP echo messages were present.

### Significance:
The complete absence of DNS, ARP, and ICMP traffic confirms that the capture was collected on a local loopback interface (`lo`) recording isolated, pre-resolved local web traffic.

---

## 8. Endpoint Analysis

Evaluation of the **IPv4 Endpoints** table identified only a single host address involved in all network frames:

* **Endpoint Address:** `127.0.0.1` (IPv4 Local Loopback)
* **Transmitted Activity:** 271 packets (38,512 bytes)
* **Received Activity:** 271 packets (38,512 bytes)
* **Total Directional Endpoint Count:** 542 packet instances

### Analytical Assessment:
Because `127.0.0.1` represents internal loopback traffic, both the client software initiating the connections and the server software accepting the requests resided on the exact same local system.

---

## 9. Conversation Analysis

Examination of **TCP Conversations** identified 48 distinct communication streams between local ephemeral client ports and target destination port `80`.

### Key Communication Pair Characteristics:
* **Source Endpoints:** `127.0.0.1` across high-numbered ephemeral ports (e.g., `47660`, `47662`, `47664`, `47862`, `47864`).
* **Destination Endpoint:** `127.0.0.1:80` (Standard HTTP Port).
* **Stream Volumes:** Each TCP stream consistently exchanged 5 to 6 packets, transferring between 741 bytes and 847 bytes per conversation.
* **Flow Duration:** Transactions occurred rapidly within microsecond-to-millisecond intervals.

### Interpretation:
The uniform stream lengths and brief connection lifetimes indicate programmatic, transactional HTTP exchanges (such as a local automated script, unit test, or web crawler hitting a local web server) rather than interactive human web browsing.

---

## 10. HTTP Analysis

Targeted application-layer filtering was performed to audit web requests and responses.

* **Observed Requests:** Multiple HTTP `GET` requests sent from local ephemeral client sockets to `127.0.0.1:80`.
* **Observed Responses:** HTTP server response frames carrying application payloads (accounting for 40.5% of total capture byte volume).
* **Redirection Audit (`http.response.code == 302`):** Applied filter `http.response.code == 302` to isolate temporary redirection responses.
  * *Result:* `Displayed: 0 (0.0%)`. No HTTP 302 Found status codes were observed in this dataset.

### Technical Context on HTTP 302:
An **HTTP 302 Found** code is a standard response indicating that a requested resource has been temporarily relocated to a different URI specified in the `Location:` header. While HTTP redirects can be leveraged in phishing or adversary infrastructure for traffic distribution, they are fundamentally legitimate web navigation controls used for authentication routing, HTTPS enforcement, and load balancing.

---

## 11. TCP Analysis

Transport-layer stability was audited to evaluate TCP flag states and packet delivery reliability.

* **Connection Establishment:** Standard TCP 3-Way Handshakes (`SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`) were successfully completed across all 48 conversation streams.
* **Connection Termination:** Streams concluded with standard grace flags (`FIN-ACK` / `ACK`) or reached complete payload transfer.
* **Retransmission Audit (`tcp.analysis.retransmission`):**
  * *Result:* `Displayed: 0 (0.0%)`. Zero packet retransmissions were flagged by Wireshark.

### Technical Context on TCP Retransmissions:
TCP retransmissions occur when a sender does not receive an acknowledgment within the expected timeout window. Common causes include physical link degradation, router buffer congestion, delayed ACKs, or capture ring-buffer dropouts. Finding 0 retransmissions confirms the loopback capture buffer was healthy and experienced zero packet loss.

---

## 12. Findings

To adhere to forensic standards, factual observations are strictly separated from analytical interpretations:

### Factual Technical Observations:
1. The capture file `http_redirects.pcapng` contains 271 frames totaling 38,512 bytes.
2. 100% of packets utilize IPv4 and TCP protocols over host address `127.0.0.1`.
3. 48 distinct TCP conversations were opened to destination port `80`.
4. HTTP traffic represents 48 packets (17.7% of packets, 40.5% of bytes).
5. Zero TCP retransmissions (`tcp.analysis.retransmission`) and zero HTTP 302 redirects (`http.response.code == 302`) were recorded.

### Analytical Interpretations:
1. The activity represents automated, local client-server interactions occurring on a single machine's loopback interface.
2. The communication pattern matches programmatic web request testing or local script execution.
3. Network transport health was optimal during the capture window, exhibiting zero packet loss.

---

## 13. Limitations

A security analyst must document operational boundaries to prevent over-reporting:

1. **Interface Boundary:** The capture is strictly limited to local loopback (`127.0.0.1`); it does not reflect external network interface activity (Ethernet/Wi-Fi).
2. **Missing Host Context:** Network metadata alone cannot identify the specific process name, Process ID (PID), or operating system user account that executed the HTTP client request. Endpoint logs (Sysmon / Windows Event Logs) are required for process attribution.
3. **Capture Completeness:** The sample is a pre-recorded snippet; it does not capture activity prior to or following the recording window.

---

## 14. Conclusion

The packet capture `http_redirects.pcapng` contains 271 packets establishing uniform, unencrypted HTTP GET communications over TCP between local loopback sockets (`127.0.0.1`) and local port `80`. 

The observed records establish that transactional HTTP traffic occurred with zero transport-layer retransmissions or packet loss. No HTTP 302 redirection responses or anomalous protocol behaviors were present within the examined dataset. 

The evidence confirms standard, localized client-server network interactions; however, network metadata alone does not establish the specific binary process or user intent behind the traffic. Additional endpoint telemetry (such as Sysmon Event ID 1 process creation logs) and organizational application context would be required to perform full host attribution.

---

## 15. References

1. Postel, J. (1981). *Transmission Control Protocol*. RFC 793. Internet Engineering Task Force (IETF).
2. Fielding, R., et al. (1999). *Hypertext Transfer Protocol -- HTTP/1.1*. RFC 2616. IETF.
3. Wireshark Documentation Team. (2026). *Wireshark User's Guide: Display Filter Reference*. Wireshark Foundation.
4. Python Software Foundation. (2026). *subprocess — Subprocess management*. Python 3.11 Documentation.

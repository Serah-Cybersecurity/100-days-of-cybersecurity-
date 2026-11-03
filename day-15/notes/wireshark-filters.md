# Day 15 - Wireshark Display Filter Forensic Reference Manual

## Overview

Display filters in Wireshark do **not** alter or drop captured packets; they selectively isolate specific protocol fields, frame characteristics, or logical conditions from view. 

This reference manual documents every display filter utilized during our Day 15 network traffic analysis labs, defining exact syntax, display outputs, analyst rationale, and forensic limitations.

---

## 1. Protocol Family Baseline Filters

### 1.1 `tcp`
* **Syntax:** `tcp`
* **What it Displays:** Filters the capture view to display only Transmission Control Protocol frames.
* **Analyst Rationale:** Isolates stateful transport-layer sessions to evaluate web traffic, SSH, file transfers, and general socket connections.
* **What it Cannot Prove:** Does not prove whether the payload within the TCP streams is benign or malicious.

### 1.2 `http`
* **Syntax:** `http`
* **What it Displays:** Filters for cleartext Hypertext Transfer Protocol request and response packets.
* **Analyst Rationale:** Allows immediate inspection of web URIs, User-Agent strings, HTTP response headers, and GET/POST data.
* **What it Cannot Prove:** Cannot display encrypted HTTPS traffic running over TLS port 443.

### 1.3 `dns`
* **Syntax:** `dns`
* **What it Displays:** Isolates Domain Name System queries and response packets.
* **Analyst Rationale:** Enables rapid identification of domain lookups, fast-flux activity, DGA patterns, and suspicious `TXT` record queries.
* **What it Cannot Prove:** Does not prove that a host successfully established a socket connection to the resolved IP address.

### 1.4 `icmp`
* **Syntax:** `icmp`
* **What it Displays:** Filters for Internet Control Message Protocol traffic (echo requests/replies, destination unreachable, time exceeded).
* **Analyst Rationale:** Helps identify network discovery ping sweeps, path MTU discovery, and ICMP tunneling.
* **What it Cannot Prove:** Finding zero ICMP traffic does not mean a target host is offline (firewalls frequently drop ping).

### 1.5 `arp`
* **Syntax:** `arp`
* **What it Displays:** Isolates Layer 2 Address Resolution Protocol broadcast requests and unicast replies.
* **Analyst Rationale:** Crucial for detecting local LAN ARP spoofing, man-in-the-middle (MITM) poisoning attacks, and MAC address conflicts.
* **What it Cannot Prove:** Does not traverse Layer 3 boundary routers; scoped strictly to the local broadcast domain.

---

## 2. Advanced Performance & Behavioral Filters

### 2.1 `tcp.analysis.retransmission`
* **Syntax:** `tcp.analysis.retransmission`
* **What it Displays:** Flags TCP frames that Wireshark identifies as suspected retransmissions of previously observed sequence numbers.
* **Analyst Rationale:** Evaluates network health, packet loss rates, physical link degradation, and congestion points.
* **What it Cannot Prove:** **Cannot prove malicious intent.** Retransmissions occur naturally due to network congestion or dropped frames.

### 2.2 `http.response.code == 302`
* **Syntax:** `http.response.code == 302`
* **What it Displays:** Filters specifically for HTTP responses containing the status code `302 Found` (temporary redirect).
* **Analyst Rationale:** Tracks application-layer redirection behavior, observing how web servers route clients to secondary location URLs.
* **What it Cannot Prove:** Does not establish that a redirect is malicious; 302 redirects are standard operational tools for load balancing and authentication.

### 2.3 `ip.addr == 127.0.0.1`
* **Syntax:** `ip.addr == 127.0.0.1`
* **What it Displays:** Filters for all packets where either the source IP OR destination IP matches `127.0.0.1`.
* **Analyst Rationale:** Isolates communications associated with a specific endpoint host address.
* **What it Cannot Prove:** Does not reveal host process executable names or operating system user contexts.

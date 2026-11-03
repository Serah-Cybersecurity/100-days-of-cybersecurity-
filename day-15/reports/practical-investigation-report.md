# Day 15 - Practical Network Traffic Triage & Forensic Analysis

## Executive Summary

As part of my network security hands-on training, I conducted a practical investigation of a provided sample packet capture (`http_redirects.pcapng`). Rather than starting with the assumption that an attack or breach had occurred, I followed a structured, 7-step forensic methodology. 

The primary goal of this investigation was to establish an objective baseline of the traffic: mapping protocol distributions, identifying communicating endpoints, evaluating TCP session health, and examining application-layer HTTP behavior.

---

## Step 1: Capture Identity & Forensic Chain of Custody

Before opening the file in Wireshark, I established the cryptographic baseline and physical capture properties to ensure chain of custody. Modifying or losing track of evidence properties invalidates investigation integrity.

* **Filename:** `http_redirects.pcapng`
* **File Format:** Wireshark pcapng format
* **Capture Interface/Source:** Local Loopback (`127.0.0.1` / `lo`)
* **SHA-256 Hash:** `ff432a6b71d06cd20720f7763e584014edd0a43c3b55981c682d1b7640207abc`
* **Total Packet Count:** 271 packets
* **Total File Size:** 47 KB (38 KB payload data size)
* **Analysis Environment:** Parrot OS (Wireshark & TShark v4.4.15)

---

## Step 2: Protocol Distribution Breakdown

Using **Statistics $\rightarrow$ Protocol Hierarchy**, I generated a bird's-eye statistical breakdown of the traffic composition.

* **Dominant Protocol:** Transmission Control Protocol (TCP) over IPv4 accounted for **100% of all observed packets** (271 frames).
* **Application Layer:** Hypertext Transfer Protocol (HTTP) represented **17.7% of total packet count** (48 packets) and **40.5% of total byte volume** (15,591 bytes).
* **Absent Protocols:** No DNS queries (`dns`), ARP frames (`arp`), ICMP echo packets (`icmp`), or TLS encrypted handshakes (`tls.handshake`) were present. 
* **Analyst Note:** Finding zero DNS or ARP packets is completely normal given that this capture recorded isolated local web transactions on the loopback interface (`127.0.0.1`).

---

## Step 3: Endpoint Identification

Using **Statistics $\rightarrow$ Endpoints** (IPv4 tab), I cataloged all active host addresses involved in the traffic stream.

* **Active Endpoint:** `127.0.0.1` (IPv4 Local Loopback)
* **Directional Activity:** Transmitted 271 packets (39 KB) and Received 271 packets (39 KB), totaling 542 endpoint packet records.
* **Analyst Reflection:** An IP address alone does not define host behavior or identity. Because `127.0.0.1` represents internal loopback traffic, both the client and server software reside on the exact same host system.

---

## Step 4: TCP Conversation Triage

Navigating to **Statistics $\rightarrow$ Conversations** ($\rightarrow$ TCP tab) allowed me to group individual packets into continuous session streams.

* **Primary Communication Flow:** Local ephemeral source ports (e.g., `47660`, `47662`, `47664`) initiating short-lived connection requests to target destination port `80` (HTTP).
* **Stream Dynamics:** The capture contains 48 distinct TCP conversations. Each stream typically spans 5 to 6 packets with total data transfers ranging between 741 bytes and 847 bytes.
* **Interpretation:** The short session duration and repetitive packet counts strongly suggest automated transactional HTTP GET requests (such as a local web crawler or script hitting a local service) rather than long-term interactive user browsing.

---

## Step 5: HTTP Redirect Analysis (`http.response.code == 302`)

To test for application-layer redirection behavior, I applied the display filter `http.response.code == 302`.

* **Filter Result:** Isolated 0 HTTP 302 redirection packets in this specific dataset.
* **Technical Context:** An **HTTP 302 Found** status code is a standard response indicating that the requested web resource has been temporarily relocated to a different URI specified in the `Location` header.
* **Key takeaway:** Web redirection is a standard functionality used daily for load balancing, authentication routing, and HTTPS enforcement. I must never label HTTP redirects as inherently malicious without verifying destination domains and payloads.

---

## Step 6: TCP Reliability & Retransmission Check

I evaluated transport-layer stability by applying `tcp`, followed by the specialized analysis filter `tcp.analysis.retransmission`.

* **Filter Result:** `Displayed: 0 (0.0%)`
* **Assessment:** Zero TCP retransmission flags were identified by Wireshark.
* **Forensic Perspective:** Retransmissions happen legitimately due to physical packet loss, Wireshark capture buffer dropouts, or network congestion. Finding zero retransmissions confirms the loopback capture environment was stable and free of connection degradation.

---

## Step 7: Investigation Limitations & Scope Boundaries

A responsible cybersecurity analyst must clearly document the boundaries of their evidence. Based on this investigation:

1. **Incomplete Scope:** The capture records isolated loopback traffic (`127.0.0.1`); it does not represent host-wide network egress or ingress.
2. **Missing Endpoint Logs:** Without local process logs (e.g., Sysmon or EDR execution events), we cannot definitively name the exact executable binary that generated the HTTP GET requests.
3. **Payload Inspection Limits:** Metadata analysis proves connection frequency and byte sizes, but full context requires inspecting the specific URI parameter values transferred within the HTTP body.

---

## Conclusion & Portfolio Takeaways

This practical investigation demonstrated how to systematically analyze raw network captures without falling into confirmation bias. By validating file hashes, extracting statistical distributions, and isolating specific protocol layers, I built an objective assessment of network activity—a core competency required for SOC analyst roles.

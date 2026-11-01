# Day 4 Comprehensive Study Notes

## 1. Networking Architecture & Models
- **OSI Model:** 7-layer theoretical framework (Physical, Data Link, Network, Transport, Session, Presentation, Application).
- **TCP/IP Model:** 4-layer practical framework (Network Access, Internet, Transport, Application).
- **Encapsulation & Decapsulation:** How data travels down layers (adding headers/trailers: Payload -> Segments/Datagrams -> Packets -> Frames -> Bits) and back up.

## 2. Hardware & Addressing
- **Routers vs. Switches:** Routers operate at Layer 3 (routing traffic between different networks/subnets using IP addresses), while switches operate at Layer 2 (forwarding frames within a local network using MAC addresses).
- **IPv4 & MAC Addressing:** Logical vs. physical addressing schemes.

## 3. Core Protocols & Transport Layer
- **TCP (Transmission Control Protocol):** Connection-oriented, reliable, uses 3-way handshake (SYN, SYN-ACK, ACK), guarantees delivery.
- **UDP (User Datagram Protocol):** Connectionless, fast, unverified delivery (used for streaming/DNS).
- **DNS (Domain Name System):** Translates human-readable domain names to numeric IP addresses (Port 53).
- **HTTP/HTTPS:** Web traffic protocols (Ports 80 & 443), with TLS securing transport confidentiality.

## 4. Cybersecurity Architecture Concepts
- **Attack Surface:** Total sum of exposed entry points (internet services, APIs, web apps, endpoints). Networking dictates a massive share of this surface.
- **Network Segmentation:** Dividing networks into isolated security tiers (Web -> App -> DB) to limit attacker lateral movement.
- **Defense in Depth:** Multiple layers of overlapping security controls so no single point of failure compromises the system.
- **Firewalls:** Inspection control points for ingress and egress traffic, implementing stateful filtering and ACLs.
- **CIA Triad in Networking:** Ensuring Confidentiality (TLS/HTTPS), Integrity (checksums/cryptography), and Availability (resilience against DDoS).

## 5. SOC Investigation Framework (The 7 Questions)
When analyzing any network event, ask:
1. **WHO?** (Source/destination accounts or endpoints)
2. **WHAT?** (Service or protocol)
3. **WHERE?** (IP addresses and network zones)
4. **WHEN?** (Timestamp and timing analysis)
5. **HOW?** (Connection mechanism and handshake flags)
6. **WHY?** (Business or technical intent)
7. **SHOULD?** (Policy authorization check)

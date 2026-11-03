# Day 15 - Auxiliary & Infrastructure Network Protocols

## Overview

A raw network packet capture (PCAP) contains far more than primary application data like HTTP or DNS. Modern networks rely on a continuous background chatter of operational, routing, time-synchronization, and address-resolution protocols. 

For a Security Operations Centre (SOC) analyst, distinguishing standard infrastructure protocol chatter from anomalous or malicious behavior is essential to effective traffic analysis and threat detection.

---

## 1. Protocol Summary & Operational Roles

| Protocol | Full Name | Standard Port / Layer | Primary Operational Function | Security Relevance & Attack Vectors |
| :--- | :--- | :--- | :--- | :--- |
| **ARP** | Address Resolution Protocol | Data Link (Layer 2) | Resolves IPv4 addresses to local physical MAC addresses. | **ARP Spoofing / Poisoning:** Man-in-the-Middle (MitM) interception on local subnets. |
| **ICMP** | Internet Control Message Protocol | Network (Layer 3) | Delivers operational diagnostic and network error messages. | **Reconnaissance & Tunneling:** Ping sweeps, ICMP exfiltration, covert C2 channels. |
| **DHCP** | Dynamic Host Configuration Protocol | UDP Ports 67/68 (L7) | Automates IP address, gateway, and DNS configuration leasing. | **Rogue DHCP Servers:** Unauthorized gateway assignment and DNS redirection. |
| **TLS** | Transport Layer Security | Transport / App (L6/7) | Provides end-to-end cryptographic privacy and integrity. | **SNI & Certificate Inspection:** Malware C2 metadata, expired or self-signed certs. |
| **SSH** | Secure Shell | TCP Port 22 (L7) | Provides encrypted remote command-line administration. | **Brute Force & Tunneling:** Password guessing attacks, SSH port forwarding/pivoting. |
| **SMB** | Server Message Block | TCP Port 445 (L7) | Enables file sharing, printer access, and RPC in Windows. | **Lateral Movement & Malware:** Primary vector for ransomware propagation (WannaCry, PsExec). |
| **NTP** | Network Time Protocol | UDP Port 123 (L7) | Synchronizes system clocks against authoritative time sources. | **Log Alignment & Amplification:** Forensic timeline integrity, NTP DDoS amplification attacks. |

---

## 2. Deep Dive: Operational Mechanics & Security Application

### 2.1 ARP (Address Resolution Protocol)
* **Mechanics:** When Host A (`192.168.1.10`) needs to transmit an IP packet to Host B (`192.168.1.50`) on the same physical network segment, it must encapsulate the packet inside an Ethernet frame with Host B's MAC address. If the MAC address is unknown, Host A broadcasts an ARP Request: *"Who has 192.168.1.50? Tell 192.168.1.10."* Host B responds with an ARP Reply containing its MAC address.
* **Wireshark Filter:** `arp`
* **Analyst Application:** Because ARP lacks built-in authentication, an attacker on the local network can transmit unsolicited (gratuitous) ARP replies claiming that the default gateway's IP address belongs to the attacker's MAC address. This enables a Man-in-the-Middle (MitM) attack.

### 2.2 ICMP (Internet Control Message Protocol)
* **Mechanics:** ICMP carries control messages rather than user data. Common message types include:
  * `Type 8` / `Type 0`: Echo Request / Echo Reply (`ping`).
  * `Type 3`: Destination Unreachable (indicates closed ports or firewall drops).
  * `Type 11`: Time Exceeded (TTL expired in transit; used by `traceroute`).
* **Wireshark Filter:** `icmp`
* **Analyst Application:** Threat actors perform ICMP ping sweeps to discover active hosts prior to port scanning. Additionally, because the ICMP Echo payload can contain arbitrary data bytes, advanced malware strains use **ICMP Tunneling** to bypass perimeter firewalls and exfiltrate sensitive files disguised as simple pings.

### 2.3 DHCP (Dynamic Host Configuration Protocol)
* **Mechanics:** Assigns dynamic network configurations to endpoints using the 4-step **DORA** handshake:
  1. **D**iscover: Client broadcasts looking for available DHCP servers.
  2. **O**ffer: Server offers an available IP configuration.
  3. **R**equest: Client requests the offered IP lease.
  4. **A**ck: Server acknowledges the lease assignment.
* **Wireshark Filter:** `dhcp` or `bootp`
* **Analyst Application:** Rogue DHCP servers placed on a network by attackers can respond faster than legitimate infrastructure, assigning victims a malicious Default Gateway or DNS server to intercept or hijack all outbound web traffic.

### 2.4 SMB (Server Message Block) — *Windows Critical Protocol*
* **Mechanics:** SMB supports file access, remote directory browsing, IPC (Inter-Process Communication), and RPC execution across Windows endpoints on **TCP Port 445**.
* **Wireshark Filter:** `smb2` or `smb`
* **Analyst Application:** SMB is the most heavily targeted protocol during lateral movement inside Active Directory environments. Tools like `PsExec` or ransomware strains (e.g., WannaCry, NotPetya) abuse SMB shares and administrative named pipes (`\PIPE\atsvc`) to remotely execute payloads across workstations.

### 2.5 NTP (Network Time Protocol)
* **Mechanics:** Client systems issue NTP requests over **UDP Port 123** to authoritative time servers to maintain clock accuracy within milliseconds.
* **Wireshark Filter:** `ntp`
* **Analyst Application:** Accurate time synchronization is critical for SIEM log correlation and incident response timelines. If an endpoint's clock drifts or is altered by malware (timestomping), event log correlation across host and network telemetry breaks.

---

## 3. Key Portfolio & Job Market Takeaways

1. **Baseline Awareness:** Normal networks generate continuous background noise from ARP, DHCP, ICMP, and NTP. An analyst must establish baseline parameters to avoid false positives.
2. **Contextual Investigation:** A single SMB connection between two admin hosts may be routine maintenance, whereas a single workstation attempting SMB connections to 50 adjacent endpoints in 10 seconds indicates active network scanning or lateral movement.
3. **Forensic Evidence:** Network protocols provide immutable header data that corroborate or challenge host-based event log entries.

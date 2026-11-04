# Technical Note: Suricata Rules, Pipeline Mechanics & Detection Engineering

**Author:** Serah Mulwa  
**Module:** Day 18 - Network Security Monitoring & Intrusion Detection  

---

## 1. Executive Summary

In a modern Security Operations Center (SOC), understanding how intrusion detection engines evaluate network traffic is just as important as knowing how to respond to alerts. Suricata is a high-performance, open-source threat detection engine that inspects network packets in real time, tracks stateful flows, decodes application protocols, and generates structured telemetry.

This technical note serves as an exhaustive reference for Suricata rule syntax, detection methodologies, the six-stage packet processing pipeline, thresholding, and false-positive management.

---

## 2. The Suricata 6-Stage Packet Processing Pipeline

When Suricata ingests live network frames or offline packet captures (PCAPs), it processes data through a strict, multi-threaded pipeline. Understanding this sequence is vital for debugging why a rule did or didn't trigger.

```text
[1. Packet Capture] ──> [2. Packet Decoding] ──> [3. Flow Tracking] ──> [4. Protocol Identification] ──> [5. Rule Evaluation] ──> [6. Event Generation (EVE JSON)]
```

1. **Packet Capture (Acquire):** Ingests raw packets from a physical interface (`eth0`), a mirrored SPAN port, or an offline PCAP file (`suricata -r capture.pcap`).
2. **Packet Decoding:** Strips away lower-layer wrappers, parsing Ethernet, IP (v4/v6), and transport headers (TCP/UDP/ICMP).
3. **Flow Tracking:** Groups individual packets into bi-directional **flows** to track session state (e.g., confirming whether a TCP handshake completed rather than looking at isolated packets).
4. **Protocol Identification (App-Layer):** Performs deep packet inspection (DPI) to identify the true application protocol. As analysts know, port numbers (e.g., port 443) can be spoofed or used for non-standard tunneling; DPI inspects actual payload signatures.
5. **Rule Evaluation (Detection):** Compares the decoded, flow-tracked, and protocol-identified traffic against active rulesets (`suricata.rules` or custom `local.rules`).
6. **Event Generation (Output):** Writes structured logs—most notably **EVE JSON** (`eve.json`)—recording alerts, connection metadata, and protocol events.

---

## 3. Core Detection Methodologies

Security engines rely on three primary analytical approaches to identify unauthorized or suspicious activity:

* **Signature-Based Detection:** Matches traffic payloads or headers against a database of known threat patterns, byte sequences, or strings. High precision for known threats, but blind to zero-days and encrypted payloads without decryption proxies.
* **Anomaly-Based Detection:** Establishes a baseline of "normal" behavior (e.g., typical hourly DNS query volume) and flags statistical deviations. Excellent for discovering novel attacks, but prone to high false-positive rates due to operational changes.
* **Behavioural-Based Detection:** Correlates sequences of actions and operational context over time (e.g., an abnormal DNS query followed immediately by an unauthorized RDP connection attempt).

---

## 4. Anatomy of a Suricata Signature

A Suricata rule consists of a **Rule Header** (defining action, protocol, IP addresses, ports, and direction) and **Rule Options** (enclosed in parentheses, defining match conditions, metadata, and unique identifiers).

```text
alert tcp $EXTERNAL_NET any -> $HOME_NET 3389 (msg:"POTENTIAL RDP BRUTE FORCE ATTACK"; flow:to_server,established; threshold:type threshold, track by_src, count 5, seconds 60; classtype:attempted-recon; sid:1000001; rev:1;)
```

### Breakdown of Rule Components:
1. **Action (`alert`):** Tells Suricata what to do when matched (`alert`, `pass`, `drop`, `reject`).
2. **Protocol (`tcp`):** The transport protocol to inspect (`tcp`, `udp`, `icmp`, `http`, `dns`, `tls`).
3. **Source / Destination IP & Port:** Defines source (`$EXTERNAL_NET any`) and target (`$HOME_NET 3389`).
4. **Direction Operator (`->`):** Indicates traffic flow direction from source to destination.
5. **`msg`:** The human-readable string displayed in logs when triggered.
6. **`flow:to_server,established`:** Ensures stateful matching, targeting only established TCP sessions moving toward the server.
7. **`threshold`:** Controls alert frequency (`count 5, seconds 60`) to prevent alert fatigue.
8. **`sid` (Signature ID):** Unique numerical identifier (SIDs above `1,000,000` are reserved for local custom rules).

---

## 5. False Positives vs. False Negatives

* **False Positive (FP):** The sensor flags legitimate traffic as malicious (e.g., routine IT software matching a broad signature). Causes analyst alert fatigue.
* **False Negative (FN):** An actual attack occurs, but the sensor fails to alert because no matching signature exists or rule conditions were too narrow. Causes unmonitored security breaches.

---

## 6. Job Market Applications

* **Detection Engineering:** Security engineers write, test, and tune custom Suricata signatures to detect emerging threats and organizational vulnerabilities.
* **SOC Tier 1/2 Analysis:** Analysts investigate EVE JSON alert logs (`eve.json`), correlating Suricata network triggers with endpoint telemetry during active incident triage.

# Technical Note: Zeek Event Correlation & Forensic Pivoting

**Author:** Serah Mulwa

**Module:** Day 19 - Network Threat Hunting with Zeek

## 1. Executive Summary

In Network Security Monitoring (NSM), analyzing Zeek logs in isolation is like reading single sentences torn from different books. A single record in `conn.log` or `dns.log` rarely tells the complete story of a security incident.

**Event correlation** is the analytical practice of stitching disparate logs, protocol records, and timestamps together to reconstruct a coherent, end-to-end timeline of network activity. This technical note explores explicit UID pivoting, implicit timestamp correlation, and practical SOC investigation workflows.

## 2. Explicit Correlation: The Power of the Zeek UID

Zeek assigns a globally unique 18-character string identifier—known as the **`uid`** (e.g., `"C9xKz13aR8b3xQ1"`)—to every master connection recorded in `conn.log`. 

When that same underlying session triggers application-layer activity (such as a DNS query, HTTP request, or TLS handshake), Zeek stamps those protocol records with the **exact same UID**. 

### Practical UID Pivoting Example:

1. **Step 1 (`conn.log`):** You spot an unusual UDP connection from an internal workstation (`10.0.2.15`) to an external IP (`203.0.113.53`) on port 53. You note its unique session identifier: **`uid: "C9xKz13aR8b3xQ1"`**.

2. **Step 2 (`dns.log`):** You search `dns.log` for `uid: "C9xKz13aR8b3xQ1"`. You discover that the UDP flow was a DNS query requesting `malicious-c2-domain.com`, which resolved to IP `198.51.100.99`.

3. **Step 3 (`conn.log` lookup on resolved IP):** You search `conn.log` for new connections originating from `10.0.2.15` to that newly resolved IP (`198.51.100.99`) occurring immediately after the DNS response. You find a TCP port 443 session (`uid: "CNewFlow456"`) that downloaded $45$ KB of data.

```
[ conn.log ] ──► UDP Flow (Port 53) ──► UID: C9xKz13aR8b3xQ1
                                              │
                                              ▼ (Shared UID Pivot)
[ dns.log  ] ──► Query: "malicious-c2-domain.com" ──► Resolves to 198.51.100.99
                                              │
                                              ▼ (Timestamp & IP Correlation)
[ conn.log ] ──► TCP Flow (Port 443) ──► UID: CNewFlow456 (Destination IP: 198.51.100.99, 45 KB Payload)

```

## 3. Implicit Correlation: Timestamp & Sequence Analysis

Not all related network events share the same `uid`. For example, a DNS query and a subsequent HTTPS connection belong to two distinct transport sessions, each generating its own unique `uid`. 

When UIDs change, analysts must rely on **timestamp and contextual correlation**:

* **Temporal Proximity:** Did the secondary connection occur within milliseconds or seconds of the DNS resolution?

* **IP Address Matching:** Does the destination IP of the new connection match one of the IP addresses returned in the `answers` array of the preceding DNS log?

* **Host Consistency:** Did the exact same internal workstation (`id.orig_h`) initiate both the DNS lookup and the subsequent web connection?

* **Behavioral Expectation:** Is this sequence normal for the application in question, or does it represent an uncharacteristic pattern (e.g., DNS lookup to an obscure domain followed immediately by an encrypted C2 connection)?

> **Analyst Caution:** Never assume two events belong together merely because they happened close to one another in time. Enterprise networks process thousands of concurrent queries; always verify IP mappings and protocol context before drawing conclusions.

## 4. SOC & Job Market Application

* **Tier 2 / Tier 3 Incident Response:** When investigating sophisticated Advanced Persistent Threats (APTs) that utilize multi-stage staging, senior analysts write multi-table correlation queries (joining `conn`, `dns`, `http`, and `ssl` logs) to map out complete adversary lateral movement and data exfiltration paths.

* **SIEM Engineering:** Security engineers write automated correlation rules in platforms like Splunk (SPL) or Elastic (KQL) to trigger high-fidelity alerts when specific sequences occur (e.g., *Alert if a host resolves a known DGA domain and establishes an outbound TLS connection within 10 seconds*).

## 5. Key Takeaways

* **The `uid` is your forensic compass:** Always check for matching UIDs when pivoting between Zeek protocol logs and connection records.

* **Correlating across logs turns raw data into actionable intelligence:** Individual logs show isolated actions; correlation reveals the complete narrative of an intrusion.

* **Verify before you conclude:** When UIDs are absent, rely on tight timestamp matching, resolved IP verification, and host consistency to validate your findings.

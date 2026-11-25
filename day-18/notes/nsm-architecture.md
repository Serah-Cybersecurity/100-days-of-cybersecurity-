# Technical Note: Network Security Monitoring & Detection Architecture

**Author:** Serah  Mulwa

**Date:** November 4, 2026

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

---

## 1. Executive Summary

Modern cybersecurity operations cannot rely strictly on perimeter firewalls. While firewalls enforce policy-based access control, sophisticated threats often bypass static perimeter rules using encrypted channels, legitimate stolen credentials, or application-layer exploits. **Network Security Monitoring (NSM)** provides continuous visibility into network communications, generating structured telemetry and alerts that enable Security Operations Center (SOC) analysts to detect, investigate, and respond to unauthorized or malicious activity.

This note documents the core architectural models of NSM, analyzing the operational differences between Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS), evaluating deployment topologies (passive TAP/SPAN vs. active inline), and comparing Network-based (NIDS) and Host-based (HIDS) security monitoring.

---

## 2. Network Security Monitoring Pipeline

Network Security Monitoring operates as an evidence-driven telemetry pipeline. Rather than making automated, isolated decisions on raw traffic alone, NSM captures, parses, and correlates network metadata to support analysts during investigations.

```
                      ENTERPRISE NETWORK TRAFFIC
                                  │
                                  ▼
                 [ SPAN Port / Network TAP Mirroring ]
                                  │
                                  ▼
                     [ Suricata NIDS Engine ]
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
[ Protocol Metadata Extraction ]              [ Signature Rule Evaluation ]
(HTTP, DNS, TLS, SSH, Flow Data)             (Custom & Emerging Threats Rules)
          │                                               │
          └───────────────────────┬───────────────────────┘
                                  │
                                  ▼
                   [ EVE JSON Telemetry Generation ]
                           (/var/log/suricata/)
                                  │
                                  ▼
                [ SIEM / Log Parser Ingestion ]
                                  │
                                  ▼
                   [ SOC Analyst Triage & Investigation ]
```

### The Operational Workflow:
$$\text{Traffic Capture} \longrightarrow \text{Protocol Decoding} \longrightarrow \text{Rule Matching} \longrightarrow \text{Telemetry Logging} \longrightarrow \text{Analyst Investigation}$$

1. **Traffic Acquisition:** Physical or virtual network interfaces mirror traffic via SPAN ports or TAPs without introducing latency or altering packet paths.
2. **Protocol Decoding & Inspection:** The detection engine (e.g., Suricata) decodes transport and application-layer protocols (TCP, UDP, HTTP, DNS, TLS) in real time.
3. **Telemetry Generation:** Observations are structured into JSON logs (`eve.json`), capturing both alerts (signature matches) and session metadata (flow durations, byte counts, request headers).
4. **Analyst Triage:** Security analysts query SIEM dashboards or run automation scripts to evaluate alert context, distinguishing benign network noise from genuine intrusions.

---

## 3. Intrusion Detection (IDS) vs. Intrusion Prevention (IPS)

A critical distinction in defensive architecture is the operational mode of the threat detection sensor: whether it operates **out-of-band** as an IDS or **inline** as an IPS.

```
IDS Deployment (Passive / Out-of-Band):
[ Client ] ───────────────> [ Switch / Router ] ───────────────> [ Server ]
                                   │ (SPAN / Mirror)
                                   ▼
                            [ Suricata IDS ] ───> [ Alert Log ]

IPS Deployment (Active / Inline):
[ Client ] ───> [ Suricata IPS Inline ] ───> [ Blocked / Allowed ] ───> [ Server ]
```

### 3.1 Intrusion Detection System (IDS)
* **Deployment Mode:** Passive, out-of-band.
* **Mechanism:** Receives a duplicated copy of network traffic mirrored from a switch or TAP.
* **Action:** Compares traffic against rulesets and generates alert logs when matches occur. It **cannot** drop or modify packets on the wire.
* **Operational Impact:** Zero risk to business continuity. If the IDS engine crashes or suffers hardware failure, live network traffic continues flowing uninterrupted.

### 3.2 Intrusion Prevention System (IPS)
* **Deployment Mode:** Active, inline (directly in the packet forwarding path).
* **Mechanism:** Every packet physically passes through the sensor engine before reaching its destination.
* **Action:** Evaluates traffic state and signatures in real time. Can actively **drop packets**, **reject TCP sessions (sending TCP RST)**, or dynamically apply perimeter firewall blocks.
* **Operational Impact:** High operational risk. A false positive in an IPS signature rule will result in blocking legitimate business communications, potentially causing unexpected service outages.

### 3.3 Comparative Architecture Matrix

| Feature | Intrusion Detection System (IDS) | Intrusion Prevention System (IPS) |
| :--- | :--- | :--- |
| **Primary Goal** | Threat visibility, alert generation, and investigation. | Automated threat mitigation and active packet blocking. |
| **Network Position** | Out-of-band / Passive (SPAN port or TAP). | Inline (placed directly in the network link). |
| **Traffic Impact** | None (operates on mirrored packet copies). | Direct (evaluates and forwards/drops live traffic). |
| **Alerting Behavior** | Writes alert entries to log files or SIEM. | Drops/resets connection AND writes alert entries. |
| **Failure Mode Risk** | Safe failure; sensor downtime does not disrupt network. | Single point of failure; sensor outage disrupts traffic flow unless fail-open hardware is used. |
| **False Positive Consequence** | Alert fatigue for SOC analysts. | Accidental service denial for legitimate users. |

---

## 4. NIDS vs. HIDS Telemetry Correlation

A mature Security Operations Center does not rely on a single vantage point. Effective threat hunting requires correlating **Network Intrusion Detection (NIDS)** with **Host Intrusion Detection (HIDS)**.

```
                     SECURITY INCIDENT TRIAGE
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
[ NIDS Telemetry (Suricata) ]                [ HIDS Telemetry (Sysmon/Wazuh) ]
- External source IP address                  - Executable binary path & hash
- Target port (e.g., 3389/TCP)                 - Process creation event (pid 4102)
- Payload signature / Byte pattern             - User identity & account privileges
- Connection duration & volume                - Registry / File modification logs
        │                                               │
        └───────────────────────┬───────────────────────┘
                                │
                                ▼
               [ Correlated True Positive Event ]
```

### 4.1 Network Intrusion Detection Systems (NIDS)
* **Vantage Point:** The wire (switches, core routers, network gateways).
* **Telemetry Collected:** IP headers, MAC addresses, port allocations, DNS request/response payloads, HTTP request URIs, TLS certificate fingerprints, and flow timing statistics.
* **Strengths:** Agentless deployment; monitors unmanaged endpoints, IoT hardware, and legacy systems where software agents cannot be installed.
* **Limitations:** Blinded by encrypted traffic payloads (unless SSL/TLS decryption is implemented); cannot determine if a target host was successfully compromised by a delivered payload.

### 4.2 Host Intrusion Detection Systems (HIDS)
* **Vantage Point:** The endpoint operating system (servers, domain controllers, endpoints).
* **Telemetry Collected:** Process execution parameters, command-line arguments, registry modifications, local account authentications, file integrity monitoring (FIM), and privilege escalation attempts.
* **Strengths:** Full visibility into local execution context and unencrypted memory/file activity regardless of network encryption.
* **Limitations:** Requires installing and managing software agents across every endpoint; can be disabled if an attacker gains root/administrative access on the host.

---

## 5. Analyst Mental Model & Best Practices

1. **IDS Provides Leads, Not Verdicts:** A triggered NIDS alert indicates that a network packet matched a specific signature, not that an intrusion succeeded. Analysts must verify if the target service was vulnerable and active.
2. **Context Over Volume:** High alert volume often leads to analyst burnout. Effective detection engineering relies on tuning signatures (using flow state tracking and thresholding) to generate high-fidelity alerts.
3. **Always Cross-Correlate:** Never conclude an investigation based solely on NIDS alerts. Validate network observations against host-level process creation logs, auth logs, and firewall state tables.

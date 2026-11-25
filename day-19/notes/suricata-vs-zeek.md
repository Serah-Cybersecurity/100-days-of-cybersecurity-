# Technical Note: Suricata vs. Zeek - Dual-Pillar Network Security Monitoring

**Author:** Serah Mulwa  
**Module:** Day 19 - Network Threat Hunting with Zeek  

---

## 1. Executive Summary

In enterprise defensive security operations, a common misconception is that organizations must choose between deploying Suricata or Zeek. In reality, modern Security Operations Centers (SOCs) deploy both platforms in tandem. 

While **Suricata** excels at signature-based detection and inline rule enforcement (IDS/IPS), **Zeek** operates as an event-driven network analysis framework that transforms raw network packets into rich, structured protocol metadata (`conn.log`, `dns.log`, `ssl.log`, `http.log`). This technical note explores their architectural differences, operational synergies, and practical SOC integration workflows.

---

## 2. Capability Matrix

| Feature / Capability | Suricata (IDS/IPS) | Zeek (NSM Framework) |
| :--- | :--- | :--- |
| **Primary Focus** | Signature threat detection & packet filtering | Network state modeling, protocol parsing & logging |
| **Signature Matching** | **Core Strength** (Snort/Suricata syntax) | Secondary (handled via scripts and Notice framework) |
| **Alert Trigger** | Generates discrete alerts on rule match | Captures session metadata for *all* observed traffic |
| **Connection Tracking** | Basic flow tracking in `eve.json` | **Core Strength** (`conn.log` state modeling) |
| **Protocol Decoders** | Protocol keywords & sticky buffers | Extensive decoders via C++ engine and Spicy framework |
| **Custom Scripting** | Lua scripting & rule keywords | Turing-complete, event-driven Zeek scripting language |
| **Primary Log Output** | Single unified `eve.json` stream | Specialized modular logs (`conn.log`, `dns.log`, etc.) |
| **Primary SOC Role** | Immediate alert generation & inline blocking | Deep forensic analysis, threat hunting & baselining |

---

## 3. Practical SOC Integration Workflow

In an operational SOC pipeline, Suricata acts as the **signal** (alarm), while Zeek provides the **context** (evidence).

```text
                             [ RAW NETWORK TRAFFIC ]
                                        │
           ┌────────────────────────────┴────────────────────────────┐
           ▼                                                         ▼
  [ SURICATA IDS ENGINE ]                                  [ ZEEK NSM SENSOR ]
           │                                                         │
           ▼                                                         ▼
"ALERT: SID 1000001 - DNS Query"                            Generates Structured Logs
(Triggered in eve.json)                                    (conn.log, dns.log, ssl.log)
           │                                                         │
           └────────────────────────────┬────────────────────────────┘
                                        ▼
                          [ SOC ANALYST TRIAGE PIPELINE ]
                                        │
  1. Extract timestamp, Source IP, and Target IP from Suricata Alert.
  2. Query Zeek's dns.log to inspect transaction IDs and resolved answers.
  3. Extract Zeek UID (e.g., C9xKz13aR8b3xQ1).
  4. Pivot across conn.log and ssl.log using the UID to evaluate session 
     duration, bytes transferred, TLS handshake SNI, and CA validity.
```

### Incident Scenario Example:
1. **Suricata Alert:** Suricata detects an outbound request matching a local rule for `example.com` and fires an alert. Suricata confirms *that* a pattern matched, but lacks complete session context.
2. **Zeek Metadata Pivot:** The analyst opens `dns.log` in Zeek and locates the query made at that exact timestamp. Zeek provides the client IP (`10.0.2.15`), DNS resolver (`192.168.100.1`), response code (`NOERROR`), IP returned (`104.20.23.154`), and a unique session identifier: **`UID: C9xKz13aR8b3xQ1`**.
3. **Session Correlation:** The analyst uses the `UID` to pivot directly into `conn.log` and `ssl.log`, discovering that $2.1$ KB of data was transferred over a valid $1.2$-second TLS v1.3 connection. 
4. **Outcome:** The analyst proves the activity was a standard, benign web session and closes the alert without escalating false alarms.

---

## 4. Job Market Relevance

* **SOC Tier 1 / Tier 2 Analyst:** Leverages Suricata alerts for immediate threat visibility and uses correlated Zeek logs to rapidly perform root-cause analysis.
* **Threat Hunter:** Utilizes Zeek's detailed protocol logs to establish traffic baselines, identify long-duration beaconing connections, and detect covert channels.
* **Detection Engineer:** Authors custom Suricata signatures for known static IOCs while writing custom `.zeek` policy scripts to flag complex, stateful behavior anomalies.

---

## 5. Key Takeaways

* **Suricata tells you THAT something matched; Zeek tells you EVERYTHING that happened.**
* **Never view these tools as competitors:** They form the dual pillars of modern enterprise network security monitoring.

# Technical Note: Proactive Threat Hunting Methodology & 5-Stage Framework

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

## 1. Executive Summary

Traditional Security Operations Center (SOC) workflows are predominantly reactive—analysts wait for automated alerts to fire, triage the notification, and close the ticket. While necessary for high-volume triage, reactive monitoring leaves organizations blind to sophisticated, multi-stage threats that evade out-of-the-box signatures.

This technical note documents the transition from reactive detection to proactive threat hunting. It outlines the foundational 5-stage threat-hunting framework and details how a testable hypothesis is validated by correlating multi-tool telemetry (Suricata alerts and Zeek connection logs) using Community ID flow hashes.

## 2. Reactive Detection vs. Proactive Threat Hunting

Understanding the operational differences between reactive alerting and proactive hunting is essential for junior analysts entering the cybersecurity job market:

| Dimension | Reactive Detection (Alert Triage) | Proactive Threat Hunting |
| :--- | :--- | :--- |
| **Starting Trigger** | An automated SIEM alert or IDS signature match. | An analyst-formulated investigative question or hypothesis. |
| **Methodology** | Evaluate an already-flagged event to determine legitimacy. | Search through un-alerted network telemetry for hidden anomalies. |
| **Primary Goal** | Minimize Mean Time to Detect (MTTD) and Respond (MTTR). | Uncover stealthy activity, blind spots, or unruled telemetry gaps. |
| **Typical Outcome** | Incident escalation, host isolation, or alert closure. | Tuned detection rules, updated baselines, and improved posture. |

## 3. The Five Stages of a Threat Hunt

Every structured threat hunt follows a rigorous, repeatable 5-stage methodology to ensure findings are defensible and evidence-based:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 1. Formulate     │────>│ 2. Identify      │────>│ 3. Analyze       │
│    Hypothesis    │     │    Evidence      │     │    Evidence      │
└──────────────────┘     └──────────────────┘     └────────┬─────────┘
                                                           │
                         ┌──────────────────┐              │
                         │ 5. Document      │<─────────────┴───────────┐
                         │    Conclusion    │                          │
                         └──────────────────┘                          ▼
                                   ▲                      ┌──────────────────┐
                                   │                      │ 4. Correlate     │
                                   └──────────────────────│    Evidence      │
                                                          └──────────────────┘
```

### Stage 1: Formulate a Hypothesis
A valid threat hunt begins with a testable statement. Rather than searching logs aimlessly, analysts ask a specific question based on MITRE ATT&CK techniques, threat intelligence, or system changes.
* **Our Lab Hypothesis:** *"If a workstation initiates a DNS query for `example.com` that triggers our custom Suricata rule, that exact session will also be logged in Zeek's `conn.log` and `dns.log`, sharing an identical Community ID hash."*

### Stage 2: Identify Required Evidence
Determine beforehand which log files, fields, and tools are needed to prove or disprove the hypothesis:
* **Packet Capture:** `pcap/day20.pcap`
* **Suricata IDS:** `eve.json` (`alert.signature`, `community_id`)
* **Zeek Metadata:** `conn.log` (`uid`, `community_id`, `conn_state`) and `dns.log` (`query`, `rcode_name`)

### Stage 3: Analyze Evidence
Inspect each tool's output independently. Verify that Suricata captured the signature alert and that Zeek dissected the application and transport layers correctly without assuming the logs will look identical.

### Stage 4: Correlate Evidence
Bridge the log files together using a universal flow identifier (**Community ID**). Match Suricata's `community_id` directly to Zeek's `community_id` to confirm that both engines are analyzing the exact same network conversation.

### Stage 5: Reach and Document Conclusions
Synthesize the findings into an objective report. Separate verified facts (what the logs show) from analyst interpretations (what those facts mean), and note any data limitations.

## 4. Key Portfolio & Job Market Takeaways

* **Hypothesis-driven investigation:** Random log browsing is inefficient; professional threat hunting always starts with a clear question.
* **Multi-tool validation:** Relying on a single security tool creates blind spots. Correlating Suricata and Zeek provides complete visibility.
* **Defensible reporting:** Documenting your hunt using a structured 5-stage framework proves to hiring managers that you possess analytical discipline.

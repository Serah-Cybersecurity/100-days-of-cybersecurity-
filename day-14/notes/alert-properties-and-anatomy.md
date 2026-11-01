# Deep Dive: SOC Alert Properties, Timestamp Forensics & Ticket Lifecycle

## 1. Executive Summary

A security alert is not just a simple alarm; it is a structured data object containing rich metadata designed to give Level 1 SOC Analysts immediate context regarding security events. 

Understanding alert properties allows analysts to pivot rapidly during triage, calculate log ingestion latency, preserve chronological accuracy during forensics, manage ticket states, and prevent collision with other SOC team members.

---

## 2. The Anatomy of a SOC Alert (14 Core Key-Value Properties)

Modern SIEM systems (Splunk ES, Microsoft Sentinel, Elastic SIEM, Wazuh) standardise detection outputs into structured key-value pairs. Below are the 14 essential properties every SOC analyst must master:

| # | Property Field | Data Type / Format | Description & Forensic Purpose |
| :-: | :--- | :--- | :--- |
| **1** | `Alert ID` | UUID / String | Unique identifier for referencing tickets across teams, logs, and escalation channels (e.g., `ALT-2026-1104-8834`). |
| **2** | `Alert Title` | String | Human-readable name describing the triggered behavior (e.g., *SSH Brute Force Followed by Successful Authentication*). |
| **3** | `Event Time` | ISO-8601 Timestamp | **The Forensic Anchor.** The exact UTC time the activity occurred on the endpoint/host (`2026-11-01T18:42:38Z`). |
| **4** | `Alert Time` | ISO-8601 Timestamp | The UTC time the SIEM detection engine processed the rule and generated the alert object (`2026-11-01T18:50:03Z`). |
| **5** | `Initial Severity` | Enum (`Low`, `Med`, `High`, `Critical`) | Automated risk assessment based on baseline rule weighting. Requires human verification. |
| **6** | `Workflow Status` | Enum | Current state of the alert ticket (`New`, `In Progress`, `Pending`, `Escalated`, `Closed`). |
| **7** | `Assignee` | String / User ID | The SOC analyst currently claiming operational ownership of the investigation. |
| **8** | `Target Host / Asset` | FQDN / Hostname | Device targeted or compromised (`LINUX-LAB-01`). Defines asset criticality context. |
| **9** | `User Account` | String | Identity or service account associated with the telemetry (`root`, `j.doe`, `svc_sql`). |
| **10** | `Source IP Address` | IPv4 / IPv6 Address | Origin IP of network connection or login attempt (`192.168.1.50` or external IP). |
| **11** | `Destination IP Address`| IPv4 / IPv6 Address | Receiver address of traffic or command target (`10.0.4.15`). |
| **12** | `Detection Rule ID` | String / Rule Name | Unique identifier for the underlying SIEM rule or Sigma logic (`win_bruteforce_ssh_01`). |
| **13** | `Telemetry Evidence` | JSON / Array | Raw sample records, process commands, or log snippets attached to the alert trigger. |
| **14** | `MITRE ATT&CK Mapping`| Technique Identifier | Standardised threat classification (e.g., `T1110.001 - Password Guessing`). |

---

## 3. Alert Time vs. Event Time Latency Forensics

One of the most critical analytical errors in junior SOC operations is confusing **Alert Time** with **Event Time**.

* **Event Time ($T_{\text{event}}$):** The real-time timestamp recorded by the operating system kernel, network gateway, or application log header when the action took place.
* **Alert Time ($T_{\text{alert}}$):** The timestamp recorded by the central SIEM database when the rule query ran and instantiated the alert record.

### 3.1 Log Ingestion Latency Pipeline

Log telemetry experiences multiple delays during enterprise transport:

```
[09:00:00 UTC] Event Occurs on Endpoint (Failed logons executed)
      │
      ▼ (Agent batching & syslog transport delay: 3 mins)
[09:03:00 UTC] Raw Log Ingested into SIEM Indexer
      │
      ▼ (SIEM scheduled detection rule execution delay: 1 min)
[09:04:00 UTC] Alert Engine Triggers & Creates Ticket (Alert Time)
      │
      ▼ (Queue assignment delay: 2 mins)
[09:06:00 UTC] L1 Analyst Opens Ticket
```

### 3.2 Ingestion Latency Formula & Forensic Rule

$$
\text{Latency Delta } (\Delta t) = T_{\text{alert}} - T_{\text{event}}
$$

> **Forensic Golden Rule:** When searching for post-compromise activity (e.g., execution of `cat /etc/passwd` or command shell spawns), **always anchor log search windows around Event Time ($T_{\text{event}}$), NOT Alert Time ($T_{\text{alert}}$)**. If $\Delta t = 15 \text{ minutes}$, querying logs around $T_{\text{alert}}$ will completely miss the attacker's footprint.

---

## 4. Alert Lifecycle & Workflow Statuses

To ensure operational efficiency across multi-shift security teams, alerts progress through standard state transitions:

```
                     ┌───────────────────────────────┐
                     │          NEW (Unassigned)     │
                     └───────────────┬───────────────┘
                                     │
                             (Analyst Claims)
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │          IN PROGRESS          │
                     └───────────────┬───────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            │                        │                        │
            ▼                        ▼                        ▼
┌───────────────────────┐┌───────────────────────┐┌───────────────────────┐
│     PENDING INFO      ││       ESCALATED       ││        CLOSED         │
│(Awaiting User/IT Input)││(Handover to Tier 2/IR)││(TP / FP / BP Verdict) │
└───────────────────────┘└───────────────────────┘└───────────────────────┘
```

### State Descriptions:
1. **New:** Alert ingested; awaiting analyst assignment.
2. **In Progress:** Assigned to an analyst; active log correlation and context gathering underway.
3. **Pending Info:** Paused while requesting confirmation from system owners, HR, or IT managers.
4. **Escalated:** Confirmed malicious/suspicious activity forwarded to Tier 2 IR with detailed handover notes.
5. **Closed:** Investigation complete. A final verdict tag (**True Positive**, **False Positive**, or **Benign Positive**) must be applied.

---

## 5. Ticket Ownership Protocols (Avoiding Collision)

In enterprise SOCs running 24/7 shifts with multiple analysts, lack of ticket ownership creates duplicated work, missed SLAs, and inconsistent verdicts.

### 4-Step SOP for SOC Analyst Ticket Ownership:

1. **Claim Before Querying:** Before running any Splunk SPL, Elastic, or terminal commands, assign the `Assignee` field to your identity and update the status to `In Progress`.
2. **Check for Parallel Tickets:** Query the SIEM queue for duplicate alerts originating from the same `Source IP` or targeting the same `Host` within the past 24 hours.
3. **Inspect Existing Incidents:** Check if the host is already linked to an open master Incident Ticket. If found, merge or link the alert to avoid redundant investigations.
4. **Log Triage Footprints:** Record all queries executed and initial observations directly into the ticket comment log so relief analysts during shift handover have full visibility.

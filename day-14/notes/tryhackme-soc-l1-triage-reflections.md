# Practical Lab Journal & Reflections: TryHackMe SOC L1 Alert Triage

## 1. Executive Summary & Lab Overview

**Platform:** TryHackMe  
**Room:** SOC L1 Alert Triage  
**Analyst:** Serah  Mulwa (Level 1 SOC Analyst)  
**Date Completed:** November 2, 2026  
**Purpose:** Personal audit-ready lab journal documenting the practical application of 9-step triage workflows, metadata extraction, risk prioritisation, and alert verdict classification inside a simulated enterprise SIEM dashboard environment.

---

## 2. Practical Reflections & Core Observations

### 2.1 Events vs. Alerts Reflection: What Differentiates Raw Telemetry from Actionable Alerts?

During dashboard operations, the fundamental distinction between an un-analyzed raw event and a generated SIEM alert becomes immediately clear:

* **Raw Events (Unfiltered Telemetry):** Individual activity records streamed continuously from endpoint security agents, firewalls, active directories, and proxy servers (e.g., a standard Windows Event ID 4624 successful logon or a routine DNS request). Events occur by the millions per day and represent normal, baseline system operations.
* **SIEM Alerts (Correlated Signals):** High-fidelity triggers created when a detection rule or correlation engine identifies one or more raw events matching a predefined threat threshold, known Indicator of Compromise (IoC), or anomalous behavioral pattern (e.g., 15 failed authentication events followed by a successful login within 30 seconds). 

An alert signifies that raw data has crossed an analytical threshold requiring human investigative intervention.

---

### 2.2 Metadata Field Utility: High-Value Alert Properties in Initial Triage

When opening an alert card in the simulated SIEM queue, six specific metadata properties provided the highest investigative yield:

1. **Timestamp (`@timestamp` / `event_time`):** Establishes when the activity occurred in UTC. Crucial for calculating ingestion latency ($\Delta t$) and anchoring the event timeline.
2. **Target Host (`host.name` / `dest_ip`):** Identifies the target system, allowing immediate cross-referencing against the enterprise asset inventory to assess criticality (Production Gateway vs. Dev Sandbox).
3. **User Account (`user.name` / `target_user`):** Identifies the privilege boundary (e.g., `root`, `SYSTEM`, `domain_admin` vs. standard corporate domain user).
4. **Source IP (`source.ip`):** Pinpoints network origin. Used for geofencing, subnetwork identification, and external threat intelligence reputation queries (VirusTotal / AbuseIPDB).
5. **Process Lineage (`process.name` / `process.command_line`):** Reveals process execution chains (e.g., `outlook.exe` spawning `powershell.exe -enc ...`), providing immediate visibility into adversary tactics.
6. **Rule Name & Severity (`rule.title` / `severity`):** Defines the underlying detection hypothesis and initial static risk rating assigned by detection engineers.

---

### 2.3 Queue Prioritisation Rationale: Managing Alert Fatigue

Queue management requires overriding raw chronological order (First-In, First-Out) to address high-risk threats first. Prioritisation decisions in the lab were made using a multi-vector risk model:

$$\text{Priority} = \text{Technical Severity} + \text{Asset Criticality} + \text{Threat Momentum} + \text{Rule Fidelity}$$

* **Asset Criticality Takeaway:** A `MEDIUM` severity brute-force alert targeting `PAYMENT-GATEWAY-01` (Tier 1 Crown Jewel) was elevated to **P1 — Critical**, taking precedence over a `HIGH` severity encoded PowerShell execution alert on `DEV-SANDBOX-04` (Tier 3 Lab Box).
* **Threat Momentum Takeaway:** Alerts with active, ongoing TCP sessions or live post-exploitation command executions were prioritized over historical log events where the binary had already terminated.

---

### 2.4 Workflow Execution Checklist: The Standardized Investigation Process

Every alert triaged in the lab was evaluated strictly against a 9-step workflow to guarantee consistency:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      9-STEP TRIAGE WORKFLOW ENGINE                     │
└────────────────────────────────────────────────────────────────────────┘
 [1] Take Ownership ─────────► [2] Understand Detection ──► [3] Map Entities
                                                                  │
 [6] Baseline Check ─────────◄ [5] Build UTC Timeline ────◄ [4] Validate Logs
        │
        ▼
 [7] Enrich Context ─────────► [8] Assign Verdict ────────► [9] Document Notes
```

1. **Claim Ticket:** Assigned alert to self, updating status from `New` to `In Progress` (timestamped MTTA).
2. **Rule Analysis:** Read detection rule parameters to understand threshold triggers.
3. **Entity Extraction:** Mapped affected host, user, source IP, and binary path.
4. **Log Integrity Check:** Queried SIEM indexers directly to verify raw log authenticity and rule match accuracy.
5. **Timeline Construction:** Constructed a chronological sequence of events using UTC timestamps.
6. **Baseline Comparison:** Verified if the user or host normally executed such actions (e.g., checking scheduled administrative task windows).
7. **Context Enrichment:** Cross-referenced source IPs against Threat Intel feeds and internal Change Management tickets (`CHG-XXXX`).
8. **Verdict Decision:** Classified the alert as `TP`, `FP`, `BP`, or `Inconclusive`.
9. **Documentation:** Logged audit-ready closure notes and recommendations.

---

### 2.5 Escalation Triggers: When to Escalate vs. When to Close

Clear boundaries were established to distinguish between closing tickets at Tier 1 and escalating to Tier 2 (Incident Response):

* **Escalation Triggers (Escalate to L2 / IR):**
  * Confirmed **True Positive (TP)** involving credential dumping (LSASS), lateral movement, unauthorized active remote access, or C2 beaconing on any production asset.
  * Activity involving compromised `Domain Admin` or privileged service accounts.
  * **Inconclusive** alerts on Tier 1 critical assets where log telemetry was wiped, corrupted, or incomplete (requiring host-level volatile memory acquisition).

* **Ticket Closure Conditions (Close at Tier 1):**
  * **False Positive (FP):** Detection rule incorrectly flagged benign activity due to flawed regex or overly broad signature (submitted tuning request).
  * **Benign Positive (BP):** Event genuinely occurred but was verified as authorized via approved Change Request or scheduled vulnerability scanner.
  * **Duplicate (DUP):** Event already actively tracked under a parent Incident Ticket.

---

### 2.6 Investigation Comment Standards: Writing Audit-Ready Ticket Notes

Professional ticket documentation must be objective, concise, and fully reproducible. Every closed or escalated ticket in the lab contained three standardized sections:

```markdown
### SOC TICKET CLOSURE & HANDOVER SUMMARY

**Ticket ID:** ALT-2026-9901  
**Analyst:** Serah Mulwa (L1 SOC Analyst)  
**Final Verdict:** TRUE POSITIVE (CONFIRMED COMPROMISE)  

#### 1. Executive Overview
Triggered by rule 'SSH Brute Force Followed by Successful Authentication' on PAYMENT-GATEWAY-01 from external IP 185.220.101.5.

#### 2. Investigative Evidence & Timeline (UTC)
- **18:42:10 UTC:** 12x failed SSH login attempts for user 'root'.
- **18:42:38 UTC:** Successful SSH authentication for user 'root' from 185.220.101.5.
- **18:43:02 UTC:** Post-compromise execution: 'cat /etc/passwd'.
- **Enrichment:** Source IP 185.220.101.5 confirmed Tor Exit Node on Threat Intel feeds. No approved change request found.

#### 3. Action Taken & Next Steps
- Host isolated from network segment.
- Firewall rule submitted to block 185.220.101.5.
- Escalated to Tier 2 IR team for SSH host key rotation and memory dump analysis.
```

---

## 3. Summary of Key Learnings

* **Never rely solely on static severity tags:** Asset business value and threat momentum dictate true operational priority.
* **Verify raw logs before deciding:** Alerts represent rule matches, not guaranteed maliciousness. Always query raw log event records.
* **Documentation is mandatory:** An un-documented investigation is legally and operationally non-existent.

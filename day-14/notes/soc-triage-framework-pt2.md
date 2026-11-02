# The 9-Step Tier 1 SOC Alert Triage Workflow

## 1. Executive Summary

Alert triage is the structured, step-by-step investigative process executed by Level 1 Security Operations Center (SOC) analysts to evaluate incoming security alerts. 

Without a rigid workflow, analysts risk falling into chaotic investigation patterns—missing critical indicators of compromise, duplicating work across shifts, or failing to meet strict Service Level Agreements (SLAs). 

This framework defines the 9 standardized operational steps required to transition an alert from raw SIEM trigger to audit-ready ticket disposition.

---

## 2. The 9-Step Standardized Triage Workflow

```
[ Step 1: Take Ownership ] ──► [ Step 2: Understand Detection ] ──► [ Step 3: Identify Entities ]
                                                                             │
[ Step 6: Baseline Check ]  ◄── [ Step 5: Build Timeline ]     ◄── [ Step 4: Validate Evidence ]
        │
        ▼
[ Step 7: External Context ] ──► [ Step 8: Decide Disposition ] ──► [ Step 9: Document Reasoning ]
```

---

### Step 1: Take Ownership (Administrative & Operational Setup)
Before opening log search dashboards or running queries, an analyst must claim the ticket to establish operational accountability.

* **Ticket Claiming:** Update the `Assignee` field to your analyst ID and change the workflow state from `New` to `In Progress`.
* **MTTA Recording:** Timestamp your investigation start time to track your **Mean Time to Acknowledge (MTTA)** metric.
* **Duplicate Check:** Query the queue for related alerts originating from the same `Source IP`, targeting the same `Host`, or involving the same `Username` within the last 24 hours.
* **Incident Check:** Verify whether an active parent Incident Ticket is already open for the target host to avoid parallel, redundant investigations.

---

### Step 2: Understand the Detection (Analyzing Rule Logic)
Do not attempt to investigate an alert without first understanding *why* the detection rule triggered.

* **Rule Logic Analysis:** Read the detection rule query (Splunk SPL, Elastic EQL, Sigma rule, or YARA signature).
* **Threshold & Time Windows:** Determine if the rule triggers on a single event or a volume threshold (e.g., 10 failed logins within 60 seconds).
* **Match Fields:** Identify which specific log fields caused the match (`EventID=4625`, `process_name=cmd.exe`, etc.).
* **Known Limitations:** Review rule documentation for known false-positive triggers (e.g., vulnerability scanners or backup scripts).

---

### Step 3: Identify Affected Entities (Mapping the Blast Radius)
Extract and categorize all distinct entities linked to the alert to evaluate the potential blast radius.

* **Target Host / Asset:** Hostname, FQDN, or IP address (`LINUX-LAB-01`, `10.0.4.15`). Identify asset criticality (Production DB vs. Staging Lab).
* **User Identity:** Account name, SID, or service principal (`root`, `SYSTEM`, `svc_backup`). Determine account privilege levels.
* **Network Nodes:** Source IP, Destination IP, ports, and protocols (`192.168.1.50:44220`).
* **Process Lineage:** Parent process, child process, command-line arguments, and binary hashes (SHA-256).

---

### Step 4: Validate Underlying Evidence (Raw Log Verification)
Never trust an alert dashboard header at face value. Verify the existence and integrity of the underlying raw log records.

* **Log Existence:** Query SIEM indexers to pull raw events matching the alert timestamp.
* **Timestamp Consistency:** Confirm that Event Time on the host matches Alert Time in the SIEM (accounting for ingestion latency $\Delta t$).
* **Field Integrity:** Verify that usernames, IP addresses, and event IDs are complete and untampered with.
* **Log Completeness:** Ensure log forwarding agents were active and did not drop events during the incident window.

---

### Step 5: Build a Chronological Timeline (Reconstructing the Event)
Reconstruct the exact sequence of events leading up to, during, and immediately following the alert trigger.

```text
[18:42:10 UTC] — Event ID 4625: 10x Failed SSH login attempts from 192.168.1.50 (user: root)
[18:42:38 UTC] — Event ID 4624: SUCCESSFUL SSH login for user root from 192.168.1.50
[18:43:02 UTC] — Command Execution: cat /etc/passwd (PID 10499)
[18:43:15 UTC] — Network Connection: Outbound curl to http://malicious-c2.com/stage2.sh
```

* **Golden Rule of Timelines:** Build the timeline directly from UTC timestamps. Do not invent a narrative first and selectively pick evidence to match it.

---

### Step 6: Compare Against Normal Behavior (Baseline Analysis)
Compare observed behavior against historical operational baselines for the specific asset and identity.

* **User Baselines:** Does this account normally log in at this hour? Does it normally connect from this IP address or subnet?
* **System Baselines:** Does this host normally launch PowerShell or curl scripts? Is this process part of a scheduled cron job?
* **Maintenance Windows:** Check if the host was undergoing scheduled IT updates or software deployment.

---

### Step 7: Check Relevant External Context (Enrichment)
Enrich your internal investigation with external context and threat intelligence data.

* **Change Management Portals:** Check ServiceNow / Jira change requests for authorized maintenance (`CHG-XXXX`).
* **Threat Intelligence Feeds:** Check IP reputation, domain creation age, and file hash signatures via VirusTotal, AbuseIPDB, or internal Threat Intelligence Platforms (TIP).
* **System Owner Inquiry:** Contact system administrators or identity owners to verify unscheduled actions when necessary.

---

### Step 8: Decide the Disposition (Assigning the Verdict)
Assign the final operational verdict supported strictly by the evidence gathered:

* **True Positive (TP):** Malicious / unauthorized activity confirmed. Initiate containment and escalate to L2 / Incident Response.
* **False Positive (FP):** Activity misinterpreted by a flawed rule. Close ticket and request rule tuning.
* **Benign Positive (BP):** Activity occurred as flagged, but was fully authorized (e.g., approved penetration test or scanner). Close ticket with reference link.
* **Inconclusive:** Evidence insufficient due to corrupted or missing logs. Document gaps and escalate for deep-dive forensics.
* **Duplicate:** Activity tracked under an active parent incident. Link and close ticket.

---

### Step 9: Document Your Reasoning (Audit-Ready Reporting)
Write detailed, reproducible ticket closure or escalation notes so relief analysts or auditors can verify your findings.

```markdown
### TICKET TRIAGE SUMMARY & HANDOVER REPORT

**Ticket ID:** ALT-2026-1104
**Assigned Analyst:** Level 1 SOC Analyst
**Disposition:** TRUE POSITIVE (CONFIRMED COMPROMISE)

#### 1. Executive Summary
High-severity alert triggered for SSH brute force followed by successful root authentication on target host `LINUX-LAB-01` from source IP `192.168.1.50`.

#### 2. Evidence & Timeline Analysis
- **18:42:10 UTC:** 10x failed authentication attempts for user `root`.
- **18:42:38 UTC:** Successful authentication for user `root` from source IP `192.168.1.50`.
- **18:43:02 UTC:** Post-exploitation command executed: `cat /etc/passwd`.
- **18:43:15 UTC:** Outbound C2 connection initiated via `curl`.

#### 3. Operational Actions Taken
1. Terminated active SSH session (PID 10499) on `LINUX-LAB-01`.
2. Isolated host `LINUX-LAB-01` from network segment.
3. Escalated ticket to Tier 2 Incident Response for credential rotation and DFIR image acquisition.
```

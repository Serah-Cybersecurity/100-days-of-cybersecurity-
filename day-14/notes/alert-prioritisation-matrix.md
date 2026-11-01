# Deep Dive: SOC Alert Prioritisation & Severity Scoring Framework

## 1. Executive Summary

Alert prioritisation is the operational methodology used by Security Operations Center (SOC) analysts to determine the order in which incoming security alerts are investigated. 

In enterprise environments ingesting thousands of security telemetry events per minute, working through an alert queue strictly chronologically (First-In, First-Out) leads to missed threats and unacceptably high Mean Time to Detect (MTTD). Effective prioritisation ensures human analytical capacity is immediately directed toward high-impact threats.

## 2. Core Operational Distinctions: Severity vs. Priority

Understanding the difference between **Severity** and **Priority** is mandatory for professional SOC operations:

* **Severity (Static Technical Potential):** An assessment of how damaging an activity *could be* if true. It is hardcoded into detection logic (e.g., malware execution is inherently higher severity than a mistyped password).

* **Priority (Dynamic Operational Urgency):** An analytical determination of how *urgently* the alert must be triaged right now. Priority incorporates severity alongside real-time business context, asset criticality, threat momentum, and detection confidence.

### 2.1 Comparative Breakdown

| Dimension | Severity | Priority | 
| ----- | ----- | ----- | 
| **Primary Question** | *"How dangerous is this activity technically?"* | *"How fast must we investigate this right now?"* | 
| **Determining Agent** | Detection Engine / Rule Creator (Sigma, EDR) | SOC Analyst / Risk Engine | 
| **Mutability** | Static (Fixed per alert rule) | Dynamic (Fluctuates based on context) | 
| **Core Inputs** | Attack technique, tool signature, CVE score | Asset value, user privilege, active vs historical | 

## 3. Dynamic Priority Calculation Model

Enterprise SOCs calculate final operational priority ($P$) by evaluating three core risk vectors:

$$
\text{Priority } (P) = f(\text{Technical Severity}, \text{Asset Criticality}, \text{Threat Momentum})
$$

```
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│   Technical Severity   │  +   │   Asset Criticality    │  +   │    Threat Momentum     │
│ (Low, Med, High, Crit) │      │ (Crown Jewel vs Lab)   │      │  (Active vs Historical)│
└───────────┬────────────┘      └───────────┬────────────┘      └───────────┬────────────┘
            │                               │                               │
            └───────────────────────────────┼───────────────────────────────┘
                                            │
                                            ▼
                        ┌───────────────────────────────────────┐
                        │    FINAL OPERATIONAL PRIORITY SCORE   │
                        │        (P1, P2, P3, P4 Matrix)        │
                        └───────────────────────────────────────┘

```

### 3.1 Priority Scoring Matrix (P1 to P4)

| Priority Level | Classification | SLA Window | Target Actions & Handling Strategy | 
| ----- | ----- | ----- | ----- | 
| **P1** | **Critical** | $< 15$ Mins | Immediate triage. Active threat to crown-jewel assets (e.g., Domain Controller, Prod DB). Immediate host isolation and Tier 2 escalation. | 
| **P2** | **High** | $< 30$ Mins | Rapid investigation. Suspicious execution or privileged credential abuse on enterprise workstations or staging servers. | 
| **P3** | **Medium** | $< 2$ Hours | Queue review. Standard alerts requiring context verification (e.g., single host brute-force failure, unauthorized admin tool). | 
| **P4** | **Low** | $< 8$ Hours | Batch triage / End of shift. Informational policy triggers, automated scan noise, or isolated test environment activity. | 

## 4. Prioritisation Decision Checklist for L1 Analysts

When triaging multiple concurrent queue alerts, run through this 5-point assessment:

1. **Asset Criticality Check:** Is the target system a Tier-1 asset (Domain Controller, Payment Gateway, Production DB) or an isolated sandbox VM?

2. **Temporal Momentum:** Is the attack actively occurring right now with open sessions, or did it execute hours ago and terminate?

3. **Detection Fidelity:** Is the rule triggered by a high-confidence signature (e.g., Mimikatz hash) or a noisy behavioral heuristic?

4. **Scope of Impact:** Is the event restricted to a single endpoint, or triggering across multiple subnets simultaneously?

5. **Privilege Elevation:** Does the target account hold domain administrative rights or service execution privileges?

## 5. What to Document in Ticket Prioritisation

Always record the rationale behind adjusting ticket priority in your investigation notes:

```
### TRIAGE PRIORITISATION LOG
- Alert ID: ALT-2026-1104
- Rule Severity: High
- Assigned Priority: P1 - Critical (Elevated due to Asset Context)
- Prioritisation Rationale: 
  * Target Host: DB-PROD-01 (Production SQL Server - Crown Jewel)
  * Account: root
  * Rationale: Rule severity 'High' elevated to P1 operational priority due to high asset criticality and active successful authentication following failed attempts.
```

## 6. Golden Rules for SOC Analysts

* **Never rely solely on severity tags:** High-severity alerts on disposable lab machines do not outweigh medium-severity alerts on production infrastructure.

* **Context dictates urgency:** Always verify the host, user role, and network segment before determining triage order.

* **Maintain SLA compliance:** Clear lower-priority tickets systematically to prevent queue backup and alert fatigue.

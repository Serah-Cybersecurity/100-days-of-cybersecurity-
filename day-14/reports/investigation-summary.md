# SOC Alert Investigation Summary

## 1. Case information

Case reference: DAY14-SOC-001

Environment: Synthetic SOC investigation

Analyst: Serah Mulwa (Tier 1 SOC Analyst)

Date: November 2, 2026

## 2. Executive summary

During this operational triage shift, a total of 3 security alerts were processed from the primary alert queue dataset (`alert-queue.jsonl`). Following rigorous Tier 1 triage methodology and cross-referencing with organizational context (`case-context.md`), 2 alerts (`SOC-2026-002` and `SOC-2026-003`) were validated against approved maintenance windows and classified as **Benign Positive**, leading to authorized closure. 

1 alert (`SOC-2026-001`) involved an unapproved external source IP executing sequential failed logins followed by a successful authentication and immediate privilege assignment. Due to evidence gaps regarding user identity validation and process execution, `SOC-2026-001` was classified as **Inconclusive** and formally escalated to Tier 2 Incident Response.

## 3. Scope

* **Ingested Telemetry:** `day-14/lab/data/alert-queue.jsonl` (SHA-256: `1fbf4499646a7428503e5ab7dc9bafd2e54ebe6648e74517522850e90dd075`)
* **Context Reference:** `day-14/lab/data/case-context.md`
* **Parsing Utilities:** Custom Python Queue Tool (`day-14/scripts/triage_queue.py`)
* **Target Systems:** `WIN-LAB-01`, `LINUX-LAB-01`
* **Target User Accounts:** `analyst`, `operator`, `backup-agent`

## 4. Investigation methodology

The investigation adhered to a standardized 9-Step Tier 1 SOC Triage Workflow:
1. **Queue Ingestion & Normalization:** Ingested JSONL alerts, parsed timestamps to UTC, and validated schema integrity using `triage_queue.py`.
2. **Priority Sorting:** Evaluated alerts based on operational severity (`High` $\rightarrow$ `Medium`).
3. **Temporal Correlation:** Reconstructed chronological sequences using event timestamps.
4. **Logon ID & Session Mapping:** Matched authentication event IDs with privilege modification logs.
5. **Baseline Verification:** Cross-referenced source IP addresses and accounts against the authorized inventory in `case-context.md`.
6. **Change Management Alignment:** Verified open Change Requests (`CHG-0142`, `CHG-0160`).
7. **Evidence Gap Identification:** Highlighted missing endpoint telemetry, process execution trees, and out-of-band identity confirmations.
8. **Verdict & Disposition Assignment:** Categorized alerts as True Positive, Benign Positive, False Positive, or Inconclusive.
9. **Formal Escalation & Reporting:** Generated individual case dossiers (`SOC-2026-001.md` through `SOC-2026-003.md`) and updated NIST SP 800-61 Rev. 3 escalation notes.

## 5. Alert summary

| Alert ID | Severity | Priority | Classification | Disposition |
|---|---|---|---|---|
| SOC-2026-001 | High | High | Inconclusive | Escalated |
| SOC-2026-002 | Medium | Low/Medium | Benign Positive | Closed |
| SOC-2026-003 | Medium | Low | Benign Positive | Closed |

## 6. Principal findings

### Case SOC-2026-001 — Repeated Failed Logons Followed by Successful Logon
* **System:** `WIN-LAB-01` | **Account:** `analyst` | **Source IP:** `198.51.100.27`
* **Evidence Reviewed:** Ingested sequence showing 3 failed logons (08:00–08:02) followed by a successful logon (08:04) and privilege escalation (08:04:10). The logon event and privilege assignment shared a matching Logon ID.
* **Findings:** Source IP `198.51.100.27` is unapproved according to `case-context.md`. While the temporal sequence resembles Credential Access (MITRE ATT&CK T1110), available telemetry does not confirm whether this was an authorized user mistyping a password or an external brute-force attack.

### Case SOC-2026-002 — Failed SSH Authentication
* **System:** `LINUX-LAB-01` | **Account:** `operator` | **Source IP:** `192.0.2.44`
* **Evidence Reviewed:** Single failed SSH authentication followed by successful logon.
* **Findings:** Source IP `192.0.2.44` is explicitly approved as an administrative host in `case-context.md`. Furthermore, activity correlates with approved maintenance ticket `CHG-0142`. The detection rule triggered accurately on real authentication events, but the context proves the action was authorized.

### Case SOC-2026-003 — New Service Started
* **System:** `WIN-LAB-01` | **Service:** `backup-agent`
* **Evidence Reviewed:** Windows service `backup-agent` initiated at 08:30.
* **Findings:** Baseline context lists `backup-agent` as an expected daily background task starting at ~08:30 under authorized change ticket `CHG-0160`. The alert fired correctly on a service state change, but the activity is legitimate.

## 7. Escalation

Alert **`SOC-2026-001`** was escalated to Tier 2 / Incident Response for the following reasons:
1. **Baseline Violation:** Source IP `198.51.100.27` is outside approved administrative subnets.
2. **Elevated Risk Pattern:** Sequential authentication failures immediately preceding successful authentication and privilege escalation.
3. **Asset Criticality:** Target host `WIN-LAB-01` hosts sensitive analyst operations.
4. **Analyst Operational Limits:** L1 analysts must not execute disruptive containment (e.g., host isolation or account disablement) without Tier 2 confirmation and out-of-band user verification.

## 8. Evidence limitations

* **Missing Endpoint Telemetry:** EDR process creation trees (e.g., Sysmon Event ID 1) were unavailable to inspect post-logon command execution for `SOC-2026-001`.
* **Missing PCAP / Network Data:** Full packet capture was not provided to analyze payload data from `198.51.100.27`.
* **Unconfirmed Identity:** Out-of-band contact with the `analyst` account owner has not yet been established.

## 9. Recommendations

1. **Immediate Tier 2 Action:** Perform out-of-band verification with account owner (`analyst`) to confirm if login from `198.51.100.27` was legitimate.
2. **EDR Investigation:** Query endpoint EDR on `WIN-LAB-01` for any sub-processes spawned under the active Logon ID created at 08:04.
3. **SIEM Rule Tuning:** Update detection logic for `SOC-2026-002` and `SOC-2026-003` to automatically suppress alerts matching approved Change Requests (`CHG-0142`, `CHG-0160`) to reduce alert fatigue.

## 10. Conclusion

The Day 14 SOC Alert Triage exercise successfully demonstrated end-to-end alert processing, baseline validation, and evidence-based decision making. Out of 3 alerts, 2 were validated as authorized maintenance (**Benign Positive**) and safely closed, while 1 high-risk anomaly (**Inconclusive**) was formally escalated with a comprehensive chain-of-custody log.

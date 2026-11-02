# SOC ENTERPRISE TRIAGE BATCH REPORT

**Generated:** 2026-11-02 14:03:02 UTC  
**Analyst:** Serah Mulwa (Tier 1 SOC Analyst)  
**System:** Enterprise Automated Triage & Investigation Engine  

---

## Executive Summary

This report documents the automated evaluation, risk prioritization, evidence validation, and operational dispositions for three alerts (Alert A, Alert B, and Alert C) processed in the enterprise master queue.

---

## Case 1: Alert A — Potential Unauthorized Account Access (`ALT-2026-9001`)

* **Target Host:** `DC-01.corp.local` (Criticality: **CRITICAL**)
* **Source IP:** `198.51.100.45`
* **Calculated Priority:** **P1 - CRITICAL ESCALATION** (Risk Score: `95`)
* **Forensic Evidence:** 3x failed Windows logins (Event 4625), 1x successful logon (Event 4624), 1x privilege grant (Event 4672).
* **External Context:** Change Request: None | Threat Intel: Unknown / Suspicious External IP
* **Final Verdict:** **TRUE POSITIVE (TP)**
* **Investigative Rationale:** Unapproved external IP performed brute-force attempts followed by a successful administrative logon. Immediate containment required.
* **Recommended Next Actions:**
  1. Immediately isolate `DC-01.corp.local` from outbound communications.
  2. Block IP `198.51.100.45` at the edge firewall.
  3. Escalate ticket to Tier 2 Incident Response for credential rotation and memory acquisition.

---

## Case 2: Alert B — Failed SSH Authentication Followed by Success (`ALT-2026-9002`)

* **Target Host:** `PAYMENT-GATEWAY-01` (Criticality: **HIGH**)
* **Source IP:** `10.0.50.12`
* **Calculated Priority:** **P2 - HIGH URGENCY** (Risk Score: `60`)
* **Forensic Evidence:** 1x failed SSH attempt followed by success from internal subnet admin host.
* **External Context:** Change Request: `CHG-2026-4401` (Scheduled Maintenance) | Threat Intel: Internal Approved Administrative Subnet
* **Final Verdict:** **BENIGN POSITIVE (BP)**
* **Investigative Rationale:** Activity matched SSH detection rule, but source IP is an approved internal administrative host backed by valid Change Request `CHG-2026-4401`.
* **Recommended Next Actions:**
  1. Verify maintenance window schedule in ServiceNow.
  2. Close ticket as Benign Positive (BP).

---

## Case 3: Alert C — New Backup Service Started (`ALT-2026-9003`)

* **Target Host:** `FILE-SRV-02` (Criticality: **MEDIUM**)
* **Source IP:** `127.0.0.1`
* **Calculated Priority:** **P4 - LOW PRIORITY** (Risk Score: `35`)
* **Forensic Evidence:** Windows Service Control Manager started `EnterpriseBackupSvc` successfully.
* **External Context:** Change Request: `CHG-2026-4399` (Automated Weekly Backup) | Threat Intel: Known Scheduled System Task
* **Final Verdict:** **FALSE POSITIVE / BENIGN (BP)**
* **Investigative Rationale:** Service startup rule triggered correctly, but activity matches expected automated weekly backup task `CHG-2026-4399`.
* **Recommended Next Actions:**
  1. Close ticket under Benign Positive baseline.
  2. Recommend signature threshold adjustment to reduce alert noise during scheduled backup windows.

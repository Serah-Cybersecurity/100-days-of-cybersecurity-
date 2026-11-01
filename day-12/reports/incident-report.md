# Incident Investigation & Event Log Triage Report - Day 12

* **Author / Analyst:** Serah Mulwa  
* **Date of Investigation:** October 31, 2026  
* **Environment Target:** Windows Local Host Endpoint (`MY-BABY`)  
* **Investigation Scope:** Read-Only Windows Event Log Triage (Security & System Channels)  

---

## 1. Lab Scope & Environment
This investigation was performed under strict **read-only forensic discipline** to preserve endpoint integrity and prevent evidence contamination. No audit policies were modified, no system configurations were altered, and no event logs were cleared or deleted. 

The objective was to evaluate local Windows Security Event logs (`.evtx`) using PowerShell (`Get-WinEvent`) and Event Viewer (`eventvwr.msc`), testing our ability to extract and interpret authentication sessions, process creations, and potential audit log tampering indicators.

---

## 2. Logon Triage Findings (Event IDs 4624 & 4625)
* **Query Execution:** Filtered the Windows **Security** log channel for Event ID `4624` (Successful Logon) and `4625` (Failed Logon) across a 7-day retrospective time window (`$since = (Get-Date).AddDays(-7)`).
* **Access Control & Results:** The query executed successfully without permission restrictions, returning numerous authentications and session records.
* **Observed Logon Types & Records:** 
  * Isolated a recent successful logon event (**Record ID: `3313598`**, timestamp: `10/31/2026 12:11:47 PM`).
  * **Logon Type Identified:** **Logon Type 5 (Service Logon)**. 
  * **Account Context:** Authenticated under `SYSTEM` (`NT AUTHORITY\SYSTEM`), initiated by background service control manager activity (`Advapi`).
  * **Correlation:** Verified that the `TargetLogonId` (`0x3E7`) correctly mapped across the session lifecycle, confirming legitimate system-level service authentication.

---

## 3. Process Creation Analysis (Event ID 4688)
* **Query Execution:** Queried the Security log for Event ID `4688` (A New Process Was Created) across the past 7 days.
* **Findings:** Successfully retrieved multiple process creation audit records (e.g., **Record IDs `3313969` through `3313978`**).
* **Analytical Observations:** 
  * Process creation auditing was active on the host, confirming that executable invocation telemetry was successfully logged by the Security auditing subsystem.
  * *Limitation Noted:* In accordance with default unhardened local audit policies, raw command-line argument auditing was not globally enabled, reinforcing the principle that an analyst must document existing baseline configurations rather than altering system settings during triage.

---

## 4. Audit Tampering Check (Event ID 1102)
* **Query Execution:** Queried the Security log for Event ID `1102` (The Windows Security Audit Log was cleared) across a 30-day lookback window.
* **Findings:** The query returned **no matching events** (`No events were found that match the specified selection criteria`).
* **Forensic Interpretation:** On a clean, personal development endpoint, an empty result for Event ID 1102 is the expected baseline. In an enterprise SOC environment, an Event ID 1102 record represents a high-severity alert indicating potential defense evasion (an adversary attempting to wipe forensic tracks via `wevtutil cl Security`). Here, no evidence of audit log tampering was detected.

---

## 5. Key Forensic Principles & Takeaways
* **Read-Only Discipline:** Maintaining strict read-only parameters ensures that investigative actions never alter file system metadata, event timestamps, or registry keys on a compromised host.
* **Absence of Evidence $\neq$ Evidence of Absence:** The lack of process command-line arguments or 1102 log-clearing events does not prove that activity never occurred; it reflects the active Group Policy audit configuration of the endpoint. Always verify audit policies before drawing final conclusions.

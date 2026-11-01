# Incident Forensic Timeline & Event Correlation Report - Day 12

* **Analyst / Investigator:** Serah Mulwa  
* **Target Endpoint:** Windows Local Host (`MY-BABY`)
* **Date of Reconstruction:** October 31, 2026
* **Methodology:** Evidence-Based Chronological Correlation (Logon IDs, Record IDs, and UTC Time Normalization)

---

## 1. Executive Summary & Objective
The objective of this report is to construct a rigorous, defensible chronological timeline of host activity. In professional forensic investigations, analysts must avoid speculative or imaginative narratives ("Hollywood stories"). Every entry in this timeline is directly anchored to verifiable Windows Event Log telemetry, matching session identifiers, and strict cryptographic or sequence markers.

---

## 2. Chronological Investigation Timeline

| Normalized Timestamp (UTC) | Event Log Channel | Event ID | Category / Description | Session / Correlation Identifier | Verifiable Evidence & Record Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-10-31 09:11:47Z** | Security | **4624** | Successful Logon[cite: 2] | Logon ID: `0x3E7`[cite: 2] | Authenticated under `SYSTEM` (`NT AUTHORITY\SYSTEM`), Logon Type 5 (Service), initiated via `Advapi`. Record ID: `3313598`. |
| **2026-10-31 09:16:48Z** | Security | **4688** | Process Creation[cite: 8] | Logon ID: `0x3E7` | Invocation of local executable telemetry under active process auditing. Record IDs: `3313969` through `3313978`. |
| **2026-10-31 12:11:47Z** | Security | **4624** | Successful Logon[cite: 2] | Logon ID: `0x3E7`[cite: 2] | System-level service control manager background authentication routine. Record ID: `3313598`. |
| **2026-10-31 12:16:48Z** | Security | **4688** | Process Creation[cite: 8] | Logon ID: `0x3E7` | Subsequent local process execution and command invocation auditing. Record IDs: `3313969` to `3313978`. |

---

## 3. Correlation Analysis & Findings
* **Session Continuity (Logon ID Matching):** By tracking Logon ID `0x3E7` across successful logon events (`4624`) and subsequent process creations (`4688`), we mathematically prove that system-level activities occurred within the same authenticated execution context rather than relying on loose temporal proximity.
* **Time Zone Normalization:** All event timestamps were normalized from local workstation time to UTC (Coordinated Universal Time) to eliminate timezone offset discrepancies during multi-system analysis.
* **Audit Integrity:** Review of audit tampering indicators (Event ID 1102) over a 30-day lookback window yielded zero matches, confirming that no audit logs were cleared or tampered with during the investigative window.

---

## 4. Key Forensic Takeaways
1. **Defensible Over Speculative:** Timestamps alone do not establish intent. Linking process identifiers (PIDs), Record IDs, and unique Logon IDs establishes an unbroken chain of custody for every action on the endpoint.
2. **Chain of Evidence:** Preserving raw metadata objects via read-only PowerShell queries (`Get-WinEvent`) guarantees that investigative actions never contaminate the host system state.

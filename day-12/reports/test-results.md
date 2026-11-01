# Script Test Execution & Validation Report - Day 12

* **Script Tested:** `Get-Day12EventSummary.ps1`
* **Test Environment:** Windows Local Host Endpoint (`MY-BABY`)
* **Tester / Analyst:** Serah Mulwa
* **Date of Execution:** October 31, 2026

---

## 1. Execution Parameters & Scope
The automated PowerShell event log summary tool was executed against local Windows event channels using the following default parameters:
* **`-HoursBack`:** `24` hours (filtering event records generated within the past day).
* **`-MaxEventsPerLog`:** `100` maximum events per query channel limit.
* **Target Channels:** `System`, `Application`, and `Security` (targeting Event IDs `4624`, `4625`, `4672`, `4688`, and `1102`).

---

## 2. Test Execution & Collection Summary
* **Total Records Collected:** `300` events successfully harvested across all queried channels.
* **Error & Exception Handling:** All query blocks executed successfully to completion. No unhandled exceptions or access-denied warning messages were encountered during local log traversal.
* **Output Artifact Generation:** The collected metadata was successfully compiled, sorted by timestamp, and exported locally to the `.gitignore`-protected directory:
  `C:\WINDOWS\system32\day-12\private-output\event-metadata.csv`

---

## 3. Group-Object Breakdown & Analysis
The script grouped collected events by log channel and Event ID, returning the following primary operational telemetry:

* **Top Event Categories Observed:**
  * **Security Log, Event ID 4688 (Process Creation):** `100` records (reflecting active process invocation auditing on the host endpoint).
  * **Application Log, Event ID 4 (Information/Operation):** `36` records
  * **Application Log, Event ID 0:** `17` records
  * **System Log, Event ID 112:** `16` records
  * **System Log, Event ID 10016 (DistributedCOM):** `11` records
  * *Various other operating system service states, time synchronizations, and application events ranging in counts from 1 to 7.*

---

## 4. Key Lessons & Security Principles
* **Privacy First:** By design, the script collects only structural metadata (Timestamps, Event IDs, Providers, Levels, and Record IDs) while deliberately omitting full message bodies. This guarantees that unredacted user credentials, private paths, or internal identifiers are never exported or accidentally leaked into version control.
* **Error Resilience:** Wrapping query blocks in robust `try/catch` logic ensures that even if a specific log channel throws a permission restriction or missing data error, the script gracefully logs a warning and continues executing rather than failing catastrophically mid-collection.

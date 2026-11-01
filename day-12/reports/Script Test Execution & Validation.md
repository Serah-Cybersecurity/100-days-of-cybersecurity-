# Script Test Execution & Validation Report - Day 12

* **Script Tested:** `Get-Day12EventSummary.ps1`
* **Test Environment:** Windows Local Host Endpoint (`MY-BABY`)
* **Tester / Analyst:** Serah Mulwa
* **Date of Execution:** October 31, 2026

---

## 1. Execution Parameters & Scope
The automated PowerShell event log summary tool was executed against local Windows event channels using default and custom parameters to validate operational behavior, error handling, and artifact generation.

---

## 2. Formal Testing Questions & Answers

1. **Did the script execute?**  
   - *Answer:* Yes, the script executed successfully and completed all query iterations across System, Application, and Security logs.

2. **Which logs were accessible?**  
   - *Answer:* System, Application, and Security logs were fully accessible on the local host.

3. **Which queries returned records?**  
   - *Answer:* All three log channels successfully returned active event telemetry (totaling 300 records in our default baseline test, and 150 records under the custom 48-hour capped test).

4. **Were any queries unavailable or restricted?**  
   - *Answer:* None; local administrator context permitted read access across all target channels.

5. **How many records were collected?**  
   - *Answer:* Exactly 300 records were collected under the 24-hour default parameter window (`-HoursBack 24`, `-MaxEventsPerLog 100`).

6. **What changed when you used a different time range?**  
   - *Answer:* Expanding `-HoursBack` to 48 and adjusting `-MaxEventsPerLog` to 50 broadened the retrospective collection window, altering total record yields and capturing older historical telemetry.

7. **Did the script modify any event logs or system configuration?**  
   - *Answer:* No. The script operated under strict read-only parameters (`Get-WinEvent`), leaving all event logs, registry keys, and audit policies completely untouched.

8. **What information does the script deliberately exclude?**  
   - *Answer:* Full raw event message bodies (protecting against leaking sensitive user accounts, internal file paths, and IP addresses into public version control).

9. **What would need to change before the script could support a more complete investigation?**  
   - *Answer:* It would require remote endpoint targeting (WinRM / CIM sessions), dynamic log parsing for structured XML event data fields, and multi-threaded execution capabilities to scale across enterprise networks.

---

## 3. Artifact Verification & Pipeline Analysis
* **CSV Report Generation:** Successfully verified that the inventory output was compiled and exported to:
  `C:\WINDOWS\system32\day-12\private-output\event-metadata.csv`
* **Independent Pipeline Verification:** Successfully re-imported the CSV artifact into PowerShell (`Import-Csv`) and re-grouped records using `Group-Object LogName, EventId` to independently validate data integrity without relying solely on the script's internal output block.

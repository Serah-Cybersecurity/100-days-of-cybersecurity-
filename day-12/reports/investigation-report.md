# Windows Event Log Investigation Report

## 1. Investigation Metadata
* **Project:** Day 12 Windows Event Log Investigation
* **Environment:** Personal Windows learning environment (`MY-BABY`)
* **Investigation Type:** Read-only event-log review
* **Date:** October 31, 2026

## 2. Objective
The objective of this investigation was to perform a read-only baseline event log triage across target Windows event log channels (`System`, `Application`, `Security`), evaluate security Event IDs for anomalous patterns, test custom PowerShell automation scripts, and build a defensible forensic event timeline.

## 3. Scope
The scope was limited to the local Windows host endpoint (`MY-BABY`). 
* **Logs Examined:** `System`, `Application`, and `Security` log channels.
* **Accessibility State:** All three queried logs were fully accessible under local administrator execution context.

## 4. Tools
* **Windows Event Viewer (`eventvwr.msc`):** GUI tool used for inspecting XML event schemas
* **Windows PowerShell:** Command-line framework used for pipeline query execution.
* **`Get-WinEvent`:** Primary cmdlet used for high-performance hashtable filtering.
* **Custom PowerShell Script (`Get-Day12EventSummary.ps1`):** Automated tool created to harvest metadata and generate CSV reports.

## 5. Methodology
1. Executed interactive PowerShell queries using `Get-WinEvent` with `-FilterHashtable` targeting default 24-hour lookback windows (`-HoursBack 24`).
2. Executed custom triage script (`Get-Day12EventSummary.ps1`) to extract structural metadata (`LogName`, `TimeCreated`, `EventId`, `Provider`, `Level`, `RecordId`) into `[PSCustomObject]` arrays.
3. Validated script resilience using custom parameters (`-HoursBack 48`, `-MaxEventsPerLog 50`).
4. Exported structured data to `.gitignore`-protected local storage (`day-12/private-output/event-metadata.csv`).
5. Analyzed exported CSV data independently using `Import-Csv` and `Group-Object LogName, EventId` pipeline sorting.

## 6. Observations
* **Total Collected Records:** 300 event records were harvested during default baseline collection.
* **Log Channel Yields:**
  * `Security Log`: Returned 100 process creation records (Event ID 4688).
  * `Application Log`: Returned 36 records of Event ID 4, 17 records of Event ID 0, and various application operational events.
  * `System Log`: Returned 16 records of Event ID 112, 11 records of Event ID 10016 (DistributedCOM), and standard driver state events.
* **Security Audit State:** Zero log clear events (Event ID 1102) and zero failed authentication cascades (Event ID 4625) were recorded.

## 7. Event Analysis
The queried Security log contained several process creation records (Event ID 4688) and successful service logon events (Event ID 4624) associated with system background tasks (`NT AUTHORITY\SYSTEM`). Their significance cannot be established from the available records alone; further review of process command-line arguments, parent process lineages, and network socket activity would be required before inferring operational intent.

## 8. Limitations
* **Permissions Limitations:** Queries were bounded by local host administrator rights.
* **Missing Audit Events:** Detailed process command-line arguments (Event ID 4688 `CommandLine`) were not populated due to local Group Policy configuration.
* **Time-Range Restrictions:** Initial collection was capped at a 24-hour lookback window.
* **Incomplete Logging Information:** Data collection was capped at 100 events per log channel (`-MaxEventsPerLog 100`).
* **Information Deliberately Excluded:** Full event message strings were excluded from export to prevent leaking sensitive local account names or path telemetry into version control.

## 9. Conclusion
The investigation successfully established that local `System`, `Application`, and `Security` log channels are actively recording expected system operational telemetry. No indicators of audit log tampering (Event ID 1102) were observed. The full extent of historical endpoint process lineage remains unverified due to parameter capping and local auditing configuration limits.

## 10. Recommendations
1. Enable Command-Line Process Auditing via Local Group Policy (`Include command line in process creation events`) to capture full `CommandLine` payloads for Event ID 4688.
2. Configure Windows Event Forwarding (WEF) to ship local log telemetry to a centralized SIEM platform.
3. Incorporate Event ID 7045 (Service Installation) into future automated monitoring script runs.

## 11. References
* [Microsoft Learn: Get-WinEvent Cmdlet Documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent)
* [Microsoft Security Auditing Reference Guide](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/security-auditing-overview)

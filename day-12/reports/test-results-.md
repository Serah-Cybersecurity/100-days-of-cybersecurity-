# Day 12 PowerShell Script Test Report

## Environment
* **Windows version:** Windows 11 Enterprise / Professional (Build 26100 / Local Host `MY-BABY`)
* **PowerShell version:** PowerShell 5.1 / 7+ Administrative Host
* **Date:** October 31, 2026
* **User permissions:** Local Administrator Context

## Test 1 — Script execution
* **Command:** 
  & .\day-12\scripts\Get-Day12EventSummary.ps1
* **Expected result:** The script executes and performs its read-only queries across target channels.
* **Actual result:** Successfully initialized, iterated through System, Application, and Security logs, and printed summary metrics.
* **Status:** Pass

## Test 2 — System log
* **Expected result:** The script retrieves available System event metadata.
* **Actual result:** Successfully harvested System log events (including Event IDs 112, 10016, and kernel-general events) without errors.

## Test 3 — Application log
* **Expected result:** The script retrieves available Application event metadata.
* **Actual result:** Successfully queried Application log channels, returning Event IDs 4, 0, and auxiliary application operational telemetry.

## Test 4 — Security log
* **Expected result:** The script attempts to retrieve selected event IDs (`4624`, `4625`, `4672`, `4688`, `1102`).
* **Actual result:** Successfully queried target Security Event IDs under local administrator context, harvesting 100 process creation records (Event ID 4688) without encountering access permission blocks.

## Test 5 — Time range
* **Command:** 
  & .\day-12\scripts\Get-Day12EventSummary.ps1 -HoursBack 48 -MaxEventsPerLog 50
* **Actual result:** Broadening the lookback window to 48 hours and capping max events at 50 per channel successfully altered the total record count down to 150 events, demonstrating dynamic parameter scaling.

## Test 6 — Private output handling
* **Expected result:** CSV output is written to the local private-output directory and excluded from git version control.
* **Actual result:** Successfully compiled and exported event metadata to `C:\WINDOWS\system32\day-12\private-output\event-metadata.csv`, with `.gitignore` properly protecting the folder.

## Limitations
* Queries were restricted to local host endpoints and bounded by local administrator read permissions.
* Process command-line auditing was limited by default operating system Group Policy settings.
* Collection was capped by `-MaxEventsPerLog` thresholds, representing a statistical event sample rather than a complete forensic image dump.

## Conclusion
The custom PowerShell event summary tool (`Get-Day12EventSummary.ps1`) behaved exactly as expected during testing. It successfully executed read-only queries, handled parameters dynamically, and exported clean metadata reports without modifying underlying system logs or configurations.

# Day 12 - Windows Event Logging, PowerShell Triage & Event Correlation

## Overview
Day 12 focuses on Windows Event Log architecture, Security Event ID analysis, automated triage scripting with PowerShell (`Get-Day12EventSummary.ps1`), and defensible incident timeline correlation.

## Directory Structure
* **`notes/`**: Comprehensive notes covering EVTX architecture, core Event IDs, PowerShell `-FilterHashtable` syntax, triage methodology, and time correlation.
* **`scripts/`**: Custom PowerShell event summary tool (`Get-Day12EventSummary.ps1`).
* **`reports/`**: Script test execution results, forensic incident timeline, and full investigation report.
* **`screenshots/`**: Visual evidence of terminal commands, Event Viewer XML analysis, and script output.
* **`private-output/`**: Local CSV exports (excluded via `.gitignore`).

## Key Artifacts & Tools
* **Script:** `scripts/Get-Day12EventSummary.ps1`
* **Test Report:** `reports/test-results.md`
* **Incident Timeline:** `reports/incident-timeline.md`

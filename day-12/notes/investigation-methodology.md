# Forensic Investigation Methodology & Evidence Handling - Day 12

## Triage Playbook
1. **Preserve Volatile State:** Use read-only queries (`Get-WinEvent`) to collect structured metadata without modifying endpoint configuration or logs.
2. **Establish Investigation Window:** Define lookback parameters (`-HoursBack`) to focus scope and prevent system resource exhaustion.
3. **Correlate Identifiers:** Link authentication (`4624`) and privilege assignments (`4672`) using unique `LogonId` values rather than relying solely on timestamps.
4. **Export Clean Artifacts:** Store metadata in structured formats (CSV/JSON) in non-tracked, protected output directories (`private-output/`).

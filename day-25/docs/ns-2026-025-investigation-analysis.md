# Case NS-2026-025 — Investigation Analysis (Section 7)

## 7.1 Chronological Sequence & Context Needed
- `09:00:00Z` (`4624`, `0x4A1`, `analyst01`, Logon Type 2): First successful interactive logon. Need source/authentication details, workstation context, and expected baseline for `analyst01`.
- `09:02:00Z` (`4625`, `logon_id: null`, `source_ip: 192.0.2.44`, Logon Type 2): Failed interactive logon. Need failure sub-status/reason, network context for documentation IP `192.0.2.44`, and surrounding attempt history.
- `09:03:00Z` (`4624`, `0x4A2`, `analyst01`, Logon Type 2): Second successful interactive logon under a new logon ID (`0x4A2`). Need authentication method and baseline for concurrent/second interactive session.
- `09:04:00Z` (`4688`, `0x4A2`, `C:\Windows\System32\notepad.exe`, `process_guid: null`): Process creation audited. Need parent process details, command line, and why `process_guid` is `null` in this record.
- `09:04:01Z` (`Sysmon 1`, `0x4A2`, `notepad.exe`, `process_guid: {TRAINING-PROC-001}`, `parent_process_guid: {TRAINING-PROC-000}`): Sysmon process creation. Need command line, file hash, integrity level, and parent `{TRAINING-PROC-000}` identity.
- `09:06:00Z` (`Sysmon 3`, `0x4A2`, `notepad.exe`, `{TRAINING-PROC-001}`, `source_ip: 203.0.113.20`): Network connection recorded. Need port, protocol, direction/endpoint roles, proxy/network logs, and baseline for `notepad.exe`.
- `09:10:00Z` (`4634`, `0x4A1`, `analyst01`): Logon session `0x4A1` ended while `0x4A2` remained active. Need logoff reason and activity context.
- `09:12:00Z` (`4672`, `0x4A2`, `analyst01`): Special privileges assigned to logon `0x4A2`. Need specific privilege list and authorization/elevation context.
- `09:15:00Z` (`Sysmon 5`, `0x4A2`, `notepad.exe`, `{TRAINING-PROC-001}`): Process terminated. Need exit code/status and full runtime context.

## 7.2–7.5 Key Analytical Takeaways
- **Separate Sessions:** `0x4A1` (`09:00:00Z`–`09:10:00Z`) and `0x4A2` (`09:03:00Z` onward) are distinct sessions; do not merge them or assume `4625` at `09:02:00Z` caused `4624` at `09:03:00Z`.
- **Process Instance Tracking:** `{TRAINING-PROC-001}` links Sysmon `1` (`09:04:01Z`), Sysmon `3` (`09:06:00Z`), and Sysmon `5` (`09:15:00Z`) for `notepad.exe` without PID-reuse ambiguity, while `4688` (`09:04:00Z`) has `process_guid: null` in this synthetic dataset.
- **No Premature Verdict:** Neither compromise nor benign activity is proven from these 9 synthetic records alone; see `reports/day25/evidence-register.csv` (`E-001`–`E-009`) for exact confidence ratings and limitations.

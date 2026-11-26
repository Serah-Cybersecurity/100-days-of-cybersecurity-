# Case NS-2026-025 — Final Investigation & Endpoint Incident Analysis (Section 8)

- **Investigation Case:** NS-2026-025 (Fictional training dataset — not a real incident)
- **Host:** NS-WKS-014
- **Account:** analyst01
- **Investigation Window:** 2026-11-26 09:00–09:30 UTC
- **Primary Sources:** `data/training/day25_endpoint_events.jsonl`, `reports/day25/day25_timeline.csv`, `reports/day25/evidence-register.csv`

---

## 1. Executive Summary
The nine normalized synthetic records in Case `NS-2026-025` show two separate interactive logon sessions (`0x4A1` and `0x4A2`) for `analyst01` on `NS-WKS-014`, one failed interactive logon (`4625` at `09:02:00Z` with `source_ip: 192.0.2.44`), `notepad.exe` creation, network, and termination telemetry (`{TRAINING-PROC-001}`) under `0x4A2`, a `0x4A1` session-end event (`4634` at `09:10:00Z`), and a special-privileges event (`4672` at `09:12:00Z`) under `0x4A2`. Based strictly on the supplied records, the evidence **does not establish unauthorized access** and **does not prove a single unbroken malicious chain** across the window. Further authorized investigation and baseline/telemetry context are required before reaching a definitive security conclusion.

---

## 2. Sequence of Events (UTC)
Chronological order from `reports/day25/day25_timeline.csv` (`09:00:00Z` to `09:15:00Z`):

1. **2026-11-26T09:00:00Z** | `Security` | `4624` | `account: analyst01`, `logon_id: 0x4A1`, `logon_type: 2`, `source_ip: null`, `process_name: null`, `process_guid: null`, `parent_process_guid: null` — Successful interactive logon (`E-001`).
2. **2026-11-26T09:02:00Z** | `Security` | `4625` | `account: analyst01`, `logon_id: null`, `logon_type: 2`, `source_ip: 192.0.2.44`, `process_name: null`, `process_guid: null`, `parent_process_guid: null` — Failed interactive logon (`E-002`).
3. **2026-11-26T09:03:00Z** | `Security` | `4624` | `account: analyst01`, `logon_id: 0x4A2`, `logon_type: 2`, `source_ip: null`, `process_name: null`, `process_guid: null`, `parent_process_guid: null` — Second successful interactive logon (`E-003`).
4. **2026-11-26T09:04:00Z** | `Security` | `4688` | `account: analyst01`, `logon_id: 0x4A2`, `logon_type: null`, `source_ip: null`, `process_name: C:\Windows\System32\notepad.exe`, `process_guid: null`, `parent_process_guid: null` — Process creation recorded (`E-004`).
5. **2026-11-26T09:04:01Z** | `Sysmon` | `1` | `account: analyst01`, `logon_id: 0x4A2`, `logon_type: null`, `source_ip: null`, `process_name: C:\Windows\System32\notepad.exe`, `process_guid: {TRAINING-PROC-001}`, `parent_process_guid: {TRAINING-PROC-000}` — Process creation with parent process information (`E-005`).
6. **2026-11-26T09:06:00Z** | `Sysmon` | `3` | `account: analyst01`, `logon_id: 0x4A2`, `logon_type: null`, `source_ip: 203.0.113.20`, `process_name: C:\Windows\System32\notepad.exe`, `process_guid: {TRAINING-PROC-001}`, `parent_process_guid: null` — Network connection recorded for the process (`E-006`).
7. **2026-11-26T09:10:00Z** | `Security` | `4634` | `account: analyst01`, `logon_id: 0x4A1`, `logon_type: null`, `source_ip: null`, `process_name: null`, `process_guid: null`, `parent_process_guid: null` — Logon session ended (`E-007`).
8. **2026-11-26T09:12:00Z** | `Security` | `4672` | `account: analyst01`, `logon_id: 0x4A2`, `logon_type: null`, `source_ip: null`, `process_name: null`, `process_guid: null`, `parent_process_guid: null` — Special privileges assigned to a new logon (`E-008`).
9. **2026-11-26T09:15:00Z** | `Sysmon` | `5` | `account: analyst01`, `logon_id: 0x4A2`, `logon_type: null`, `source_ip: null`, `process_name: C:\Windows\System32\notepad.exe`, `process_guid: {TRAINING-PROC-001}`, `parent_process_guid: null` — Process termination recorded (`E-009`).

---

## 3. Two Successful Logon Sessions & Their Identifiers
There are two Event ID `4624` records, both showing `account: analyst01`, `logon_type: 2` (interactive logon), and `source_ip: null`, but carrying **different** logon session identifiers:
- **Session `0x4A1`:** Begins at `2026-11-26T09:00:00Z` (`4624`) and ends at `2026-11-26T09:10:00Z` (`4634`). It does not appear on the `notepad.exe` process/network events, `4672`, or `Sysmon 5`.
- **Session `0x4A2`:** Begins at `2026-11-26T09:03:00Z` (`4624`)—while `0x4A1` is still open—and appears on `4688` (`09:04:00Z`), `Sysmon 1` (`09:04:01Z`), `Sysmon 3` (`09:06:00Z`), `4672` (`09:12:00Z`), and `Sysmon 5` (`09:15:00Z`).

Having distinct logon IDs means `0x4A1` and `0x4A2` represent separate logon sessions rather than one single session.

---

## 4. Failed Logon Analysis
At `2026-11-26T09:02:00Z`, Event ID `4625` records a failed interactive logon (`logon_type: 2`) for `analyst01` with `logon_id: null` and `source_ip: 192.0.2.44`.
- An unsuccessful authentication attempt (`4625`) shows a failure outcome, not confirmed unauthorized access or compromise.
- Its placement one minute before the `09:03:00Z` `4624` (`0x4A2`) event on the same host and account does not by itself prove that the same actor performed both actions or that the failed logon caused the `0x4A2` logon.

---

## 5. Process Correlation Analysis
- **Linked Telemetry:** `Sysmon 1` (`09:04:01Z`), `Sysmon 3` (`09:06:00Z`), and `Sysmon 5` (`09:15:00Z`) all share `process_guid: {TRAINING-PROC-001}`, `process_name: C:\Windows\System32\notepad.exe`, `account: analyst01`, and `logon_id: 0x4A2`, linking the creation, network event, and termination of that tracked Sysmon process instance. `4688` (`09:04:00Z`) also references `C:\Windows\System32\notepad.exe` under `analyst01` and `logon_id: 0x4A2` one second before `Sysmon 1`.
- **Unestablished Details:** `4688` has `process_guid: null` in this synthetic record, and full command lines, parent process names/details (beyond `parent_process_guid: {TRAINING-PROC-000}`), and process IDs are not present in the dataset. Thus, correlation shows shared identifiers and sequence, not full causal or authorization context.

---

## 6. Network-Event Analysis
`Sysmon 3` at `2026-11-26T09:06:00Z` records network activity associated with `C:\Windows\System32\notepad.exe`, `process_guid: {TRAINING-PROC-001}`, `logon_id: 0x4A2`, `account: analyst01`, and `source_ip: 203.0.113.20`.
- A recorded network event is not automatically malicious; legitimate applications, administrative tools, or test/benign activity can generate network events.
- Because the schema lacks destination port, protocol, direction/field semantics, host/user baseline data, and full Sysmon filter configuration, this record alone cannot determine whether the connection was expected or malicious.

---

## 7. Limitations of the Dataset
1. **Synthetic Training Schema & Fictional/Documentation Values:** The dataset contains 9 simplified records with fictional timestamps, synthetic GUIDs (`{TRAINING-PROC-000}`, `{TRAINING-PROC-001}`), and RFC 5737 documentation IP addresses (`192.0.2.44` and `203.0.113.20`), not full native Windows Security or Sysmon logs.
2. **Missing or Null Contextual Fields:** Key investigative fields are absent or `null`, including failure sub-status/reason codes on `4625`, `process_guid` on `4688`, full command lines, parent process names, and network port/protocol/direction fields.
3. **Lack of Baseline & Collection Coverage Context:** There is no historical baseline for `analyst01` or `NS-WKS-014`, no visibility before `09:00:00Z` or after `09:15:00Z` within the sample, and no audit policy or Sysmon configuration details showing what events or filters were active.

---

## 8. Assessment of Whether the Evidence Establishes Unauthorized Access
**No.** The supplied evidence does not establish unauthorized access. While there is a failed logon (`4625`), two separate successful interactive logons (`0x4A1` and `0x4A2`), `notepad.exe` process/network/termination events under `0x4A2`, and a `4672` special-privileges event at `09:12:00Z` under `0x4A2`, none of these records alone prove unauthorized access, malicious intent, or a direct causal link between the `09:02:00Z` failure and subsequent session activity.

---

## 9. Recommended Additional Evidence for Authorized IR Follow-Up
An authorized incident response team could review:
- Full native Windows Security (`4624`, `4625`, `4634`, `4672`, `4688`) and Sysmon Operational logs (including failure status codes, command lines, parent process details, hashes, and active Sysmon configuration).
- Identity/authentication and directory logs, plus logon history and work/change baselines for `analyst01` and `NS-WKS-014`.
- Endpoint/EDR telemetry and network/firewall/DNS/proxy logs covering `NS-WKS-014` and relevant addresses/ports around `2026-11-26 09:00–09:30 UTC`.

---

## 10. Final Disposition
**Inconclusive from supplied evidence — further investigation warranted.** The current records provide clear chronological observations and session/process groupings (`0x4A1` vs. `0x4A2` and `{TRAINING-PROC-001}`), but cannot confirm or rule out unauthorized access or malicious activity without additional telemetry and baseline context.

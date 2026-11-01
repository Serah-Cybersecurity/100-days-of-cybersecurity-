# Incident Triage Report

## 1. Report metadata
* **Case ID:** DAY11-SYNTHETIC-001
* **Environment:** Synthetic Linux server dataset (`labhost`)
* **Analyst:** Serah (Defensive Security Engineering Portfolio)
* **Date:** 29 October 2026
* **Report status:** Initial triage exercise

## 2. Executive summary
Initial log triage of the synthetic `labhost` dataset reveals a notable authentication anomaly: three consecutive failed login attempts followed by a successful authentication from source IP `198.51.100.27`, which is identified in the case context as an unapproved administrative source. While this pattern warrants review, available logs lack sufficient endpoint telemetry to establish whether the account was compromised or if the activity was unauthorized. Routine scheduled tasks and approved administrative sessions align with baseline expectations.

## 3. Scope
* **Files Examined:** `day-11/lab/data/events.jsonl`, `day-11/lab/data/case-context.md`
* **Event Types:** Authentication (`sshd`), privilege use (`sudo`), scheduled tasks (`systemd` timers and services).
* **Explicit Constraint:** The dataset evaluated is entirely synthetic. No production or live infrastructure was assessed or modified.

## 4. Evidence Examined
* **Log Dataset:** `day-11/lab/data/events.jsonl` (8 structured JSONL event records).
* **Analysis Tools:** Custom Python parser (`day-11/scripts/analyze_events.py`), core Linux utilities (`cat`, `wc`, `grep`).

## 5. Findings

### Finding 1: Authentication sequence
* **Observation:** Three failed login attempts (`admin`, `oracle`, `student`) were recorded from `198.51.100.27` between 09:12:03 and 09:12:15, followed by a successful password login for user `student` from the same IP at 09:13:22.
* **Interpretation:** The sequence of multiple failures followed by a success from an unapproved IP address matches potential credential probing patterns.
* **Confidence:** Directly supported by records 1 through 4 in `events.jsonl`.
* **Limitations:** Does not prove the attacker's physical location, user intent, or whether the credential entry was made by an authorized remote user typing incorrectly.
* **Recommended next step:** Conduct out-of-band user verification and inspect session logs.

### Finding 2: Privilege-use activity
* **Observation:** At 09:13:58, user `student` executed `sudo systemctl status cron` from source IP `198.51.100.27`.
* **Interpretation:** The command requests read-only service status information and is not intrinsically malicious, but its timing post-login requires contextual review.
* **Limitations:** Dataset lacks session linkage to prove authorization status.
* **Recommended next step:** Review sudo authorization configurations and user permission grants.

### Finding 3: Scheduled task
* **Observation:** `daily-report.timer` fired at 09:15:00 and `daily-report.service` started at 09:15:04.
* **Interpretation:** Matches the routine schedule defined in `case-context.md`. Temporal proximity to the login event does not establish causation.
* **Limitations:** Does not verify broader system configuration integrity beyond the scope of the log window.

## 6. Timeline

| Time (+03:00) | Event | Initial Interpretation |
| :--- | :--- | :--- |
| `09:12:03` | Failed authentication | An authentication failure was recorded |
| `09:12:08` | Failed authentication | A second failure came from the same source |
| `09:12:15` | Failed authentication | A third failure came from the same source |
| `09:13:22` | Successful authentication | A success from the same source warrants review |
| `09:13:58` | Privilege-use event | The recorded command and its authorisation need contextual review |
| `09:15:00` | Scheduled timer fired | Consistent with the supplied scheduling information |
| `09:15:04` | Service started | The event's timing matches the supplied expectation |
| `09:17:20` | Successful authentication | Consistent with the supplied approved-source information |

## 7. Overall assessment
The authentication sequence involving `198.51.100.27` merits further review due to unapproved source classification and failure-to-success correlation. Privilege-use commands require contextual validation but remain read-only. Scheduled timer and service activity match baseline expectations and should not be treated as malicious.

## 8. Recommended next steps
1. Perform out-of-band communication with user `student`.
2. Inspect endpoint shell history and detailed SSH daemon logs.
3. Enforce strict multi-factor authentication and IP whitelisting.

## 9. Limitations
This exercise relies on a small synthetic dataset. Findings highlight review workflows and do not establish whether a real-world system is compromised.

## 10. Conclusion
The available synthetic evidence warrants structured investigative review regarding authentication anomalies from unapproved IP sources, but does not, by itself, establish that `labhost` was compromised.

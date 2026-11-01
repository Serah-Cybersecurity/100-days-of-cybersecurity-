# Incident Triage Report: labhost Authentication Anomaly

**Date of Investigation:** October 30, 2026  
**Investigator:** Serah (Defensive Security Analyst)  
**Target Host:** `labhost`  
**Dataset Evaluated:** `day-11/lab/data/events.jsonl`  

---

## 1. Investigation Scope & Data Limitations

### Scope Boundaries
* **Target System:** Simulated Linux host (`labhost`).
* **Time Window Examined:** `2026-10-29 09:12:03+03:00` to `2026-10-29 09:17:20+03:00`.
* **Primary Evidence Source:** Local JSONL event log dataset (`events.jsonl`).

### Dataset Limitations & Data Gaps
* **Missing Artifacts:** The provided dataset does not contain full memory dumps, endpoint process execution trees, shell command histories (`.bash_history`), network packet captures (PCAPs), or Multi-Factor Authentication (MFA) logs.
* **Analytical Constraint:** Findings are strictly based on the synthetic dataset provided. No live or production enterprise assets were modified or evaluated.

---

## 2. Chronological Event Timeline

| Timestamp (+03:00) | Source Service | Event Type | User | Source IP | Result | Details / Command |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `09:12:03` | `sshd` | Authentication | `admin` | `198.51.100.27` | Failed | `invalid_user` |
| `09:12:08` | `sshd` | Authentication | `oracle` | `198.51.100.27` | Failed | `invalid_user` |
| `09:12:15` | `sshd` | Authentication | `student` | `198.51.100.27` | Failed | `incorrect_password` |
| `09:13:22` | `sshd` | Authentication | `student` | `198.51.100.27` | Success | Method: Password |
| `09:13:58` | `sudo` | Privilege Use | `student` | `198.51.100.27` | Success | `systemctl status cron` |
| `09:15:00` | `systemd` | Scheduled Task| `root` | N/A | Fired | `daily-report.timer` |
| `09:15:04` | `systemd` | Service | N/A | N/A | Started | `daily-report.service` |
| `09:17:20` | `sshd` | Authentication | `student` | `192.0.2.44` | Success | Method: Public Key |

---

## 3. Core Analytical Findings

### Finding 1: Authentication Anomaly from Unapproved Source IP
* **Observation:** Three consecutive failed authentication attempts were recorded from source IP `198.51.100.27` targeting accounts `admin`, `oracle`, and `student`. At `09:13:22`, account `student` successfully authenticated from that same IP via password.
* **Contextual Evaluation:** `case-context.md` explicitly lists `198.51.100.27` as an **unapproved administrative source**.
* **Analyst Assessment:** This pattern represents a credential-guessing/probing sequence followed by a successful login. However, this sequence alone does not prove account compromise; a legitimate user connecting off-site may have mistyped their password before gaining access.

### Finding 2: Read-Only Privilege Execution
* **Observation:** At `09:13:58`, user `student` executed `sudo systemctl status cron` from source IP `198.51.100.27`.
* **Analyst Assessment:** This command is an **informational, read-only status check**. It did not alter system configurations or edit cron files. While its timing warrants contextual review due to the preceding login anomaly, the action is not intrinsically malicious.

### Finding 3: Baseline-Compliant Scheduled Task Execution
* **Observation:** At `09:15:00`, `daily-report.timer` fired and executed `daily-report.service`.
* **Analyst Assessment:** This activity matches the established operational baseline in `case-context.md`. Its occurrence two minutes after the login is coincidental (**temporal proximity does not equal causation**).

### Finding 4: Approved Administrative Connection
* **Observation:** At `09:17:20`, user `student` successfully logged in via SSH public key from `192.0.2.44`.
* **Analyst Assessment:** This connection aligns perfectly with the approved administrative baseline defined in `case-context.md`.

---

## 4. Key Uncertainties & What Cannot Be Proven

1. **Identity Verification:** The logs cannot confirm the physical identity of the individual operating from `198.51.100.27`.
2. **Intent & Authorization:** The telemetry cannot determine whether the successful login from `198.51.100.27` was an authorized employee working remotely or an unauthorized actor.
3. **Session Linkage:** Lack of explicit SSH session IDs prevents verifying whether the `sudo` command was executed within the exact interactive session established at `09:13:22`.

---

## 5. Recommended Next Steps

1. **User Out-of-Band Verification:** Contact the owner of account `student` to confirm whether they initiated the connections from `198.51.100.27` at `09:12`–`09:13`.
2. **Session & History Audit:** Inspect endpoint shell history (`~student/.bash_history`) and auth log session IDs on `labhost`.
3. **Security Hardening:** Enforce Multi-Factor Authentication (MFA) across all SSH logins and restrict SSH access strictly to approved administrative subnet ranges.

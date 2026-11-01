# Day 11 - Incident Triage Report: Simulated Authentication & Persistence Investigation

## 1. Executive Summary
* **Incident ID:** INC-2026-1029-01
* **Date of Evaluation:** October 29, 2026
* **Investigator:** Junior Defensive Security Analyst (Serah Mulwa)
* **Summary:** A synthetic security event dataset simulating authentication attempts, administrative privilege escalation, and scheduled tasks was ingested and analyzed using a custom Python parsing script (`log_parser.py`). The investigation established a baseline timeline of events involving multiple failed root login attempts followed by a successful administrative login, sudo execution, and cron job scheduling. Based on log telemetry and known environment parameters, no definitive indicator of unauthorized compromise was identified; however, anomalous credential-probing patterns require ongoing monitoring.

## 2. Scope & Environment
* **Target System:** Simulated Linux Lab Host (`labhost`)
* **Data Sources:** Structured JSON security event logs (`day-11/logs.json`)
* **Time Range Inspected:** 2026-10-29T08:12:01+03:00 to 2026-10-29T08:20:00+03:00
* **Operational Constraints:** Analysis conducted under local unprivileged viewing scope. Raw log contents sanitized to exclude sensitive organizational identifiers.

## 3. Chronological Event Timeline

| Timestamp | Source Service | Event Type | User | Source IP / Target | Outcome / Details |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **08:12:01** | `sshd` | Authentication | `root` | `192.168.1.50` | **Failed:** Password authentication rejected. |
| **08:12:03** | `sshd` | Authentication | `root` | `192.168.1.50` | **Failed:** Repeated password rejection from same source. |
| **08:15:22** | `sshd` | Authentication | `admin` | `10.0.0.15` | **Success:** Valid administrative login established. |
| **08:16:05** | `sudo` | Privilege Escalation | `admin` | Localhost | **Allowed:** Executed `/usr/bin/apt-get update`. |
| **08:20:00** | `cron` | Scheduled Task | `root` | Localhost | **Executed:** Triggered `/usr/local/bin/triage_sync.sh`. |

## 4. Analytical Findings & Correlation
* **Observation 1 (Credential Probing):** Two rapid failed root authentication attempts originated from external IP `192.168.1.50`. This pattern is characteristic of automated brute-force scanning or credential guessing.
* **Observation 2 (Legitimate Administrative Access):** A successful login for user `admin` occurred shortly after from IP `10.0.0.15`. When cross-referenced against local lab baseline notes, `10.0.0.15` is identified as an approved internal administrative connection.
* **Observation 3 (Post-Login Activity):** The authenticated `admin` user successfully executed package update commands via `sudo`, followed by a routine system maintenance cron script executing under root privileges.

## 5. Alternative Explanations
* **Hypothesis A (Compromise):** An attacker successfully guessed the root password and established persistence via cron. *(Refuted: Root login attempts failed entirely; successful authentication utilized a distinct user account (`admin`) from a trusted internal IP `10.0.0.15`).*
* **Hypothesis B (Routine Admin Activity with Background Noise):** The server experienced generic internet-facing brute-force noise (common for exposed SSH daemons) while a legitimate administrator concurrently performed routine maintenance and system updates. *(Supported by log metrics and baseline IP correlation).*

## 6. Limitations
* **Incomplete Visibility:** The available log dataset only captures SSH, sudo, and cron events. It does not provide full endpoint memory acquisition, network packet captures (PCAP), or file integrity checksum verification.
* **No Malware Verdict:** Analysis of log telemetry alone cannot verify whether binaries executed on disk contained malicious payloads.

## 7. Conclusion & Recommendations
* **Conclusion:** The available evidence indicates standard administrative maintenance coinciding with external scanning noise. No definitive breach or unauthorized execution was proven.
* **Recommendations:**
  1. Implement fail2ban or disable password-based SSH authentication in favor of SSH cryptographic key pairs.
  2. Audit cron job scripts in `/usr/local/bin/` to verify file integrity and strict permission controls.
  3. Maintain continuous SIEM log aggregation for anomaly detection.

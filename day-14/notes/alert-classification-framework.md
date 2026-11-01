# Deep Dive: SOC Alert Classification Framework & Analyst Verdicts

## 1. Executive Summary & Context

Assigning an investigative verdict to a SIEM or EDR alert is the primary operational outcome for Level 1 Security Operations Center (SOC) analysts. Alert classification bridges raw detection triggers and actionable security intelligence.

Accurate classifications provide critical operational metrics that directly impact:
* **Detection Engineering:** Identifying noisy or broken rules requiring tuning, whitelisting, or signature modification.
* **Threat Hunting & DFIR:** Establishing historical IoC correlation baselines across enterprise endpoints.
* **Metrics & Compliance:** Measuring SOC performance indicators such as Mean Time to Detect (MTTD), Mean Time to Resolve (MTTR), and overall signal-to-noise ratios.

---

## 2. Deep-Dive Verdict Classifications & Examples

### 2.1 True Positive (TP) - *Confirmed Malicious Activity*

* **Definition:** The detection rule correctly identified activity that is genuinely malicious, unauthorized, or violates enterprise security policy, supported by secondary investigation evidence.
* **Analyst Action:** Immediate isolation, ticket escalation to Tier 2 Incident Response, and execution of containment playbooks.
* **Enterprise Example:** A SIEM alert fires for `Repeated Failed Logons Followed by Success`. Log correlation reveals 15 password attempts from external IP `185.220.101.5` (Tor exit node), followed by a successful login to user `j.doe`, and an immediate PowerShell command executing an encoded web-c2 downloader script.

---

### 2.2 False Positive (FP) - *Misinterpreted / Broken Detection Logic*

* **Definition:** The detection system flagged legitimate, harmless activity as malicious because the detection logic, threshold, or regular expression was overly broad, noisy, or flawed.
* **Analyst Action:** Close ticket as False Positive; submit a rule-tuning request to the Detection Engineering team with specific context exclusions.
* **Enterprise Example:** An alert triggers for `Suspicious PowerShell Encoded Command Execution`. Investigation reveals the script was launched locally by an enterprise MDM solution (e.g., Microsoft Intune) to deploy a routine software patch using standard base64 encoding.

---

### 2.3 Benign Positive (BP) - *Authorized / Safe Match*

* **Definition:** The alert triggered accurately based on the rule parameters, and the event genuinely occurred, but the activity was fully authorized, scheduled, or performed by approved personnel.
* **Analyst Action:** Verify authorization records (Change Management Tickets, Pentest notifications), link approval details, and close ticket.
* **Enterprise Example:** An alert fires for `Port Scanning and Credential Spraying`. Log correlation shows the source IP belongs to the internal vulnerability scanner (`10.0.50.25`), performing a scheduled weekly vulnerability audit authorized under Change Request `CHG-2026-881`.

---

### 2.4 Inconclusive - *Insufficient Telemetry / Evidence*

* **Definition:** Available log data, endpoint telemetry, or network traffic records are insufficient to confirm whether the activity was malicious or benign.
* **Analyst Action:** Document missing telemetry sources, preserve volatile data where possible, and escalate to Tier 2 for advanced host forensics or network packet capture review.
* **Enterprise Example:** An alert flags a single DNS query to an unrated domain. Endpoint logs are missing due to log forwarder service failure on the workstation, and network proxy logs were purged. It is impossible to verify which process initiated the connection or if malicious payloads were transferred.

---

### 2.5 Duplicate (DUP) - *Correlated Event / Existing Ticket*

* **Definition:** The alert represents the exact same underlying event or activity stream that is already actively tracked in another ticket or master incident record.
* **Analyst Action:** Link the duplicate alert to the master Incident Ticket ID and close out the redundant queue entry.
* **Enterprise Example:** Three separate alerts fire concurrently: `Suspicious Email Attachment Opened`, `Process Spawned from Outlook`, and `Outbound Connection to Suspicious IP`. All three reference host `FIN-WORKSTATION-02` at 14:02 UTC and are linked to an active Incident Ticket `#INC-9942`.

---

### 2.6 False Negative (FN) - *Missed Threat (Retrospective)*

* **Definition:** Malicious activity occurred within the environment but was completely missed by detection rules and security controls (no alert generated).
* **Identification:** Discovered retrospectively via threat hunting hypotheses, external breach notifications, or proactive red team simulations rather than standard queue triage.

---

## 3. Comparative Verdict Matrix

| Classification Verdict | Did the activity occur? | Was it malicious / unauthorized? | Did the detection engine function correctly? | Operational Handling |
| :--- | :--- | :--- | :--- | :--- |
| **True Positive (TP)** | Yes | **Yes** | Yes | Escalate to Incident Response; isolate host. |
| **False Positive (FP)** | No (misidentified) | No | **No (Rule Flawed)** | Close ticket; submit rule-tuning request. |
| **Benign Positive (BP)** | **Yes** | No (Authorized) | **Yes** | Close ticket; attach change ticket reference. |
| **Inconclusive** | Unknown | Unknown | Unknown | Escalate for deeper forensic review. |
| **Duplicate (DUP)** | Yes | Same as parent | N/A | Link to existing ticket; close duplicate. |

---

## 4. Analyst Golden Rules & Best Practices

1. **Never Force a Verdict:** Do not default to labeling an alert as False Positive or True Positive simply to close a ticket faster or meet dashboard expectations.
2. **Document Inconclusive Data Clearly:** If log telemetry is missing, state explicitly what data source was unavailable (e.g., *"Sysmon Event ID 1 logs missing for host WS-01"*).
3. **Always Attach Proof:** Every closed ticket must contain supporting Splunk SPL/grep query outputs, timestamp markers, and verified hash/IP reputations.
4. **Differentiate FP and BP:** False Positives indicate a rule flaw; Benign Positives indicate authorized activity. Conflating the two damages detection engineering metrics.

---

## 5. Standardized Ticket Closure Documentation Template

```markdown
### SOC TICKET CLOSURE SUMMARY

**Ticket ID:** ALT-2026-1104-99
**Analyst:** Level 1 SOC Analyst
**Timestamp:** 2026-11-01 22:45:00 UTC

#### 1. Verdict & Classification
- **Final Verdict:** BENIGN POSITIVE (BP)
- **Target Asset:** `LINUX-LAB-01` (10.0.4.15)
- **Associated Identity:** `root`

#### 2. Investigative Evidence
- Verified source IP `192.168.1.50` belongs to internal admin workstation.
- Cross-referenced execution timestamp against Change Management System: Matched authorized maintenance window `CHG-88421`.

#### 3. Resolution & Next Steps
- Closed ticket as Benign Positive.
- No further incident escalation required.
```

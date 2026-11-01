# Day 13 - Detection Engineering Fundamentals, Tuning, and Logic Design

* **Author:** Serah Mulwa

* **Date:** October 31, 2026

* **Module:** SIEM Fundamentals & Detection Engineering

* **Target Audience:** Tier 1 SOC Analysts & Junior Detection Engineers

## 1. What is Detection Engineering?

**Detection engineering** is the systematic discipline of designing, building, testing, maintaining, and refining the logic—such as SIEM queries, Sigma rules, or heuristic scripts—that identifies potentially malicious or suspicious behavior across enterprise telemetry.

A detection rule is an automated hypothesis: *"If specific indicators (X, Y, Z) occur within a defined time frame, flag the activity as a high-risk security alert for human investigation."*

## 2. The 8 Pillars of a Well-Designed Detection

Writing a robust detection rule involves much more than throwing together a quick conditional statement. Every production-grade detection must address 8 critical design questions:

1. **What behavior are we trying to identify?** (e.g., credential stuffing, lateral movement via WMI, unauthorized persistence mechanism creation).
2. **Which logs contain the necessary information?** (e.g., Windows Security Event ID 4625, Linux `/var/log/auth.log`, firewall traffic logs).
3. **Are those logs reliably collected?** (Ensuring the log forwarder is active and not dropping packets or experiencing queue congestion).
4. **Which fields are required?** (e.g., `TargetUserName`, `IpAddress`, `LogonType`, `_time`).
5. **What rule should be applied?** (The mathematical threshold or temporal correlation logic).
6. **What legitimate activities might trigger it?** (Sysadmins resetting passwords, developers using automated scripts, users with 'fat fingers').
7. **How should the rule be tested?** (Using synthetic test harnesses, atomic red team tests, or historical baselines).
8. **What should an analyst investigate next?** (The exact triage playbook steps: check endpoint process tree, verify IP geo-location, interview the user).

## 3. False Positives vs. False Negatives

### 3.1 False Positives (The Noise Problem)
* **Definition:** A **False Positive (FP)** occurs when a detection rule triggers an alert on completely legitimate, benign user or system activity.
* **Real-World Example:** An executive makes three typos entering their password after returning from lunch, then successfully logs in. Your brute-force detection rule triggers because it saw $\ge 3$ failures followed by a success.
* **The Impact:** **Alert Fatigue**. If an analyst receives 500 alerts a day and 490 of them are false positives, they will eventually ignore alerts entirely—allowing real attacks to slip through unnoticed.
* **How to Fix It (Tuning):** Adjust thresholds, add authorized administrative source IP whitelists (e.g., internal jump boxes), or exclude known service accounts.

### 3.2 False Negatives (The Blind Spot Problem)
* **Definition:** A **False Negative (FN)** occurs when an actual malicious attack takes place, but your detection rule fails to trigger or alert on it.
* **Real-World Example:** An attacker executes a password spraying attack against a Linux server, but your detection rule only monitors Windows Event logs (`Event ID 4625`) and completely ignores Linux SSH syslogs.
* **The Impact:** Complete compromise goes undetected while the security team assumes the network is secure.
* **How to Fix It (Tuning):** Expand log coverage, normalize logs into a unified schema (CIM), and write cross-platform correlation rules.

## 4. Detection Thresholds & Tuning

A **Threshold** is the numerical or temporal limit that determines when an event pattern crosses from "normal noise" into "suspicious behavior requiring human review."

* *Example 1:* 3 failed logins within 10 minutes.
* *Example 2:* 5 failed logins within 15 minutes across different subnets.

### The Tuning Dilemma
There is **no universally correct threshold**. Every organization has a unique operational baseline:
* **Too Sensitive (Low Threshold):** Generates excessive false positives and crushes SOC efficiency with alert fatigue.
* **Too Relaxed (High Threshold):** Generates zero false positives, but completely misses slow-and-low attacks (like credential stuffing spaced out over hours).

## 5. What to Document & What I Must Remember

### What to Document in Detection Engineering Reports
1. **Detection Hypothesis:** Clearly state what threat vector the rule is designed to catch.
2. **Known False Positive Vectors:** Document legitimate administrative behaviors that might mimic the attack.
3. **Tuning History:** Record why specific thresholds (e.g., threshold=3, window=10 minutes) were chosen.

### What I Must Remember
* *Detection engineering is an iterative process.* No rule is perfect on day one; rules require continuous tuning based on environmental feedback.
* *Context is king.* An alert is never proof of a compromise on its own—it is simply a signal requiring structured human investigation and triage.

## 6. How It Is Applied in the Job Market

During interviews for **Security Engineer** or **Detection Engineer** roles, hiring managers will ask: *"How do you handle high false-positive rates on a noisy detection rule?"*
Your structured answer:
> *"First, I review historical alert data to identify the root cause of the noise—whether it's automated service accounts or user typos. Second, I tune the rule by refining thresholds, adding exception filters for approved administrative IPs, or enriching the event with context before alerting. Finally, I validate the tuned rule against historical telemetry to ensure we haven't introduced false negatives."*
